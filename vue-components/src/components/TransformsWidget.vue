<script setup lang="ts">
import type { TransformDescription, TransformValue } from '../types'

import TransformWidget from './TransformWidget.vue'

interface Props {
  values: TransformValue[]
  descriptions: { [name: string]: TransformDescription }
}

type Events = {
  addTransform: []
  removeTransform: [id: number]
  typeChanged: [{ id: number; type: string }]
  paramsChanged: [{ id: number; params: any }]
}

defineProps<Props>()
const emit = defineEmits<Events>()
</script>

<template>
  <TransformWidget
    v-for="(value, i) in values"
    :key="i"
    :pos="i"
    :value="value"
    :descriptions="descriptions"
    @remove="() => emit('removeTransform', i)"
    @update:type="(t: string) => emit('typeChanged', { id: i, type: t })"
    @update:params="(params: any) => emit('paramsChanged', { id: i, params })"
  />
  <q-btn @click="() => emit('addTransform')" class="full-width" flat>Add Transform</q-btn>
</template>
