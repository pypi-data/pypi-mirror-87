<template>
    <div>
        <b-alert
            :show="showFormErrorAlert"
            class="col-12"
            variant="danger"
        >
            <p class="m-0" v-for="(e,idx) in formErrors" :key="idx">{{ e }}</p>
        </b-alert>

        <b-alert
            :show="showNonFieldAlert"
            class="col-12"
            variant="warning"
        >
            <p class="m-0" v-for="(e,idx) in nonFieldErrors" :key="idx">{{ e }}</p>
        </b-alert>

        <div class="d-flex justify-content-between pb-3"
             v-if="showRemove"
        >
            <b-badge pill variant="secondary" class="align-self-baseline">{{ inlineKey + 1 }}</b-badge>
            <BButton
                @click="$emit('remove', inlineKey)"
                size="sm"
                variant="danger"
            >
                <BIcon icon="trash"></BIcon>
            </BButton>
        </div>

        <b-form :class="formClass">
            <Layout :layout="form">
                <template v-slot:[f.name]="slotProps" v-for="f in Fields">
                    <component
                        :is="getComponent(f)"
                        :key="f.name"
                        :layout="f.layout"
                        v-bind="getAttributes(f)"
                    >
                        <div class="d-inline-flex w-100">

                            <div class="d-flex flex-column flex-grow-1">
                                <component
                                    :is="getWidget(f)"
                                    v-model="value[f.name]"
                                    @input="onInput(f.name, $event)"
                                    v-bind="getAttributes(f).input"
                                    :state="getErrorState(f)"
                                    :errors="getFieldError(f)"
                                >
                                </component>
                                <b-form-invalid-feedback :state="getErrorState(f)">
                                    {{ getFieldError(f)[0] || '' }}
                                </b-form-invalid-feedback>
                            </div>
                            <div class="align-items-start">
                                <ModalForm v-if="f.allowCreation" :modelPath="f.createModelPath" :operation="0"
                                           class="ml-2 d-flex"></ModalForm>
                            </div>
                        </div>
                    </component>
                </template>
            </Layout>
        </b-form>
    </div>
</template>

<script lang="ts">
import {Component, Prop, Vue, Watch} from 'vue-property-decorator';
import BaseInput from "@/components/forms/BaseInput.vue";
import {DVFormWidget, EOperation, FieldMeta, StringKeyArrayString} from "@/interfaces/ApiInfo";
import DjVueSelect from "@/components/forms/DjVueSelect.vue";
import DjVueAcSelect from "@/components/forms/DjVueAcSelect.vue";
import DjVueRadioGroup from "@/components/forms/DjVueRadioGroup.vue";
import DjVueCheckboxGroup from "@/components/forms/DjVueCheckboxGroup.vue";
import FormComponent from "@/components/FormComponent";
import {BFormCheckbox, BFormInput, BFormTextarea} from "bootstrap-vue";
import InlineForm from "@/components/InlineForm.vue";
import DjVueHidden from "@/components/forms/DjVueHidden.vue";
import DjVueCheckbox from "@/components/forms/DjVueCheckbox.vue";
import DjVueInputGroup from "@/components/forms/DjVueInputGroup.vue";
import Layout from "@/components/Layout.vue";


@Component({
    name: 'Form',
    components: {
        Layout,
        ModalForm: () => import('@/components/ModalForm.vue'),
        DjVueAcSelect,
        DjVueSelect,
        BFormTextarea
    },
})
export default class Form extends FormComponent {
    @Prop(Number) private readonly operation!: EOperation
    @Prop() private readonly value!: any
    @Prop() private readonly form!: any
    @Prop() private readonly fields!: any
    @Prop() private readonly inlineKey!: number
    @Prop() private readonly showRemove!: boolean

    @Prop({
        type: Object, default: () => {
            return {}
        }
    }) private readonly fieldErrors!: StringKeyArrayString
    @Prop({
        type: Array, default: () => {
            return []
        }
    }) private readonly formErrors!: string[]
    @Prop({
        type: Array, default: () => {
            return []
        }
    }) private readonly nonFieldErrors!: string[]
    @Prop({type: Boolean, default: true}) private readonly prevent_id!: boolean

    get showSend() {
        return this.operation !== EOperation.DETAIL
    }

    get Fields() {
        return this.fields
    }

    get formClass() {
        return this.form && this.form.form_class
    }

    get showFormErrorAlert() {
        return this.formErrors.length > 0
    }

    get showNonFieldAlert() {
        return this.nonFieldErrors.length > 0
    }

