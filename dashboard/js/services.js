'use strict';

var conceptualServices = angular.module('dashboard.services', ['ngResource']);

conceptualServices.config(['$httpProvider', function($http) {
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

conceptualServices.factory('Profile',
    ['$resource',
    function($resource) {
        return $resource('/api/profile/');
    }
]);

conceptualServices.factory('Website',
    ['$resource',
    function($resource) {
        return $resource('/api/websites/:websiteId', {}, {
            save: {method: 'POST'},
            update: {method: 'PUT'}
        });
    }
]);

conceptualServices.factory('Page',
    ['$resource',
    function($resource) {
        return $resource('/api/websites/:websiteId/pages/:pageId', {}, {
            save: {method: 'POST'},
            update: {method: 'PUT'}
        });
    }
]);
