$.Tip=function(t,e){var i=function(t){return new i.prototype.init(t)};return i.prototype={constructor:i,init:function(e){this.setting=e=t.extend({selector:".JS_tip_a",mouseHandle:"click",cssText:"",closeWay:"clickOutSide",success:null,content:"",className:"",needAjax:!0,callback:null},e);var i=this;window.__tip=this,t(document).on(e.mouseHandle,e.selector,function(e){return t(this).hasClass("JS_sock_tip")?!1:(t(".JS_sock_tip").not(t(this)).removeClass("JS_sock_tip"),i.setting.eventTarget=this,t(this).addClass("JS_sock_tip"),i.showModel(),i.bindHideEvent(),i.setPosition(),i.setting.needAjax?i.loadData():"function"==typeof i.setting.callback&&i.setting.callback(),void e.stopPropagation())})},getHtml:function(){var t='<p style="text-align: center;"><img src="http://www.pinbot.me/static/alpha/images/loading.gif" alt="" style="vertical-align: -3px; margin-right:10px;">加载中...</p>';return t},showModel:function(){t("#JS_tip_model").remove();var e="";e=this.setting.needAjax?this.getHtml():this.setting.content,e='<div class="tip-model '+this.setting.className+'" id="JS_tip_model" style="'+this.setting.cssText+'">'+e+"</div>",t("body").append(e)},setPosition:function(){var e,i,s=t(this.setting.eventTarget),o=s.offset(),n=s.outerWidth(),a=s.outerHeight(),l=t("#JS_tip_model"),c=l.outerWidth(),r=l.outerHeight(),p=t(window).width(),d=t(document).height(),g=(t(document).scrollTop(),o.left+n/2+c/2+5>p),u=o.left+n/2-c/2<0,_=a+r+o.top+5>d;g&&_?(i=o.top+a-r,e=o.left-5-c,l.addClass("right-bottom-side")):g||!_||u?g&&!_?(i=o.top+a+5,e=o.left+n-c,l.addClass("right-top-side")):u&&!_?(i=o.top-5,e=o.left+n+5,l.addClass("left-top-side")):u&&_?(i=o.top+a-r,e=o.left+n+5,l.addClass("left-bottom-side")):(i=o.top+a+5,e=o.left+n/2-c/2):(i=o.top-5-r,e=o.left+n/2-c/2,l.addClass("down-side")),l.css({left:e+"px",top:i+"px"})},bindHideEvent:function(){var e=this,i=function(s){var o=t(e.setting.selector);if(s.target!=t("#JS_tip_model")[0]&&!t(s.target).closest("#JS_tip_model").length){var n=t(s.target),a=n.closest(".JS_sock_tip");n.hasClass("JS_sock_tip")?t(".JS_sock_tip").not(n).removeClass("JS_sock_tip"):a.length?t(".JS_sock_tip").not(a).removeClass("JS_sock_tip"):t(".JS_sock_tip").removeClass("JS_sock_tip"),window._tipAjax&&(window._tipAjax.abort(),window._tipAjax=null),t(document).off("click",i),-1==t.inArray(s.target,o)&&t("#JS_tip_model").remove()}};t(document).on("click",document,i)},loadData:function(e){var i=this,s=t(e||i.setting.eventTarget),o=t.extend(!0,{},s.data()),n=o.method?o.method:"get",a=o.url;delete o.url,i.setting.url=a,window._tipAjax=t[n](a,o,function(t){t&&("function"==typeof i.setting.success?i.setting.success.apply(i,[t]):i.insertHtml(t))})},insertHtml:function(e){var i=this,s=t("#JS_tip_model"),o="",n=e.data;if(!s.length)return!1;if(n.length){o+='<table cellpadding="0" cellspacing="0" class="ajax-tip-list" width="100%">';for(var a=0,l=n.length;l>a;a++){var c=n[a];o+="<tr>";for(var r in c)o+="<td>"+c[r]+"</td>";o+="</tr>"}o+="</table>"}else o+='<p class="text-center">暂无数据！</p>';o+='<p class="tip-pages clearfix">',e.current>1&&(o+='<a class="JS_tip_page" href="javascript:;" data-url="'+this.setting.url+'" data-page="'+(e.current-1)+'">上一页</a>'),e.current<e.pages&&(o+='<a class="JS_tip_page" href="javascript:;" data-url="'+this.setting.url+'" data-page="'+(e.current+1)+'">下一页</a>'),o+="</p>",s.html(o),this.setPosition(i.setting.eventTarget),t(".JS_tip_page").on("click",function(){i.loadData(this)}),"function"==typeof this.setting.callback&&this.setting.callback()}},i.prototype.init.prototype=i.prototype,function(t){return i(t)}}(jQuery);