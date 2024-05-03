<script setup>
import {ref} from 'vue'
import {defaultLayoutConfig, GoldenLayout} from "@/components/golden/index.js";
import Lines from "@/components/Lines.vue";
import Stations from "@/components/Stations.vue";
import interact from "interactjs";

const GLayoutRoot = ref();

interact('.el-dialog')
    .draggable({
        inertia: true,
        autoScroll: true,
        listeners: {
            move: (event) => {
                let target = event.target;
                let x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
                let y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

                target.style.transform = 'translate(' + x + 'px, ' + y + 'px)';

                target.setAttribute('data-x', x);
                target.setAttribute('data-y', y);
            }
        }
    });
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
    </golden-layout>
</template>

<style scoped>
</style>
