<template>
  <div class="page-wrapper">
    <nav class="navbar">
      <div class="logo">🧬 PhyMaBiCh</div>
      <!-- <ul class="nav-links">
        <li><a href="#">About</a></li>
        <li><a href="#">Features</a></li>
        <li><a href="#">Test</a></li>
        <li><a href="#">Docs</a></li>
      </ul> -->
      <div class="nav-right">
        <!-- <button class="toggle-theme">☀️ / 🌙</button> -->
        <div class="profile-circle">R</div>
      </div>
    </nav>

    <div class="chat-ui">
      <div class="chat-container">
        <div class="chat-box" ref="chatWindow">
          <div
            v-for="(msg, index) in messages"
            :key="index"
            class="chat-message"
          >
            <div :class="msg.role === 'user' ? 'user-msg' : 'assistant-msg'">
              <div
                :class="msg.role === 'user'
                  ? 'bubble user-bubble'
                  : 'bubble assistant-bubble'"
              >
                <strong class="role-label">{{ msg.role }}</strong>
                {{ msg.content }}
              </div>
            </div>
          </div>
        </div>

        <div class="input-area">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            placeholder="What's on your mind?..."
            class="chat-input"
          />
          <button @click="sendMessage" class="send-button">Talk</button>
        </div>
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
          content: "\n⚠️ Sorry, there was an error getting a response. Try again later!",
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
  height: 100vh;
  overflow: hidden;
  /* height: 100%; */
}
/* max-height: 90vh; */

.chat-ui {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.chat-container {
  width: 50%;
  display: flex;
  flex-direction: column;
  border: solid 1px rgb(255, 199, 95);
  overflow: auto;
  border-radius: 1rem;
}

.chat-box {
  background-color: #1f2937;
  border-bottom: none;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
  padding: 1.5rem;
  height: auto;
  min-height: 7em;
  max-block-size: 100%;
  overflow-y: auto;
  width: auto;
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
  border-radius: 19px;
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
  background: none;
  color: white;
  font-family: Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
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
  box-shadow: 8px #000000, 4px #000000;
  border-bottom-right-radius: -100px;
}

.chat-input {
  flex: 1;
  padding: 0.75rem 1rem;
  background-color: #1f2937;
  border-bottom-left-radius: 19px;
  border: none;
  font-size: medium;
  padding: 1em;
  color: white;
  outline: none;
  flex-shrink: 0;
}

.chat-input::placeholder {
  color: #a2a4a7;
}

.send-button {
  background-color: #1f2937;
  padding: 0.75rem;
  border-bottom-right-radius: 1rem;
  font-weight: bold;
  font-size: 0.875rem;
  margin: 0;
  color: rgb(255, 199, 95);
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

/* === NAVBAR STYLING === */
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow: hidden;
}

.navbar {
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  /* box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3); */
  position: sticky;
  top: 0;
  z-index: 1000;
}

.logo {
  font-size: 1.2rem;
  font-weight: bold;
  color: rgb(255, 199, 95);
  font-family: 'Courier New', Courier, monospace;
  letter-spacing: 1px;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 1.5rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
  position: relative;
  padding: 0.25rem;
  transition: color 0.3s ease;
}

.nav-links a::after {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0%;
  height: 2px;
  background-color: rgb(255, 199, 95);
  transition: width 0.3s ease;
}

.nav-links a:hover {
  color: rgb(255, 199, 95);
}

.nav-links a:hover::after {
  width: 100%;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.toggle-theme {
  background: transparent;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  color: white;
}

.profile-circle {
  background-color: rgb(255, 199, 95);
  color: #111827;
  border-radius: 50%;
  width: 2rem;
  height: 2rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: monospace;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.profile-circle:hover {
  transform: scale(1.1);
}

</style>
