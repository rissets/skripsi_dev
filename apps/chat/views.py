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
from .forms import PDFForm, TeachableAgentForm
from .models import PDF


class TeachableView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        agent = request.user.teachable_agents.get(slug=slug)
        if agent.mode == 'QA':
            return render(request, "pages/teachable.html", {'teachable_agent': slug})
        if agent.mode == 'PDF':
            pdfs = request.user.pdfs.all()
            return render(request, "pages/teachable_pdf.html", {'teachable_agent': slug, 'pdfs': pdfs})
        return redirect('chat:teachable-agent')


class TestTeachableView(View):
    def get(self, request, *args, **kwargs):
        agents = request.user.teachable_agents.all()
        return render(request, "pages/test_teachable_agent.html", {'agents': agents})



class ChatView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/chat.html")


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


class CreateTeachableAgent(View):
    template_name = "pages/create-teachable-agent.html"
    form = TeachableAgentForm
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            teachable_agent = form.save(commit=False)
            teachable_agent.user = request.user
            teachable_agent.save()
            return redirect('chat:teachable-agent')
        return render(request, self.template_name, {'form': form})


class TeachableAgentView(View):
    def get(self, request, *args, **kwargs):
        agents = request.user.teachable_agents.all()
        return render(request, "pages/teachable_agents.html", {'agents': agents})