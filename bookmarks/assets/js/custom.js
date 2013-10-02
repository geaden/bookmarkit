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

function updateAccounts() {
    $.get('/accounts/list/?ajax', function(data) {
        console.debug(data);
        var addedAccount = data[0].fields;
        // TODO: user templater
        $('tbody').append(
            '<tr>' +
            '<td>' + addedAccount.name + '</td>' +
            '<td>' + (addedAccount.account_bank !== null) ?
                '<a href="">' + addedAccount.account_bank + '</a>' : '' + '</td>' +
            '<td>' + addedAccount.account_number + '</td>' +
            '<td>' + addedAccount.amount + '</td>' +
            '</tr>'
        )
    })
}


function saveAccount() {
    var form = $('#account_form');
    var url = form.attr('action');

    $('#save_account').click(function(e) {
        e.preventDefault();
        console.debug(form.serializeArray());
        $.ajax({
            url: url + '?ajax',
            method: 'post',
            data: form.serializeArray(),
            statusCode: {
                400: function(error) {
                    // Mark as error field
                    var errors = $.parseJSON(error.responseText);
                    for (field in errors) {
                        $(form.find("#id_" + field).get(0)).parent().addClass('has-error');
                        $(form.find("#id_" + field).get(0)).after(
                            errors[field].map(function(val){
                                return '<span class="help-block">' + val + '</span>';
                            }).join()
                        );
                    };
                    // Get rid of error class on field change
                    form.find("input, textarea, select").one("keypress change", function(){
                        $(this).parent().removeClass('has-error');
                        console.log($(this).siblings("help-block"));
                        $(this).siblings(".help-block").first().remove();
                    });
                },
                200: function(success) {
                    clearInputs('#account_form');
                    $('#add_account_modal').modal('hide');
                    updateAccounts();
                }
            }
        })
    })
}


$(document).ready(function() {
    $("#add").tooltip();
    $("#add").click(function() {
        $("#add_account_modal").modal('show');
    });
    banksAutocomplete();
    saveAccount()
})