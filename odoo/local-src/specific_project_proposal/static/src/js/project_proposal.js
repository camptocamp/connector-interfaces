odoo.define('specific_project_proposal.specific_project_proposal', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var website = require('website.website');

var _t = core._t;

if(!$('.oe_website_proposals').length) {
    return $.Deferred().reject("DOM doesn't contain '.oe_website_proposals'");
}

    $('.hide_proposal').on('click', function (ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        ajax.jsonRpc($link.data('href'), 'call', {}).then(function () {
            $link.parents('.proposal_item').first().remove();
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

});
