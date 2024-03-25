from django.urls import path

from post.views import PostWriteView, PostDetailView, PostUpdateView, PostDeleteView, PostListView, PostListAPI

app_name = 'post'

urlpatterns = [
    path('write/', PostWriteView.as_view(), name='write'),
    path('detail/', PostDetailView.as_view(), name='detail'),
    path('update/', PostUpdateView.as_view(), name='update'),
    path('delete/', PostDeleteView.as_view(), name='delete'),
    path('list/', PostListView.as_view(), name='list'),
    path('list/<int:page>/', PostListAPI.as_view(), name='list-api'),
]














