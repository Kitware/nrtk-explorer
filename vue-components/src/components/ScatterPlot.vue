<script setup  lang="ts">
import { ref, unref, watch, onMounted, toRefs } from "vue";

import  type { Ref } from "vue";

import type { Vector3, Vector2 } from "../types";

import { ScatterGL } from "scatter-gl";

type Props = {
  points: Ref<Vector3<number>[] | Vector2<number>[]>;
}

type Events = {
  click: [point: number | null];
  select: [points: number[]];
}

const props = defineProps<Props>();
const emit = defineEmits<Events>();

const plotContainer = ref<HTMLDivElement>();
let scatterPlot: ScatterGL | undefined;

const selectMode = ref<boolean>(false);

function drawPoints(points: Vector3<number>[] | Vector2<number>[]) {
if (!scatterPlot) {
    return;
  }

  const dataset = new ScatterGL.Dataset(points);
  scatterPlot.render(dataset);

  (scatterPlot as any).scatterPlot.render();
}

watch(props.points, function(newValue, oldValue){
  drawPoints(unref(props.points));
});

onMounted(() => {
  if (!plotContainer.value) {
    return;
  }

  scatterPlot = new ScatterGL(plotContainer.value, {
    rotateOnStart: false,
    onClick(point) {
      emit('click', point);
    },
    onSelect(points) {
      emit('select', points);
    },
  });

  drawPoints(unref(props.points));
});

function onSelectModeClick(ev: MouseEvent) {
  if (selectMode.value) {
    return;
  }

  selectMode.value = true;

  scatterPlot?.setSelectMode();
}

function onPanModeClick(ev: MouseEvent) {
  if (!selectMode.value) {
    return;
  }

  selectMode.value = false;

  scatterPlot?.setPanMode();
}

function onSpinClick(ev: MouseEvent) {
  if (scatterPlot?.isOrbiting()) {
    scatterPlot?.stopOrbitAnimation();
  } else {
    scatterPlot?.startOrbitAnimation();
  }
}

</script>

<template>
  <div style="width: 100%; height: 100%; position: relative;">
    <div style="position:absolute; top: 0; left: 0; width: 100%; height: 100%;" ref="plotContainer"></div>
    <div style="position:absolute; top: 0; left: 0;" class="q-pa-md q-gutter-sm">
      <q-toolbar classes="bg-purple q-pa-md q-gutter-y-sm shadow-2">
        <q-btn round :color="selectMode ? 'white' : 'grey'" text-color="black" icon="videocam" @click="onPanModeClick"/>
        <q-btn round :color="selectMode ? 'grey' : 'white'" text-color="black" icon="highlight_alt" @click="onSelectModeClick" />
        <q-btn round color="white" text-color="black" icon="360" @click="onSpinClick" />
        <q-separator></q-separator>
      </q-toolbar>
    </div>
  </div>
</template>
