from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customers/<str:id>', views.customers, name='customers'),
    path('create_order/<str:pk>', views.create_order, name='create_order'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('create_customer', views.create_customer, name='create_customer'),
    path('confirm_delete/<str:pk>/', views.confirm_delete, name='confirm_delete'),
    path('delete/<str:pk>/', views.delete, name='delete'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userpage, name='user-page'),
    path('account/', views.accountSettings, name='account')
]
