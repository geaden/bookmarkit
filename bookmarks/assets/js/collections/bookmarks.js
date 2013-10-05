/** Describes collection of bookmarks */
/** Describes Folders Backbone.JS collection */
define(
    [
        'underscore',
        'backbone',
        'models/bookmark'
    ],
    function (_, Backbone, Bookmark) {
        var BookmarksCollection = Backbone.Collection.extend({
            // Reference to this collection's model.
            model: Bookmark,

            url: '/bookmarks/',

            // Folders are sorted by their original id
            comparator: function(todo) {
                return todo.get('id');
            }
        });
    return new BookmarksCollection();
});