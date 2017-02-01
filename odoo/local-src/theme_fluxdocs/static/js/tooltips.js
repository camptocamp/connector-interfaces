odoo.define('theme_fluxdock.tooltips', function (require) {
    'use strict';

    // var Model = require('web.Model');
    var ajax = require('web.ajax');
    var base = require('web_editor.base');

    $(document).ready(function () {
        $('[data-toggle="popover"]').each(function(){
            $(this).popover({
                html: true,
                content: $($(this).data('htmlcontent')).html()
            });
            if($(this).is(':visible') && $(this).hasClass('popover_sticky')){
                $(this).popover('show')
            }
        })
    });
});
