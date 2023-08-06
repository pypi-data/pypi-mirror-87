<template>
  <b-input-group :prepend="prepend" :append="append" :size="$attrs.size">
    <b-form-input
        v-model="Model"
        :disabled="disabled"
        :class="$attrs.input_class"
        :size="$attrs.size"
        :placeholder="placeholder"
        :state="state"
        ></b-form-input>
  </b-input-group>
</template>

<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';

@Component({
  name: 'DjVueInputGroup',
})
export default class DjVueInputGroup extends Vue {
  @Prop(String) private readonly prepend!: string
  @Prop(String) private readonly append!: string
  @Prop() private readonly value!: string;
  @Prop() private readonly disabled!: boolean;
  @Prop() private readonly placeholder!: string;
  @Prop() private readonly state!: boolean | null;

  get Model() {
    return this.value
  }

  set Model(val: any) {
    this.$emit('input', val)
  }

}
</script>
