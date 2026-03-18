from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Auth / main pages
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('homepage/', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # ONE-PAGE PASSWORD RESET FLOW
    path('forgot-password/', views.password_reset_onepage, name='password_reset'),
    path('forgot-password/<uidb64>/<token>/', views.password_reset_onepage, name='password_reset_confirm'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)