<script setup>
import {ref} from 'vue'
import {defaultLayoutConfig, GoldenLayout} from "@/components/golden/index.js";
import Lines from "@/components/Lines.vue";
import Stations from "@/components/Stations.vue";

const GLayoutRoot = ref();

</script>

<template>
    <golden-layout ref="GLayoutRoot" :config="defaultLayoutConfig" id="layout-body">
        <template v-slot:lines>
            <Lines/>
        </template>

        <template v-slot:stations>
            <Stations/>
        </template>

        <template v-slot:cards>
            Cards
        </template>

        <template v-slot:passengers>
            Passengers
        </template>
    </golden-layout>
</template>

<style scoped>
</style>
