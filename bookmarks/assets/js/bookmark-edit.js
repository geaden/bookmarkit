/**
 * Opens modal window to edit bookmark
 *
 * @param e
 * @returns {boolean}
 */

var flashMessage = new FlashMessage();

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
    $('#id_url').val(obj.url);
    $('#id_title').val(obj.title);
    $('#id_tags').importTags(obj.tags);
    return false;
}

/**
 * Helper method to display tooltip
 */
function editTooltip() {
    $('a.bookmark-edit').tooltip();
    $('a.bookmark-edit').on('click', bookmark_edit);
}

$(document).ready(function () {
    editTooltip();
    $('a.bookmark-add').click(function(e) {
        e.preventDefault();
        $('#saveBookmark').modal('show');
    });
    $('#bookmark-save-form').on('submit', bookmark_save);
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
            $('input').each(function() {
                $(this).attr('disabled');
            })
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
                        // This is necessary for tagsinput as well
                        $formGroup.addClass('has-error');
                        if (field === 'tags') {
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
                // TODO i18n flash message
                $('#saveBookmark').modal('hide');
                flashMessage.show(['Bookmark <a href="',
                    bookmark.url, '">', bookmark.title, '</a> has been successfully saved.'].join(''), 'success', 'flashMessageWrapper');
                var formattedTags = bookmark.tags.map(function(val) {
                    return ['<a href="/tags/', val,
                        '">',
                        '<span class="label">', val, '</span></a>'].join('');
                });
                var sharedTemplate = '';
                if (bookmark.shared) {
                    sharedTemplate = ['<a class="bookmark-share" data-toggle="tooltip" title="Stop sharing bookmark" ',
                        'href="/ajax/share/">', '<span class="glyphicon glyphicon-share-alt"></span></a>'].join('');
                }
                var bookmarkTemplate = ['<tr>',
                            '<td>', '<img src="',
                            bookmark.favicon, '" />',
                            '</td>', '<td>', '<a href="', bookmark.url, '">',
                            bookmark.title, "</a></td>",
                            '<td>', formattedTags.join('&nbsp;'), '</td>',
                            '<td class="bookmark-share-col" data-value="',
                            bookmark.pk, '">', sharedTemplate, '</td>',
                            '<td>', '<a class="bookmark-edit" href="/save/?url=',
                            bookmark.url, '" data-toggle="tooltip" title="Edit bookmark">',
                            '<span class="glyphicon glyphicon-pencil"></span></a></td>',
                            '</tr>'
                ].join('');
                if (bookmark.created) {
                    if ($('.bookmark-empty')) {
                        $('.bookmark-empty').remove();
                        $('.table tbody').append(bookmarkTemplate);
                    } else {
                        $(bookmarkTemplate).insertBefore('.table tbody tr:first');
                    }
                } else {
                    // As alerts could be present bookmark urls could be more than one
                    var $urls = $('a[href="' + bookmark.url + '"');
                    var $url = $urls.length > 0 ? $urls[1] : $urls[0];
                    var $td = $($url).parent();
                    $td.parent().html(bookmarkTemplate.slice(1, bookmarkTemplate.length - 2));
                }
                editTooltip();
            }
        }
    });
    return false;
}