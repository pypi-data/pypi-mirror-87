import {Component, Prop, Vue} from 'vue-property-decorator';

@Component({
    name: "BaseComponent"
})
export default class BaseComponent extends Vue {
    @Prop(String) protected readonly baseUrl!: string;
    @Prop(Object) protected readonly defaultParams!: object;


    id: string = '';
    initialized: boolean = false;
    busy: boolean = false;

    created() {
        // @ts-ignore
        this.id = this._uid.toString()
    }

    init() {

    }

}

