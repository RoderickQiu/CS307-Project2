import GlTemplate from "./GlTemplate.vue";
import GoldenLayout from "./GoldenLayout.vue";

export {GlTemplate, GoldenLayout};

export const layoutKey = Symbol("layout");

export const defaultLayoutConfig = {
    root: {
        type: 'stack',
        content: [
            {
                type: 'component',
                componentType: 'stations',
                title: 'Stations',
                height: 20
            },
            {
                type: 'component',
                componentType: 'lines',
                title: 'Lines',
                height: 20
            },
            {
                type: 'component',
                componentType: 'cards',
                title: 'Cards & Passengers',
                height: 20
            },
        ]
    }
};