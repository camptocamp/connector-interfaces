odoo.define('theme_fluxdock.publish', function (require) {
    'use strict';

    // var Model = require('web.Model');
    var ajax = require('web.ajax');
    var base = require('web_editor.base');
    var msg_tool = require('cms_status_message.tool');
    var core = require('web.core');
    var _t = core._t;

    $(document).ready(function() {
        if($('section.signup_login').length && $('#user-menu').length){
            // dirty trick to remove login/signup snippet if the user is not logged-in
            $('section.signup_login').remove();
        }
    });

    // unbind existing publish widget event
    $(document).off('click','.js_publish_management .js_publish_btn');

    $(document).on('click', '.js_publish_management .js_publish_btn', function (e) {
        // original publish handler just updates the buttons and trigger publishing
        // we need to redirect after a while to user's home
        e.preventDefault();
        var $data = $(this).parents(".js_publish_management:first");
        ajax.jsonRpc(
            '/flux/publisher', 'call',
            {'id': +$data.data('id'), 'object': $data.data('object')}
        ).then(function (result) {
            if (result.ok){
                $data.toggleClass("css_unpublished css_published");
                $data.parents("[data-publish]").attr("data-publish", + result ? 'on' : 'off');
            }

            // inject status message
            var msg;
            if (result.status) {
                msg = {
                    'msg': _t('Item published.'),
                    'title': _t('Info')
                }
            } else {
                msg = {
                    'msg': _t('Item unpublished.'),
                    'title': _t('Warning'),
                    'type': 'warning'
                }
            }
            // wipe existing
            $('.status_message').remove();
            // inject new
            $(msg_tool.render_messages(msg)).hide().prependTo('main').fadeIn('slow');

            if(result.redirect){
                window.setTimeout(function() {
                    location.href = result.redirect;
                }, 2000);
            }
        }).fail(function (err, data) {
            error(data, '/web#return_label=Website&model='+$data.data('object')+'&id='+$data.data('id'));
        });
    });
});
