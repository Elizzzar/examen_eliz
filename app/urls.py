from django.urls import path, reverse_lazy
from .views import ArticleDeleteView, CommentDeleteView, CommentUpdateView, HomeView, ArticleDetailView, CreateArticleView, EditArticleView, SignUpView, VerificationSuccess, VerificationError, VerifyEmailView, Login, my_logout

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('create/', CreateArticleView.as_view(), name='create_article'),
    path('update/<int:pk>/', EditArticleView.as_view(), name='article_update'),
    path('delete/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    # 
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/<int:user_id>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('verify/success/', VerificationSuccess.as_view(), name='verify_success'),
    path('verify/error/', VerificationError.as_view(), name='verify_error'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', my_logout, name='logout'),
]