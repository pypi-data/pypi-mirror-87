<template>
    <multiselect
        :loading="isLoading"
        @search-change="search"
        track-by="id"
        :options="Options"
        :placeholder="placeholder"
        :custom-label="toLabel"
        v-model="MsVmodel"
        :multiple="multiple"
        open-direction="bottom"
        :disabled="disabled"
        :allow-empty="!required || multiple"
        :internal-search="!ac"
    >
    </multiselect>
</template>

<script lang="ts">
import {Component, Prop, Vue, Watch} from 'vue-property-decorator';
import {Autocomplete, FormLayout, ModelCreatedResponse} from "@/interfaces/ApiInfo";
import Multiselect from "vue-multiselect";

@Component({
    name: 'DjVueAcSelect',
    components: {
        Multiselect
    },
})
export default class DjVueAcSelect extends Vue {
    @Prop() private readonly name!: string;
    @Prop() private readonly baseUrl!: string;
    @Prop() private readonly createModelPath!: string;
    @Prop() private readonly options!: Autocomplete[];
    @Prop() private readonly placeholder!: string;
    @Prop() private readonly ac!: boolean;
    @Prop() private readonly value!: number[] | number | undefined;
    @Prop() private readonly state!: boolean | null;
    @Prop() private readonly allowCreation!: boolean | null;
    @Prop() private readonly multiple!: boolean;
    @Prop() private readonly required!: boolean;
    @Prop() private readonly disabled!: boolean;

    private options_: Autocomplete[] = this.options || []
    private isLoading = false
    private cancel: any;
    private cancelTimeout: number = -1;

    /**
     * utilizzo un setter ed un getter per ritornare il valore al componente padre, per il componente vue-multiselect
     * continuo ad utilizzare la struttura delle opzioni in quanto mi risolve delle beghe relativamente alla ricerca
     * tramite ajax, altrimenti sarei costretto ad utilizzare delle strutture di supporto e mantenerne una consistenza
     */
    get MsVmodel() {
        if (this.multiple) {
            return this.Options.filter((opt) => {
                return (this.value as number[]).includes(opt.id)
            })
        }
        return this.Options.find((opt) => {
            return this.value === opt.id
        })
    }

    set MsVmodel(vls: Autocomplete[] | Autocomplete | undefined) {
        if (this.multiple) {
            this.$emit('input', (vls as Autocomplete[]).map((vl) => {
                return vl.id
            }))
        } else {
            /**
             * Vue multiselect permette di deselezionare il valore e mette il vls a null, quindi prima di lanciare l'evento
             * controllo che esista il valore, questo comportamento avviene solamente quando il campo non è required
             * altrimenti il campo vls è sempre popolato
             */
            let id = null
            if (vls) {
                id = (vls as Autocomplete).id;
            }
            this.$emit('input', id)
        }
    }

    get Options() {
        return this.options_
    }

    set Options(opt: Autocomplete[]) {
        this.options_ = opt
    }

    toLabel(ac: Autocomplete) {
        return ac.text
    }

    created() {
        this.$root.$on(['dv::object::created', 'dv::object::updated'], (evt: ModelCreatedResponse) => {
            //non è detto che la cosa sia necessariamente giusta, potrei avere più url che creano un modello
            if (evt.baseUrl == this.createModelPath) {
                this.search('', true)
            }
        })
    }

    //questo serve perché se la form effettua la get dopo che il componente si è renderizzato non vedo le modifiche
    @Watch('value')
    onValueChange() {
        this.search('', true);
    }

    mounted() {
        this.search('', true)
    }

    fetchOptions(query: string, ids?: string) {
        this.isLoading = true
        Vue.axios.get(`${this.baseUrl}autocomplete/?field=${this.name}&search=${query}&ids=${ids}`, {
            cancelToken: new Vue.axios.CancelToken((c) => {
                // An executor function receives a cancel function as a parameter
                this.cancel = c;
            })
        }).then(response => {
            this.Options = response.data
        }).catch((err) => {
            if (Vue.axios.isCancel(err)) {
                console.warn('Request canceled');
            } else {
                // handle error
            }
        }).finally(() => {
            this.isLoading = false
        })
    }

    search(query: string, force?: boolean) {

        let ids: number[] = []
        if (this.ac) {
            if (this.cancel) {
                this.cancel()
            }
            if (this.value) {
                if (this.value.constructor != Array) {
                    ids = [this.value as number]

                } else {
                    ids = this.value as number[]
                }
            }
            window.clearTimeout(this.cancelTimeout)
            if (force) {
                this.fetchOptions(query, ids.join(','))
            } else {
                this.cancelTimeout = window.setTimeout(() => {
                    this.fetchOptions(query, ids.join(','))
                }, 200);
            }
        }
    }
}
</script>

