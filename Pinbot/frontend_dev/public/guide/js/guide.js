(function(){
	var Guide = function( setting ){
		return new Guide.prototype.init( setting );
	};
	Guide.prototype = {
		constructor: Guide,
		version: '',
		extend: function( origin , merge ){
			for( var i in merge ){
				origin[ i ] =  merge[i];
			};
			return origin;
		},
		loadCss: function(){
			var style = document.createElement('link');
			style.rel = 'stylesheet';
			style.href = this.setting.cssUrl;
			document.getElementsByTagName( 'head' )[0].appendChild( style );
		},
		init: function( setting ){
			if( window._guide ) delete _guide;
			this.setting = setting = this.extend({
				imgList: [],
				before: null,
				autoPlay: false,
				after: null,
				cssUrl: '/static/guide/css/guide.min.css',
				present: 0,
				length: 0
			},setting);
			_guide = this;
			this.loadCss();
			this.setting.length = this.setting.imgList.length;
			if( typeof setting.before == 'function' ){
				setting.before();
			}else{
				this.play();
			};
		},
		addShadow: function(){
			var div = document.createElement( 'div' );
			div.setAttribute( 'id' , 'JS_guide_shadow' );
			div.className = 'guide-backdrop fade in';
			document.getElementsByTagName( 'body' )[ 0 ].appendChild( div );
		},
		addContent: function( html , css ){
			var div = document.createElement( 'div' );
			css = css || '';
			html = '<div class="guide-dialog" id="JS_guide_dialog" style="' + css + '">' + html + '</div>';
			div.innerHTML = html;
			div.setAttribute( 'id' , 'JS_myModal' );
			div.className = 'guide-modal';
			div.style.cssText = 'display: block;';
			window._guide.addShadow();
			document.getElementsByTagName( 'body' )[ 0 ].appendChild( div );
			this.setPositionCenter();
		},
		setPositionCenter: function(){
			var dom = document.getElementById( 'JS_guide_dialog' ),
				dHeight = dom.offsetHeight,
				bHeight = document.documentElement.clientHeight,
				marginTop = dHeight < 250 ? ( bHeight - dHeight ) / 2 - 65 : ( bHeight - dHeight ) / 2;
			dom.style.marginTop =  marginTop + 'px';
		},
		play: function(){
			var setting = this.setting,
				img = setting.imgList[ setting.present ],
				html = '',
				css = 'width: ' + img.lWidth + 'px; height: ' + img.lHeight + 'px; background: url(' + img.src + ') 0 0 no-repeat;';
			this.removeNode();
			this.addContent( html , css );
			for( var i = 0 , l = img.btn.length ; i < l ; i++ ){
				var btn = img.btn[i],
					a = document.createElement( 'a' ),
					func = typeof btn.event == 'function' ? btn.event : setting.present >= setting.length - 1 ? window._guide.close : window._guide.play;
				a.style.cssText = 'position: absolute; display: inline-block; width:' + btn.bWidth + 'px; height: ' + btn.bHeight + 'px; left: ' + btn.left + 'px; top: ' + btn.top + 'px; cursor: pointer;';
				a.onclick = function(){
					func.call( window._guide );
				};
				document.getElementById( 'JS_guide_dialog' ).appendChild( a );
			};
			this.setPositionCenter();
			this.setting.present++;
		},
		removeNode: function(){
			var dom = document.getElementById( 'JS_guide_shadow' ),
				dom1 = document.getElementById( 'JS_myModal' );
			dom1.parentNode.removeChild( dom1 );
			dom.parentNode.removeChild( dom );
		},
		close: function(){
			this.removeNode();
			window._guide = null;
		}
	};
	Guide.prototype.init.prototype = Guide.prototype;

	window.Guide = Guide;
})();

Guide({
	before: function(){
		var html = '<div style=" padding: 70px 40px 50px; background: #fffbf8;border:solid 1px #ddd; font-size:14px;"><img src="/static/guide/img/avatar.png" width="44" height="55" style="position: absolute;top: -21px;left: -8px;"><a class="close-guide" onclick="window._guide.close();"></a><p style="line-height:35px;font-size:20px; font-weight:bold; letter-spacing:2px;color:#000;">你可以在购买简历前 <span style="color:#fc7524">提前了解候选人</span> 的意愿啦！<br>查看“新手引导”进一步了解<span style="color:#fc7524;">企业名片</span>使用方法吧！</p><div style="text-align:center; padding-top: 40px;"><a class="layer-button blue-button" onclick="window._guide.play();">开始了解</a></div></div>';
		window._guide.addContent( html , 'width:615px;');
	},
	imgList: [
		{
			src: '/static/guide/img/company_card1.jpg',
			lHeight: 598,
			lWidth: 1066,
			btn: [
				{
					bWidth: 220,
					bHeight: 60,
					left: 594,
					top: 235,
					event: null
				}
			]
		},
		{
			src: '/static/guide/img/company_card2.jpg',
			lHeight: 598,
			lWidth: 1066,
			btn: [
				{
					bWidth: 220,
					bHeight: 60,
					left: 594,
					top: 154
				}
			]
		},
		{
			src: '/static/guide/img/company_card3.jpg',
			lHeight: 597,
			lWidth: 1066,
			btn: [
				{
					bWidth: 210,
					bHeight: 48,
					left: 420,
					top: 283
				}
			]
		},
		{
			src: '/static/guide/img/company_card4.jpg',
			lHeight: 598,
			lWidth: 1066,
			btn: [
				{
					bWidth: 316,
					bHeight: 62,
					left: 368,
					top: 502
				}
			]
		},
		{
			src: '/static/guide/img/company_card5.jpg',
			lHeight: 598,
			lWidth: 1066,
			btn: [
				{
					bWidth: 67,
					bHeight: 24,
					left: 501,
					top: 549
				}
			]
		},
		{
			src: '/static/guide/img/company_card6.jpg',
			lHeight: 598,
			lWidth: 1066,
			btn: [
				{
					bWidth: 90,
					bHeight: 32,
					left: 313,
					top: 552
				},
				{
					bWidth: 418,
					bHeight: 329,
					left: 559,
					top: 109
				}
			]
		},
		{
			src: '/static/guide/img/company_card7.jpg',
			lHeight: 598,
			lWidth: 1066,
			btn: [
				{
					bWidth: 220,
					bHeight: 60,
					left: 594,
					top: 235
				}
			]
		},
		{
			src: '/static/guide/img/company_card8.jpg',
			lHeight: 598,
			lWidth: 1066,
			btn: [
				{
					bWidth: 87,
					bHeight: 31,
					left: 248,
					top: 493
				}
			]
		},
		{
			src: '/static/guide/img/company_card9.jpg',
			lHeight: 598,
			lWidth: 1066,
			btn: [
				{
					bWidth: 149,
					bHeight: 40,
					left: 478,
					top: 353
				}
			]
		}
	]
});