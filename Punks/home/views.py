from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from ProfileUser import UserForm
from models import UserProfile
from gallery.models import Category
from gallery.models import Artwork
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from article.models import Article
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
import re
# Create your views here.

def home(request):
	profile = UserProfile.objects.all()[:6]
	return render_to_response("home/home.html", {"profiles" : profile , "the_user" : request.user})

@login_required   # Login required takes care of unauthed pages

def profile_edit(request, owner):

  # CSRF token for form validation, a must have :)
  c = {}
  c.update(csrf(request))

  if owner:
      user_profile = get_object_or_404(UserProfile, user__username = owner)

      # the if statements just added for sanity
      if str(user_profile.user) != str(request.user):
          # return HttpResponse("You don't have the right to edit [30]")
          return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  else: # if the profile is unposted, repopulate id
      user_profile = UserForm(user=request.user)

  if request.POST:
      form = UserForm(request.POST, request.FILES, instance=user_profile)
      if form.is_valid():
          form.save()

          # If the save was successful, redirect to another page
          return HttpResponse('save successful[40]')

  else:
      form = UserForm(instance=user_profile)

  return render(request, 'home/profile_page.html', {
      'form': form,
      'owner' : owner, # owner is passed from the url, because a url that doesnt work throws 404
      'the_user' : request.user,
      'token' : c,
  }, context_instance=RequestContext(request))

def profile(request, owner):

  try:
    profile_owner = UserProfile.objects.get(user__username=owner)
    images = Artwork.objects.filter(owner=profile_owner)
    categories = Category.objects.filter(owner=profile_owner)
  except ObjectDoesNotExist:
    return HttpResponseRedirect("Object does not exist")

  articles = Article.objects.filter(owner__user__username__contains=owner).filter(is_project=False).order_by('-created_at')
  projects = Article.objects.filter(owner__user__username__contains=owner).filter(is_project=True).order_by('-created_at')

  return render_to_response('home/profile.html', 
    {'owner' : profile_owner, 
    'the_user' : request.user, 
    'images' : images, 
    'categories' : categories,
    'articles' : articles,
    'projects' : projects,
    })


def login_user(request, template_name='home/login_form.html'):
  c = {}
  c.update(csrf(request))
 
  if request.POST:
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)


    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/home/')
        else:
            # Return a 'disabled account' error message
            return render(request, template_name, {'error': 'disabled account'})
    else:
        # Return an 'invalid login' error message.
        return render(request, template_name, {'error': 'invalid login'})
  else:
    return render(request, 'home/login_form.html', {
      'the_user' : request.user,
      'token' : c,
      'request' : "unimplemented",
  }, context_instance=RequestContext(request))