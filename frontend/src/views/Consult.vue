<template>
  <div class="consult">
    <header class="header">
      <button class="back-btn" @click="goHome">← 返回</button>
      <h1>未来 · 咨询</h1>
      <button class="reset-btn" @click="resetChat">清空</button>
    </header>

    <div class="chat-area" ref="chatArea">
      <div v-if="messages.length === 0" class="empty-state">
        <p>张老师：我跟你说，有问题你就问，别客气。</p>
        <p>你可以告诉我：孩子分数、省份、想学什么专业...</p>
      </div>

      <div v-for="(msg, index) in messages" :key="index" class="message">
        <div :class="['bubble', msg.role]">
          <span class="role-label">{{ msg.role === 'user' ? '你' : '张老师' }}</span>
          <div class="content">{{ msg.content }}</div>
        </div>
      </div>

      <div v-if="isLoading" class="message">
        <div class="bubble assistant loading">
          <span class="role-label">张老师</span>
          <div class="content">
            <span class="typing">思考中...</span>
          </div>
        </div>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="inputText"
        type="text"
        placeholder="输入你的问题..."
        :disabled="isLoading"
        @keyup.enter="sendMessage"
      />
      <button :disabled="isLoading || !inputText.trim()" @click="sendMessage">
        发送
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const messages = ref([])
const inputText = ref('')
const isLoading = ref(false)
const chatArea = ref(null)
const error = ref(null)

const API_BASE = '/api'

const goHome = () => {
  router.push('/')
}

const resetChat = () => {
  messages.value = []
  inputText.value = ''
  error.value = null
}

const sendMessage = async () => {
  if (!inputText.value.trim() || isLoading.value) return

  const userMessage = inputText.value.trim()
  inputText.value = ''
  error.value = null

  messages.value.push({
    role: 'user',
    content: userMessage
  })

  await nextTick()
  scrollToBottom()

  isLoading.value = true

  let assistantMessage = {
    role: 'assistant',
    content: ''
  }
  messages.value.push(assistantMessage)

  try {
    const history = messages.value.slice(0, -2).map(m => [m.role, m.content])

    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: userMessage,
        history: history
      })
    })

    if (!response.ok) {
      const text = await response.text()
      throw new Error(`API请求失败: ${response.status} - ${text}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value, { stream: true })
      const lines = chunk.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            if (data.error) {
              throw new Error(data.error)
            }
            if (data.content) {
              assistantMessage.content += data.content
              await nextTick()
              scrollToBottom()
            }
            if (data.done) {
              break
            }
          } catch (e) {
            if (e.message !== 'JSON.parse error') {
              throw e
            }
          }
        }
      }
    }
  } catch (err) {
    console.error('Chat error:', err)
    error.value = err.message || '抱歉，出了点问题，请稍后再试。'
    assistantMessage.content = ''
  } finally {
    isLoading.value = false
  }
}

const scrollToBottom = () => {
  if (chatArea.value) {
    chatArea.value.scrollTop = chatArea.value.scrollHeight
  }
}

onMounted(() => {
  const q = route.query.q
  if (q) {
    inputText.value = q
  }
})
</script>

<style scoped>
.consult {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header h1 {
  font-size: 18px;
  margin: 0;
}

.back-btn, .reset-btn {
  background: rgba(255,255,255,0.2);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

.back-btn:hover, .reset-btn:hover {
  background: rgba(255,255,255,0.3);
}

.chat-area {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-state {
  text-align: center;
  color: #666;
  padding: 60px 20px;
  font-size: 15px;
  line-height: 1.8;
}

.empty-state p:first-child {
  font-size: 18px;
  color: #333;
  margin-bottom: 16px;
}

.message {
  display: flex;
  flex-direction: column;
}

.bubble {
  max-width: 80%;
  padding: 14px 18px;
  border-radius: 16px;
  line-height: 1.6;
}

.bubble.user {
  background: #667eea;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.bubble.assistant {
  background: white;
  color: #333;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.role-label {
  font-size: 12px;
  opacity: 0.6;
  display: block;
  margin-bottom: 4px;
}

.content {
  white-space: pre-wrap;
  word-break: break-word;
}

.typing {
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

.error-message {
  background: #fee;
  color: #c00;
  padding: 12px 16px;
  border-radius: 8px;
  text-align: center;
  margin: 8px 0;
}

.input-area {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  background: white;
  border-top: 1px solid #eee;
}

.input-area input {
  flex: 1;
  padding: 14px 18px;
  border: 1px solid #ddd;
  border-radius: 24px;
  font-size: 15px;
  outline: none;
  transition: border-color 0.2s;
}

.input-area input:focus {
  border-color: #667eea;
}

.input-area button {
  background: #667eea;
  color: white;
  border: none;
  padding: 12px 28px;
  border-radius: 24px;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.2s;
}

.input-area button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.input-area button:not(:disabled):hover {
  background: #5568d3;
}
</style>
