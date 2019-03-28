(function ($) {

    var EventEntryArea = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    EventEntryArea.prototype = {
        setup: function() {
            this.picker = this.wrapper.find('#event-form-picker');
            this.text = this.wrapper.find('#hidden-text');
            this.forms = {};
            this.activeForm = null;

            this.initialiseForms();
            this.startWatcher();
        },

        initialiseForms: function() {
            var forms = this.wrapper.find('.event-form');
            for (var i = 0; i < forms.length; i++) {
                var hintID = forms[i].id + '-hint';
                var hint = this.wrapper.find('#' + hintID)
                this.forms[forms[i].id] = new EventForm(forms[i], hint);
            }
        },

        initialiseHintSections: function() {
            var hints = this.wrapper.find('.event-hints');
            for (var i = 0; i < forms.length; i++) {
                this.forms[forms[i].id] = new EventForm(forms[i]);
            }
        },

        startWatcher: function() {
            var that = this;
            this.picker.change(function(e) {
                that.forms[that.picker[0].value].show();
                that.hideOtherForms(that.picker[0].value);
                that.text.show();
            });
        },

        hideOtherForms: function(selectedKey) {
            if (this.activeForm) {
                this.forms[this.activeForm].hide();
                this.activeForm = selectedKey;
            } else {
                this.activeForm = selectedKey;
            }
        }
    }

    var EventForm = function(form, hint) {
        this.form = $(form);
        this.hint = $(hint);
        this.setup();
    }

    EventForm.prototype = {
        setup: function() {
            this.inputs = this.form.find('input');
        },

        show: function() {
            this.form.show();
            this.hint.show();
        },

        hide: function() {
            this.form.hide();
            this.hint.hide();
        }
    }




    function init() {
        var eventEntry = $('.case-event-forms');
        for (var i = 0; i < eventEntry.length; i++) {
            new EventEntryArea(eventEntry[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
