from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('payer/<int:payer_id>/', views.PayerView.as_view(), name='payer_list'),
    path('categories/<int:category_id>/', views.CategoryView.as_view(), name='category_list'),
    path('create_spend/', views.CreateSpend.as_view(), name='create_spend'),
    path('create_category', views.CreateCategory.as_view(), name='create_category')
]
