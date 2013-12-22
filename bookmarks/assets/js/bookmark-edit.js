/**
 * Opens modal window to edit bookmark
 *
 * @param e
 * @returns {boolean}
 */
function bookmark_edit(e) {
    e.preventDefault();
    $("#saveBookmark").modal('show');
    var $item = $(this).parent().parent();
    var $data = $($item[0]).find('td');
    var $title = $($data[1]).text();
    var $url = $($data[1]).find('a').attr('href');
    var tags_array = [];
    $($data[2]).find('span').each(function () {
        tags_array.push($(this).text());
    });
    var tags = tags_array.join(',');
    var obj = {title: $title, url: $url, tags: tags};
    console.log();
    $('#id_url').val(obj.url);
    $('#id_title').val(obj.title);
    $('#id_tags').importTags(obj.tags);
    return false;
}

$(document).ready(function () {
    $('a.bookmark-edit').click(bookmark_edit);
    $('a.bookmark-add').click(function(e) {
        e.preventDefault();
        $('#saveBookmark').modal('show');
    });
    $('#bookmark-save-form').submit(bookmark_save);
});


/**
 * Saves bookmark
 * @param e
 * @returns {boolean}
 */
function bookmark_save(event) {
    var $form = $(this);
    event.stopPropagation();
    event.preventDefault();
    $form.find(".text-error").remove();
    $.ajax({
        data: $form.serialize(),
        url: '/save/?ajax',
        type: 'post',
        beforeSend: function() {
            $('input[type=submit]').val('Saving...');
        },
        statusCode: {
            400: function(error) {
                $form.find('input[type=submit]').val('Save');
                var errors = $.parseJSON(error.responseText);
                for (var field in errors) {
                    var $field = $form.find("#id_" + field);
                    var $formGroup = $field.parent();
                    if (!$formGroup.hasClass('has-error')) {
                        $formGroup.addClass('has-error');
                        if (field === 'tags') {
                            console.log('tags..');
                            var $tags = $('.tagsinput');
                            $tags.addClass('has-error');
                            $tags.parent().append(['<span class="help-block">',
                                errors[field], '</span>'].join(''));
                        } else {
                            $field.after(['<span class="help-block">',
                                errors[field], '</span>'].join(''));
                        }
                    }
                };
                $form.find('input, textarea, select').one("keypress change", function() {
                    $(this).parent().removeClass('has-error');
                    $(this).siblings('.help-block').remove();
                    // Special for tags
                    $('.tagsinput').parent().removeClass('has-error');
                    $('.tagsinput').removeClass('has-error');
                    $('.tagsinput').siblings('.help-block').remove();
                });
            },
            200: function(bookmark) {
                $form.hide();
                $('#saveBookmark .modal-body').append('<h5 id="bookmark-saved">Saved successfully</h5>');
                $('#saveBookmark .modal-body').append(['<div class="modal-footer">',
                    '<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>',
                    '</div>'].join(''));
                var formattedTags = bookmark.tags.map(function(val) {
                    return ['<span class="label">', val, '</span>'].join('');
                });
                var bookmarkTemplate = ['<tr>',
                            '<td>', '<img src="',
                            bookmark.favicon, '" />',
                            '</td>', '<td>', '<a href="', bookmark.url, '">',
                            bookmark.title, "</a></td>",
                            '<td>', formattedTags.join('&nbsp;'), '</td>',
                            '<td>', '<a class="bookmark-edit" href="/save/?ajax&url=',
                            bookmark.url, '"><span class="glyphicon glyphicon-pencil"></span></a></td>',
                            '</tr>'
                ].join('');
                if (bookmark.created) {
                    if ($('.bookmark-empty')) {
                        $('.bookmark-empty').remove();
                    }
                    $('.table tbody').append(bookmarkTemplate);
                } else {
                    // TODO: replace item
                    var $url = $('a[href="' + bookmark.url + '"');
                    var $td = $url.parent();
                    $td.parent().html(bookmarkTemplate.slice(1, bookmarkTemplate.length - 2));
                }
            }
        }
    });
    return false;
}