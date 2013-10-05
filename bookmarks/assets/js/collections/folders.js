/** Describes Folders Backbone.JS collection */
define(
    [
        'underscore',
        'backbone',
        'models/folder'
    ],
    function (_, Backbone, Folder) {
        var FoldersCollection = Backbone.Collection.extend({
            // Reference to this collection's model.
            model: Folder,

            url: '/folders/',

            // Folders are sorted by their original id
            comparator: function(todo) {
                return todo.get('id');
            }
        });
    return new FoldersCollection();
});