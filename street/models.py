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


class Resident(models.Model):
    user = models.OneToOneField(User, related_name='resident', null=True)
    suburb = models.ForeignKey(Suburb, related_name="residency", null=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("suburb", "user")

    # Create Resident Profile when creating a User
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Resident.objects.create(user=instance)
        instance.resident.save()


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", null=True)
    image = models.ImageField(upload_to='post_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    topic = models.ForeignKey(
        Topic, related_name="posts", null=True, blank=True)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "single_post",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]


class Comments(models.Model):
    comment = models.CharField(max_length=300)
    posted_on = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def get_comments_by_images(cls, id):
        comments = Comments.objects.filter(image__pk=id)
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

