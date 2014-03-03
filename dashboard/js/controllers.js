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
        $scope.newSite = {};

        $scope.addSite = function() {
            websites.save($scope.newSite);
            $scope.sites.push($scope.newSite);
            $scope.newSite = {
                name: '',
                url: ''
            };
        };

        $scope.tmpSite = {};

        $scope.editSiteOpen = function(site) {
            site.updated = {
                'name': site.name,
                'url': site.url
            };
        };

        $scope.updateSite = function(site) {
            websites.update({websiteId: site.id}, site.updated);
            site.name = site.updated.name;
            site.url = site.updated.url;
        };

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
