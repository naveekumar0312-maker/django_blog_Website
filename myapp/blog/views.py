from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Post,AboutUs
from django.http import Http404
from .forms import ContactForm
from .models import Contact
# Create your views here.
#Static demo data
# posts = [
#         {'id':1,'title':'post 1','content':'content of post 1'},
#         {'id':2,'title':'post 2','content':'content of post 2'},
#         {'id':3,'title':'post 3','content':'content of post 3'},
#         {'id':4,'title':'post 4','content':'content of post 4'},
#         {'id':5,'title':'post 5','content':'content of post 5'},
#         {'id':6,'title':'post 6','content':'content of post 6'},
# ]

def index(request):
    blog_title = "Latest Posts"
    # getting data from post model
    posts = Post.objects.all()
    return render(request,'blog/index.html',{'blog_title':blog_title,'posts':posts})
def detail(request,post_id):
    #static data
    # post = next((item for item in posts if item['id'] == int(post_id)), None)
    # getting data from model by post id
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("post does not exist")
    return render(request,'blog/detail.html',{'post':post})
def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))
def new_url_view(request):
    return HttpResponse("this is the new url")

def contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
       # Manually save to DB
        Contact.objects.create(
          name=form.cleaned_data['name'],
          email=form.cleaned_data['email'],
          message=form.cleaned_data['message']
        )
        success_message = 'Your message has been saved in the database!'
        return render(request, 'blog/contact.html',{
           'form': ContactForm(),  # reset form
           'success_message': success_message
        })

    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})
def about(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Default content goes here."
    else:
        about_content = about_content.content

    return render(request,'blog/about.html',{'about_content':about_content})
