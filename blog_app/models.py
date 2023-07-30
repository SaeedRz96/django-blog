from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from bs4 import BeautifulSoup
import os
from taggit.managers import TaggableManager



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

    @property
    def subscribers(self):
        return Subscriber.objects.filter(blog=self)

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
    tags = TaggableManager()

    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title
    
    @property
    def absolute_url(self):
        return f'/post/{self.slug}/'
    
    @property
    def comments(self):
        return Comment.objects.filter(post=self)
    
    @property
    def likes(self):
        return Like.objects.filter(post=self).count()

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
        # save new tags in tags table
        for tag in self.tags.all():
            try:
                Tag.objects.get(name=tag.name)
            except:
                Tag.objects.create(name=tag.name)
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

    @property
    def likes(self):
        return LikeComment.objects.filter(comment=self).count()

    @property
    def replies(self):
        return Comment.objects.filter(reply_to=self)
    
    @property
    def likers(self):
        return [like.user for like in LikeComment.objects.filter(comment=self)]
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


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f'{self.user} on {self.post}'
    
    def save(self, *args, **kwargs):
        # check if user is subscribed to this blog or blog is not private
        if self.post.blog.is_private:
            if not self.post.blog.subscribers.filter(user=self.user).exists():
                raise Exception('This blog is private. make request to subscribe.')
        super().save(*args, **kwargs)


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Like Comments'

    def __str__(self):
        return f'{self.user} on {self.comment}'
    
    def save(self, *args, **kwargs):
        # check if user is subscribed to this blog or blog is not private
        if self.comment.post.blog.is_private:
            if not self.comment.post.blog.subscribers.filter(user=self.user).exists() and self.comment.post.blog.owner != self.user and self.comment.post.author != self.user:
                raise Exception('This blog is private. make request to subscribe.')
        super().save(*args, **kwargs)


class SavedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Saved Posts'

    def __str__(self):
        return f'{self.user} on {self.post}'
    
    def save(self, *args, **kwargs):
        # check if user is subscribed to this blog or blog is not private
        if self.post.blog.is_private:
            if not self.post.blog.subscribers.filter(user=self.user).exists() and self.post.blog.owner != self.user and self.post.author != self.user:
                raise Exception('This blog is private. make request to subscribe.')
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def posts(self):
        return Post.objects.filter(tags__name=self.name)
    
    @property
    def posts_count(self):
        return self.posts.count()
    
    @property
    def followers(self):
        return [follow.user for follow in FollowTag.objects.filter(tag=self)]
    
    @property
    def followers_count(self):
        return len(self.followers)
    
    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name
    

class FollowTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Follow Tags'

    def __str__(self):
        return f'{self.user} on {self.tag}'


class Report(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    report_type = models.CharField(choices=[('abusive', 'Abusive'), ('spam', 'Spam'), ('inappropriate', 'Inappropriate'),('advertising', 'Advertising'), ('other', 'Other')], default='other')
    description = models.TextField(blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')

    class Meta:
        verbose_name_plural = 'Reports'

    def __str__(self):
        return f'{self.user} on {self.post}'


class Series(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, related_name='series_posts', blank=True, null=True)
    title = models.CharField()
    slug = models.CharField(unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Series'

    def __str__(self):
        return self.title

    @property
    def absolute_url(self):
        return f'/series/{self.slug}/'
    
    @property
    def posts_count(self):
        return self.posts.count()
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        super().save(*args, **kwargs)
