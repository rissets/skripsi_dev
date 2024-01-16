import autogen

from IPython import get_ipython

import autogen
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager, ConversableAgent
from autogen.agentchat.contrib.capabilities import Teachability

config_list=[
    {
        "model": "TheBloke/Magicoder-S-DS-6.7B-GPTQ",
        "base_url": "https://tions-lights-dot-israeli.trycloudflare.com/v1",
        'api_key': 'any string here is fine',
        # 'api_type': 'openai',
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.2,
    "seed": 1117,
    "timeout": 6000,
}


teachable_agent = ConversableAgent(
    name="teachable_agent",  # The name can be anything.
    llm_config=llm_config
)

teachability = Teachability(
    reset_db=False,  # Use True to force-reset the memo DB, and False to use an existing DB.
    path_to_db_dir="./tmp/interactive/teachability_db",  # The path to the DB directory.
)

# Now add teachability to the agent.
teachability.add_to_agent(teachable_agent)

# For this test, create a user proxy agent as usual.
user = UserProxyAgent("user", human_input_mode="ALWAYS")



#%%
# This function will return once the user types 'exit'.
teachable_agent.initiate_chat(user, message="Hi, I'm a teachable user assistant! What's on your mind?")
#%%
