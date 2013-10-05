/** Main Bookmarkit configuration */
require.config({
    baseUrl: "/static/js",
    paths: {
        jquery: "lib/jquery/jquery-1.10.2.min",
        underscore: "lib/underscore/underscore-min",
        backbone: "lib/backbone/backbone-min",
        text: "lib/require/text",
        bootstrap: "lib/bootstrap/bootstrap.min",
        csrf: "utils/csrf"
    },

    shim: {
        underscore: {
            exports: '_'
        },

        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        }
    }
});

require(['views/app', 'collections/folders'], function(AppView, FoldersCollection) {
    var appView = new AppView({
        collection: FoldersCollection
    });
})