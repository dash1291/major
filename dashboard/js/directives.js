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

dashboardDirectives.directive('btnWebsiteUpdate', ['websites',
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

dashboardDirectives.directive('btnWebsiteAdd', ['websites',
    function(websites) {
        return {
            restrict: 'A',
            link: function(scope, element) {
                element.bind('click', function() {
                    var modal = $(element).closest('.modal');
                    console.log(modal);
                    var addr = modal.find('.address').val();
                    var name = modal.find('.name').val();
                    websites.save({
                        name: name,
                        url: addr
                    });
                });
            }
        };
    }
]);