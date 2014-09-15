from django.shortcuts import render
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import RequestContext
from models import UserProfile
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from gallery.models import Artwork,Category
from gallery.gallery_form import CategoryForm, ArtworkForm
from django.contrib.auth.decorators import login_required

@login_required
def add_category(request):

  if not request.user.is_authenticated():
    return HttpResponseRedirect('base/login')
  c = {}
  c.update(csrf(request))

  if request.method == "POST":
    form = CategoryForm(request.POST, request.FILES)

    if form.is_valid():
      category = form.save(commit=False)
      profile_owner = UserProfile.objects.get(user__username__contains=request.user.username)
      category.owner = profile_owner
      
      category.save()
      # return HttpResponseRedirect("/") 
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      # return HttpResponse(profile_owner.user.username) 
      
    # return HttpResponse("invalid form")
  else:
    form = CategoryForm()
  
  not_working = "not working"
  return render(request, 'gallery/add_category.html', 
    {
    "form" : form, 
    "token" : c, 
    })

def category_view(request,owner,category):
  artworks = Artwork.objects.filter(category__pk = category)
  return render_to_response("gallery/category_view.html", {'artworks' : artworks})

@login_required
def add_artwork(request, category_id=0):

  if not request.user.is_authenticated():
    return HttpResponse('You are not allowed to add here :/ !')
  category = get_object_or_404(Category,  pk=category_id)
  owner = get_object_or_404(Category,  pk=category_id).owner

  if request.user.username is owner.user.username:
    return HttpResponse(str(request.user.username) + str(owner.user.username))
  c = {}
  c.update(csrf(request))

  if request.method == "POST":
    form = ArtworkForm(request.POST, request.FILES)

    if form.is_valid():
      artwork = form.save(commit=False)

      artwork.category = category
      artwork.owner = category.owner
      
      artwork.save()
      # return HttpResponseRedirect("/") 
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      # return HttpResponse(profile_owner.user.username) 
      
    # return HttpResponse("invalid form")
  else:
    form = ArtworkForm()
  
  return render(request, 'gallery/add_artwork.html', 
    {
    "form" : form, 
    "token" : c,
    "category" : category
    })