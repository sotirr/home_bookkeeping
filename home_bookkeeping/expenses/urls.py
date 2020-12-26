from django.urls import path

from . import views

app_name = 'expenses'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('create_spend/', views.CreateSpend.as_view(), name='create_spend'),
    path('create_category/', views.CreateCategory.as_view(), name='create_category'),
    path('<pk>/delete', views.DeleteSpend.as_view(), name='delete_spend'),
]
