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
    
    @property
    def absolute_url(self):
        return f'/blog/{self.slug}/'

    @property
    def posts(self):
        return Post.objects.filter(blog=self)
    
    @property
    def posts_count(self):
        return self.posts.count()

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
    
    @property
    def absolute_url(self):
        return f'/post/{self.slug}/'
    
    def save(self, *args, **kwargs):
        # check if author is in blog authers
        if self.author not in self.blog.authers.all():
            raise Exception('Author is not in blog authers')
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


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.author} on {self.post}'
    
    def save(self, *args, **kwargs):
        # check reply_to is in post comments
        if self.reply_to:
            if self.reply_to.post != self.post:
                raise Exception('Reply to is not in post comments')
        super().save(*args, **kwargs)


class Subscriber(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Subscribers'

    def __str__(self):
        return f'{self.user} on {self.blog}'
    

class SubscribeRequest(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Subscribe Requests'

    def __str__(self):
        return f'{self.user} on {self.blog}'
    
    def save(self, *args, **kwargs):
        # check subscribe request for only private blogs
        if not self.blog.is_private:
            raise Exception('Blog is not private')
        # check if user is in blog authers or owner
        if self.user not in self.blog.authers.all() and self.user != self.blog.owner:
            # check if user is already requested
            try:
                SubscribeRequest.objects.get(blog=self.blog, user=self.user)
                raise Exception('User is already requested')
            except:
                pass
            # check if user is already subscribed
            try:
                Subscriber.objects.get(blog=self.blog, user=self.user)
                raise Exception('User is already subscribed')
            except:
                if self.status == 'accepted':
                    # create subscriber
                    Subscriber.objects.create(blog=self.blog, user=self.user)
                    self.is_deleted = True
                elif self.status == 'rejected':
                    self.is_deleted = True
                super().save(*args, **kwargs)
            