odoo.define('specific_project_proposal.specific_project_proposal', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var website = require('website.website');

var _t = core._t;

if(!$('.oe_website_proposals').length) {
    return $.Deferred().reject("DOM doesn't contain '.oe_website_proposals'");
}

    $('.hide_listing_item').on('click', function (ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        ajax.jsonRpc($link.data('href'), 'call', {}).then(function () {
            $link.parents('.list-item').first().remove();
        });
    });

    $('.publish_proposal').on('click', function (ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        ajax.jsonRpc($link.data('href'), 'call', {}).then(function() {
            var to_show = $link.find('.hidden');
            var to_hide = $link.find('span').not('.hidden');
            to_show.removeClass('hidden');
            to_hide.addClass('hidden');
        });
    });

    $("div.input-group span.fa-calendar").on('click', function(e) {
        $(e.currentTarget).closest("div.date").datetimepicker({
            useSeconds: true,
            icons : {
                time: 'fa fa-clock-o',
                date: 'fa fa-calendar',
                up: 'fa fa-chevron-up',
                down: 'fa fa-chevron-down'
            },
        });
    });
});
