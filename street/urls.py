from django.conf.urls import url
from django.conf import settings
from . import views
from django.conf.urls.static import static


urlpatterns = [
    url('^$', views.index, name='index'),
    url('^home/', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^user/(?P<username>\w+)', views.profile, name='profile'),
    url(r'^accounts/edit/', views.edit_profile, name='editprofile'),
    url(r'^comment/(?P<post_id>\d+)', views.comment, name='comment'),
    url(r'^hood/$', views.hood, name='hood'),
    url(r'^join/(\d+)', views.join, name='join'),
    url(r'^exitHood/(\d+)', views.exitHood, name='exitHood'),
    url(r'^myHood/$', views.hoodHome, name='hoodHome'),
    url(r'^business/$', views.business, name='business'),
    url(r'^allBusinesses/$', views.allBusinesses, name='allBusinesses'),
    url(r'^searchBusiness/$', views.search, name='search'),
    url(r'^createPost/$', views.createPost, name='createPost'),
    url(r'^allPosts/$',views.allPosts, name='allPosts'),
    url(r'^myPosts/$', views.myPosts, name='myPosts'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
