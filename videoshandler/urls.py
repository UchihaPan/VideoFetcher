from django.contrib.auth import views
from django.urls import path
from .views import index, Signup, Createwall, Deletewall, Detailwall, Updatewall, dashboard,add_video,search,Deletevideo

urlpatterns = [
    path('', index, name='index'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(template_name='videoshandler/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create/', Createwall.as_view(), name='create'),
    path('detail/<int:pk>/', Detailwall.as_view(), name='detail'),
    path('update/<int:pk>/', Updatewall.as_view(), name='update'),
    path('delete/<int:pk>/', Deletewall.as_view(), name='delete'),
    path('deletevideo/<int:pk>/', Deletevideo.as_view(), name='deletevideo'),

    path('add/<int:pk>/', add_video, name='add'),
    path('search/', search, name='search'),

]
