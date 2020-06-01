from django import forms
from posts.models import PostModel,CommentsModel


class PostForm(forms.ModelForm):
    
    class Meta:
        model = PostModel
        fields =  ['topic','text_area']
        
class CommentsForm(forms.ModelForm):
    
    class Meta:
        model = CommentsModel
        fields = ['comment_text']