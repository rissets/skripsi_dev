from autogen import AssistantAgent, UserProxyAgent, oai, GroupChat, GroupChatManager

import openai

# Configure OpenAI settings
openai.api_type = "openai"
openai.api_key = "..."
openai.api_base = ""
openai.api_version = "2023-05-15"

# oai.ChatCompletion.start_logging()

config_list=[
    {
        "model": "TheBloke_Magicoder-S-DS-6.7B-GPTQ_gptq-4bit-32g-actorder_True",
        "base_url": "https://beside-makes-daddy-subaru.trycloudflare.com/v1",
        'api_key': 'any string here is fine',
        # 'api_type': 'openai',
    }
]

llm_config={
    "config_list": config_list,
}

coder = AssistantAgent(
    name="Coder",
    system_message="You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.",
    llm_config=llm_config,
)

critic = AssistantAgent(
    name="critic",
    system_message="You will make sure that the code provided by coder is bug free and all requirements are met. also provide coder with ideas for more features that make the project better. do not provide any code.",
    llm_config=llm_config
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    system_message="A human admin wo will give the idea and run the code provided by Coder. You will also install if needed any dependencies for the code to run.",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
    code_execution_config={
        "work_dir": "_output",
        # "use_docker": "python:3.9"
        "use_docker": False,
    },
)

message = """
write a python code for scraping the data from the website https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports and save it in a csv file. the csv file must contain the following columns: date, country, cases, deaths, transmission classification, days since last reported case. operating sistem using windows 11.
"""

groupchat = GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=20)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
manager.initiate_chat(manager, message=message, clear_history=True, config_list=config_list)
# user_proxy.initiate_chat(manager, message="Write a chatbot web page using html, tailwind css and javascript. The web design must resemble an AI chatbot generate text and save it with the name index.html file in the directory. just write code", clear_history=False, config_list=config_list)

#%%