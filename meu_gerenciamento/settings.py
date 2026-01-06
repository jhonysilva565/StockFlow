import os
from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave de segurança (Mantenha em segredo em produção!)
SECRET_KEY = 'django-insecure-d@zvbv4y89a@qbhpvb&#=_$myh_z-^0ru+t^wbj#h&+vz$_gb3'

DEBUG = True

ALLOWED_HOSTS = ['stockflow-5iie.onrender.com', 'localhost', '127.0.0.1']

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

# ID do site (Obrigatório para o framework sites do Django)
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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

# --- BANCO DE DADOS (POSTGRESQL) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stockflow_db',
        'USER': 'postgres',
        'PASSWORD': 'jhony008',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# --- BACKENDS DE AUTENTICAÇÃO ---
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# --- CONFIGURAÇÕES ALLAUTH (ATUALIZADAS PARA DJANGO 6.0) ---

# Configura o Google para sempre pedir seleção de conta (prompt)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'AUTH_PARAMS': {
            'prompt': 'select_account',
        },
        'SCOPE': [
            'profile',
            'email',
        ],
    }
}

# Define que o login será feito por e-mail
ACCOUNT_LOGIN_METHODS = {'email'}

# Define campos obrigatórios no cadastro
ACCOUNT_SIGNUP_FIELDS = ['email'] 

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_UNIQUE_EMAIL = True

# Login Social - Comportamento
SOCIALACCOUNT_LOGIN_ON_GET = False 
SOCIALACCOUNT_AUTO_SIGNUP = True   
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

# Redirecionamento
LOGIN_REDIRECT_URL = '/dashboard/' 
LOGOUT_REDIRECT_URL = '/login/' 

# --- VALIDAÇÃO E INTERNACIONALIZAÇÃO ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- ARQUIVOS ESTÁTICOS ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'