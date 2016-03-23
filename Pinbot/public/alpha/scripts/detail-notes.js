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
      $scope.addComment = function () {
        if (!$scope.comment.length) {
          setTimeout(function () {
            $('.notes-textbox textarea').focus();
          });
          return;
        }
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
