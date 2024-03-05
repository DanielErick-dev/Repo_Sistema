from datetime import datetime
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DeleteView
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
    
    
    
    def post(self, request, *args, **kwargs):
        print('executando método post')
        name = request.POST.get('name')
        print(f'nome digitado pelo usuário: {name}')

        # filtrando se o usuário digitado pelo administrador existe no banco de dados 
        usuario = Academy.objects.filter(name=name)
        if usuario:
            for informacao in usuario:
                print(f'nome do usuário: {informacao.name}, sobrenome do usuário: {informacao.lastname}, número de telefone do usuário: {informacao.contact}, data de criação do usuário: {informacao.created_at.date()}, data de vencimento do usuário: {informacao.vencimento}')
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
    

def CriandoUsuario(request):
    if request.method == 'get':
        form = AcademyForm()
    else:
        form = AcademyForm(request.POST)
        if form.is_valid():
            print('formulário válido')
            form.save()
            return redirect('administrative_view')
    context = {
        'form': form
    }
    print(context)
    return render(request, 'academy/academy_form.html', context)
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
                    if usuario.vencimento.date() < datetime.now().date():
                        vencimentos_pendentes = True
                        lista_de_informacoes.append(usuario.name)

            return lista_de_informacoes
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        
        # usando método para verificar se existem usuários pendentes
        context['usuarios_pendentes'] = self.verificando_vencimentos_pendentes()

        # usando método de verificação de login do ADMIN
        context['logado'] = IndexView.validando_login(self, request=self.request)
        return context
    
        