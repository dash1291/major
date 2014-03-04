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
    ['$scope', 'websites', 'pages',
    function($scope, websites, pages) {
        var selectedSiteId;

        var sites = websites.query();
        $scope.sites = sites;

        sites.$promise.then(function(sites) {
            selectedSiteId = sites[0].id;
            $scope.pages = pages.query({websiteId: sites[0].id});
        });

        $scope.selectSite = function(site) {
            selectedSiteId = site.id;
            $scope.pages = pages.query({websiteId: site.id});
        };

        $scope.newPage = {};
        $scope.addPage = function() {
            pages.save({websiteId: selectedSiteId}, $scope.newPage);
            $scope.pages.push($scope.newPage);
            $scope.newPage = {
                name: '',
                url: ''
            };
        };
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
