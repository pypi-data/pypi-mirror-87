<template>
    <b-form-select
        v-model="SModel"
        :class="{'is-invalid': state === false }"
        :multiple="multiple"
        :size="size"
        :disabled="disabled"
        class="position-relative"
        value-field="id"
        text-field="text"
    >
        <template v-if="allow_null" v-slot:first>
            <b-form-select-option :value="null">-- Please select an option --</b-form-select-option>
        </template>
        <b-form-select-option
            :key="o.id"
            :value="o.id"
            v-for="o in Options">
            {{ o.text }}
        </b-form-select-option>
    </b-form-select>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
import {Autocomplete, ModelCreatedResponse} from "@/interfaces/ApiInfo";
import BaseComponent from "@/components/BaseComponent";

@Component({
    name: 'DjVueSelect',
})
export default class DjVueSelect extends BaseComponent {
    @Prop() private readonly name!: string;
    @Prop() private readonly createModelPath!: string;
    @Prop() private readonly options!: Autocomplete[];
    @Prop() private readonly ac!: boolean;
    @Prop({
        default: () => {
            return [null]
        }
    }) private readonly value!: number | number[];
    @Prop() private readonly state!: boolean | null;
    @Prop() private readonly multiple!: boolean | null;
    @Prop() private readonly allowCreation!: boolean;
    @Prop() private readonly size!: string;
    @Prop() private readonly disabled!: boolean;
    @Prop() private readonly allow_null!: boolean;

    private options_: Autocomplete[] = []
    private _uid!: number;

    get SModel() {
        if (this.multiple) {
            this.options.filter((opt) => {
                return (this.value as number[]).includes(opt.id)
            })
        }
        return this.value
    }

    set SModel(val: any) {
        /**
         * questa situazione è assai più semplice da gestire rispetto al controllo multiselect
         */
        this.$emit('input', val)
    }

    get Options() {
        if (this.ac) {
            return this.options_
        }
        return this.options
    }

    set Options(opt: Autocomplete[]) {
        this.options_ = opt
    }

    mounted() {
        this.fetchOptions()
    }

    created() {
        this.$root.$on(['dv::object::created', 'dv::object::updated'], (evt: ModelCreatedResponse) => {
            //non è detto che la cosa sia necessariamente giusta, potrei avere più url che creano un modello
            if (evt.baseUrl == this.createModelPath) {
                this.fetchOptions()
            }
        })
    }

    fetchOptions() {
        if (this.ac) {
            Vue.axios.get(`${this.baseUrl}autocomplete/`,
                {
                    params: {
                        //nelle select normali la paginazione non ha senso
                        pagination: 0,
                        field: this.name,
                        ...this.defaultParams
                    }
                }
            ).then((e) => {
                this.Options = e.data
            })
        }
    }
}
</script>

<style lang="scss" scoped>

</style>
