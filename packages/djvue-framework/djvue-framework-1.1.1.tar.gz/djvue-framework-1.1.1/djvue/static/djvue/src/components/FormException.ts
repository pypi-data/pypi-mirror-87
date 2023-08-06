/**
 *
 * Questo componente si occupa della gestione delle eccezioni per le form, a partire dalle risposte
 * provenienti dal server (che di base hanno una struttura non sempre omogenea) viene creata e ritornata
 * una struttura sempre uguale in modo che il componente front possa renderizzare correttamente le
 * informazioni, e creare un componente riciclabile
 *
 * in questo modulo si assume che la tipologia di errore ritornato provenga dalla chiamata detail di DRF
 * corrispondente. Per maggiori dettagli vedi https://www.django-rest-framework.org/api-guide/exceptions/#apiexception
 *
 * Il principale problema è che drf utilizza una funzione ricorsiva per parsare gli errori, quindi
 * capire la struttura finale che viene ritornata non è semplice a meno che non venga sovrascritta.
 *
 * Ogni errore infatti può essere una stringa un array o un dizionario
 */
import {AxiosResponse} from "axios";
import {APIExceptionError, FormErrors, StringKeyArrayString} from "@/interfaces/ApiInfo";

export default class FormException {
    //errori generici della form per esempio errore di autenticazione
    private form_errors: string[];
    //errori relativi ai campi della form per esempio errore di tipo o campo obbligatorio
    private field_errors: StringKeyArrayString;
    //altre tipologie di errori, per esempio vincoli di chiave o unique together
    private non_field_errors: string[];

    constructor() {
        this.form_errors = []
        this.field_errors = {}
        this.non_field_errors = []
    }

    reset() {
        this.form_errors = []
        this.field_errors = {}
        this.non_field_errors = []
    }

    getFieldErrors(data: any) {
        /**
         * in teoria qui non serve che faccia nulla
         * mi trovo un oggetto chiave valore dove gli elementi sono array di stringhe e le chiavi sono i nomi dei campi
         */
        this.field_errors = data
    }

    getNonFieldErrors(data: any) {
        /**
         * in teoria qui non serve che faccia nulla
         * mi trovo un array di stringhe
         */
        this.non_field_errors = data
    }

    getFormErrors(data: any) {
        /**
         * qui si fa un'assunzione sul tipo: è un oggetto con elementi di tipo stringa o di tipo array di stringhe
         * in realtà così dovrebbe essere perché DRF forza tutto a stringa se non si tratta di una lista (cioé Array)
         */
        let ret: string[] = []
        try {

            for (let [key, value] of Object.entries(data)) {
                if ((value as string[]).constructor == Array) {
                    ret = ret.concat(value as string[])
                } else if ((value as string).constructor == String) {
                    ret.push(value as string)
                }
            }
        } catch (e) {
            ret = []
        }
        this.form_errors = ret
    }

    hasNonFieldErrorKey(data: any) {
        return Object.prototype.hasOwnProperty.call(data, 'non_field_errors')
    }

    hasFieldErrorKey(data: any) {
        return Object.prototype.hasOwnProperty.call(data, 'field_errors')
    }

    getErrors(response:AxiosResponse<any>): FormErrors{
        this.reset()
        this.parseRequest(response);

        return {
            non_field_errors: this.non_field_errors,
            field_errors: this.field_errors,
            form_errors: this.form_errors
        }
    }

    get fieldErrors(){
        return this.field_errors
    }

    get nonFieldErrors(){
        return this.non_field_errors
    }

    get formErrors(){
        return this.form_errors
    }

    parseRequest(response: AxiosResponse<any>) {
        switch (response.status) {
            case APIExceptionError.HTTP_400_BAD_REQUEST:
                //di base qui dentro arrivano gli errori di validazione dei campi
                if (this.hasNonFieldErrorKey(response.data)) {
                    this.getNonFieldErrors(response.data.non_field_errors)
                    if (this.hasFieldErrorKey(response.data)) {
                        this.getFieldErrors(response.data.field_errors)
                    }
                } else {
                    /**
                     * se le chiave non_field_errors non è presenti ??allora?? non c'è nemmeno field_errors
                     * e quindi tutti gli errori sono errori di campi
                     */
                    this.getFieldErrors(response.data)
                }
                break;
            case APIExceptionError.HTTP_500_INTERNAL_SERVER_ERROR:
                this.form_errors = ['Internal server error']
                break;
            default:
                /**
                 * in tutti gli altri casi si tratta di errori di form
                 */
                this.getFormErrors(response.data)
        }
    }
}