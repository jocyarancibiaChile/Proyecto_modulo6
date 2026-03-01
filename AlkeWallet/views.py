from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction as db_transaction
from django.db.models import Q, Sum
from AlkeWallet.models import Wallet, Transaction, Contact
from .forms import RegistroForm, DepositoForm, EnvioDineroForm, AgregarContactoForm
from decimal import Decimal
from django.db import transaction

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'AlkeWallet/index.html')


def registro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'¡Bienvenido, {user.first_name}! Tu billetera fue creada.')
        return redirect('dashboard')
    return render(request, 'AlkeWallet/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'AlkeWallet/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    wallet = request.user.wallet
    recent_transactions = Transaction.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )[:5]
    total_enviado = Transaction.objects.filter(sender=request.user, tipo='envio').aggregate(Sum('amount'))['amount__sum'] or 0
    total_recibido = Transaction.objects.filter(receiver=request.user, tipo='recepcion').aggregate(Sum('amount'))['amount__sum'] or 0
    total_depositos = Transaction.objects.filter(receiver=request.user, tipo='deposito').aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'wallet': wallet,
        'recent_transactions': recent_transactions,
        'total_enviado': total_enviado,
        'total_recibido': total_recibido,
        'total_depositos': total_depositos,
    }
    return render(request, 'AlkeWallet/dashboard.html', context)


@login_required
def deposito(request):
    form = DepositoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']
        description = form.cleaned_data.get('description', '')
        with db_transaction.atomic():
            wallet = request.user.wallet
            wallet.balance += Decimal(amount)
            wallet.save()
            Transaction.objects.create(
                receiver=request.user,
                amount=amount,
                tipo='deposito',
                status='completado',
                description=description or f'Depósito de ${amount}',
            )
        messages.success(request, f'¡Depósito de ${amount} realizado con éxito!')
        return redirect('dashboard')
    return render(request, 'AlkeWallet/deposito.html', {'form': form})



@login_required
def envio_dinero(request):
    contacts = Contact.objects.filter(owner=request.user)
    print("CONTACTOS:", list(contacts.values('nombre', 'numero_cuenta')))
    opciones = [('', '— Seleccioná un contacto —')]
    if contacts.exists():
        opciones += [(c.numero_cuenta, f"{c.nombre} — {c.get_banco_display()} N° {c.numero_cuenta}") for c in contacts]
    else:
        opciones += [('', 'No tenés contactos guardados')]

    form = EnvioDineroForm(request.POST or None)
    form.fields['destinatario'].choices = opciones

    if request.method == 'POST' and form.is_valid():
        destinatario_cuenta = form.cleaned_data['destinatario']
        amount = Decimal(form.cleaned_data['amount'])
        description = form.cleaned_data.get('description', '')

        try:
            contacto = Contact.objects.get(owner=request.user, numero_cuenta=destinatario_cuenta)
        except Contact.DoesNotExist:
            messages.error(request, 'Contacto no encontrado.')
            return render(request, 'AlkeWallet/envio_dinero.html', {'form': form, 'contacts': contacts})

        wallet = request.user.wallet
        if wallet.balance < amount:
            messages.error(request, 'Saldo insuficiente.')
            return render(request, 'AlkeWallet/envio_dinero.html', {'form': form, 'contacts': contacts})

        with transaction.atomic():
            wallet.balance -= amount
            wallet.save()
            Transaction.objects.create(
                sender=request.user,
                amount=amount,
                tipo='envio',
                status='completado',
                description=description or f'Envío a {contacto.nombre}',
            )
        messages.success(request, f'¡Enviaste ${amount} a {contacto.nombre}!')
        return redirect('dashboard')

    return render(request, 'AlkeWallet/envio_dinero.html', {'form': form, 'contacts': contacts})


@login_required
def transacciones(request):
    tipo_filter = request.GET.get('tipo', '')
    qs = Transaction.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    if tipo_filter:
        qs = qs.filter(tipo=tipo_filter)
    return render(request, 'AlkeWallet/transacciones.html', {
        'transactions': qs,
        'tipo_filter': tipo_filter,
    })


@login_required
def contactos(request):
    form = AgregarContactoForm(request.POST or None)
    contacts = Contact.objects.filter(owner=request.user)

    if request.method == 'POST' and form.is_valid():
        Contact.objects.create(
            owner=request.user,
            nombre=form.cleaned_data['nombre'],
            email=form.cleaned_data.get('email', ''),
            numero_cuenta=form.cleaned_data['numero_cuenta'],
            tipo_cuenta=form.cleaned_data['tipo_cuenta'],
            banco=form.cleaned_data['banco'],
            alias=form.cleaned_data.get('alias', ''),
        )
        messages.success(request, f"Contacto agregado correctamente.")
        return redirect('contactos')

    return render(request, 'AlkeWallet/contactos.html', {'form': form, 'contacts': contacts})

@login_required
def eliminar_contacto(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, owner=request.user)
    contact.delete()
    messages.success(request, 'Contacto eliminado.')
    return redirect('contactos')
