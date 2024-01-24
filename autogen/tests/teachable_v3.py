import autogen
from autogen.agentchat.contrib.capabilities import Teachability


config_list = [
    {
        "model": "TheBloke_Magicoder-S-DS-6.7B-GPTQ_gptq-4bit-32g-actorder_True",
        "base_url": "https://proud-refresh-vital-tested.trycloudflare.com/v1",
        'api_key': 'any string here is fine',
        # 'api_type': 'openai',
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
    "timeout": 120,
}

teachable_agent = autogen.ConversableAgent(
    name="teachable_agent",  # The name can be anything.
    llm_config=llm_config,
)

teachability = Teachability(
    verbosity=0,
    reset_db=False,  # Use True to force-reset the memo DB, and False to use an existing DB.
    path_to_db_dir="./tmp/test-agent_v1/teachability_db",  # The path to the DB directory.
    recall_threshold=0.5,  # Higher numbers allow more (but less relevant) memos to be recalled.
    # max_num_retrievals=0,
)

teachability.add_to_agent(teachable_agent)

user = autogen.UserProxyAgent(
    "user",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
    max_consecutive_auto_reply=0,
    code_execution_config={
        "work_dir": "./tmp/notebook",
        "use_docker": False
    },
    # system_message="My name is danang haris setiawan",
    # default_auto_reply=
)

# teachability


teachable_agent.initiate_chat(user, message="Hi, I'm a teachable user assistant! What's on your mind?",
                                          clear_history=False)



# teachable_agent.send(recipient=user, message="My name is danang haris setiawan")
user.send(recipient=teachable_agent, message="My name is danang haris setiawan")

user.initiate_chat(teachable_agent, message="What is my name ?",
                                          clear_history=False)

# user.initiate_chat(teachable_agent, message="My name is danang haris",
#                                           clear_history=False)
# response = teachable_agent.last_message(user)

# print(response)

#%%