from django.shortcuts import render, redirect
from .models import Post, Comment, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostCreateUpdateForm, CustomUserCreationForm, CommentForm, PostForm
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

class ListBlogPost(ListView):
    model = Post
    template_name = 'blog/listing_post.html'
    context_object_name = 'posts'

class DetailBlogPost(DetailView):
    model = Post
    template_name = 'blog/viewing_post.html'
    context_object_name = 'detail_blog'   

class CreatBlogPost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateUpdateForm
    template_name = 'blog/creating_post.html'
    success_url = reverse_lazy('posts')


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateBlogPost(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostCreateUpdateForm
    template_name = 'blog/editing_post.html'
    success_url = reverse_lazy('posts')

    def test_func(self):
        post = self.get_object()  # Get the current Post instance
        return self.request.user == post.author  # Allow only the author to update
    
    def handle_no_permission(self):
        # You can change this to the response you want
        return HttpResponseForbidden("You do not have permission to update this post.")

    def form_valid(self, form):
        form.instance.author = self.request.user  # This is optional since the author should not change
        return super().form_valid(form)


class DeleteBlogPost(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/deleting_post.html'
    context_object_name = 'Delete_blog'

    def test_func(self):
        post = self.get_object()  # Get the current Post instance
        return self.request.user == post.author  # Allow only the author to update
    
    def handle_no_permission(self):
        # You can change this to the response you want
        return HttpResponseForbidden("You do not have permission to delete this post.")
    

### User Authentication

def RegisterView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('posts')  # Redirect to a homepage or another relevant page
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


### profile
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm

@login_required
def profile_view(request):
    user = request.user  # Get the currently authenticated user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)  # Bind the form to the user instance
        if form.is_valid():
            form.save()  # Save changes to the user profile
            return redirect('profile')  # Redirect to the same profile page after saving
    else:
        form = UserProfileForm(instance=user)  # Create a form instance for the GET request

    return render(request, 'blog/profile.html', {'form': form})


class CommentCreateView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()  # Get all comments related to the post
        comment_form = CommentForm()  # Create an empty comment form
        return render(request, 'blog/detail.html', {
            'post': post,
            'comments': comments,
            'comment_form': comment_form,
        })

    @method_decorator(login_required)
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post  # Associate the comment with the post
            comment.author = request.user  # Associate the comment with the logged-in user
            comment.save()  # Save the comment
            return redirect('detail', pk=pk)  # Redirect back to the post detail page

        comments = post.comments.all()  # Get all comments for the post
        return render(request, 'blog/detail.html', {
            'post': post,
            'comments': comments,
            'comment_form': comment_form,
        })

class CommentUpdateView(View):
    @method_decorator(login_required)
    def post(self, request, post_pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk, author=request.user)
        comment_form = CommentForm(request.POST, instance=comment)

        if comment_form.is_valid():
            comment_form.save()  # Save the updated comment
            return redirect('detail', pk=post_pk)

class CommentDeleteView(View):
    @method_decorator(login_required)
    def post(self, request, post_pk, comment_pk):
        comment = get_object_or_404(Comment, pk=comment_pk, author=request.user)
        comment.delete()  # Delete the comment
        return redirect('detail', pk=post_pk)


class PostByTagListView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the logged-in user
        return super().form_valid(form)
    

### Search Functionality
from django.db.models import Q
def search_view(request):
    query = request.GET.get('q')
    results = Post.objects.none()  # Start with an empty QuerySet

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |  # Matches title
            Q(content__icontains=query) |  # Matches content
            Q(tags__name__icontains=query)  # Matches tags
        ).distinct()  # Ensure no duplicate posts are shown

    return render(request, 'blog/search_results.html', {'results': results, 'query': query})