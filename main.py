from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, RunConfig
import asyncio

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

async def marketing_agent():
    assistant = Agent(
        name="Marketing Agent",
        instructions="You are a creative marketing expert. Explain things in a way that grabs customer attention and highlights product benefits.",
        model=model
    )
    result = await Runner.run(assistant, "Tell me something interesting about bladeless fans", run_config=config)
    return result.final_output

async def mobile_app_devolper():
    assistant = Agent(
        name="Mobile App Developer Agent",
        instructions="You are a mobile app developer. Think about how this concept can be applied or enhanced through a mobile app.",
        model=model
    )
    result = await Runner.run(assistant, "Tell me something interesting about bladeless fans", run_config=config)
    return result.final_output

async def web_devolper():
    assistant = Agent(
        name="Web Developer Agent",
        instructions="You are a web developer. Focus on how this concept can be presented or implemented in a website or web app.",
        model=model
    )
    result = await Runner.run(assistant, "Tell me something interesting about bladeless fans", run_config=config)
    return result.final_output

async def manager():
    assistant = Agent(
        name="Manager Agent",
        instructions="You are a team manager. Your job is to assign tasks to other agents and collect their responses.",
        model=model
    )

    # Manager doing an optional task itself
    manager_result = await Runner.run(assistant, "Assigning task: bladeless fan research", run_config=config)
    print("\n📋 Manager Task Summary:")
    print(manager_result.final_output)

    # Now assigning tasks to agents
    print("\n📢 Marketing Agent Response:")
    marketing_response = await marketing_agent()
    print(marketing_response)

    print("\n📱 Mobile App Developer Response:")
    mobile_response = await mobile_app_devolper()
    print(mobile_response)

    print("\n💻 Web Developer Response:")
    web_response = await web_devolper()
    print(web_response)

if __name__ == "__main__":
    asyncio.run(manager())
