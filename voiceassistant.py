import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig


# Load environment variables from .env file
load_dotenv()

# Get the ElevenLabs API key from environment variables
AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("ElevenLabs API key is not set. Please set the AGENT_KEY environment variable.")

user_name = "Tyler"
assistant_name = "Lebron"
schedule = "Gym with Quynh at 12:00 PM, Gaming with the boys at 6:00 PM"
prompt = f"""
You are a personal assistant named {assistant_name}. You are very helpful and friendly.
My name is {user_name}. Here are my plans:{schedule}
You can help me with my schedule, my tasks, and you can also help me with my reminders.
"""
first_message = f"Hello {user_name}, I am {assistant_name}. How can I help you today?"

# Initialize ElevenLabs client
conversation_override = {
    "agent": {
        "prompt": {
            "prompt": prompt,
        },
        "first_message": first_message,
    },
}

config = ConversationConfig(
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
)

client = ElevenLabs(api_key=API_KEY)

conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
)

# Handle assistant responses
def print_agent_response(response):
    print(f"Agent: {response}")

def print_interrupted_response(original, corrected):
    print(f"Agent Interrupted: {corrected}")

def print_user_transcript(transcript):
    print(f"User: {transcript}")


#Initialize the conversation
conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=print_agent_response,
    callback_agent_response_correction=print_interrupted_response,
    callback_user_transcript=print_user_transcript,
)

conversation.start_session()


