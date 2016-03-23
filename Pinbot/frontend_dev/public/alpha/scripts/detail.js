(function () {
  var resumeid = document.body.getAttribute('data-resumeid');
  var myApp = angular.module('Notes', []);
  myApp.config([
    '$interpolateProvider',
    function ($interpolateProvider) {
      $interpolateProvider.startSymbol('{[{');
      $interpolateProvider.endSymbol('}]}');
    }
  ]);
  myApp.factory('notes', [
    '$http',
    function ($http) {
    }
  ]);
  myApp.controller('notes', [
    '$scope',
    '$timeout',
    function ($scope, $timeout) {
      var $prev = $('.ic-notes-prev');
      var $next = $('.ic-notes-next');
      $scope.openDialog = false;
      $scope.comment = '';
      $scope.currPos = 0;
      $scope.maxRow = 3;
      $scope.sliceData = function () {
        return ($scope.cachedData || []).slice($scope.currPos, $scope.currPos + $scope.maxRow);
      };
      $.get('/resumes/get_comments/' + resumeid + '/', function (result) {
      //$.get('/data/n.jgon', function (result) {

        if (result.status) {
          $timeout(function () {
            $scope.cachedData = result.data || [];
            $scope.data = $scope.sliceData();
            $scope.maxLength = $scope.cachedData.length;
            $('.notes-body').show();
            $('.notes').removeClass('loading');
          });
        }
      });
      $scope.toggle = function () {
        if ($scope.openDialog = !$scope.openDialog) {
          setTimeout(function () {
            $('.notes-textbox textarea').focus();
          });
        }
      };
      $scope.addComment = function (e) {
        var $add = $(e.target);
        if (!$scope.comment.length) {
          setTimeout(function () {
            $('.notes-textbox textarea').focus();
          });
          return;
        }
        $add.unbind('click');
        $.post('/resumes/add_comment/' + resumeid + '/', { comment: $scope.comment }, function (result) {
          if (result.status) {
            $timeout(function () {
              if ($scope.cachedData) {
                $scope.cachedData.unshift({
                  'id': result.data.comment_id,
                  'date': new Date().toLocaleDateString(),
                  'text': $scope.comment
                });
              }
              $scope.comment = '';
              $scope.toggle();
              $scope.currPos = 0;
              $scope.maxLength = $scope.cachedData.length;
              $scope.updatePagerState();
              $add.bind('click', $scope.addComment);
            });
          }
        });
      };
      $scope.delComment = function (id, index) {
        $.post('/resumes/delete_comment/' + resumeid + '/' + id + '/', function (result) {
          $timeout(function () {
            $scope.cachedData.splice(index, 1);
            $scope.maxLength = $scope.cachedData.length;
            $scope.updatePagerState();
          });
        });
      };
      $scope.updatePagerState = function () {
        $scope.data = $scope.sliceData();
        if (!$scope.data.length && $scope.currPos) {
          $scope.currPos -= $scope.maxRow;
          $scope.data = $scope.sliceData();
        }
        if ($scope.currPos >= $scope.maxRow) {
          $prev.removeClass('disabled');
        } else {
          $prev.addClass('disabled');
        }
        if ($scope.currPos < $scope.maxLength - $scope.maxRow) {
          $next.removeClass('disabled');
        } else {
          $next.addClass('disabled');
        }
      };
      $scope.nextPage = function () {
        $timeout(function () {
          if ($scope.currPos < $scope.maxLength - $scope.maxRow) {
            $scope.currPos += $scope.maxRow;
            $scope.updatePagerState();
          }
        });
      };
      $scope.prevPage = function () {
        $timeout(function () {
          if ($scope.currPos >= $scope.maxRow) {
            $scope.currPos -= $scope.maxRow;
            $scope.updatePagerState();
          }
        });
      };
    }
  ]);
}());

