from autogen import AssistantAgent, UserProxyAgent, oai

config_list=[
    {
        "model": "TheBloke/Magicoder-S-DS-6.7B-GPTQ",
        "base_url": "https://vacancies-fastest-displaying-bo.trycloudflare.com/v1",
        'api_key': 'any string here is fine',
        # 'api_type': 'openai',
    }
]

student = AssistantAgent(name="student",
                       max_consecutive_auto_reply=1,
                       system_message="Bertindak sebagai seorang mahasiswa.",
                       llm_config={
                           "config_list": config_list,
                           "temperature": 0.7,
                       })

programmer = AssistantAgent(name="programmer",
                     max_consecutive_auto_reply=2,
                     system_message="Bertindak sebagai seorang guru pemrogramman.",
                     llm_config={
                         "config_list": config_list,
                         "temperature": 0.7,
                     })


# student.initiate_chat(programmer, message="saya ingin belajar tentang bahasa pemrogramman python, jelaskan fundamental bahasa pemrogramman python!")

student.initiate_chat(programmer, message="python tutorial for beginners, please explain about python fundamental!")

student.initiate_chat(programmer, message="please explain about python data types!")
student.initiate_chat(programmer, message="write an example program for each data type!")

student.initiate_chat(programmer, message="python tutorial for beginners, please explain about python variables!")
student.initiate_chat(programmer, message="write an example program for each variable!")


#%%