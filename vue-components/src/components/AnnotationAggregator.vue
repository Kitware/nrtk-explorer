<script setup lang="ts">
import { ref, inject, watch, onBeforeMount, onBeforeUnmount } from 'vue'

interface Props {
  imageId: string
  transformed: boolean
  models: { [modelId: string]: any }
}

const props = defineProps<Props>()

const trame: any = inject('trame')

const aggregateAnnotations = ref({})

function updateAnnotations() {
  if (props.imageId == undefined || props.models == undefined) {
    aggregateAnnotations.value = {}
    return
  }

  const agg = Object.entries(props.models).reduce(function (acc, [model_id, model]) {
    const originalId = `img_${props.imageId}`
    const transformedId = `transformed_img_${props.imageId}`

    let imageId: string = props.transformed ? transformedId : originalId

    if (model.name == 'groundtruth') {
      acc[model_id] = trame.state.get(`result_${originalId}_${model.name}`)
    } else {
      acc[model_id] = trame.state.get(`result_${imageId}_${model.name}`)
    }

    return acc
  }, {} as any)

  aggregateAnnotations.value = agg
}

watch(() => [props.imageId, props.transformed, props.models], updateAnnotations)

onBeforeMount(() => {
  trame.state.addListener(updateAnnotations)
  updateAnnotations()
})

onBeforeUnmount(() => {
  trame.state.removeListener(updateAnnotations)
})
</script>

<template>
  <slot :aggregateAnnotations></slot>
</template>
