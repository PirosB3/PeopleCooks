var PC = (function(module){
  module.recipeNamesURL = '/api/getRecipeNames';
  module.ingredientNamesURL = '/api/getIngredientNames';
  module.getRecipeByTitleURL = function(title) {
    return '/api/getRecipeByTitle?title=' + escape(title.toLowerCase());
  }
  module.getIngredientByNameURL = function(name) {
    return '/api/getIngredientByTitle?name=' + escape(name.toLowerCase());
  }
  module.getRecipeNamesByIngredientURL = function(name) {
    return '/api/getRecipeNamesByIngredient?name=' + escape(name.toLowerCase());
  }
  return module;
})(PC || {})

// Initialization
$(function() {
    // Create Model
    var Recipe= Backbone.Model.extend();
    
    // Create Collections
    var RecipeCollection = Backbone.Collection.extend();

    // Create Views
    var RecipeView = Backbone.View.extend({
        template: _.template($('#recipeView').html()),
        tagName: 'li',
        className: 'recipeElement',
        render: function() {
            $(this.el).html(this.template({
                title: this.model.get('title'),
                slug: this.model.get('slug')
            }));
            return this;
        },

    });

    var RecipeListView = Backbone.View.extend({
        el: $('#recipeList'),
        render: function() {
            var that = this;
            this.collection.forEach(function(recipe) {
                var recipeView = new RecipeView({ model: recipe });
                that.el.appendChild(recipeView.render().el);
            });
        }
    });

    var RecipeDetailView = Backbone.View.extend({
        el: $('#contentView'),
        template: _.template($('#recipeDetailView').html()),
        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
        }
    });

    // Backbone history
    var AppRouter = Backbone.Router.extend({

        initialize: function() {
            // Start load
            $.getJSON(PC.recipeNamesURL, function(res) {
                App.recipeCollection = new RecipeCollection(_.map(res.result, function(recipe) {
                    return new Recipe({
                        title: recipe.title,
                        slug: recipe.slug
                    });
                }));
                new RecipeListView({ collection: App.recipeCollection }).render();
                Backbone.history.start();
            });
        },

        routes: {
            "recipe/:slug": "getRecipe",
        },

        getRecipe: function( slug ) {
            var model = App.recipeCollection.where( {slug: slug} )[0];
        }

    });

    // Initialize
    App = {}
    new AppRouter();

});
