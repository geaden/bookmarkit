/**
 * Created with PyCharm.
 * User: geaden
 * Date: 9/15/13
 * Time: 7:25 PM
 * To change this template use File | Settings | File Templates.
 */

function clearInputs(form) {
    $(':input', form)
        .not(':button, :submit, :reset, :hidden')
        .val('')
        .removeAttr('checked')
        .removeAttr('selected');
    $(form + ' .help-block').each(function (key, value) {
        value.remove();
    });
    $(form + ' .has-error').each(function (key, value) {
        $(value).removeClass('has-error');
    });
    var $tags = $('#id_tags').val().split(',');
    for (var i = 0; i < $tags.length; i++) {
        $('#id_tags').removeTag($tags[i]);
    }
}

$(document).ready(function () {
    $('.bookmark-tag').tooltip({
        placement: 'right'
    });
    // Clear inputs
    $('#saveBookmark').on('hide.bs.modal', function (e) {
        clearInputs('#bookmark-save-form');
    });
    // Show form and recall values
    $('#saveBookmark').on('hidden.bs.modal', function (e) {
        $('#bookmark-save-form').show();
        $('#saveBookmark .modal-body #bookmark-saved').remove();
        $('#saveBookmark .modal-footer').remove();
        $('#bookmark-save-form input[type=submit]').val('Save');
    });
});