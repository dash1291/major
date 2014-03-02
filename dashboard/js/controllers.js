'use strict';

var dashboardControllers = angular.module('dashboard.controllers', []);

dashboardControllers.controller('home',
    ['$scope', '$http',
    function () {}
]);

dashboardControllers.controller('profile',
    ['$scope', 'profile',
    function ($scope, profile) {
        $scope.profile = profile.get();
    }
]);

dashboardControllers.controller('websites',
    ['$scope', 'websites',
    function ($scope, websites) {

        $scope.sites = websites.query();
    }
]);

dashboardControllers.controller('pages',
    ['$scope', '$routeParams',
    function($scope) {
        $scope.pages = [
            {url: '/home.html'},
            {url: '/about.html'},
            {url: '/post1.html'}
        ];
    }
]);

dashboardControllers.controller('embed',
    ['$scope', '$routeParams',
    function() {}
]);

dashboardControllers.controller('settings',
    ['$scope', '$routeParams',
    function() {}
]);
