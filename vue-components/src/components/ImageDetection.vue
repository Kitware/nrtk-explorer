<script setup  lang="ts">
import { ref, unref, watch, onMounted, toRefs } from "vue";

import  type { Ref } from "vue";

import { Quadtree, Rectangle } from "@timohausmann/quadtree-ts";

import type { Annotation, ImageMetadata, Category, Vector3 } from "../types";

const CATEGORY_COLORS: Vector3<number>[] = [
  [255, 0, 0],
  [0, 255, 0],
  [0, 0, 255],
  [255, 255, 0],
  [255, 0, 255],
  [0, 255, 255],
];

interface Props {
  src: Ref<string>;
  meta: Ref<ImageMetadata>;
  annotations: Ref<Annotation[]>;
  categories: Ref<{[key: number]: Category}>;
}

let annotationsTree: Quadtree<Rectangle<number>> | undefined = undefined;

function drawAnnotations(canvas: HTMLCanvasElement | undefined, meta: ImageMetadata, annotations: Annotation[]) {
  if (!canvas) {
    return;
  }

  canvas.width = meta.width;
  canvas.height = meta.height;

  const ctx = canvas.getContext("2d");

  if (!ctx) {
    return;
  }

  const opacity = 0.5;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  annotations.forEach((annotation) => {
    const color = CATEGORY_COLORS[annotation.category_id % CATEGORY_COLORS.length];
    ctx.fillStyle = `rgba(${[...color, opacity].join(",")})`;

    ctx.fillRect(annotation.bbox[0], annotation.bbox[1], annotation.bbox[2], annotation.bbox[3]);
  });
}

function doRectanglesOverlap(recA: Rectangle<any>, recB: Rectangle<any>) {
  const noHOverlap : boolean = (
    (recB.x >= recA.x + recA.width) ||
    (recA.x >= recB.x + recB.width)
  );

  if (noHOverlap) {
    return false;
  }

  const noVOverlap : boolean = (
    (recB.y >= recA.y + recA.height) ||
    (recA.y >= recB.y + recB.height)
  );

  return !noVOverlap
}

function drawPickingAnnotations(canvas: HTMLCanvasElement | undefined, meta: ImageMetadata, annotations: Annotation[]) {
  annotationsTree = undefined;

  if (!canvas) {
    return;
  }

  canvas.width = meta.width;
  canvas.height = meta.height;

  const ctx = canvas.getContext("2d");

  if (!ctx) {
    return;
  }

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  annotationsTree = new Quadtree({width: canvas.width, height: canvas.height, maxLevels: 8, maxObjects: 10});

  annotations.forEach((annotation, i) => {
    const treeNode = new Rectangle<number>({
      x: annotation.bbox[0],
      y: annotation.bbox[1],
      width: annotation.bbox[2],
      height: annotation.bbox[3],
      data: i,
    });

    annotationsTree?.insert(treeNode);

    ctx.fillStyle = `rgb(255, 0, 0)`;

    ctx.fillRect(annotation.bbox[0], annotation.bbox[1], annotation.bbox[2], annotation.bbox[3]);
  });
}

const props = defineProps<Props>();

const canvas = ref<HTMLCanvasElement>();
const pickingCanvas = ref<HTMLCanvasElement>();
const labelContainer = ref<HTMLDivElement>();

const showLabelContainer = ref(false);

watch(props.categories, function(newValue, oldValue){
});

watch(props.meta, function(newValue, oldValue){
  drawAnnotations(canvas.value, unref(props.meta), unref(props.annotations));
  drawPickingAnnotations(pickingCanvas.value, unref(props.meta), unref(props.annotations));
});

watch(props.annotations, function(newValue, oldValue){
  drawAnnotations(canvas.value, unref(props.meta), unref(props.annotations));
  drawPickingAnnotations(pickingCanvas.value, unref(props.meta), unref(props.annotations));
});

onMounted(() => {
  drawAnnotations(canvas.value, unref(props.meta), unref(props.annotations));
  drawPickingAnnotations(pickingCanvas.value, unref(props.meta), unref(props.annotations));
});

function displayToPixel(x: number, y: number, canvas: HTMLCanvasElement) : [number, number] {
  const canvasBounds = canvas.getBoundingClientRect();
  
  const pixelX = canvas.width * (x - canvasBounds.left) / canvasBounds.width;
  const pixelY = canvas.height * (y - canvasBounds.top) / canvasBounds.height;

  return [pixelX, pixelY];
}

function mouseEnter(e: MouseEvent) {
}

function mouseMove(e: MouseEvent) {
  if (!canvas.value || !pickingCanvas.value || !labelContainer.value || !annotationsTree || !props.categories.value || !props.annotations.value) {
    return;
  }

  const [pixelX, pixelY] = displayToPixel(e.clientX, e.clientY, canvas.value);

  const ctx = pickingCanvas.value.getContext("2d");

  if (!ctx) {
    return;
  }

  const pixelValue = ctx.getImageData(pixelX, pixelY, 1, 1).data[0];

  const pickedSomething = pixelValue > 0;

  if (pickedSomething) {
    labelContainer.value.style.left = `${e.offsetX + 8}px`;
    labelContainer.value.style.top = `${e.offsetY + 8}px`;
    showLabelContainer.value = true;
  } else {
    showLabelContainer.value = false;
  }

  if (pickedSomething) {
    const pixelRectangle = new Rectangle<number>({x: pixelX, y: pixelY, width: 2, height: 2});

    const hits = annotationsTree.retrieve(pixelRectangle).filter((rect: any) => doRectanglesOverlap(rect, pixelRectangle));

    let list = document.createElement('ul');
    list.style.padding = "0";
    list.style.margin = "0";

    hits.forEach((hit) => {
      const item = document.createElement('li');
      if (hit.data != undefined) {
        const annotation = props.annotations.value[hit.data];
        const category = props.categories.value[annotation.category_id];
        item.textContent = `(${annotation.id}): ${category.name}`;
        const color = CATEGORY_COLORS[annotation.category_id % CATEGORY_COLORS.length];
        item.style.textShadow = `rgba(${color.join(",")},0.6) 1px 1px 3px`;
        list.appendChild(item);
      }
    });

    labelContainer.value.replaceChildren(list);
  }
}

function mouseLeave(e: MouseEvent) {
  showLabelContainer.value = false;
}


const { src } = toRefs(props);

</script>

<template>
  <div style="width: 100%; position:relative; white-space: pre; font-size: small;">
    <img :src="src" style="width: 100%; position: relative; left: 0; top: 0;"/>
    <canvas ref="canvas" width=100 height=100 style="width: 100%; position: absolute; left: 0; top: 0;"></canvas>
    <div v-show="showLabelContainer" ref="labelContainer"
      style="position: absolute; background-color: #efefef; z-index: 10;
              list-style-position: inside;
              padding: 0.4rem;
              border-radius: 0.2rem;
              border-color: rgba(127,127,127,0.75);
              border-style: solid;
              border-width: thin;"
    >
    </div>
    <canvas
      ref="pickingCanvas" width=100 height=100 style="opacity: 0; width: 100%; position: absolute; left: 0; top: 0;"
      @mouseenter="mouseEnter" @mousemove="mouseMove" @mouseleave="mouseLeave"
    ></canvas>
  </div>
</template>
