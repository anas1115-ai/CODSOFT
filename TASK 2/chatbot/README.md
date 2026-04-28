# Nova — Rule-Based Chatbot 🤖

A simple chatbot built with vanilla HTML, CSS, and JavaScript. It uses **pattern matching** and **if-else style rule definitions** to understand user input and respond accordingly.

---

## 🚀 Features

- Pattern-based natural language processing (no external libraries)
- Randomized responses so conversations feel natural
- Dynamic responses (live time & date)
- Typing animation for a realistic chat feel
- Clean, responsive UI

---

## 💬 What Can Nova Do?

| Topic         | Example Input                  |
|---------------|-------------------------------|
| Greeting      | "hi", "hello", "hey"          |
| Time & Date   | "what time is it?"            |
| Jokes         | "tell me a joke"              |
| Fun Facts     | "give me a fun fact"          |
| Help          | "what can you do?"            |
| Farewell      | "bye", "goodbye"              |
| Compliments   | "you're awesome"              |

---

## 📁 Project Structure

```
chatbot/
├── index.html     # Main UI structure
├── style.css      # Styling & animations
├── chatbot.js     # Bot logic & pattern matching
└── README.md      # Project info
```

---

## 🛠️ How It Works

### Pattern Matching

Each rule has a list of **keywords** and a list of **possible responses**:

```js
{
  patterns: ["hello", "hi", "hey"],
  responses: [
    "Hey! How's it going? 😊",
    "Hi there! What can I help you with?",
  ]
}
```

When the user types a message, the bot:
1. Converts the input to lowercase and strips punctuation
2. Checks if the input **includes** any known pattern
3. Picks a **random response** from the matching rule
4. Falls back to a default message if nothing matches

### Dynamic Responses

Some responses are functions that generate output at call time:

```js
() => `Right now it's ${new Date().toLocaleTimeString()} ⏰`
```

---

## ▶️ How to Run

No setup needed. Just open `index.html` in any modern browser:

```bash
# Option 1 - double click index.html
# Option 2 - use VS Code Live Server extension
# Option 3 - run a quick local server
python -m http.server 3000
```

---

## 🧠 Concepts Covered

- Natural Language Processing basics (tokenization, pattern matching)
- Conversation flow design
- DOM manipulation with JavaScript
- CSS animations and responsive layout

---

## 📌 Future Improvements

- [ ] Connect to a weather API for live forecasts
- [ ] Add a memory system (remember user's name)
- [ ] Support multi-turn conversations
- [ ] Add text-to-speech output

---

## 👤 Author

Made for learning purposes as part of an NLP basics project.
