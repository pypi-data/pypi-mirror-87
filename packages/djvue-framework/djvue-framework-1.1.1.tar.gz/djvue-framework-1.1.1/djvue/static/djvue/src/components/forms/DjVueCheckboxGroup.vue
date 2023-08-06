<template>
    <b-form-checkbox-group
        v-model="Vmodel"
        :options="Options"
        :name="name"
        :disabled="disabled"
        :description="$attrs.help_text"
        value-field="id"
        text-field="text"
        :size="$attrs.size"
    >
    </b-form-checkbox-group>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
import {Autocomplete, ModelCreatedResponse} from "@/interfaces/ApiInfo";

@Component({
    name: 'DjVueCheckboxGroup',
    inheritAttrs: false
})
export default class DjVueCheckboxGroup extends Vue {
    @Prop() private readonly name!: string;
    @Prop({
        default: () => {
            return []
        }
    }) private readonly value!: string
    @Prop() private readonly options!: Autocomplete[]
    @Prop() private readonly state!: boolean | null;
    @Prop() private readonly baseUrl!: string;
    @Prop() private readonly createModelPath!: string;
    @Prop() private readonly ac!: boolean;
    @Prop() private readonly allowCreation!: boolean | null;
    @Prop() private readonly disabled!: boolean;
    @Prop({
        default: () => {
            return []
        }
    }) private readonly errors!: string[];

    private options_: Autocomplete[] = this.options || []

    get Options() {
        return this.options_
    }

    set Options(opt: Autocomplete[]) {
        this.options_ = opt
    }

    get Vmodel() {
        return this.value
    }

    set Vmodel(vls: string) {
        this.$emit('input', vls)
    }

    created() {
        this.$root.$on(['dv::object::created', 'dv::object::updated'], (evt: ModelCreatedResponse) => {
            //non è detto che la cosa sia necessariamente giusta, potrei avere più url che creano un modello
            if (evt.baseUrl == this.createModelPath) {
                this.fetchOptions()
            }
        })
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
