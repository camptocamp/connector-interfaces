odoo.define('theme_fluxdock.tooltips', function (require) {
    'use strict';

    // var Model = require('web.Model');
    var ajax = require('web.ajax');
    var base = require('web_editor.base');

    $(document).ready(function () {
        $('[data-toggle="popover"]').each(function(){
            var $el = $(this);
            var options = {
                html: true,
                content: $($el.data('htmlcontent')) ? $($el.data('htmlcontent')).html(): $el.data('content'),
                placement: $el.data('placement') ? $el.data('placement') : 'bottom',
                title: $el.data('title') ? $el.data('title') : '',
                trigger: 'click|hover|focus'
            }
            $el.popover(options);
            if($el.is(':visible') && $el.hasClass('popover_sticky')){
                $el.popover('show')
            }
        })
    });
});
