<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { ScatterGL, Dataset } from 'scatter-gl'

import type { Vector3, Vector2 } from '../types'

interface Props {
  cameraPosition: number[]
  highlightedPoint: number
  displayControl: boolean
  points: Vector3<number>[] | Vector2<number>[]
  selectedPoints: number[]
}

const props = withDefaults(defineProps<Props>(), {
  cameraPosition: () => [],
  highlightedPoint: -1,
  displayControl: true,
  points: () => [],
  selectedPoints: () => []
})

type Events = {
  cameraMove: [camera_position: Vector3<number> | Vector2<number>]
  hover: [point: number | null]
  select: [indices: number[]]
}

const emit = defineEmits<Events>()

const plotContainer = ref<HTMLDivElement>()
const selectMode = ref<boolean>(false)

let scatterPlot: ScatterGL | undefined

onMounted(() => {
  if (!plotContainer.value) {
    return
  }

  scatterPlot = new ScatterGL(plotContainer.value, {
    rotateOnStart: false,
    selectEnabled: props.displayControl,
    pointColorer(i) {
      if (props.selectedPoints.indexOf(i) > -1) {
        return 'grey'
      }
      if (!props.displayControl) {
        const numValues = props.selectedPoints.length
        const originalLength = props.points.length - numValues
        if (numValues > 0 && i >= originalLength) {
          return 'red'
        }
      }
      return 'blue'
    },
    onHover(index) {
      if (!props.displayControl && index != null) {
        const realLen = props.points.length - props.selectedPoints.length
        if (index > realLen - 1) {
          const selectedPointsIdx = index - realLen
          index = props.selectedPoints[selectedPointsIdx]
        }
      }
      emit('hover', index)
    },
    onSelect(indices) {
      onPanModeClick()
      emit('select', indices)
    }
  })

  let cameraControls = ((scatterPlot as any).scatterPlot as any).orbitCameraControls

  cameraControls.addEventListener('start', emitCameraPosition)
  cameraControls.addEventListener('change', emitCameraPosition)
  cameraControls.addEventListener('end', emitCameraPosition)

  updateCameraPosition(props.cameraPosition)
  drawPoints()
})

function emitCameraPosition() {
  if (scatterPlot) {
    let plotImpl = (scatterPlot as any).scatterPlot as any
    emit('cameraMove', plotImpl.camera.position.toArray())
  }
}

function drawPoints() {
  if (scatterPlot) {
    let ds: Dataset
    if (props.points.length <= 0) {
      // If there are no points, we need to create a dataset with at least one point
      ds = new ScatterGL.Dataset([[0, 0, 0]])
      // Then we remove the point
      ds.points = []
    } else {
      ds = new ScatterGL.Dataset(props.points)
    }
    scatterPlot.render(ds)
    ;(scatterPlot as any).scatterPlot.render()
  }
}

// Update the camera position if the prop changes
function updateCameraPosition(newValue: number[], oldValue: number[] = []) {
  // Only update if the parameters fit the precondition
  if (
    (newValue.length != 2 && newValue.length != 3) ||
    !newValue.every(function (v) {
      return v != null
    })
  ) {
    return
  }

  // Only update position if it is different, otherwise this can trigger an infinite loop
  if (
    (oldValue.length != 2 && oldValue.length != 3) ||
    !newValue.every(function (v, i) {
      v === oldValue[i]
    })
  ) {
    if (scatterPlot) {
      ;(scatterPlot as any).scatterPlot.setCameraPositionAndTarget(newValue, [0, 0, 0])
    }
  }
}

watch(() => props.cameraPosition, updateCameraPosition)
watch(() => props.points, drawPoints)
watch(
  () => props.highlightedPoint,
  function (newValue) {
    if (scatterPlot) {
      scatterPlot.setHoverPointIndex(newValue)

      if (!props.displayControl) {
        const transformationIdx = props.selectedPoints.indexOf(newValue)
        if (transformationIdx > -1) {
          const revIndex = props.selectedPoints.length - transformationIdx
          const index = props.points.length - revIndex
          scatterPlot.setHoverPointIndex(index)
        }
      }
    }
  }
)

function onSelectModeClick() {
  if (!selectMode.value) {
    selectMode.value = true
    scatterPlot?.setSelectMode()
  }
}

function onPanModeClick() {
  if (selectMode.value) {
    selectMode.value = false
    scatterPlot?.setPanMode()
  }
}

function onResetModeClick() {
  scatterPlot?.resetZoom()
  emitCameraPosition()
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
          icon="mouse"
          @click="onPanModeClick"
        />
        <q-btn
          round
          :color="selectMode ? 'grey' : 'white'"
          text-color="black"
          icon="highlight_alt"
          @click="onSelectModeClick"
        />
        <q-btn round color="white" text-color="black" icon="refresh" @click="onResetModeClick" />
        <q-separator></q-separator>
      </q-toolbar>
    </div>
  </div>
</template>
