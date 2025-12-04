from django.shortcuts import render, redirect
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostCreateUpdateForm, CustomUserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

class ListBlogPost(ListView):
    model = Post
    template_name = 'blog/ListView.html'
    context_object_name = 'posts'

class DetailBlogPost(DetailView):
    model = Post
    template_name = 'blog/DetailView.html'
    context_object_name = 'detail_blog'   

class CreatBlogPost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateUpdateForm
    template_name = 'blog/CreateView.html'
    success_url = reverse_lazy('posts')


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateBlogPost(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostCreateUpdateForm
    template_name = 'blog/UpdateView.html'
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
    template_name = 'blog/DeleteView.html'
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