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
        template: _.template('<a href="#<%= slug %>"><%= title %></a>'),
        el: 'li',
        render: function() {
            $(this.el).html(this.template({
                title: this.model.get('title'),
                slug: this.model.get('slug')
            }));
            return this;
        }
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

    // Start load
    $.getJSON(PC.recipeNamesURL, function(res) {
        var recipeCollection = new RecipeCollection(_.map(res.result, function(recipe) {
            return new Recipe({
                title: recipe.title,
                slug: recipe.slug
            });
        }));
        new RecipeListView({ collection: recipeCollection }).render();
    });

});
