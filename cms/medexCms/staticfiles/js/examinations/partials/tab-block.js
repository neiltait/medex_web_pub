var TabBlock = function(wrapper, checkForChanges, tabChangeModal) {
    this.wrapper = wrapper;
    this.checkForChanges = checkForChanges;
    this.tabChangeModal = tabChangeModal;
    this.setup();
}

TabBlock.prototype = {
    setup: function() {
        this.tabs = [];
        this.initialiseTabs();
    },

    initialiseTabs: function() {
        var tabInfo = this.wrapper.find('.tab-item');
        for (var i = 0; i < tabInfo.length; i++) {
            this.tabs.push(new Tab(tabInfo[i], this.showTab.bind(this)));
        }
    },

    showTab: function (tabName, evt) {
      if (this.checkForChanges()) {
        evt.preventDefault();
        this.tabChangeModal.show(tabName);
      }
    },
}

var Tab = function(tab, clickCallback) {
    this.tab = $(tab);
    this.clickCallback = clickCallback;
    this.setup();
}

Tab.prototype = {
    setup: function() {
        this.page = this.tab[0].id.slice(0,-4)
        this.startWatcher();
    },

    startWatcher: function() {
        var that = this;
        this.tab.click(function(evt) {
            that.clickCallback(that.page, evt);
        })
    }
}