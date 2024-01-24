import json
from json import loads
import PyPDF2
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View

from .forms import PDFForm, TeachableAgentForm, GroupChatForm, AgentForm
from .models import PDF


class TeachableView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        agent = request.user.teachable_agents.get(slug=slug)
        if agent.mode == 'QA':
            return render(request, "pages/teachable.html", {'teachable_agent': slug})
        if agent.mode == 'PDF':
            pdfs = request.user.pdfs.all()
            return render(request, "pages/teachable_pdf.html", {'teachable_agent': slug, 'pdfs': pdfs})
        return redirect('chat:teachable-agent')


class TestTeachableView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        agents = request.user.teachable_agents.all()
        return render(request, "pages/test_teachable_agent.html", {'agents': agents})


class CreateTeachableAgent(LoginRequiredMixin, View):
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


class TeachableAgentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        agents = request.user.teachable_agents.all()
        return render(request, "pages/teachable_agents.html", {'agents': agents})


class TeachableAgentDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        agent = request.user.teachable_agents.get(slug=slug)
        agent.delete()
        # delete folder tmp/<slug>
        import os
        os.system(f"rm -rf tmp/{slug}")
        return redirect('chat:teachable-agent')


class ChatView(LoginRequiredMixin, View):
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


class UploadPDFView(LoginRequiredMixin, View):
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
            form.instance.user = request.user
            uploaded_pdf = form.save()

            # Read the content of the PDF file
            pdf_text, count_words, num_pages = read_pdf(uploaded_pdf.pdf_file.path)

            # Save the content of the PDF file to the database
            uploaded_pdf.content = pdf_text
            uploaded_pdf.count_words = count_words
            uploaded_pdf.num_pages = num_pages
            uploaded_pdf.save()

            # Do something with the PDF content (e.g., display it in the template)
            return redirect('chat:pdfs')

        return render(request, self.template_name, {'form': form})


class RenderPDF(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pdf = PDF.objects.get(pk=kwargs['pk'])
        return render(request, 'pages/render-pdf.html', {'pdf': pdf})


class ChatPDFListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pdfs = request.user.pdfs.all()
        return render(request, "pages/chat-pdfs.html", {'pdfs': pdfs})


class ChatPDFDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        pdf = request.user.pdfs.get(pk=pk)
        pdf.delete()
        return redirect('chat:pdfs')


class GroupChatListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        group_chats = request.user.group_chats.all()
        return render(request, "pages/groupchats.html", {'group_chats': group_chats})


class GroupChatCreateView(LoginRequiredMixin, View):
    template_name = "pages/groupchat-create.html"
    form = GroupChatForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            group_chat = form.save(commit=False)
            group_chat.user = request.user
            group_chat.save()
            return redirect('chat:group-chat')
        return render(request, self.template_name, {'form': form})


class AgentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        group_chats = request.user.group_chats.get(slug=kwargs.get('slug'))
        agents = group_chats.agents.all()

        return render(request, "pages/agents.html", {'agents': agents, 'group_chat': group_chats})


class AgentCreateView(LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AgentCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                data = loads(request.body)
                agent_name = data['name']
                agent_instruction = data['instruction']
                group_chat_id = data['group_chat_id']

                form = AgentForm({'name': agent_name, 'instruction': agent_instruction})
                group_chat = request.user.group_chats.get(pk=group_chat_id)

                if form.is_valid():
                    agent = form.save(commit=False)
                    agent.user = request.user
                    agent.group_chat = group_chat
                    agent.save()

                    response_data = {
                        'status': 'success',
                        'message': 'Agent created successfully',
                        'agent_name': agent.name,
                        'agent_slug': agent.slug,
                        'agent_instruction': agent.instruction,
                    }
                    return JsonResponse(response_data)
                else:
                    response_data = {
                        'status': 'error',
                        'message': 'Form is invalid'
                    }
                    return JsonResponse(response_data)

            except json.JSONDecodeError as e:
                response_data = {
                    'status': 'error',
                    'message': 'Invalid JSON format'
                }
                return JsonResponse(response_data)

        else:
            response_data = {
                'status': 'error',
                'message': 'Invalid request method'
            }
            return JsonResponse(response_data)


class AgentDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        agent = request.user.agents.get(slug=slug)
        slug = agent.group_chat.slug
        agent.delete()
        return redirect("chat:agent", slug=slug)


class AgentUpdateView(LoginRequiredMixin, View):
    template_name = "pages/agent-update.html"
    form = AgentForm

    def get(self, request, *args, **kwargs):
        agent = request.user.agents.get(slug=kwargs.get('slug'))
        return render(request, self.template_name, {'form': self.form(instance=agent)})

    def post(self, request, *args, **kwargs):
        agent = request.user.agents.get(slug=kwargs.get('slug'))
        form = self.form(request.POST, instance=agent)
        if form.is_valid():
            form.save()
            return redirect("chat:agent", slug=agent.group_chat.slug)
        return render(request, self.template_name, {'form': form})


class GroupChatView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        group_chats = request.user.group_chats.all()
        return render(request, "pages/group_chat.html", {'group_chats': group_chats})