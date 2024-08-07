<script setup lang="ts">
import { ref, watchEffect, computed, onMounted, type MaybeRef, unref } from 'vue'

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

const TOOLTIP_OFFSET = [8, 8]
const TOOLTIP_HEIGHT_PADDING = 12 // fudge to keep bottom border from clipping. In pixels

let annotationsTree: Quadtree<Rectangle<number>> | undefined = undefined

function doRectanglesOverlap(recA: Rectangle<any>, recB: Rectangle<any>) {
  const noHOverlap = recB.x >= recA.x + recA.width || recA.x >= recB.x + recB.width

  if (noHOverlap) {
    return false
  }

  const noVOverlap = recB.y >= recA.y + recA.height || recA.y >= recB.y + recB.height

  return !noVOverlap
}

const props = defineProps<{
  identifier: string
  src: MaybeRef<string>
  annotations?: MaybeRef<Annotation[]>
  categories: { [key: number]: Category }
  selected: boolean
  containerSelector?: string
}>()

const visibleCanvas = ref<HTMLCanvasElement>()
const visibleCtx = computed(() => visibleCanvas.value?.getContext('2d', { alpha: true }))
const pickingCanvas = ref<HTMLCanvasElement>()
const pickingCtx = computed(() =>
  pickingCanvas.value?.getContext('2d', { willReadFrequently: true })
)
const labelContainer = ref<HTMLDivElement>()

const imageSize = ref({ width: 0, height: 0 })
const img = ref<HTMLImageElement>()
const onImageLoad = () => {
  imageSize.value = { width: img.value?.naturalWidth ?? 0, height: img.value?.naturalHeight ?? 0 }
}

const annotations = computed(() => unref(props.annotations) ?? [])

const annotationsWithColor = computed(() => {
  return annotations.value.map((annotation) => {
    const mutex = annotation.category_id ?? 0
    const color = CATEGORY_COLORS[mutex % CATEGORY_COLORS.length]
    return { ...annotation, color }
  })
})

// draw visible annotations
watchEffect(() => {
  if (!visibleCanvas.value || !visibleCtx.value) {
    return
  }
  const canvas = visibleCanvas.value
  const ctx = visibleCtx.value

  canvas.width = imageSize.value.width
  canvas.height = imageSize.value.height
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  const opacity = 0.5
  annotationsWithColor.value.forEach(({ color, bbox }) => {
    ctx.fillStyle = `rgba(${[...color, opacity].join(',')})`
    ctx.fillRect(bbox[0], bbox[1], bbox[2], bbox[3])
  })
})

