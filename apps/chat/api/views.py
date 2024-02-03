import time

from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from datetime import datetime
from requests import get, post
from json import loads

import autogen
from autogen.agentchat.contrib.capabilities import Teachability

from django.conf import settings


def prompt_template(prompt: str):
    template = f"""You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.
    @@ Instruction
    {prompt}

    @@ Response
    """
    return template


class BackendApi(View):
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            json_data = loads(request.body)
            _conversation = json_data['meta']['content']['conversation']
            prompt = json_data['meta']['content']['parts'][0]
            chat_mode = json_data['chat_mode']
            print(chat_mode)
            current_date = datetime.now().strftime("%Y-%m-%d")
            if chat_mode == 'general':
                system_message = f'You are an exceptionally intelligent {chat_mode} coding assistant that consistently delivers accurate and reliable responses to user instructions.'
            else:
                system_message = f'You are an exceptionally intelligent {chat_mode} coding assistant that consistently delivers accurate and reliable responses to user instructions.'

            conversation = [{'role': 'system', 'content': system_message}] + \
                           _conversation + [prompt]

            endpoint = settings.MODEL_URL
            url = f"{endpoint}v1/chat/completions"

            gpt_resp = post(
                url=url,
                headers={
                    "Content-Type": "application/json"
                },
                json={
                    'mode': "instruct",
                    'messages': conversation,
                    'stream': True
                },
                stream=True
            )

            if gpt_resp.status_code >= 400:
                error_data = gpt_resp.json().get('error', {})
                error_code = error_data.get('code', None)
                error_message = error_data.get('message', "An error occurred")
                return JsonResponse({
                    'successs': False,
                    'error_code': error_code,
                    'message': error_message,
                    'status_code': gpt_resp.status_code
                }, status=gpt_resp.status_code)

            def stream():
                for chunk in gpt_resp.iter_lines():
                    try:
                        decoded_line = loads(chunk.decode("utf-8").split("data: ")[1])
                        token = decoded_line["choices"][0]['message'].get('content')
                        print(token)

                        if token is not None:
                            yield token

                    except GeneratorExit:
                        break

                    except Exception as e:
                        print(e)
                        print(e.__traceback__.tb_next)
                        continue

            return StreamingHttpResponse(stream(), content_type='text/event-stream')

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_next)
            return JsonResponse({
                '_action': '_ask',
                'success': False,
                "error": f"an error occurred {str(e)}"
            }, status=400)


class BackendApiPDF(View):
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            json_data = loads(request.body)

            _conversation = json_data['meta']['content']['conversation']
            prompt = json_data['meta']['content']['parts'][0]
            pdf_content = json_data['meta']['content']['parts'][1]['content_pdf']
            # print(prompt)
            # print(pdf_content)
            # print(_conversation)
            # prompt = f"""{pdf_content} \n {prompt}"""

            # split pdf if len words > 10000 and store per 5000 in dict

            endpoint = settings.MODEL_URL
            url = f"{endpoint}v1/chat/completions"

            if len(pdf_content.split(' ')) > 11000 and _conversation == []:

                contents = [pdf_content[i:i + 10000] for i in range(0, len(pdf_content), 10000)]

                for i in range(len(contents)):
                    pdf_content = contents[i]
                    print(f"{len(contents)} - {i} - {len(pdf_content)}")

                    message = f"""{pdf_content}"""

                    conversation = [{'role': 'system', 'content': message}, {'role': 'user',
                                                                             'content': 'please remember the document. I will ask you for help later'}]

                    res = post(
                        url=url,
                        headers={
                            "Content-Type": "application/json"
                        },
                        json={
                            'mode': "instruct",
                            'messages': conversation,
                        },
                    )
                    print(res.json())
                system_message = f"""
                        You are a highly intelligent learning assistant that consistently provides accurate and reliable responses to user instructions based on previous chat history.
                        """

            else:
                system_message = f"""
                    You are an assistant who can summarize, explain, draw lessons from these pdf documents. and consistently provide accurate and reliable responses to users.

                    pdf document: {pdf_content}
                    """

            conversation = [{'role': 'system', 'content': system_message}] + \
                           _conversation + [prompt]

            print(conversation)

            gpt_resp = post(
                url=url,
                headers={
                    "Content-Type": "application/json"
                },
                json={
                    'mode': "instruct",
                    'messages': conversation,
                    'stream': True
                },
                stream=True
            )

            if gpt_resp.status_code >= 400:
                error_data = gpt_resp.json().get('error', {})
                error_code = error_data.get('code', None)
                error_message = error_data.get('message', "An error occurred")
                return JsonResponse({
                    'successs': False,
                    'error_code': error_code,
                    'message': error_message,
                    'status_code': gpt_resp.status_code
                }, status=gpt_resp.status_code)

            def stream():
                for chunk in gpt_resp.iter_lines():
                    try:
                        decoded_line = loads(chunk.decode("utf-8").split("data: ")[1])
                        token = decoded_line["choices"][0]['message'].get('content')
                        print(token)

                        if token is not None:
                            yield token

                    except GeneratorExit:
                        break

                    except Exception as e:
                        print(e)
                        print(e.__traceback__.tb_next)
                        continue

            return StreamingHttpResponse(stream(), content_type='text/event-stream')

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_next)
            return JsonResponse({
                '_action': '_ask',
                'success': False,
                "error": f"an error occurred {str(e)}"
            }, status=400)


