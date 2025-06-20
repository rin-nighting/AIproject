import { mount } from '@vue/test-utils'
import Poll from '../src/components/Poll.vue'
import { describe, it, expect, vi } from 'vitest'
import axios from 'axios'
import flushPromises from 'flush-promises'

vi.mock('axios')

describe('Poll.vue', () => {
  it('renders question and options after fetching', async () => {
    const pollData = {
      id: 1,
      question: 'What is your favorite color?',
      options: [
        { id: 1, option_text: 'Red', vote_count: 0 },
        { id: 2, option_text: 'Green', vote_count: 0 },
        { id: 3, option_text: 'Blue', vote_count: 0 }
      ]
    }
    
    ;(axios.get as any).mockResolvedValue({ data: pollData })

    const wrapper = mount(Poll)

    await flushPromises()
    await wrapper.vm.$nextTick()


    expect(wrapper.html()).toContain('What is your favorite color?')
    expect(wrapper.html()).toContain('Red')
    expect(wrapper.html()).toContain('Green')
    expect(wrapper.html()).toContain('Blue')
  })
}) 