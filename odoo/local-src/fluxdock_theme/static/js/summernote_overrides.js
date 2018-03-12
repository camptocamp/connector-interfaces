odoo.define('theme_fluxdock.summernote_overrides', function (require) {
    'use strict';
    require('summernote/summernote'); // wait that summernote is loaded
    var summernote = require('web_editor.summernote');
    var core = require('web.core');
    var _t = core._t;
    // add `20` and `40`
    summernote.options.fontSizes = [_t('Default'), 8, 9, 10, 11, 12, 14, 18, 20, 24, 36, 40, 48, 62];
    return summernote;
});
