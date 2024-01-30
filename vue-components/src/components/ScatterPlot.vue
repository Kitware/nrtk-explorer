<script setup lang="ts">
import { ref, unref, watch, onMounted } from 'vue'
import { ScatterGL } from 'scatter-gl'

import type { Ref } from 'vue'
import type { Vector3, Vector2 } from '../types'

interface Props {
  cameraPosition: Ref<number[]>
  highlightedPoint: Ref<number>
  displayControl: boolean
  points: Ref<Vector3<number>[] | Vector2<number>[]>
  selectedPoints: Ref<number[]>
}

const props = withDefaults(defineProps<Props>(), {
  displayControl: true
})

type Events = {
  cameraMove: [cameraPosition: Vector3<number>]
  hover: [point: number | null]
  select: [points: number[]]
}

const emit = defineEmits<Events>()

const plotContainer = ref<HTMLDivElement>()
const selectMode = ref<boolean>(false)

let scatterPlot: ScatterGL | undefined
let userSelectedPoints: number[] = []

onMounted(() => {
  if (!plotContainer.value) {
    return
  }

  userSelectedPoints = unref(props.selectedPoints)

  scatterPlot = new ScatterGL(plotContainer.value, {
    rotateOnStart: false,
    selectEnabled: props.displayControl,
    onHover(point) {
      emit('hover', point)
    },
    onSelect(points) {
      selectMode.value = true
      scatterPlot?.setSelectMode()
      emit('select', points)
    }
  })

  let plotImpl = (scatterPlot as any).scatterPlot as any
  plotImpl.orbitCameraControls.addEventListener('end', () => {
    plotImpl.stopOrbitAnimation()
    const cameraPosition = plotImpl.camera.position.toArray()
    emit('cameraMove', cameraPosition)
  })

  drawPoints(unref(props.points))
})

function drawPoints(points: Vector3<number>[] | Vector2<number>[]) {
  if (!scatterPlot) {
    return
  }

  scatterPlot.setPointColorer((i) => {
    if (userSelectedPoints.indexOf(i) > -1) {
      return 'grey'
    }

    if (!props.displayControl) {
      const numValues = userSelectedPoints.length
      const originalLength = points.length - numValues
      if (numValues > 0 && i >= originalLength) {
        return 'red'
      }
    }

    return 'blue'
  })

  const dataset = new ScatterGL.Dataset(points)
  scatterPlot.render(dataset)
  ;(scatterPlot as any).scatterPlot.render()
}

watch(props.cameraPosition, function (newValue, oldValue) {
  // Only update position if it is different, otherwise this can trigger an infinite loop
  if (
    newValue.length != oldValue.length ||
    !newValue.every(function (v, i) {
      return v === oldValue[i]
    })
  ) {
    if (scatterPlot) {
      ;(scatterPlot as any).scatterPlot.setCameraPositionAndTarget(newValue, [0, 0, 0])
    }
  }
})

watch(props.highlightedPoint, function (newValue) {
  if (scatterPlot) {
    scatterPlot.setHoverPointIndex(newValue)
  }
})

watch(props.points, function (newValue) {
  drawPoints(newValue)
})

watch(props.selectedPoints, function (newValue) {
  userSelectedPoints = newValue
  drawPoints(unref(props.points))
})

function onSelectModeClick() {
  if (selectMode.value) {
    return
  }

  selectMode.value = true

  scatterPlot?.setSelectMode()
}

function onPanModeClick() {
  if (!selectMode.value) {
    return
  }

  selectMode.value = false

  scatterPlot?.setPanMode()
}

function onSpinClick() {
  if (scatterPlot?.isOrbiting()) {
    scatterPlot?.stopOrbitAnimation()
  } else {
    scatterPlot?.startOrbitAnimation()
  }
}
</script>

<template>
  <div style="width: 100%; height: 100%; position: relative">
    <div
      style="position: absolute; top: 0; left: 0; width: 100%; height: 100%"
      ref="plotContainer"
    ></div>
    <div
      v-if="displayControl"
      style="position: absolute; top: 0; left: 0"
      class="q-pa-md q-gutter-sm"
    >
      <q-toolbar classes="bg-purple q-pa-md q-gutter-y-sm shadow-2">
        <q-btn
          round
          :color="selectMode ? 'white' : 'grey'"
          text-color="black"
          icon="videocam"
          @click="onPanModeClick"
        />
        <q-btn
          round
          :color="selectMode ? 'grey' : 'white'"
          text-color="black"
          icon="highlight_alt"
          @click="onSelectModeClick"
        />
        <q-btn round color="white" text-color="black" icon="360" @click="onSpinClick" />
        <q-separator></q-separator>
      </q-toolbar>
    </div>
  </div>
</template>
