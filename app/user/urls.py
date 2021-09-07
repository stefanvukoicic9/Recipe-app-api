from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path("signin/", views.SiginUserView.as_view(), name='signin'),
    path('login/', views.CreateTokenView.as_view(), name='login'),
]