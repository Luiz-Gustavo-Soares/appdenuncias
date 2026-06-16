/* ============================================================
   triagem.js — Wizard de triagem da landing page
   Responsabilidades:
     - Controlar qual passo está visível
     - Aplicar lógica condicional entre passos
     - Atualizar barra de progresso e label do passo
     - Salvar e restaurar progresso no localStorage
     - Exibir aviso de perigo imediato (passo 1 = Sim)
   ============================================================ */


/* ------------------------------------------------------------
   1. ESTADO
   Objeto central que representa onde a usuária está
   e o que ela respondeu até agora.
   ------------------------------------------------------------ */
const estado = {
  passoAtual: '1',       // ID do passo visível (string, pois bate com os IDs do HTML)
  historico:  [],        // Pilha de passos anteriores, usada pelo botão Voltar
  respostas:  {},        // { '1': 'nao', '2': 'sim', '2b': 'encerrada', '3': 'eu-mesma' }
  endereco:   {},        // Campos preenchidos no passo 4a ou 4b
};

// Chave usada no localStorage
const CHAVE_STORAGE = 'deam_triagem_progresso';

// Percentual de progresso por passo (para a barra laranja)
const PROGRESSO = {
  '1':      25,
  '2':      50,
  '2b':     50,
  'perigo': 100,
  '3':      75,
  '4a':     100,
  '4b':     100,
};

// Label exibido no canto direito do cabeçalho por passo
const LABEL_PASSO = {
  '1':      'Passo 1',
  '2':      'Passo 2',
  '2b':     'Passo 2',
  'perigo': 'Atenção',
  '3':      'Passo 3',
  '4a':     'Passo 4',
  '4b':     'Passo 4',
};


/* ------------------------------------------------------------
   2. REFERÊNCIAS AO DOM
   ------------------------------------------------------------ */
const btnVoltar      = document.getElementById('painel-voltar');
const labelPasso     = document.getElementById('painel-passo-label');
const barraFill      = document.getElementById('painel-barra-fill');
const barra          = barraFill?.parentElement;

// Todos os blocos de conteúdo de passo
const todosPascos    = document.querySelectorAll('.painel-triagem__passo-conteudo');

// Botões de avançar (passo 4a e 4b)
const btnAvancar4a   = document.getElementById('btn-avancar-4a');
const btnAvancar4b   = document.getElementById('btn-avancar-4b');


/* ------------------------------------------------------------
   3. FUNÇÕES DE EXIBIÇÃO
   ------------------------------------------------------------ */

/**
 * Esconde todos os passos e exibe apenas o de ID informado.
 * @param {string} idPasso - ID do elemento a exibir (ex: 'passo-1')
 */
function mostrarPasso(idPasso) {
  todosPascos.forEach(el => el.hidden = true);

  const alvo = document.getElementById(`passo-${idPasso}`);
  if (alvo) alvo.hidden = false;
}

/**
 * Atualiza a barra de progresso e o label do cabeçalho.
 * @param {string} passo - Chave do passo atual
 */
function atualizarCabecalho(passo) {
  const pct = PROGRESSO[passo] ?? 25;
  barraFill.style.width = `${pct}%`;

  // Atualiza aria para leitores de tela
  if (barra) {
    barra.setAttribute('aria-valuenow', pct);
  }

  labelPasso.textContent = LABEL_PASSO[passo] ?? `Passo ${passo}`;
}

/**
 * Habilita ou desabilita o botão Voltar.
 */
function atualizarBotaoVoltar() {
  btnVoltar.disabled = estado.historico.length === 0;
}

/**
 * Navega para um novo passo, empilhando o atual no histórico.
 * @param {string} proximoPasso - ID do próximo passo
 */
function irPara(proximoPasso) {
  estado.historico.push(estado.passoAtual);
  estado.passoAtual = proximoPasso;

  mostrarPasso(proximoPasso);
  atualizarCabecalho(proximoPasso);
  atualizarBotaoVoltar();
  salvarProgresso();
}

/**
 * Volta ao passo anterior usando o histórico.
 */
function voltarPasso() {
  if (estado.historico.length === 0) return;

  const passoAnterior = estado.historico.pop();
  estado.passoAtual   = passoAnterior;

  mostrarPasso(passoAnterior);
  atualizarCabecalho(passoAnterior);
  atualizarBotaoVoltar();
  salvarProgresso();
}


/* ------------------------------------------------------------
   4. STATE MACHINE — FLUXO DE PASSOS
   Cada passo mapeia suas respostas possíveis para o próximo
   passo. Para adicionar ou alterar o fluxo, basta editar
   este objeto — sem tocar na lógica de navegação.
   ------------------------------------------------------------ */
const FLUXO = {
  '1': {
    'sim': 'perigo',  // Perigo imediato — exibe aviso
    'nao': '2',
  },
  '2': {
    'sim': '2b',      // Já registrou antes — pergunta situação
    'nao': '3',
  },
  '2b': {
    'encerrada': '3', // Qualquer resposta avança para passo 3
    'andamento': '3',
    'incerto':   '3',
  },
  '3': {
    'eu-mesma':    '4a',
    'outra-pessoa':'4b',
  },
};

