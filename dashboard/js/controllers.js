var dashboardControllers = angular.module('dashboard.controllers', []);

dashboardControllers.controller('home',
    ['$scope', '$http',
    function ($scope, $http) {

    }
]);

dashboardControllers.controller('profile',
    ['$scope', 'profile',
    function ($scope, profile) {
        $scope.profile = profile.query();
    }
]);

dashboardControllers.controller('websites',
    ['$scope', 'Website',
    function ($scope, website) {
        $scope.sites = website.query();
    }
]);

dashboardControllers.controller('pages',
    ['$scope', '$routeParams',
    function($scope, $routeParams) {
        $scope.pages = [
            {url: '/home.html'},
            {url: '/about.html'},
            {url: '/post1.html'}
        ];
    }
]);

dashboardControllers.controller('embed',
    ['$scope', '$routeParams',
    function($scope, $routeParams) {
    }
]);

dashboardControllers.controller('settings',
    ['$scope', '$routeParams',
    function($scope, $routeParams) {
    }
]);
