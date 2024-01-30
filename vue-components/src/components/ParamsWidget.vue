<script setup lang="ts">
import { toRefs } from 'vue'

import type { Ref } from 'vue'

import type { ParameterValue, ParameterDescription } from '../types'

import ParamWidget from './ParamWidget.vue'

interface Props {
  values: Ref<{ [name: string]: ParameterValue }>
  descriptions: Ref<{ [name: string]: ParameterDescription }>
}

const props = defineProps<Props>()
const emit = defineEmits(['valuesChanged'])

const { values, descriptions } = toRefs(props)

function onParamValueChange(name: string, newValue: ParameterValue) {
  const newValues = {
    ...values.value,
    [name]: newValue
  }

  emit('valuesChanged', newValues)
}
</script>

<template>
  <div class="q-gutter-md">
    <ParamWidget
      v-for="(value, name) in values"
      :key="name"
      :name="name as any"
      :model-value="value as any"
      :description="descriptions[name] as any"
      @update:model-value="(newValue) => onParamValueChange(name as any, newValue)"
    >
    </ParamWidget>
  </div>
</template>
