import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

from openai.types.responses import ResponseTextDeltaEvent
import asyncio

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please ensure it is defined in your .env file."
    )


async def main():
    agent = Agent(
        name="Joker",
        instructions="You are helpful Assistent.",
        model=LitellmModel(model="gemini/gemini-2.0-flash", api_key=gemini_api_key)
    )
    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

def main_wrapper():
    asyncio.run(main())
    
if __name__ == "__main__":
    main_wrapper()