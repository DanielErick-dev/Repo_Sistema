from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DeleteView
from django.views.generic.edit import FormView
from .models import Academy
from datetime import date
from django.urls import reverse_lazy
from .forms import AcademyForm
from datetime import timedelta
import pyttsx3
from time import sleep
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


def Academy_search(request):
    context = {}
    if str(request.method) == 'POST':
        cpf = request.POST.get('input_cpf')
        try:
            usuario = get_object_or_404(Academy, cpf=cpf)
        except:
            context['erro'] = '!Erro, usuário não existe'
        else:
            context['usuario'] = usuario
            
    return render(request, 'academy/academy_search.html', context)


def Atualizando_pagamento_usuario(request):
    context = {}
    engine = pyttsx3.init()
    if str(request.method) == 'POST':
        cpf = request.POST.get('input_cpf')
        try:
            usuario = get_object_or_404(Academy, cpf=cpf)
        except:
            context['erro'] = '!Erro, usuário não existe'
            engine.say(context['erro'])
            engine.runAndWait()
        else:
            engine.say('usuário atualizado com sucesso')
            engine.runAndWait()
            usuario.created_at = datetime.now()
            data_vencimento = datetime.now() + timedelta(days=30)
            usuario.vencimento = data_vencimento.date()
            usuario.save()
            return redirect('administrative_view')
    return render(request, 'academy/academy_atualizar_pagamento.html', context)



class AcademyListView(ListView):
    # listando usuários salvos
    model = Academy
    template_name = 'academy/list_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # usando método de verificação de login do ADMIN
        context['logado'] = IndexView.validando_login(self, request=self.request)
        return context
        
        
def Listando_usuarios_pendentes(request):
    context = {}
    usuarios = Academy.objects.all()
    vencimentos_pendentes = False
    for usuario in usuarios:
        if usuario.vencimento.date() < datetime.now().date():
            print(f'data de vencimento do usuário: {usuario.vencimento.date}\ndata atual: {datetime.now().date()}')
            vencimentos_pendentes = True
    if vencimentos_pendentes:
        context['usuarios_pendentes'] = 'existem usuários pendentes'
    if request.user.is_authenticated:
        context['logado'] = True
    else:
        pass
    return render(request, 'academy/list_pendentes.html', context)
