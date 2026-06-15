# Referência de campos dos formulários
Mapeamento completo de todos os `name` dos campos HTML
para uso no backend Django via `request.POST` e `request.FILES`.

---

## 1. Form da Triagem — `form-triagem`
`POST /denuncia/triagem/`

| name                  | tipo    | valores possíveis                                      |
|-----------------------|---------|--------------------------------------------------------|
| `perigo_imediato`     | hidden  | `sim` / `nao`                                          |
| `ocorrencia_anterior` | hidden  | `sim` / `nao`                                          |
| `situacao_anterior`   | hidden  | `encerrada` / `andamento` / `incerto` / _(vazio)_      |
| `vitima`              | hidden  | `eu-mesma` / `outra-pessoa`                            |
| `end_logradouro`      | hidden  | texto livre                                            |
| `end_numero`          | hidden  | texto livre                                            |
| `end_bairro`          | hidden  | texto livre                                            |
| `end_cidade`          | hidden  | texto livre                                            |
| `end_estado`          | hidden  | UF (2 letras)                                          |
| `end_complemento`     | hidden  | texto livre                                            |

**Exemplo de acesso no Django:**
```python
def triagem(request):
    if request.method == 'POST':
        request.session['triagem'] = {
            'perigo_imediato':     request.POST.get('perigo_imediato'),
            'ocorrencia_anterior': request.POST.get('ocorrencia_anterior'),
            'situacao_anterior':   request.POST.get('situacao_anterior'),
            'vitima':              request.POST.get('vitima'),
            'endereco': {
                'logradouro':  request.POST.get('end_logradouro'),
                'numero':      request.POST.get('end_numero'),
                'bairro':      request.POST.get('end_bairro'),
                'cidade':      request.POST.get('end_cidade'),
                'estado':      request.POST.get('end_estado'),
                'complemento': request.POST.get('end_complemento'),
            }
        }
        return redirect('denuncia:registro')
    return redirect('index')
```

---

## 2. Form do Registro — `form-registro`
`POST /denuncia/registro/`
`enctype: multipart/form-data` (necessário por causa dos anexos)

### Etapa 1 — Questionário

| name                  | tipo   | valores possíveis                                                                 |
|-----------------------|--------|-----------------------------------------------------------------------------------|
| `relacao_autora`      | select | `conjuge` / `ex_conjuge` / `namorado` / `ex_namorado` / `familiar` / `conhecido` / `desconhecido` |
| `local_fato`          | select | `residencia_vitima` / `residencia_autor` / `residencia_comum` / `via_publica` / `local_trabalho` / `outro` |
| `risco_iminente`      | radio  | `sim` / `nao` / `nao_sei`                                                        |
| `criancas_envolvidas` | radio  | `sim` / `nao`                                                                    |

### Etapa 2 — Dados Básicos

| name              | tipo  | observação            |
|-------------------|-------|-----------------------|
| `data_fato`       | date  | obrigatório           |
| `hora_fato`       | time  | opcional              |
| `logradouro_fato` | text  | obrigatório           |
| `numero_fato`     | text  | opcional              |
| `bairro_fato`     | text  | obrigatório           |
| `cidade_fato`     | text  | obrigatório           |
| `estado_fato`     | text  | obrigatório, 2 chars  |

### Etapa 3 — Dados da Vítima

| name               | tipo  | observação  |
|--------------------|-------|-------------|
| `vitima_nome`      | text  | obrigatório |
| `vitima_nascimento`| date  | opcional    |
| `vitima_cpf`       | text  | opcional    |
| `vitima_telefone`  | tel   | opcional    |
| `vitima_email`     | email | opcional    |
| `vitima_endereco`  | text  | opcional    |

### Etapa 4 — Dados do Autor

| name                   | tipo     | observação |
|------------------------|----------|------------|
| `autor_nome`           | text     | opcional   |
| `autor_nascimento`     | date     | opcional   |
| `autor_cpf`            | text     | opcional   |
| `autor_caracteristicas`| textarea | opcional   |
| `autor_endereco`       | text     | opcional   |

### Etapa 5 — Veículos Envolvidos

| name            | tipo   | valores possíveis                              |
|-----------------|--------|------------------------------------------------|
| `veiculo_tipo`  | select | `carro` / `moto` / `caminhao` / `onibus` / `outro` |
| `veiculo_placa` | text   | opcional                                       |
| `veiculo_cor`   | text   | opcional                                       |
| `veiculo_modelo`| text   | opcional                                       |

### Etapa 6 — Objetos Envolvidos

| name                 | tipo     | valores possíveis                                                        |
|----------------------|----------|--------------------------------------------------------------------------|
| `objetos_arma`       | select   | `nenhum` / `arma_fogo` / `arma_branca` / `objeto_contundente` / `outro` |
| `objetos_subtraidos` | textarea | opcional                                                                 |

### Etapa 7 — Descrição do Fato

| name           | tipo     | observação  |
|----------------|----------|-------------|
| `descricao_fato` | textarea | obrigatório |
| `testemunhas`  | textarea | opcional    |

### Etapa 8 — Questões Complementares

| name                    | tipo  | valores possíveis        |
|-------------------------|-------|--------------------------|
| `violencia_recorrente`  | radio | `sim` / `nao` / `nao_sei`|
| `medida_protetiva`      | radio | `sim` / `nao` / `nao_sei`|
| `representacao_criminal`| radio | `sim` / `nao` / `nao_sei`|

### Etapa 9 — Anexos

| name      | tipo | observação                                      |
|-----------|------|-------------------------------------------------|
| `anexos`  | file | múltiplos arquivos — acessar via `request.FILES.getlist('anexos')` |

**Exemplo de acesso no Django:**
```python
def registro(request):
    if request.method == 'POST':
        # Campos de texto/select/radio
        dados = request.POST.dict()

        # Arquivos
        anexos = request.FILES.getlist('anexos')

        # Dados da triagem (salvos na sessão anteriormente)
        triagem = request.session.get('triagem', {})

        # ... salvar no banco ...
        return redirect('denuncia:confirmacao')

    return render(request, 'denuncia/registro.html')
```