<!-- Partially from https://github.com/emedware/v3-gl-ext -->

<template>
    <i style="display: none;">Slots extraction</i>
</template>

<script lang="ts" setup>
import {getCurrentInstance, type Slots} from "vue";

defineExpose({
    slots: <Slots>getCurrentInstance()?.slots
});
</script>
