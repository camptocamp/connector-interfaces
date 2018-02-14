odoo.define('theme_fluxdock.lazyload', function (require) {
    'use strict';

    require('web.dom_ready');

    if(!$('.lazy').length) {
        return $.Deferred().reject("DOM doesn't contain '.lazy'");
    }

    $(function() {
      $('.lazy').Lazy();
    });

});
