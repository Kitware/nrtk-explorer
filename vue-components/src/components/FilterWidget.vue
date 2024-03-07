<script setup lang="ts">
import { computed } from 'vue'

import type { Category } from '../types'

interface Props {
  label: string
  options: { [key: number]: Category }
  modelValue: number[]
  operator: 'and' | 'or'
  invert: boolean
}

type Events = {
  'update:modelValue': [value: number[]]
  'update:operator': [value: 'and' | 'or']
  'update:invert': [value: boolean]
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

function onOperatorChange(value: any) {
  console.log(value)
  emit('update:operator', value)
}

function onNotClick() {
  emit('update:invert', !props.invert)
}
</script>

<template>
  <div>
    <div style="display: flex" class="q-mb-md">
      <span class="text-h6">{{ label }}</span>
      <q-space />
      <q-btn @click="onNotClick" :color="invert ? 'grey' : undefined" size="sm" class="q-mr-sm">
        !
      </q-btn>
      <q-btn-toggle
        size="sm"
        :options="[
          { label: '&&', value: 'and' },
          { label: '||', value: 'or' }
        ]"
        :model-value="operator"
        @update:model-value="onOperatorChange"
        toggle-color="grey"
      />
    </div>
    <div class="q-mb-sm">
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
    </div>
  </div>
</template>
