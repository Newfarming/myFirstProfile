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
  var setRegex = function(input) {
    //input = input.replace(/[^\w0-9\\u ]+/, "").replace(/[ ]+/g, "|");
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
        var match = document.createElement(hiliteTag);
        match.appendChild(document.createTextNode(regs[0]));
        match.style.fontStyle = "inherit";
        match.className = cname;
        var after = node.splitText(regs.index);
        after.nodeValue = after.nodeValue.substring(regs[0].length);
        node.parentNode.insertBefore(match, after);
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
          myStyle.clear().load(
            '.pinbot-keyword-current{ background: #95C9F8 !important; color: #000;}',
            '.' + cname + '{background: #D7EDFF; color: #000;-webkit-transition: all 1s ease; transition: all 1s ease}'
          )
        }
        var span = cycle.get(cname);
        selector(document.querySelector('.pinbot-keyword-current')).removeClass('pinbot-keyword-current');
        selector(span).addClass('pinbot-keyword-current');
        span && $('body, html').stop().animate({
          scrollTop: findPos(span) - 100
        }, 'normal')
      }
    }
  }
}());

$(function() {
  var flag = true;

  var offset = $('#resume-detail').offset().top;
  var $window = $(window);
  var $locate = $('.locate-keywords');

  $window.scroll(function() {
    if ($window.scrollTop() >= offset) {
      $locate.fadeIn();
    } else {
      $locate.fadeOut();
    }
  });


  function slideDown() {
    $("dl").each(function() {
      var dl = $(this);
      if (!dl.hasClass('wrap-span-open')) {
        dl.find('.span-arrow').trigger('click');    
      }
    });
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


});

