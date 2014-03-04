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
        var updatedSite;
        $scope.newSite = {};
        $scope.updated = {};
        $scope.deleted = {};

        $scope.addSite = function() {
            Website.save($scope.newSite);
            $scope.sites.push($scope.newSite);
            $scope.newSite = {
                name: '',
                url: ''
            };
        };

        $scope.editSiteOpen = function(site) {
            updatedSite = site;
            $scope.updated = {
                'name': site.name,
                'url': site.url
            };
        };

        $scope.updateSite = function() {
            Website.update({websiteId: updatedSite.id}, $scope.updated);
            updatedSite.name = $scope.updated.name;
            updatedSite.url = $scope.updated.url;
        };

        $scope.deleteSiteOpen = function(site) {
            $scope.deleted = site;
        };

        $scope.deleteSite = function() {
            Website.delete({websiteId: $scope.deleted.id});
            $scope.sites.pop($scope.deleted);
        };

        $scope.sites = Website.query();
    }
]);

dashboardControllers.controller('pages',
    ['$scope', 'Website', 'Page',
    function($scope, Website, Page) {
        var selectedSiteId;
        var updatedPage;
        $scope.updated = {};
        $scope.deleted = {};

        var sites = Website.query();
        $scope.sites = sites;

        sites.$promise.then(function(sites) {
            if (sites[0]) {
                selectedSiteId = sites[0].id;
                $scope.pages = Page.query({websiteId: sites[0].id});
            }
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

        $scope.editPageOpen = function(page) {
            updatedPage = page;
            console.log(updatedPage);
            $scope.updated = {
                url: page.url,
                name: page.name
            };
        };

        $scope.updatePage = function() {
            Page.update({websiteId: selectedSiteId, pageId: updatedPage.id}, $scope.updated);
            updatedPage.name = $scope.updated.name;
            updatedPage.url = $scope.updated.url;
        };

        $scope.deletePageOpen = function(page) {
            $scope.deleted = page;
        };

        $scope.deletePage = function() {
            Page.delete({websiteId: selectedSiteId, pageId: $scope.deleted.id});
            $scope.pages.pop($scope.deleted);
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
