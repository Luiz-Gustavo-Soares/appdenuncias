/* ============================================================
   saida-rapida.js — Botão de saída rápida do DEAM
   Responsabilidades:
     - Ao clicar, substituir a entrada atual do histórico
       do navegador por um site neutro (sem deixar rastro)
     - Redirecionar imediatamente para esse site neutro
     - Preservar o progresso salvo no localStorage,
       permitindo que a usuária retome depois
   ============================================================ */


/* ------------------------------------------------------------
   1. CONFIGURAÇÃO
   Site neutro para o qual a usuária será redirecionada.
   Escolha um site comum e inofensivo que não levante suspeitas.
   ------------------------------------------------------------ */
const SITE_NEUTRO = 'https://www.google.com';


/* ------------------------------------------------------------
   2. FUNÇÃO PRINCIPAL
   ------------------------------------------------------------ */

/**
 * Executa a saída rápida:
 *   1. Substitui todas as entradas do histórico acessíveis
 *      pela URL do site neutro (apaga o rastro do DEAM)
 *   2. Redireciona para o site neutro imediatamente
 *
 * O progresso salvo no localStorage é preservado
 * para que a usuária possa retomar quando estiver segura.
 */
function executarSaidaRapida() {
  // location.replace redireciona sem adicionar entrada no histórico,
  // então o botão "Voltar" do navegador não retorna ao DEAM.
  window.location.replace(SITE_NEUTRO);
}


/* ------------------------------------------------------------
   3. EVENTO
   ------------------------------------------------------------ */
const btnSaidaRapida = document.getElementById('btn-saida-rapida');

if (btnSaidaRapida) {
  btnSaidaRapida.addEventListener('click', executarSaidaRapida);

  // Atalho de teclado: tecla Escape também aciona a saída rápida.
  // Útil se a usuária não conseguir clicar no botão a tempo.
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      executarSaidaRapida();
    }
  });
}