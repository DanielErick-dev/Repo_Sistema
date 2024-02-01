from datetime import datetime
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.views.generic.edit import FormView
from .models import Academy
from datetime import date
from django.urls import reverse_lazy
from .forms import AcademyForm


class IndexView(TemplateView):
    template_name = "academy/index_view.html"
    # verificando se o usuário está logado no ADMIN do sistema
    def validando_login(self, request=None):
        if request is None:
            request = self.request
        if request.user.is_authenticated:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # obtendo contexto logado caso o usuário esteja logado no sistema
        context["logado"] = self.validando_login(request=self.request)
        return context
    
class AcademyDeleteView(DeleteView):
    model = Academy
    success_url=reverse_lazy('administrative_view')

class AcademyAdministrativeView(FormView):
    form_class = AcademyForm
    template_name = 'academy/administrative_view.html'
    success_url = reverse_lazy('administrative_view')
    model = Academy


    def form_valid(self, form):
        # obtendo lista de DDDs válidos do Brasil
        lista_de_ddd = str([11, 12 , 13 , 14, 15 , 16, 17 , 18 , 19, 21, 22, 24, 27, 28, 32, 33, 34, 35, 37, 38, 41, 42, 43, 44, 46, 47, 48, 49, 51, 53, 54, 55, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 73 ,74 ,75,77,79, 81, 82, 83, 84 ,85, 86,87,88,89,91 , 92, 93 , 94, 95,96,97,98,99])

        # pegando dados submetidos no formulário
        nome = form.cleaned_data["name"].lower()
        contato = form.cleaned_data["contact"]
        sobrenome = form.cleaned_data["lastname"].lower()
        
        # pegando lista de usuários existentes
        usuarios_salvos = Academy.objects.all()

        # pegando DDD do número submetido
        ddd_do_numero = str(contato[:2])

        # pegando número adicional do número submetido
        numero_adicional = str(contato[2])

        # verificando se o número de contato só contém digitos
        if not contato.isdigit():
            form.add_error("contact", "o formato do número é inválido")
            erro_contato = "o formato do número é inválido"
        
        # verificando se o DDD do número é válido
        if ddd_do_numero not in lista_de_ddd:
            form.add_error("contact", "o DDD do número é inválido")
            erro_contato = "o DDD do número é inválido"

        # verificando se o número de contato contém 11 digitos
        if len(contato) != 11: 
            form.add_error("contact", "este número não é válido")
            erro_contato = "o número de telefone é inválido"

        # verificando se o número adicional é o número 9
        if numero_adicional != '9':
            form.add_error("contact", "número adicional obrigatório inválido")
            erro_contato = "número adicional obrigatório inválido"

        # verificando se existem dados repetidos
        for usuarios in usuarios_salvos:
            if nome == usuarios.name and sobrenome == usuarios.lastname:
                form.add_error('name', f"Já existe um usuário com este nome")
                erro_contato = f"Já existe um usuário com este nome"
            if contato == usuarios.contact:
                form.add_error('contact', f"já existe um usuário com este número")
                erro_contato = f"já existe um usuário com este número"

        # verificando se foi gerado algum erro nas verificações
        if form.errors:
            print(f'erro: {erro_contato}')
            context = self.get_context_data(erro_contato=erro_contato+', aperte em "cadastrar usuário" e insira os dados corretos novamente por favor')
            return self.render_to_response(context)
        else:
            context = self.get_context_data(erro_contato='usuário cadastrado com sucesso')
            return self.render_to_response(context)
        # salvando formulário com os dados submetidos usando o método save
        form.instance.save()
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        usuario = Academy.objects.filter(name=name)
        print('executando método post')
        print(usuario)
        if usuario:
            for informacao in usuario:
                print(informacao.name, informacao.lastname, informacao.contact, informacao.created_at.date())
        else:
            print('usuário não existe ou foi digitado incorretamente')  
        context = self.get_context_data(usuario=usuario)
        if usuario:
            return self.render_to_response(context)
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logado"] = IndexView.validando_login(self, request=self.request)
        context["usuarios"] = Academy.objects.all()
        context["usuários_pendentes"] = AcademyUsuariosPendentesView.verificando_vencimentos_pendentes(self)
        return context
    

