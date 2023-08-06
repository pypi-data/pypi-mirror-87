<template>
    <div>

        <b-form-group
                :label-for="filterId"
        >
            <b-form-input
                    v-model="filter"
                    type="search"
                    :id="filterId"
                    size="sm" placeholder="cerca..."
                    ref="filter_input"
            ></b-form-input>

        </b-form-group>

        <b-list-group ref="list" :id="id">
            <b-list-group-item v-for="item in items" :key="item[keyField]" v-on="$listeners">
                <slot name="list-item" v-bind="item">
                    {{item[valueField]}}
                </slot>
            </b-list-group-item>
        </b-list-group>

        <div class="d-flex justify-content-end pt-3">
            <b-pagination
                    v-model="currentPage"
                    :aria-controls="id"
                    :total-rows="totalItems"
                    :per-page="perPage"
                    ref="pagination"
            ></b-pagination>
        </div>


    </div>
</template>

<script lang="ts">
    import {Component, Prop, Watch} from 'vue-property-decorator';
    import ListComponent from "@/components/ListComponent";

    @Component({
        name: "List"
    })
    export default class List extends ListComponent {
        @Prop(String) protected readonly keyField!: string;
        @Prop(String) protected readonly valueField!: string;

        get filterId() {
            return 'filterInput_' + this.id;
        }

        get filteredItems() {
            // todo: implementare filtro lato front
            return this.items
        }

        @Watch('filter')
        onFilterChange() {
            this.fetch();
        }

        @Watch('currentPage')
        onCurrentPageChange() {
            this.fetch();
        }

        init() {
            this.fetch();
        }

    }
</script>

<style scoped>

</style>
