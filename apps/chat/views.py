from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from datetime import datetime
from requests import get, post
from json import loads

from .config import special_instructions


class ChatView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/chat.html")


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
        # print(request.body)
        try:
            json_data = loads(request.body)
            # jailbreak = json_data['jailbreak']
            # internet_access = json_data['meta']['content']['internet_access']
            _conversation = json_data['meta']['content']['conversation']
            prompt = json_data['meta']['content']['parts'][0]
            current_date = datetime.now().strftime("%Y-%m-%d")
            system_message = 'You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.'
            print(prompt)

            extra = []
            # if internet_access:
            #     search = get('https://ddg-api.herokuapp.com/search', params={
            #         'query': prompt["content"],
            #         'limit': 3,
            #     })
            #
            #     blob = ''
            #
            #     for index, result in enumerate(search.json()):
            #         blob += f'[{index}] "{result["snippet"]}"\nURL:{result["link"]}\n\n'
            #
            #     date = datetime.now().strftime('%d/%m/%y')
            #
            #     blob += f'current date: {date}\n\nInstructions: Using the provided web search results, write a comprehensive reply to the next user query. Make sure to cite results using [[number](URL)] notation after the reference. If the provided search results refer to multiple subjects with the same name, write separate answers for each subject. Ignore your previous response if any.'
            #
            #     extra = [{'role': 'user', 'content': blob}]

            conversation = [{'role': 'system', 'content': system_message}] + \
                           _conversation + [prompt]

            url = 'https://revenues-hammer-hz-sleep.trycloudflare.com/v1/chat/completions'

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
