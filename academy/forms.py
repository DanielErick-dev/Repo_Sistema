from django import forms
from .models import Academy
from django.forms import ValidationError

class AcademyForm(forms.ModelForm):
    
    class Meta:
        model = Academy
        fields = ['name', 'lastname', 'contact', 'cpf']

    def __init__(self, *args, **kwargs):
        super(AcademyForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'username'
        self.fields['lastname'].widget.attrs['placeholder'] = 'lastname'
        self.fields['contact'].widget.attrs['placeholder'] = '(99) 9-9999-9999'
        self.fields['cpf'].widget.attrs['placeholder'] = '999.999.999-99'
        
        
    def clean_lastname(self):
        lastname = self.cleaned_data['lastname']
        teste_last_name = Academy.objects.filter(lastname=lastname)
        if teste_last_name:
            raise ValidationError("sobrenome já existente")
        else:
            return lastname
    
    def clean_name(self):
        name = self.cleaned_data['name']
        teste_name = Academy.objects.filter(name=name)
        if teste_name:
            raise ValidationError("nome já existente")
        else:
            return name
    def clean_contact(self):
        contato = self.cleaned_data["contact"]
        teste_contato = Academy.objects.filter(contact=contato)
        
        if teste_contato:
            raise ValidationError('número já existe')
        if not contato.isdigit() or contato[2] != '9':
            raise ValidationError('número inválido')
        else:
            return contato
        
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        teste_cpf = Academy.objects.filter(cpf=cpf)
        
        if len(cpf) != 11:
            raise ValidationError('cpf inválido')
        
        if teste_cpf:
            raise ValidationError('cpf já existe')
        else:
            return cpf