/**
 * Consulta o FLUXO e navega para o próximo passo.
 * Se o passo não tiver próximo no FLUXO (ex: 4b com "incerto"),
 * finaliza a triagem diretamente.
 * @param {string} passo - Passo atual
 * @param {string} valor - Resposta da usuária
 */
function decidirProximoPasso(passo, valor) {
  estado.respostas[passo] = valor;

  const proximo = FLUXO[passo]?.[valor];

  if (proximo) {
    irPara(proximo);
    return;
  }

  // Passo 4b — "Não tenho certeza": finaliza sem endereço
  if (passo === '4b') {
    estado.endereco = { tipo: 'terceiro', incerto: true };
    finalizarTriagem();
  }
}


/* ------------------------------------------------------------
   5. MODAL DE INSTRUÇÕES
   Exibido após o preenchimento do endereço,
   antes de redirecionar para o registro.
   ------------------------------------------------------------ */
const modalInstrucoes = document.getElementById('modal-instrucoes');
const modalOverlay    = document.getElementById('modal-overlay');

/**
 * Abre o modal de instruções salvando o progresso antes.
 */
function abrirModal() {
  salvarProgresso();

  modalInstrucoes.hidden = false;
  modalOverlay.hidden    = false;
  document.body.style.overflow = 'hidden'; // trava scroll da página

  // Foco no modal para acessibilidade
  modalInstrucoes.focus();
}

/**
 * Fecha o modal de instruções.
 */
function fecharModal() {
  modalInstrucoes.hidden = true;
  modalOverlay.hidden    = true;
  document.body.style.overflow = '';
}

// Fecha o modal ao clicar no overlay
modalOverlay?.addEventListener('click', fecharModal);

// Botão "Iniciar" — submete o form oculto ao Django
document.getElementById('btn-iniciar')?.addEventListener('click', function () {
  localStorage.removeItem(CHAVE_STORAGE); // triagem concluída
  document.getElementById('form-triagem').submit();
});

// Fecha o modal com Escape
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape' && !modalInstrucoes?.hidden) {
    fecharModal();
  }
});

/**
 * Lê os campos de endereço de um passo (4a ou 4b) e retorna objeto.
 * @param {string} prefixo - 'end' para 4a, 'end2' para 4b
 * @returns {object}
 */
function coletarEndereco(prefixo) {
  return {
    logradouro:  document.getElementById(`${prefixo}-logradouro`)?.value.trim()  || '',
    numero:      document.getElementById(`${prefixo}-numero`)?.value.trim()      || '',
    bairro:      document.getElementById(`${prefixo}-bairro`)?.value.trim()      || '',
    cidade:      document.getElementById(`${prefixo}-cidade`)?.value.trim()      || '',
    estado_uf:   document.getElementById(`${prefixo}-estado`)?.value.trim()      || '',
    complemento: document.getElementById(`${prefixo}-complemento`)?.value.trim() || '',
  };
}

/**
 * Valida que ao menos logradouro e cidade foram preenchidos.
 * @param {object} endereco
 * @returns {boolean}
 */
function enderecoValido(endereco) {
  return endereco.logradouro.length > 0 && endereco.cidade.length > 0;
}

/**
 * Finaliza a triagem: salva endereço no estado e abre o modal de instruções.
 * O submit do form oculto acontece quando a usuária clica "Iniciar".
 */
function finalizarTriagem() {
  salvarProgresso();
  preencherFormOculto();
  abrirModal();
}

/**
 * Preenche os campos do form oculto com os dados coletados na triagem.
 */
function preencherFormOculto() {
  const r = estado.respostas;
  const e = estado.endereco;

  document.getElementById('f-perigo-imediato').value     = r['1']  || '';
  document.getElementById('f-ocorrencia-anterior').value = r['2']  || '';
  document.getElementById('f-situacao-anterior').value   = r['2b'] || '';
  document.getElementById('f-vitima').value              = r['3']  || '';
  document.getElementById('f-end-logradouro').value      = e.logradouro  || '';
  document.getElementById('f-end-numero').value          = e.numero      || '';
  document.getElementById('f-end-bairro').value          = e.bairro      || '';
  document.getElementById('f-end-cidade').value          = e.cidade      || '';
  document.getElementById('f-end-estado').value          = e.estado_uf   || '';
  document.getElementById('f-end-complemento').value     = e.complemento || '';
}


/* ------------------------------------------------------------
   6. PERSISTÊNCIA (localStorage)
   ------------------------------------------------------------ */

/**
 * Salva o estado atual no localStorage para retomada posterior.
 */
function salvarProgresso() {
  const dados = {
    passoAtual: estado.passoAtual,
    historico:  estado.historico,
    respostas:  estado.respostas,
    endereco:   estado.endereco,
  };
  localStorage.setItem(CHAVE_STORAGE, JSON.stringify(dados));
}

