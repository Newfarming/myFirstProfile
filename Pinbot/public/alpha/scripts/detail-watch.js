$(function() {
  var resumeid = document.body.getAttribute('data-resumeid');
  $('a.fav').on('click', function() {
    $.get('/resumes/add_watch/' + resumeid, function(result) {
      if (result && result.status) {
        $('.faved').addClass('fav-current');
        $('.unfav').removeClass('fav-current');
      }
    });
    return false;
  });

  $('a.btn-unfav').on('click', function() {
    $.get('/resumes/remove_watch/' + resumeid, function(result) {
      if (result && result.status) {
        $('.faved').removeClass('fav-current');
        $('.unfav').addClass('fav-current'); 
      }
    });
    return false;
  });

  $('a.del').on('click', function() {
    $.get('/resumes/discard_resume/' + resumeid, function(result) {
      if (result && result.status) {
        window.location.href = '/resumes/all';
      }
    });
    return false;
  });

});
