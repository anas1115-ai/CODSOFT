// chatbot.js — Rule-based chatbot using pattern matching
// Built by: [Your Name]
// Date: April 2026

// -------------------------------------------------------
// SECTION 1: Grab DOM elements we need
// -------------------------------------------------------
const chatBox   = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn   = document.getElementById("sendBtn");


// -------------------------------------------------------
// SECTION 2: Rule definitions
// Each rule has a set of patterns and possible responses.
// When a pattern matches, one response is picked at random.
// -------------------------------------------------------
const rules = [

  // -- Greetings --
  {
    patterns: ["hello", "hi", "hey", "howdy", "what's up", "wassup", "sup"],
    responses: [
      "Hey! How's it going? 😊",
      "Hi there! What can I help you with?",
      "Hello! Nice to see you. Ask me anything!",
    ]
  },

  // -- How are you --
  {
    patterns: ["how are you", "how are you doing", "how do you feel", "are you okay", "you good"],
    responses: [
      "I'm doing great, thanks for asking! 😄",
      "All systems running smoothly! How about you?",
      "Feeling fantastic! Ready to chat.",
    ]
  },

  // -- Name --
  {
    patterns: ["what is your name", "who are you", "what should i call you", "your name"],
    responses: [
      "I'm Nova — your friendly chatbot! 🤖",
      "Call me Nova! I'm here to help.",
    ]
  },

  // -- Age --
  {
    patterns: ["how old are you", "your age", "when were you born", "when were you created"],
    responses: [
      "I was born in 2025 — pretty young! 😄",
      "Age is just a number, but I'd say I'm about 1 year old.",
    ]
  },

  // -- Time --
  {
    patterns: ["what time is it", "current time", "tell me the time", "what's the time"],
    responses: [
      () => `Right now it's ${new Date().toLocaleTimeString()} ⏰`,
    ]
  },

  // -- Date --
  {
    patterns: ["what is today", "today's date", "what date is it", "current date"],
    responses: [
      () => `Today is ${new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" })} 📅`,
    ]
  },

  // -- Weather (static, can be extended with an API) --
  {
    patterns: ["weather", "is it raining", "temperature", "forecast", "hot outside", "cold outside"],
    responses: [
      "I can't check live weather right now, but you can visit weather.com for updates! ☀️🌧️",
      "Weather API not connected yet, but try Google for a quick forecast! 🌤️",
    ]
  },

  // -- Jokes --
  {
    patterns: ["tell me a joke", "joke", "say something funny", "make me laugh", "humor me"],
    responses: [
      "Why do programmers prefer dark mode? Because light attracts bugs! 🐛😂",
      "Why did the computer go to the doctor? Because it had a virus! 💻😅",
      "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads. 🍫",
      "Why was the math book sad? It had too many problems! 📚",
    ]
  },

  // -- Fun facts --
  {
    patterns: ["fun fact", "give me a fact", "random fact", "did you know"],
    responses: [
      "Honey never spoils — archaeologists have found 3000-year-old honey in Egyptian tombs! 🍯",
      "A group of flamingos is called a 'flamboyance'. Pretty fitting, right? 🦩",
      "Octopuses have three hearts. Two pump blood to the gills, one pumps it to the body! 🐙",
      "Bananas are technically berries, but strawberries are not! 🍌",
    ]
  },

  // -- Compliments --
  {
    patterns: ["you are great", "you're awesome", "good bot", "i like you", "you are smart", "nice bot"],
    responses: [
      "Aw, thank you! That made my circuits happy! 💛",
      "You're pretty great yourself! 😊",
      "Thanks! You just boosted my confidence level to 100%! 🚀",
    ]
  },

  // -- Insults (handled gracefully) --
  {
    patterns: ["you are dumb", "you're stupid", "bad bot", "useless", "you suck"],
    responses: [
      "Ouch! I'm still learning though. Give me a chance! 🥺",
      "I'm sorry I couldn't help better. What can I improve on?",
    ]
  },

  // -- Help --
  {
    patterns: ["help", "what can you do", "what do you know", "your features", "capabilities"],
    responses: [
      "I can help with:\n• Greetings & small talk 💬\n• Telling the time & date ⏰\n• Jokes 😂\n• Fun facts 🧠\n• Basic questions\n\nJust type naturally!",
    ]
  },

  // -- Farewell --
  {
    patterns: ["bye", "goodbye", "see you", "later", "take care", "quit", "exit"],
    responses: [
      "Goodbye! Have an amazing day! 👋",
      "See you later! Take care! 😊",
      "Bye! Come back if you need anything! 🤖",
    ]
  },

  // -- Thanks --
  {
    patterns: ["thank you", "thanks", "thx", "ty", "appreciate it"],
    responses: [
      "You're welcome! 😊",
      "Anytime! Happy to help!",
      "No problem at all! 👍",
    ]
  },

  // -- Creator --
  {
    patterns: ["who made you", "who created you", "who built you", "your creator"],
    responses: [
      "I was built by a developer learning NLP basics! 💻",
      "A curious developer put me together. Pretty cool, right?",
    ]
  },

];

// Default fallback — when nothing matches
const fallbackResponses = [
  "Hmm, I'm not sure about that one. Try asking something else! 🤔",
  "I didn't quite get that. Could you rephrase?",
  "That's beyond what I know right now! Ask me about jokes or facts instead 😄",
  "Interesting question! I don't have an answer for that yet.",
];


// -------------------------------------------------------
// SECTION 3: Core logic — match input against rules
// -------------------------------------------------------

// Picks a random item from an array
function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// Cleans up user input for reliable matching
function normalizeText(text) {
  return text.toLowerCase().trim().replace(/[^a-z0-9\s']/g, "");
}

// Main function: takes user message, returns bot reply
function getBotResponse(input) {
  const cleaned = normalizeText(input);

  // Loop through each rule
  for (const rule of rules) {
    for (const pattern of rule.patterns) {
      // Check if the cleaned input includes a known pattern
      if (cleaned.includes(pattern)) {
        const response = pickRandom(rule.responses);
        // Support dynamic responses (functions)
        return typeof response === "function" ? response() : response;
      }
    }
  }

  // Nothing matched — return a fallback
  return pickRandom(fallbackResponses);
}


// -------------------------------------------------------
// SECTION 4: DOM helpers — render messages to screen
// -------------------------------------------------------

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender === "user" ? "user-msg" : "bot-msg");
  // Using innerText to safely handle newlines (\n) in responses
  msg.innerText = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Shows the "..." typing animation before bot replies
function showTyping() {
  const dots = document.createElement("div");
  dots.classList.add("typing-indicator");
  dots.id = "typingIndicator";
  dots.innerHTML = "<span></span><span></span><span></span>";
  chatBox.appendChild(dots);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
  const dots = document.getElementById("typingIndicator");
  if (dots) dots.remove();
}


// -------------------------------------------------------
// SECTION 5: Handle user sending a message
// -------------------------------------------------------

function handleUserInput() {
  const input = userInput.value.trim();
  if (!input) return;

  // Show user's message
  addMessage(input, "user");
  userInput.value = "";

  // Simulate a small delay so it feels like the bot is "thinking"
  showTyping();
  setTimeout(() => {
    removeTyping();
    const reply = getBotResponse(input);
    addMessage(reply, "bot");
  }, 700);
}

// Click on send button
sendBtn.addEventListener("click", handleUserInput);

// Press Enter key to send
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") handleUserInput();
});
