'use strict';

// Declare app level module which depends on filters, and services
angular.module('dashboard', [
    'ngRoute',
    'dashboard.controllers'
]).config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/',
        {templateUrl: 'partials/home.html',
         controller: 'home'
    });
    $routeProvider.when('/websites',
        {templateUrl: 'partials/websites.html',
         controller: 'websites'
    });
    $routeProvider.when('/pages',
        {templateUrl: 'partials/pages.html',
         controller: 'pages'
    });
     $routeProvider.when('/embed',
        {templateUrl: 'partials/embed.html',
         controller: 'embed'
    });
}]);