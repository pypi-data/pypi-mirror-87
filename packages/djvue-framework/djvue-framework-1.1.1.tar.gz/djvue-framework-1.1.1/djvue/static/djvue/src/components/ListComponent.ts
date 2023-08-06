import {Component, Vue} from 'vue-property-decorator';
import BaseComponent from "@/components/BaseComponent";
import {ApiInfo, GETAction} from "@/interfaces/ApiInfo";

@Component({
    name: "ListComponent"
})
export default class ListComponent extends BaseComponent {
    protected currentPage: number = 1;
    protected items: any[] = [];
    protected totalItems: number = 0;
    protected filter: string = '';
    protected sortBy: string = '';
    protected sortDesc: boolean = false;
    list_api_info: GETAction = {
        is_paginated: false,
        page_size: 0,
        page_param: '',
        list_fields: [],
        has_extra_buttons: false,
        allow_creation: false,
        list_select_key: '',
        has_footer: false,
        search_filter: {
            search_fields: [],
            search_param: ''
        },
        ordering_filter: {
            ordering_fields: [],
            ordering_param: ''
        },
        fields: {},
        create_button:{}
    };

    mounted() {
        if (this.baseUrl) {
            Vue.axios.options(this.baseUrl).then((response) => {
                this.list_api_info = (response.data.actions.GET as GETAction);
                this.initialized = true;
                this.$emit('init');
                this.init()
            });
        }
    }

    fetch() {
        /*Questo metodo puo' essere messo dentro la provider della tabella, o per lo meno passare il cntesto e cercare
        di evitare tutti i controlli seguenti
        */

        this.busy = true;

        let params: any = this.defaultParams || {};

        if (this.list_api_info.is_paginated) {
            params[this.list_api_info.page_param] = this.currentPage;

            if (this.list_api_info.search_filter) {
                params[this.list_api_info.search_filter.search_param] = this.filter
            }

            if (this.list_api_info.ordering_filter && this.sortBy) {
                params[this.list_api_info.ordering_filter.ordering_param] = (this.sortDesc ? "-" : "") + this.sortBy
            }

        }

        return Vue.axios.get(this.baseUrl, {params: params}).then((res) => {
            if (res.data.results) {
                this.totalItems = res.data.count
                this.items = res.data.results
            } else {
                this.items = res.data;
                this.totalItems = this.items.length
            }
            this.busy = false;
        })

    }


    get perPage() {
        if (this.list_api_info.is_paginated) {
            return this.list_api_info.page_size
        } else {
            return 15;
        }
    }

    get isServerPaginated() {
        return this.list_api_info.is_paginated
    }


}

