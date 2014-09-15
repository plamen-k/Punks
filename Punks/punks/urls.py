from django.conf.urls import patterns, include, url
from django.shortcuts import redirect
from django.contrib import admin
from django.contrib.auth.views import login

admin.autodiscover()

urlpatterns = patterns('',

# Examples:
  url(r'^home/', 'home.views.home', name='home'),

# admin url

  url(r'^admin/', include(admin.site.urls)),
  url(r'^$', 'home.views.home', name='home_2'),

# user authentication links
  # user authentication links
  url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'home/login_form.html'}, name="login_authentication"),
  url(r'^logout/', 'django.contrib.auth.views.logout', ),
  url(r'^accounts/login/$', login, {'template_name': 'home/login_form.html'}),
  
# article urls
  url(r'^publishing/articles/edit/(?P<id>\d+)/$', 'article.views.edit', {}, 'article_edit'),
  url(r'^publishing/articles/delete/(?P<id>\d+)/$', 'article.views.delete', {}, 'article_delete'),
  url(r'^publishing/(?P<type>\w+)/add/$', 'article.views.add_article', name='add_article'),
  url(r'^publishing/(?P<name>\w+)/articles/(?P<article_id>\d+)', 'article.views.full_article', name='fullArticle'),
  url(r'^publishing/(?P<name>\w+)/(?P<type>\w+)/', 'article.views.articles', name='articles'),

    

# profiles url
  url(r'^profile/(?P<owner>\w+)/', 'home.views.profile_edit', name='profile_edit'),
  url(r'(?P<owner>\w+)/$', 'home.views.profile', name='profile'),

# Gallery url
  
  url(r'(?P<owner>\w+)/gallery/(?P<category>\d+)', 'gallery.views.category_view', name='category_view'),
  url(r'gallery/category/add', 'gallery.views.add_category', name='add_category'),
  url(r'gallery/(?P<category_id>\d+)/add', 'gallery.views.add_artwork', name='add_artwork'),

)
