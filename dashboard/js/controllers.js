var dashboardControllers = angular.module('dashboard.controllers', []);

dashboardControllers.controller('home',
    ['$scope', '$http',
    function ($scope, $http) {

    }
]);

dashboardControllers.controller('websites',
    ['$scope', '$http',
    function ($scope, $http) {
        $scope.sites = [
            {name: 'blog', domain: 'ashishdubey.com'},
            {name: 'blog2', domain: 'ashishdubey1.com'},
            {name: 'blog3', domain: 'ashishdubey1.com'},
            {name: 'blog3', domain: 'ashishdubey1.com'}


        ];
    }
]);

dashboardControllers.controller('pages',
    ['$scope', '$routeParams',
    function($scope, $routeParams) {
        $scope.pages = [
            {url: '/home.html'},
            {url: '/about.html'}
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
