/**
 Describes Folders Backbone.JS views
 */
define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/folders.html'
], function($, _, Backbone, foldersTemplate) {
        var FolderView = Backbone.View.extend({
        // Is a list tag
        tagName: "tr",

        className: "folder",

        // Cache the template function for a single item.
        template: _.template(foldersTemplate),

        // The TodoView listens for changes to its model, re-rendering. Since there's
        // a one-to-one correspondence between a **Folder** and a **FolderView** in this
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
            "click .folder": "openFolder",
            "mouseover .folder-name": "showEditPanel",
            "mouseout .folder-name": "hideEditPanel",
            "click a.edit-folder": "edit",
            "click a.remove-folder": "remove",
            "keypress .folder-input": "updateOnEnter",
            "blur .folder-input": "close"
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
            this.cacheInput();
            return this;
        },

        // Cache input value
        cacheInput: function() {
            this.$input = this.$('.folder-input > input');
        },

        // Switch this view into `"editing"` mode, displaying the input field.
        edit: function() {
            console.log('Editing...');
            this.$('.folder-name').addClass("editing");
            this.$('.folder-input').show();
            this.$input.focus();
        },

        // Close the `"editing"` mode, saving changes to the folder.
        close: function() {
            var value = this.$input.val();
            if (!value) {
                this.$input.val('Unnamed');
            }
            this.model.save({name: this.$input.val()});
            this.$('.folder-input').hide();
            this.$('.folder-name').removeClass("editing");
        },

        // If `enter` is pressed, we're through editing the item.
        updateOnEnter: function(e) {
            if (e.keyCode == 13) this.close();
            if (e.keyCode == 27) {
                console.log('escape...');
                this.$el.removeClass("editing");
                this.$('.folder-input').hide();
            }
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
    return FolderView;
})