    getFieldError(f: FieldMeta) {
        return this.fieldErrors[f.name] || []
    }

    getErrorState(f: FieldMeta) {
        if (this.fieldErrors && this.fieldErrors[f.name]) {
            return this.fieldErrors[f.name].length == 0
        }
        return null
    }

    getType(f: FieldMeta) {
        switch (f.type) {
            case 'integer':
            case 'decimal':
            case 'float':
                return 'number'
            case 'string':
                return 'text'
            case 'boolean':
                return 'number'
            case 'field':
                return 'select'
            case 'datetime':
                return 'datetime-local'
            default:
                return f.type
        }
    }

    isInline(f: FieldMeta) {
        return f.type === 'nested object'
    }

    getInlineAttribute(f: FieldMeta) {
        return {
            field: f,
            value: this.value[f.name],
            operation: this.operation,
            fieldErrors: this.getFieldError(f)
        }
    }

    isHidden(f: FieldMeta) {
        return (f.widget && f.widget === DVFormWidget.HIDDEN)
    }

    getHiddenAttribute(f: FieldMeta) {
        return {
            value: this.value[f.name],
        }
    }

    getAttributes(f: FieldMeta) {
        if (this.isHidden(f)) {
            return this.getHiddenAttribute(f)
        } else if (this.isInline(f)) {
            return this.getInlineAttribute(f)
        }
        return {
            ...f,
            input: {
                size: f.size,
                required: f.required,
                allow_null: f.allow_null,
                disabled: this.operation == EOperation.DETAIL ? true : f.read_only,
                name: f.name,
                placeholder: f.placeholder,
                type: this.getType(f),
                min: f.min_value,
                max: f.max_value,
                step: f.step,
                ac: f.ac,
                help_text: f.help_text,
                options: (f.options || []),
                multiple: f.many || false,
                baseUrl: this.baseUrl,
                createModelPath: f.createModelPath,
                allowCreation: f.allowCreation || false,
                defaultParams: this.defaultParams,
                append: f.append || null,
                prepend: f.prepend || null,
                input_class: f.input_class || ''
            }
        }
    }


    getComponent(f: FieldMeta) {
        if (this.isHidden(f)) {
            return DjVueHidden
        } else if (this.isInline(f)) {
            return InlineForm;
        } else {
            return BaseInput;
        }
    }

    getWidget(f: FieldMeta) {
        switch (f.widget) {
            case DVFormWidget.DJVUE_INPUT_GROUP:
                return DjVueInputGroup
            case DVFormWidget.TEXTAREA:
                return BFormTextarea
            case DVFormWidget.CHECKBOX:
                return BFormCheckbox
            case DVFormWidget.DJVUE_RADIO_GROUP:
                return DjVueRadioGroup
            case DVFormWidget.DJVUE_CHECKBOX_GROUP:
                return DjVueCheckboxGroup
            case DVFormWidget.DJVUE_AC_SELECT:
                return DjVueAcSelect
            case DVFormWidget.DJVUE_SELECT:
                return DjVueSelect
            default:
                switch (f.type) {
                    case 'field':
                    case 'choice':
                        if (f.many) {
                            return DjVueAcSelect
                        }
                        return DjVueSelect
                    case 'boolean':
                        return BFormCheckbox
                }
                return BFormInput
        }
    }

    onInput(name: string, val: any) {
        this.value[name] = val;
        this.$emit('input', this.value);
    }

    @Watch('fields')
    initData() {
        for (const f in this.Fields) {
            if (this.value && !Object.prototype.hasOwnProperty.call(this.value, f)) {
                this.initFieldData(this.Fields[f])
            }
        }
    }

    initFieldData(f: FieldMeta) {
        if (f.type == 'nested object') {
            this.$set(this.value, f.name, [])
            return
        } else if (!Object.prototype.hasOwnProperty.call(this.value, f.name)) {
            if (typeof f.default !== "undefined") {
                this.$set(this.value, f.name, f.default)
            } else if (f.type == 'field' && f.many) {
                this.$set(this.value, f.name, [])
            } else if (f.required) {
                switch (f.type) {
                    //nel caso dei booleano settare il default per non avere un messaggio di errore, oppure usare un
                    //nullable boolean lato backcend
                    case 'boolean':
                        if (!f.allow_null) {
                            this.$set(this.value, f.name, false)
                        }
                        break
                    default:
                        //in tutti gli altri casi metto ad undefined. Se non lo faccio alcuni componenti come la multiselect si incartano
                        this.$set(this.value, f.name, undefined)

                }
            }
        }
    }
}
</script>

<style lang="scss" scoped>

</style>
