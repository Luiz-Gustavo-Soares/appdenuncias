/* ============================================================
   registro.js — Formulário de registro de ocorrência
   Responsabilidades:
     - Navegação entre as 9 etapas (abas + botões)
     - Validação dos campos obrigatórios por etapa
     - Atualização do contador "Etapa X de 9"
     - Salvar e restaurar progresso no localStorage
     - Feedback visual da lista de arquivos (etapa 9)
     - Submissão do form na última etapa
   ============================================================ */


/* ------------------------------------------------------------
   1. CONFIGURAÇÃO
   ------------------------------------------------------------ */
const TOTAL_ETAPAS  = 9;
const CHAVE_STORAGE = 'deam_registro_progresso';

// Campos obrigatórios por etapa — IDs dos elementos no HTML
const CAMPOS_OBRIGATORIOS = {
  1: ['relacao_autora', 'local_fato'],
  2: ['data_fato', 'logradouro_fato', 'bairro_fato', 'cidade_fato', 'estado_fato'],
  3: ['vitima_nome'],
  4: [],   // Todos opcionais
  5: [],
  6: [],
  7: ['descricao_fato'],
  8: [],
  9: [],
};


/* ------------------------------------------------------------
   2. ESTADO
   ------------------------------------------------------------ */
const estado = {
  etapaAtual: 1,
};


/* ------------------------------------------------------------
   3. REFERÊNCIAS AO DOM
   ------------------------------------------------------------ */
const form         = document.getElementById('form-registro');
const btnRetornar  = document.getElementById('btn-retornar');
const btnContinuar = document.getElementById('btn-continuar');
const contador     = document.getElementById('registro-contador');
const todasAbas    = document.querySelectorAll('.registro__aba');
const todasEtapas  = document.querySelectorAll('.registro__etapa');
const inputAnexos  = document.getElementById('anexos');
const listaAnexos  = document.getElementById('lista-anexos');


/* ------------------------------------------------------------
   4. NAVEGAÇÃO ENTRE ETAPAS
   ------------------------------------------------------------ */

/**
 * Ativa a etapa informada:
 * - Esconde a etapa atual e mostra a nova
 * - Atualiza a aba ativa
 * - Atualiza o contador e os botões
 * @param {number} novaEtapa
 */
