
(function() {

  var Notes = {}

  Notes.load = function(callback) {
    this.data = [
      {"date": "2012.09.23", "text": "hello"},
      {"date": "2012.09.23", "text": "world!"}
    ]
    this.data = [];
    var self = this;
    setTimeout(function() {
    $('.notes').removeClass('loading');
      callback && callback.call(self);
    }, 100);
  }

  Notes.ready = function(callback) {
    Notes.load(callback);
  };

  Notes.init =  function() {
    var sec = this.sec = {};
    this.sec.body = $('.notes-body').show();
    this.sec.placeholder = 
    this.sec.body.find('.notes-placeholder').hide()
    this.sec.pager = sec.body.find('.notes-pager').hide();
    this.sec.list = sec.body.find('.notes-list').hide();
    this.sec.textbox = sec.body.find('.notes-textbox-wrap').hide();

    this.sec.placeholder.on('click', function() {
      $(this).hide();
      sec.textbox.show();
      sec.textbox.find('textarea').focus();
    });

    $('.notes>h3 a').on('click', function() {
      sec.textbox.toggle();   
      sec.textbox.find('textarea').focus();
      return false;
    });

  }

  Notes.update = function() {
    if (!this.data.length) {
      console.log(this);
      this.sec.placeholder.show();
      return;
    }
    Notes.sec.placeholder.hide();
    Notes.sec.textbox.hide();
    Notes.sec.list.show();
    Notes.buildList(0);
  }

  Notes.ready(function()  {
    Notes.init();
    Notes.update();  
  });

}());
