!function(e,t){"use strict";var n,r=e,a=r.document,i=r.navigator,o=r.setTimeout,l=r.encodeURIComponent,s=r.ActiveXObject,u=r.Error,c=r.Number.parseInt||r.parseInt,f=r.Number.parseFloat||r.parseFloat,p=r.Number.isNaN||r.isNaN,d=r.Math.round,h=r.Date.now,y=r.Object.keys,v=r.Object.defineProperty,m=r.Object.prototype.hasOwnProperty,g=r.Array.prototype.slice,b=function(e){return g.call(e,0)},w=function(){var e,n,r,a,i,o,l=b(arguments),s=l[0]||{};for(e=1,n=l.length;n>e;e++)if(null!=(r=l[e]))for(a in r)m.call(r,a)&&(i=s[a],o=r[a],s!==o&&o!==t&&(s[a]=o));return s},x=function(e){var t,n,r,a;if("object"!=typeof e||null==e)t=e;else if("number"==typeof e.length)for(t=[],n=0,r=e.length;r>n;n++)m.call(e,n)&&(t[n]=x(e[n]));else{t={};for(a in e)m.call(e,a)&&(t[a]=x(e[a]))}return t},C=function(e,t){for(var n={},r=0,a=t.length;a>r;r++)t[r]in e&&(n[t[r]]=e[t[r]]);return n},T=function(e,t){var n={};for(var r in e)-1===t.indexOf(r)&&(n[r]=e[r]);return n},D=function(e){if(e)for(var t in e)m.call(e,t)&&delete e[t];return e},E=function(e,t){if(e&&1===e.nodeType&&e.ownerDocument&&t&&(1===t.nodeType&&t.ownerDocument&&t.ownerDocument===e.ownerDocument||9===t.nodeType&&!t.ownerDocument&&t===e.ownerDocument))do{if(e===t)return!0;e=e.parentNode}while(e);return!1},j=function(e){var t;return"string"==typeof e&&e&&(t=e.split("#")[0].split("?")[0],t=e.slice(0,e.lastIndexOf("/")+1)),t},O=function(e){var t,n;return"string"==typeof e&&e&&(n=e.match(/^(?:|[^:@]*@|.+\)@(?=http[s]?|file)|.+?\s+(?: at |@)(?:[^:\(]+ )*[\(]?)((?:http[s]?|file):\/\/[\/]?.+?\/[^:\)]*?)(?::\d+)(?::\d+)?/),n&&n[1]?t=n[1]:(n=e.match(/\)@((?:http[s]?|file):\/\/[\/]?.+?\/[^:\)]*?)(?::\d+)(?::\d+)?/),n&&n[1]&&(t=n[1]))),t},k=function(){var e,t;try{throw new u}catch(n){t=n}return t&&(e=t.sourceURL||t.fileName||O(t.stack)),e},I=function(){var e,n,r;if(a.currentScript&&(e=a.currentScript.src))return e;if(n=a.getElementsByTagName("script"),1===n.length)return n[0].src||t;if("readyState"in n[0])for(r=n.length;r--;)if("interactive"===n[r].readyState&&(e=n[r].src))return e;return"loading"===a.readyState&&(e=n[n.length-1].src)?e:(e=k())?e:t},N=function(){var e,n,r,i=a.getElementsByTagName("script");for(e=i.length;e--;){if(!(r=i[e].src)){n=null;break}if(r=j(r),null==n)n=r;else if(n!==r){n=null;break}}return n||t},L=function(){var e=j(I())||N()||"";return "/static/alpha/scripts/ZeroClipboard.swf"},_={bridge:null,version:"0.0.0",pluginType:"unknown",disabled:null,outdated:null,unavailable:null,deactivated:null,overdue:null,ready:null},z="11.0.0",S={},F={},A=null,X={ready:"Flash communication is established",error:{"flash-disabled":"Flash is disabled or not installed","flash-outdated":"Flash is too outdated to support ZeroClipboard","flash-unavailable":"Flash is unable to communicate bidirectionally with JavaScript","flash-deactivated":"Flash is too outdated for your browser and/or is configured as click-to-activate","flash-overdue":"Flash communication was established but NOT within the acceptable time limit"}},Y={swfPath:L(),trustedDomains:e.location.host?[e.location.host]:[],cacheBust:!0,forceEnhancedClipboard:!1,flashLoadTimeout:3e4,autoActivate:!0,bubbleEvents:!0,containerId:"global-zeroclipboard-html-bridge",containerClass:"global-zeroclipboard-container",swfObjectId:"global-zeroclipboard-flash-bridge",hoverClass:"zeroclipboard-is-hover",activeClass:"zeroclipboard-is-active",forceHandCursor:!1,title:null,zIndex:999999999},$=function(e){if("object"==typeof e&&null!==e)for(var t in e)if(m.call(e,t))if(/^(?:forceHandCursor|title|zIndex|bubbleEvents)$/.test(t))Y[t]=e[t];else if(null==_.bridge)if("containerId"===t||"swfObjectId"===t){if(!et(e[t]))throw new Error("The specified `"+t+"` value is not valid as an HTML4 Element ID");Y[t]=e[t]}else Y[t]=e[t];{if("string"!=typeof e||!e)return x(Y);if(m.call(Y,e))return Y[e]}},B=function(){return{browser:C(i,["userAgent","platform","appName"]),flash:T(_,["bridge"]),zeroclipboard:{version:It.version,config:It.config()}}},H=function(){return!!(_.disabled||_.outdated||_.unavailable||_.deactivated)},M=function(e,t){var n,r,a,i={};if("string"==typeof e&&e)a=e.toLowerCase().split(/\s+/);else if("object"==typeof e&&e&&"undefined"==typeof t)for(n in e)m.call(e,n)&&"string"==typeof n&&n&&"function"==typeof e[n]&&It.on(n,e[n]);if(a&&a.length){for(n=0,r=a.length;r>n;n++)e=a[n].replace(/^on/,""),i[e]=!0,S[e]||(S[e]=[]),S[e].push(t);if(i.ready&&_.ready&&It.emit({type:"ready"}),i.error){var o=["disabled","outdated","unavailable","deactivated","overdue"];for(n=0,r=o.length;r>n;n++)if(_[o[n]]===!0){It.emit({type:"error",name:"flash-"+o[n]});break}}}return It},P=function(e,t){var n,r,a,i,o;if(0===arguments.length)i=y(S);else if("string"==typeof e&&e)i=e.split(/\s+/);else if("object"==typeof e&&e&&"undefined"==typeof t)for(n in e)m.call(e,n)&&"string"==typeof n&&n&&"function"==typeof e[n]&&It.off(n,e[n]);if(i&&i.length)for(n=0,r=i.length;r>n;n++)if(e=i[n].toLowerCase().replace(/^on/,""),o=S[e],o&&o.length)if(t)for(a=o.indexOf(t);-1!==a;)o.splice(a,1),a=o.indexOf(t,a);else o.length=0;return It},R=function(e){var t;return t="string"==typeof e&&e?x(S[e])||null:x(S)},Z=function(e){var t,n,r;return e=tt(e),e&&!lt(e)?"ready"===e.type&&_.overdue===!0?It.emit({type:"error",name:"flash-overdue"}):(t=w({},e),ot.call(this,t),"copy"===e.type&&(r=dt(F),n=r.data,A=r.formatMap),n):void 0},V=function(){if("boolean"!=typeof _.ready&&(_.ready=!1),!It.isFlashUnusable()&&null===_.bridge){var e=Y.flashLoadTimeout;"number"==typeof e&&e>=0&&o(function(){"boolean"!=typeof _.deactivated&&(_.deactivated=!0),_.deactivated===!0&&It.emit({type:"error",name:"flash-deactivated"})},e),_.overdue=!1,ft()}},K=function(){It.clearData(),It.blur(),It.emit("destroy"),pt(),It.off()},U=function(e,t){var n;if("object"==typeof e&&e&&"undefined"==typeof t)n=e,It.clearData();else{if("string"!=typeof e||!e)return;n={},n[e]=t}for(var r in n)"string"==typeof r&&r&&m.call(n,r)&&"string"==typeof n[r]&&n[r]&&(F[r]=n[r])},G=function(e){"undefined"==typeof e?(D(F),A=null):"string"==typeof e&&m.call(F,e)&&delete F[e]},J=function(e){return"undefined"==typeof e?x(F):"string"==typeof e&&m.call(F,e)?F[e]:void 0},W=function(e){if(e&&1===e.nodeType){n&&(xt(n,Y.activeClass),n!==e&&xt(n,Y.hoverClass)),n=e,wt(e,Y.hoverClass);var t=e.getAttribute("title")||Y.title;if("string"==typeof t&&t){var r=ct(_.bridge);r&&r.setAttribute("title",t)}var a=Y.forceHandCursor===!0||"pointer"===Ct(e,"cursor");jt(a),Et()}},q=function(){var e=ct(_.bridge);e&&(e.removeAttribute("title"),e.style.left="0px",e.style.top="-9999px",e.style.width="1px",e.style.top="1px"),n&&(xt(n,Y.hoverClass),xt(n,Y.activeClass),n=null)},Q=function(){return n||null},et=function(e){return"string"==typeof e&&e&&/^[A-Za-z][A-Za-z0-9_:\-\.]*$/.test(e)},tt=function(e){var t;if("string"==typeof e&&e?(t=e,e={}):"object"==typeof e&&e&&"string"==typeof e.type&&e.type&&(t=e.type),t){w(e,{type:t.toLowerCase(),target:e.target||n||null,relatedTarget:e.relatedTarget||null,currentTarget:_&&_.bridge||null,timeStamp:e.timeStamp||h()||null});var r=X[e.type];return"error"===e.type&&e.name&&r&&(r=r[e.name]),r&&(e.message=r),"ready"===e.type&&w(e,{target:null,version:_.version}),"error"===e.type&&(/^flash-(disabled|outdated|unavailable|deactivated|overdue)$/.test(e.name)&&w(e,{target:null,minimumVersion:z}),/^flash-(outdated|unavailable|deactivated|overdue)$/.test(e.name)&&w(e,{version:_.version})),"copy"===e.type&&(e.clipboardData={setData:It.setData,clearData:It.clearData}),"aftercopy"===e.type&&(e=ht(e,A)),e.target&&!e.relatedTarget&&(e.relatedTarget=nt(e.target)),e=rt(e)}},nt=function(e){var t=e&&e.getAttribute&&e.getAttribute("data-clipboard-target");return t?a.getElementById(t):null},rt=function(e){if(e&&/^_(?:click|mouse(?:over|out|down|up|move))$/.test(e.type)){var n=e.target,i="_mouseover"===e.type&&e.relatedTarget?e.relatedTarget:t,o="_mouseout"===e.type&&e.relatedTarget?e.relatedTarget:t,l=Dt(n),s=r.screenLeft||r.screenX||0,u=r.screenTop||r.screenY||0,c=a.body.scrollLeft+a.documentElement.scrollLeft,f=a.body.scrollTop+a.documentElement.scrollTop,p=l.left+("number"==typeof e._stageX?e._stageX:0),d=l.top+("number"==typeof e._stageY?e._stageY:0),h=p-c,y=d-f,v=s+h,m=u+y,g="number"==typeof e.movementX?e.movementX:0,b="number"==typeof e.movementY?e.movementY:0;delete e._stageX,delete e._stageY,w(e,{srcElement:n,fromElement:i,toElement:o,screenX:v,screenY:m,pageX:p,pageY:d,clientX:h,clientY:y,x:h,y:y,movementX:g,movementY:b,offsetX:0,offsetY:0,layerX:0,layerY:0})}return e},at=function(e){var t=e&&"string"==typeof e.type&&e.type||"";return!/^(?:(?:before)?copy|destroy)$/.test(t)},it=function(e,t,n,r){r?o(function(){e.apply(t,n)},0):e.apply(t,n)},ot=function(e){if("object"==typeof e&&e&&e.type){var t=at(e),n=S["*"]||[],a=S[e.type]||[],i=n.concat(a);if(i&&i.length){var o,l,s,u,c,f=this;for(o=0,l=i.length;l>o;o++)s=i[o],u=f,"string"==typeof s&&"function"==typeof r[s]&&(s=r[s]),"object"==typeof s&&s&&"function"==typeof s.handleEvent&&(u=s,s=s.handleEvent),"function"==typeof s&&(c=w({},e),it(s,u,[c],t))}return this}},lt=function(e){var t=e.target||n||null,r="swf"===e._source;delete e._source;var a=["flash-disabled","flash-outdated","flash-unavailable","flash-deactivated","flash-overdue"];switch(e.type){case"error":-1!==a.indexOf(e.name)&&w(_,{disabled:"flash-disabled"===e.name,outdated:"flash-outdated"===e.name,unavailable:"flash-unavailable"===e.name,deactivated:"flash-deactivated"===e.name,overdue:"flash-overdue"===e.name,ready:!1});break;case"ready":var i=_.deactivated===!0;w(_,{disabled:!1,outdated:!1,unavailable:!1,deactivated:!1,overdue:i,ready:!i});break;case"copy":var o,l,s=e.relatedTarget;!F["text/html"]&&!F["text/plain"]&&s&&(l=s.value||s.outerHTML||s.innerHTML)&&(o=s.value||s.textContent||s.innerText)?(e.clipboardData.clearData(),e.clipboardData.setData("text/plain",o),l!==o&&e.clipboardData.setData("text/html",l)):!F["text/plain"]&&e.target&&(o=e.target.getAttribute("data-clipboard-text"))&&(e.clipboardData.clearData(),e.clipboardData.setData("text/plain",o));break;case"aftercopy":It.clearData(),t&&t!==bt()&&t.focus&&t.focus();break;case"_mouseover":It.focus(t),Y.bubbleEvents===!0&&r&&(t&&t!==e.relatedTarget&&!E(e.relatedTarget,t)&&st(w({},e,{type:"mouseenter",bubbles:!1,cancelable:!1})),st(w({},e,{type:"mouseover"})));break;case"_mouseout":It.blur(),Y.bubbleEvents===!0&&r&&(t&&t!==e.relatedTarget&&!E(e.relatedTarget,t)&&st(w({},e,{type:"mouseleave",bubbles:!1,cancelable:!1})),st(w({},e,{type:"mouseout"})));break;case"_mousedown":wt(t,Y.activeClass),Y.bubbleEvents===!0&&r&&st(w({},e,{type:e.type.slice(1)}));break;case"_mouseup":xt(t,Y.activeClass),Y.bubbleEvents===!0&&r&&st(w({},e,{type:e.type.slice(1)}));break;case"_click":case"_mousemove":Y.bubbleEvents===!0&&r&&st(w({},e,{type:e.type.slice(1)}))}return/^_(?:click|mouse(?:over|out|down|up|move))$/.test(e.type)?!0:void 0},st=function(e){if(e&&"string"==typeof e.type&&e){var t,n=e.target||null,i=n&&n.ownerDocument||a,o={view:i.defaultView||r,canBubble:!0,cancelable:!0,detail:"click"===e.type?1:0,button:"number"==typeof e.which?e.which-1:"number"==typeof e.button?e.button:i.createEvent?0:1},l=w(o,e);n&&i.createEvent&&n.dispatchEvent&&(l=[l.type,l.canBubble,l.cancelable,l.view,l.detail,l.screenX,l.screenY,l.clientX,l.clientY,l.ctrlKey,l.altKey,l.shiftKey,l.metaKey,l.button,l.relatedTarget],t=i.createEvent("MouseEvents"),t.initMouseEvent&&(t.initMouseEvent.apply(t,l),t._source="js",n.dispatchEvent(t)))}},ut=function(){var e=a.createElement("div");return e.id=Y.containerId,e.className=Y.containerClass,e.style.position="absolute",e.style.left="0px",e.style.top="-9999px",e.style.width="1px",e.style.height="1px",e.style.zIndex=""+Ot(Y.zIndex),e},ct=function(e){for(var t=e&&e.parentNode;t&&"OBJECT"===t.nodeName&&t.parentNode;)t=t.parentNode;return t||null},ft=function(){var e,t=_.bridge,n=ct(t);if(!t){var i=gt(r.location.host,Y),o="never"===i?"none":"all",l=vt(Y),s=Y.swfPath+yt(Y.swfPath,Y);n=ut();var u=a.createElement("div");n.appendChild(u),a.body.appendChild(n);var c=a.createElement("div"),f="activex"===_.pluginType;c.innerHTML='<object id="'+Y.swfObjectId+'" name="'+Y.swfObjectId+'" width="100%" height="100%" '+(f?'classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000"':'type="application/x-shockwave-flash" data="'+s+'"')+">"+(f?'<param name="movie" value="'+s+'"/>':"")+'<param name="allowScriptAccess" value="'+i+'"/><param name="allowNetworking" value="'+o+'"/><param name="menu" value="false"/><param name="wmode" value="transparent"/><param name="flashvars" value="'+l+'"/></object>',t=c.firstChild,c=null,t.ZeroClipboard=It,n.replaceChild(t,u)}return t||(t=a[Y.swfObjectId],t&&(e=t.length)&&(t=t[e-1]),!t&&n&&(t=n.firstChild)),_.bridge=t||null,t},pt=function(){var e=_.bridge;if(e){var t=ct(e);t&&("activex"===_.pluginType&&"readyState"in e?(e.style.display="none",function n(){if(4===e.readyState){for(var r in e)"function"==typeof e[r]&&(e[r]=null);e.parentNode&&e.parentNode.removeChild(e),t.parentNode&&t.parentNode.removeChild(t)}else o(n,10)}()):(e.parentNode&&e.parentNode.removeChild(e),t.parentNode&&t.parentNode.removeChild(t))),_.ready=null,_.bridge=null,_.deactivated=null}},dt=function(e){var t={},n={};if("object"==typeof e&&e){for(var r in e)if(r&&m.call(e,r)&&"string"==typeof e[r]&&e[r])switch(r.toLowerCase()){case"text/plain":case"text":case"air:text":case"flash:text":t.text=e[r],n.text=r;break;case"text/html":case"html":case"air:html":case"flash:html":t.html=e[r],n.html=r;break;case"application/rtf":case"text/rtf":case"rtf":case"richtext":case"air:rtf":case"flash:rtf":t.rtf=e[r],n.rtf=r}return{data:t,formatMap:n}}},ht=function(e,t){if("object"!=typeof e||!e||"object"!=typeof t||!t)return e;var n={};for(var r in e)if(m.call(e,r)){if("success"!==r&&"data"!==r){n[r]=e[r];continue}n[r]={};var a=e[r];for(var i in a)i&&m.call(a,i)&&m.call(t,i)&&(n[r][t[i]]=a[i])}return n},yt=function(e,t){var n=null==t||t&&t.cacheBust===!0;return n?(-1===e.indexOf("?")?"?":"&")+"noCache="+h():""},vt=function(e){var t,n,a,i,o="",s=[];if(e.trustedDomains&&("string"==typeof e.trustedDomains?i=[e.trustedDomains]:"object"==typeof e.trustedDomains&&"length"in e.trustedDomains&&(i=e.trustedDomains)),i&&i.length)for(t=0,n=i.length;n>t;t++)if(m.call(i,t)&&i[t]&&"string"==typeof i[t]){if(a=mt(i[t]),!a)continue;if("*"===a){s.length=0,s.push(a);break}s.push.apply(s,[a,"//"+a,r.location.protocol+"//"+a])}return s.length&&(o+="trustedOrigins="+l(s.join(","))),e.forceEnhancedClipboard===!0&&(o+=(o?"&":"")+"forceEnhancedClipboard=true"),"string"==typeof e.swfObjectId&&e.swfObjectId&&(o+=(o?"&":"")+"swfObjectId="+l(e.swfObjectId)),o},mt=function(e){if(null==e||""===e)return null;if(e=e.replace(/^\s+|\s+$/g,""),""===e)return null;var t=e.indexOf("//");e=-1===t?e:e.slice(t+2);var n=e.indexOf("/");return e=-1===n?e:-1===t||0===n?null:e.slice(0,n),e&&".swf"===e.slice(-4).toLowerCase()?null:e||null},gt=function(){var e=function(e){var t,n,r,a=[];if("string"==typeof e&&(e=[e]),"object"!=typeof e||!e||"number"!=typeof e.length)return a;for(t=0,n=e.length;n>t;t++)if(m.call(e,t)&&(r=mt(e[t]))){if("*"===r){a.length=0,a.push("*");break}-1===a.indexOf(r)&&a.push(r)}return a};return function(t,n){var r=mt(n.swfPath);null===r&&(r=t);var a=e(n.trustedDomains),i=a.length;if(i>0){if(1===i&&"*"===a[0])return"always";if(-1!==a.indexOf(t))return 1===i&&t===r?"sameDomain":"always"}return"never"}}(),bt=function(){try{return a.activeElement}catch(e){return null}},wt=function(e,t){if(!e||1!==e.nodeType)return e;if(e.classList)return e.classList.contains(t)||e.classList.add(t),e;if(t&&"string"==typeof t){var n=(t||"").split(/\s+/);if(1===e.nodeType)if(e.className){for(var r=" "+e.className+" ",a=e.className,i=0,o=n.length;o>i;i++)r.indexOf(" "+n[i]+" ")<0&&(a+=" "+n[i]);e.className=a.replace(/^\s+|\s+$/g,"")}else e.className=t}return e},xt=function(e,t){if(!e||1!==e.nodeType)return e;if(e.classList)return e.classList.contains(t)&&e.classList.remove(t),e;if("string"==typeof t&&t){var n=t.split(/\s+/);if(1===e.nodeType&&e.className){for(var r=(" "+e.className+" ").replace(/[\n\t]/g," "),a=0,i=n.length;i>a;a++)r=r.replace(" "+n[a]+" "," ");e.className=r.replace(/^\s+|\s+$/g,"")}}return e},Ct=function(e,t){var n=r.getComputedStyle(e,null).getPropertyValue(t);return"cursor"!==t||n&&"auto"!==n||"A"!==e.nodeName?n:"pointer"},Tt=function(){var e,t,n,r=1;return"function"==typeof a.body.getBoundingClientRect&&(e=a.body.getBoundingClientRect(),t=e.right-e.left,n=a.body.offsetWidth,r=d(t/n*100)/100),r},Dt=function(e){var t={left:0,top:0,width:0,height:0};if(e.getBoundingClientRect){var n,i,o,l=e.getBoundingClientRect();"pageXOffset"in r&&"pageYOffset"in r?(n=r.pageXOffset,i=r.pageYOffset):(o=Tt(),n=d(a.documentElement.scrollLeft/o),i=d(a.documentElement.scrollTop/o));var s=a.documentElement.clientLeft||0,u=a.documentElement.clientTop||0;t.left=l.left+n-s,t.top=l.top+i-u,t.width="width"in l?l.width:l.right-l.left,t.height="height"in l?l.height:l.bottom-l.top}return t},Et=function(){var e;if(n&&(e=ct(_.bridge))){var t=Dt(n);w(e.style,{width:t.width+"px",height:t.height+"px",top:t.top+"px",left:t.left+"px",zIndex:""+Ot(Y.zIndex)})}},jt=function(e){_.ready===!0&&(_.bridge&&"function"==typeof _.bridge.setHandCursor?_.bridge.setHandCursor(e):_.ready=!1)},Ot=function(e){if(/^(?:auto|inherit)$/.test(e))return e;var t;return"number"!=typeof e||p(e)?"string"==typeof e&&(t=Ot(c(e,10))):t=e,"number"==typeof t?t:"auto"},kt=function(e){function t(e){var t=e.match(/[\d]+/g);return t.length=3,t.join(".")}function n(e){return!!e&&(e=e.toLowerCase())&&(/^(pepflashplayer\.dll|libpepflashplayer\.so|pepperflashplayer\.plugin)$/.test(e)||"chrome.plugin"===e.slice(-13))}function r(e){e&&(s=!0,e.version&&(p=t(e.version)),!p&&e.description&&(p=t(e.description)),e.filename&&(c=n(e.filename)))}var a,o,l,s=!1,u=!1,c=!1,p="";if(i.plugins&&i.plugins.length)a=i.plugins["Shockwave Flash"],r(a),i.plugins["Shockwave Flash 2.0"]&&(s=!0,p="2.0.0.11");else if(i.mimeTypes&&i.mimeTypes.length)l=i.mimeTypes["application/x-shockwave-flash"],a=l&&l.enabledPlugin,r(a);else if("undefined"!=typeof e){u=!0;try{o=new e("ShockwaveFlash.ShockwaveFlash.7"),s=!0,p=t(o.GetVariable("$version"))}catch(d){try{o=new e("ShockwaveFlash.ShockwaveFlash.6"),s=!0,p="6.0.21"}catch(h){try{o=new e("ShockwaveFlash.ShockwaveFlash"),s=!0,p=t(o.GetVariable("$version"))}catch(y){u=!1}}}}_.disabled=s!==!0,_.outdated=p&&f(p)<f(z),_.version=p||"0.0.0",_.pluginType=c?"pepper":u?"activex":s?"netscape":"unknown"};kt(s);var It=function(){return this instanceof It?("function"==typeof It._createClient&&It._createClient.apply(this,b(arguments)),void 0):new It};v(It,"version",{value:"2.1.3",writable:!1,configurable:!0,enumerable:!0}),It.config=function(){return $.apply(this,b(arguments))},It.state=function(){return B.apply(this,b(arguments))},It.isFlashUnusable=function(){return H.apply(this,b(arguments))},It.on=function(){return M.apply(this,b(arguments))},It.off=function(){return P.apply(this,b(arguments))},It.handlers=function(){return R.apply(this,b(arguments))},It.emit=function(){return Z.apply(this,b(arguments))},It.create=function(){return V.apply(this,b(arguments))},It.destroy=function(){return K.apply(this,b(arguments))},It.setData=function(){return U.apply(this,b(arguments))},It.clearData=function(){return G.apply(this,b(arguments))},It.getData=function(){return J.apply(this,b(arguments))},It.focus=It.activate=function(){return W.apply(this,b(arguments))},It.blur=It.deactivate=function(){return q.apply(this,b(arguments))},It.activeElement=function(){return Q.apply(this,b(arguments))};var Nt=0,Lt={},_t=0,zt={},St={};w(Y,{autoActivate:!0});var Ft=function(e){var t=this;t.id=""+Nt++,Lt[t.id]={instance:t,elements:[],handlers:{}},e&&t.clip(e),It.on("*",function(e){return t.emit(e)}),It.on("destroy",function(){t.destroy()}),It.create()},At=function(e,t){var n,r,a,i={},o=Lt[this.id]&&Lt[this.id].handlers;if("string"==typeof e&&e)a=e.toLowerCase().split(/\s+/);else if("object"==typeof e&&e&&"undefined"==typeof t)for(n in e)m.call(e,n)&&"string"==typeof n&&n&&"function"==typeof e[n]&&this.on(n,e[n]);if(a&&a.length){for(n=0,r=a.length;r>n;n++)e=a[n].replace(/^on/,""),i[e]=!0,o[e]||(o[e]=[]),o[e].push(t);if(i.ready&&_.ready&&this.emit({type:"ready",client:this}),i.error){var l=["disabled","outdated","unavailable","deactivated","overdue"];for(n=0,r=l.length;r>n;n++)if(_[l[n]]){this.emit({type:"error",name:"flash-"+l[n],client:this});break}}}return this},Xt=function(e,t){var n,r,a,i,o,l=Lt[this.id]&&Lt[this.id].handlers;if(0===arguments.length)i=y(l);else if("string"==typeof e&&e)i=e.split(/\s+/);else if("object"==typeof e&&e&&"undefined"==typeof t)for(n in e)m.call(e,n)&&"string"==typeof n&&n&&"function"==typeof e[n]&&this.off(n,e[n]);if(i&&i.length)for(n=0,r=i.length;r>n;n++)if(e=i[n].toLowerCase().replace(/^on/,""),o=l[e],o&&o.length)if(t)for(a=o.indexOf(t);-1!==a;)o.splice(a,1),a=o.indexOf(t,a);else o.length=0;return this},Yt=function(e){var t=null,n=Lt[this.id]&&Lt[this.id].handlers;return n&&(t="string"==typeof e&&e?n[e]?n[e].slice(0):[]:x(n)),t},$t=function(e){if(Rt.call(this,e)){"object"==typeof e&&e&&"string"==typeof e.type&&e.type&&(e=w({},e));var t=w({},tt(e),{client:this});Zt.call(this,t)}return this},Bt=function(e){e=Vt(e);for(var t=0;t<e.length;t++)if(m.call(e,t)&&e[t]&&1===e[t].nodeType){e[t].zcClippingId?-1===zt[e[t].zcClippingId].indexOf(this.id)&&zt[e[t].zcClippingId].push(this.id):(e[t].zcClippingId="zcClippingId_"+_t++,zt[e[t].zcClippingId]=[this.id],Y.autoActivate===!0&&Kt(e[t]));var n=Lt[this.id]&&Lt[this.id].elements;-1===n.indexOf(e[t])&&n.push(e[t])}return this},Ht=function(e){var t=Lt[this.id];if(!t)return this;var n,r=t.elements;e="undefined"==typeof e?r.slice(0):Vt(e);for(var a=e.length;a--;)if(m.call(e,a)&&e[a]&&1===e[a].nodeType){for(n=0;-1!==(n=r.indexOf(e[a],n));)r.splice(n,1);var i=zt[e[a].zcClippingId];if(i){for(n=0;-1!==(n=i.indexOf(this.id,n));)i.splice(n,1);0===i.length&&(Y.autoActivate===!0&&Ut(e[a]),delete e[a].zcClippingId)}}return this},Mt=function(){var e=Lt[this.id];return e&&e.elements?e.elements.slice(0):[]},Pt=function(){this.unclip(),this.off(),delete Lt[this.id]},Rt=function(e){if(!e||!e.type)return!1;if(e.client&&e.client!==this)return!1;var t=Lt[this.id]&&Lt[this.id].elements,n=!!t&&t.length>0,r=!e.target||n&&-1!==t.indexOf(e.target),a=e.relatedTarget&&n&&-1!==t.indexOf(e.relatedTarget),i=e.client&&e.client===this;return r||a||i?!0:!1},Zt=function(e){if("object"==typeof e&&e&&e.type){var t=at(e),n=Lt[this.id]&&Lt[this.id].handlers["*"]||[],a=Lt[this.id]&&Lt[this.id].handlers[e.type]||[],i=n.concat(a);if(i&&i.length){var o,l,s,u,c,f=this;for(o=0,l=i.length;l>o;o++)s=i[o],u=f,"string"==typeof s&&"function"==typeof r[s]&&(s=r[s]),"object"==typeof s&&s&&"function"==typeof s.handleEvent&&(u=s,s=s.handleEvent),"function"==typeof s&&(c=w({},e),it(s,u,[c],t))}return this}},Vt=function(e){return"string"==typeof e&&(e=[]),"number"!=typeof e.length?[e]:e},Kt=function(e){if(e&&1===e.nodeType){var t=function(e){(e||(e=r.event))&&("js"!==e._source&&(e.stopImmediatePropagation(),e.preventDefault()),delete e._source)},n=function(n){(n||(n=r.event))&&(t(n),It.focus(e))};e.addEventListener("mouseover",n,!1),e.addEventListener("mouseout",t,!1),e.addEventListener("mouseenter",t,!1),e.addEventListener("mouseleave",t,!1),e.addEventListener("mousemove",t,!1),St[e.zcClippingId]={mouseover:n,mouseout:t,mouseenter:t,mouseleave:t,mousemove:t}}},Ut=function(e){if(e&&1===e.nodeType){var t=St[e.zcClippingId];if("object"==typeof t&&t){for(var n,r,a=["move","leave","enter","out","over"],i=0,o=a.length;o>i;i++)n="mouse"+a[i],r=t[n],"function"==typeof r&&e.removeEventListener(n,r,!1);delete St[e.zcClippingId]}}};It._createClient=function(){Ft.apply(this,b(arguments))},It.prototype.on=function(){return At.apply(this,b(arguments))},It.prototype.off=function(){return Xt.apply(this,b(arguments))},It.prototype.handlers=function(){return Yt.apply(this,b(arguments))},It.prototype.emit=function(){return $t.apply(this,b(arguments))},It.prototype.clip=function(){return Bt.apply(this,b(arguments))},It.prototype.unclip=function(){return Ht.apply(this,b(arguments))},It.prototype.elements=function(){return Mt.apply(this,b(arguments))},It.prototype.destroy=function(){return Pt.apply(this,b(arguments))},It.prototype.setText=function(e){return It.setData("text/plain",e),this},It.prototype.setHtml=function(e){return It.setData("text/html",e),this},It.prototype.setRichText=function(e){return It.setData("application/rtf",e),this},It.prototype.setData=function(){return It.setData.apply(this,b(arguments)),this},It.prototype.clearData=function(){return It.clearData.apply(this,b(arguments)),this},It.prototype.getData=function(){return It.getData.apply(this,b(arguments))},"function"==typeof define&&define.amd?define(function(){return It}):"object"==typeof module&&module&&"object"==typeof module.exports&&module.exports?module.exports=It:e.ZeroClipboard=It}(function(){return this||window}());