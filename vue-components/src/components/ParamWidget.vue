<script setup lang="ts">
import type { ParameterValue, ParameterDescription } from '../types'

interface Props {
  name: string
  modelValue: ParameterValue
  description: ParameterDescription
}

type Events = {
  'update:modelValue': [value: ParameterValue]
}

const props = defineProps<Props>()

const emit = defineEmits<Events>()

function onValueChange(newValue: any) {
  if (props.description.type == 'float') {
    newValue = parseFloat(newValue)
    if (Number.isNaN(newValue)) {
      return
    }
  } else if (props.description.type == 'integer') {
    newValue = parseInt(newValue)
    if (Number.isNaN(newValue)) {
      return
    }
  }

  emit('update:modelValue', newValue)
}
</script>

<template>
  <div>
    <q-select
      v-if="description.options"
      outlined
      dense
      options-dense
      stack-label
      map-options
      :model-value="modelValue"
      :label="description.label"
      :options="description.options"
      @update:model-value="onValueChange"
    />
    <q-checkbox
      v-else-if="description.type === 'boolean'"
      outlined
      dense
      :model-value="modelValue"
      :label="description.label"
      @update:model-value="onValueChange"
    />
    <q-input
      v-else
      outlined
      dense
      stack-label
      :model-value="modelValue"
      :label="description.label"
      :type="description.type === 'string' ? 'text' : 'number'"
      @update:model-value="onValueChange"
    />
  </div>
</template>
