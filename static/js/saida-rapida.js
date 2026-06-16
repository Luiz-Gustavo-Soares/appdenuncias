/* ============================================================
   saida-rapida.js — Botão de saída rápida do DEAM
   Camadas de proteção:
     1. sessionStorage sinaliza saída
     2. Script inline no <head> esconde e redireciona antes do paint
     3. pageshow garante redirecionamento mesmo sem event.persisted
     4. visibilitychange cobre retorno por troca de aba
     5. Cache-Control no-store via Django (@never_cache)
   ============================================================ */

const SITE_NEUTRO = 'https://www.google.com';
const CHAVE_SAIDA = 'deam_saida_rapida';


/* ------------------------------------------------------------
   FUNÇÃO PRINCIPAL
   ------------------------------------------------------------ */
function executarSaidaRapida() {
  sessionStorage.setItem(CHAVE_SAIDA, '1');
  window.location.href = SITE_NEUTRO;
}


/* ------------------------------------------------------------
   PAGESHOW — sem depender de event.persisted
   Cobre bfcache e navegadores que não marcam persisted
   corretamente.
   ------------------------------------------------------------ */
window.addEventListener('pageshow', function () {
  if (sessionStorage.getItem(CHAVE_SAIDA) === '1') {
    document.documentElement.style.visibility = 'hidden';
    location.replace(SITE_NEUTRO);
  }
});


/* ------------------------------------------------------------
   VISIBILITYCHANGE — cobre retorno por troca de aba
   ------------------------------------------------------------ */
document.addEventListener('visibilitychange', function () {
  if (
    document.visibilityState === 'visible' &&
    sessionStorage.getItem(CHAVE_SAIDA) === '1'
  ) {
    document.documentElement.style.visibility = 'hidden';
    location.replace(SITE_NEUTRO);
  }
});


/* ------------------------------------------------------------
   EVENTOS
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