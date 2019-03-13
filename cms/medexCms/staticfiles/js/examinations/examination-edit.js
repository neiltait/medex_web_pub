(function ($) {

  var ExaminationEditForm = function (form) {
    this.form = $(form);
    this.setup();
  }

  ExaminationEditForm.prototype = {
    setup: function () {
      this.saveBar = this.form.find('.sticky-save');
      this.hasChanges = false;
      this.hasErrors = this.form[0].dataset.errorCount > 0;
      this.initialiseInputs();
      this.initialiseTabs();
      this.tabChangeModal = new ChangeTabModal($('#tab-change-modal'), this.forceSave.bind(this));
      this.setupAdditionalNotes();
      this.setupAddRemoveItemSections();
      this.setInitialView();
    },

    setInitialView: function() {
      if (location.search && this.hasErrors) {
        var paramsJSON = this.decodeQueryParams(location.search.substr(1));
        this.showTab(paramsObject['previousTab']);
        window.history.replaceState({}, document.title, location.origin + location.pathname);
      }
      else if (location.hash) {
        this.showTab(location.hash.substr(1));
        window.history.replaceState({}, document.title, location.origin + location.pathname);
      }
    },

    decodeQueryParams: function(params) {
      var pairs = params.split('&');
      paramsObject = {};
      pairs.forEach(function(pair) {
        var key = pair.split('=')[0];
        var value = pair.split('=')[1];
        paramsObject[key] = value;
      });
      return paramsObject
    },

    initialiseTabs: function () {
      this.tab1 = this.form.find('#patient-details-tab');
      this.tab2 = this.form.find('#medical-team-tab');
      this.tab3 = this.form.find('#case-breakdown-tab');
      this.tab4 = this.form.find('#case-outcomes-tab');
      this.section1 = this.form.find('#patient-details-section');
      this.section2 = this.form.find('#medical-team-section');
      this.section3 = this.form.find('#case-breakdown-section');
      this.section4 = this.form.find('#case-outcomes-section');
      let that = this;
      this.tab1.click(function () {
        that.showTab("patient-details")
      });
      this.tab2.click(function () {
        that.showTab("medical-team")
      });
      this.tab3.click(function () {
        that.showTab("case-breakdown")
      });
      this.tab4.click(function () {
        that.showTab("case-outcomes")
      });
    },

    setupAdditionalNotes() {
      var additionalNotesFields = $('.additional-notes');
      for (var i = 0; i < additionalNotesFields.length; i++) {
        new AdditionalNotesSection(additionalNotesFields[i]);
      }
    },

    setupAddRemoveItemSections() {
      var addRemoveItemSections = $('.add-remove-item-section')
      for (var i = 0; i < addRemoveItemSections.length; i++) {
        new AddRemoveItemSection(addRemoveItemSections[i]);
      }
    },

    showTab: function (tabId) {
      if (this.hasChanges) {
        var currentTab = this.form.find('.tab-item.active')[0].id.slice(0, -4);
        this.tabChangeModal.show(tabId, currentTab);

      } else {
        for (tab of [this.tab1, this.tab2, this.tab3, this.tab4]) {
          if (tab[0].id === tabId + "-tab") {
            tab.addClass("active");
          } else {
            tab.removeClass("active");
          }
        }

        for (section of [this.section1, this.section2, this.section3, this.section4]) {
          if (section[0].id === tabId + "-section") {
            section.removeClass("medex-hidden");
          } else {
            section.addClass("medex-hidden");
          }
        }
      }
    },

    initialiseInputs: function () {
      var inputs = this.form.find('input');
      for (var i = 0; i < inputs.length; i++) {
        new Input(inputs[i], this.handleChange.bind(this));
      }

      var selects = this.form.find('select');
      for (var i = 0; i < selects.length; i++) {
        new Input(selects[i], this.handleChange.bind(this));
      }

      var textAreas = this.form.find('textarea');
      for (var i = 0; i < textAreas.length; i++) {
        new Input(textAreas[i], this.handleChange.bind(this));
      }
    },

    forceSave: function(currentTab, nextTab) {
      this.form[0].action += '?previousTab=' + currentTab + '#' + nextTab;
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

  var ChangeTabModal = function(modal, saveCallBack) {
    this.modal = $(modal);
    this.saveCallBack = saveCallBack;
    this.setup();
  }

  ChangeTabModal.prototype = {
    setup: function() {
      this.saveButton = this.modal.find('#save-continue');
      this.discardButton = this.modal.find('#discard');
      this.startWatchers();
    },

    startWatchers: function() {
      var that = this;

      this.saveButton.click(function() {
        that.saveCallBack(that.currentTab, that.nextTab);
      });

      this.discardButton.click(function() {
        window.location.hash = that.nextTab;
        location.reload();
      });
    },

    show: function(nextTab, currentTab) {
      this.currentTab = currentTab;
      this.nextTab = nextTab;
      this.modal.show();
    }
  }


  var AdditionalNotesSection = function (section) {
    this.section = $(section);
    this.setup();
  };

  AdditionalNotesSection.prototype = {
    setup: function () {
      this.button = this.section.find('.additional-notes-button');
      this.panel = this.section.find('.additional-notes-panel');

      let that = this
      this.button.on('click', function (event) {
        event.preventDefault()
        that.panel.removeClass("medex-hidden")
        that.button.addClass("medex-hidden")
      })
    },
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
      this.addButton.on('click', function(event) {
        event.preventDefault();
        that.show()
      });
      this.removeButton.on('click', function(event) {
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
    var examinationsForms = $('#examination__edit--form');
    for (var i = 0; i < examinationsForms.length; i++) {
      new ExaminationEditForm(examinationsForms[i]);
    }
  }


  $(document).on('page:load', init);
  $(init)
}(jQuery))
