<template>
    <div class="inline_striped">
        <Form
            @remove="Remove($event)"
            class="card p-3 mb-3"
            :inline-key="i"
            v-for="(f,i) in value"
            :key="i"
            :baseUrl="baseUrl"
            v-bind:value="value[i]"
            @input="onInput(i,$event)"
            :form="{}"
            :fields="fields"
            :fieldErrors="fieldErrors[i]"
            :operation="operation"
            :showRemove="showRemove"
        >
        </Form>
        <div v-if="showAdd" class="d-flex justify-content-center">
            <BButton size='sm' @click="Add()">Add</BButton>
        </div>
    </div>
</template>

<script lang="ts">
import {Component, Prop, Vue, Watch} from 'vue-property-decorator';
import {EOperation, FieldMeta, FormOption, ModelInfo} from "@/interfaces/ApiInfo";


@Component({
    name: 'InlineForm',
    components: {
        Form: () => import('@/components/Form.vue'),
    },
})
export default class InlineForm extends Vue {
    @Prop() private readonly field!: FieldMeta;
    @Prop({default:()=>{return []}}) private readonly fieldErrors!: any[];
    @Prop({
        default: () => {
            return []
        }
    }) private readonly value!: any[];
    @Prop({default: 0}) private readonly min!: number
    @Prop({default: Infinity}) private readonly max!: number
    @Prop() private readonly operation!: EOperation

    private form: any = {}
    private fields: any = {}

    get baseUrl() {
        if (this.operation == EOperation.CREATE) {
            return (this.field.model as ModelInfo).listBaseUrl
        }
        return (this.field.model as ModelInfo).detailBaseUrl
    }

    @Watch('value')
    initValue() {
        const diff = this.min - this.value.length;
        if (diff > 0) {
            for (let i = 0; i < diff; i++) {
                this.value.push({})
            }
        }
    }

    created() {
        this.fetchSpec()
        this.initValue()
    }

    fetchSpec() {
        return Vue.axios.options(this.baseUrl).then((a) => {
            const op = a.data as FormOption
            if (this.operation == EOperation.CREATE) {
                this.form = op.actions.POST.form
                this.fields = op.actions.POST.fields
            } else if (this.operation == EOperation.UPDATE) {
                this.form = op.actions.PUT.form
                this.fields = op.actions.PUT.fields
            } else if (this.operation == EOperation.DETAIL) {
                this.form = op.actions.GET.form
                this.fields = op.actions.GET.fields
            }
        })
    }

    Add() {
        this.value.push({})
    }

    Remove(el: number) {
        this.value.splice(el, 1)
    }

    get showRemove() {
        return this.operation !== EOperation.DETAIL && this.value.length > this.min
    }

    get showAdd() {
        return this.operation !== EOperation.DETAIL && this.value.length < this.max
    }

    onInput(id: number, val: any) {
        this.value[id] = val;
        this.$emit('input', this.value);
    }
}
</script>

<style lang="scss" scoped>

@import "~bootstrap/scss/functions";
@import "~bootstrap/scss/mixins";
@import "~bootstrap/scss/variables";

.inline_striped{
    .card:nth-child(odd){
        background-color: $light;
    }
}
</style>