function irParaEtapa(novaEtapa) {
  if (novaEtapa < 1 || novaEtapa > TOTAL_ETAPAS) return;

  // Esconde etapa atual e mostra a nova
  document.getElementById(`etapa-${estado.etapaAtual}`).hidden = true;
  document.getElementById(`etapa-${novaEtapa}`).hidden = false;

  // Atualiza abas
  todasAbas.forEach(aba => {
    const eAtiva = parseInt(aba.dataset.etapa) === novaEtapa;
    aba.classList.toggle('registro__aba--ativa', eAtiva);
    aba.setAttribute('aria-selected', eAtiva ? 'true' : 'false');
  });

  estado.etapaAtual = novaEtapa;

  atualizarContador();
  atualizarBotoes();
  salvarProgresso();

  // Rola para o topo do painel ao trocar de etapa
  form.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Atualiza o texto "Etapa X de 9".
 */
function atualizarContador() {
  contador.textContent = `Etapa ${estado.etapaAtual} de ${TOTAL_ETAPAS}`;
}

/**
 * Atualiza estado dos botões Retornar e Continuar.
 */
function atualizarBotoes() {
  // Retornar: desabilitado na primeira etapa
  btnRetornar.disabled = estado.etapaAtual === 1;

  // Continuar: vira "Enviar" na última etapa
  const eUltimaEtapa = estado.etapaAtual === TOTAL_ETAPAS;

  if (eUltimaEtapa) {
    btnContinuar.textContent = 'Enviar denúncia';
    btnContinuar.classList.add('registro__btn-continuar--enviar');
  } else {
    btnContinuar.innerHTML = `
      Continuar
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <polyline points="9 18 15 12 9 6"/>
      </svg>
    `;
    btnContinuar.classList.remove('registro__btn-continuar--enviar');
  }
}


/* ------------------------------------------------------------
   5. VALIDAÇÃO POR ETAPA
   ------------------------------------------------------------ */

/**
 * Valida os campos obrigatórios da etapa informada.
 * Injeta mensagens de erro nos campos inválidos.
 * @param {number} etapa
 * @returns {boolean} true se todos válidos
 */
function validarEtapa(etapa) {
  const idsObrigatorios = CAMPOS_OBRIGATORIOS[etapa] || [];
  let valido = true;

  // Limpa erros anteriores da etapa
  const secao = document.getElementById(`etapa-${etapa}`);
  secao.querySelectorAll('.campo__erro-msg').forEach(el => el.remove());
  secao.querySelectorAll('.campo__input--erro, .campo__select--erro')
    .forEach(el => el.classList.remove('campo__input--erro', 'campo__select--erro'));

  idsObrigatorios.forEach(id => {
    const campo = document.getElementById(id);
    if (!campo) return;

    const vazio = campo.value.trim() === '' || campo.value === '';

    if (vazio) {
      valido = false;
      marcarErro(campo);
    }
  });

  return valido;
}

/**
 * Marca um campo como inválido e injeta mensagem de erro abaixo dele.
 * @param {HTMLElement} campo
 */
function marcarErro(campo) {
  const classeErro = campo.tagName === 'SELECT'
    ? 'campo__select--erro'
    : 'campo__input--erro';

  campo.classList.add(classeErro);

  // Remove mensagem anterior se existir
  const anterior = campo.parentElement.querySelector('.campo__erro-msg');
  if (anterior) anterior.remove();

  const msg = document.createElement('span');
  msg.className  = 'campo__erro-msg';
  msg.textContent = 'Este campo é obrigatório.';
  campo.insertAdjacentElement('afterend', msg);

  // Remove o erro quando a usuária começar a preencher
  campo.addEventListener('input', function limpar() {
    campo.classList.remove(classeErro);
    msg.remove();
    campo.removeEventListener('input', limpar);
  }, { once: true });
}


/* ------------------------------------------------------------
   6. PERSISTÊNCIA (localStorage)
   ------------------------------------------------------------ */

/**
 * Salva os valores atuais de todos os campos de texto/select
 * e a etapa atual no localStorage.
 */
function salvarProgresso() {
  const dados = {
    etapaAtual: estado.etapaAtual,
    campos:     coletarCampos(),
  };
  localStorage.setItem(CHAVE_STORAGE, JSON.stringify(dados));
}

/**
 * Coleta o valor de todos os inputs, selects e textareas do form.
 * Ignora inputs file (não serializáveis).
 * @returns {object} { id: valor }
 */
function coletarCampos() {
  const resultado = {};
  form.querySelectorAll('input:not([type="file"]), select, textarea').forEach(el => {
    if (!el.name) return;

    if (el.type === 'radio') {
      if (el.checked) resultado[el.name] = el.value;
    } else {
      resultado[el.name] = el.value;
    }
  });
  return resultado;
}

/**
 * Tenta restaurar progresso salvo.
 * Se existir e a etapa for maior que 1, pergunta à usuária.
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

  if (!dados.etapaAtual || dados.etapaAtual <= 1) {
    localStorage.removeItem(CHAVE_STORAGE);
    return;
  }

  const desejaContinuar = window.confirm(
    'Você tem um registro em andamento. Deseja continuar de onde parou?'
  );

  if (!desejaContinuar) {
    localStorage.removeItem(CHAVE_STORAGE);
    return;
  }

  // Restaura valores dos campos
  if (dados.campos) {
    restaurarCampos(dados.campos);
  }

  // Navega para a etapa salva
  irParaEtapa(dados.etapaAtual);
}

/**
 * Preenche os campos do form com os valores salvos.
 * @param {object} campos - { name: valor }
 */
function restaurarCampos(campos) {
  Object.entries(campos).forEach(([name, valor]) => {
    const els = form.querySelectorAll(`[name="${name}"]`);

    els.forEach(el => {
      if (el.type === 'radio') {
        el.checked = el.value === valor;
      } else {
        el.value = valor;
      }
    });
  });
}


/* ------------------------------------------------------------
   7. UPLOAD DE ARQUIVOS (Etapa 9)
   ------------------------------------------------------------ */

/**
 * Atualiza a lista visual de arquivos selecionados.
 */
function atualizarListaAnexos() {
  if (!listaAnexos || !inputAnexos) return;

  listaAnexos.innerHTML = '';

  Array.from(inputAnexos.files).forEach(arquivo => {
    const tamanhoMB = (arquivo.size / 1024 / 1024).toFixed(2);

    const item = document.createElement('li');
    item.innerHTML = `
      <span>${arquivo.name}</span>
      <span>${tamanhoMB} MB</span>
    `;
    listaAnexos.appendChild(item);
  });
}


/* ------------------------------------------------------------
   8. SUBMISSÃO
   ------------------------------------------------------------ */

/**
 * Valida a última etapa e submete o form.
 * Limpa o localStorage ao enviar com sucesso.
 */
function submeterForm() {
  const valido = validarEtapa(TOTAL_ETAPAS);
  if (!valido) return;

  // Limpa progresso salvo — denúncia enviada
  localStorage.removeItem(CHAVE_STORAGE);

  form.submit();
}


/* ------------------------------------------------------------
   9. EVENTOS
   ------------------------------------------------------------ */

// Botão Continuar
btnContinuar.addEventListener('click', function () {
  if (estado.etapaAtual === TOTAL_ETAPAS) {
    submeterForm();
    return;
  }

  const valido = validarEtapa(estado.etapaAtual);
  if (!valido) return;

  irParaEtapa(estado.etapaAtual + 1);
});

// Botão Retornar
btnRetornar.addEventListener('click', function () {
  irParaEtapa(estado.etapaAtual - 1);
});

// Clique nas abas — permite navegar para etapas já visitadas
todasAbas.forEach(aba => {
  aba.addEventListener('click', function () {
    const etapaAlvo = parseInt(aba.dataset.etapa);

    // Só permite ir para etapas anteriores ou a atual
    // (evita pular etapas sem validar)
    if (etapaAlvo < estado.etapaAtual) {
      irParaEtapa(etapaAlvo);
    }
  });
});

// Salva progresso ao sair/atualizar a página
window.addEventListener('beforeunload', salvarProgresso);

// Feedback de arquivos selecionados
inputAnexos?.addEventListener('change', atualizarListaAnexos);


/* ------------------------------------------------------------
   10. INICIALIZAÇÃO
   ------------------------------------------------------------ */
(function init() {
  // Garante que apenas a etapa 1 esteja visível
  todasEtapas.forEach((etapa, i) => {
    etapa.hidden = i !== 0;
  });

  atualizarContador();
  atualizarBotoes();

  // Verifica progresso salvo
  restaurarProgressoSeExistir();
})();