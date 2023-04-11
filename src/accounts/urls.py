from django.urls import path, re_path, reverse_lazy
from .views import *
from .save_views import *
from django.contrib.auth import views as auth_views

app_name = 'accounts'


urlpatterns=[
    path('sign-up',signup,name="signup"),
    path('login/',login,name="login"),
    path('logout/', logout_page, name='logout'),

    path('settings/', account_settings, name='account_settings'),
    path('u/<uuid:pk>/', my_profile, name='my_profile'),

    path('delete/<uuid:pk>/', delete, name='delete'),

    path('all-users/', alluser, name='all_user'),
    path('my-connections/<uuid:pk>/', following_list, name='following_list'),
    path('followers/<uuid:pk>/', followers_list, name='followers_list'),
    path('<uuid:pk>/follower/add',AddFollower.as_view(),name="add-follower"),
    path('<uuid:pk>/follower/remove',RemoveFollower.as_view(),name="remove-follower"),

    path('password/change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password/reset/', auth_views.PasswordResetView.as_view(success_url = reverse_lazy("accounts:password_reset_done")), name='password_reset'),
    path('password/reset/done/',  auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url = reverse_lazy("accounts:password_reset_complete")), name='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('save_basicinfo/', save_basicinfo, name='save_basicinfo'),
    path('change_password/', change_password, name='change_password'),
    path('save_email/', save_email, name='save_email'),
    path('save_preferences/', save_preferences, name='save_preferences'),

    path('payment_method/', payment_method_page, name='payment_method_page'),

    path('payout_method/', payout_method_page, name='payout_method_page'),
    
    ]