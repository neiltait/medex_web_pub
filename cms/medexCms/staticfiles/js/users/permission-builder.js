(function($){

  var PermissionBuilderForm = function(form) {
    this.form = $(form);
    this.setup();
  }

  PermissionBuilderForm.prototype = {
    setup: function() {
      this.regionSelector = this.form.find('#region-selector');
      this.trustSelector = this.form.find('#trust-selector');
      this.addAnotherInput = this.form.find('input[name=add_another]')
      this.addAnotherButton = this.form.find('#add-another');
      this.setupLevelRadios();
      this.setupRoleRadios();
      this.startClickWatcher();
    },

    setupRoleRadios: function() {
      this.roleRadios = new RadioGroup(this.form.find('#role-radio-buttons'), this.handleRoleChange.bind(this));
      if (this.roleRadios.selected()) {
        this.handleRoleChange();
      }
    },

    setupLevelRadios: function() {
      this.levelRadios = new RadioGroup(this.form.find('#level-radio-buttons'), this.handleLevelChange.bind(this));
      if (this.levelRadios.selected()) {
        this.handleLevelChange(this.levelRadios.selected());
      }
    },

    handleRoleChange: function(target) {
      this.levelRadios.show();
    },

    handleLevelChange: function(selectedLevel) {
      console.log(selectedLevel)
      if (selectedLevel === 'regional') {
        this.trustSelector.hide();
        this.regionSelector.show();
      } else if (selectedLevel === 'trust') {
        this.trustSelector.show();
        this.regionSelector.hide();
      } else {
        this.trustSelector.hide();
        this.regionSelector.hide();
      }
    },

    startClickWatcher: function() {
      var that = this;
      this.addAnotherButton.click(function(e) {
        e.preventDefault();
        that.addAnotherInput[0].value = 'true';
        that.form.submit();
      })
    }
  }

  var RadioGroup = function(wrapper, changeCallback) {
    this.wrapper = wrapper;
    this.changeCallback = changeCallback;
    this.setup();
  }

  RadioGroup.prototype = {
    setup: function() {
      this.radios = this.wrapper.find('input[type=radio]');
      this.startWatchers();
    },

    startWatchers: function() {
      var that = this;
      for (var i = 0; i < this.radios.length; i++) {
        $(this.radios[i]).change(function(e) {
          that.changeCallback(e.target.value);
        });
      }
    },

    show: function() {
      this.wrapper.show();
    },

    selected: function() {
      var optionSelected = null;
      for (var i = 0; i < this.radios.length; i++) {
        if (this.radios[i].checked) {
          optionSelected = this.radios[i].value;
        }
      }
      return optionSelected;
    }
  }

  function init(){
    var permissionForms = $('#permission-builder-form');
    for (var i = 0; i < permissionForms.length; i++) {
      new PermissionBuilderForm(permissionForms[i]);
    }
  }

  $(document).on('page:load', init);
  $(init)
}(jQuery))
