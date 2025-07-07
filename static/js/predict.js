// static/js/predict.js
$(function () {
  const USD_RATE = 85.75;                         
  const $btn   = $('#submitBtn'),
        $spin  = $btn.find('.spinner-border'),
        $text  = $btn.find('.btn-text'),
        $alert = $('#resultCard');

  function fmtPrice(rupees, cur) {
    if (cur === 'usd') {
      return '$ ' + (rupees / USD_RATE).toFixed(2);
    }
    return '₹ ' + rupees.toFixed(2);
  }

  $('#predictionForm').on('submit', function (e) {
    e.preventDefault();
    $alert.addClass('d-none');
    $spin.removeClass('d-none');  $text.text('Predicting…');

    $.post('/predict', $(this).serialize())
      .done(res => {
        $alert.data('rupees', Number(res.predicted_price));

        const cur = $('input[name="currency"]:checked').val();
        $alert
          .removeClass('d-none alert-danger')
          .addClass('alert-success')
          .text('Estimated Market Value: ' + fmtPrice(res.predicted_price, cur));
      })
      .fail(xhr => {
        const msg = xhr.responseJSON ? xhr.responseJSON.error : xhr.statusText;
        $alert
          .removeClass('d-none alert-success')
          .addClass('alert-danger')
          .text('Error: ' + msg);
      })
      .always(() => {
        $spin.addClass('d-none');  $text.text('Predict Price');
      });
  });

  $('input[name="currency"]').on('change', function () {
    const rupees = $alert.data('rupees');
    if (!rupees) return;                 
    const cur = $(this).val();
    $alert.text('Estimated Market Value: ' + fmtPrice(rupees, cur));
  });
});