from django.urls import path

from . import views

app_name = 'expenses'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('create_spend/', views.CreateSpend.as_view(), name='create_spend'),
    path('create_category/', views.CreateCategory.as_view(), name='create_category'),
    path('<pk>/delete', views.DeleteSpend.as_view(), name='delete_spend'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('api/categories_chart_data', views.ApiCategoriesChart.as_view(), name='categories_chart_data'),
    path('api/payers_chart_data', views.ApiPayersChart.as_view(), name='payers_chart_data'),
]
