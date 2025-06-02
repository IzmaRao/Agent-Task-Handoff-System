# 🤖 Multi-Agent Chainlit Assistant

This project demonstrates a multi-agent system powered by [Chainlit](https://www.chainlit.io/) where a **Manager Agent** assigns tasks to three specialized agents:

- 🎯 **Marketing Agent** – Crafts creative and benefit-driven content.
- 📱 **Mobile App Developer Agent** – Suggests mobile app ideas or features.
- 💻 **Web Developer Agent** – Gives web implementation ideas or approaches.

Each agent is powered by Google Gemini (`gemini-2.0-flash`) using the LangGraph `agents` framework.

## 🛠 Features

- ✅ Chainlit-powered conversational UI
- 🤝 Multi-agent task delegation
- 🔐 Uses `.env` for API key (Google Gemini)
- 📦 Simple, extendable structure


## 💡 How it Works
- The manager agent delegates the same task (user input) to all three agents and collects their unique responses. It's a modular structure that can be extended with more roles or smarter routing logic.