/**
 * Tenta restaurar um progresso salvo anteriormente.
 * Se existir, pergunta à usuária se deseja continuar.
 */
function restaurarProgressoSeExistir() {
  const raw = localStorage.getItem(CHAVE_STORAGE);
  if (!raw) return;

  let dados;
  try {
    dados = JSON.parse(raw);
  } catch {
    localStorage.removeItem(CHAVE_STORAGE);
    return;
  }

  // Só restaura se havia progresso real (além do passo 1)
  if (!dados.passoAtual || dados.passoAtual === '1') {
    localStorage.removeItem(CHAVE_STORAGE);
    return;
  }

  const desejaContinuar = window.confirm(
    'Você tem um registro em andamento. Deseja continuar de onde parou?'
  );

  if (desejaContinuar) {
    Object.assign(estado, dados);
    mostrarPasso(estado.passoAtual);
    atualizarCabecalho(estado.passoAtual);
    atualizarBotaoVoltar();
  } else {
    localStorage.removeItem(CHAVE_STORAGE);
  }
}


/* ------------------------------------------------------------
   7. EVENTOS
   ------------------------------------------------------------ */

// Botão Voltar
btnVoltar.addEventListener('click', voltarPasso);

// Botões de opção (Sim, Não, Eu mesma, etc.) — delegação no painel inteiro
document.querySelector('.painel-triagem')?.addEventListener('click', function (e) {
  const btn = e.target.closest('[data-passo][data-valor]');
  if (!btn) return;

  const passo = btn.dataset.passo;
  const valor = btn.dataset.valor;

  decidirProximoPasso(passo, valor);
});

// Botão Continuar do passo 4a (endereço próprio)
btnAvancar4a?.addEventListener('click', function () {
  const endereco = coletarEndereco('end');

  if (!enderecoValido(endereco)) {
    alert('Por favor, preencha ao menos o logradouro e a cidade.');
    return;
  }

  estado.endereco = { tipo: 'proprio', ...endereco };
  finalizarTriagem();
});

// Botão Continuar do passo 4b (endereço de outra pessoa)
btnAvancar4b?.addEventListener('click', function () {
  const endereco = coletarEndereco('end2');

  if (!enderecoValido(endereco)) {
    alert('Por favor, preencha ao menos o logradouro e a cidade.');
    return;
  }

  estado.endereco = { tipo: 'terceiro', ...endereco };
  finalizarTriagem();
});


/* ------------------------------------------------------------
   10. INICIALIZAÇÃO E RETOMADA
   ------------------------------------------------------------ */
window.addEventListener('pageshow', function (event) {
  const params = new URLSearchParams(window.location.search);
  
  // 1. Reset manual: Se houver ordem explícita na URL
  if (params.get('reset') === '1') {
    localStorage.removeItem('deam_registro_progresso');
    localStorage.removeItem(CHAVE_STORAGE); // triagem
    window.history.replaceState({}, '', window.location.pathname);
  } else {
    // 2. Acesso limpo: verifica se existe uma denúncia salva no registro
    const rawProgresso = localStorage.getItem('deam_registro_progresso');
    
    if (rawProgresso) {
      try {
        const dados = JSON.parse(rawProgresso);
        
        // Verifica se realmente há dados preenchidos
        const temCampos = dados.campos && Object.values(dados.campos).some(v => String(v).trim() !== '');
        
        // CORREÇÃO: Removemos a dependência estrita do "dados.cod_denuncia" existir
        if (temCampos) {
          // Pequeno timeout garante a renderização visual do HTML antes de travar a tela
          setTimeout(() => {
            const desejaContinuar = window.confirm(
              'Identificamos uma denúncia em andamento. Deseja continuar de onde parou?'
            );

            if (desejaContinuar) {
              // Se tiver um código, usa a URL específica. Se não tiver, vai para a URL base.
              const urlDestino = dados.cod_denuncia 
                ? `/denuncia/registro/${dados.cod_denuncia}/` 
                : '/denuncia/registro/';
                
              window.location.href = urlDestino;
            } else {
              // Usuária recusou: apaga a denúncia da memória e inicia triagem do zero
              localStorage.removeItem('deam_registro_progresso');
              iniciarTriagemLimpa();
            }
          }, 100);
          
          return; // Para a execução do script aqui para não sobrepor telas
        }
      } catch (e) {
        localStorage.removeItem('deam_registro_progresso');
      }
    }
  }

  // 3. Fluxo normal: se não achou denúncia no formulário, inicia a triagem
  iniciarTriagemLimpa();
});

/**
 * Função auxiliar para montar a tela de triagem original
 */
function iniciarTriagemLimpa() {
  mostrarPasso('1');
  atualizarCabecalho('1');
  atualizarBotaoVoltar();
  restaurarProgressoSeExistir(); // Esta função no triagem.js restaura APENAS rascunho de triagem
}