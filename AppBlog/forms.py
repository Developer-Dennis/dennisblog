from django import forms
from AppBlog.models import Blog, Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', )
