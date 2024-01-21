# forms.py
from django import forms
from .models import PDF, TeachableAgent


class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['pdf_file']


class TeachableAgentForm(forms.ModelForm):
    class Meta:
        model = TeachableAgent
        fields = ['name', 'mode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['mode'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})