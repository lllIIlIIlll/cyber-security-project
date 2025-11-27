from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden

from .models import BlogPost

# Create your views here.
def index(request):
  blog_posts = BlogPost.objects.order_by('-created_at')
  return render(request, 'blog/index.html', {'blog_posts': blog_posts})

@login_required
#-------------------------------------------------------
# Comment out the line below to fix the csrf flaw
@csrf_exempt
#-------------------------------------------------------
def create_post(request):
  if request.method == 'POST':
    content = request.POST.get('content')
    author = request.user

    BlogPost.objects.create(
      content = content,
      author = author
    )
  return redirect(index)

@login_required
def delete_post(request, post_id):
  if request.method == 'POST':
    user = request.user
    post = BlogPost.objects.get(id=post_id)
    #---------------------------------------------------
    # Uncomment the check below to fix the broken access control flaw
    #if post.author != user and not user.is_superuser:
    #  return HttpResponseForbidden("Not allowed")
    #---------------------------------------------------

    post.delete()
    
  return redirect(index)