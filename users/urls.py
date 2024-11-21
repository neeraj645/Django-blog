from django.urls import path
from .views import signup, login_page, profile_page, logout_view

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', login_page, name="login_page"),
    path('logout/',logout_view, name="logout_view"),
    path('profile/', profile_page, name='profile_page'),
]

