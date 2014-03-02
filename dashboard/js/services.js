'use strict';

var conceptualServices = angular.module('dashboard.services', ['ngResource']);

conceptualServices.factory('profile',
    ['$resource',
    function($resource) {
        return $resource('/api/profile/');
    }
]);

conceptualServices.factory('websites',
    ['$resource',
    function($resource) {
        return $resource('/api/websites/:websiteId', {}, {
            update: {method: 'PUT'}
        });
    }
]);

conceptualServices.factory('pages',
    ['$resource',
    function($resource) {
        return $resource('/api/websites/:websiteId/pages/:pageId', {}, {
            update: {method: 'PUT'}
        });
    }
]);
