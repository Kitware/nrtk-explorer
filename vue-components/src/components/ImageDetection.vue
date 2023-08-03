<script setup  lang="ts">
import { ref, unref, watch, onMounted, toRefs } from "vue";

import  type { Ref } from "vue";

import type { Annotation, ImageMetadata, Vector4 } from "../types";

const CATEGORY_COLORS: Vector4<number>[] = [
  [255, 0, 0, 0.5],
  [0, 255, 0, 0.5],
  [0, 0, 255, 0.5],
  [255, 255, 0, 0.5],
  [255, 0, 255, 0.5],
  [0, 255, 255, 0.5],
];

interface Props {
  src: Ref<string>;
  meta: Ref<ImageMetadata>;
  annotations: Ref<Annotation[]>;
}

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

  annotations.forEach((annotation) => {
    const color = CATEGORY_COLORS[annotation.category_id % CATEGORY_COLORS.length];
    ctx.fillStyle = `rgba(${color.join(",")})`;

    ctx.fillRect(annotation.bbox[0], annotation.bbox[1], annotation.bbox[2], annotation.bbox[3]);
  });
}

const props = defineProps<Props>();

const canvas = ref<HTMLCanvasElement>();

watch(props.meta, function(newValue, oldValue){
  drawAnnotations(canvas.value, unref(props.meta), unref(props.annotations));
});

watch(props.annotations, function(newValue, oldValue){
  drawAnnotations(canvas.value, unref(props.meta), unref(props.annotations));
});

onMounted(() => {
  drawAnnotations(canvas.value, unref(props.meta), unref(props.annotations));
});

const { src } = toRefs(props);

</script>

<template>
  <div style="width: 100%; position:relative;">
    <img :src="src" style="width: 100%; position: relative; left: 0; top: 0;"/>
    <canvas ref="canvas" width=100 height=100 style="width: 100%; position: absolute; left: 0; top: 0;"></canvas>
  </div>
</template>