<style lang="scss">
@import "~bootstrap/scss/functions";
@import "~bootstrap/scss/mixins";
@import "~bootstrap/scss/variables";

$ms_border: $input-border-color;
$ms_pill: $gray-400;
$ms_tag_color: $gray-900;

fieldset[disabled] .multiselect {
    pointer-events: none;
}

.multiselect__spinner {
    position: absolute;
    right: 1px;
    top: 1px;
    width: 48px;
    height: 35px;
    background: #fff;
    display: block;
}

.multiselect__spinner:before,
.multiselect__spinner:after {
    position: absolute;
    content: "";
    top: 50%;
    left: 50%;
    margin: -8px 0 0 -8px;
    width: 16px;
    height: 16px;
    border-radius: 100%;
    border-color: $ms_pill transparent transparent;
    border-style: solid;
    border-width: 2px;
    box-shadow: 0 0 0 1px transparent;
}

.multiselect__spinner:before {
    animation: spinning 2.4s cubic-bezier(0.41, 0.26, 0.2, 0.62);
    animation-iteration-count: infinite;
}

.multiselect__spinner:after {
    animation: spinning 2.4s cubic-bezier(0.51, 0.09, 0.21, 0.8);
    animation-iteration-count: infinite;
}

.multiselect__loading-enter-active,
.multiselect__loading-leave-active {
    transition: opacity 0.4s ease-in-out;
    opacity: 1;
}

.multiselect__loading-enter,
.multiselect__loading-leave-active {
    opacity: 0;
}

.multiselect,
.multiselect__input,
.multiselect__single {
    font-family: inherit;
    font-size: 16px;
    touch-action: manipulation;
}

.multiselect {
    box-sizing: content-box;
    display: block;
    position: relative;
    width: 100%;
    min-height: 40px;
    text-align: left;
    color: #35495e;
}

.multiselect * {
    box-sizing: border-box;
}

.multiselect:focus {
    outline: none;
}

.multiselect--disabled {
    background: #ededed;
    pointer-events: none;
    opacity: 0.6;
}

.multiselect--active {
    z-index: 50;
}

.multiselect--active:not(.multiselect--above) .multiselect__current,
.multiselect--active:not(.multiselect--above) .multiselect__input,
.multiselect--active:not(.multiselect--above) .multiselect__tags {
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
}

.multiselect--active .multiselect__select {
    transform: rotateZ(180deg);
}

.multiselect--above.multiselect--active .multiselect__current,
.multiselect--above.multiselect--active .multiselect__input,
.multiselect--above.multiselect--active .multiselect__tags {
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}

.multiselect__input,
.multiselect__single {
    position: relative;
    display: inline-block;
    min-height: 20px;
    line-height: 20px;
    border: none;
    border-radius: 5px;
    background: #fff;
    padding: 0 0 0 5px;
    width: calc(100%);
    transition: border 0.1s ease;
    box-sizing: border-box;
    margin-bottom: 8px;
    vertical-align: top;
}

.multiselect__input::placeholder {
    color: #35495e;
}

.multiselect__tag ~ .multiselect__input,
.multiselect__tag ~ .multiselect__single {
    width: auto;
}

.multiselect__input:hover,
.multiselect__single:hover {
    border-color: #cfcfcf;
}

.multiselect__input:focus,
.multiselect__single:focus {
    border-color: #a8a8a8;
    outline: none;
}

.multiselect__single {
    padding-left: 5px;
    margin-bottom: 8px;
}

.multiselect__tags-wrap {
    display: inline;
}

.multiselect__tags {
    min-height: 40px;
    display: block;
    padding: 8px 40px 0 8px;
    border-radius: 5px;
    border: 1px solid $ms_border;
    background: #fff;
    font-size: 14px;
}

.multiselect__tag {
    position: relative;
    display: inline-block;
    padding: 4px 26px 4px 10px;
    border-radius: 5px;
    margin-right: 10px;
    color: $ms_tag_color;
    line-height: 1;
    background: $ms_pill;
    margin-bottom: 5px;
    white-space: nowrap;
    overflow: hidden;
    max-width: 100%;
    text-overflow: ellipsis;
}

.multiselect__tag-icon {
    cursor: pointer;
    margin-left: 7px;
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    font-weight: 700;
    font-style: initial;
    width: 22px;
    text-align: center;
    line-height: 22px;
    transition: all 0.2s ease;
    border-radius: 5px;
}

.multiselect__tag-icon:after {
    content: "×";
    color: #266d4d;
    font-size: 14px;
}

.multiselect__tag-icon:focus,
.multiselect__tag-icon:hover {
    background: #369a6e;
}

.multiselect__tag-icon:focus:after,
.multiselect__tag-icon:hover:after {
    color: white;
}

