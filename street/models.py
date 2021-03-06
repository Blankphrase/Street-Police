from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime as dt

# Create your models here.

class Neighbourhood(models.Model):
    """
    Model for neighbourhood
    """
    NAIROBI_HOODS=(
        ('Dandora','Nairobi'),
        ('Mathare','Nairobi'),
        ('Githurai','Nairobi'),
        ('Kayole','Nairobi'),
        ('Donholm','Nairobi'),
        ('Hurlingham','Nairobi'),
        ('Ngara','Nairobi'),
        ('Huruma','Nairobi'),
        ('Kawangware','Nairobi'),
        ('Kibera','Nairobi'),
        ('Kariobangi','Nairobi'),
        ('Kileleshwa','Nairobi'),
        ('Rongai','Nairobi'),
        ('Umoja','Nairobi'),
        ('Karen','Nairobi'),
        ('South B & C','Nairobi'),
        ('Langata','Nairobi'),
        ('Pangani','Nairobi'),
        ('Roysambu','Nairobi'),
    )
    user = models.OneToOneField(User, related_name='Neighbourhood', null=True)
    name = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=100, choices=NAIROBI_HOODS)
    population=models.IntegerField()
    
    def __str__(self):
        return self.name

    def save_hood(self):
        self.save()

    @classmethod
    def search_hood(cls,search_term):
        hoods=cls.objects.filter(name__icontains=search_term)
        return hoods


class Profile(models.Model):
    '''
    Model that creates the profile logic
    '''

    user = models.OneToOneField(User, related_name='profile', null=True, on_delete=models.CASCADE)
    hood = models.ForeignKey(Neighbourhood, related_name="neighbourhood", null=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    bio = models.TextField(max_length=500, default="I love my hood")
    
    def __str__(self):
        return self.user

    class Meta:
        unique_together = ("hood", "user")

    # Create Resident Profile when creating a User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", null=True)
    image = models.ImageField(upload_to='post_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    message = models.TextField()
    topic = models.CharField(max_length=300)
    hood=models.ForeignKey(Neighbourhood)


    def __str__(self):
        return self.topic

    def save_post(self):
        self.save()


class Comments(models.Model):
    '''
    Model to handle the comments logic
    '''

    comment = models.CharField(max_length=300)
    posted_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_comment(self):
        self.save()

    @classmethod
    def get_comments_by_posts(cls, id):
        comments = Comments.objects.filter(post__pk=id)
        return comments


class Business(models.Model):
	'''
	Model class that creates the Business logic
	'''
	name = models.CharField(max_length=300)
	description = models.TextField()
	email_address = models.EmailField()
	user = models.ForeignKey(User)
	hood = models.ForeignKey(Neighbourhood)

	def __str__(self):
		return self.name

	def save_business(self):
		self.save()

	@classmethod
	def search_business(cls, search_term):
		business = cls.objects.filter(name__icontains=search_term)
		return business

    

class hooders(models.Model):
	'''
	Model that keeps track of what user has joined what neighbourhood
	'''
	user_id = models.OneToOneField(User)
	hood_id = models.ForeignKey(Neighbourhood)

	def __str__(self):
		return self.user_id
