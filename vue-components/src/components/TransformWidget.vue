<script setup lang="ts">
import { computed, ref } from 'vue'
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

const props = defineProps<Props>()
const emit = defineEmits<Events>()

const stringOptions = Object.keys(props.descriptions)
const options = ref(stringOptions)

function filterFn(val: string, update: (arg0: () => void) => void, abort: any) {
  update(() => {
    const needle = val.toLowerCase()
    options.value = stringOptions.filter((option) => {
      return option.toLowerCase().indexOf(needle) > -1
    })
  })
}
</script>

<template>
  <div>
    <q-select
      filled
      options-dense
      stack-label
      map-options
      :model-value="value.name"
      :options="options"
      @filter="filterFn"
      use-input
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
