from django.urls import path
from .views import ServicoFormView, ServicoListView, ExcluirServicoView
from django.views.generic.base import TemplateView

app_name = 'servico'

urlpatterns = [
    path('servico/', ServicoFormView.as_view(), name='Servico'),
    path('servico/success/', TemplateView.as_view(template_name='Servico_pronto.html'), name='Servico_pronto'),
    path('listar/', ServicoListView.as_view(), name='Lista_servico'),
    path('excluir/<int:pk>/', ExcluirServicoView.as_view(), name='excluir_servico'),
]
