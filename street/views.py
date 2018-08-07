from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from .email import send_welcome_email
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
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your instagram account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.''<a href="/accounts/login/"> click here </a>')
    else:
        return HttpResponse('Activation link is invalid!''<br> If you have an account <a href="/accounts/login/"> Log in here </a>')


@login_required(login_url='/accounts/login/')
def index(request):
	'''
	This view function will render the index  landing page
	'''
	if request.user.is_authenticated:
		if hooders.objects.filter(user_id=request.user).exists():
			hood = Neighbourhood.objects.get(pk=request.user.join.hood_id.id)
			posts = Posts.objects.filter(hood=request.user.join.hood_id.id)
			businesses = Business.objects.filter(hood=request.user.join.hood_id.id)
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
def profile(request, username):
    title = "Profile"
    profile = User.objects.get(username=username)
    comments = Comments.objects.all()
    users = User.objects.get(username=username)
    id = request.user.id
    form = CommentForm()

    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)

    images = Image.get_profile_pic(profile.id)
    return render(request, 'profile/profile.html', {'title': title, 'comments': comments, 'profile': profile, 'profile_details': profile_details, 'images': images, 'follow': follow, 'following': following, 'list': mylist, 'people_following': people_following, 'form': form})


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    profile = User.objects.get(username=request.user)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('profile', username=request.user)
    else:
        form = ProfileForm()

    return render(request, 'profile/edit_profile.html', {'form': form, 'profile_details': profile_details})


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
