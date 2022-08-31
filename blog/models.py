from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')

class DraftManager(models.Manager):
	def get_queryset(self):
		return super(DraftManager, self).get_queryset().filter(status='draft')

class BodyAManager(models.Manager):
	def get_queryset(self):
		return super(BodyAManager, self).get_queryset().filter(body__startswith='A')

class Post(models.Model):
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
	)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	author = models.ForeignKey(User,
		on_delete=models.CASCADE,
		related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,
		choices=STATUS_CHOICES,
		default='draft')

	def __str__(self): # this makes it so that the representation of the object itself shows as a string (the title of the post)
		return self.title
	
	def get_absolute_url(self):
		return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

	class Meta:
		ordering = ('-publish',)

	objects = models.Manager()
	published = PublishedManager() # like a custom manager like .objects but can be called and using the code in the return statement
									# in PublishedManager - can now call like Post.published.filter(<whatever>) and will get
									# all results that are published instead of all results together
	draft = DraftManager()
	body_starts_with_a = BodyAManager()

	tags = TaggableManager()

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return f"Comment by {self.name} on {self.post}"






