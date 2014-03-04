'use strict';

var dashboardControllers = angular.module('dashboard.controllers', []);

dashboardControllers.controller('home',
    ['$scope', '$http',
    function () {}
]);

dashboardControllers.controller('profile',
    ['$scope', 'Profile',
    function ($scope, Profile) {
        $scope.profile = Profile.get();
    }
]);

dashboardControllers.controller('websites',
    ['$scope', 'Website',
    function ($scope, Website) {
        $scope.newSite = {};

        $scope.addSite = function() {
            Website.save($scope.newSite);
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
            Website.update({websiteId: site.id}, site.updated);
            site.name = site.updated.name;
            site.url = site.updated.url;
        };

        $scope.sites = Website.query();
    }
]);

dashboardControllers.controller('pages',
    ['$scope', 'Website', 'Page',
    function($scope, Website, Page) {
        var selectedSiteId;

        var sites = Website.query();
        $scope.sites = sites;

        sites.$promise.then(function(sites) {
            selectedSiteId = sites[0].id;
            $scope.pages = Page.query({websiteId: sites[0].id});
        });

        $scope.selectSite = function(site) {
            selectedSiteId = site.id;
            $scope.pages = Page.query({websiteId: site.id});
        };

        $scope.newPage = {};
        $scope.addPage = function() {
            Page.save({websiteId: selectedSiteId}, $scope.newPage);
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
