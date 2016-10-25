odoo.define('specific_membership.image_upload', function (require) {
"use strict";

var core = require('web.core');
var website = require('website.website');

if(!$('.o_website_portal_details').length) {
    return $.Deferred().reject("DOM doesn't contain '.o_website_portal_details'");
}
    $('.imgupload').imgupload({
        allowedFormats: ['jpg', 'jpeg', 'png'],
    });

});
