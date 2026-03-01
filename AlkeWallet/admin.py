from django.contrib import admin
from .models import Wallet, Transaction, Contact

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'account_number', 'created_at']
    readonly_fields = ['account_number', 'created_at']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'sender', 'receiver', 'amount', 'tipo', 'status', 'created_at']
    list_filter = ['tipo', 'status']
    readonly_fields = ['reference', 'created_at']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['owner', 'contact_user', 'alias', 'created_at']
