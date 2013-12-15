/**
 * Created with PyCharm.
 * User: geaden
 * Date: 9/15/13
 * Time: 7:25 PM
 * To change this template use File | Settings | File Templates.
 */
function banksAutocomplete() {
    $('#id_bank').autocomplete({
        serviceUrl: '/banks/autocomplete/',
        paramName: 'q',
        zIndex: 9999
    })
}

function clearInputs(form) {
    $(':input', form)
      .not(':button, :submit, :reset, :hidden')
      .val('')
      .removeAttr('checked')
      .removeAttr('selected');
}