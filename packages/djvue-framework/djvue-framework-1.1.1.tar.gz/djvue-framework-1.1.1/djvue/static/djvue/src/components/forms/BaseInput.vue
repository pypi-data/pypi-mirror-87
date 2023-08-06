<template>
    <b-form-group
        :class="$attrs.field_class"
        :id="`label-${$attrs.label}`"
        :label="$attrs.label"
        :label-for="$attrs.name"
        :description="$attrs.help_text"
        :label-cols="$attrs.labelCols"
        :label-cols-sm="$attrs.labelColsSm"
        :label-cols-md="$attrs.labelColsMd"
        :label-cols-lg="$attrs.labelColsLg"
        :label-cols-xl="$attrs.labelColsXl"
        :label-align="$attrs.labelAlign"
        :label-align-sm="$attrs.labelAlignSm"
        :label-align-md="$attrs.labelAlignMd"
        :label-align-lg="$attrs.labelAlignLg"
        :label-align-xl="$attrs.labelAlignXl"
    >
        <slot></slot>
    </b-form-group>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';

@Component({
    name: 'BaseInput',
})
export default class BaseInput extends Vue {
}
</script>
