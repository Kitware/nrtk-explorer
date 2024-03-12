<script setup lang="ts">
interface Props {
  operator: 'and' | 'or'
  invert: boolean
}

type Events = {
  'update:operator': [value: 'and' | 'or']
  'update:invert': [value: boolean]
}

const props = defineProps<Props>()

const emit = defineEmits<Events>()

function onOperatorChange(value: any) {
  emit('update:operator', value)
}

function onNotClick() {
  emit('update:invert', !props.invert)
}
</script>

<template>
  <div style="display: flex" class="q-mb-md">
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
</template>
