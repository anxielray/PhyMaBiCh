<template>
  <div class="chat-ui">
    <div class="chat-container">
      <div class="chat-box" ref="chatWindow">
        <div v-for="(msg, index) in messages" :key="index" class="chat-message">
          <div :class="msg.role === 'user' ? 'user-msg' : 'assistant-msg'">
            <div :class="msg.role === 'user' ? 'bubble user-bubble' : 'bubble assistant-bubble'">
              <strong class="role-label">{{ msg.role }}</strong>
              {{ msg.content }}
            </div>
          </div>
        </div>
      </div>

      <div class="input-area">
        <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Type your message..." class="chat-input" />
        <button @click="sendMessage" class="send-button">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInput: "",
      messages: [],
    };
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim()) return;

      const userMessage = { role: "user", content: this.userInput.trim() };
      this.messages.push(userMessage);
      this.userInput = "";

      try {
        const res = await fetch("http://localhost:27277/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ messages: this.messages }),
        });

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let botResponse = "";
        let done = false;

        while (!done) {
          const { value, done: streamDone } = await reader.read();
          done = streamDone;

          buffer += decoder.decode(value, { stream: !done });

          let lines = buffer.split("\n");
          buffer = lines.pop(); // Save incomplete line for next read

          for (const line of lines) {
            if (!line.trim()) continue;
            try {
              const json = JSON.parse(line);
              const chunk = json.message?.content || "";

              botResponse += chunk;

              // Update assistant message dynamically
              if (
                this.messages.length > 0 &&
                this.messages[this.messages.length - 1].role === "assistant"
              ) {
                this.messages[this.messages.length - 1].content = botResponse;
              } else {
                this.messages.push({ role: "assistant", content: botResponse });
              }

              this.$nextTick(() => {
                const chatWindow = this.$refs.chatWindow;
                chatWindow.scrollTop = chatWindow.scrollHeight;
              });
            } catch (err) {
              console.error("Could not parse line", line, err);
            }
          }
        }

      } catch (error) {
        this.messages.push({
          role: "assistant",
          content: "⚠️ Sorry, there was an error getting a response.",
        });
      }
    },
  },
};
</script>

<style>
/* Nastia-style UI */
body,
html {
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
  background: linear-gradient(to bottom right, #111827, #1f2937);
  color: white;
  height: 100%;
}

.chat-ui {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.chat-container {
  width: 100%;
  max-width: 700px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chat-box {
  background-color: #1f2937;
  border-radius: 1rem;
  padding: 1.5rem;
  height: 600px;
  overflow-y: auto;
  scroll-behavior: smooth;
}

.chat-message {
  margin-bottom: 1rem;
}

.user-msg {
  text-align: right;
}

.assistant-msg {
  text-align: left;
}

.bubble {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  max-width: 80%;
  word-break: break-word;
  white-space: pre-wrap;
}

.user-bubble {
  background-color: #0284c7;
  color: white;
}

.assistant-bubble {
  background-color: #374151;
  color: white;
}

.role-label {
  display: block;
  margin-bottom: 0.25rem;
  font-size: 0.75rem;
  text-transform: uppercase;
  opacity: 0.5;
}

/* Input Section */
.input-area {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chat-input {
  flex: 1;
  padding: 0.75rem 1rem;
  background-color: #374151;
  border: none;
  border-radius: 9999px;
  font-size: medium;
  color: white;
  outline: none;
}

.chat-input::placeholder {
  color: #a2a4a7;
}

.send-button {
  background-color: #0284c7;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 9999px;
  font-weight: bold;
  font-size: 0.875rem;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.send-button:hover {
  background-color: #0369a1;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 3px;
}
</style>
