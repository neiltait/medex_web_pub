(function($){

  var PermissionBuilderForm = function(form) {
    this.form = $(form);
    this.setup();
  }

  PermissionBuilderForm.prototype = {
    setup: function() {
      this.roleRadios = new RadioGroup(this.form.find('#role-radio-buttons'), this.handleRoleChange.bind(this));
      this.levelRadios = new RadioGroup(this.form.find('#level-radio-buttons'), this.handleLevelChange.bind(this));
      this.regionSelector = this.form.find('#region-selector');
      this.trustSelector = this.form.find('#trust-selector');
      this.addAnotherInput = this.form.find('input[name=add_another]')
      this.addAnotherButton = this.form.find('#add-another');
      this.startClickWatcher();
    },

    handleRoleChange: function(target) {
      this.levelRadios.show();
    },

    handleLevelChange: function(target) {
      if (target.value === 'regional') {
        this.trustSelector.hide();
        this.regionSelector.show();
      } else if (target.value === 'trust') {
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
          that.changeCallback(e.target);
        });
      }
    },

    show: function() {
      this.wrapper.show();
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
