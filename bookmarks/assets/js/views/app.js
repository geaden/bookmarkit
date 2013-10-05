/**
 Main Bookmark.It View
 */

define([
    'jquery',
    'underscore',
    'backbone',
    'views/folder',
    'collections/bookmarks',
    'views/bookmark',
    'csrf',
    'bootstrap'
], function ($, _, Backbone, FolderView, BookmarksCollection, BookmarkView) {
        var loaded = false;
        var created = false;
        var AppView = Backbone.View.extend({

        // Instead of generating a new element, bind to the existing skeleton of
        // the App already present in the HTML.
        el: $("#bookmarkit"),

        // Delegated events for creating new folders
        events: {
            "click #new-folder": "createFolder",
            "click #new-bookmark": "createBookmark"
        },

        bookmarks: BookmarksCollection,

        // At initialization we listen to the relevant events on the `Todos`
        // collection, when items are added or changed. This collection is
        // passed on the constructor of this AppView. Kick things off by
        // loading any preexisting folders that might be saved in *localStorage*.
        initialize: function() {
            this.input = this.$(".folder-input");
            console.log('initializing...');
            console.log(this.bookmarks);
            this.listenTo(this.collection, 'add', this.addFolder);
            this.listenTo(this.bookmarks, 'add', this.renderBookmark);
            this.listenTo(this.collection, 'reset', this.addAllFolders);
            this.listenTo(this.collection, 'all', this.render);
            this.collection.fetch({success: function() {
                loaded = true;
            }});
            this.bookmarks.fetch();
        },

        // Re-rendering the App just means refreshing the statistics -- the rest
        // of the app doesn't change.
        render: function() {
            console.log("LOADED: " + loaded + ", FOLDERS: " + this.collection.length);
            if (loaded) {
                if (this.collection.length === 0) {
                    this.$('#folder-list').html(
                        ['<tr id="folders-null">',
                         '<td colspan="5">',
                         'No items</td></tr>'].join(''));
                } else {
                    this.$('#folders-null').remove();
                }
            }
            console.log("CREATED: " + created);
            if (created) {
                console.log('focusing element...');
                created = false;
            }
        },

        // Add a new folder
        // appending its element to the table.
        addFolder: function(folder) {
            var view = new FolderView({model: folder});
            console.log(view);
            var renderedView = view.render().el;
            this.$('#folder-list').append(renderedView);
            if (created) {
                this.$('.folder-name:last').addClass('editing');
                this.$('.folder-input:last').show();
                this.$('.folder-input:last > input').focus();
                created = false;
            }
        },

        // Add all items in the **Folders** collection at once.
        addAllFolders: function() {
            this.collection.each(this.addFolder);
        },

        // Generate the attributes for a new Folder.
        newAttributes: function() {
            return {
                name: 'Unnamed',
                icon: 'default'
            };
        },

        // Create folder
        createFolder: function() {
            this.collection.create(this.newAttributes());
            created = true;
        },

        // Create bookmark
        createBookmark: function(e) {
            // TODO: createBookmark
            console.log("Create bookmark");
            var newBookmark = new this.bookmarks.model(
                {title: '', link: '', tags: ''});
            var view = new BookmarkView({model: newBookmark});
            view.render().showModalForm(newBookmark);
            $('#bookmark-save').click(this.saveBookmark);
        },

        // Save bookmark
        saveBookmark: function() {
            console.log('Saving bookmark...');
            var formData = {};
            $.each($('#bookmark-form').serializeArray(), function(i, v) {
                if (v.value != '') {
                    formData[v.name] = v.value;
                }
            });
            bookmarks = BookmarksCollection;
            bookmarks.add(new bookmarks.model(formData));
            $('#bookmark-modal').modal('hide');
        },

        // Render bookmark
        renderBookmark: function(bookmark) {
            var bookView = new BookmarkView({
                model: bookmark
            });
            this.$('#folder-list').append(bookView.render().el);
        }
  });
  return AppView;
});