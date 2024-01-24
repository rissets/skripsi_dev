from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Chat(models.Model):
    pass


class PDF(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdfs')
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdfs/')
    content = models.TextField(blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    count_words = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.pk}. {self.name}"

    def save(self, *args, **kwargs):
        # hilangkan tanda _, -, dan spasi
        self.name = self.pdf_file.name.replace('_', ' ').replace('-', ' ').replace('.pdf', '')
        self.name = self.name.replace('pdfs/', '').replace('.pdf', '')
        super().save(*args, **kwargs)

class TeachableAgent(models.Model):
    MODE_CHOICES = (
        ('QA', 'Question-Answer'),
        ('PDF', 'PDF'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teachable_agents')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    mode = models.CharField(max_length=255, choices=MODE_CHOICES, default='QA')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pk}. {self.name}"

    def get_absolute_url(self):
        return reverse('teachable_agent_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class GroupChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_chats')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pk}. {self.name}"

    def get_absolute_url(self):
        return reverse('group_chat_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class Agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agents')
    name = models.CharField(max_length=255)
    instruction = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='agents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pk}. {self.name}"

    # def get_absolute_url(self):
    #     return reverse('agent_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)