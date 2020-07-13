from django.urls import path
from . import views

urlpatterns = [

    path('about', views.AboutView.as_view(), name="about"),
    path('drafts', views.draftview, name="drafts"),

    path('', views.PostView.as_view(), name="posts"),
    path('newpost', views.CreatePostView.as_view(), name="create_post"),
    path('<int:pk>/edit', views.PostUpdateView.as_view(), name="edit_post"),
    path('<int:pk>', views.PostDetailView.as_view(), name="detail_post"),
    path('<int:pk>/delete', views.PostDeleteView.as_view(), name="remove_post"),
    path('<int:pk>/publish', views.postPublish, name="publish_post"),

    path('<int:pk>/comment', views.addCommentToPost, name="addcomment_post"),
    path('<int:pk>/comment/approve', views.approveComment, name="approve_cmt"),
    path('<int:pk>/comment/remove', views.removeComment, name="remove_cmt"),

]
