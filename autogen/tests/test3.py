import os
import autogen


class AutoGenChatter:
    def __init__(self, autogen_user_proxy, autogen_assistant):
        self.user_proxy = autogen_user_proxy
        self.assistant = autogen_assistant

    async def chat(self, message, silent=False):
        sender = self.user_proxy
        message = {"content": message}
        self.assistant.add_message(sender, message)
        response = await self.assistant.a_generate_reply(sender=sender)
        return response


config_list = [
    {
        "model": "TheBloke_Magicoder-S-DS-6.7B-GPTQ_gptq-4bit-32g-actorder_True",
        "base_url": "https://policy-devel-format-tm.trycloudflare.com/v1",
        'api_key': 'any string here is fine',
        # 'api_type': 'openai',
    }
]

llm_config = {
    "config_list": config_list,
}


assistant_message = '''
                Answer any question user asks you politely with details.
            '''

user_proxy_message = '''
            You are a helpful assistant who answers any questions.
        '''

test_assistant = autogen.AssistantAgent(
    name="test_assistant",
    system_message=assistant_message,
    llm_config=llm_config,
)

test_user_proxy = autogen.UserProxyAgent(
    name="Dave",
    human_input_mode="ALWAYS",

)
test_assistant.reset()
autogen_chatter = AutoGenChatter(test_user_proxy, test_assistant)
response = autogen_chatter.chat(user_proxy_message)
print(response)


    #%%