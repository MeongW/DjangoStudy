from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('board/create/', views.board_create, name='board_create'),
    path('<int:pk>/edit/', views.board_edit, name='board_edit'),
    path('<int:pk>/delete/', views.board_delete, name='board_delete'),
    path('board/', views.board_list, name='board_list'),
    path('<int:pk>/', views.board_detail, name='board_detail'),
]