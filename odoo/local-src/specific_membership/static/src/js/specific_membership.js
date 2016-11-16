odoo.define('specific_membership.portal_profile', function (require) {
'use strict';

var Model = require('web.Model');
var ajax = require('web.ajax');
var core = require('web.core');
var base = require('web_editor.base');

var _t = core._t;

var lastsearch;

if(!$('.js_select2_categories').length) {
    return $.Deferred().reject("DOM doesn't contain '.js_select2_categories'");
}

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
        query: function (query) {
            ajax.jsonRpc("/web/dataset/call_kw_pub", 'call', {
    			model: 'res.partner.category',
    			method: 'search_read',
    			args: [],
    			kwargs: {
    				fields: ['display_name'],
    				context: base.get_context()
    			}
    		}).then(function (data) {
                var tags = { results: [] };
                data.sort(function(a, b) {
                    return a.display_name.localeCompare(b.display_name);
                });
                _.each(data, function(x) {
                    tags.results.push({ id: x.id, text: x.display_name, isNew: false });
                });
                lastsearch = tags;
                query.callback(tags);
            });
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
	query: function (query) {
		ajax.jsonRpc("/web/dataset/call_kw_pub", 'call', {
			model: 'partner.project.expertise',
			method: 'search_read',
			args: [],
			kwargs: {
				fields: ['name'],
				context: base.get_context()
			}
		}).then(function (data) {
			var tags = { results: [] };
			_.each(data, function(x) {
			    tags.results.push({ id: x.id, text: x.name, isNew: false });
			});
			lastsearch = tags;
			query.callback(tags);
	        });
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
