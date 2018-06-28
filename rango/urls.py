from django.conf.urls import url
from rango import views

urlpatterns = [
               url(r'^$',  views.index, name='index'),
               url(r'^about',  views.about_page, name='about'),
               url(r'^add_category/$', views.add_cat, name='add_cat'),
               url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
               url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_cat, name='category'),
               url(r'^rango/goto/$', views.track_url, name='goto'),
               url(r'^search/$', views.mod_cat, name='search'),
               url(r'^profiles/', views.list_profiles, name='profiles'),
               url(r'^register_profile/$', views.register_profile, name='register_profile'),
               url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
               url(r'^like_category/', views.like_category, name='like_category'),
               url(r'^dislike_category/', views.dislike_category, name='dislike_category'),
               url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),

               ]
