<script setup  lang="ts">

import { ref, unref, watch, onMounted, toRefs } from "vue";
import { ScatterGL } from "scatter-gl";

import type { Ref } from "vue";
import type { Vector3, Vector2 } from "../types";

interface Props {
  cameraPosition: Ref<number[]>;
  highlightedPoint: Ref<number>;
  plotTransformations: Ref<boolean>;
  points: Ref<Vector3<number>[] | Vector2<number>[]>;
  userSelectedPoints: Ref<number[]>;
}

type Events = {
  cameraMove: [cameraPosition: Vector3<number>];
  hover: [point: number | null];
  select: [points: number[]];
}

const emit = defineEmits<Events>();
const props = defineProps<Props>();

const plotContainer = ref<HTMLDivElement>();
const plotTransformations = ref<boolean>(false);
const selectMode = ref<boolean>(false);

let cameraPosition: number[] = [];
let scatterPlot: ScatterGL | undefined;
let userSelectedPoints: number[] = [];

onMounted(() => {
  if (!plotContainer.value) {
    return;
  }

  userSelectedPoints = unref(props.userSelectedPoints);
  plotTransformations.value = unref(props.plotTransformations);

  scatterPlot = new ScatterGL(plotContainer.value, {
    rotateOnStart: false,
    selectEnabled: !plotTransformations.value,
    onHover(point) {
      emit('hover', point);
    },
    onSelect(points) {
      selectMode.value = true;
      scatterPlot?.setSelectMode();
      emit('select', points);
    },
    onCameraMove(position, target) {
      // This callback is bogus since it triggers after clicking.
    },
  });

  let plotImpl = ((scatterPlot as any).scatterPlot as any);
  plotImpl.orbitCameraControls.addEventListener('end', () => {
      plotImpl.stopOrbitAnimation();
      const cameraPosition = plotImpl.camera.position.toArray();
      emit('cameraMove', cameraPosition);
  });

  drawPoints(unref(props.points));
});

function drawPoints(points: Vector3<number>[] | Vector2<number>[]) {
  if (!scatterPlot) {
    return;
  }

  scatterPlot.setPointColorer((i, arg1, arg2) => {
    if (userSelectedPoints.indexOf(i) > -1) {
      return 'grey';
    }

    if (plotTransformations.value) {
      const numValues = userSelectedPoints.length;
      const originalLength = points.length - numValues;
      if (numValues > 0 && i >= originalLength) {
        return 'red';
      }
    }

    return 'blue';
  });

  const dataset = new ScatterGL.Dataset(points);
  scatterPlot.render(dataset);
  (scatterPlot as any).scatterPlot.render();
}

watch(props.cameraPosition, function(newValue, oldValue){
  let pos = unref(props.cameraPosition);

  // Only update position if it is different, otherwise this can trigger an infinite loop
  if (pos.length != cameraPosition.length || !pos.every(function(v, i) { return v === cameraPosition[i]}))
  {
    cameraPosition = pos;
    if (scatterPlot) {
      (scatterPlot as any).scatterPlot.setCameraPositionAndTarget(cameraPosition, [0,0,0]);
    }
  }
});

watch(props.highlightedPoint, function(newValue, oldValue){
  if (scatterPlot) {
    scatterPlot.setHoverPointIndex(newValue);
  }
});

watch(props.points, function(newValue, oldValue){
  drawPoints(newValue);
});

watch(props.userSelectedPoints, function(newValue, oldValue){
  userSelectedPoints = newValue;
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
    <div v-if="!plotTransformations" style="position:absolute; top: 0; left: 0;" class="q-pa-md q-gutter-sm">
      <q-toolbar classes="bg-purple q-pa-md q-gutter-y-sm shadow-2">
        <q-btn round :color="selectMode ? 'white' : 'grey'" text-color="black" icon="videocam" @click="onPanModeClick"/>
        <q-btn round :color="selectMode ? 'grey' : 'white'" text-color="black" icon="highlight_alt" @click="onSelectModeClick" />
        <q-btn round color="white" text-color="black" icon="360" @click="onSpinClick" />
        <q-separator></q-separator>
      </q-toolbar>
    </div>
  </div>
</template>
