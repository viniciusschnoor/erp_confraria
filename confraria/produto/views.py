from django.db.models import Q
from .models import Produto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from .forms import ProdutoForm
from django.urls import reverse_lazy


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    paginate_by = 15

    def get_queryset(self):
        nome_produto = self.request.GET.get('nome')
        produto_disponivel = self.request.GET.get('disponibilidade')
        produtos = super(ProdutoListView, self).get_queryset()
        q = Q()
        objects_id = (obj.id for obj in produtos if obj.disponibilidade is True)

        if nome_produto:
            q = q & Q(nome__icontains=nome_produto)

        if produto_disponivel:
            q = q & Q(id__in=objects_id)

        produtos = produtos.filter(q).order_by("-nome")

        return produtos


class ProdutoCreateView(CreateView):
    model = Produto
    form_class = ProdutoForm

    def get_success_url(self):
        return reverse_lazy('produto_list')


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm

    def get_success_url(self):
        return reverse_lazy('produto_list')
