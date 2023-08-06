<template>
    <div>
        <slot name="modal-open-button" v-bind:buttons="{Open:Open,isDetail,isCreate,isUpdate,isDelete}">
            <b-button @click="Open"
                      v-bind="button_props"
            >
              <b-icon v-if="buttonIcon" aria-hidden="true" :icon="buttonIcon"></b-icon>{{buttonLabel}}
            </b-button>
        </slot>
        <b-modal noCloseOnBackdrop noCloseOnEsc :id="`${_uid}`" :size="modalSize"
                 :title="title">
            <div v-if="isDelete">
                <b-alert
                    v-model="showAlert"
                    class="col-12"
                    dismissible
                    variant="danger">
                    <p>Si è verificato un errore durante la richiesta di cancellazione</p>
                </b-alert>

                <p>Sei sicuro?</p>
            </div>


            <Form v-else
                  :fieldErrors="formExceptionBuilder.fieldErrors"
                  :nonFieldErrors="formExceptionBuilder.nonFieldErrors"
                  :formErrors="formExceptionBuilder.formErrors"
                  :baseUrl="baseUrl"
                  v-model="models"
                  :form="form"
                  :fields="fields"
                  :operation="operation"
                  :defaultParams="defaultParams"
            ></Form>

            <template v-slot:modal-footer>
                <div v-if="isDelete" class="w-100 d-flex justify-content-between">
                    <b-button @click="okCallback()" size="sm" variant="danger">Elimina</b-button>
                    <b-button @click="Close()" size="sm">Annulla</b-button>
                </div>
                <div v-if="isUpdate || isCreate" class="w-100 d-flex justify-content-end">
                    <b-button @click="onSubmit()" size="sm" variant="success">Invia</b-button>
                </div>
                <div v-if="isDetail" class="w-100 d-flex justify-content-end">
                    <b-button @click="Close()" size="sm">Chiudi</b-button>
                </div>
            </template>

        </b-modal>
    </div>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';
import Form from "@/components/Form.vue";
import {EOperation, FormOption, ModelCreatedResponse} from "@/interfaces/ApiInfo";
import BaseComponent from "@/components/BaseComponent";
import FormException from "@/components/FormException";

@Component({
    name: 'ModalForm',
    components: {
        Form
    },
    inheritAttrs: false
})
export default class ModalForm extends BaseComponent {
    @Prop(Number) private readonly operation!: number
    @Prop({type:Object, default:()=>{return {}}}) private readonly button_props!: any

    private _uid!: number;
    private models = {};
    private showAlert = false;
    private formExceptionBuilder = new FormException()
    private form: any = {}
    private fields: any = {}

    get isCreate() {
        return this.operation == EOperation.CREATE
    }

    get isDetail() {
        return this.operation == EOperation.DETAIL
    }

    get isUpdate() {
        return this.operation == EOperation.UPDATE
    }

    get isDelete() {
        return this.operation == EOperation.DELETE
    }

    get title() {
        if (this.isCreate) {
            return 'Crea nuovo'
        } else if (this.isUpdate) {
            return 'Modifica'
        } else if (this.isDelete) {
            return 'Cancella'
        } else if (this.isDetail) {
            return 'Dettaglio'
        }
        return ''
    }

    get buttonLabel(){
      if(this.button_props.hasOwnProperty('label')) {
        return this.button_props.label
      }
      if (this.isCreate) {
            return 'Aggiungi'
        } else if (this.isUpdate) {
            return 'Modifica'
        } else if (this.isDelete) {
            return 'Elimina'
        } else if (this.isDetail) {
            return 'Dettaglio'
        }
        return ''
    }

    get buttonIcon(){
      if(this.button_props.hasOwnProperty('icon')) {
        return this.button_props.icon
      }
      if (this.isCreate) {
            return 'plus'
        } else if (this.isUpdate) {
            return 'pencil'
        } else if (this.isDelete) {
            return 'trash'
        } else if (this.isDetail) {
            return 'eye'
        }
        return false
    }

    get modalSize() {
        if (!this.isDelete) {
            return 'lg'
        }
        return 'sm'
    }

    get Variant() {
        if (this.isCreate) {
            return 'success'
        } else if (this.isUpdate) {
            return 'warning'
        } else if (this.isDelete) {
            return 'danger'
        }
        return 'primary'
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

    async Open() {
        this.$root.$emit('bv::show::modal', `${this._uid}`);

        if (this.operation == EOperation.UPDATE || this.operation == EOperation.DETAIL) {
            const promise = Vue.axios.get(`${this.baseUrl}`, {params: this.defaultParams})

            const res = await promise
            this.models = res.data
        }
        this.fetchSpec()
    }

    Close() {
        this.$root.$emit('bv::hide::modal', `${this._uid}`)
    }

    okCallback() {
        Vue.axios.delete(this.baseUrl, {params: this.defaultParams}).then(() => {
            this.Close();
            this.$emit('dv::object::deleted');
            this.$root.$emit('dv::object::deleted');
        }).catch(() => {
            this.showAlert = true;
        });
    }

    onSubmit() {
        let req;
        if (this.operation == EOperation.UPDATE) {
            req = Vue.axios.put(this.baseUrl, this.models, {params: this.defaultParams})
        } else if (this.operation == EOperation.CREATE) {
            req = Vue.axios.post(this.baseUrl, this.models, {params: this.defaultParams})
        }

        if (req) {
            req.then((e) => {
                let data: ModelCreatedResponse = {
                    baseUrl: this.baseUrl,
                    model: undefined
                }
                if (e && e.data) {
                    data = {...data, model: e.data}
                }
                switch (e.status) {
                    case 201:
                        //quando creo o cancello qualcosa emetto due eventi, uno specifico per il contenitore che ospita
                        //il modal uno generico per eventuali altri componenti nella pagina che possono necessitare di
                        //eseguire delle operazioni di aggiornamento
                        this.$emit('dv::object::created', data)
                        this.$root.$emit('dv::object::created', data)
                        break;
                    case 200:
                        this.$emit('dv::object::updated', data)
                        this.$root.$emit('dv::object::updated', data)
                        break;
                }
                this.models = {}
                this.formExceptionBuilder.reset()
                this.Close()
            }).catch((e) => {
                this.formExceptionBuilder.getErrors(e.response);
                const modal = document.querySelector(`[id='${this._uid}']`);
                if(modal){
                  modal.scrollTop =0
                }
            })
        }
    }
}
</script>

<style lang="scss" scoped>
</style>
