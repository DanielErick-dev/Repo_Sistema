from django.test import TestCase
from academy.models import Academy
from datetime import date
import arrow

class AcademyModelTest(TestCase):
    def setUp(self):
        self.usuario_instanciado = Academy(name='daniel',lastname='erick' ,contact='61996058272')
        
    def test_validating_contact_field(self):
        terceiro_digito = self.usuario_instanciado.contact[2]
        self.assertEqual(len(self.usuario_instanciado.contact), 11)
        self.assertEqual(terceiro_digito, '9')
        
        
    