class BackendApiTeachable(View):
    config_list = [
        {
            "model": "TheBloke_Magicoder-S-DS-6.7B-GPTQ_gptq-4bit-32g-actorder_True",
            "base_url": f"{settings.MODEL_URL}v1/",
            'api_key': 'any string here is fine',
            # 'api_type': 'openai',
        }
    ]

    llm_config = {
        "config_list": config_list,
        "temperature": 0.7,
        "timeout": 120,
        "cache_seed": None,
    }

    def create_teachable_agent(self, reset_db=False, verbosity=0, db_dir=None):

        # Start by instantiating any agent that inherits from ConversableAgent.
        teachable_agent = autogen.ConversableAgent(
            name="teachable_agent",
            llm_config=self.llm_config,  #
            code_execution_config={
                "work_dir": f"./tmp/_output",
                "use_docker": False
            }
        )

        # Instantiate the Teachability capability. Its parameters are all optional.
        teachability = Teachability(
            verbosity=verbosity,
            reset_db=reset_db,
            path_to_db_dir=f"./tmp/{db_dir}/teachability_db",
            recall_threshold=1,  # Higher numbers allow more (but less relevant) memos to be recalled.
        )

        # Now add the Teachability capability to the agent.
        teachability.add_to_agent(teachable_agent)

        return teachable_agent

    def extract_pdf(self, pdf_text):
        # extract pdf per page page 0, page 1, ect

        pdf_text = pdf_text.split('page')
        pdf_text = [text for text in pdf_text if text != '']
        pdf_text = [text.strip() for text in pdf_text]

        print(pdf_text)
        return pdf_text

    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            json_data = loads(request.body)
            # _conversation = json_data['meta']['content']['conversation']
            prompt = json_data['meta']['content']['parts'][0]['content']
            teachable_agent_name = json_data['meta']['content']['teachable_agent_slug']

            agent = request.user.teachable_agents.get(slug=teachable_agent_name)

            if agent.mode == 'QA':
                conversation = prompt
                teachable_agent = self.create_teachable_agent(reset_db=False, verbosity=0, db_dir=teachable_agent_name)
                user = autogen.ConversableAgent("user",
                                                llm_config=False,
                                                human_input_mode="NEVER",
                                                max_consecutive_auto_reply=0,
                                                code_execution_config={
                                                    "work_dir": f"./tmp/{teachable_agent_name}/_output",
                                                    "use_docker": False
                                                }
                                                )

                user.initiate_chat(recipient=teachable_agent, message=conversation)

                response = user.last_message(teachable_agent)

                def stream():
                    # respon kata perkata
                    for chunk in response['content']:
                        yield chunk

                return StreamingHttpResponse(stream(), content_type='text/event-stream')
            else:
                teachable_agent = self.create_teachable_agent(reset_db=False, verbosity=0, db_dir=teachable_agent_name)
                user = autogen.ConversableAgent("user",
                                                llm_config=False,
                                                human_input_mode="NEVER",
                                                max_consecutive_auto_reply=0,
                                                code_execution_config={
                                                    "work_dir": f"./tmp/{teachable_agent_name}/_output",
                                                    "use_docker": False
                                                }
                                                )
                pdf = request.user.pdfs.get(pk=int(json_data['meta']['content']['pdf_id']))
                print(f"pdf {pdf}")
                if agent.is_active:
                    agent.is_active = False
                    agent.save()

                for conversation in self.extract_pdf(pdf.content):
                    user.initiate_chat(recipient=teachable_agent, message=conversation)

                agent.is_active = True
                agent.save()

                return JsonResponse({ '_action': '_ask', 'success': True, 'message': 'Teachable agent is active' })



        except Exception as e:
            print(e)
            print(e.__traceback__.tb_next)
            return JsonResponse({
                '_action': '_ask',
                'success': False,
                "error": f"an error occurred {str(e)}"
            }, status=400)


