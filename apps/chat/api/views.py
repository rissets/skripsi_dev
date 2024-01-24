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
            print(_conversation)
            system_message = f"""
            Anda adalah asisten belajar yang sangat cerdas yang secara konsisten memberikan respons yang akuran dan andal terhadap instruksi pengguna. selalu jawab menggunakan bahasa yang sesuai di dokumen.
            
            DOKUMEN PDF
            {pdf_content}
            
            """

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
    }

    def create_teachable_agent(self, reset_db=False, verbosity=0, db_dir=None):

        # Start by instantiating any agent that inherits from ConversableAgent.
        teachable_agent = autogen.ConversableAgent(
            name="teachable_agent",
            llm_config={"config_list": self.config_list, "timeout": 120, "cache_seed": None},  # Disable caching.
        )

        # Instantiate the Teachability capability. Its parameters are all optional.
        teachability = Teachability(
            verbosity=verbosity,
            reset_db=reset_db,
            path_to_db_dir=f"./tmp/{db_dir}/teachability_db",
            recall_threshold=0.5,  # Higher numbers allow more (but less relevant) memos to be recalled.
        )

        # Now add the Teachability capability to the agent.
        teachability.add_to_agent(teachable_agent)

        return teachable_agent, teachability

    def interact_freely_with_agent(self, message, db_dir):
        """Starts a free-form chat between the user and a teachable agent."""

        # Create the agents.
        teachable_agent, teachability = self.create_teachable_agent(reset_db=False, verbosity=0, db_dir=db_dir)
        user = autogen.UserProxyAgent("user", human_input_mode="NEVER", max_consecutive_auto_reply=0,
                                      code_execution_config={"work_dir": "./tmp/notebook", "use_docker": False})
        teachable_agent.initiate_chat(user, message="Hi, I'm a teachable user assistant! What's on your mind?",
                                      clear_history=True)

        # Start the chat.
        user.send(recipient=teachable_agent, message=message)

        response = user.last_message(teachable_agent)
        return response

    def extract_pdf(self, pdf_text):
        # extract pdf per dot if after . is capital letter
        paragraphs = []
        paragraph = ''
        for word in pdf_text.split():
            if word.endswith('.'):
                paragraph += word
                paragraphs.append(paragraph)
                paragraph = ''
            else:
                paragraph += word + ' '

        return paragraphs

    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            json_data = loads(request.body)
            # _conversation = json_data['meta']['content']['conversation']
            prompt = json_data['meta']['content']['parts'][0]['content']
            teachable_agent = json_data['meta']['content']['teachable_agent_slug']

            agent = request.user.teachable_agents.get(slug=teachable_agent)

            if agent.mode == 'QA':
                conversation = prompt
                response = self.interact_freely_with_agent(conversation, db_dir=teachable_agent)

                print(response['content'])

                def stream():
                    # respon kata perkata
                    for chunk in response['content']:
                        yield chunk

                return StreamingHttpResponse(stream(), content_type='text/event-stream')
            else:
                pdf = request.user.pdfs.get(pk=int(json_data['meta']['content']['pdf_id']))

                if agent.is_active:
                    agent.is_active = False
                    agent.save()

                responses = []
                for conversation in self.extract_pdf(pdf.content):
                    response = self.interact_freely_with_agent(conversation, db_dir=teachable_agent)
                    responses.append(response['content'])

                agent.is_active = True
                agent.save()

                def stream():
                    # respon kata perkata
                    for chunk in responses:
                        for chunk2 in chunk:
                            yield chunk2

                return StreamingHttpResponse(stream(), content_type='text/event-stream')



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
            # 'api_type': 'openai',
        }
    ]

    llm_config = {
        "config_list": config_list,
        "temperature": 0.7,
        "seed": 1117,
        "timeout": 120,
    }

    def create_teachable_agent(self, reset_db=False, verbosity=0, db_dir=None):

        # Start by instantiating any agent that inherits from ConversableAgent.
        teachable_agent = autogen.ConversableAgent(
            name="teachable_agent",
            llm_config={"config_list": self.config_list, "timeout": 120, "cache_seed": None},  # Disable caching.
        )

        # Instantiate the Teachability capability. Its parameters are all optional.
        teachability = Teachability(
            verbosity=verbosity,
            reset_db=reset_db,
            path_to_db_dir=f"./tmp/{db_dir}/teachability_db",
            recall_threshold=0.5,  # Higher numbers allow more (but less relevant) memos to be recalled.
        )

        # Now add the Teachability capability to the agent.
        teachability.add_to_agent(teachable_agent)

        return teachable_agent, teachability

    def interact_freely_with_agent(self, message, db_dir):
        """Starts a free-form chat between the user and a teachable agent."""

        # Create the agents.
        teachable_agent, teachability = self.create_teachable_agent(reset_db=False, verbosity=0, db_dir=db_dir)
        user = autogen.UserProxyAgent("user", human_input_mode="NEVER", max_consecutive_auto_reply=0,
                                      code_execution_config={"work_dir": "./tmp/notebook", "use_docker": False})
        # teachability.prepopulate_db()
        #

        # Start the chat.
        user.initiate_chat(teachable_agent, message=message, clear_history=True)

        response = user.last_message(teachable_agent)
        return response


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
            conversation = prompt
            response = self.interact_freely_with_agent(conversation, db_dir=agent_slug)

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
