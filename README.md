# Sistema de Registro e Gestão de Denúncias

Sistema web desenvolvido em Django para registro, acompanhamento e auditoria de denúncias, permitindo o preenchimento de questionários estruturados, anexação de evidências e geração de relatórios em PDF.

## Objetivo

O projeto tem como objetivo fornecer uma plataforma para coleta padronizada de informações relacionadas a denúncias, auxiliando no registro, análise e encaminhamento dos casos.

## Funcionalidades

- Cadastro de denúncias
- Questionário estruturado para coleta de informações
- Upload de evidências (imagens, documentos e outros arquivos)
- Geração automática de relatório em PDF
- Painel administrativo para auditoria das denúncias
- Controle de status da denúncia
- Histórico de movimentação do caso
- Validação de dados através de Django Forms

## Tecnologias Utilizadas

- Python 3
- Django
- uuid4
- WeasyPrint
- HTML5
- CSS3
- JavaScript

## Arquitetura

O projeto utiliza a arquitetura MVT (Model-View-Template) fornecida pelo Django.

Além disso, aplica o padrão de projeto State para controle do fluxo de estados das denúncias:

```text
Rascunho
    ↓
Salvo
    ↓
Validada
    ↓
Encaminhada
    ↓
Finalizada
```

Cada estado possui regras específicas para determinar quais operações podem ser executadas.

## Pré-requisitos

Antes de executar o projeto, certifique-se de possuir instalado:

- Python 3.10 ou superior
- Git

## Instalação

### Clonar o repositório

```bash
git clone https://github.com/Luiz-Gustavo-Soares/appdenuncias.git
cd app-denuncia
```

### Criar ambiente virtual

Linux:

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```cmd
python -m venv venv
venv\Scripts\activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

## Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta

DEBUG=True
ALLOWED_HOSTS=127.0.0.1
```

## Configuração do Banco de Dados


Aplicar migrações:

```bash
python manage.py migrate
```

## Criar Usuário Administrador

```bash
python manage.py createsuperuser
```

## Executar o Projeto

```bash
python manage.py runserver
```

A aplicação estará disponível em:

```text
http://127.0.0.1:8000/
```

Painel administrativo:

```text
http://127.0.0.1:8000/admin/
```

## Executar o Projeto em Produção
Preparar o ambiente
```bash
./build.sh
```

Execuçao
```bash
gunicorn appdenuncias.wsgi:application
```


## Arquivos de Mídia

Os arquivos enviados pelos usuários são armazenados no diretório:

```text
media/
```

Certifique-se de que as seguintes configurações existam no `settings.py`:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```



## Fluxo de Trabalho

1. Usuário registra uma denúncia.
2. Sistema valida os dados enviados.
3. Evidências são armazenadas.
4. A denúncia recebe status inicial.
5. Administradores realizam auditoria.
6. O sistema gera relatórios PDF quando necessário.
7. A denúncia pode ser encaminhada e finalizada.
