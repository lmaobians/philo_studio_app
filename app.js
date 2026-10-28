const { createApp } = Vue;

createApp({
  data() {
    return {
      hasActiveSession: false,
      activeSession: null,
      photos: [],
      templates: [],
      assignments: {},
      offsets: {},
      gridOrientations: {},
      currentActiveKey: null,
      activePhoto: null,
      showStaffModal: false,

      // History Stacks for Undo / Redo
      history: [],
      historyIndex: -1,

      staffForm: {
        date_folder: 'OCT 28',
        client_name: 'BIANCA',
        selected_package: 'SOLO'
      }
    };
  },
  computed: {
    canUndo() {
      return this.historyIndex > 0;
    },
    canRedo() {
      return this.historyIndex < this.history.length - 1;
    }
  },
  async mounted() {
    await this.fetchActiveSession();
  },
  methods: {
    async fetchActiveSession() {
      try {
        const res = await fetch('/api/client/active-session');
        const data = await res.json();

        if (data.has_active_session) {
          this.hasActiveSession = true;
          this.activeSession = data.session;
          this.photos = data.photos;
          this.templates = data.templates;

          if (this.templates.length > 0 && this.templates[0].slots.length > 0) {
            this.currentActiveKey = `${this.templates[0].id}_0`;
          }

          this.saveHistory();
        } else {
          this.hasActiveSession = false;
        }
      } catch (e) {
        console.error("Error fetching session:", e);
      }
    },

    saveHistory() {
      if (this.historyIndex < this.history.length - 1) {
        this.history = this.history.slice(0, this.historyIndex + 1);
      }
      this.history.push({
        assignments: JSON.parse(JSON.stringify(this.assignments)),
        offsets: JSON.parse(JSON.stringify(this.offsets)),
        gridOrientations: JSON.parse(JSON.stringify(this.gridOrientations))
      });
      this.historyIndex = this.history.length - 1;
    },

    undo() {
      if (this.canUndo) {
        this.historyIndex--;
        const state = this.history[this.historyIndex];
        this.assignments = JSON.parse(JSON.stringify(state.assignments));
        this.offsets = JSON.parse(JSON.stringify(state.offsets));
        this.gridOrientations = JSON.parse(JSON.stringify(state.gridOrientations || {}));
      }
    },

    redo() {
      if (this.canRedo) {
        this.historyIndex++;
        const state = this.history[this.historyIndex];
        this.assignments = JSON.parse(JSON.stringify(state.assignments));
        this.offsets = JSON.parse(JSON.stringify(state.offsets));
        this.gridOrientations = JSON.parse(JSON.stringify(state.gridOrientations || {}));
      }
    },

    async loadStaffSession() {
      if (!this.staffForm.date_folder || !this.staffForm.client_name) {
        alert("Please fill in both Date Folder and Client Name.");
        return;
      }

      try {
        const res = await fetch('/api/staff/load-session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.staffForm)
        });

        const data = await res.json();
        if (res.ok) {
          this.showStaffModal = false;
          await this.fetchActiveSession();
        } else {
          alert(`Error: ${data.detail}`);
        }
      } catch (e) {
        alert("Failed to connect to backend engine.");
      }
    },

    getSlotIndexKey(tplId, index) {
      return `${tplId}_${index}`;
    },

    setActiveSlot(tplId, index) {
      this.currentActiveKey = `${tplId}_${index}`;
    },

    assignPhotoToActiveSlot(filename) {
      this.activePhoto = filename;
      if (this.currentActiveKey) {
        this.assignments[this.currentActiveKey] = filename;
        if (this.offsets[this.currentActiveKey] === undefined) {
          this.offsets[this.currentActiveKey] = 0;
        }
        this.saveHistory();
      } else {
        alert("Please tap a photo slot on a template first!");
      }
    },

    adjustPhotoOffset(tplId, index, delta) {
      const key = `${tplId}_${index}`;
      const current = this.offsets[key] || 0;
      const newOffset = Math.max(-8, Math.min(8, current + delta));
      this.offsets[key] = newOffset;
      this.saveHistory();
    },

    getImageTransform(tplId, index) {
      const key = `${tplId}_${index}`;
      const offset = this.offsets[key] || 0;
      return { transform: `translate(0px, ${offset}px)` };
    },

    getGridOrientation(tplId) {
      return this.gridOrientations[tplId] || 'vertical';
    },

    setGridOrientation(tplId, orientation) {
      this.gridOrientations[tplId] = orientation;
      this.saveHistory();
    },

    getCanvasStyle(tpl) {
      const isHorizontal = this.getGridOrientation(tpl.id) === 'horizontal';
      const w = isHorizontal ? tpl.height_mm : tpl.width_mm;
      const h = isHorizontal ? tpl.width_mm : tpl.height_mm;
      return {
        width: `${w * 2.8}px`,
        height: `${h * 2.8}px`
      };
    },

    getActiveSlots(tpl) {
      if (!tpl.template_key.includes('grid')) {
        return tpl.slots;
      }

      const isHorizontal = this.getGridOrientation(tpl.id) === 'horizontal';
      if (!isHorizontal) {
        return tpl.slots;
      }

      const hSlots = [];
      for (let row = 0; row < 2; row++) {
        for (let col = 0; col < 4; col++) {
          hSlots.push({
            id: `slot_h_${row}_${col}`,
            x: 2 + (col * 36),
            y: 2 + (row * 47),
            width: 34,
            height: 45
          });
        }
      }
      return hSlots;
    },

    getSlotStyle(tpl, slot) {
      const isHorizontal = this.getGridOrientation(tpl.id) === 'horizontal';
      const canvasW = isHorizontal ? tpl.height_mm : tpl.width_mm;
      const canvasH = isHorizontal ? tpl.width_mm : tpl.height_mm;

      return {
        width: `${(slot.width / canvasW) * 100}%`,
        height: `${(slot.height / canvasH) * 100}%`,
        left: `${(slot.x / canvasW) * 100}%`,
        top: `${(slot.y / canvasH) * 100}%`
      };
    }
  }
}).mount('#app');