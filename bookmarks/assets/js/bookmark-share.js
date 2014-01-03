/**
 * Share bookmark methods.
 */
var isShared;


/**
 * Toggles share link
 */
function toggleShareLink() {
    $('tr').hover(function() {
        if (!$(this).find('a.bookmark-share').length) {
            var $appendTo = $(this).find('td.bookmark-share-col');
            $appendTo.append(['<a class="bookmark-share notshared" data-toggle="tooltip"',
                ' title="Share bookmark" href="/ajax/share/"><span class="glyphicon glyphicon-share-alt"></span></a>'].join(''));
            isShared = false;
        }
        $('a.bookmark-share').tooltip();
    }, function() {
        if (!isShared) {
            $(this).find('a.bookmark-share.notshared').remove();
        }
    });
}

/**
 * Shares bookmark
 */
function shareBookmark() {
    var flash = new FlashMessage();
    $('body').on('click', 'a.bookmark-share', function(e) {
        e.preventDefault();
        var _this = this;
        var bookmark = $(this).parent().data('value');
        console.log(bookmark);
        $.ajax({
            url: $(_this).attr('href'),
            method: 'POST',
            data: {bookmark: bookmark},
            statusCode: {
                200: function(shared_bookmark) {
                    var tooltipTitle;
                    if (shared_bookmark.shared) {
                        flash.show(['Bookmark <a href="',
                            shared_bookmark.url, '">', shared_bookmark.title,
                            '</a> has been successfully shared!'].join(''),
                        'success', 'flashMessageWrapper');
                        $(_this).attr('title', 'Share bookmark');
                        tooltipTitle = 'Share bookmark';
                    } else {
                        flash.show(['Bookmark <a href="',
                            shared_bookmark.url, '">', shared_bookmark.title,
                            '</a> is not shared anymore!'].join(''),
                        'info', 'flashMessageWrapper');
                        tooltipTitle = 'Stop sharing bookmark';
                    }
                    isShared = shared_bookmark.shared;
                    $(_this).attr('title', tooltipTitle);
                    $(_this).toggleClass('notshared');
                },
                400: function(error) {
                    flash.show('<strong>Error</stron> while sharing bookmark.', 'danger', 'flashMessageWrapper');
                }
            }
        });
    });
}

$(document).ready(function() {
    $('body').on('hover', 'a.bookmark-share', function() {
        console.log($(this));
        $(this).tooltip();
    });
    toggleShareLink();
    shareBookmark();
});
