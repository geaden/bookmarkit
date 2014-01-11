/**
 * Vote bookmark methods
 */
function voteUp(e) {
    e.preventDefault();
    var flash = new FlashMessage();
    var $sharedBookmark = $(this).parent().data('value');
    var _this = this;
    $.ajax({
        url: $(_this).attr('href'),
        data: {bookmark: $sharedBookmark},
        method: 'POST',
        statusCode: {
            200: function(success) {
                var msg = ['You voted for <a href="',
                    success.bookmark.url, '">', success.bookmark.title,
                    '</a>!'].join('');
                flash.show(msg, 'success');
                var $votes = $($(_this).parent().siblings().splice(-1)[0]).find('span.badge');
                var $votesCount = $votes.text();
                $votes.text(Number($votesCount) + 1);
            },
            400: function(error) {
                var msg = 'You can\'t vote for this bookmark!';
                flash.show(msg, 'danger');
            },
            403: function(error) {
                var msg = 'You have to be logged in to vote.';
                flash.show(msg, 'warning');
            }
        }
    });
}

function showTooltip() {
    'use strict';
    $('a.vote-up').tooltip();
}

$(document).ready(function() {
    'use strict';
    $('body').on('click', 'a.vote-up', voteUp);
    $('table#popular-bookmarks tr').hover(function() {
        $(this).find('td.bookmark-vote-col').html([
            '<a href="/ajax/vote/" class="vote-up" data-toggle="tooltip" title="Vote"><span class="glyphicon glyphicon-thumbs-up">',
            '</span></a>'
        ].join(''));
        showTooltip();
    }, function() {
        $(this).find('td.bookmark-vote-col').html('');
    });
});
