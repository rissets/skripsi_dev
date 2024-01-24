from autogen import UserProxyAgent, config_list_from_json
from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen import ConversableAgent

import os
import sys

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# from test_assistant_agent import OAI_CONFIG_LIST, KEY_LOC  # noqa: E402


try:
    from termcolor import colored
except ImportError:

    def colored(x, *args, **kwargs):
        return x


# Specify the model to use. GPT-3.5 is less reliable than GPT-4 at learning from user input.
# filter_dict = {"model": ["gpt-4-1106-preview"]}
# filter_dict = {"model": ["gpt-3.5-turbo-1106"]}
# filter_dict = {"model": ["gpt-4-0613"]}
# filter_dict = {"model": ["gpt-3.5-turbo-0613"]}
# filter_dict = {"model": ["gpt-4"]}
# filter_dict = {"model": ["gpt-35-turbo-16k", "gpt-3.5-turbo-16k"]}

config_list=[
    {
        "model": "TheBloke_Magicoder-S-DS-6.7B-GPTQ_gptq-4bit-32g-actorder_True",
        "base_url": "https://buys-corrections-approx-defend.trycloudflare.com/v1",
        'api_key': 'any string here is fine',
        # 'api_type': 'openai',
    }
]


def create_teachable_agent(reset_db=False, verbosity=0):
    """Instantiates a teachable agent using the settings from the top of this file."""
    # Load LLM inference endpoints from an env variable or a file
    # See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
    # and OAI_CONFIG_LIST_sample

    # Start by instantiating any agent that inherits from ConversableAgent.
    teachable_agent = ConversableAgent(
        name="teachable_agent",
        llm_config={"config_list": config_list, "timeout": 120, "cache_seed": None},  # Disable caching.
    )

    # Instantiate the Teachability capability. Its parameters are all optional.
    teachability = Teachability(
        verbosity=verbosity,
        reset_db=reset_db,
        path_to_db_dir="./tmp/interactive_v4/teachability_db",
        recall_threshold=1.5,  # Higher numbers allow more (but less relevant) memos to be recalled.
    )

    # Now add the Teachability capability to the agent.
    teachability.add_to_agent(teachable_agent)
    teachability.recall_threshold

    return teachable_agent, teachability

def interact_freely_with_user():
    """Starts a free-form chat between the user and a teachable agent."""

    default_auto_repl = {
        "content": "My name is Danang Haris Setiawan",
        "content": "My hoby is coding, music and writing"
    }

    # Create the agents.
    print(colored("\nLoading previous memory (if any) from disk.", "light_cyan"))
    teachable_agent, teachability = create_teachable_agent(reset_db=True, verbosity=0)
    user = UserProxyAgent("user", human_input_mode="NEVER", max_consecutive_auto_reply=1, default_auto_reply="My name is danang haris setiawan")
    teachability.prepopulate_db()

    # Start the chat.
    teachable_agent.initiate_chat(user, message="Greetings, I'm a teachable user assistant! What's on your mind today?", clear_history=True)


def interactive_with_agent():
    """Starts a free-form chat between the user and a teachable agent."""

    # Create the agents.
    print(colored("\nLoading previous memory (if any) from disk.", "light_cyan"))
    teachable_agent, teachability = create_teachable_agent(reset_db=True, verbosity=0)
    user = ConversableAgent("user", human_input_mode="NEVER", llm_config={"config_list": config_list, "timeout": 120, "cache_seed": None}, max_consecutive_auto_reply=1, code_execution_config={"work_dir": "./tmp/notebook", "use_docker": False})
    teachability.prepopulate_db()

    # Start the chat.
    user.initiate_chat(teachable_agent, message="what is my name ?", clear_history=True)
#%%

if __name__ == "__main__":
    """Lets the user test a teachable agent interactively."""
    interact_freely_with_user()