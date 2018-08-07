from django.test import TestCase
from .models import Neighbourhood, Business, Post, Comments, hooders
from django.contrib.auth.models import User


# Create your tests here.
class NeighborhoodTestClass(TestCase):
    def setUp(self):
        self.new_user = User(username='michael', email='michael@gmail.com')
        self.new_user.save()
        self.Dandora = Neighbourhood(name='Dandora', location='Dandora', occupants=5)
        self.dandora.save()

    def tearDown(self):
        User.objects.all().delete()
        Neighbourhood.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.thome, Neighbourhood))

    def test_save_neighborhood(self):
        self.Dandora.save_neighborhood()
        neighborhood = Neighbourhood.objects.all()
        self.assertTrue(len(neighborhood) > 0)


class BusinessTestClass(TestCase):
    def setUp(self):
        self.new_user = User(username="michael", email="michael@gmail.com")
        self.new_user.save()
        self.Dandora = Neighbourhood(
            name='Dandora', location='Dandora', occupants_count=5, admin=self.new_user)
        self.Dandora.save_neighborhood()
        self.kinyozi = Business(
            name='restaurant', email='michael@gmail.com', user=self.new_user, neighborhood=self.thome)
        self.restaurant.save()

    def tearDown(self):
        User.objects.all().delete()
        Neighbourhood.objects.all().delete()
        Business.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.restaurant, Business))

    def test_save_business(self):
        self.restaurant.save_business()
        business = Business.objects.all()
        self.assertTrue(len(business) > 0)


class PostTestClass(TestCase):
    def setUp(self):
        self.new_user = User(username="michael", email="michael@gmail.com")
        self.new_user.save()
        self.Dandora = Neighbourhood(
            name='Dandora', location='Dandora', occupants_count=5, admin=self.new_user)
        self.Dandora.save_neighborhood()
        self.michael = User(name="michael", user=self.new_user,
                         neighborhood=self.Dandora)
        self.michael.save_user()
        self.new_post = Post(post='I wanna get lit', author=self.michael)

    def tearDown(self):
        User.objects.all().delete()
        Neighbourhood.objects.all().delete()
        User.objects.all().delete()
        Post.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post, Post))

    def test_save_post(self):
        self.new_post.save_post()
        post = Post.objects.all()
        self.assertTrue(len(post) > 0)


class UserTestClass(TestCase):
    def setUp(self):
        self.new_user = User(username="michael", email="michael@gmail.com")
        self.new_user.save()
        self.Dandora = Neighbourhood(
            name='Dandora', location='Dandora', occupants_count=5, admin=self.new_user)
        self.Dandora.save_neighborhood()
        self.michael = User(name="michael", user=self.new_user,
                         neighborhood=self.Dandora)
        self.michael.save()

    def tearDown(self):
        User.objects.all().delete()
        Neighbourhood.objects.all().delete()
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.michael, User))
