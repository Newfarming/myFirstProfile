window.Guide = (function(){
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
		init: function( setting ){
			if( window._guide ) delete _guide;
			this.setting = setting = this.extend({
				imgList: [],
				before: null,
				autoPlay: false,
				after: null,
				cssUrl: 'newguide.css',
				present: 0,
				length: 0
			},setting);
			_guide = this;
			this.setting.length = this.setting.imgList.length;
			if( typeof setting.before == 'function' ){
				setting.before();
			}else{
				this.play();
			};
		},
		play: function(){
			
			var setting = this.setting;

			if( setting.present > setting.imgList.length - 1 ){
				this.finish();
				return;
			};

			this.loading( 'block' );
			this.toggleSkipBtn( 'none' );

			if( setting.present > 0 ){
				this.removeNode();
			};

			this.loadBgImg();
		},
		toggleSkipBtn: function( display ){
			document.getElementById('JS_skip').style.display = display;
		},
		loading: function( status ){
			document.getElementById('JS_myModal').style.display = status;
		},
		loadBgImg: function(){
			var setting = this.setting,
				present = setting.imgList[ setting.present ],
				img = new Image(),
				bgCss = 'background: url(' + present.src + ') center top no-repeat;',
				that = this;
			img.onload = img.onerror = function(){
				document.getElementsByTagName( 'body' )[0].style.cssText = bgCss;
				document.documentElement.scrollTop = 0;
				document.body.scrollTop = 0;
				img = null;
				that.loadBtn();
			};
			img.src = present.src;
		},
		loadBtn: function(){
			var setting = this.setting,
				present = setting.imgList[ setting.present ];

			document.getElementById( 'JS_content' ).style.height = present.lHeight + 'px';

			if( !present.preventShowMouse ){
				this.igShowScrollImg( present.lHeight );
			};
			
			for( var i = 0 , l = present.btn.length ; i < l ; i++ ){
				var btn = present.btn[i],
					a = document.createElement( 'a' ),
					func = typeof btn.event == 'function' ? btn.event : setting.present >= setting.length - 1 ? window._guide.finish : window._guide.play;

				if( btn.hasEffect ){
					a.innerHTML = '<span></span>' + 
							        '<em class="swave1"></em>' +
							        '<em class="swave2"></em>' +
							        '<em class="swave3"></em>';
					a.className = 'btn';
				}else{
					a.innerHTML = btn.html;
					a.className = btn.className;
				};

				a.style.cssText = 'left:' + btn.left + 'px; top: ' + btn.top + 'px;';

				a.onclick = function(){
					func.call( window._guide );
				};

				document.getElementById( 'JS_btns' ).appendChild( a );
			
			};

			this.loading( 'none' );

			this.toggleSkipBtn( 'inline-block' );

			this.setting.present++;

		},
		igShowScrollImg: function( lHeight ){
			var sHeight = screen.height;
			if( lHeight > sHeight ){
				document.getElementById( 'JS_mouse' ).style.display = 'inline-block';
				if( !window.tm ){
					document.getElementById( 'JS_mouse' ).className = 'mouse active';
					tm = setTimeout(function(){
						document.getElementById( 'JS_mouse' ).className = 'mouse';
						tm = null;
					}, 3000 );
				};
			};
		},
		removeNode: function(){
			var dom = document.getElementById( 'JS_btns' );
			dom.innerHTML = '';
		},
		finish: function(){
			this.toggleSkipBtn( 'none' );
			this.removeNode();
			document.getElementById('JS_finish').style.display = 'block';
			window._guide = null;
		}
	};
	Guide.prototype.init.prototype = Guide.prototype;

	return Guide;
})();

Guide({
	imgList: [
		{
			src: '/static/tutorial/1.jpg',
			lHeight: 1298,
			btn: [
				{
					left: 563,
					top: 1191,
					hasEffect: true,
					event: null
				}
			]
		},
		{
			src: '/static/tutorial/2.jpg',
			lHeight: 1428,
			btn: [
				{
					left: 572,
					top: 1354,
					hasEffect: true
				}
			]
		},
		{
			src: '/static/tutorial/3.jpg',
			lHeight: 1579,
			btn: [
				{
					left: 571,
					top: 1388,
					hasEffect: true
				}
			]
		},
		{
			src: '/static/tutorial/4.jpg',
			lHeight: 1496,
			btn: [
				{
					left: 1012,
					top: 743,
					hasEffect: true
				},
				{
					left: 927,
					top: 1382,
					className: 'default-btn step4',
					html: ''
				}
			]
		},
		{
			src: '/static/tutorial/5.jpg',
			lHeight: 2033,
			btn: [
				{
					left: 1046,
					top: 424,
					hasEffect: true
				}
			]
		},
		{
			src: '/static/tutorial/6.jpg',
			lHeight: 2033,
			preventShowMouse: true,
			btn: [
				{
					left: 431,
					top: 767,
					hasEffect: true
				},
				{
					left: 622,
					top: 740,
					className: 'default-btn step6',
					html: ''
				}
			]
		},
		{
			src: '/static/tutorial/7.jpg',
			lHeight: 1226,
			btn: [
				{
					left: 173,
					top: 551,
					hasEffect: true
				}
			]
		}
	]
});