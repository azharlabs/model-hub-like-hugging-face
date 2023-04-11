import uuid

from hitcount.models import HitCountMixin, HitCount
from ckeditor_uploader.fields import RichTextUploadingField 
from taggit.managers import TaggableManager
from markdown2 import markdown

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_save

from .utils import get_read_time

User._meta.get_field('email')._unique = True


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


class Post(models.Model, HitCountMixin):
    
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')
            
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('hidden', 'Hidden'),
    )

    
    # id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False, db_index=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    
    body = RichTextUploadingField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    favourites = models.ManyToManyField(
        User, related_name='favourite', default=None, blank=True)
    category = models.CharField(max_length=250, default='uncategorized')
    newmanager = PublishedManager()  # custom manager

    thumbsup = models.IntegerField(default='0')
    thumbsdown = models.IntegerField(default='0')
    thumbs = models.ManyToManyField(User, related_name='thumbs', default=None, blank=True)
    
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')
    tags = TaggableManager() 

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
    
    objects = models.Manager() # The default manager.
    read_time =  models.IntegerField(default=0)
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.slug])

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

    def get_markdown(self):
        content = self.body
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

def pre_save_post_receiver(sender, instance, *args, **kwargs):

    if instance.body:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=Post)


class Vote(models.Model):

    post = models.ForeignKey(Post, related_name='postid',
                             on_delete=models.CASCADE, default=None, blank=True)
    user = models.ForeignKey(User, related_name='userid',
                             on_delete=models.CASCADE, default=None, blank=True)
    vote = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user) 

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    name=models.CharField(max_length=50)
    email=models.EmailField()
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
        