from django.urls import path
from monitor_panel.views import IndexView, GetChartDataView, SetActiveHostView, SetActiveMeasureView, LoadHostsView

urlpatterns = [
    path('', LoadHostsView.as_view(), name='load'),
    path('get-chart-data/', GetChartDataView.as_view(), name='get_chart_data'),
    path('set-active-host/', SetActiveHostView.as_view(), name='set_active_host'),
    path('set-active-measure/', SetActiveMeasureView.as_view(), name='set_active_measure'),
    path('dashboard/', IndexView.as_view(), name='index'),
]
