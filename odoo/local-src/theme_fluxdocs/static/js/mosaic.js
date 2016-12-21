odoo.define('theme_fluxdock.mosaic', function (require) {
    'use strict';

    // var Model = require('web.Model');
    var ajax = require('web.ajax');
    var base = require('web_editor.base');

    var unEntity = function unEntity(str){
       return str
        .replace(/\/&amp;/g, "&")
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">");
    }

    if(!$('.mosaic.grid').length) {
        return $.Deferred().reject("DOM doesn't contain '.mosaic.grid'");
    }

    $(document).ready(function () {
        $('.mosaic.grid[data-model]').each(function(){
            var $grid = $(this);
            $('.grid-item', $grid).remove();
            var data = $grid.data();
            var fields = _.keys(data.fields);
            var tmpl = unEntity($('.' + data.template, $grid).html());
            var template = _.template(tmpl);
            // 1st load items
            ajax.jsonRpc("/web/dataset/call_kw", 'call', {
                model: data.model,
                method: 'search_read',
                args: [data.domain],
                kwargs: {
                    fields: fields,
                    limit: data.limit,
                    order: data.order,
                    context: base.get_context()
                }
            }).then(function(records) {
                // redefine as is not available anymore here (???)
                var data = $grid.data();
                var html = '';
                // invert mapping
                $.each(records, function(){
                    var record = this;
                    var item = {};
                    $.each(data.fields, function(key, val) {
                        item[val] = record[key];
                    });
                    html += template(item);
                })
                $grid.append(html);
                $('.grid-item', $grid).removeClass('hidden');
            }).then(function(){
                // make grid items clickable as links
                $('.clickable').on('click', function(){
                    window.location.href=$(this).data('url');
                })
            })
        })
    });
});
