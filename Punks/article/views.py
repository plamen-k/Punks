from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.template import RequestContext
from models import UserProfile
from django.core.context_processors import csrf
from home.login_form import UserLoginForm
from article.models import Article
from django.contrib.auth.decorators import login_required
from article_edit_form import EditForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def articles(request, name="", type=""):
  if type=="articles":
    articles = Article.objects.filter(owner__user__username__contains=name).filter(is_project=False).order_by('-created_at')
  else:
    articles = Article.objects.filter(owner__user__username__contains=name).filter(is_project=True).order_by('-created_at')

  paginator = Paginator(articles, 15)
#  creates the pagination
  page = request.GET.get('page')
  try:
      content = paginator.page(page)
  except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      content = paginator.page(1)
  except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      content = paginator.page(paginator.num_pages)

  profile_owner = UserProfile.objects.get(user__username=name)

  return render_to_response('article/articles.html', 
    {"articles" : articles, 
    "the_user" : request.user, 
    "owner" : profile_owner,
    "content" : content,
    "type" : type,
    } )

def edit(request, id=None):
  if not request.user.is_authenticated():
    return HttpResponse("not logged int")

  c = {}
  c.update(csrf(request))

  if id:
      article = get_object_or_404(Article, pk=id)
      if str(article.owner) != str(request.user):
          return HttpResponseRedirect("/")
  else:
      article = Article(author=request.user)

  if request.POST:
      form = EditForm(request.POST, request.FILES, instance=article)
      if form.is_valid():
          form.image = request.POST.get('image', False)
          form.save()

          # If the save was successful, redirect to another page
          return HttpResponseRedirect('/')

  else:
      form = EditForm(instance=article)

  return render(request, 'article/edit_article.html', {
      'form': form,
      'article_id' : id,
      'the_user' : request.user,
      'token' : c,
  }, context_instance=RequestContext(request))

@login_required
def delete(request, id=None):
  if not request.user.is_authenticated():
    return HttpResponse("not logged int")

  if id:
      article = get_object_or_404(Article, pk=id)
      if article.owner.user.username == request.user.username:
        article.delete()
        return render_to_response("article/deleted_message", {"article" : article})

      return HttpResponseRedirect("/")
  else:
      HttpResponse("Action cannot be performed")

def full_article(request, name, article_id):
  article = Article.objects.get(pk=article_id)
  return render_to_response("article/full_article.html", {'article' : article, "the_user" : request.user})


def add_article(request, type):

  if not request.user.is_authenticated():
    return HttpResponseRedirect('base/login')
  c = {}
  c.update(csrf(request))

  if request.method == "POST":
    form = EditForm(request.POST, request.FILES)

    if form.is_valid():
      article = form.save(commit=False)
      profile_owner = UserProfile.objects.get(user__username__contains=request.user.username)
      article.owner = profile_owner
      if type=="article":
        article.is_project = False
      else:
        article.is_project = True
      article.save()
      # return HttpResponseRedirect("/") 
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      # return HttpResponse(profile_owner.user.username) 
      
    # return HttpResponse("invalid form")
  else:
    form = EditForm()
  
  not_working = "not working"
  return render(request, 'article/add_article.html', 
    {"form" : form, 
    "token" : c, 
    "working" : not_working,
    "type" : type,
    })
