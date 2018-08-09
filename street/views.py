from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from .forms import SignupForm,NeighbourhoodForm,BusinessForm,PostForm,ProfileForm,CommentsForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Neighbourhood, Business, Profile, hooders, Post, Comments
from django.contrib import messages
# Create your views here.


def signup(request):
	'''
	This view function will implement user signup
	'''
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			messages.success(
				request, 'Success! Signup was a success, now join or create a neighbourhood to start using Kaa Rada')
			return redirect('index')
	else:
		form = SignupForm()
	return render(request, 'registration/signup.html', {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your instagram account.'
#             message = render_to_string('registration/acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = SignupForm()
#     return render(request, 'registration/signup.html', {'form': form})


# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         # return redirect('home')
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.''<a href="/accounts/login/"> click here </a>')
#     else:
#         return HttpResponse('Activation link is invalid!''<br> If you have an account <a href="/accounts/login/"> Log in here </a>')


@login_required(login_url='/accounts/login/')
def index(request):
	'''
	This view function will render the index  landing page
	'''
	if request.user.is_authenticated:
		if hooders.objects.filter(user_id=request.user).exists():
			hood = Neighbourhood.objects.get(pk=request.user.hooders.hood_id.id)
			posts = Post.objects.filter(hood=request.user.hooders.hood_id.id)
			businesses = Business.objects.filter(hood=request.user.hooders.hood_id.id)
			return render(request, 'hood/myhood.html', {"hood": hood, "businesses": businesses, "posts": posts})
		else:
			neighbourhoods = Neighbourhood.objects.all()
			return render(request, 'index.html', {"neighbourhoods": neighbourhoods})
	else:
		neighbourhoods = Neighbourhood.objects.all()
		return render(request, 'index.html', {"neighbourhoods": neighbourhoods})


@login_required(login_url='/accounts/login/')
def comment(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(Image, pk=image_id)
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.image = image
            comment.save()
            return redirect('index')
    else:
        form = CommentForm()

    title = 'Home'
    return render(request, 'index.html', {'title': title})


@login_required(login_url='/accounts/login/')
def home(request):

    title = 'Home'
    return render(request, 'registration/home.html', {'title': title})


@login_required(login_url='/accounts/login/')
def profile(request):
	'''
	This view function will fetch a user's profile
	'''
	profile = Profile.objects.get(user=request.user)
	return render(request, 'registration/profile.html', {"profile": profile})



@login_required(login_url='/accounts/login/')
def edit_profile(request):
	'''
	This view function will edit a profile instance
	'''
	profile = Profile.objects.get(user=request.user)
	if request.method == 'POST':
		form = EditprofileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successful profile edit!')
			return redirect('profile')
	else:
		form = EditprofileForm(instance=profile)
		return render(request, 'registration/edit.html', {"form": form})


@login_required(login_url='/accounts/login/')
def join(request, hoodId):
	'''
	This view function will implement adding 
	'''
	neighbourhood = Neighbourhood.objects.get(pk=hoodId)
	if Join.objects.filter(user_id=request.user).exists():

		Join.objects.filter(user_id=request.user).update(hood_id=neighbourhood)
	else:

		Join(user_id=request.user, hood_id=neighbourhood).save()

	messages.success(
	    request, 'Success! You have succesfully joined this Neighbourhood ')
	return redirect('index')


@login_required(login_url='/accounts/login/')
def business(request):
	'''
	This function will create a Business Instance
	'''
	if Join.objects.filter(user_id=request.user).exists():

		if request.method == 'POST':

			form = CreateBusinessForm(request.POST)
			if form.is_valid():
				business = form.save(commit=False)
				business.user = request.user
				business.hood = request.user.join.hood_id
				business.save()
				messages.success(request, 'Success! You have created a business')
				return redirect('allBusinesses')
		else:
			form = CreateBusinessForm()
			return render(request, 'business/create.html', {"form": form})

	else:

		messages.error(request, 'Error! Join a Neighbourhood to create a Business')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def search(request):
	'''
	View function to retrive searches neighbourhood businesses
	'''
	if request.GET['searchBusiness']:
		search_term = request.GET.get("searchBusiness")
		hood = Neighbourhood.objects.get(pk=request.user.join.hood_id.id)
		posts = Posts.objects.filter(hood=request.user.join.hood_id.id)
		businesses = Business.objects.filter(
		    name__icontains=search_term, hood=request.user.join.hood_id.id)
		message = f"{search_term}"
		return render(request, 'business/search.html', {"message": message, "hood": hood, "businesses": businesses, "posts": posts})

	else:
		message = "You Haven't searched for any item"
		hood = Neighbourhood.objects.get(pk=request.user.join.hood_id.id)
		posts = Posts.objects.filter(hood=request.user.join.hood_id.id)
		return render(request, 'business/search.html', {"message": message, "hood": hood, "posts": posts})



@login_required(login_url='/accounts/login/')
def allBusinesses(request):
	'''
	This post will fetch all business instances belonging to the current logged in user
	'''
	businesses = Business.objects.filter(user=request.user)
	return render(request, 'business/index.html', {"businesses": businesses})


@login_required(login_url='/accounts/login/')
def editBusiness(request, businessId):
	'''
	This view function will edit an instance of a Business
	'''
	business = Business.objects.get(pk=businessId)
	if request.method == 'POST':
		form = CreateBusinessForm(request.POST, instance=business)
		if form.is_valid():
			form.save()
			return redirect('allBusinesses')
	else:
		form = CreateBusinessForm(instance=business)
	return render(request, 'business/edit.html', {"form": form, "business": business})

@login_required(login_url='/accounts/login/')
def hood(request):
	'''
	This view function will create an instance of a neighbourhood
	'''
	if request.method == 'POST':
		form = NeighbourhoodForm(request.POST)
		if form.is_valid():
			hood = form.save(commit=False)
			hood.user = request.user
			hood.save()
			messages.success(
			    request, 'You Have succesfully created a hood.You may now join your neighbourhood')
			return redirect('myHood')

	else:
		form = NeighbourhoodForm()
		return render(request, 'hood/create.html', {"form": form})


@login_required(login_url='/accounts/login/')
def editHood(request, hood_id):
	'''
	This view function will edit an instance of a neighbourhood
	'''
	neighbourhood = Neighbourhood.objects.get(pk=hood_id)
	if request.method == 'POST':
		form = CreateHoodForm(request.POST, instance=neighbourhood)
		if form.is_valid():
			form.save()
			messages.success(request, 'Success! You Have succesfully edited your hood')

			return redirect('myHood')
	else:
		form = CreateHoodForm(instance=neighbourhood)
		return render(request, 'hood/edit.html', {"form": form, "neighbourhood": neighbourhood})

def hoodHome(request):
	'''
	This function will retrive instances of a neighbourhood
	'''
	hoods = Neighbourhood.objects.filter(user=request.user)
	return render(request, 'hood/index.html', {"hoods": hoods})


@login_required(login_url='/accounts/login/')
def exitHood(request, hoodId):
	'''
	This function will delete a neighbourhood instance in the join table
	'''
	if Join.objects.filter(user_id=request.user).exists():
		Join.objects.get(user_id=request.user).delete()
		messages.error(request, 'You have succesfully exited this Neighbourhood.')
		return redirect('index')


def myPosts(request):
	'''
	View functions to retrieve all post instances belonging to a logged in user
	'''
	myPosts = Posts.objects.filter(user=request.user)
	return render(request, 'posts/index.html', {"myPosts": myPosts})

def allPosts(request):
    '''
    view function to retrive all post instances belonging to a neighbourhood
    '''
    allPosts=Posts.objects.filter(hood)
    return render(request, 'posts/neigh.html', {"allPosts":allPosts})
@login_required(login_url='/accounts/login/')
def createPost(request):
	'''
	This function will create a Posts instance
	'''
	if Join.objects.filter(user_id=request.user).exists():
		if request.method == 'POST':
			form = ForumPostForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				post.user = request.user
				post.hood = request.user.join.hood_id
				post.save()
				messages.success(request, 'You have succesfully created a Forum Post')
				return redirect('index')
		else:
			form = ForumPostForm()
			return render(request, 'posts/create.html', {"form": form})
	else:
		messages.error(
		    request, 'Error! You can only create a forum post after Joining/Creating a neighbourhood')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def changeHood(request):
	'''
	View function to retrieve hood resources incase a user wants to change their current neighbourhood
	'''
	neighbourhoods = Neighbourhood.objects.all()
	return render(request, 'hood/joinhood.html', {"neighbourhoods": neighbourhoods})


