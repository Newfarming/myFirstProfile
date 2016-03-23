(function($) {

  $.fn.overflown = function(){
    var e = this[0];
    return e.scrollHeight>e.clientHeight||e.scrollWidth>e.clientWidth;
  }; 

  $(function() {

    $('.project, .exp').find('dl').each(function() {
      var $self = $(this);
      var $spans = $self.find('.desc-span');
      var flag = false;
      $spans.each(function() {
        if ($(this).find('div').overflown()) {
          flag = true;
        }
      });

      if (flag) {
       $('<a class="span-arrow"></a>')
        .appendTo($self.css('padding-bottom', '30px'))
        .on('click', function() {
          if ($spans.eq(0).hasClass('desc-span-open')) {
            $spans.removeClass('desc-span-open');
            $self.removeClass('wrap-span-open');      
            $self.css('cursor', 'pointer');
          } else {
            $spans.addClass('desc-span-open');      
            $self.addClass('wrap-span-open');      
            $self.css('cursor', 'default');
          }
          return false;         
        });

        $self
          .css('cursor', 'pointer')
          .on('click', function() {
            if (!$spans.eq(0).hasClass('desc-span-open')) {
              $(this).find('.span-arrow').trigger('click');  
            }
          })
      }
    });

    
  });
}(jQuery));
