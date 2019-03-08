(function($){

  var ExaminationEditForm = function(form) {
    this.form = $(form);
    this.setup();
  }

  ExaminationEditForm.prototype = {
    setup: function() {
      this.saveBar = this.form.find('.sticky-save');
      this.hasChanges = false;
      this.initialiseInputs();
    },

    initialiseInputs: function() {
      var inputs = this.form.find('input');
      for (var i = 0; i < inputs.length; i++) {
        new Input(inputs[i], this.handleChange.bind(this));
      }
    },

    handleChange: function() {
      this.hasChanges = true;
      this.showSave();
    },

    showSave: function() {
      this.saveBar.show();
    }
  }

  var Input = function(input, changeCallback) {
    this.input = $(input);
    this.changeCallback = changeCallback;
    this.setup();
  }

  Input.prototype = {
    setup: function() {
      this.startWatchers();
    },

    startWatchers: function() {
      this.input.change(this.changeCallback);

      this.input.on('input', this.changeCallback);
    }
  }

  function init(){
    var examinationsForms = $('#examination__edit--form');
    for (var i = 0; i < examinationsForms.length; i++) {
      new ExaminationEditForm(examinationsForms[i]);
    }
  }

  $(document).on('page:load', init);
  $(init)
}(jQuery))
