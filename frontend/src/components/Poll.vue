<template>
  <div>
    <h2 style="text-align:center; color:#333;">{{ poll?.question }}</h2>
    <form v-if="poll && !voted" @submit.prevent="submitVote">
      <div v-for="option in poll.options" :key="option.id" class="option-row">
        <input type="radio" :id="'opt'+option.id" :value="option.id" v-model="selected" required />
        <label :for="'opt'+option.id">{{ option.option_text }}</label>
      </div>
      <button class="vote-btn" type="submit">投票</button>
    </form>
    <div v-else-if="voted">
      <div class="thanks">感谢您的投票！</div>
      <div v-for="option in poll?.options || []" :key="option.id" class="option-row">
        <span>{{ option.option_text }}：{{ option.vote_count }}票</span>
      </div>
    </div>
    <Chart :options="poll?.options || []" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Chart from './Chart.vue'

interface Option {
  id: number
  option_text: string
  vote_count: number
}
interface Poll {
  id: number
  question: string
  options: Option[]
}

const poll = ref<Poll | null>(null)
const selected = ref<number | null>(null)
const voted = ref(false)

const fetchPoll = async () => {
  const res = await axios.get('/api/poll')
  poll.value = res.data
}

const submitVote = async () => {
  if (selected.value && poll.value) {
    await axios.post('/api/poll/vote', {
      poll_id: poll.value.id,
      option_id: selected.value
    })
    voted.value = true
  }
}

onMounted(() => {
  fetchPoll()
  // WebSocket 实时更新
  const ws = new WebSocket(`ws://${location.host}/ws/poll`)
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (poll.value && data.poll_id === poll.value.id) {
      poll.value.options = data.options
    }
  }
})
</script>

<style scoped>
.option-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 1.1em;
}
.option-row input[type="radio"] {
  accent-color: #fda085;
  margin-right: 8px;
}
.vote-btn {
  background: linear-gradient(90deg, #f6d365 0%, #fda085 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 32px;
  font-size: 1.1em;
  cursor: pointer;
  margin-top: 16px;
  transition: box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(253,160,133,0.15);
}
.vote-btn:hover {
  box-shadow: 0 4px 16px rgba(253,160,133,0.25);
}
.thanks {
  color: #fda085;
  font-weight: bold;
  text-align: center;
  margin: 24px 0;
  font-size: 1.2em;
}
</style> 