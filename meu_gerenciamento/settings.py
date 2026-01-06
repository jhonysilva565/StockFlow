import os
from pathlib import Path
import dj_database_url

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave de segurança (Mantenha em segredo em produção!)
SECRET_KEY = 'django-insecure-d@zvbv4y89a@qbhpvb&#=_$myh_z-^0ru+t^wbj#h&+vz$_gb3'

# Mantenha True para testes, mas mude para False quando o site estiver pronto para o público final
DEBUG = True

ALLOWED_HOSTS = ['stockflow-5iie.onrender.com', 'localhost', '127.0.0.1', '*']

# --- CONFIGURAÇÃO DE APLICATIVOS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    
    # Apps do Projeto
    'gerencia_plus',
    
    # Apps Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Adicionado para carregar CSS na nuvem
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'meu_gerenciamento.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meu_gerenciamento.wsgi.application'

# --- BANCO DE DADOS (CONFIGURAÇÃO AUTOMÁTICA) ---
# Aqui ele tenta ler o banco do Render. Se não achar, usa o seu local.
DATABASES = {
    'default': dj_database_url.config(
        # COLE A "EXTERNAL DATABASE URL" DO RENDER ENTRE AS ASPAS ABAIXO:
        default='postgresql://jhony008:I1LgMut52tFCzqaQh0EgI6AGBtnEWJmw@dpg-d5ej7t63jp1c73dep0sg-a.oregon-postgres.render.com/stockflow_6axy',
        conn_max_age=600
    )
}

# --- BACKENDS DE AUTENTICAÇÃO ---
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'AUTH_PARAMS': {'prompt': 'select_account'},
        'SCOPE': ['profile', 'email'],
    }
}

ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email'] 
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET = False 
SOCIALACCOUNT_AUTO_SIGNUP = True   
SOCIALACCOUNT_QUERY_EMAIL = True

LOGIN_REDIRECT_URL = '/dashboard/' 
LOGOUT_REDIRECT_URL = '/login/' 

# --- VALIDAÇÃO E INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- ARQUIVOS ESTÁTICOS ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Necessário para o Render
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'