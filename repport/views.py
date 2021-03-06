from .models import Post # . menes directory to the models.
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # mix in sikre os at user autorotiet
from django.views.generic import (
    ListView,
    DetailView, # når vil kigges efter detail of post
    CreateView,
    UpdateView,
    DeleteView
)

def home(request):
    context = {
        #'posts': posts # istedet for dommy data vi hente data fra database i det næste linje
        'posts': Post.objects.all()
    }
    return render(request, 'repport/home.html', context)

def about(request):
    return render(request, 'repport/about.html', {'title': 'About'})

class PostListView(ListView):
    model = Post
    template_name = 'repport/home.html'  # <app>/<model>_<viewtype>.html  PostListView.as_view() med den mens <app> / <model>_<vietype> html- app er ligsom vores repport app. model er database og vieetype er list.
    context_object_name = 'posts'
    ordering = ['-date_posted'] # med - vil nyeste post vil stå først
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'repport/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self): # queryset er et ord ellers vil vi få fejl med at læse antal post for hver brugeren
        user = get_object_or_404(User, username=self.kwargs.get('username')) # kwargs er query paramater
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):# mix er brugeren autoritet- her vil vi inherit fra login som krav. når vi vil se postes skal user være logget ind ellers vil den redirctet to login side
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # acctuele user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # add mixin hjælper os at postens skaberen får lov til update post
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author: #tjekke at den post user is log in
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # efter delete a object så vil redirect os to

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

'''
posts = [
    {
        'author': 'Sam',
        'title': 'rapport 1',
        'content': 'First post content',
        'date_posted': 'Sep 7, 2020'
    }
]
'''