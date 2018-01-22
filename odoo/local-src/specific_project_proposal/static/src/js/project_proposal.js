odoo.define('specific_project_proposal.specific_project_proposal', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var website = require('website.website');
var msg_tool = require('cms_status_message.tool');

var _t = core._t;

// TODO: move this to fluxdock_theme as it's general stuff now


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

    // enable datetimepicker
    $("div.date input").datetimepicker({
        useSeconds: true,
        icons : {
            time: 'fa fa-clock-o',
            date: 'fa fa-calendar',
            up: 'fa fa-chevron-up',
            down: 'fa fa-chevron-down'
        }
    });
    // show it also with calendar icon
    // FIXME: is not working ATM :S
    $("div.date span.fa-calendar").on('click', function() {
        $(this).closest("div.date").find('input').datetimepicker('show');
    });

    // TMP fix to prevent proposal submit w/ end date < start date
    // waiting for default validation in cms_form
    if ( $('.cms_form_wrapper [name=start_date]').length && $('.cms_form_wrapper [name=stop_date]').length){
        $('.cms_form_wrapper [name=start_date], .cms_form_wrapper [name=stop_date]').change(function(){
            var $start = $('.cms_form_wrapper [name=start_date]');
            var $stop = $('.cms_form_wrapper [name=stop_date]');
            if ($start.val() && $stop.val()) {
                if( moment($start.val()) > moment($stop.val()) ) {
                    var start_label = $start.closest('.form-group').find('label').text(),
                        stop_label = $stop.closest('.form-group').find('label').text(),
                        // FIXME: dirty hack to enforce translation that sometime does not work w/ JS
                        txt_en = 'End date must be greate than start date',
                        txt_de = 'Enddatum muss grösser sein als Startdatum',
                        txt = $('html').attr('lang') == 'de-DE' ? txt_de: txt_en,
                        msg = {
                            'msg': txt,
                            'type': 'danger',
                            'dismissible': false
                        }
                    // wipe existing
                    $('#' + $stop.attr('id') + 'msg').remove();
                    // inject
                    $(msg_tool.render_messages(msg))
                        .hide().insertAfter($stop.closest('.form-group'))
                        .fadeIn('slow').attr('id', $stop.attr('id') + 'msg');
                    $('.cms_form_wrapper form .form-controls button[type=submit]')
                        .attr('disabled', 'disabled').attr('title', _('You have errors.'));
                } else {
                    $('#' + $stop.attr('id') + 'msg').remove();
                    $('.cms_form_wrapper form .form-controls button[type=submit]')
                        .attr('disabled', null).attr('title', '');
                }
            }
        })
    }
});
