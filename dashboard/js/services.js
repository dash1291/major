'use strict';

var conceptualServices = angular.module('dashboard.services', ['ngResource']);

conceptualServices.config(['$httpProvider', function($http) {
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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
            save: {method: 'POST'},
            update: {method: 'PUT'}
        });
    }
]);

conceptualServices.factory('pages',
    ['$resource',
    function($resource) {
        return $resource('/api/websites/:websiteId/pages/:pageId', {}, {
            save: {method: 'POST'},
            update: {method: 'PUT'}
        });
    }
]);
