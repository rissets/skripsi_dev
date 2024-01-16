from django.db import models


class Chat(models.Model):
    pass


class PDF(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')
    content = models.TextField(blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    count_words = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.pk}. {self.pdf_file.name}"