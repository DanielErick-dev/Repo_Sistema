
from datetime import datetime
from typing import Any
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, View
from .models import Academy
from datetime import date
from django.urls import reverse_lazy
class IndexView(TemplateView):
    template_name = "academy/index_view.html"

    def validando_login(self, request=None):
        if request is None:
            request = self.request
        if request.user.is_authenticated:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logado"] = self.validando_login(request=self.request)
        return context
    
class AcademyDeleteView(DeleteView):
    model = Academy
    success_url=reverse_lazy('index_view')
class CadastroView(CreateView):
    template_name = 'academy/create_view.html'
    model = Academy
    fields = ["name", "lastname", "contact"]
    success_url = reverse_lazy("index_view")

    def get(self, request, *args, **kwargs):
        print("Requisição GET recebida") 
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        lista_de_ddd = str([11, 12 , 13 , 14, 15 , 16, 17 , 18 , 19, 21, 22, 24, 27, 28, 32, 33, 34, 35, 37, 38, 41, 42, 43, 44, 46, 47, 48, 49, 51, 53, 54, 55, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 73 ,74 ,75,77,79, 81, 82, 83, 84 ,85, 86,87,88,89,91 , 92, 93 , 94, 95,96,97,98,99])
        nome = form.cleaned_data["name"].lower()
        contato = form.cleaned_data["contact"]
        sobrenome = form.cleaned_data["lastname"].lower()
        usuarios_salvos = Academy.objects.all()
        ddd_do_numero = str(contato[:2])
        numero_adicional = str(contato[2])
        if contato.isdigit():
            print(f'o formato do número {contato} é válido por só conter digitos')
        else:  
            print(f'o formato do número {contato} é inválido por conter letras')
            form.add_error("contact", "o formato do número é inválido")
            erro_contato = "o formato do número é inválido"
        if ddd_do_numero not in lista_de_ddd:
            form.add_error("contact", "o DDD do número é inválido")
            erro_contato = "o DDD do número é inválido"
        if len(contato) != 11: 
            form.add_error("contact", "este número não é válido")
            erro_contato = "o número de telefone é inválido"
        if numero_adicional != '9':
            form.add_error("contact", "número adicional obrigatório inválido")
            erro_contato = "número adicional obrigatório inválido"
        for usuarios in usuarios_salvos:
            if nome == usuarios.name and sobrenome == usuarios.lastname:
                form.add_error('name', f"Já existe um usuário com este nome")
                erro_contato = f"Já existe um usuário com este nome"
            if contato == usuarios.contact:
                form.add_error('contact', f"já existe um usuário com este número")
                erro_contato = f"já existe um usuário com este número"
        if form.errors:
            context = self.get_context_data(erro_contato=erro_contato)
            return self.render_to_response(context)
        
        form.instance.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

class AcademyListView(ListView):
    model = Academy


class AcademyUsuariosPendentesView(ListView):
    model = Academy

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        def verificando_vencimentos_pendentes(self, **kwargs):
            vencimentos_pendentes = False
            data_atual = date.today()
            usuarios = self.get_queryset()
            for usuario in usuarios:
                if usuario.vencimento < datetime.now().date():
                    vencimentos_pendentes = True
                    print(f'existe usuarios com vencimento pendente: {usuario.name} {usuario.lastname}\ndata de vencimento: {usuario.vencimento}')
                    break
                else:
                    print("não houve usuários com vencimento pendente")
            return vencimentos_pendentes
        context['usuarios_pendentes'] = verificando_vencimentos_pendentes(self)
        context['pagina_usuarios_pendentes'] = True
        return context
    
        