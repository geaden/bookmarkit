/**
 Describes folder Backbone.JS model
 */

define([
    'underscore',
    'backbone'
], function(_, Backbone) {
    var FolderModel = Backbone.Model.extend({
        // Default values for folder
        defaults: {
            'icon': 'default',
            'name': 'Unnamed'
        },

        // Each folder should have title and icon
        initialize: function() {
            if (!this.get('name') && !this.get('icon')) {
                this.set({'name': this.defaults.name});
                this.set({'icon': this.defaults.icon});
            }
        }
    });
    return FolderModel;
})