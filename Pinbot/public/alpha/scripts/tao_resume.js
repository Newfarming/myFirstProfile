function scrollTo(to, fn) {
  $('html, body').stop().animate({ 'scrollTop': to }, 'normal', fn||function(){});
};
     
function formartTags( list ){
    if( !list.length ) return;
    var html = '';
    for( var i = 0 , l = list.length ; i < l ; i++ ){
        var item = list[i];
        html += '<a href="javascript:;" class="JS_tags_a" data-tag="' + item.tag + '" data-tag_id="' + item.tag_id + '">' + item.tag + '</a>';
    };
    $('#JS_list_tags').html( html );
};

var feedApp = angular.module('feedApp', []);
feedApp.config([
  '$interpolateProvider',
  function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
  }
]);
feedApp.config([
  '$routeProvider',
  function ($routeProvider) {
    var $feedTemplate = $('#template-feeditem').html();
    var first = $('.feed-nav >li').first().find('a').attr('href').substr(1);

    $routeProvider.when('/group/:id', {
      template: $feedTemplate,
      controller: 'feedPage'
   });
    $routeProvider.otherwise({ redirectTo: first });
  }
]);
feedApp.factory('Feed', [
  '$http',
  function ($http) {
    var pathname = window.location.pathname || '';
    var default_view = 'user';
    if (pathname === '/statis/feed_result/') {
      default_view = 'cached';
    }
    return {
      group: function (id, start, latest, view, fn) {
       return $http.get('/feed/group/' + id + '?start=' + start + '&limit=100&view=' + view + '&t=' + +new Date()).then(function (response) {
       //return $http.get('/data/items-all.json?start=' + start + '&latest=' + latest + '&limit=100&t=' + +new Date()).then(function (response) {
            formartTags( response.data.all_tags );
            if( response.data.data.length ){
                var date = new Date( response.data.data[0].calc_time ),
                    y = date.getFullYear(),
                    m = date.getMonth() + 1,
                    d = date.getDate();
                m = ( m.toString().length > 1 ? m : '0' + m );
                d = ( d.toString().length > 1 ? d : '0' + d );
                $('#JS_calendar').html('<i class="i-calendar">' + d + '</i> <span>' + y + '年' + m + '月' + d + '日</span>').show();
            };
            window.taoResumes = response.data;
            return response.data;
        }).then(fn);
      },
      current: {
        id: '',
        view: default_view,
        start: 0,
        latest: 1,
        total_count: 0,
        total_recommend_count: 0,
        scope: {},
        selected: []
      }
    };
  }
]);
function minusOne($elems) {
  $elems.each(function () {
    var $this = $(this);
    var count = parseInt($this.html(), 10) - 1;
    if (count <= 0)
      count = '';
    $this.html(count);
  });
}
function setNum($elems, num) {
  $elems.each(function () {
    if (num <= 0) num = '';
    $(this).html(num);
  });
}
feedApp.filter('gender', function () {
  return function (text) {
    if(text == 'female') {
      return '女';
    }else if (text == 'male'){
      return '男';
    }else {
      return text;
    }
  };
}).filter('nospace', function() {
  return function(text) {
    return text.split(/\s+/)[0];
  };
}).filter('checkFeedOpen', function () {
  return function (input) {
    return input ? '' : 'feed-unread';
  };
}).filter('checkFeedLatest', function () {
  return function (input) {
    return input ? 'feed-latest' : '';
  };
}).filter('chop', function() {
  return function(text) {
    if (text.length >150) {
      text = text.substr(0, 147) + '</br>...';
    }
    return text;
  }
}).filter('checkSelect', function() {
  return function(span, scope) {
    if (span.tag) {
      for (var i = 0; i < scope.selected; ++i) {
        if (span.tag == scope.selected[i].tag) {
          return 'curr'
        }
      }
    }
    return '';
  };
}).filter('select', function() {
  return function(items, scope) {
    if (!scope.selected.length) return items;
    var filtered = [];
    if (scope.all_tags) {
      angular.forEach(items, function(item) {
        if (item.tags) {
          var map = {};
            
          for (var j = 0; j < item.tags.length;++j) {
            map[item.tags[j].tag] = 1;
          }
          
          var count = 0;
          for (var i = 0; i < scope.selected.length; ++i) {
            if (map[scope.selected[i].tag]) {
              count++;
            }
          }
          if (count == scope.selected.length) {
            filtered.push(item);
          }
        }
      });
      return filtered;
    }
  };
});
feedApp.directive('fixedtop', function () {
  return {
    restrict: 'A',
    link: function (scope, elem, attrs) {
      var offset = attrs.fixedtop || 0;
      var top = $(elem).offset().top;
      var $el = $(elem);
      var $win = $(window);
      var pos = $el.css('position');

      $win.on('scroll', function () {
        if ($win.scrollTop() >= top - offset) {
          $el.parent().css('height', $el.height() + parseInt($el.parent().css('margin-bottom')));
          $el.width($el.parent().width());
          $el.css({
            'position': 'fixed',
            top: offset + 'px'
          });
        } else {
          $el.css({
            'position': pos,
            top: 'auto'
          });
        }
      });
    }
  };
});
var $more = $('.load-more');
feedApp.controller('aside', [
  '$scope',
  '$location',
  function ($scope, $location) {
    $scope.isActive = function (route) {
      return $location.path().indexOf(route) != -1;
    };
  }
]).controller('feedApp', [
  '$scope',
  'Feed',
  '$timeout',
  function ($scope, Feed, $timeout) {
    $scope.current = Feed.current;
    $scope.toggleLatest = function ($event) {
      if (!$scope.current.latest) {
        $scope.current.latest = 1;
      } else {
        $scope.current.latest = 0;
      }
      $timeout(function () {
        var link = $('.feed-nav .curr').find('a');
        var href = link.attr('href');
        window.location.replace(href.split('?')[0] + '?' + Math.random().toString(16).substr(2));
      });
    };
    $scope.toggleView = function(view, $event) {
      if ($scope.current.view == view) return false;
      $scope.current.view = view || 'user';
      $timeout(function () {
        var link = $('.feed-nav .curr').find('a');
        var href = link.attr('href');
        window.location.replace(href.split('?')[0] + '?' + Math.random().toString(16).substr(2));
      }); 
    }
  }
]).controller('feedPage', [
  '$scope',
  'Feed',
  '$timeout',
  '$routeParams',
  '$rootScope',
  function ($scope, Feed, $timeout, $routeParams, $rootScope) {
    Feed.current.id = $routeParams.id;
    Feed.current.start = 0;
    Feed.current.limit = 6;
    
    $scope.fetch = function ($event) {
      $scope.loadmore = true;
      $scope.hasmore = false;
      Feed.group(Feed.current.id, Feed.current.start, Feed.current.latest, Feed.current.view, function (data) {
        $timeout(function () {
          $scope.feeditems.push.apply($scope.feeditems, data.data);
          Feed.current.start = data.next_start;
          $scope.loadmore = false;
          if (data.next_start != '-1') {
            $scope.hasmore = true;
          }

          //if ($('.feed-nav li.curr').find('.feed-latest-count').data('count-group') == 'all') {
          //  return false;
          //} else if ($scope.current.latest) {
          if ($scope.current.latest) {
            setNum(
              $('.feed-nav li.curr').find('.feed-latest-count'), 
              data.newest_recommend_count
            ); 
          } else if (data.newest_recommend_count) {
            if(_.filter(data.data||[], function(d) {
              return !!d.latest;
            }).length) {
              setNum(
                $('.feed-nav li.curr').find('.feed-latest-count'), 
                data.newest_recommend_count
              );
            }
          }

        });
      });
    };
    $timeout(function () {
      $scope.initLoading = true;
      $scope.loadmore = false;
      $scope.hasmore = false;
      $scope.waiting = false;
    });
    if (Feed.current.id) {
      Feed.group(Feed.current.id, Feed.current.start, Feed.current.latest, Feed.current.view, function (data) {
        $timeout(function () {
          $scope.feeditems = data.data;
          $scope.all_tags = data.all_tags;

          $scope.initLoading = false;
          Feed.current.total_count = data.total_count;
          Feed.current.total_recommend_count = data.total_recommend_count;
          Feed.current.start = data.next_start;
          if (data.next_start != '-1') {
            $scope.hasmore = true;
          }
          if (!data.count || !data.data.length) {
            $scope.waiting = true;
            $scope.hasmore = false;
          }

          // all 100 
          $scope.hasmore = false;

          //if ($('.feed-nav li.curr').find('.feed-latest-count').data('count-group') == 'all') {
          //  return false; 
          //} else if ($scope.current.latest) {
          if ($scope.current.latest) {
            setNum(
              $('.feed-nav li.curr').find('.feed-latest-count'), 
              data.newest_recommend_count
            ); 
          } else if (data.newest_recommend_count) {
            if(_.filter(data.data||[], function(d) {
              return !!(d && d.latest);
            }).length) {
              setNum(
                $('.feed-nav li.curr').find('.feed-latest-count'), 
                data.newest_recommend_count
              );
            }
          } 
        });
      });
    }

    $scope.selected = [];
    $scope.allSelect = {};

    $scope.toggleTag = function(tag, $event) {

      $('.feed-item-out').addClass('feed-item-out-loading');
      scrollTo(0, function() {
        $('.feed-item-out').removeClass('feed-item-out-loading');
        var $span = $($event.target);
        var action = 'add';

        if ($span.hasClass('curr')) {
          action = 'del';
        }

        if (tag) {
          if (action == 'add') {
            $timeout(function() {
              $scope.selected.push(tag);
              $scope.allSelect[tag.tag] = 1;
            });
          } else {
            for (var i = 0; i < $scope.selected.length; ++i) {
              if (tag.tag == $scope.selected[i].tag) {
                $timeout(function() {
                  $scope.selected.splice(i, 1);
                  delete $scope.allSelect[tag.tag];
                })
                return;
              }
            }
          }
        }
        
      });
    };

    $scope.isSelected = function(tag) {
      for (var i = 0; i < $scope.selected.length; ++i) {
        if ((''+tag.tag) === (''+$scope.selected[i].tag)) {
          return 'curr';
        }
      }
      return '';
    }

    $scope.openFeed = function (idx, group) {
      if ($scope.feeditems[idx].latest) {
        minusOne($('span[data-count-group="' + $scope.feeditems[idx].feed_id + '"], span[data-count-group="all"]'));
      }
      $scope.feeditems[idx].latest = false;
      $scope.feeditems[idx].opened = true;
    };
    $scope.dislike = function(idx) {
      $.get('/feed/modify_feed_result', {
        feed_id: $scope.feeditems[idx].feed_id,
        resume_id: $scope.feeditems[idx].resume_id,
        reco_index: '-150'
      });
      $timeout(function() {
        $scope.feeditems[idx].dislike = true;
        $scope.feeditems[idx].latest = false;
        $scope.feeditems[idx].opened = true; 
      });
    }
  }
]);
$(function () {
  var $submitForm = $('#feed-submit-form');
  $submitForm.find('.options').each(function () {
    var $options = $(this);
    var name = $options.data('name');
    var input = $('input[name="' + name + '"]');
    $options.find('span').on('click', function () {
      if ($options.hasClass('op-multi')) {
        $(this).toggleClass('selected');
      } else if ($options.hasClass('op-single')) {
        $(this).parents('li').find('.selected').removeClass('selected');
        $(this).addClass('selected');
      }
      input.val($options.find('.selected').map(function () {
        return $.trim($(this).html());
      }).toArray().join(','));
    });
  });

  $('.suggested-keywords').on('click', 'span', function() {
    var val = $(this).html();
    $('input[name="keywords"]').val(val).focus();
  });

  var is_submitting = false;
  $submitForm.on('submit', function() {
    if (is_submitting) return false;
    if (!$('input[name="job_type"]').val()) {
      scrollTo( $submitForm.find('li').eq(0).offset().top);
      return false;
    }
    if (!$('input[name="keywords"]').val()) {
      scrollTo( $submitForm.find('li').eq(1).offset().top);
      return false; 
    }
     
    if (!$('input[name="talent_level"]').val()) {
      scrollTo( $submitForm.find('li').eq(2).offset().top);
      return false; 
    }
    if (!$('input[name="expect_area"]').val()) {
      scrollTo( $submitForm.find('li').eq(3).offset().top);
      return false; 
    }
    is_submitting = true;
    $('#btn-feed-submit').val('正在提交..');
  });

  $('.select-btn-more>a').on('click', function(e) {
    e.preventDefault();
    var $a = $(this);
    $('.select-expect-area').toggleClass('expect-area-span')
      .find('.op-multi').slideToggle(200);
    var text = $.trim($a.html());
    $a.html($a.data('text-span'));
    $a.data('text-span', text); 
  }); 


  $('p[data-name="job_type"]>span').on('click', function() {
    var suggest = $(this).data('suggest');
    if (suggest) {
      $('.suggested-keywords').html(
        $.map(suggest.split('|'), function(s) {
          return '<span>' + s + '</span>';
        }).join('')  
      )
    }
  });


  $('a[href^="/feed/delete"]').on('click', function (e) {
    var choice = window.confirm('\u5220\u9664\u8ba2\u9605\u6761\u4ef6\u5c06\u6e05\u9664\u6b64\u8ba2\u9605\u4e0b\u7684\u6240\u6709\u7b80\u5386\uff01\u662f\u5426\u7ee7\u7eed\uff1f');
    if (!choice)
      return false;
  });
  
  $('.feed-edit-jd >form').on('submit', function (e) {
    e.preventDefault();
    var $form = $(this);
    var action = $form.attr('action');
    var job_desc = $form.find('textarea[name="job_desc"]').val();
    if (job_desc == window.feed_edit_jd_old) {
      $form.find('textarea[name="job_desc"]').focus();
      return false;
    }
    var $btn = $form.find('button[type="submit"]').html('\u6b63\u5728\u4fdd\u5b58');
    $btn.addClass('submitting');
    $.post(action, { job_desc: job_desc }, function (ret) {
      $btn.removeClass('submitting');
      $btn.html('\u4fdd\u5b58');
      if (ret && ret.status) {
        window.feed_edit_jd_old = job_desc;
        $btn.prev().remove();
        $('<span style="margin-right: 10px; color:green;">\u5df2\u4fdd\u5b58!</span>').insertBefore($btn).fadeOut(1500, function () {
          $(this).remove();
        });
      } else {
        $btn.prev().remove();
        $('<span style="margin-right: 10px; color:red;">\u4fdd\u5b58\u5931\u8d25\uff0c\u8bf7\u91cd\u8bd5!</span>').insertBefore($btn).fadeOut(3000, function () {
          $(this).remove();
        });
      }
    });
  });

  $('.feed-page').on('click', '.want-more-tags-handler', function(e) {
    e.preventDefault();
    $('.want-more-tags-addition').toggle();
    if (!$('.want-more-tags-addition').is(':hidden')) {
      $('.want-more-tags').find('textarea').focus();
    }
  }).on('click', '.want-more-tags-addition-action .action-cancel', function(e) {
    e.preventDefault();
    $('.want-more-tags-addition').hide();
  }).on('click', '.action-add-tags', function(e) {
    var text = $.trim($('.want-more-tags').find('textarea').val());
    if (!text) {
      $('.want-more-tags').find('textarea').focus();
      return false;
    }
    var feed_id = $('.feed-nav').find('.curr>a').data('feed_id');
    $.post('/resumes/add_tag_search', {tag: text, feed_id: feed_id}, function(e) {
      $('.want-more-tags').find('textarea').val('');
    });
    $('.want-more-tags-addition').hide();
    $('.want-more-submitted').fadeIn();
  }).on('click', '.want-more-submitted', function() {
    $('.want-more-submitted').fadeOut('fast');
  });

  var hovertimer;
  $('body')
    .on('mouseover', '.resume-tags-hook', function() {
      clearTimeout(hovertimer);
      $(this).parents('.item-header').find('.item-action-keywords').fadeIn();
    })
    .on('mouseout', '.resume-tags-hook, .item-action-keywords', function() {
      hovertimer = setTimeout(function() {
        $('.item-action-keywords').hide();
      }, 400);
    })
    .on('mouseover', '.item-action-keywords', function() {
      clearTimeout(hovertimer);
    })
   
  ;(function() {
    var $doc = $(document);
    $(window).on('scroll', function() {
      var more =  $('a[ng-show="hasmore"]');
      if (!more.length) return false;
      if (!more.is(':hidden')) {
        var offset = $doc.height() - $doc.scrollTop() - $(window).height();
        if (offset < 100) {
          more.get(0).click();
        }
      }
    });

  }());
    
    $( document ).on( 'click' , '.JS_tags_a' , function(){
        var $this = $( this ),
            tag = $this.attr('data-tag'),
            tag_id = $this.attr('data-tag_id');
        $('.JS_tags_a[data-tag_id="' + tag_id + '"]').toggleClass('curr');
        if( Filter && Filter.tags && Filter.tags[tag_id] ){
            delete Filter.tags[tag_id];
        }else{
            Filter.tags[tag_id] = tag;
        };
        getList();
    });

    $( document ).on( 'click' , '#JS_submit_btn' , function(){
        if( window.lockSearch ) return false;
        window.lockSearch = true;
        var form = $( this ).closest('form');
        if( !checkForm( form ) ) return false;
        var filter = getFilter( form );
        filter = groupFilter( filter );
        window.Filter = filter;
        getList();
        window.lockSearch = false;
    });

});

