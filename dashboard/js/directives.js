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

dashboardDirectives.directive('btnWebsiteSave', ['websites',
    function(websites) {
        return {
            restrict: 'A',
            link: function(scope, element) {
                element.bind('click', function() {
                    var modal = $(element).closest('.modal');
                    var addr = modal.find('.address');
                    var name = modal.find('.name');
                    websites.save({
                        name: name,
                        address: addr
                    });
                });
            }
        };
    }
]);
