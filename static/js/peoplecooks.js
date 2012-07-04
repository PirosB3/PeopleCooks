var PC = (function(module){
  module.recipeNamesURL = '/api/getRecipeNames';
  module.ingredientNamesURL = '/api/getIngredientNames';
  module.getRecipeBySlugURL = function(slug) {
    return '/api/getRecipeBySlug?slug=' + slug;
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
    Recipe.prototype.retrieve = function(callback) {
        // If already fetched forget about it
        if (this.get('fetched') == true)
            return callback();
            
        // Fetch and cache
        var that = this;
        if (this.get('slug') != null) {
            $.getJSON(PC.getRecipeBySlugURL(this.get('slug')), function(res) {
                var result = res.result;
                that.set('description', result.description);
                that.set('fetched', true);
                return callback();
            });
        }
    }
    
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
            model.retrieve(function() {
                new RecipeDetailView( {model: model} ).render();
            });
        }

    });

    // Initialize
    App = {}
    new AppRouter();

});
