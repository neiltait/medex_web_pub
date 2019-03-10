(function ($) {

    var SecondaryInfoForm = function (form) {
        this.form = $(form);
        this.setup();
    }

    SecondaryInfoForm.prototype = {
        setup: function () {
            this.personalEffectsGroup = new AdditionalInfoGroup(this.form.find('#implant-devices'), 'yes');
            this.personalEffectsGroup = new AdditionalInfoGroup(this.form.find('#personal-effects'), 'yes');
        }
    }

    var AdditionalInfoGroup = function (group, showValue) {
        this.group = $(group);
        this.showValue = showValue;
        this.setup();
    }

    AdditionalInfoGroup.prototype = {
        setup: function () {
            this.radios = this.group.find('input[type=radio]');
            this.additionalInfoArea = this.group.find('.additional-info');
            this.startWatcher();
        },

        startWatcher: function () {
            var that = this;

            this.radios.change(function(e) {
              if (e.target.value === that.showValue) {
                that.additionalInfoArea.show();
              } else {
                that.additionalInfoArea.hide();
              }
            });
        }
    }

    function init() {
        var secondaryInfoForms = $('.secondary-info-form');
        for (var i = 0; i < secondaryInfoForms.length; i++) {
            new SecondaryInfoForm(secondaryInfoForms[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