$(function() {
  var resumeid = document.body.getAttribute('data-resumeid');
  $('a.control-btn-fav').on('click', function() {
    var url = $(this).attr('href');
    $btn = $(this);
    if ($btn.find('span').hasClass('ctrl-pending')) {
      return false;
    }
    $btn.find('span').addClass('ctrl-pending');
    if (url.length < 2) url = '/resumes/add_watch/' + resumeid;
    $.get(url, function(result) {
      $btn.find('span').removeClass('ctrl-pending');
      if (result && result.status) {
        $('.control-btn-unfav').addClass('fav-current');
        $('.control-btn-fav').removeClass('fav-current');
      }
    });
    return false;
  });

  $('a.btn-unfav').on('click', function() {
    var url = $(this).attr('href');
    var $btn = $(this);
    if ($btn.parent().hasClass('ctrl-pending')) {
      return false;
    }
    $btn.parent().addClass('ctrl-pending');
    if (url.length < 2) url = '/resumes/remove_watch/' + resumeid;
    $.get(url, function(result) {
      $btn.parent().removeClass('ctrl-pending');
      if (result && result.status) {
        $('.control-btn-unfav').removeClass('fav-current');
        $('.control-btn-fav').addClass('fav-current');
      }
    });
    return false;
  });

  $('a.del').on('click', function() {
    var url = $(this).attr('href');
    if (url.length < 2) url = '/resumes/discard_watch/' + resumeid;
    $.get(url, function(result) {
      if (result && result.status) {
        window.location.href = '/resumes/all';
      }
    });
    return false;
  });

  $('.btn-toggle').on('click', function(e) {
    e.preventDefault();
    var btn = $(this),
        $h3 = $('.sec-resume h3');
    if (btn.hasClass('btn-toggle-span')) {
      btn.removeClass('btn-toggle-span');
      btn.parents('.sec-resume').find('dl').show();
    } else {
      btn.addClass('btn-toggle-span');
      btn.parents('.sec-resume').find('dl').hide();
    }
  });

  $('.btn-resume-feedback').on('click', function(e) {
    e.preventDefault();
    var $btn = $(this);
    var resume_id = document.body.getAttribute('data-resumeid');
    var feed_id = $btn.data('feed_id');
    if ($btn.hasClass('pending')) return false;

    if ($btn.hasClass('feed-back-sended')) {
      $btn.addClass('pending');
      $btn.find('span').addClass('ctrl-pending');
      $.get('/feed/modify_feed_result', {
        feed_id: feed_id,
        resume_id: resume_id,
        reco_index: '200'
      }, function() {
        $btn.find('span').removeClass('ctrl-pending');
        $btn.removeClass('feed-back-sended').removeClass('pending');
      });
    } else {
      $btn.addClass('pending');
      $btn.find('span').addClass('ctrl-pending');
      $.get('/feed/modify_feed_result', {
        feed_id: feed_id,
        resume_id: resume_id,
        reco_index: '-200'
      }, function() {
        $btn.find('span').removeClass('ctrl-pending');
        $btn.addClass('feed-back-sended').removeClass('pending');
      });
    }

  });

    /*$(window).on('scroll', function(){
        var $aside = $('.aside'),
            $doc = $(document),
            top = 105,
            scrollY = window.scrollY ? window.scrollY : document.documentElement.scrollTop;
        if(scrollY >= top){
            $aside.css('top', (scrollY - top + 10) + 'px');
        }else {
            $aside.css('top', 0);
        }
    });*/
});


(function($) {

  $.fn.overflown = function(){
    var e = this[0];
    return e.scrollHeight>e.clientHeight||e.scrollWidth>e.clientWidth;
  };

  /*
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
  });*/
}(jQuery));



