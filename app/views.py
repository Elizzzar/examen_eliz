from telnetlib import LOGOUT
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView, View, DeleteView
from django.urls import reverse_lazy
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import  HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

class HomeView(View):
    template_name = 'home.html'
    paginate_by = 9

    def get(self, request):
        object_list = Article.objects.all().order_by('-created_at')
        paginator = Paginator(object_list, self.paginate_by)
        page = request.GET.get('page')

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        user_obj = request.user if request.user.is_authenticated else None

        return render(request, self.template_name, {'articles': articles, 'user_obj': user_obj})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(article=self.object)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = self.object
            new_comment.author = request.user
            new_comment.save()
            return self.render_to_response(self.get_context_data(comment_form=comment_form))
        else:
            return self.render_to_response(self.get_context_data(comment_form=comment_form))

class CreateArticleView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'create_article.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class EditArticleView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_update.html'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})


class ArticleUpdateView(UserPassesTestMixin, UpdateView):
    model = Article
    template_name = 'article_update.html'
    form_class = ArticleForm
    success_url = reverse_lazy('home')

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

class CommentUpdateView(UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'comment_update.html'
    form_class = CommentForm
    success_url = reverse_lazy('home')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author




class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def send_verify_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}')
        message = f'Здравствуйте, {user.username}! Перейдите по ссылке ниже для подтверждения почты:\n\n{verify_url}'
        send_mail('Подтверждение почты', message, 'chelovek228opapopabelov@gmail.com', [user.email])
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        print(user)
        user.is_active = False
        user.save()
        self.send_verify_email(user)
        return response
    
class VerificationSuccess(TemplateView):
    template_name = 'verification_success.html'

class VerificationError(TemplateView):
    template_name = 'verification_error.html'

class VerifyEmailView(View):
    def get(self, request, user_id, token):
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('verify_success')
        else:
            return redirect('verify_error')

class Login(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')

    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(password=password,username=username)
        if user is not None and user.is_active:
            login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(reverse_lazy('login')+'?active=false')


def my_logout(request):
    logout(request)
    return redirect('login')