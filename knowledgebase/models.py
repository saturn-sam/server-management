from authentication.models import CustomUser
from django.db import models
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q
import random
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
import readtime

from django.conf import settings
from serverinfo.models import RunningServices

# Create your models here.
class KBTopic(models.Model):
    title = models.CharField(max_length=255,blank=False)
    slug = models.SlugField(max_length = 255, editable=False,)
    delete_status = models.IntegerField(blank=False, default=0)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="kbtopic_deleted_by_user")


    def __str__(self):
        return self.slug
    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

STATUS_CHOICES = ( 
   ('draft', 'Draft'), 
   ('published', 'Published'), 
   ('protected', 'Protected'), 
) 
  
class KnowledgeBase(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250, editable=False,)
    related_service = models.ManyToManyField(RunningServices, blank=True)
    body = RichTextUploadingField(blank=False, null=False)
    topic = models.ForeignKey(KBTopic, on_delete=models.CASCADE)
    tags = TaggableManager()
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default ='draft')
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_with', blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    delete_status = models.IntegerField(blank=False, default=0)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="knowledgebase_deleted_by_user")


    def __str__(self):
        return self.slug

    @staticmethod
    def rand_color():
        color = "#%06x" % random.randint(0, 0xFFFFFF)
        return color


    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        #return reverse("post-details", kwargs=kwargs)
        return reverse("add-kb")

    def get_readtime(self):
        result = readtime.of_text(self.body)
        return result.text 

    def save(self, *args, **kwargs):
        # def unique_slugify(slug):
        #     # model = instance.__class__
        #     unique_slug = slug
        #     while KnowledgeBase.objects.filter(slug=unique_slug).exists():
        #         unique_slug = get_random_string(length=4).lower() + "-" + slug
        #     return unique_slug
        # # value = self.title
        # pre_slug = slugify(self.title)
        # # self.slug = slugify(value, allow_unicode=True)
        # self.slug = unique_slugify(pre_slug)
        value = self.title
        self.slug = slugify(value, allow_unicode=True)

        super().save(*args, **kwargs)

    @property
    def views_count(self):
        return KBViews.objects.filter(kb=self).count()


    def users_except_shared(self):
        # return self.shared_with.all().values('id')
        # return CustomUser.objects.filter(is_active = True).exclude(id = self.author.id).exclude(id__in=self.shared_with.all().values('id'))
        print(CustomUser.objects.filter(is_active = True).exclude(id = self.author.id).exclude(id__in=self.shared_with.all().values('id')))
        return CustomUser.objects.filter(is_active = True).exclude(id = self.author.id).exclude(id__in=self.shared_with.all().values('id'))


class Comment(models.Model):
    kb = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    reply = models.ForeignKey('Comment', null=True, blank=True, related_name='replies', on_delete=models.DO_NOTHING)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return '{}-{}' . format(str(self.kb), str(self.username))
    @property
    def user_full_name(self):
        if self.username:
            return self.username.get_full_name()
        else:
            return self.nickname

class KBViews(models.Model):
    IPAddres= models.GenericIPAddressField(default="0.0.0.0")
    kb = models.ForeignKey('KnowledgeBase', on_delete=models.CASCADE)
    created = models.DateTimeField( auto_now=True )

    def __str__(self):
        return '{0} in {1} kb'.format(self.IPAddres,self.kb.title)