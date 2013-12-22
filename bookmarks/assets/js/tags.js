/**
 * Created with PyCharm.
 * User: geaden
 * Date: 15/12/13
 * Time: 18:13
 * To change this template use File | Settings | File Templates.
 */


$(document).ready(function() {
    $('#id_tags').tagsInput({
        autocomplete_url: '/tags/autocomplete/',
        autocomplete: {
            selectFirst: true,
            width: '100px',
            autoFill: true
        },
        height: '45px',
        width: '100%',
        defaultText: 'Tags'
    });

    $('div.tagsinput input').on('focus', function() {
        console.log('focused');
        $('div.tagsinput').addClass('focused');
    }).on('blur', function() {
        $('div.tagsinput').removeClass('focused');
    });
})
