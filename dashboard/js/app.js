'use strict';

// Declare app level module which depends on filters, and services
angular.module('dashboard', [
    'ngRoute',
    'dashboard.controllers'
]).config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/websites',
        {templateUrl: 'partials/websites.html',
         controller: 'websites'
    });
    $routeProvider.when('/pages',
        {templateUrl: 'partials/pages.html',
         controller: 'pages'
    });
}]);