var Style = (function() {

/**
 * Create an instance of Style
 * @param {Object} pre-defined variables
 */
function Style(map) {
  if (!(this instanceof Style)) {
    return new Style(map);
  }
  this.map = _mixin({}, map);
  this.rules = '';
  this.elem = null;
};


Style.prototype = {

  /**
   * Define new variables.
   * @param {object}
   */
  define: function(map) {
    this.map = _mixin(this.map, map);
    return this;
  },


  /**
   * Add new css but won't refresh the style element's content.
   * @param {string} Accepts multiple params
   */
  add: function() {
    var rules = _getRules(arguments);
    rules && (this.rules += rules);
    return this;
  },


  /**
   * Append new css to the style element or refresh its content.
   * @param {string}
   */
  load: function() {
    if (!this.elem) {
      this.elem = _createStyleElem();
    }
    if (arguments.length) {
      this.add.apply(this, arguments);
    }
    _refreshStyleContent(this.elem, this.rules, this.map);
    return this;
  },


  /**
   * Clear the style and varialbes.
   */
  clear: function() {
    _setStyleContent(this.elem, '');
    this.rules = '';
    this.map = {};
    return this;
  },


  /**
   * Remove the style element completely.
   */
  remove: function() {
    var elem = this.elem;
    if (elem && elem.parentNode) {
      this.clear();
      this.elem = null;
      elem.parentNode.removeChild(elem);
    }
    return this;
  }

};


function _mixin() {
  var mix = {}, idx, arg, name;
  for (idx = 0; idx < arguments.length; idx += 1) {
    arg = arguments[idx];
    for (name in arg) {
      if (arg.hasOwnProperty(name)) {
        mix[name] = arg[name];
      }
    }
  }
  return mix;
}


// Make a list of parameters of css into a single string.
function _getRules(args) {
  return [].join.call(args, '');
}


// Create new stylesheet.
function _createStyleElem() {
  var elem = document.createElement('style')
    , head = document.getElementsByTagName('head')[0];
  head && head.appendChild(elem);
  return elem;
}


// Substitute variables in the string with defined map.
function _substitute(str, map) {
  for (var name in map) {
    if (map.hasOwnProperty(name)) {
      str = str.replace(new RegExp('@' + name, 'gi'), map[name]);
    }
  }
  return str;
}


// Set the style element's content.
function _setStyleContent(el, content) {
  if (el && el.tagName.toLowerCase() === 'style') {
    el.styleSheet
      ? (el.styleSheet.cssText = content )
      : (el.innerHTML = content);
  }
}


// Refresh the content with the rules and defined variables.
function _refreshStyleContent(elem, rules, map) {
  _setStyleContent(elem,
    _substitute(rules, map)
  );
}

return Style;

}());


/**
 * Original JavaScript code by Chirp Internet: www.chirp.com.au
 */
function Hilitor(input, cname) {
  if(input == undefined || !input) return;
  var cname = cname || '';
  var targetNode = document.getElementById('resume-content') || document.body;
  var hiliteTag = "EM";
  var skipTags = new RegExp("^(?:" + hiliteTag + "|SCRIPT|FORM)$");
  var matchRegex = "";
  var openLeft = false;
  var openRight = false;
  var formatInput = function( i , v , arr ){
    return '\\' + i;
  };
  var setRegex = function(input) {
    //input = input.replace(/[^\w0-9\\u ]+/, "").replace(/[ ]+/g, "|");
    input = input.replace( /[+|.|*|$|^|?]/gi , formatInput );
    var re = "(" + input + ")";
    matchRegex = new RegExp(re, "i");
  };
  // recursively apply word highlighting
  var hiliteWords = function(node) {
    if(node == undefined || !node) return;
    if(!matchRegex) return;
    if(skipTags.test(node.nodeName)) return;
    if(node.hasChildNodes()) {
      for(var i=0; i < node.childNodes.length; i++)
        hiliteWords(node.childNodes[i]);
    }
    if(node.nodeType == 3) { // NODE_TEXT
      if((nv = node.nodeValue) && (regs = matchRegex.exec(nv))) {

        var matchKeywrod = regs[0];
        if(matchKeywrod && matchKeywrod.match(/^[0-9a-z]{3,}$/i)){
          //resolve keywords hilight bugs
          var nvZm=nv.replace(/[^0-9a-z]/ig," ");
          var nvZmArr=nvZm.split(" ");
          for(var i=0,imax=nvZmArr.length;i<imax;i++){
            var currentKw = matchKeywrod;
            var findMatch = new RegExp(""+currentKw+"","i");
            if(matchKeywrod!=nvZmArr[i] && nvZmArr[i].match(findMatch)){
              matchKeywrod = nvZmArr[i];
            }
          }
        }
        var match = document.createElement(hiliteTag);
        match.appendChild(document.createTextNode(matchKeywrod));
        match.style.fontStyle = "inherit";
        match.className = cname;
        var after = node.splitText(regs.index);
        after.nodeValue = after.nodeValue.substring(matchKeywrod.length);
        node.parentNode.insertBefore(match, after);
        //console.log('NODE_TEXT nv^^',nv,regs,regs.index,matchKeywrod,match, after);

      }
    };
  };

/*
  var el;
  var arr = document.getElementsByTagName(hiliteTag);
  while(arr.length && (el = arr[0])) {
    var parent = el.parentNode;
    parent.replaceChild(el.firstChild, el);
    parent.normalize();
  }
  */
  setRegex(convertCharStr2jEsc(input));
  hiliteWords(targetNode);
}

