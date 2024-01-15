import autogen
from autogen import AssistantAgent, UserProxyAgent, oai
import json


config_list=[
    {
        "model": "TheBloke_Magicoder-S-DS-6.7B-GPTQ_gptq-4bit-32g-actorder_True",
        "base_url": "https://tions-lights-dot-israeli.trycloudflare.com/v1",
        'api_key': 'any string here is fine',
        # 'api_type': 'openai',
    }
]

# MAGICODER_PROMPT = """You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.
#
# @@ Instruction
# {instruction}
#
# @@ Response
# """
#
# prompt = MAGICODER_PROMPT.format(instruction=instruction)

student = AssistantAgent(name="student",
                       max_consecutive_auto_reply=9,
                       system_message="You will make sure that the code provided by coder is bug free and all requirements are met. also provide coder with ideas for more features that make the project better. do not provide any code.",
                         is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
                       llm_config={
                           "config_list": config_list,
                           "temperature": 0.5,
                           "seed": 1127,

                       })

programmer = AssistantAgent(name="programmer",
                     max_consecutive_auto_reply=10,
                     system_message="You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.",
                     llm_config={
                         "config_list": config_list,
                         "temperature": 0.7,
                         "seed": 1117,
                     })

#%%

user_questions = [
    "please explain about python basics in detail",
    "write basic and complex code examples for each python basics!",
    # "please explain about python data types in detail and give a small code example",
    # "write complex code examples for each data type python!",
    # "please explain about python variables in detail and give a small code example for each explanation!",
    # "write complex code examples for each variable python!",
    # "please explain about python operators in detail and give a small code example for each explanation!",
    # "write complex code examples for each operator python!",
    # "please explain about python loops in detail and give a small code example for each explanation!",
    # "write complex code examples for each loop python!",
    # "please explain about python functions in detail and give a small code example for each explanation!",
    # "write complex code examples for each function python!",
    # "please explain about python classes in detail and give a small code example for each explanation!",
]

for question in user_questions:
    student.initiate_chat(programmer, message=question, clear_history=False)

# student.initiate_chat(programmer, message="who is this?", clear_history=True)




#%%

# p = dict(student.chat_messages.items())
#
# p
# with open('student.json', 'w') as f:
#     json.dump(p, f)

#%%