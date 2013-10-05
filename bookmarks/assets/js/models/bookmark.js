define(['underscore', 'backbone'], function(_, Backbone) {
    var BookmarkModel = Backbone.Model.extend({
        // Default values for bookmark
        defaults: {
            'icon': 'default',
            'title': '',
            'link': '',
            'tags': ''
        },

        validate: function(attrs) {
            if (!attrs.link) {
                return 'Please fill link field.';
            }
            if (!attrs.title) {
                return 'Please fill title field.';
            }
        }
    });
    return BookmarkModel;
})