class CadastroView(CreateView):
    template_name = 'academy/create_view.html'
    
    model = Academy
    fields = ["name", "lastname", "contact"]
    success_url = reverse_lazy("administrative_view")

    def get(self, request, *args, **kwargs):
        print("Requisição GET recebida") 
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        # obtendo lista de DDDs válidos do Brasil
        lista_de_ddd = str([11, 12 , 13 , 14, 15 , 16, 17 , 18 , 19, 21, 22, 24, 27, 28, 32, 33, 34, 35, 37, 38, 41, 42, 43, 44, 46, 47, 48, 49, 51, 53, 54, 55, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 73 ,74 ,75,77,79, 81, 82, 83, 84 ,85, 86,87,88,89,91 , 92, 93 , 94, 95,96,97,98,99])

        # pegando dados submetidos no formulário
        nome = form.cleaned_data["name"].lower()
        contato = form.cleaned_data["contact"]
        sobrenome = form.cleaned_data["lastname"].lower()
        
        usuarios_salvos = Academy.objects.all()
        ddd_do_numero = str(contato[:2])
        numero_adicional = str(contato[2])

        # verificando se o número de contato só contém digitos
        if not contato.isdigit():
            form.add_error("contact", "o formato do número é inválido")
            erro_contato = "o formato do número é inválido"
        
        # verificando se o DDD do número é válido
        if ddd_do_numero not in lista_de_ddd:
            form.add_error("contact", "o DDD do número é inválido")
            erro_contato = "o DDD do número é inválido"

        # verificando se o número de contato contém 11 digitos
        if len(contato) != 11: 
            form.add_error("contact", "este número não é válido")
            erro_contato = "o número de telefone é inválido"

        # verificando se o número adicional é o número 9
        if numero_adicional != '9':
            form.add_error("contact", "número adicional obrigatório inválido")
            erro_contato = "número adicional obrigatório inválido"

        # verificando se existem dados repetidos
        for usuarios in usuarios_salvos:
            if nome == usuarios.name and sobrenome == usuarios.lastname:
                form.add_error('name', f"Já existe um usuário com este nome")
                erro_contato = f"Já existe um usuário com este nome"
            if contato == usuarios.contact:
                form.add_error('contact', f"já existe um usuário com este número")
                erro_contato = f"já existe um usuário com este número"

        # verificando se foi gerado algum erro nas verificações
        if form.errors:
            context = self.get_context_data(erro_contato=erro_contato)
            return self.render_to_response(context)
        
        # salvando formulário com os dados submetidos usando o método save
        form.instance.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

class AcademyListView(ListView):
    # listando usuários salvos
    model = Academy
    template_name = 'academy/list_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # usando método de verificação de login do ADMIN
        context['logado'] = IndexView.validando_login(self, request=self.request)
        return context
        
        


class AcademyUsuariosPendentesView(ListView):
    # listando usuários pendentes
    model = Academy
    template_name = 'academy/list_pendentes.html'

    def verificando_vencimentos_pendentes(self):
            vencimentos_pendentes = False
            data_atual = date.today()
            lista_de_informacoes = [vencimentos_pendentes]
            usuarios = Academy.objects.all()
            for usuario in usuarios:
                if usuario.vencimento is not None:
                    if usuario.vencimento < datetime.now().date():
                        vencimentos_pendentes = True
                        lista_de_informacoes.append(usuario.nome)

            return lista_de_informacoes
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        # usando método para verificar se existem usuários pendentes
        context['usuarios_pendentes'] = self.verificando_vencimentos_pendentes()

        # usando método de verificação de login do ADMIN
        context['logado'] = IndexView.validando_login(self, request=self.request)
        return context
    
        