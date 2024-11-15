<script setup lang="ts">
import type { ParameterValue, TransformDescription, TransformValue } from '../types'

import ParamsWidget from './ParamsWidget.vue'

interface Props {
  pos: number
  value: TransformValue
  descriptions: { [name: string]: TransformDescription }
}

type Events = {
  'update:type': [type: string]
  'update:params': [params: { [name: string]: ParameterValue }]
  remove: []
}

defineProps<Props>()
const emit = defineEmits<Events>()
</script>

<template>
  <div>
    <q-select
      filled
      options-dense
      stack-label
      map-options
      :model-value="value.name"
      :options="Object.keys(descriptions)"
      @update:model-value="(t: string) => emit('update:type', t)"
    >
      <template v-slot:prepend>
        <q-chip>{{ pos }}</q-chip>
      </template>

      <template v-slot:append>
        <q-icon name="delete" @click.stop.prevent="() => emit('remove')" class="cursor-pointer" />
      </template>
    </q-select>

    <div
      v-if="descriptions[value.name] && Object.keys(descriptions[value.name]).length > 0"
      class="q-ml-md q-mr-md q-mt-lg"
    >
      <ParamsWidget
        :values="value.parameters"
        :descriptions="descriptions[value.name]"
        @valuesChanged="(params) => emit('update:params', params)"
      />
    </div>

    <q-separator class="q-mt-md q-mb-md" />
  </div>
</template>
