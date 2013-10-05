/** Bookmarks Backbone.JS view */
/**
 Describes Folders Backbone.JS views
 */
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/bookmarks',
    'text!templates/bookmarks.html',
    'text!templates/bookmark_form.html'
], function($, _, Backbone, BookmarksCollection, foldersTemplate, bookmarkForm) {
        var BookmarkView = Backbone.View.extend({
        // Is a list tag
        tagName: "tr",

        className: "bookmark",

        // Cache the template function for a single item.
        template: _.template(foldersTemplate),

        // Cache form template
        form: _.template(bookmarkForm),

        collection: BookmarksCollection,

        // The TodoView listens for changes to its model, re-rendering. Since there's
        // a one-to-one correspondence between a **Bookmark** and a **BookmarkView** in this
        // app, we set a direct reference on the model for convenience.
        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
            // in case the model is destroyed via a collection method
            // and not by a user interaction from the DOM, the view
            // should remove itself
            this.listenTo(this.model, 'destroy', this.remove);
        },

        // The DOM events specific to item
        events: {
            "mouseover .folder-name": "showEditPanel",
            "mouseout .folder-name": "hideEditPanel",
            "click a.edit-bookmark": "edit",
            "click a.remove-bookmark": "remove",
            "keypress .folder-input": "updateOnEnter",
            "blur .folder-input": "close"
        },

        showModalForm: function(bookmark) {
            // Console log show form
            $('body').append(this.form(bookmark.toJSON()));
            $('#bookmark-modal').modal('show');
        },

        // Shows edit panel on hovering folder
        showEditPanel: function(e) {
            this.$('span.edit-panel').show();
        },

        // Hides edit panel on hovering folder
        hideEditPanel: function() {
            this.$('span.edit-panel').hide();
        },


        // Re-render the contents of the folder item.
        // To avoid XSS (not that it would be harmful in this particular app),
        // use underscore's "<%-" syntax in template to set the contents of the folder item.
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },


        // Switch this view into `"editing"` mode, displaying the input field.
        edit: function() {
            // TODO:
            console.log('Editing...');
        },

        // Close the `"editing"` mode, saving changes to the bookmark.
        close: function() {
            // TODO:

        },

        // Remove this view from the DOM.
        // Remove event listeners from: DOM, this.model
        remove: function() {
            console.log("removing...");
            this.stopListening();
            this.undelegateEvents();
            this.$el.remove();
            this.clear();
        },

        // Remove the item, destroy the model.
        clear: function() {
            this.model.destroy();
        }
    });
    return BookmarkView;
})
