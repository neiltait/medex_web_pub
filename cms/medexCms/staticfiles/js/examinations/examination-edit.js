(function ($) {

  var ExaminationEditForm = function (wrapper) {
    this.wrapper = $(wrapper);
    this.setup();
  }

  ExaminationEditForm.prototype = {
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

  var Input = function (input, changeCallback) {
    this.input = $(input);
    this.changeCallback = changeCallback;
    this.setup();
  }

  Input.prototype = {
    setup: function () {
      this.startWatchers();
    },

    startWatchers: function () {
      this.input.change(this.changeCallback);

      this.input.on('input', this.changeCallback);
    }
  }

  var AddRemoveItemSection = function (section) {
    this.visible = false;
    this.section = $(section);
    this.setup();
  };

  AddRemoveItemSection.prototype = {
    setup: function () {
      this.panel = this.section.find('.add-remove-item-panel');
      this.addButton = this.section.find('.add-item-button');
      this.removeButton = this.section.find('.remove-item-button');

      let that = this;
      this.addButton.on('click', function (event) {
        event.preventDefault();
        that.show()
      });
      this.removeButton.on('click', function (event) {
        event.preventDefault();
        that.hide()
      });
    },
    show: function (event) {
      this.visible = true;
      this.panel.removeClass('medex-hidden')
      this.removeButton.removeClass('medex-hidden')
      this.addButton.addClass('medex-hidden')
    },
    hide: function (event) {
      this.visible = false;
      this.panel.addClass('medex-hidden')
      this.removeButton.addClass('medex-hidden')
      this.addButton.removeClass('medex-hidden')
    },
  }

  function init() {
    var examinationsForms = $('.examination__edit');
    for (var i = 0; i < examinationsForms.length; i++) {
      new ExaminationEditForm(examinationsForms[i]);
    }
  }


  $(document).on('page:load', init);
  $(init)
}(jQuery))
