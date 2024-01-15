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
llm_config = {"config_list": config_list, "cache_seed": 1117}
user_proxy = UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 3, "work_dir": "groupchat", "use_docker": False},
    human_input_mode="NEVER",
)
coder = AssistantAgent(
    name="Coder",  # the default assistant agent is capable of solving problems with code
    # system_message="You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.",
    llm_config=llm_config,
)
critic = AssistantAgent(
    name="Critic",
    system_message="""Critic. You are a helpful assistant highly skilled in evaluating the quality of a given visualization code by providing a score from 1 (bad) - 10 (good) while providing clear rationale. YOU MUST CONSIDER VISUALIZATION BEST PRACTICES for each evaluation. Specifically, you can carefully evaluate the code across the following dimensions
- bugs (bugs):  are there bugs, logic errors, syntax error or typos? Are there any reasons why the code may fail to compile? How should it be fixed? If ANY bug exists, the bug score MUST be less than 5.
- Data transformation (transformation): Is the data transformed appropriately for the visualization type? E.g., is the dataset appropriated filtered, aggregated, or grouped  if needed? If a date field is used, is the date field first converted to a date object etc?
- Goal compliance (compliance): how well the code meets the specified visualization goals?
- Visualization type (type): CONSIDERING BEST PRACTICES, is the visualization type appropriate for the data and intent? Is there a visualization type that would be more effective in conveying insights? If a different visualization type is more appropriate, the score MUST BE LESS THAN 5.
- Data encoding (encoding): Is the data encoded appropriately for the visualization type?
- aesthetics (aesthetics): Are the aesthetics of the visualization appropriate for the visualization type and the data?

YOU MUST PROVIDE A SCORE for each of the above dimensions.
{bugs: 0, transformation: 0, compliance: 0, type: 0, encoding: 0, aesthetics: 0}
Do not suggest code.
Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
""",
    llm_config=llm_config,
)

groupchat = GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=20)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
user_proxy.initiate_chat(
    manager,
    message="download data from https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv and plot a visualization that tells us about the relationship between weight and horsepower. Save the plot to a file. Print the fields in a dataset before visualizing it.",
)


# groupchat = GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=20)
# manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
# manager.initiate_chat(manager, message=message, clear_history=True, config_list=config_list)
# user_proxy.initiate_chat(manager, message="Write a chatbot web page using html, tailwind css and javascript. The web design must resemble an AI chatbot generate text and save it with the name index.html file in the directory. just write code", clear_history=False, config_list=config_list)

#%%

