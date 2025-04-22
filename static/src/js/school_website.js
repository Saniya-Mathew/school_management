/** @odoo-module **/
import {rpc} from "@web/core/network/rpc";
import PublicWidget from "@web/legacy/js/public/public_widget";


	publicWidget.registry.generic_form_data = publicWidget.Widget.extend({
    	selector: '#student_list_template',
    	events: {
       	'click .remove_line': '_onClickRemove_line',
        },

    _onClickRemove_line: function(ev){
        $(ev.target).parent().parent().remove();
    },
     });