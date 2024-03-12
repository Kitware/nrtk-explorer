<script setup lang="ts">
import { computed } from 'vue'

import type { Category } from '../types'

interface Props {
  options: { [key: number]: Category }
  modelValue: number[]
}

type Events = {
  'update:modelValue': [value: number[]]
}

const props = defineProps<Props>()

const emit = defineEmits<Events>()

const modelValueSet = computed(() => {
  return new Set(props.modelValue)
})

function onChipClick(value: Category) {
  const newModelValueSet = new Set(modelValueSet.value)
  if (newModelValueSet.has(value.id)) {
    newModelValueSet.delete(value.id)
  } else {
    newModelValueSet.add(value.id)
  }

  const newValue = Object.values(props.options)
    .filter((cat) => newModelValueSet.has(cat.id))
    .map((cat) => cat.id)

  emit('update:modelValue', newValue)
}
</script>

<template>
  <q-chip
    v-for="option in options"
    :key="option.id"
    :color="modelValueSet.has(option.id) ? 'primary' : ''"
    :text-color="modelValueSet.has(option.id) ? 'white' : ''"
    clickable
    @click="() => onChipClick(option)"
    size="sm"
    >{{ option.name }}</q-chip
  >
</template>
