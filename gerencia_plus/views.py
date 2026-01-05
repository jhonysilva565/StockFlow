from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponseRedirect
from .models import Gerenciamento, Contato
from django.contrib.auth import authenticate, login as auth_login
from .models import Login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F


def home(request):
    return render(request, 'gerenciamento/index.html')

def cadastro(request):
    return render(request, 'cadastro.html')
        
def inicial(request):
    return render(request, 'inicial.html')

@login_required
def dashboard(request):
    # Aqui estamos pegando o nome do usuário para exibir o "Olá, Gestor!" de forma personalizada
    context = {
        'nome_usuario': request.user.username
    }
    return render(request, 'dashboard.html', context)

from django.shortcuts import render, redirect
from .models import Gerenciamento

def editar_produto(request, pk):
    # Busca o produto garantindo que pertence ao usuário logado
    produto = Gerenciamento.objects.get(pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Atualiza os campos com o que veio do formulário do Modal
        produto.nome_produto = request.POST.get('nome_produto')
        produto.quantidade = request.POST.get('quantidade')
        
        # Trata o preço (troca vírgula por ponto para o banco de dados aceitar)
        preco_raw = request.POST.get('preco').replace('R$', '').replace(',', '.').strip()
        produto.preco = preco_raw
        
        produto.save()
        return redirect('salvo') # Redireciona de volta para a lista
    
@login_required
def salvo(request):
    if request.method == 'POST':
        # --- PARTE PARA SALVAR NOVO PRODUTO ---
        gere = Gerenciamento()
        gere.user = request.user
        gere.nome_produto = request.POST.get('nome-produto')
        gere.quantidade = request.POST.get('quantidade')
        gere.descricao = request.POST.get('descricao')
        gere.peso = request.POST.get('peso-estoque')
        gere.preco = request.POST.get('preco')
        gere.fornecedor = request.POST.get('fornecedor')
        gere.categoria = request.POST.get('categoria')
        gere.data_entrada = request.POST.get('data-entrada')
        gere.save()
        return redirect('salvo')

    else:
        # --- PARTE PARA EXIBIR A LISTA E OS CARDS ---
        produtos = Gerenciamento.objects.filter(user=request.user)
        
        # Cálculos para os Cards (KPIs)
        total_itens = produtos.count()
        quantidade_total = produtos.aggregate(Sum('quantidade'))['quantidade__sum'] or 0
        
        # Cálculo do Valor Total (Preço * Quantidade)
        valor_total = produtos.aggregate(
            total=Sum(F('preco') * F('quantidade'))
        )['total'] or 0

        context = {
            'cadastro_estoque': produtos.order_by('-id'),
            'total_itens': total_itens,
            'quantidade_total': quantidade_total,
            'valor_total': valor_total,
        }

        return render(request, 'estoque.html', context)

@login_required  # Adicione o decorador para garantir que apenas usuários autenticados possam acessar esta view



def avaliar(request):
    return render(request, 'avaliar.html')

def sucesso(request):
    return render(request, 'sucesso.html')

def contato(request):
    return render(request, 'contato.html')

def emailsucesso(request):
    return render(request, 'emailsucesso.html')

def turorial(request):
    return render(request, 'tutorial.html')

def sucesso(request):
    if request.method == 'POST':
        rating = request.POST['rating']
        feedback = request.POST['feedback']
        review = avaliar(rating=rating, feedback=feedback)
        review.save()
        return HttpResponseRedirect('/sucesso/')

    return render(request, 'sucesso.html')

class EstoqueDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Gerenciamento.objects.get(pk=pk)
        except Gerenciamento.DoesNotExist:
            raise Http404
    
    def delete(self, request, pk):
        estoque = self.get_object(pk)
        estoque.delete()
        return Response(status=204)
    
def enviar_formulario(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        mensagem = request.POST['mensagem']

        # Crie um novo objeto Contato e salve-o no banco de dados
        contato = Contato(nome=nome, email=email, mensagem=mensagem)
        contato.save()

        return redirect('emailsucesso')  # Substitua 'sucesso' pela URL da página de sucesso desejada

    return render(request, 'contato.html')
# Substitua 'formulario.html' pelo nome do seu template de formulário


def register(request):
    user_exists_error = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            if User.objects.filter(username=username).exists():
                user_exists_error = True
            elif len([c for c in username if c.isdigit()]) < 3 or len([c for c in password if c.isdigit()]) < 3:
                messages.error(request, 'O nome de usuário e a senha devem conter pelo menos 3 números.')
            else:
                user = User.objects.create_user(username=username, password=password)
                
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('home')
    
    return render(request, 'register.html', {'user_exists_error': user_exists_error})



def login_view(request):
    error_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                
                # Crie uma instância do modelo Login e salve as informações no banco de dados
                login_instance = Login(usuario=username, senha=password)
                login_instance.save()

                return redirect('dashboard')
            else:
                error_message = 'Usuário ou senha inválidos.'
    
    return render(request, 'login.html', {'error_message': error_message})

def politica_de_privacidade(request):
    return render(request, 'politica_de_privacidade.html')

def termos_de_servico(request):
    return render(request, 'termos_de_servico.html')
