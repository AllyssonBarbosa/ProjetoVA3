from django.views.generic.edit import FormView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.db.models import Sum
from django.utils.timezone import now

from .models import Servico
from .forms import ServicoForm

class ServicoFormView(FormView):
    template_name = 'Servico.html'
    form_class = ServicoForm
    success_url = reverse_lazy('servico:Lista_servico')

    def form_valid(self, form):
        servico = form.save(commit=False)
        servico.usuario = self.request.user
        servico.save()
        return super().form_valid(form)


class ServicoSuccessView(TemplateView):
    template_name = 'Servico_pronto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicos = Servico.objects.all()
        valor_total = servicos.aggregate(total=Sum('valor_cobrado'))['total'] or 0
        inicio_mes = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        quantidade_servicos_mes = servicos.filter(data__gte=inicio_mes).count()

        context['servicos'] = servicos
        context['valor_total'] = valor_total
        context['quantidade_servicos_mes'] = quantidade_servicos_mes
        return context


class ServicoListView(ListView):
    model = Servico
    template_name = 'Lista_servico.html'
    context_object_name = 'servicos'
    ordering = ['-data']


class ExcluirServicoView(DeleteView):
    model = Servico
    success_url = reverse_lazy('servico:Lista_servico')
    template_name = 'confirmar_exclusao.html'
