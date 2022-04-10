import uuid

from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.settings import EMAIL_HOST_USER, DEFAULT_FROM_EMAIL


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    release_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    extract = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to="media/posts/images/%Y/%m")
    content = models.TextField()
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Email(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


@receiver(post_save, sender=Email)
def post_save_send_email(sender, instance, **kwargs):
    name =instance.name
    email = instance.email
    message = instance.message

    send_mail(
    f'Email from tech blog: sended by {name}',
    f'Message:\n{message} - sended from {email}',
    from_email=DEFAULT_FROM_EMAIL,
    recipient_list=[EMAIL_HOST_USER],
    fail_silently=False,
)
