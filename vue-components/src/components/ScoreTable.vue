<script setup lang="ts">
import { computed, unref, type MaybeRef } from 'vue'

interface Props {
  scores: { [modelId: string]: MaybeRef<number> }
  models: { [modelId: string]: { name: string } }
}

const props = defineProps<Props>()

const tableData = computed(() => {
  return Object.entries(props.models).reduce(
    (acc, [modelId, modelObj]) => {
      const score = props.scores[modelId]

      if (score != undefined) {
        acc.push({ model: modelObj.name, score: unref(score) })
      }

      return acc
    },
    [] as { model: string; score: number }[]
  )
})
</script>

<template>
  <table>
    <tbody>
      <tr style="font-weight: bold">
        <td>Model</td>
        <td>Score</td>
      </tr>
      <tr v-for="row in tableData" :key="row.model">
        <td>{{ row.model }}</td>
        <td>{{ row.score.toFixed(2) }}</td>
      </tr>
    </tbody>
  </table>
</template>
