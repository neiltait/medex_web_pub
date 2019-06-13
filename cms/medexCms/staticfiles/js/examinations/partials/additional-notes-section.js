var AdditionalNotesSection = function (section) {
    this.section = $(section);
    this.setup();
};

AdditionalNotesSection.prototype = {
    setup: function () {
      this.button = this.section.find('.additional-notes-button');
      this.panel = this.section.find('.additional-notes-panel');
      this.notes = this.section.find('textarea');

      this.setupWatchers();

      this.openPopulatedPanelOnStartup()
    },

    setupWatchers: function() {
        let that = this;
        this.button.on('click', function (event) {
            event.preventDefault()
            that.openPanel()
        });
    },

    openPanel: function () {
        this.panel.removeClass("medex-hidden")
        this.button.addClass("medex-hidden")
    },

    openPopulatedPanelOnStartup: function () {
        if(this.notes.val() !== '') {
            this.openPanel()
        }
    }
};