.multiselect__current {
    line-height: 16px;
    min-height: 40px;
    box-sizing: border-box;
    display: block;
    overflow: hidden;
    padding: 8px 12px 0;
    padding-right: 30px;
    white-space: nowrap;
    margin: 0;
    text-decoration: none;
    border-radius: 5px;
    border: 1px solid $ms_border;
    cursor: pointer;
}

.multiselect__select {
    line-height: 16px;
    display: block;
    position: absolute;
    box-sizing: border-box;
    width: 40px;
    height: 38px;
    right: 1px;
    top: 1px;
    padding: 4px 8px;
    margin: 0;
    text-decoration: none;
    text-align: center;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.multiselect__select:before {
    position: relative;
    right: 0;
    top: 65%;
    color: #999;
    margin-top: 4px;
    border-style: solid;
    border-width: 5px 5px 0 5px;
    border-color: #999999 transparent transparent transparent;
    content: "";
}

.multiselect__placeholder {
    color: #adadad;
    display: inline-block;
    margin-bottom: 10px;
    padding-top: 2px;
}

.multiselect--active .multiselect__placeholder {
    display: none;
}

.multiselect__content-wrapper {
    position: absolute;
    display: block;
    background: #fff;
    width: 100%;
    max-height: 240px;
    overflow: auto;
    border: 1px solid $ms_border;
    border-top: none;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    z-index: 50;
    -webkit-overflow-scrolling: touch;
}

.multiselect__content {
    list-style: none;
    display: inline-block;
    padding: 0;
    margin: 0;
    min-width: 100%;
    vertical-align: top;
}

.multiselect--above .multiselect__content-wrapper {
    bottom: 100%;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom: none;
    border-top: 1px solid $ms_border;
}

.multiselect__content::webkit-scrollbar {
    display: none;
}

.multiselect__element {
    display: block;
}

.multiselect__option {
    display: block;
    padding: 12px;
    min-height: 40px;
    line-height: 16px;
    text-decoration: none;
    text-transform: none;
    vertical-align: middle;
    position: relative;
    cursor: pointer;
    white-space: nowrap;
}

.multiselect__option:after {
    top: 0;
    right: 0;
    position: absolute;
    line-height: 40px;
    padding-right: 12px;
    padding-left: 20px;
    font-size: 13px;
}

.multiselect__option--highlight {
    background: $ms_pill;
    outline: none;
    color: white;
}

.multiselect__option--highlight:after {
    content: attr(data-select);
    background: $ms_pill;
    color: white;
}

.multiselect__option--selected {
    background: #f3f3f3;
    color: #35495e;
    font-weight: bold;
}

.multiselect__option--selected:after {
    content: attr(data-selected);
    color: silver;
}

.multiselect__option--selected.multiselect__option--highlight {
    background: #ff6a6a;
    color: #fff;
}

.multiselect__option--selected.multiselect__option--highlight:after {
    background: #ff6a6a;
    content: attr(data-deselect);
    color: #fff;
}

.multiselect--disabled .multiselect__current,
.multiselect--disabled .multiselect__select {
    background: #ededed;
    color: #a6a6a6;
}

.multiselect__option--disabled {
    background: #ededed !important;
    color: #a6a6a6 !important;
    cursor: text;
    pointer-events: none;
}

.multiselect__option--group {
    background: #ededed;
    color: #35495e;
}

.multiselect__option--group.multiselect__option--highlight {
    background: #35495e;
    color: #fff;
}

.multiselect__option--group.multiselect__option--highlight:after {
    background: #35495e;
}

.multiselect__option--disabled.multiselect__option--highlight {
    background: #dedede;
}

.multiselect__option--group-selected.multiselect__option--highlight {
    background: #ff6a6a;
    color: #fff;
}

.multiselect__option--group-selected.multiselect__option--highlight:after {
    background: #ff6a6a;
    content: attr(data-deselect);
    color: #fff;
}

.multiselect-enter-active,
.multiselect-leave-active {
    transition: all 0.15s ease;
}

.multiselect-enter,
.multiselect-leave-active {
    opacity: 0;
}

.multiselect__strong {
    margin-bottom: 8px;
    line-height: 20px;
    display: inline-block;
    vertical-align: top;
}

*[dir="rtl"] .multiselect {
    text-align: right;
}

*[dir="rtl"] .multiselect__select {
    right: auto;
    left: 1px;
}

*[dir="rtl"] .multiselect__tags {
    padding: 8px 8px 0px 40px;
}

*[dir="rtl"] .multiselect__content {
    text-align: right;
}

*[dir="rtl"] .multiselect__option:after {
    right: auto;
    left: 0;
}

*[dir="rtl"] .multiselect__clear {
    right: auto;
    left: 12px;
}

*[dir="rtl"] .multiselect__spinner {
    right: auto;
    left: 1px;
}

@keyframes spinning {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(2turn);
    }
}

</style>