class BackendApiTestTeachable(View):
    config_list = [
        {
            "model": "TheBloke_Magicoder-S-DS-6.7B-GPTQ_gptq-4bit-32g-actorder_True",
            "base_url": f"{settings.MODEL_URL}v1/",
            'api_key': 'any string here is fine',
        }
    ]

    llm_config = {
        "config_list": config_list,
        "temperature": 0.7,
        "timeout": 120,
    }

    def create_teachable_agent(self, reset_db=False, verbosity=0, db_dir=None):

        # Start by instantiating any agent that inherits from ConversableAgent.
        teachable_agent = autogen.ConversableAgent(
            name="teachable_agent",
            llm_config=self.llm_config,  #
            code_execution_config={
                "work_dir": f"./tmp/_output",
                "use_docker": False
            }
        )

        # Instantiate the Teachability capability. Its parameters are all optional.
        teachability = Teachability(
            verbosity=verbosity,
            reset_db=reset_db,
            path_to_db_dir=f"./tmp/{db_dir}/teachability_db",
            recall_threshold=1,  # Higher numbers allow more (but less relevant) memos to be recalled.
        )

        # Now add the Teachability capability to the agent.
        teachability.add_to_agent(teachable_agent)

        return teachable_agent

    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            json_data = loads(request.body)
            # _conversation = json_data['meta']['content']['conversation']
            prompt = json_data['meta']['content']['parts'][0]['content']
            agent_slug = json_data['agent_slug']

            print(agent_slug)
            # response = self.interact_freely_with_agent(conversation, db_dir=agent_slug)

            conversation = prompt
            print(conversation)
            teachable_agent = self.create_teachable_agent(reset_db=False, verbosity=0, db_dir=agent_slug)
            user = autogen.ConversableAgent("user",
                                            llm_config=False,
                                            human_input_mode="NEVER",
                                            max_consecutive_auto_reply=0,
                                            code_execution_config={
                                                "work_dir": f"./tmp/{agent_slug}/_output",
                                                "use_docker": False
                                            }
                                            )

            user.initiate_chat(recipient=teachable_agent, message=conversation)

            response = user.last_message(teachable_agent)

            def stream():
                # respon kata perkata
                for chunk in response['content']:
                    yield chunk

            return StreamingHttpResponse(stream(), content_type='text/event-stream')


        except Exception as e:
            print(e)
            print(e.__traceback__.tb_next)
            return JsonResponse({
                '_action': '_ask',
                'success': False,
                "error": f"an error occurred {str(e)}"
            }, status=400)


class BackendApiGroupChat(View):
    config_list = [
        {
            "model": "TheBloke_Magicoder-S-DS-6.7B-GPTQ_gptq-4bit-32g-actorder_True",
            "base_url": f"{settings.MODEL_URL}v1/",
            'api_key': 'any string here is fine',
            # 'api_type': 'openai',
        }
    ]

    llm_config = {
        "config_list": config_list,
        "temperature": 0.7,
        "timeout": 120,
    }

    all_messages = []

    def create_group_chat(self, agents: list):

        def print_messages(recipient, messages, sender, config):
            if "callback" in config and config["callback"] is not None:
                callback = config["callback"]
                callback(sender, recipient, messages[-1])
            # print(f"Messages sent to: {recipient.name} | num messages: {len(messages)}")
            print(f"Last Messages: {messages[-1]}")
            # print(f"Messsages: {messages}")
            self.all_messages.append(messages[-1])

            return False, None  # required to ensure the agent communication flow continues

        user_proxy = autogen.UserProxyAgent(
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

        agents_list = []
        for agent in agents:
            agents_list.append(autogen.AssistantAgent(
                name=agent['name'],
                system_message=agent['instruction'],
                llm_config=self.llm_config,
            ))

        agents_list.append(user_proxy)

        for agent in agents_list:
            agent.register_reply(
                [autogen.Agent, None],
                reply_func=print_messages,
                config={"callback": None},
            )

        group_chat = autogen.GroupChat(agents=agents_list, messages=[], max_round=10)

        return group_chat

    def initiate_chat(self, group_chat, message):
        manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=self.llm_config)
        manager.initiate_chat(manager, message=message, clear_history=True, config_list=self.config_list)

        return manager

    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            json_data = loads(request.body)
            prompt = json_data['meta']['content']['parts'][0]['content']
            groupChat = json_data['groupChat']

            group_chat = self.request.user.group_chats.get(slug=groupChat)
            agents = []
            for agent in group_chat.agents.all():
                agents.append({
                    "name": agent.name.lower().replace(' ', '_'),
                    "instruction": agent.instruction,
                })
            
            print(agents)
            print(group_chat)
            group_chat = self.create_group_chat(agents=agents)
            self.initiate_chat(group_chat, message=prompt)

            response = self.all_messages

            def stream():
                for chunk in response:
                    name = f" \n\n **{chunk['name']}: ** \n " if 'name' in chunk and chunk['name'] else f" \n\n **{chunk.get('role', '')}** \n "
                    for word in name.split(' '):
                        yield word
                    
                    chunk['content'] = chunk['content'].split(' ')
                    
                    for word in chunk['content']:
                        # sleep(0.1)
                        time.sleep(0.03)
                        yield word + ' '

            self.all_messages = []
            return StreamingHttpResponse(stream(), content_type='text/event-stream')

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_next)
            return JsonResponse({
                '_action': '_ask',
                'success': False,
                "error": f"an error occurred {str(e)}"
            }, status=400)
