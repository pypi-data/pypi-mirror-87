<template>
  <span></span>
</template>
<script lang="ts">
import {Component, Prop, Vue} from 'vue-property-decorator';

@Component({
    name: 'DjVueHidden',
})
export default class DjVueHidden extends Vue {
    @Prop() private readonly value!:any
}
</script>
