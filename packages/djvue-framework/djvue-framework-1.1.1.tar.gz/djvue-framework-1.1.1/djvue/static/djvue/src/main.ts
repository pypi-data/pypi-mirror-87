import axios from 'axios'
import VueAxios from 'vue-axios'

function getCookie(name:string) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

axios.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');

import Table from './components/Table.vue'
import List from './components/List.vue'
import Form from './components/Form.vue'
import ModalForm from './components/ModalForm.vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Declare install function executed by Vue.use()
export function install(Vue: any) {
	// @ts-ignore
    if (install.installed) return;
	// @ts-ignore
    install.installed = true;
	Vue.component('djvue-table', Table);
	Vue.component('djvue-list', List);
	Vue.component('djvue-form', Form);
	Vue.component('djvue-modal-form', ModalForm);
}

const plugin = {
	install,
};

// Auto-install when vue is found (eg. in browser via <script> tag)
let GlobalVue = null;
if (typeof window !== 'undefined') {
	GlobalVue = (window as any).Vue;
}
if (GlobalVue) {

	// Install BootstrapVue
	GlobalVue.use(BootstrapVue);
	// Optionally install the BootstrapVue icon components plugin
	GlobalVue.use(IconsPlugin);
	GlobalVue.use(VueAxios, axios);
	GlobalVue.use(plugin);
}

export {Table, Form, List, ModalForm}

