<script setup lang="ts">
import { ref, watchEffect, computed } from 'vue'

import { Quadtree, Rectangle } from '@timohausmann/quadtree-ts'

import type { Annotation, Category, Vector3 } from '../types'

const CATEGORY_COLORS: Vector3<number>[] = [
  [255, 0, 0],
  [0, 255, 0],
  [0, 0, 255],
  [255, 255, 0],
  [255, 0, 255],
  [0, 255, 255]
]

interface Props {
  identifier: string
  src: string
  annotations: Annotation[]
  categories: { [key: number]: Category }
  selected: boolean
}

let annotationsTree: Quadtree<Rectangle<number>> | undefined = undefined

function doRectanglesOverlap(recA: Rectangle<any>, recB: Rectangle<any>) {
  const noHOverlap: boolean = recB.x >= recA.x + recA.width || recA.x >= recB.x + recB.width

  if (noHOverlap) {
    return false
  }

  const noVOverlap: boolean = recB.y >= recA.y + recA.height || recA.y >= recB.y + recB.height

  return !noVOverlap
}

const props = defineProps<Props>()

const visibleCanvas = ref<HTMLCanvasElement>()
const pickingCanvas = ref<HTMLCanvasElement>()
const labelContainer = ref<HTMLDivElement>()

const showLabelContainer = ref(false)

const imageSize = ref({ width: 0, height: 0 })
const img = ref<HTMLImageElement>()
const onImageLoad = () => {
  imageSize.value = { width: img.value?.naturalWidth ?? 0, height: img.value?.naturalHeight ?? 0 }
}

// draw visible annotations
watchEffect(() => {
  const canvas = visibleCanvas.value
  if (!canvas) {
    return
  }
  const ctx = canvas.getContext('2d')
  if (!ctx) {
    console.error('Could not get 2d context')
    return
  }

  canvas.width = imageSize.value.width
  canvas.height = imageSize.value.height
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  const opacity = 0.5
  props.annotations.forEach((annotation) => {
    const color = CATEGORY_COLORS[annotation.category_id % CATEGORY_COLORS.length]
    ctx.fillStyle = `rgba(${[...color, opacity].join(',')})`
    ctx.fillRect(annotation.bbox[0], annotation.bbox[1], annotation.bbox[2], annotation.bbox[3])
  })
})

// draw picking annotations
watchEffect(() => {
  const canvas = pickingCanvas.value
  if (!canvas) {
    return
  }
  const ctx = canvas.getContext('2d')
  if (!ctx) {
    console.error('Could not get 2d context')
    return
  }

  canvas.width = imageSize.value.width
  canvas.height = imageSize.value.height
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  annotationsTree = new Quadtree({
    width: canvas.width,
    height: canvas.height,
    maxLevels: 8,
    maxObjects: 10
  })

  props.annotations.forEach((annotation, i) => {
    const treeNode = new Rectangle<number>({
      x: annotation.bbox[0],
      y: annotation.bbox[1],
      width: annotation.bbox[2],
      height: annotation.bbox[3],
      data: i
    })
    annotationsTree?.insert(treeNode)
    ctx.fillStyle = `rgb(255, 0, 0)`
    ctx.fillRect(annotation.bbox[0], annotation.bbox[1], annotation.bbox[2], annotation.bbox[3])
  })
})

interface HoverEvent {
  id: string
}

type Events = {
  hover: [HoverEvent]
}

const emit = defineEmits<Events>()

function mouseEnter() {
  emit('hover', { id: props.identifier })
}

function mouseLeave() {
  showLabelContainer.value = false
  emit('hover', { id: '' })
}

function displayToPixel(x: number, y: number, canvas: HTMLCanvasElement): [number, number] {
  const canvasBounds = canvas.getBoundingClientRect()

  const pixelX = (canvas.width * (x - canvasBounds.left)) / canvasBounds.width
  const pixelY = (canvas.height * (y - canvasBounds.top)) / canvasBounds.height

  return [pixelX, pixelY]
}

function mouseMove(e: MouseEvent) {
  if (
    !pickingCanvas.value ||
    pickingCanvas.value.width === 0 ||
    !labelContainer.value ||
    !annotationsTree ||
    !props.categories ||
    !props.annotations
  ) {
    return
  }

  const [pixelX, pixelY] = displayToPixel(e.clientX, e.clientY, pickingCanvas.value)

  const ctx = pickingCanvas.value.getContext('2d')

  if (!ctx) {
    return
  }

  const pixelValue = ctx.getImageData(pixelX, pixelY, 1, 1).data[0]

  const pickedSomething = pixelValue > 0

  if (pickedSomething) {
    labelContainer.value.style.left = `${e.offsetX + 8}px`
    labelContainer.value.style.top = `${e.offsetY + 8}px`
    showLabelContainer.value = true
  } else {
    showLabelContainer.value = false
  }

  if (pickedSomething) {
    const pixelRectangle = new Rectangle<number>({ x: pixelX, y: pixelY, width: 2, height: 2 })

    const hits = annotationsTree
      .retrieve(pixelRectangle)
      .filter((rect: any) => doRectanglesOverlap(rect, pixelRectangle))

    let list = document.createElement('ul')
    list.style.padding = '0'
    list.style.margin = '0'

    hits.forEach((hit) => {
      const item = document.createElement('li')
      if (hit.data != undefined) {
        const annotation = props.annotations[hit.data]
        const { name } = props.categories[annotation.category_id] ?? { name: 'Unknown' }
        item.textContent = `(${annotation.id}): ${name}`
        const color = CATEGORY_COLORS[annotation.category_id % CATEGORY_COLORS.length]
        item.style.textShadow = `rgba(${color.join(',')},0.6) 1px 1px 3px`
        list.appendChild(item)
      }
    })

    labelContainer.value.replaceChildren(list)
  }
}

const borderSize = computed(() => (props.selected ? '4' : '0'))
</script>

<template>
  <div style="width: 100%; position: relative; white-space: pre; font-size: small">
    <img
      :src="src"
      ref="img"
      @load="onImageLoad"
      :style="{ outlineWidth: borderSize + 'px' }"
      style="
        width: 100%;
        position: relative;
        left: 0;
        top: 0;
        outline-style: dotted;
        outline-color: red;
      "
    />
    <canvas ref="visibleCanvas" style="width: 100%; position: absolute; left: 0; top: 0"></canvas>
    <div
      v-show="showLabelContainer"
      ref="labelContainer"
      style="
        position: absolute;
        background-color: #efefef;
        z-index: 10;
        list-style-position: inside;
        padding: 0.4rem;
        border-radius: 0.2rem;
        border-color: rgba(127, 127, 127, 0.75);
        border-style: solid;
        border-width: thin;
      "
    ></div>
    <canvas
      ref="pickingCanvas"
      style="opacity: 0; width: 100%; position: absolute; left: 0; top: 0"
      @mouseenter="mouseEnter"
      @mousemove="mouseMove"
      @mouseleave="mouseLeave"
    ></canvas>
  </div>
</template>
