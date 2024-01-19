from typing import Any
from django.db import models
import arrow
from datetime import date

# Create your models here.



class Academy(models.Model):
    name = models.CharField(max_length=100,null=False, blank=False, verbose_name="nome", default=None)
    lastname = models.CharField(max_length=100,null=False, blank=False, verbose_name="sobrenome", default=None,)
    contact = models.CharField(max_length=100, null=False, blank=False, verbose_name="contato", default=None, )
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False,)
    vencimento = models.DateField(null=True, blank=True)
    
    def save(self, **kwargs):
        super().save(**kwargs)
        data_com_shift = arrow.get(str(self.created_at))
        self.vencimento = data_com_shift.shift(days=30).date()
        

    def get_vencimento(self):
        return self.vencimento

    
