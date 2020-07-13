from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, Comment
from blog.forms import PostForms, CommentForm


class AboutView(TemplateView):
    template_name = 'blog/about.html'


class PostView(ListView):
    model = Post
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.order_by('publish_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_details.html'

    form_class = PostForms
    model = Post


class PostUpdateView(UpdateView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_details.html'

    form_class = PostForms
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts')


class Draft(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list'
    model = Post

    # def get_queryset(self):
    #     return Post.objects.filter(publish_date__isnull=True)


def addCommentToPost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('detail_post', pk=post.pk)

    else:
        form = CommentForm()

    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def approveComment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('posts', pk=comment.post.pk)


@login_required
def removeComment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('posts', pk=post_pk)


@login_required
def postPublish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    print(pk)
    post.publish()
    return redirect('posts')