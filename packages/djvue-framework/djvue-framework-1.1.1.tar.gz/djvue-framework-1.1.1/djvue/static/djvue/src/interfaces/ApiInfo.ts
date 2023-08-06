import DjVueCheckbox from "@/components/forms/DjVueCheckbox.vue";

export interface SearchFilter {
    search_fields: string[];
    search_param: string;
}

export interface OrderingFilter {
    ordering_fields: string[];
    ordering_param: string;
}

export interface FormMeta {
    form_class: string
}

export interface FieldMeta {
    type: string,
    name: string,
    required?: boolean,
    read_only?: boolean,
    label?: string,
    placeholder?: string,
    min_value?: number,
    max_value?: number,
    step?: number,
}

export interface GETAction {
    is_paginated: boolean
    page_size: number
    page_param: string
    search_filter: SearchFilter
    ordering_filter: OrderingFilter
    list_fields: any[]
    has_extra_buttons: boolean
    allow_creation: boolean
    list_select_key: string
    fields: FieldDefinition
    create_button: object
    has_footer: boolean
    tableProps?: object
}

export interface ApiInfo {
    name: string
    description: string
    renders: string[]
    parses: string[]
    actions: HttpMethod
}

export interface FormMeta {
    form_class: string;
}

export enum FormLayout {
    NONE = 0,
    INLINE,
}

export interface ModelCreatedResponse {
    baseUrl: string;
    model: object | undefined;
}

export interface ModelInfo{
    listBaseUrl: string
    detailBaseUrl: string
}

export interface FieldMeta {
    //il componente da usare
    component?: string;
    //widget front da usare
    widget?: DVFormWidget;
    type: string;
    name: string;
    required?: boolean;
    //valore di default
    default?: any;
    allow_blank?: boolean | null;
    read_only?: boolean;
    //label da visualizzare
    label?: string;
    //placeholder da visualuzzare
    placeholder?: string;
    min_value?: number;
    max_value?: number;
    step?: number;
    //url autocompletamento
    ac?: boolean;
    many?: boolean;
    //nel caso di campi con select contiene le ozioni
    options?: any[];
    allowCreation: boolean;
    modelPath: string;
    createModelPath: string;
    size: string;
    help_text: string;
    allow_null?: boolean;
    child? : any
    model?: ModelInfo
    append?: string
    prepend?: string
    input_class?: string
}

export interface StringKeyAnyObject {
    [key: string]: any;
}

export interface StringKeyArrayString {
    [key: string]: string[];
}

export interface FieldDefinition {
    [key: string]: FieldMeta;
}

export interface HttpAction {
    fields: FieldDefinition;
    form: FormMeta;
}

export enum EHttpMethod {
    POST = 'POST',
    GET = 'GET',
    PATCH = 'PATCH',
    PUT = 'PUT',
    OPTIONS = 'OPTIONS',
    HEAD = 'HEAD',
}

type HttpMethod = {
    [key in keyof typeof EHttpMethod]: HttpAction
}

export enum EOperation {
    CREATE = 0,
    UPDATE = 1,
    DELETE = 2,
    DETAIL = 3,
}


export interface FormOption {
    name: string;
    description: string;
    renders: string[];
    parses: string[];
    actions: HttpMethod;
}

export interface Autocomplete {
    id: number;
    text: string;
    extra?: any;
}

export enum ExtraButtonType {
    MODAL = 1,
    BUTTON = 2
}

export interface TableActionInterface {
    key: string;
    type: ExtraButtonType;
    props: StringKeyAnyObject;
}

export interface TableField {
    key: string;
    label: string;
    sortable: boolean;
}

export enum APIExceptionError {
    HTTP_400_BAD_REQUEST = 400,
    HTTP_401_UNAUTHORIZED = 401,
    HTTP_403_FORBIDDEN = 403,
    HTTP_404_NOT_FOUND = 404,
    HTTP_405_METHOD_NOT_ALLOWED = 405,
    HTTP_406_NOT_ACCEPTABLE = 406,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415,
    HTTP_429_TOO_MANY_REQUESTS = 429,
    HTTP_500_INTERNAL_SERVER_ERROR = 500,
}
export enum DVFormWidget{
    BASE_INPUT,
    CHECKBOX,
    TEXTAREA,
    HIDDEN,
    DJVUE_SELECT,
    DJVUE_CHECKBOX_GROUP,
    DJVUE_RADIO_GROUP,
    DJVUE_AC_SELECT,
    DJVUE_INPUT_GROUP
}

export interface FormErrors{
    form_errors: string[];
    non_field_errors:string[];
    field_errors: StringKeyArrayString;
}