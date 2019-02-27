(function($){

  var SearchDropdown = function(container) {
    this.container = $(container);
    this.minSearchTermLength = 3;
    this.setup()
  }

  SearchDropdown.prototype = {
    setup: function() {
      this.isSingleSelection = this.container[0].attributes.class.value.indexOf('multiple') === -1 ? true : false;
      this.selectionField = this.container.find('.selection-field')[0];
      this.searchField = $(this.container.find('input[name=searchField]'));
      this.optionList = $(this.container.find('.options-list'));
      console.info('Initialising search dropdown', this.container);
      this.initialiseOptions();
      this.watchForSearchTerm();
    },

    initialiseOptions: function() {
      this.options = []
      var options = this.optionList.find('option');
      for (var i = 0; i < options.length; i++) {
        this.options.push(new SearchOption(options[i], this.handleSelection.bind(this)));
      }
    },

    watchForSearchTerm: function() {
      var that = this;
      this.searchField.keyup(function(e) {
        if (e.target.value.length >= that.minSearchTermLength) {
          console.info('Filtering options');
          that.filterOptionsList(e.target.value);
        } else {
          that.clearFilter();
        }
      });
    },

    clearFilter: function() {
      for (var i = 0; i < this.options.length; i++) {
        this.options[i].hideOption();
      }
    },

    filterOptionsList: function(searchTerm) {
      var searchTerm = searchTerm.toLowerCase();
      for (var i = 0; i < this.options.length; i++) {
        this.options[i].filterForSearch(searchTerm, this.selectionField.value);
      }
    },

    handleSelection: function(option) {
      if (this.isSingleSelection) {
        this.handleSingleSelection(option);
      } else {
        this.handleMultilpeSelection(option);
      }
    },

    handleSingleSelection: function(option) {
      this.selectionField.value = option.idValue;
    },

    handleMultilpeSelection: function(option) {
      if (this.selectionField.value.length === 0) {
        this.selectionField.value = option.idValue;
      } else {
        this.selectionField.value = this.selectionField.value + ',' + option.idValue;
      }
    }
  }

  var SearchOption = function(option, handleSelectionCallback) {
    this.option = option;
    this.textValue = option.innerText.toLowerCase();
    this.idValue = option.value;
    this.handleSelection = handleSelectionCallback;
    this.setup();
  }

  SearchOption.prototype = {
    setup: function(){
      this.watchForSelection();
    },

    watchForSelection: function() {
      var that = this;
      $(this.option).click(function(e) {
        console.info(that.textValue + ' selected');
        that.handleSelection(that);
      })
    },

    filterForSearch: function(searchTerm, selectedOptions) {
      if (this.textValue.indexOf(searchTerm) > -1 && selectedOptions.indexOf(this.idValue) === -1) {
        $(this.option).show();
      } else {
        $(this.option).hide();
      }
    },

    hideOption: function() {
      $(this.option).hide();
    }
  }

  function init(){
    var searchDropdowns = $('.search-dropdown');
    for (var i = 0; i < searchDropdowns.length; i++) {
      new SearchDropdown(searchDropdowns[i]);
    }
  }

  $(document).on('page:load', init);
  $(init)
}(jQuery))
