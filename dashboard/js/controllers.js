var dashboardControllers = angular.module('dashboard.controllers', []);

dashboardControllers.controller('home', ['$scope', '$http',
  function ($scope, $http) {
    alert("hi there");

  }]);

dashboardControllers.controller('websites', ['$scope', '$http',
  function ($scope, $http) {

  }]);

dashboardControllers.controller('pages', ['$scope', '$routeParams',
  function($scope, $routeParams) {
  }]);