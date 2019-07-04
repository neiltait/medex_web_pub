var AddRemovePanelList = function (section, visibleCount) {
    this.visibleCount = visibleCount;
    this.panels = section.find('.add-remove-panel');
    this.addButton = section.find('.add-panel-button');
    this.removeButton = section.find('.remove-panel-button');
    this.setup();
};

AddRemovePanelList.prototype = {
    setup: function () {
        let that = this;
        this.addButton.on('click', function (event) {
            event.preventDefault();
            that.addButton.blur();
            if (that.visibleCount < that.panels.length) {
                that.visibleCount += 1;
                that.refreshVisible();
            }
        });

        this.removeButton.on('click', function (event) {
            event.preventDefault();
            that.removeButton.blur();
            if (that.visibleCount > 0) {
                that.visibleCount -= 1;
                that.refreshVisible();
            }
        });
        this.refreshVisible();
    },

    refreshVisible: function() {
        this.refreshVisiblePanels();
        this.refreshVisibleButtons();
    },

    refreshVisiblePanels: function() {
        for (i = 0; i < this.panels.length; i += 1) {
            if (i < this.visibleCount) {
                this.panels[i].classList.remove("medex-hidden");
            } else {
                this.panels[i].classList.add("medex-hidden");
                $(this.panels[i]).find("input").val("");

            }
        }
    },

    refreshVisibleButtons: function() {
        if (this.visibleCount === 0) {
            this.removeButton.addClass("medex-hidden");
        } else {
            this.removeButton.removeClass("medex-hidden");
        }

        if (this.visibleCount === this.panels.length) {
            this.addButton.addClass("medex-hidden");
        } else {
            this.addButton.removeClass("medex-hidden");
        }
    }
};