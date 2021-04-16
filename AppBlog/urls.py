from django.urls import path
from . import views

app_name = 'AppBlog'

urlpatterns = [
  path('', views.BlogList.as_view(),name='bloglist'),
  path('my-blog/',views.UserBlogs.as_view(), name='my_blogs'),
  path('write/',views.CreateBlog.as_view(),name='CreateBlog'),
  path('<slug:slug>/',views.blog_details,name='blog_Details'),
  path('<slug:slug>/edit',views.BlogUpdateView.as_view(),name='blog_Update'),
  path('<slug:slug>/delete',views.BlogDeleteView.as_view(),name='blog_Delete'),
  path('liked/<int:pk>',views.liked,name='liked_post'),
  path('unliked/<int:pk>',views.unliked,name='unliked_post'),
]