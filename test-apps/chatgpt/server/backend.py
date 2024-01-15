from json import dumps
from time import time
from flask import request
from hashlib import sha256
from datetime import datetime
from requests import get
from requests import post 
from json     import loads
import os

from .config import special_instructions


def prompt_template(prompt: str):
    template =\
        f"""You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.
        @@ Instruction
        {prompt}
        
        @@ Response
        """
    return template


class Backend_Api:
    def __init__(self, app, config: dict) -> None:
        self.app = app
        self.host = "farms-this-preferences-provincial.trycloudflare.com"
        self.endpoint_url  = f'https://{self.host}/v1/chat/completions'

        self.history = []

        self.proxy = config['proxy']
        self.routes = {
            '/backend-api/v2/conversation': {
                'function': self._conversation,
                'methods': ['POST']
            }
        }

    def _conversation(self):
        try:
            jailbreak = request.json['jailbreak']
            internet_access = request.json['meta']['content']['internet_access']
            _conversation = request.json['meta']['content']['conversation']
            prompt = request.json['meta']['content']['parts'][0]
            current_date = datetime.now().strftime("%Y-%m-%d")
            system_message = f'You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.'

            extra = []
            if internet_access:
                search = get('https://ddg-api.herokuapp.com/search', params={
                    'query': prompt["content"],
                    'limit': 3,
                })

                blob = ''

                for index, result in enumerate(search.json()):
                    blob += f'[{index}] "{result["snippet"]}"\nURL:{result["link"]}\n\n'

                date = datetime.now().strftime('%d/%m/%y')

                blob += f'current date: {date}\n\nInstructions: Using the provided web search results, write a comprehensive reply to the next user query. Make sure to cite results using [[number](URL)] notation after the reference. If the provided search results refer to multiple subjects with the same name, write separate answers for each subject. Ignore your previous response if any.'

                extra = [{'role': 'user', 'content': blob}]

            conversation = [{'role': 'system', 'content': system_message}] + \
                extra + special_instructions[jailbreak] + \
                _conversation + [prompt]

            url = f"{self.host}/v1/chat/completions"

            # proxies = None
            # if self.proxy['enable']:
            #     proxies = {
            #         'http': self.proxy['http'],
            #         'https': self.proxy['https'],
            #     }

            gpt_resp = post(
                url     = self.endpoint_url,
                # proxies = proxies,
                headers = {
                    "Content-Type": "application/json"
                }, 
                json    = {
                    'mode'             : "instruct",
                    'messages'          : conversation,
                    'stream'            : True
                },
                stream  = True
            )
            # client = sss

            if gpt_resp.status_code >= 400:
                error_data =gpt_resp.json().get('error', {})
                error_code = error_data.get('code', None)
                error_message = error_data.get('message', "An error occurred")
                return {
                    'successs': False,
                    'error_code': error_code,
                    'message': error_message,
                    'status_code': gpt_resp.status_code
                }, gpt_resp.status_code

            def stream():
                for chunk in gpt_resp.iter_lines():
                    try:
                        decoded_line = loads(chunk.decode("utf-8").split("data: ")[1])
                        token = decoded_line["choices"][0]['message'].get('content')
                        print(token)

                        if token != None: 
                            yield token
                            
                    except GeneratorExit:
                        break

                    except Exception as e:
                        print(e)
                        print(e.__traceback__.tb_next)
                        continue
                        
            return self.app.response_class(stream(), mimetype='text/event-stream')

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_next)
            return {
                '_action': '_ask',
                'success': False,
                "error": f"an error occurred {str(e)}"}, 400
