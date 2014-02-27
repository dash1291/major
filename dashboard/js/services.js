'use strict';

var conceptualServices = angular.module('dashboard.services', ['ngResource']);

conceptualServices.factory('profile',
    ['$resource',
    function($resource) {
        return $resource('/api/profile/', {}, {
          query: {method: 'GET'}
        });
    }
]);

conceptualServices.factory('Website',
    ['$resource',
    function($resource) {
        return $resource('/api/websites/:websiteId', {}, {
          query: {method: 'GET', params: {websiteId: ''}, isArray: true}
        });
    }
]);
