odoo.define('website_portal_profile.portal_profile', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var website = require('website.website');

var _t = core._t;

var lastsearch;

// if(!$('.portal_profile').length) {
//     return $.Deferred().reject("DOM doesn't contain '.portal_profile'");
// }

    $('input.js_select2_categories').select2({
        tags: true,
        tokenSeparators: [",", " ", "_"],
        lastsearch: [],
        createSearchChoice: function (term) {
            if ($(lastsearch).filter(function () { return this.text.localeCompare(term) === 0;}).length === 0) {
		return {
			id: "_" + $.trim(term),
			text: $.trim(term) + ' *',
			isNew: true,
		};
            }
        },
        formatResult: function(term) {
            if (term.isNew) {
                return '<span class="label label-primary">New</span> ' + _.escape(term.text);
            }
            else {
                return _.escape(term.text);
            }
        },
        ajax: {
            url: '/my/get_categories',
            dataType: 'json',
            data: function(term) {
                return {
                    q: term,
                    l: 50
                };
            },
            results: function(data) {
                var ret = [];
                _.each(data, function(x) {
                    ret.push({ id: x.id, text: x.name, isNew: false });
                });
                lastsearch = ret;
                return { results: ret };
            }
        },
        // Default elements from the input value
        initSelection: function (element, callback) {
            var data = [];
            _.each(element.data('init-value'), function(x) {
                data.push({ id: x.id, text: x.name, isNew: false });
            });
            element.val('');
            callback(data);
        },
    });
    $('input.js_select2_expertises').select2({
        tags: true,
        tokenSeparators: [",", " ", "_"],
        lastsearch: [],
        createSearchChoice: function (term) {
            if ($(lastsearch).filter(function () { return this.text.localeCompare(term) === 0;}).length === 0) {
		return {
			id: "_" + $.trim(term),
			text: $.trim(term) + ' *',
			isNew: true,
		};
            }
        },
        formatResult: function(term) {
            if (term.isNew) {
                return '<span class="label label-primary">New</span> ' + _.escape(term.text);
            }
            else {
                return _.escape(term.text);
            }
        },
        ajax: {
            url: '/my/get_expertises',
            dataType: 'json',
            data: function(term) {
                return {
                    q: term,
                    l: 50
                };
            },
            results: function(data) {
                var ret = [];
                _.each(data, function(x) {
                    ret.push({ id: x.id, text: x.name, isNew: false });
                });
                lastsearch = ret;
                return { results: ret };
            }
        },
        // Default tags from the input value
        initSelection: function (element, callback) {
            var data = [];
            _.each(element.data('init-value'), function(x) {
                data.push({ id: x.id, text: x.name, isNew: false });
            });
            element.val('');
            callback(data);
        },
    });

});
