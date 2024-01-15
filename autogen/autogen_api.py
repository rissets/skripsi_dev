from autogen import AssistantAgent, UserProxyAgent, oai, GroupChat, GroupChatManager


config_list=[
    {
        "model": "TheBloke/Magicoder-S-DS-6.7B-GPTQ",
        "base_url": "https://arabia-sas-brooks-charts.trycloudflare.com/v1/chat/completion",
        "api_type": "open_ai",
        # "api_key": "NULL", # just a placeholder
    }
]

llm_config={
    "config_list": config_list,
}

coder = AssistantAgent(
    name="Coder",
    system_message="You write the code to solve the required Task. Implement improvements provided by the critic.",
    llm_config=llm_config,
)

critic = AssistantAgent(
    name="critic",
    system_message="You will make sure that the code provided by coder is bug free and all requirements are met. also provide coder with ideas for more features that make the project better. do not provide any code.",
    llm_config=llm_config
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    system_message="A human admin wo will give the idea and run the code provided by Coder.",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)

groupchat = GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=12)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
user_proxy.initiate_chat(manager, message="Write a calculator app using tkinter for the gui. the GUI Layout should resemble the layout of a casio calculator and save it with name calculater.py in directory.", clear_history=False, config_list=config_list)

#%%
