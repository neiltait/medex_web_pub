(function ($) {

  var MedicalTeamPage = function (wrapper) {
    this.wrapper = $(wrapper);
    this.setup();
  }

  MedicalTeamPage.prototype = {
    setup: function () {
      this.saveBar = this.wrapper.find('.sticky-save');
      this.form = this.wrapper.find('form');
      this.hasChanges = false;
      this.tabChangeModal = new ChangeTabModal($('#tab-change-modal'), this.forceSave.bind(this));
      this.initialiseTabs();
      this.initialiseInputs();
      this.setupAdditionalNotes();
      this.setupAddRemovePanels();
    },

    initialiseTabs: function () {
      this.tabBlock = new TabBlock(this.wrapper.find('.examination__tab-bar'), this.getHasChanges.bind(this), this.tabChangeModal);
    },

    setupAdditionalNotes() {
      var additionalNotesFields = $('.additional-notes');
      for (var i = 0; i < additionalNotesFields.length; i++) {
        new AdditionalNotesSection(additionalNotesFields[i]);
      }
    },

    setupAddRemovePanels() {
      var addRemovePanelSection = $('#add-remove-panel-section');
      var consultantCount = $('#consultant-count').val();
      var optionalConsultantCount = consultantCount && parseInt(consultantCount) > 1 ? parseInt(consultantCount) - 1 : 0;

      new AddRemovePanelList(addRemovePanelSection, optionalConsultantCount)
    },

    initialiseInputs: function () {
      var inputs = this.wrapper.find('input');
      for (var i = 0; i < inputs.length; i++) {
        new Input(inputs[i], this.handleChange.bind(this));
      }

      var selects = this.wrapper.find('select');
      for (var i = 0; i < selects.length; i++) {
        new Input(selects[i], this.handleChange.bind(this));
      }

      var textAreas = this.wrapper.find('textarea');
      for (var i = 0; i < textAreas.length; i++) {
        new Input(textAreas[i], this.handleChange.bind(this));
      }
    },

    getHasChanges: function() {
        return this.hasChanges;
    },

    forceSave: function (nextTab) {
      this.form[0].action += '?nextTab=' + nextTab;
      this.form.submit();
    },

    handleChange: function () {
      this.hasChanges = true;
      this.showSave();
    },

    showSave: function () {
      this.saveBar.show();
    }
  }

  function init() {
    var medicalTeamPage = $('.examination__edit');
    for (var i = 0; i < medicalTeamPage.length; i++) {
      new MedicalTeamPage(medicalTeamPage[i]);
    }
  }


  $(document).on('page:load', init);
  $(init)
}(jQuery))
