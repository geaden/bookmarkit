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
}

/**
 * Shows flash message with provided message and type
 * @param msg
 * @param type
 */
FlashMessage.prototype.show = function(msg, type, el) {
    this.message = msg;
    this.id = 'flashMessage';
    if (MESSAGE_TYPES.indexOf(type) >= 0) {
    this.type = type;
    } else {
    this.type = 'info';
    }
    var $addTo;
    if (el) {
      $addTo = $('#' + el);
    } else {
      $addTo = $('body');
    }
    if (!this.isShown) {
        $addTo.append('<div id="%s%" class="alert fade in"></div>'.replace(/%s%/, this.id));
        this.el = $('#' + this.id);
        this.el.addClass('alert-' + type);
        this.el.html(this.message);
        // Add close button
        var withClose = false;
        if (!withClose) {
            this.el.append('<a class="close" data-dismiss="alert" href="#" aria-hidden="true">&times;</a>');
        }
    }
    this.isShown = true;
    var _this = this;
    this.el.bind('closed.bs.alert', function () {
        _this.isShown = false;
    });
    setTimeout(function() {
        _this.el.alert('close');
    }, 3000);
};
