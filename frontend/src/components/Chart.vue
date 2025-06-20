<template>
  <div>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import ChartJS from 'chart.js/auto'

const props = defineProps<{
  options: { id: number, option_text: string, vote_count: number }[]
}>()

const canvas = ref<HTMLCanvasElement | null>(null)
let chart: ChartJS | null = null

const renderChart = () => {
  if (!canvas.value) return
  if (chart) chart.destroy()
  chart = new ChartJS(canvas.value, {
    type: 'bar',
    data: {
      labels: props.options.map(o => o.option_text),
      datasets: [{
        label: '票数',
        data: props.options.map(o => o.vote_count),
        backgroundColor: [
          '#fda085', '#f6d365', '#a1c4fd', '#c2e9fb', '#fdcbf1'
        ]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true, ticks: { stepSize: 1 } }
      }
    }
  })
}

onMounted(renderChart)
watch(() => props.options, renderChart, { deep: true })
</script> 