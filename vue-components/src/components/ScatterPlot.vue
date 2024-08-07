<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { ScatterGL, Dataset, type Sequence } from 'scatter-gl'

import { createColorMap, linearScale } from '@colormap/core'
import { viridis, cividis, magma, inferno } from '@colormap/presets'
import type { ColorMap } from '@colormap/core'

import type { Vector3, Vector2 } from '../types'
import { toRGB } from '../utilities/colors'

interface Props<Vector extends Vector3<number> | Vector2<number>> {
  cameraPosition: number[]
  highlightedPoint: number
  points: Vector[]
  transformedPoints: Vector[]
  selectedPoints: number[]
}

const props = withDefaults(defineProps<Props<Vector3<number> | Vector2<number>>>(), {
  cameraPosition: () => [],
  highlightedPoint: () => -1,
  points: () => [],
  transformedPoints: () => [],
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
const colors = ref({ viridis, cividis, magma, inferno })
const colorMapName = ref<keyof typeof colors.value>('viridis')
const domain: Vector2<number> = [0, 1]
const range: Vector2<number> = [0, 1]
const scale = linearScale(domain, range)
const colorMapDomain = ref<Vector2<number>>(domain)
const colorMap = ref<ColorMap>(createColorMap(colors.value[colorMapName.value], scale))

let currenthighlightedPoint: number = -1
let scatterPlot: ScatterGL | undefined
let hideSourcePoints = ref(false)

onMounted(() => {
  if (!plotContainer.value) {
    return
  }

  scatterPlot = new ScatterGL(plotContainer.value, {
    rotateOnStart: false,
    selectEnabled: true,
    pointColorer(i) {
      if (i == currenthighlightedPoint) {
        return `rgba(255,0,0,255)`
      }

      if (i >= props.points.length) {
        const nPoints = props.points.length
        const transformedPointIndex = i - nPoints
        const pointIndex = props.selectedPoints[transformedPointIndex]
        const p0 = props.points[pointIndex]
        const p1 = props.transformedPoints[transformedPointIndex]
        const dx = Math.abs(p0[0] - p1[0])
        const dy = Math.abs(p0[1] - p1[1])
        const dz = p0.length == 3 && p1.length == 3 ? Math.abs(p0[2] - p1[2]) : 0
        const dist = Math.sqrt(dx * dx + dy * dy + dz * dz)
        const color = colorMap.value(dist)
        return `rgba(${toRGB(color)}, 255)`
      }

      if (props.selectedPoints.indexOf(i) > -1) {
        // Return silver for selected points
        return `rgba(189,189,189,255)`
      }

      // Return blue for unselected points
      let alpha = hideSourcePoints.value ? 0 : 255
      return `rgba(25,118,210,${alpha})`
    },
    onHover(index: number | null) {
      emit('hover', index)
    },
    onSelect(indices) {
      onPanModeClick()
      scatterPlot!.setSequences([])
      emit('select', indices)
    }
  })
  ;(window as any).scatterPlot = scatterPlot

  let cameraControls = ((scatterPlot as any).scatterPlot as any).orbitCameraControls

  cameraControls.addEventListener('start', emitCameraPosition)
  cameraControls.addEventListener('change', emitCameraPosition)
  cameraControls.addEventListener('end', emitCameraPosition)

  updateCameraPosition(props.cameraPosition)
  updateColorMapDomain()
  drawPoints()
  drawLines()
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
      ds = new ScatterGL.Dataset([...props.points, ...props.transformedPoints])
    }
    scatterPlot.render(ds)
    ;(scatterPlot as any).scatterPlot.render()
  }
}

function drawLines() {
  if (scatterPlot) {
    // Due to a bug in scatter-gl we unselect all points before setting the sequences
    scatterPlot?.select([])
    if (props.selectedPoints.length > 0) {
      const originalLength = props.points.length
      const sequences: Sequence[] = props.transformedPoints.map((_, i) => ({
        indices: [props.selectedPoints[i], i + originalLength]
      }))
      scatterPlot.setSequences(sequences)
    } else {
      scatterPlot.setSequences([])
    }
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

function updateColorMapDomain() {
  let bounds: Vector3<Vector2<number>> = [
    [Infinity, -Infinity],
    [Infinity, -Infinity],
    [Infinity, -Infinity]
  ]

  for (let i = 0; i < props.points.length; ++i) {
    for (let j = 0; j < 3; ++j) {
      const v = props.points[i][j] || 0
      if (v < bounds[j][0]) {
        bounds[j][0] = v
      }
      if (v > bounds[j][1]) {
        bounds[j][1] = v
      }
    }
  }

  const spans: Vector3<number> = [
    bounds[0][1] - bounds[0][0],
    bounds[1][1] - bounds[1][0],
    bounds[2][1] - bounds[2][0]
  ]

  colorMapDomain.value = [0, Math.max(...spans) / 3]
}

watch(() => props.cameraPosition, updateCameraPosition)
watch(
  () => props.points,
  () => {
    updateColorMapDomain()
    drawPoints()
  }
)
watch(
  () => props.transformedPoints,
  () => {
    drawPoints()
    drawLines()
  }
)
watch(
  () => props.selectedPoints,
  () => {
    drawPoints()
    drawLines()
  }
)

watch(
  () => props.highlightedPoint,
  (newValue) => {
    if (scatterPlot) {
      if (newValue == -1) {
        currenthighlightedPoint = -1
        scatterPlot.setHoverPointIndex(-1)
      } else {
        currenthighlightedPoint = newValue
        scatterPlot.setHoverPointIndex(newValue)
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

function onHideModeClick() {
  if (hideSourcePoints.value) {
    hideSourcePoints.value = false
  } else {
    hideSourcePoints.value = true
  }

  drawPoints()
  drawLines()
}

function onColorMapChange(name: keyof typeof colors.value) {
  colorMapName.value = name
  const scale = linearScale(colorMapDomain.value, range)
  colorMap.value = createColorMap(colors.value[name], scale)

  if (scatterPlot) {
    ;(scatterPlot as any).scatterPlot.render()
  }
}

function onContainerResize() {
  if (scatterPlot) {
    scatterPlot.resize()
  }
}
</script>

<template>
  <q-resize-observer @resize="onContainerResize" :debounce="50" />
  <div style="width: 100%; height: 100%; position: relative; overflow: hidden">
    <div
      style="position: absolute; top: 0; left: 0; width: 100%; height: 100%"
      ref="plotContainer"
    ></div>
    <div style="position: absolute; top: 0; left: 0" class="q-pa-md q-gutter-sm">
      <q-toolbar classes="q-gutter-y-sm shadow-2">
        <q-btn
          class="q-ma-sm"
          round
          :color="selectMode ? 'white' : 'grey'"
          text-color="black"
          icon="mouse"
          @click="onPanModeClick"
        />
        <q-btn
          class="q-ma-sm"
          round
          :color="selectMode ? 'grey' : 'white'"
          text-color="black"
          icon="highlight_alt"
          @click="onSelectModeClick"
        />
        <q-btn
          class="q-ma-sm"
          round
          color="white"
          text-color="black"
          icon="refresh"
          @click="onResetModeClick"
        />
        <q-btn
          class="q-ma-sm"
          round
          :color="hideSourcePoints ? 'grey' : 'white'"
          text-color="black"
          icon="hide_source"
          @click="onHideModeClick"
        />
        <q-btn-dropdown class="q-ma-sm" rounded :label="colorMapName">
          <q-list>
            <q-item
              v-for="(_, key) in colors"
              clickable
              v-close-popup
              @click="() => onColorMapChange(key)"
              :key="key"
            >
              <q-item-section>
                <q-item-label>{{ key }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
        <q-separator></q-separator>
      </q-toolbar>
    </div>
  </div>
</template>
