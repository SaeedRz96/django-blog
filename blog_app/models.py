from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from bs4 import BeautifulSoup
import os


# you should set max_length for CharFileds if you use Django<4 or SQLite

class Blog(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    authers = models.ManyToManyField(User, related_name='blog_writers')
    title = models.CharField()
    slug = models.CharField(unique=True)
    logo = models.ImageField(upload_to='blog/logos/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/blog/{self.slug}/'

    def get_posts(self):
        return Post.objects.filter(blog=self)
    
    def get_posts_count(self):
        return self.get_posts().count()

    def save(self, *args, **kwargs):
        # delete old logo file from storage when blog is updated
        try:
            this = Blog.objects.get(id=self.id)
            if this.logo != self.logo:
                this.logo.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # delete logo file from storage when blog is deleted
        self.logo.delete()
        super().delete(*args, **kwargs)


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField()
    slug = models.CharField(unique=True)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/post/{self.slug}/'
    
    def save(self, *args, **kwargs):
        # delete old uploaded files from storage when post is updated
        try:
            this = Post.objects.get(id=self.id)
            if this.content != self.content:
                soup = BeautifulSoup(this.content, 'html.parser')
                page_images = [image["src"] for image in soup.findAll("img")]
                for image in page_images:
                    image = image[1:]
                    os.remove(image)
        except:
            pass
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # delete uploaded files from storage when post is deleted
        try:
            soup = BeautifulSoup(self.content, 'html.parser')
            page_images = [image["src"] for image in soup.findAll("img")]
            for image in page_images:
                image = image[1:]
                os.remove(image)
        except:
            pass
        super().delete(*args, **kwargs)