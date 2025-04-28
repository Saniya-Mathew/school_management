/** @odoo-module */
//import { _ } from './module';
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
publicWidget.registry.get_event_tab = publicWidget.Widget.extend({
    selector : '.categories_section',
    async willStart() {
        const result = await rpc('/get_event_categories', {});
        if(result){
            this.$target.empty().html(renderToElement('school.category_data', {result: result}))
        }
    },
//    start: function() {
//        var chunks = chunk(this.result, 4)
//        chunks[0].is_active = true
//        this.$el.find('#courosel').html(
//        qweb.render('school.category_data', {
//        chunks
//        }))
//    },
});


