import PyPDF2
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
from requests import get, post
from json import loads

from .config import special_instructions
from .forms import PDFForm
from .models import PDF




def read_pdf(pdf_file):
    # Read the content of the PDF file
    with open(pdf_file, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        pdf_text = ''
        for page_num in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page_num]
            pdf_text += f"page {page_num} \n\n{page_obj.extract_text()}\n\n"

        count_words = len(pdf_text.split())
        num_pages = len(pdf_reader.pages)

    return pdf_text, count_words, num_pages


class ChatView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/chat.html")


class ChatPDFView(View):
    template_name = "pages/chat-pdf.html"

    def get(self, request, *args, **kwargs):
        form = PDFForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PDFForm(request.POST, request.FILES)

        # Check if the file size is within the limit (5 MB)
        max_size = 5 * 1024 * 1024  # 5 MB in bytes
        if request.FILES and 'pdf_file' in request.FILES:
            file_size = request.FILES['pdf_file'].size
            if file_size > max_size:
                form.add_error('pdf_file',
                               f'File size must be at most 5 MB. Your file size is {file_size / (1024 * 1024):.2f} MB.')
                return render(request, self.template_name, {'form': form})

        if form.is_valid():
            uploaded_pdf = form.save()

            # Read the content of the PDF file
            pdf_text, count_words, num_pages = read_pdf(uploaded_pdf.pdf_file.path)

            # Save the content of the PDF file to the database
            uploaded_pdf.content = pdf_text
            uploaded_pdf.count_words = count_words
            uploaded_pdf.num_pages = num_pages
            uploaded_pdf.save()

            # Do something with the PDF content (e.g., display it in the template)
            return redirect('chat:render-pdf', pk=uploaded_pdf.pk)

        return render(request, self.template_name, {'form': form})


class RenderPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = PDF.objects.get(pk=kwargs['pk'])
        return render(request, 'pages/render-pdf.html', {'pdf': pdf})

# class BackendApi(View):
#     @method_decorator(csrf_exempt)
#     @method_decorator(require_POST)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         # print(request.body)
#         try:
#             json_data = loads(request.body)
#             # jailbreak = json_data['jailbreak']
#             # internet_access = json_data['meta']['content']['internet_access']
#             _conversation = json_data['meta']['content']['conversation']
#             prompt = json_data['meta']['content']['parts'][0]
#             current_date = datetime.now().strftime("%Y-%m-%d")
#             system_message = 'You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.'
#
#
#             conversation = [{'role': 'system', 'content': system_message}] + \
#                            _conversation + [prompt]
#
#             url = 'https://seconds-ascii-select-below.trycloudflare.com/v1/chat/completions'
#
#             gpt_resp = post(
#                 url=url,
#                 headers={
#                     "Content-Type": "application/json"
#                 },
#                 json={
#                     'mode': "instruct",
#                     'messages': conversation,
#                     'stream': True
#                 },
#                 stream=True
#             )
#
#             if gpt_resp.status_code >= 400:
#                 error_data = gpt_resp.json().get('error', {})
#                 error_code = error_data.get('code', None)
#                 error_message = error_data.get('message', "An error occurred")
#                 return JsonResponse({
#                     'successs': False,
#                     'error_code': error_code,
#                     'message': error_message,
#                     'status_code': gpt_resp.status_code
#                 }, status=gpt_resp.status_code)
#
#             def stream():
#                 for chunk in gpt_resp.iter_lines():
#                     try:
#                         decoded_line = loads(chunk.decode("utf-8").split("data: ")[1])
#                         token = decoded_line["choices"][0]['message'].get('content')
#                         print(token)
#
#                         if token is not None:
#                             yield token
#
#                     except GeneratorExit:
#                         break
#
#                     except Exception as e:
#                         print(e)
#                         print(e.__traceback__.tb_next)
#                         continue
#
#             return StreamingHttpResponse(stream(), content_type='text/event-stream')
#
#         except Exception as e:
#             print(e)
#             print(e.__traceback__.tb_next)
#             return JsonResponse({
#                 '_action': '_ask',
#                 'success': False,
#                 "error": f"an error occurred {str(e)}"
#             }, status=400)
