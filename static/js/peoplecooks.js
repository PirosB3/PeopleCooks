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

    var _retrieve = function(caller_function, params) {
        
        return function(callback) {
            // If already fetched forget about it
            if (this.get('fetched') == true)
                return callback();
                
            // Fetch and cache
            var that = this;
            if (this.get('slug') != null) {
                $.getJSON(caller_function(this.get('slug')), function(res) {
                    var result = res.result;
                    params.forEach(function(el) {
                        that.set(el, result[el]);
                    });
                    that.set('fetched', true);
                    return callback();
                });
            }
        }
    }

    // Create Models
    var Recipe= Backbone.Model.extend();
    var Amount = Backbone.Model.extend();
    var Ingredient = Backbone.Model.extend();

    Recipe.prototype.retrieve = _retrieve(PC.getRecipeBySlugURL, ['description', 'steps', 'ingredients']);
    
    // Create Collections
    var RecipeCollection = Backbone.Collection.extend();
    var AmountCollection = Backbone.Collection.extend();
    var IngredientCollection = Backbone.Collection.extend();

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

    var RecipeDetailView = Backbone.View.extend({
        el: $('#contentView'),
        template: _.template($('#recipeDetailView').html()),
        template_step: _.template($('#recipeStepView').html()),
        template_ingredient: _.template($('#recipeIngredientView').html()),
        render: function() {
            var that = this;
            $(this.el).html(this.template(this.model.toJSON()));
            var counter = 0;
            _.each(this.model.get('steps'), function(step) {
                counter++;
                $('#pc_steps tbody', this.el).append(that.template_step({
                    step_num: counter,
                    description: step
                }));
            });
            _.each(this.model.get('ingredients'), function(ingredient) {
                $('#pc_ingredients tbody', this.el).append(that.template_ingredient({
                    amount: ingredient.amount,
                    slug: ingredient.slug,
                    name: App.ingredientCollection.where({slug : ingredient.slug})[0].get('name')
                }));
            });
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
                $.getJSON(PC.ingredientNamesURL, function(res) {
                    App.ingredientCollection = new IngredientCollection(_.map(res.result, function(ingredient) {
                        return new Ingredient({
                            name: ingredient.name,
                            slug: ingredient.slug
                        });
                    }));
                    new RecipeListView({ collection: App.recipeCollection }).render();
                    Backbone.history.start();
                });
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
