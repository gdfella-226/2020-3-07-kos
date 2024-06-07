from django.urls import path
from monitor_panel import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_chart_data/', views.get_chart_data, name='get_chart_data'),
    path('set_active_host/', views.set_active_host, name='set_active_host'),
    path('set_active_measure/', views.set_active_measure, name='set_active_measure'),
]
