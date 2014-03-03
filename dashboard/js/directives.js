'use strict';

var dashboardDirectives = angular.module('dashboard.directives', []);

dashboardDirectives.directive('editButton', function() {
    return {
        restrict: 'A',
        link: function(scope, element) {
            element.bind('click', function() {
                $(element).siblings('.modal').modal();
            });
        }
    };
});
