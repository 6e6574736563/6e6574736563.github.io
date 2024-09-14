(function() {

  document.addEventListener('DOMContentLoaded', function() {
    const config = window.challConfig;
    const form = document.getElementById('answerForm');
    if (form) {
      form.addEventListener('submit', function(e) {
        e.preventDefault();

        const inputText = document.getElementById('inputText').value.toUpperCase();
        const inputHash = CryptoJS.MD5(inputText).toString();

        if (inputHash === config.h) {
          if (config.n === 'None') {
            //TODO: obfuscate the pincode
            document.getElementById('result').innerHTML = '<div class="alert alert-success d-flex justify-content-between align-items-center" role="alert"><span>Gratulerer, du har fullført alle oppgavene!<br>Koden til skapet: 123456789</span>';
          } else {
            document.getElementById('result').innerHTML = '<div class="alert alert-success d-flex justify-content-between align-items-center" role="alert"><span>Riktig svar, bra jobba!</span><a href="'+config.n+'" class="text-success"><i class="fa-solid fa-arrow-right"></i></a>';
          }

        } else {
          document.getElementById('result').innerHTML = '<div class="alert alert-danger">Feil svar prøv igjen</div>';
        }
      });
    }
  });
})();