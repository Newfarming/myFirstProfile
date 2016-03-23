// 跨浏览器取消冒泡
function cancelBubble(e){
    if (!e)
        var e = window.event;
        e.cancelBubble = true;
    if (e.stopPropagation)
        e.stopPropagation();
}
/**
 * 扩展数组对象，添加方法，根据索引删除元素
 * @param  {[type]} dx [description]
 * @return {[type]}    [description]
 */
Array.prototype.remove=function(dx)
{
    if(isNaN(dx)||dx > this.length)
        return false;
    for(var i = 0,n = 0;i < this.length;i++)
    {
        if(this[i] != this[dx])
        {
            this[n++] = this[i]
        }
    }
    this.length -= 1;
};
(function(){

    var app = angular.module( 'recoTaskApp' , [ 'ui.router' , 'app.config' , 'app.filter' ] ),
        $injector = angular.injector( [ 'app.utils' , 'app.django' ] ),
        id_url = $injector.get('id_url'),
        tmpl = $injector.get('tmpl'),
        static_url = $injector.get('static_url');

    app.config([
        '$stateProvider',
        '$urlRouterProvider',
        function( $stateProvider , $urlRouterProvider ){
            $urlRouterProvider.otherwise('/list');
            $stateProvider
                .state( 'list' , {
                    url: '/list',
                    controller: 'recoListCtrl',
                    templateUrl: tmpl( 'partner/task_time.html' )
                });
            $stateProvider
                .state( 'resume_first', {
                    url: '/resume_first',
                    templateUrl: tmpl('partner/resume_first.html'),
                    //controller: 'resumeFirstCtrl'
                });
        }
    ]);

    /*app.controller( 'resumeFirstCtrl' , [
        '$scope',
        '$http',
        '$state',
        function( $scope , $http , $state ){

        }
    ]);*/

    app.controller( 'recoListCtrl' , [
        '$scope',
        '$http',
        '$state',
        function( $scope , $http , $state ){

            // 获取本地存储对象
            var storage = window.localStorage;

            // init city
            $scope.city_list = [];

            // 搜索功能的两个list默认不展示
            $scope.showCityList = false;
            $scope.showHistoryList = false;

            // 已选择的城市
            $scope.selected_city = storage.getItem('selected_city') ? storage.getItem('selected_city').split(',') : [];

            // 搜索历史记录
            $scope.history_list = storage.getItem('history_list') ? storage.getItem('history_list').split(',') : [];

            // init keyword
            $scope.keyword = $scope.history_list.length === 0 ? '' : angular.copy($scope.history_list[$scope.history_list.length - 1]);

            // init examples
            $scope.examples = [];

            // init hot_tasks
            $scope.hot_tasks = [];

            //显示loading
            $scope.loading = true;

            //默认页
            $scope.current = 1;

            //显示弹窗
            $scope.showBackdrop = false;

            //获取数据
            $scope.getAjaxData = function(){

                $http.get( '/partner/reco_task_list/' , {
                    params: {
                                page: $scope.current,
                                city: $scope.selected_city,
                                keywords: $scope.keyword
                            }
                } )
                .success(function( res ){

                    //请求成功
                    if( res ){

                        //任务进行中
                        if( res.data && res.data.length > 0 ){
                            $scope.datas = res;
                            $scope.noAnyData = false;
                        }else{
                            $scope.noData();
                        };

                        if(res.all_citys.length != 0) {
                            $scope.city_list = res.all_citys;
                        };

                        if(res.examples.length != 0) {
                            $scope.examples = res.examples;
                        }

                        if(res.hot_tasks.length != 0) {
                            $scope.hot_tasks = res.hot_tasks;
                        }

                    }else{
                        $scope.noData();
                    };

                    $scope.loading = false;

                }).error(function(){

                    $scope.loading = false;
                    $scope.noData();

                });

            };

            //获取默认数据
            $scope.getAjaxData();

            //没有数据
            $scope.noData = function(){
                $scope.noAnyData = true;
            };

            //上一页
            $scope.prev = function(){
                if( $scope.current <= 1 ) return;
                $scope.loading = true;
                $scope.current--;
                $scope.getAjaxData();
            };

            //下一页
            $scope.next = function(){
                if( $scope.current >= $scope.datas.pages ) return;
                $scope.loading = true;
                $scope.current++;
                $scope.getAjaxData();
            };

            //接受任务弹窗开关
            $scope.toogleBackdrop = function( bool ){
                $scope.showBackdrop = bool;
            };

            //接受任务事件
            $scope.isShowLayer = function( $e , id , datas ){
                $scope.checkTask();
                $scope.viewFeed = false;
                if( datas.has_resume ){
                    $scope.toogleBackdrop( true );
                    $e.stopPropagation();
                    $scope.upload_url =  datas.upload_task_url + id;
                    $scope.select_url =  datas.select_resume_url + id + '/';
                }else{
                    location.href = datas.upload_task_url + id;
                };
            };


            //定制预览
            $scope.showViewDesc = true;
            $scope.viewFeed = false;

            //定制显示开关
            $scope.toggleView = function( bool ){
                $scope.viewFeed = bool;
            };

            //预览定制
            $scope.showFeed = function( task ){
                $scope.checkTask();
                $scope.toggleView( true );
                $scope.feedData = {
                    task: task,
                    feed: task.feed,
                    company: task.feed.company
                };
                $scope.refresh();
            };

            //切换职位详情
            $scope.toggleDesc = function(){
                $scope.showViewDesc = !$scope.showViewDesc;
                $scope.refresh();
            };

            //更新弹窗位置
            $scope.refresh = function(){
                if( !$scope.viewFeed ) return;
                setTimeout( function(){
                    $('.modal-dialog-view').css({
                        marginTop: ( $(window).height() - $('.modal-dialog-view').height() ) / 2 + 'px'
                    });
                }, 0);
            };

            // check_task
            $scope.checkTask = function(){
                $http.get('/partner/check_task/');
            }

            // toggle city list
            $scope.toggleCity = function(bool){
                $scope.showCityList = !bool;
            }

            // show history list
            $scope.showHistory = function(){
                if($scope.history_list.length != 0){
                    var $history = $('.history-list');
                    $history.show();
                    $scope.showHistoryList = true;
                }
            }

            // 历史记录列表项hover索引
            var hoveredNode = -1;

            $scope.toggleUpDown = function(e){
                var $history_node = $('.history-list').find('li');
                if(e.keyCode === 40) {
                    // 向下切换
                    if(hoveredNode != -1){
                        $history_node.eq(hoveredNode).removeClass('hovered');
                    }
                    hoveredNode++;
                    if (hoveredNode === $history_node.length) {
                        hoveredNode = 0;
                    }
                    $history_node.eq(hoveredNode).addClass('hovered');
                } else if (e.keyCode === 38) {
                    // 向上切换
                    if(hoveredNode != -1){
                        $history_node.eq(hoveredNode).removeClass('hovered');
                        hoveredNode--;
                    }
                    if (hoveredNode == -1) {
                        hoveredNode = $history_node.length - 1;
                    }
                    $history_node.eq(hoveredNode).addClass('hovered');
                } else if (e.keyCode === 13 && hoveredNode != -1) {
                    // 下拉列表展示时键入enter
                    $scope.keyword = $history_node.eq(hoveredNode)[0].innerText;
                    $scope.hideHistory();
                } else if (e.keyCode === 13) {
                    // 下拉列表隐藏时键入enter（发起筛选请求）
                    $scope.loading = true;
                    $scope.current = 1;
                    $scope.getAjaxData();
                    $scope.saveKeyword();
                    $scope.hideHistory();
                    return;
                } else if (e.keyCode === 188) {
                    // 限制输入英文逗号
                    $(e.target)[0].value = $(e.target)[0].value.replace(/[,]/g, "");
                }
                $scope.showHistory();
            }

            $scope.setHovered = function(e, index){
                $('.hovered').removeClass('hovered');
                var $history_node = $('.history-list').find('li');
                hoveredNode = index;
                $history_node.eq(hoveredNode).addClass('hovered');
            }

            $scope.clearHovered = function(){
                hoveredNode = -1;
                $('.hovered').removeClass('hovered');
            }

            // 点击body事件
            $('body').on('click', function(e){
                e.stopPropagation();
                var $target = $(e.target),
                    target_type = $target.attr('target_type');
                if (target_type != undefined){
                    return false;
                } else {
                    $scope.hideHistory();
                }
            });

            // hide history list
            $scope.hideHistory = function() {
                hoveredNode = -1;
                $('.hovered').removeClass('hovered');
                $('.history-list').hide();
                $scope.showHistoryList = false;
            }

            // 判断城市是否已选中
            $scope.isSelected = function(city) {
                for (var i = $scope.selected_city.length - 1; i >= 0; i--) {
                    if($scope.selected_city[i] === city){
                        return true;
                    }
                };
                return false;
            }

            $scope.setCity = function(city, e) {
                var $target = $(e.target);
                if ($target.hasClass('selected')) {
                    $target.removeClass('selected');
                    for(var i = 0,n = 0;i < $scope.selected_city.length;i++)
                    {
                        if($scope.selected_city[i] != city)
                        {
                            $scope.selected_city[n++] = $scope.selected_city[i]
                        }
                    }
                    $scope.selected_city.length -= 1;
                } else {
                    $target.addClass('selected');
                    $scope.selected_city.push(city);
                }
            };

            // 保存已选城市到本地存储
            $scope.saveCity = function() {
                storage.setItem('selected_city', $scope.selected_city);
                $scope.showCityList = false;
            };

            $scope.setKeyword = function(item) {
                $scope.keyword = item;
                $scope.loading = true;
                $scope.current = 1;
                $scope.getAjaxData();
                $scope.saveKeyword();
            }

            // 保存keyword到本地存储
            $scope.saveKeyword = function() {
                if ($scope.keyword === '') {
                    return;
                };
                if($scope.history_list.length > 0){
                    for (var i = $scope.history_list.length - 1; i >= 0; i--) {
                        if($scope.history_list[i] === $scope.keyword){
                            return false;
                        }
                    };
                    if ($scope.history_list.length === 5) {
                        $scope.history_list.shift();
                    }
                    $scope.history_list.push($scope.keyword);
                } else {
                    $scope.history_list.push($scope.keyword);
                }
                storage.setItem('history_list', $scope.history_list);
            }

            // 点击筛选任务
            $scope.clickSearch = function() {
                $scope.loading = true;
                $scope.current = 1;
                $scope.getAjaxData();
                $scope.saveKeyword();
            }

            // 点击热门职位
            $scope.clickKeyword = function(item) {
                $scope.setKeyword(item);
                $scope.saveKeyword();
                $scope.loading = true;
                $scope.current = 1;
                $scope.getAjaxData();
            }

            // 点击红叉删除历史记录
            $scope.deleteHistory = function(e, r_index) {
                cancelBubble(e);
                var index = $scope.history_list.length - r_index - 1;
                $scope.history_list.remove(index);
                storage.setItem('history_list', $scope.history_list);
            }
        }
    ]);

    app.filter( 'formatCity' , function(){
        return function( arr ){
            var newArr = [];
            if(arr.length === 0) {
                return '请选择';
            } else if(arr.length < 3) {
                return arr.join(',');
            } else {
                for (var i = 0; i < 2; i++) {
                    newArr.push(arr[i]);
                };
                return newArr.join(',') + '...';
            }
        }
    });

    app.filter( 'formatExamples' , function(){
        return function( arr ){
            var newArr = [];
            for (var i = 0; i < arr.length; i++) {
                newArr.push(arr[i]);
            };
            return newArr.join(';');
        }
    });

    app.filter('reverse', function() {
        return function(items) {
            return items.slice().reverse();
        };
    });

})();

