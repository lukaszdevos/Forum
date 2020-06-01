from django.urls import path
from accounts import views
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.tokens import PasswordResetTokenGenerator

app_name = 'accounts'

urlpatterns = [
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name="logout"),
    
    path('profile/<username>/',views.profile_details_view,name='profile'),
    path('profile/edit',views.profile_edit_view,name='profile_edit'),
    path('profile/edit/password',views.change_password,name='profile_password'),
    
    path('password_reset/',views.PasswordReset.as_view(),name='password_reset'),
    path('password_reset_done/',views.PasswordResetDone.as_view(),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',views.PasswordResetConfirm.as_view(),name='password_reset_confirm'),
    path('password_reset_complete/',views.PasswordResetComplete.as_view(),name='password_reset_complete'),    
    
    
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)