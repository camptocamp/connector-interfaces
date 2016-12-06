odoo.define('specific_membership.image_upload', function (require) {
"use strict";

    var core = require('web.core');
    var website = require('website.website');

    if(!$('.imgupload').length) {
        return $.Deferred().reject("DOM doesn't contain '.imgupload'");
    }

    $('.imgupload').each(function(){
        $(this).imgupload({
            allowedFormats: ['jpg', 'jpeg', 'png'],
            previewWidth: $(this).data('preview-width')
        })
    });

});
