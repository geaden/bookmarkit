/**
 * Flash messages system
 */
var MESSAGE_TYPES = [
    'success',
    'info',
    'warning',
    'danger'
]

function FlashMessage() {
    'use strict';
    this.id = 'flashMessage';
    this.type = MESSAGE_TYPES[1];
    this.el = $('#' + this.id);
    this.isShown = false;
}

/**
 * Hides flash message
 */
FlashMessage.prototype.hide = function() {
    'use strict';
    var _this = this;
    var stopHiding = false;
    var timePassed;
    this.el.hover(function() {
        stopHiding = true;
    }, function() {
        stopHiding = false;
    });
    if (!stopHiding) {
        setTimeout(function() {
            _this.el.alert('close');
        }, 3000);
    }
    this.el.bind('closed.bs.alert', function () {
        _this.isShown = false;
    });
};

/**
 * Shows flash message with provided message and type
 * @param msg
 * @param type
 */
FlashMessage.prototype.show = function(msg, type, appender) {
    'use strict';
    this.message = msg;
    if (MESSAGE_TYPES.indexOf(type) >= 0) {
        this.type = type;
    }
    var $addTo;
    if (appender) {
      $addTo = $('#' + appender);
    } else {
      $addTo = $('#flashMessageWrapper');
    }
    var _this = this;
    if (!this.isShown) {
        $addTo.append('<div id="%s%" class="alert fade"></div>'.replace(/%s%/, this.id));
        this.el = $('#' + this.id);
        this.el.addClass('alert-' + type);
        this.el.html(this.message);
        // Add close button
        var withClose = true;
        if (withClose) {
            this.el.append('<a class="close" data-dismiss="alert" href="#" aria-hidden="true">&times;</a>');
        }
        // Animate out
        window.setTimeout(function() {
            _this.el.addClass('in');
        }, 300);
        var $width = $('.alert').width() / 2;
        $addTo.css('margin-left', -1 * $width + 'px');
        $('.alert').alert();
        this.isShown = true;
    }
    this.hide();
};
