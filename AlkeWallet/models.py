from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    account_number = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billetera de {self.user.username} - Saldo: ${self.balance}"

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = str(uuid.uuid4().int)[:10]
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


class Contact(models.Model):
    TIPO_CUENTA_CHOICES = [
        ('vista', 'Cuenta Vista'),
        ('corriente', 'Cuenta Corriente'),
        ('ahorro', 'Cuenta de Ahorro'),
    ]
    BANCO_CHOICES = [
        ('banco_estado', 'BancoEstado'),
        ('banco_chile', 'Banco de Chile'),
        ('santander', 'Santander'),
        ('bci', 'BCI'),
        ('scotiabank', 'Scotiabank'),
        ('itau', 'Itaú'),
        ('falabella', 'Banco Falabella'),
        ('ripley', 'Banco Ripley'),
        ('security', 'Banco Security'),
        ('consorcio', 'Banco Consorcio'),
        ('bice', 'BICE'),
        ('hsbc', 'HSBC'),
        ('internacional', 'Banco Internacional'),
        ('coopeuch', 'Coopeuch'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    contact_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_by', null=True, blank=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    numero_cuenta = models.CharField(max_length=30)
    tipo_cuenta = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES)
    banco = models.CharField(max_length=30, choices=BANCO_CHOICES)
    alias = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'numero_cuenta')

    def __str__(self):
        return f"{self.nombre} — {self.get_banco_display()}"
    
    
class Transaction(models.Model):
    TIPO_CHOICES = [
        ('deposito', 'Depósito'),
        ('envio', 'Envío'),
        ('recepcion', 'Recepción'),
    ]
    STATUS_CHOICES = [
        ('completado', 'Completado'),
        ('pendiente', 'Pendiente'),
        ('fallido', 'Fallido'),
    ]

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completado')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = str(uuid.uuid4().int)[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"TX#{self.reference} - {self.tipo} ${self.amount}"

    class Meta:
        ordering = ['-created_at']
