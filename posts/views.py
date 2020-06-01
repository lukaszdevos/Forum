from django.shortcuts import render, redirect,get_object_or_404, reverse
from django.http import request, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from django.views import generic
from posts.models import PostModel, CommentsModel, PostModelHistory
from accounts.models import Profile
from django.contrib.auth.models import User
from posts.forms import PostForm, CommentsForm
from django.utils import timezone
from datetime import date, timedelta
import datetime
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




class CreatePost(LoginRequiredMixin,CreateView):
    model = PostModel
    template_name = 'posts/post_create.html'
    fields =  ['topic','text_area']

    def form_valid(self,form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PostsListView(ListView):
    model = PostModel
    template_name = 'posts/post_list.html'
    ordering = ['-pub_date']
    paginate_by = 5
    
    def get_queryset(self,*args, **kwargs):
        
        query = super().get_queryset()
        
        all_post = self.request.GET.get('all_post')
        today = self.request.GET.get('today')
        week = self.request.GET.get('week')
        
        if today:
            return query.filter(pub_date__date=timezone.now())
        elif week:
            return query.filter(pub_date__gte=(timezone.now() - timedelta(days=7)))
        elif all_post:
            return query
        else: 
            return query
                                
def posts_user_listview(request,username):
    user_name = User.objects.get(username=request.user.username)
    context = {'object_list':PostModel.objects.filter(created_by=user_name).order_by('-pub_date'),
               'profile_name':username}
    return render(request, 'posts/post_list.html', context)

class PostDetailView(DetailView):
    model = PostModel
    template_name = 'posts/post_detail.html'
    form_class = CommentsForm

    def get_context_data(self,**kwargs):
        form = CommentsForm()
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(PostModel, pk=self.object.id)
        edited_posts = PostModelHistory.objects.filter(post=self.object.id)
        
        context['comments_list'] = CommentsModel.objects.filter(post=self.object.id)
        context['form'] = form
        context['edited_posts'] = edited_posts
        return context


    def post(self, request, *args, **kwargs):
        form = CommentsForm(request.POST)
        context = {}
        post = self.get_object()

        if form.is_valid():
            add_comment = form.save(commit=False)
            add_comment.created_by = request.user
            add_comment.post = post
            add_comment.save()

            return HttpResponseRedirect(reverse('posts:post_detail', args=[post.id]))

        else:
            form = CommentsForm(request.POST)
            context = {'form':form}

        return self.render_to_response(context=context)


class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = PostModel
    form_class = PostForm
    template_name = 'posts/post_edit.html'

    def form_valid(self,form):
        return super().form_valid(form)
    

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = PostModel
    success_url = '/'


def post_comment_delete(request, post_id, comment_id):
    template_name = 'posts/post_detail.html'
    comment = CommentsModel.objects.get(pk=comment_id)

    if request.method == 'POST':
        if request.user == comment.created_by or request.user.is_staff == True:
            comment.delete()

    return HttpResponseRedirect(reverse('posts:post_detail', args={ post_id }))


def post_comment_edit(request, post_id, comment_id):
    template_name = 'posts/post_detail.html'
    comment = CommentsModel.objects.get(pk=comment_id)
    
    if request.method == 'POST':
        if request.user == comment.created_by or request.user.is_staff == True:
            comment_content = request.POST['comment_content']
            comment.comment_text = comment_content
            comment.save()
    return HttpResponseRedirect(reverse('posts:post_detail', args={ post_id }))



def post_search(request):
    template_name = 'posts/post_list.html'
    post = PostModel.objects.all()
    query = request.GET.get('search_value')


    if query:
        post = post.filter(topic__icontains=query)
        context = {'object_list':post.order_by('-pub_date')}
    else:
        context = {'object_list': {} }

    return render(request, template_name, context)