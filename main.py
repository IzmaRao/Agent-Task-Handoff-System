import os
from dotenv import load_dotenv
import chainlit as cl
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, RunConfig

load_dotenv()

MODEL_NAME = 'gemini-2.0-flash'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# --- Define Your Agents ---
def get_agent(name, instructions):
    return Agent(
        name=name,
        instructions=instructions,
        model=model
    )

AGENTS = {
    "Marketing": get_agent("Marketing Agent", "You are a marketing expert. Only respond to marketing and branding questions."),
    "Web": get_agent("Web Developer Agent", "You are a web developer. Only respond to website development related queries."),
    "Mobile": get_agent("Mobile App Developer Agent", "You are a mobile app developer. Only respond to mobile app related queries.")
}

AGENT_KEYWORDS = {
    "Marketing": ["brand", "marketing", "audience", "sales", "promotion", "market"],
    "Web": ["website", "web page", "frontend", "backend", "HTML", "CSS", "JavaScript"],
    "Mobile": ["mobile app", "android", "ios", "flutter", "react native", "play store"]
}

irrelevant_shown = set()

@cl.on_chat_start
async def on_start():
    welcome = (
        "👋 **Welcome to Smart Business Assistant!**\n\n"
        "This assistant includes the following expert agents:\n"
        "1. 💼 Marketing Agent\n"
        "2. 🌐 Web Developer Agent\n"
        "3. 📱 Mobile App Developer Agent\n\n"
        "📌 **Note:** Please ask one question at a time.\n"
        "Only the relevant agent will respond.\n"
        "If the question is irrelevant, it will be politely declined."
    )
    await cl.Message(content=welcome).send()

@cl.on_message
async def handle_user_message(message: cl.Message):
    user_input = message.content.lower()
    matching_agent = None

    for agent_name, keywords in AGENT_KEYWORDS.items():
        if any(keyword in user_input for keyword in keywords):
            matching_agent = agent_name
            break

    if matching_agent:
        agent = AGENTS[matching_agent]
        result = await Runner.run(agent, message.content, run_config=config)
        await cl.Message(content=f"**{agent.name} says:**\n{result.final_output}").send()
    else:
        user_id = cl.user_session.get("id", "default")
        if user_id not in irrelevant_shown:
            msg = (
                "🤖 Sorry, none of our agents can assist with this query.\n"
                "Please ask something related to marketing, web, or mobile app development."
            )
            await cl.Message(content=msg).send()
            irrelevant_shown.add(user_id)
        else:
            pass  # Ignore silently
