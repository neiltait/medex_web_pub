var ChangeTabModal = function (modal, saveCallBack) {
    this.modal = $(modal);
    this.saveCallBack = saveCallBack;
    this.setup();
  }

ChangeTabModal.prototype = {
    setup: function () {
      this.saveButton = this.modal.find('#save-continue');
      this.discardButton = this.modal.find('#discard');
      this.startWatchers();
    },

    startWatchers: function () {
      var that = this;

      this.saveButton.click(function () {
        that.saveCallBack(that.nextTab);
      });

      this.discardButton.click(function () {
        var pathPieces = location.pathname.split('/');
        pathPieces[pathPieces.length - 1] = that.nextTab;
        newPath = pathPieces.join('/');
        location.pathname = newPath;
      });
    },

    show: function (nextTab) {
      this.nextTab = nextTab;
      this.modal.show();
    }
  }
