from django.contrib.auth import views
from django.urls import path
from .views import index, Signup, Createwall, Deletewall, Detailwall, Updatewall, dashboard,add_video

urlpatterns = [
    path('', index, name='index'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(template_name='videoshandler/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create/', Createwall.as_view(), name='create'),
    path('wally/<int:pk>/', Detailwall.as_view(), name='detail'),
    path('wally/<int:pk>/update', Updatewall.as_view(), name='update'),
    path('wally/<int:pk>/delete', Deletewall.as_view(), name='delete'),
    path('wally/<int:pk>/add', add_video, name='add_video'),

]
