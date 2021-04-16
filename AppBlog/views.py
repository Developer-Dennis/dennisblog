from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import CreateView,UpdateView,ListView,DetailView,TemplateView,DeleteView
from .models import Blog,Comment,Likes
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from AppBlog.forms import CommentForm

# Create your views here.

class UserBlogs(LoginRequiredMixin,ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'AppBlog/myBlogs.html'

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user).order_by('-publish_date')
    
    



class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'AppBlog/bloglist.html'

    def get_queryset(self):
        return Blog.objects.order_by('-publish_date')
    
   

   
class CreateBlog(LoginRequiredMixin,CreateView):
    model = Blog
    template_name = 'AppBlog/createBlog.html'
    fields =  ('blog_title','blog_content','blog_image')
    
    def form_valid(self,form):
            blog_obj = form.save(commit=False)
            blog_obj.author = self.request.user
            title = blog_obj.blog_title
            blog_obj.slug = title.replace(" ","-")+ "-"+str(uuid.uuid4())
            blog_obj.save()
            return HttpResponseRedirect(reverse('index'))


class BlogUpdateView(UpdateView):
    model = Blog
    template_name = "AppBlog/editBlog.html"
    fields =  ('blog_title','blog_content','blog_image')

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = "AppBlog/delete.html"
    success_url = reverse_lazy('AppBlog:my_blogs')



@login_required
def blog_details(request,slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(blog=blog,user=request.user)
    if already_liked:
        liked = True
    else:
        liked = False

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('AppBlog:blog_Details',kwargs={'slug':slug}))
    return render(request, 'AppBlog/blogDetails.html' ,context={'blog':blog,'comment_form':comment_form,'liked':liked})


@login_required
def liked(request,pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog,user=user)
    if not already_liked:
        liked_post = Likes(blog=blog,user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('AppBlog:blog_Details',kwargs={'slug':blog.slug}))




@login_required
def unliked(request,pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog,user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('AppBlog:blog_Details',kwargs={'slug':blog.slug}))

    