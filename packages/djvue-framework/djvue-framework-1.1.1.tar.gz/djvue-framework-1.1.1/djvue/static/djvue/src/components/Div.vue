<template>
    <div>
        <slot></slot>
    </div>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';

@Component({
    name: 'Div',
    components: {
    },
})
export default class Div extends Vue {
}
</script>

<style lang="scss" scoped>

</style>