function groupFilter( filter ){
    var tagDom = $('#JS_list_tags').find('.curr'),
        obj = {};

    if(!tagDom.length ){
        return filter;
    };
    for( var i = 0 , l = tagDom.length ; i < l ; i++ ){
        var dom = tagDom.eq(i),
            tag = dom.attr('data-tag'),
            tag_id = dom.attr('data-tag_id');
        filter.tags[tag_id] = tag;
    };
    return filter;
};

function checkForm( form ){
    if( form.find('.tip-error').length > 0 ){
        window.lockSearch = false;
        alert('请填写正确!');
        return false;
    };
    return true;
};

function getFilter( form ){
    var arr = form.serialize().split('&'),
        obj = {tags:{}};
    for( var i = 0 , l = arr.length ; i < l ; i++ ){
        var item = arr[i].split('=');
        if( item[1] ){
            obj[item[0]] = decodeURIComponent( item[1] );
        };
    };
    return obj;
};

function checkList( item ){

    if( !$.isEmptyObject( Filter.tags ) ){
        if(!item.tags || !item.tags.length ) return false;
        var hasTag = false;
        for( var i = 0 , l = item.tags.length ; i < l ; i++ ){
            var tag = item.tags[i];
            if( Filter.tags[ tag.tag_id ] ){
                hasTag = true;
            };
        };
        if( !hasTag ) return false;
    };
    
    if( Filter.lower_year || Filter.upper_year ){
        if( !item.profile || !item.profile.work_years ) return false;
        var work_years = parseInt(item.profile.work_years);
        if( work_years < parseInt(Filter.lower_year) || work_years > parseInt(Filter.upper_year) ) return false;
    };

    if( Filter.lower_money || Filter.upper_money ){
        if( !item.job_target || !item.job_target.salary ) return false;
        var salary = item.job_target.salary.split('-'),
            upper_money = parseInt(Filter.upper_money),
            lower_money = parseInt(Filter.lower_money);
        salary[0] = parseInt(salary[0]);
        salary[1] = parseInt(salary[1]);
        if( upper_money < lower_money ) return false;
        if( salary[1] < lower_money * 1000 || salary[0] > upper_money * 1000 ) return false;
        // console.log( salary[0] , salary[1] , Filter.lower_money ,Filter.upper_money  )
    };

    if( Filter.degree ){
        if( !item.profile || !item.profile.degree || ( item.profile.degree != Filter.degree ) ) return false;
    };

    return true;
};

