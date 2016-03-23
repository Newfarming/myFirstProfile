
$(function() {

  if (!('autofocus' in document.createElement('input'))) {
    $('input[autofocus]').first().focus();
  }

  if (!('required' in document.createElement('input'))) {
    $('form').on('submit', function() {
      var all = $(this).find('input[required]');
      for (var i = 0; i < all.length; ++i) {
        if (!$.trim(all.eq(i).val())) {
          all.eq(i).focus();
          return false;
        }
      }
    });
  }

  if (!('placeholder' in document.createElement('input'))) {
    $('input[placeholder]').each(function() {

      var $input = $(this);
      var $label = $('<label>');
      $label.html($input.attr('placeholder'));
      $label.css({
        'font-size': '14px',
        'position': 'absolute',
        'left': '15px',
        'top': '13px',
        'color': '#999',
        'cursor': 'text',
        'width': '90%',
        'text-align': 'left'
      });

      $input.on('keydown paste', function() {
        setTimeout(function() {
          $label[ $input.val() ? 'hide' : 'show' ]();
        }, 0);
      }).parent().append(
        $label.on('click', function() {
          $input.focus();
        })
      );
    });
  }
});