// draw picking annotations
watchEffect(() => {
  if (!pickingCtx.value || !pickingCanvas.value) {
    return
  }
  const canvas = pickingCanvas.value
  const ctx = pickingCtx.value

  canvas.width = imageSize.value.width
  canvas.height = imageSize.value.height
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  annotationsTree = new Quadtree({
    width: canvas.width,
    height: canvas.height,
    maxLevels: 8,
    maxObjects: 10
  })

  annotations.value.forEach((annotation, i) => {
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

function hideLabel() {
  if (labelContainer.value) labelContainer.value.style.visibility = 'hidden'
}

onMounted(hideLabel)

function mouseEnter() {
  emit('hover', { id: props.identifier })
}
function mouseLeave() {
  emit('hover', { id: '' })
  hideLabel()
}

function displayToPixel(x: number, y: number, canvas: HTMLCanvasElement): [number, number] {
  const canvasBounds = canvas.getBoundingClientRect()

  const pixelX = (canvas.width * (x - canvasBounds.left)) / canvasBounds.width
  const pixelY = (canvas.height * (y - canvasBounds.top)) / canvasBounds.height

  return [pixelX, pixelY]
}

const mounted = ref(false)
onMounted(() => {
  mounted.value = true
})
const container = computed(() => {
  if (!mounted.value || !props.containerSelector) return null
  return document.querySelector(props.containerSelector)
})

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
  const ctx = pickingCtx.value
  if (!ctx) {
    return
  }

  const [pixelX, pixelY] = displayToPixel(e.clientX, e.clientY, pickingCanvas.value)
  const pixelValue = ctx.getImageData(pixelX, pixelY, 1, 1).data[0]
  const pickedSomething = pixelValue > 0

  if (!pickedSomething) {
    labelContainer.value.style.visibility = 'hidden'
    return
  }

  labelContainer.value.style.visibility = 'visible'

  const pixelRectangle = new Rectangle<number>({ x: pixelX, y: pixelY, width: 2, height: 2 })
  const hits = annotationsTree
    .retrieve(pixelRectangle)
    .filter((rect: any) => doRectanglesOverlap(rect, pixelRectangle))
    .filter((hit) => hit.data != undefined)
    .map((hit) => {
      const annotation = annotationsWithColor.value[hit.data!]
      const name = props.categories[annotation.category_id]?.name ?? annotation.label
      const color = annotation.color
      const category = document.createElement('li')
      category.style.textShadow = `rgba(${color.join(',')},0.6) 1px 1px 3px`
      const annotationId = annotation.id ? ` : ${annotation.id}` : ''
      category.textContent = `${name}${annotationId}`
      return category
    })

  labelContainer.value.replaceChildren(...hits)

  // Position the tooltip
  const [x, y] = [e.offsetX, e.offsetY]
  let posX = x + TOOLTIP_OFFSET[0]
  let posY = y + TOOLTIP_OFFSET[1]

  const tooltipRect = labelContainer.value.getBoundingClientRect()
  const parentRect = pickingCanvas.value.getBoundingClientRect()
  const containerRect = container.value?.getBoundingClientRect() ?? {
    left: 0,
    top: 0,
    width: window.innerWidth,
    height: window.innerHeight
  }

  const toolTipInContainer = {
    left: parentRect.left + posX - containerRect.left,
    top: parentRect.top + posY - containerRect.top,
    width: tooltipRect.width,
    height: tooltipRect.height + TOOLTIP_HEIGHT_PADDING
  }

  // if text goes off the edge, move up and/or left
  if (toolTipInContainer.left + toolTipInContainer.width > containerRect.width) {
    posX = x - tooltipRect.width - TOOLTIP_OFFSET[0]
  }
  if (toolTipInContainer.top + toolTipInContainer.height > containerRect.height) {
    posY = y - tooltipRect.height - TOOLTIP_OFFSET[1]
  }

  labelContainer.value.style.left = `${posX}px`
  labelContainer.value.style.top = `${posY}px`
}

const borderSize = computed(() => (props.selected ? '4' : '0'))

const src = computed(() => unref(props.src))

const showSpinner = computed(() => !src.value || unref(props.annotations) == undefined)
</script>

<template>
  <div style="position: relative">
    <img
      :src="src"
      ref="img"
      @load="onImageLoad"
      :style="{ outlineWidth: borderSize + 'px' }"
      style="width: 100%; outline-style: dotted; outline-color: red"
    />
    <canvas ref="visibleCanvas" style="width: 100%; position: absolute; left: 0; top: 0"></canvas>
    <canvas
      ref="pickingCanvas"
      style="opacity: 0; width: 100%; position: absolute; left: 0; top: 0"
      @mouseenter="mouseEnter"
      @mousemove="mouseMove"
      @mouseleave="mouseLeave"
    ></canvas>
    <ul
      ref="labelContainer"
      style="
        position: absolute;
        z-index: 10;
        padding: 0.4rem;
        white-space: pre;
        font-size: small;
        border-radius: 0.2rem;
        border-color: rgba(127, 127, 127, 0.75);
        border-style: solid;
        border-width: thin;
        background-color: #efefef;
        list-style-type: none;
      "
    ></ul>
    <q-inner-loading :showing="showSpinner" />
  </div>
</template>
