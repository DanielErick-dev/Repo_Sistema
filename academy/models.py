
from django.db import models
from datetime import timedelta
from django.db.models.signals import post_save
from django.core.validators import MinLengthValidator
class Academy(models.Model):
    name = models.CharField(max_length=100, verbose_name="nome", validators=[MinLengthValidator(3)])
    lastname = models.CharField(max_length=100, verbose_name="sobrenome", validators=[MinLengthValidator(3)])
    contact = models.CharField(max_length=11, verbose_name="contato", validators=[MinLengthValidator(11)])
    cpf = models.CharField(max_length=11, verbose_name="cpf", validators=[MinLengthValidator(11)])
    created_at = models.DateTimeField(auto_now_add=True)
    vencimento = models.DateTimeField(auto_now_add=True, null=False)
    def __str__(self):
        return self.name

def atualizar_vencimento(sender, instance, **kwargs):
    post_save.disconnect(atualizar_vencimento, sender=Academy)
    if instance.created_at:
        data_somada = instance.created_at + timedelta(days=30)
        instance.vencimento = data_somada.date()
        print(instance.vencimento) 
        instance.save()
            
post_save.connect(atualizar_vencimento, sender=Academy)
 
