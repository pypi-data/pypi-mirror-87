<template>
    <b-form-radio-group
        v-model="Vmodel"
        :options="Options"
        :name="name"
        :disabled="disabled"
        :size="$attrs.size"
        :class="{'is-invalid': state === false }"
        value-field="id"
        text-field="text"
    >
    </b-form-radio-group>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
import {BFormRadioGroup} from 'bootstrap-vue'
import {Autocomplete} from "@/interfaces/ApiInfo";
import BaseComponent from "@/components/BaseComponent";

@Component({
    name: 'DjVueRadioGroup',
    components: {
        BFormRadioGroup
    },
    inheritAttrs: false
})
export default class DjVueRadioGroup extends BaseComponent {
    @Prop() private readonly name!: string
    @Prop() private readonly ac!: boolean;
    @Prop({default: null}) private readonly value!: number
    @Prop({
        default: () => {
            return []
        }
    }) private readonly options!: Autocomplete[]
    @Prop() private readonly state!: boolean | null;
    @Prop() private readonly disabled!: boolean;

    private options_: Autocomplete[] = this.options

    get Options() {
        return this.options_
    }

    set Options(opt: Autocomplete[]) {
        this.options_ = opt
    }

    get Vmodel() {
        return this.value
    }

    set Vmodel(vls: number | null) {
        this.$emit('input', vls)
    }

    mounted() {
        this.fetchOptions()
    }

    fetchOptions() {
        if (this.ac) {
            Vue.axios.get(`${this.baseUrl}autocomplete/`,
                {
                    params: {
                        //nelle checkbox la paginazione non ha senso
                        pagination: 0,
                        field: this.name
                    }
                }
            ).then((e) => {
                this.Options = e.data.map((opt: any) => {
                    opt['value'] = opt.id
                    return opt
                })
            })
        }
    }

    getError(errors: string[]) {
        return errors[0] || ''
    }
}
</script>

<style lang="scss" scoped>

</style>