function dec2hex4(textString) {
  var hexequiv = new Array("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F");
  return hexequiv[(textString >> 12) & 0xF] + hexequiv[(textString >> 8) & 0xF] + hexequiv[(textString >> 4) & 0xF] + hexequiv[textString & 0xF];
}

function convertCharStr2jEsc(str, cstyle) {
  // Converts a string of characters to JavaScript escapes
  // str: sequence of Unicode characters
  var highsurrogate = 0;
  var suppCP;
  var pad;
  var n = 0;
  var outputString = '';
  for (var i = 0; i < str.length; i++) {
    var cc = str.charCodeAt(i);
    if (cc < 0 || cc > 0xFFFF) {
      outputString += '!Error in convertCharStr2UTF16: unexpected charCodeAt result, cc=' + cc + '!';
    }
    if (highsurrogate != 0) { // this is a supp char, and cc contains the low surrogate
      if (0xDC00 <= cc && cc <= 0xDFFF) {
        suppCP = 0x10000 + ((highsurrogate - 0xD800) << 10) + (cc - 0xDC00);
        if (cstyle) {
          pad = suppCP.toString(16);
          while (pad.length < 8) {
            pad = '0' + pad;
          }
          outputString += '\\U' + pad;
        } else {
          suppCP -= 0x10000;
          outputString += '\\u' + dec2hex4(0xD800 | (suppCP >> 10)) + '\\u' + dec2hex4(0xDC00 | (suppCP & 0x3FF));
        }
        highsurrogate = 0;
        continue;
      } else {
        outputString += 'Error in convertCharStr2UTF16: low surrogate expected, cc=' + cc + '!';
        highsurrogate = 0;
      }
    }
    if (0xD800 <= cc && cc <= 0xDBFF) { // start of supplementary character
      highsurrogate = cc;
    } else { // this is a BMP character
      switch (cc) {
      case 0:
        outputString += '\\0';
        break;
      case 8:
        outputString += '\\b';
        break;
      case 9:
        outputString += '\\t';
        break;
      case 10:
        outputString += '\\n';
        break;
      case 13:
        outputString += '\\r';
        break;
      case 11:
        outputString += '\\v';
        break;
      case 12:
        outputString += '\\f';
        break;
      case 34:
        outputString += '\\\"';
        break;
      case 39:
        outputString += '\\\'';
        break;
      case 92:
        outputString += '\\\\';
        break;
      default:
        if (cc > 0x1f && cc < 0x7F) {
          outputString += String.fromCharCode(cc);
        } else {
          pad = cc.toString(16).toUpperCase();
          while (pad.length < 4) {
            pad = '0' + pad;
          }
          outputString += '\\u' + pad;
        }
      }
    }
  }
  return outputString;
}


var Keywords= (function() {
  var randClass = function() {
    var pre = 'pinbot-keyword-';
    return pre + Math.random().toString(16).substr(2)
  };
  var findPos = function(obj) {
    var curtop = 0;
      if (obj.offsetParent) {
      do {
        curtop += obj.offsetTop;
      } while (obj = obj.offsetParent);
      return [curtop];
    }
  };
  var createIndex = function(from, to) {
    var curr = from;
    return {
      prev: function() {
        return curr <= from ? (curr = to) : --curr;
      },
      next: function() {
        return curr >= to ? (curr = from) : ++curr;
      },
      curr: function(idx) {
        return curr = (idx === undefined) ? curr : idx;
      }
    }
  };

  var selector = window.selector = (function() {
    function selector(el) {
      this.el = el || document.createElement('div');
    };
    selector.prototype = {
      hasClass: function(cname) {
        var str = (this.el.className || '').split(/\s+/);
        for (var i = 0; i < str.length; ++i) {
          if (cname == str[i]) return true;
        }
        return false;
      },
      addClass: function(cname) {
        var str = this.el.className;
        if (!this.hasClass(cname)) {
          this.el.className += (' ' + cname);
        }
        return this;
      },
      removeClass: function(cname) {
        var str = this.el.className;
        var array = str.split(/\s+/);
        var temp = [];
        for (var i = 0; i < array.length; ++i) {
          if (array[i]!= cname) {
            temp.push(array[i]);
          }
        }
        this.el.className = temp.join(' ');
        return this;
      }
    }
    return function(el) {
      return new selector(el);
    }
  }());

  var cycle = (function() {
    var container = {};
    return {
      add: function(cname) {
        var all = document.querySelectorAll('.' + cname);
        container[cname] = {
          index: createIndex(0, all.length - 1),
          element: all,
          get: function() {
            return this.element[this.index.next()]
          }
        }
      },
      get: function(cname) {
        if (!container[cname]) return {};
        return container[cname].get()
      },
      currIndex: function(cname) {
        if (container[cname]) {
          return container[cname].index.curr();
        }
      }
    }
  }());

  var cache = {};
  var currentKeyword = '';
  var myStyle = new Style();
  return {
    init: function(word) {
      if (cache.hasOwnProperty(word)) return this;
      var cname = randClass();
      Hilitor(word, cname);
      cache[word] = cname;
      cycle.add(cname);
      return this;
    },
    locate: function(word) {
      var cname = cache[word];
      if (cname) {
        if (currentKeyword != word) {
          currentKeyword = word;
          myStyle.load(
            '.pinbot-keyword-current{ background: #44b5e8 !important; color: #fff;}',
            '.' + cname + '{background: #44b5e8; color: #fff;-webkit-transition: all 1s ease; transition: all 1s ease}'
          )
        }
        var span = cycle.get(cname);
        selector(document.querySelector('.pinbot-keyword-current')).removeClass('pinbot-keyword-current');
        selector(span).addClass('pinbot-keyword-current');
        // span && $('body, html').stop().animate({
        //   scrollTop: findPos(span) - 100
        // }, 'normal')
      }
    }
  }
}());

