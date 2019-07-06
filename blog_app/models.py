from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug  = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category,self).save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])


class PostManager(models.Manager):
    def get_queryset(self):
        return super(PostManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    category  = models.ForeignKey('Category',related_name='blog_posts1', on_delete=models.CASCADE)
    author    = models.ForeignKey(User, related_name='blog_posts2',on_delete=models.CASCADE)
    image     = models.ImageField(upload_to='post_img/')
    title     = models.CharField(max_length=250)
    slug      = models.SlugField(blank=True, null=True)
    body      = models.TextField()
    publish   = models.DateTimeField(default=timezone.now)
    created   = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)
    status    = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    objects   = models.Manager()
    published = PostManager()
    tags      = TaggableManager()

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Post,self).save(*args,**kwargs)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', args=[self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])
    
class InstgramFeeds(models.Model):
    img = models.ImageField(upload_to='instagram-feeds/')
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    post    = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name    = models.CharField(max_length=80)
    email   = models.EmailField()
    body    = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active  = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return "Comment by {} on {}".format(self.name,self.post)