from django.urls import path, re_path
from posts import views

app_name='posts'

urlpatterns = [
    path('post/create/',views.CreatePost.as_view(),name='post_create'),
    path('post/',views.PostsListView.as_view(template_name='posts/post_list.html'),name='post_list'),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
    path('post/<pk>/edit/',views.PostUpdateView.as_view(),name='post_update'),
    path('post/<pk>/delete/',views.PostDeleteView.as_view(template_name = 'posts/post_delete_confirm.html'),name='post_delete'),
    path('post/<int:post_id>/comment/<int:comment_id>/', views.post_comment_delete, name='post_comment_delete'),
    path('post/<int:post_id>/comment/<int:comment_id>/edit/', views.post_comment_edit, name='post_comment_edit'),
    path('post/list/<username>/',views.posts_user_listview,name='post_userlist'),
    path('search/',views.post_search,name='post_search')

]
