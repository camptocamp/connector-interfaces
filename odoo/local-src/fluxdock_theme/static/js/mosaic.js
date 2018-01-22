odoo.define('theme_fluxdock.mosaic', function (require) {
    'use strict';

    // var Model = require('web.Model');
    var ajax = require('web.ajax');
    var base = require('web_editor.base');
    var core = require('web.core');
    var qweb = core.qweb;

    // load existing qweb templates
    ajax.jsonRpc('/web/dataset/call', 'call', {
        'model': 'ir.ui.view',
        'method': 'read_template',
        'args': ['fluxdock_theme.mosaic_item']
    }).done(function (data) {
        qweb.add_template(data);
    });

    if(!$('.mosaic.grid').length) {
        return $.Deferred().reject("DOM doesn't contain '.mosaic.grid'");
    }

    var Mosaic = function(el, loadfrom) {
        this.$grid = $(el);
        this.loadfrom = loadfrom;
        this.data = this.$grid.data();
        this.fields = ["display_name", "website_url", "image_url"];
        this.html = '';
    };
    Mosaic.prototype = {
        render: function render() {
            var self = this;
            self.load_items().done(function(){
                self.$grid.html(self.html);
                self.$grid.find('.grid-item').removeClass('hidden');
                $('.clickable').on('click', function(){
                    window.location.href = $(this).data('url');
                })
            })
        },
        _render: function _render(item) {
            return qweb.render(
                'fluxdock_theme.mosaic_item', {'item': item}
            );
        },
        load_items: function load_items() {
            var self = this;
            if (self.loadfrom) {
                return self.load_from();
            } else {
                return self.load_search_read();
            }
        },
        load_from: function() {
            var self = this;
            return $.getJSON(self.loadfrom, {'limit': self.data.limit}).then(function(response) {
                if(response.ok){
                    // prepare and inject final html
                    $.each(response.results, function(){
                        self.html += self._render(this);
                    })
                }
    		});
        },
        load_search_read: function() {
            var self = this;
            return ajax.jsonRpc("/web/dataset/call_kw", 'call', {
                model: self.data.model,
                method: 'search_read',
                args: [self.data.domain],
                kwargs: {
                    fields: self.fields,
                    limit: self.data.limit,
                    order: self.data.order,
                    context: base.get_context()
                }
            }).then(function(records) {
                // invert mapping
                $.each(records, function(){
                    self.html += self._render(this);
                })
            })
        }
    }

    $(document).ready(function () {
        $('.clickable').on('click', function(){
            window.location.href=$(this).data('url');
        })
        $('.mosaic.grid[data-model]').each(function(){
            var mosaic = new Mosaic(this);
            mosaic.render();
        })
        $('.mosaic.grid[data-loadfrom]').each(function(){
            var mosaic = new Mosaic(this, $(this).data('loadfrom'));
            mosaic.render();
        })
    });
});
