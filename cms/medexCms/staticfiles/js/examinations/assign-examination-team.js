(function ($) {

    var AssignExaminationTeam = function (wrapper, saveBtn, modalSaveBtn) {
        this.wrapper = $(wrapper);
        this.saveBtn = saveBtn;
        this.modalSaveBtn = modalSaveBtn;
        this.setup();
    }

    AssignExaminationTeam.prototype = {
        setup: function () {
            this.isOpen = false;
            this.meSelect = this.wrapper.find('#medical_examiner');
            this.meoSelect = this.wrapper.find('#medical_examiners_officer');
            this.confirmSection = this.wrapper.find('#confirm-section');
            this.confirmYes = this.wrapper.find('#confirm-yes');
            this.confirmNo = this.wrapper.find('#confirm-no');
            this.confirmMessage = this.wrapper.find('#confirm-message');

            this.savedMe = this.meSelect.val();
            this.savedMeo = this.meoSelect.val();

            this.continueBtn = this.wrapper.find('#assign-team-btn');
            this.startWatchers();
        },

        startWatchers: function () {
            var that = this;
            this.meSelect.change(function () {
                that.onDropdownChange()
            });

            this.meoSelect.change(function () {
                that.onDropdownChange()
            });

            this.confirmYes.click(function () {
                that.activateConfirmBtn()
            });
            this.confirmNo.click(function () {
                that.activateConfirmBtn()
            });

            this.continueBtn.click(function (event) {
                that.onClickContinue()
            })
        },

        onDropdownChange: function () {
            if (this.savedMe !== this.meSelect.val() || this.savedMeo !== this.meoSelect.val()) {
                this.confirmSection.removeClass("nhsuk-u-visually-hidden")
                this.confirmMessage.html(this.getConfirmationMessage());
                this.clearConfirmation();
                this.saveBtn.addClass("submit-btn--disabled")
                this.modalSaveBtn.addClass("submit-btn--disabled")
            } else {
                this.closeExaminationTeamEdit()
            }
        },

        closeExaminationTeamEdit: function () {
            this.savedMe = this.meSelect.val();
            this.savedMeo = this.meoSelect.val();

            this.confirmSection.addClass("nhsuk-u-visually-hidden")
            this.saveBtn.removeClass("submit-btn--disabled")
            this.modalSaveBtn.removeClass("submit-btn--disabled")
        },

        onClickContinue: function () {
            event.preventDefault();
            if (this.confirmNo.is(":checked")) {
                this.meSelect.val(this.savedMe);
                this.meoSelect.val(this.savedMeo);
            }
            this.closeExaminationTeamEdit()
        },

        activateConfirmBtn: function () {
            this.continueBtn.removeClass("nhsuk-button--disabled")
        },

        clearConfirmation: function () {
            this.confirmYes.prop("checked", false);
            this.confirmNo.prop("checked", false);
            this.continueBtn.addClass("nhsuk-button--disabled")
        },

        getConfirmationMessage: function() {
            if(this.savedMe === this.meSelect.val()) {
                return this.onePersonMessage(this.getMeoName())
            } else if (this.savedMeo === this.meoSelect.val()) {
                return this.onePersonMessage(this.getMeName())
            } else {
                return this.twoPeopleMessage(this.getMeoName(), this.getMeName())
            }
        },

        getMeName: function() {
            return this.wrapper.find("#medical_examiner option:selected").html();
        },
        getMeoName: function() {
            return this.wrapper.find("#medical_examiners_officer option:selected").html();
        },
        onePersonMessage: function(person) {
            return "Are you sure you would like to assign <strong>" + person + "</strong> to this case?"
        },
        twoPeopleMessage: function (person1, person2) {
            return "Are you sure you would like to assign <strong>" + person1 + "</strong> and <strong>" + person2 + "</strong> to this case?"
        }

    };

    function init() {
        var assignTeamForm = $('#examination__examination-team-section');
        var saveBtn = $('#save-btn');
        var modalSaveBtn = $('#save-continue');
        for (var i = 0; i < assignTeamForm.length; i++) {
            new AssignExaminationTeam(assignTeamForm[i], saveBtn, modalSaveBtn);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