$(function() {
  var flag = true;

  var offset = $('#resume-detail').offset().top;
  var $window = $(window);
  var $locate = $('.locate-keywords');


  // var Popup = (function() {
  //   var Popup = $('.popup-box');
  //   var Body = Popup.find('.popup-box-body');
  //   var Container = Popup.find('.popup-box-container');
  //   $('.popup-box-close').on('click', function(){
  //     Popup.hide();
  //   });

  //   var templates = {
  //     'confirm': $('#popup-template-confirm').html(),
  //     'ok':   $('#popup-template-ok').html(),
  //     'ok-wait': $('#popup-template-ok-wait').html(),
  //     'warn-1': $('#popup-template-warn-1').html(),
  //     'warn-2': $('#popup-template-warn-2').html(),
  //     'warn-3': $('#popup-template-warn-3').html(),
  //     'warn-4': $('#popup-template-warn-4').html()
  //   };

  //   return {
  //     render: function(id) {
  //       if (templates[id]) {
  //         Body.html(templates[id]);
  //         Container.removeClass('pay-pending');
  //         Popup.find('.popup-box-close').show();
  //         Popup.show();
  //       }
  //     },
  //     pending: function() {
  //       Body.html('');
  //       Container.addClass('pay-pending');
  //       Popup.find('.popup-box-close').hide();
  //     },
  //     close: function() {
  //       Popup.hide();
  //     }
  //   }
  // }());

  // var payTimer;

  // $('body').on('click', '.popup-action-cancel', function() {
  //     Popup.close();
  //   })
  //   .on('click', '.popup-action-reload', function() {
  //     window.location.replace('');
  //   })
  //   .on('click', '.popup-action-back', function() {
  //     Popup.close();
  //   })
  //   .on('click', '.popup-action-switch', function() {
  //     $('.ic-control-pay').parents('a').replaceWith(
  //       $('<span class="control-btn-pay-status"><i class="ic ic-control-paying"></i> 简历准备中</span>')
  //     );
  //   });
  window.subscribe = function(res){
    $('#JS_username').html( res.username );
    $('#JS_mission_time').html( res.mission_time );
    $('.modal-backdrop-tip,.modal-tip').show();
    $('.modal-dialog-tip').css({
        marginTop: ( $(window).height() - $('.modal-dialog-tip').height() ) / 2 + 'px'
    });
    $('.close-btn').on('click', function(e){
      e.preventDefault();
      $('.modal-backdrop-tip,.modal-tip').remove();
      delete $._LayerOut;
    });
  };

  function slideDown() {
    $('.btn-toggle-span').click();
    flag = false;
  }

  $('.locate-keywords-container>span').on('click', function() {
    if (flag) slideDown();
    var word = $(this).html();
    Keywords.init(word).locate(word);
    return false;
  });

  $('.btn-scroll-top').on('click', function() {
    $('body, html').stop().animate({
      scrollTop: 0
    }, 'normal')
    return false;
  });
  if(window.feed_keywords != undefined){
    for (var i = window.feed_keywords.length - 1; i >= 0; i--) {
        (function(arg){
            var word = window.feed_keywords[arg];
            Keywords.init(word).locate(word);
        })(i);
    };
  }

  // $('.buy-status-1 a').on('click', function(e) {
  //   e.preventDefault();
  //   var hasCompanyCard = function(){
  //         var html = $('#JS_has_card_html').html();
  //         $.LayerOut({
  //             html: html,
  //             dialogCss: 'width:540px;'
  //         });
  //       };
  //     isHasCompanyInfo( hasCompanyCard );
  // });

  // $('.tao-enter-btn').not('.submitted').on('click', function() {
  //   var $con = $('.tao-feed-container').toggle();
  //   setTimeout(function() {
  //     $con.toggleClass('translatex');
  //   }, 0);
  // });

  $( document ).on('click', '.tao-cancel' , function() {
    $('.tao-enter-btn').not('.submitted').click();
  });

  $( document ).on( 'click' , '.choice-list li' , function() {
    $('.choice-list>li.selected').removeClass('selected').find('div').hide();
    $(this).addClass('selected');
    if ($(this).find('input').length) {
      $(this).find('input').focus();
    };
    if ($(this).find('div').length) {
      $(this).find('div').show().focus();
    };
    $('.tao-feed-container').find('.selected-choice').removeClass('selected-choice');
    $(this).parents('.choice-group').addClass('selected-choice');
  });


  // $('.tao-feed-container').find('.header>ul>li>a').each(function(i) {
  //   var $con = $('.tao-feed-container');
  //   $con.find('.header>ul>li>a').eq(i).on('click', function() {
  //     $(this).parents('ul').find('.on').removeClass('on');
  //     $(this).addClass('on');
  //     $con.find('.footer')[i == 1 ? 'hide': 'show']();
  //     $con.find('.body>.on').removeClass('on');
  //     $con.find('.tab-content').eq(i).addClass('on');
  //   });
  // });

  $( document ).on('click', '.tao-submit' , function(e) {
      e.preventDefault();
      if ( $(this).hasClass('tao-submitting')) return false;
      var url = $('.tao-feed-container').find('.choice-groups').data('submit-url');
      var selected = $('.tao-feed-container').find('.selected-choice').find('li.selected');
      var input = selected.find('input[type="text"]').length ? selected.find('input[type="text"]') : selected.find('textarea');
      var data = {
        'feedback_id': selected.data('id'),
        'feedback_value': input.length && input.val() || '',
        'resume_id': $('body').data('resumeid')
      };
      if (!selected.length) {
          $(this).parent().find('span').css('color', 'red').html('请选择并填写好你的反馈.').show();
          return false;
      } else if (input.length && ( !$.trim(input.val()).length || $.trim(input.val()) == input.attr('placeholder') ) ) {
          $(this).parent().find('span').css('color', 'red').html('请选择并填写好你的反馈.').show();
          input.focus();
          return false;
      } else {
          $(this).parent().find('span').hide();
          $(this).addClass('tao-submitting');
          $(this).html('提交中..');
          $.post(url, data, function(d) {
              $(this).removeClass('tao-submitting');
              $(this).html('提交');
              if (d && d.status == 'success') {
                $('.tao-enter').addClass('tao-status-3');
                $.alert('保存成功');
                window.location.reload(true);
              } else if( d && d.msg ){
                $.alert( d.msg );
              }else{
                $.alert('保存失败，请重试！');
              };
              $('.tao-submit').removeClass('tao-submitting').html( '提交' );
          }, 'json').fail(function(){
              $.alert('保存失败，请重试！');
              $('.tao-submit').removeClass('tao-submitting').html( '提交' );
          });
      };
  });

  //标记简历状态
  $( document ).on( 'click' , '#JS_feedback_btn' , function(){
    var html = $('#JS_feedback').html();
    $.LayerOut({
        html: html,
        dialogCss: 'width:725px;height:630px;'
    });
  });

  //保存到本地
  $( document ).on( 'click' , '#JS_down_to_local' , function(){
    var html = $('#JS_download_local').html();
    $.LayerOut({
        html: html,
        dialogCss: 'width:660px;'
    });
  });

  // toggle hr评价
  $( document ).on( 'click' , '#JS_toggle_evaluate' , function(){
    $(this).find('.hr-evaluate').toggle();
  })
});