function getList(){
    if( !window.taoResumes || !window.taoResumes.data ) return;
    var data = window.taoResumes.data,
        html = '';
    for( var i = 0 , l = data.length ; i < l ; i++ ){
        var item = data[i];

        if( !checkList( item ) ) continue;

        html += '<div class="feed-item ' + ( item.opened ? '' : 'feed-unread' ) + ' ' + ( item.latest ? 'feed-latest' : '' ) + '">' +
        '<div class="feed-item-wrapper">' +
          '<div class="item-header">' +
            '<div class="item-header-wrapper">' +
              '<div class="item-profile">' +
                '<h3 class="item-work-position">' +
                  '<span style="margin-right: 5px; color: rgb(255, 153, 0); display: none;" class="ng-binding"></span>' +
                  ( item.latest_work && item.latest_work.position_title ? item.latest_work.position_title : '' ) +
                '</h3>' +
                '<span class="item-update-time" ng-show="item.calc_time">推荐时间： ' + ( item.calc_time ? item.calc_time : '') + '</span>' +
                '<p>' +
                  '<span class="item-profile-gender ng-binding">' + ( item.profile && item.profile.gender ? ( item.profile.gender == 'male' ? '男' : ( item.profile.gender == 'female' ? '女' : item.profile.gender ) ) : '' ) + '</span>' +
                  '<span class="item-profile-age ng-binding">' + ( item.profile && item.profile.age ? item.profile.age : '' ) + '&nbsp; &nbsp; </span>' +
                  '<span class="ng-binding">' + ( item.job_target && item.job_target.job_hunting_state ? item.job_target.job_hunting_state : '' ) + '</span>' +
                  '<span class="item-profile-sep">|</span>';
                  if( item.profile && item.profile.address ){
                    html += '<span class="ng-binding">现居地：' + item.profile.address + '&nbsp; &nbsp;</span>';
                  };
                  if( item.profile && item.profile.address ){
                    html += '<span class="ng-binding">意向地：' + item.profile.address + '</span>';
                  };
                html += '</p>' +
              '</div>' +
              '<div class="item-resume-tags clearfix">';
              for( var ii = 0 , ll = item.tags.length ; ii < ll ; ii++ ){
                var tagItem = item.tags[ii];
                html += '<a href="" class="JS_tags_a ' + ( Filter.tags && Filter.tags[tagItem.tag_id] ? 'curr' :'' ) + '" data-tag="' + tagItem.tag + '" data-tag_id="' + tagItem.tag_id + '" >' + tagItem.tag + '</a>';
              };
              html += '</div>' +
            '</div>' +
          '</div>' +
          '<div class="item-body">' +
            '<div class="item-body-wrapper">' +
              '<div class="item-summary"> ' +
                '<div class="item-main">' +
                 ' <p>' +
                    '<span class="item-profile-exp"><em class="ng-binding">' + ( item.profile && item.profile.work_years ? item.profile.work_years : '' ) + '</em>年经验</span>' +
                    '<span class="item-profile-sep">|</span>' +
                    '<span class="item-work-salary">期望薪资：<em class="ng-binding">' + ( item.job_target && item.job_target.salary ? item.job_target.salary : '' ) + '</em></span>' +
                  '</p>' +
                '</div>';

                if( item.latest_work ){
                    html += '<div class="item-work">' +
                      '<p>' +
                        '<span class="item-work-comp ng-binding">' + ( item.latest_work && item.latest_work.company_name ? item.latest_work.company_name : '' ) + '</span>' +
                        '<span class="item-profile-sep">|</span>' +
                        '<span class="item-work-position>' + ( item.latest_work && item.latest_work.position_title ? item.latest_work.position_title : '' ) + ' </span>' +
                        '&nbsp;' +
                        '<span class="item-work-salary>' + ( item.latest_work && item.latest_work.salary ? item.latest_work.salary : '' ) + '</span>' +
                      '</p>' +
                      '<p class="work-detail ng-binding">' + ( item.latest_work && item.latest_work.job_desc ? item.latest_work.job_desc : '' ) + '</p>' +
                    '</div>';
                };
                
                html += '<div class="item-edu">' +
                  '<p>' +
                    '<span class="item-edu-school ng-binding">' + ( item.profile && item.profile.school ? item.profile.school : '' ) + '</span>' +
                    '<span class="item-profile-degree ng-binding">' + ( item.profile && item.profile.degree ? item.profile.degree : '' ) + '</span>' +
                  '</p>' +
                '</div>' +
              '</div>' +
              '<div class="item-footer">' +
                '<p class="resume-link">' +
                  '<a title="点击查看简历详情" onclick="openFeed($index)" href="/feed/get/' + item.feed_id + '/' + item.resume_id + '" target="_blank">查看简历</a>' +
                '</p>' +
              '</div>' +          
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>'
    };
    if( !html ){
        html += '<div class="feed-item-out-empty"><p>可惜没找到。</p></div>';
    };
    $('#JS_list_content').html( html );
};