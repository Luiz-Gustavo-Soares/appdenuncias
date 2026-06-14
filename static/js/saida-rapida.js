/* ============================================================
   saida-rapida.js — Botão de saída rápida do DEAM
   Responsabilidades:
     - Ao clicar, redirecionar imediatamente para site neutro
     - Bloquear retorno via botão "Voltar" do navegador
     - Permitir retorno via URL digitada, link interno ou externo
   ============================================================ */


/* ------------------------------------------------------------
   1. CONFIGURAÇÃO
   ------------------------------------------------------------ */
const SITE_NEUTRO = 'https://www.google.com';
const CHAVE_SAIDA = 'deam_saida_rapida';


/* ------------------------------------------------------------
   2. VERIFICAÇÃO DE NAVEGAÇÃO INTENCIONAL
   Detecta se a usuária chegou à página de forma intencional
   (URL digitada, link interno ou link externo) e limpa o
   sinalizador de saída rápida se for o caso.
   ------------------------------------------------------------ */
(function verificarNavegacaoIntencional() {
  if (sessionStorage.getItem(CHAVE_SAIDA) !== '1') return;

  const nav = performance.getEntriesByType('navigation')[0];

  // 'navigate'      = URL digitada, link clicado (interno ou externo)
  // 'back_forward'  = botão Voltar/Avançar do navegador
  // 'reload'        = F5 / recarregar
  // 'prerender'     = pré-renderização do navegador
  const tipo = nav?.type ?? 'navigate';

  if (tipo === 'navigate') {
    // Chegou por link ou URL — navegação intencional, libera acesso
    sessionStorage.removeItem(CHAVE_SAIDA);
  }

  // 'back_forward' e 'reload' mantém o sinalizador ativo,
  // o bloqueio será aplicado pelos eventos abaixo
})();


/* ------------------------------------------------------------
   3. FUNÇÃO PRINCIPAL
   ------------------------------------------------------------ */
function executarSaidaRapida() {
  sessionStorage.setItem(CHAVE_SAIDA, '1');
  window.location.replace(SITE_NEUTRO);
}


/* ------------------------------------------------------------
   4. DETECÇÃO DE RETORNO VIA BOTÃO "VOLTAR"
   ------------------------------------------------------------ */

// Restauração via bfcache (cache de navegação do navegador)
window.addEventListener('pageshow', function (e) {
  if (e.persisted && sessionStorage.getItem(CHAVE_SAIDA) === '1') {
    window.location.replace(SITE_NEUTRO);
  }
});

// Aba volta ao foco
document.addEventListener('visibilitychange', function () {
  if (
    document.visibilityState === 'visible' &&
    sessionStorage.getItem(CHAVE_SAIDA) === '1'
  ) {
    window.location.replace(SITE_NEUTRO);
  }
});


/* ------------------------------------------------------------
   5. EVENTOS
   ------------------------------------------------------------ */
const btnSaidaRapida = document.getElementById('btn-saida-rapida');

if (btnSaidaRapida) {
  btnSaidaRapida.addEventListener('click', executarSaidaRapida);

  // Atalho de teclado: Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      executarSaidaRapida();
    }
  });
}