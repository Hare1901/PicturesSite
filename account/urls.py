from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    #path('login/', views.user_login, name='login'),
    # путь для логина- разлогинивания
    path(
        "login/",
        auth_views.LogoutView.as_view(),
        name='login'
    ),
    path(
       "logout/",
       auth_views.LogoutView.as_view(),
       name='logout'
    ),
    # путь для смены пароля
    path(
        "password-change/",
        auth_views.PasswordResetView.as_view(),
        name='password_change'
    ),
    #PasswordResetDoneView - отображает сообщение о удачной смене пароля
    path(
        "password-change/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_change_done"
    ),

    path("", views.dashboard, name='dashboard')

]
