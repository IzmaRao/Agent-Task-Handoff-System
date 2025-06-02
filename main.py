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

# --- Agent Definitions ---

def get_agent(name, instructions):
    return Agent(
        name=name,
        instructions=instructions,
        model=model
    )

async def delegate_task_to_all_agents(task_prompt: str):
    agents_info = [
        ("Marketing Agent", "You are a creative marketing expert. Explain things in a way that grabs customer attention and highlights product benefits."),
        ("Mobile App Developer Agent", "You are a mobile app developer. Think about how this concept can be applied or enhanced through a mobile app."),
        ("Web Developer Agent", "You are a web developer. Focus on how this concept can be presented or implemented in a website or web app."),
    ]

    results = []

    for name, instructions in agents_info:
        agent = get_agent(name, instructions)
        result = await Runner.run(agent, task_prompt, run_config=config)
        results.append((name, result.final_output))

    return results

# --- Chainlit Entry Point ---

@cl.on_message
async def handle_user_message(message: cl.Message):
    user_input = message.content

    manager = get_agent(
        "Manager Agent",
        "You are a team manager. Your job is to assign tasks to other agents and collect their responses."
    )

    await cl.Message(content="🧠 Manager Agent is delegating the task...").send()

    task_prompt = user_input or "Tell me something interesting about bladeless fans"

    results = await delegate_task_to_all_agents(task_prompt)

    # Display all agent results
    for name, output in results:
        await cl.Message(content=f"**{name} says:**\n{output}").send()
