var PC = (function(module){
    module.recipeNamesURL = '/api/getRecipeNames';
    module.ingredientNamesURL = '/api/getIngredientNames';
    module.getRecipeBySlugURL = function(slug) {
        return '/api/getRecipeBySlug?slug=' + slug;
    }
    module.getIngredientBySlugURL = function(slug) {
        return '/api/getIngredientBySlug?slug=' + slug;
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
    var Ingredient = Backbone.Model.extend();

    // Create Collections
    var RecipeCollection = Backbone.Collection.extend();
    var IngredientCollection = Backbone.Collection.extend();

    // Customizations
    Recipe.prototype.retrieve = _retrieve(PC.getRecipeBySlugURL, ['description', 'steps', 'ingredients']);
    Ingredient.prototype.retrieve = _retrieve(PC.getIngredientBySlugURL, ['recipes']);

    // Create Views
    var NavItemView = Backbone.View.extend({
        template: _.template($('#navItemView').html()),
        tagName: 'li',
        render: function() {
            $(this.el).html(this.template({
                title: this.options.title,
                slug: this.options.slug,
                type: this.options.type
            }));
            return this;
        }
    });

    var RecipeListView = Backbone.View.extend({
        el: $('#recipeList'),
        render: function() {
            var that = this;
            this.collection.forEach(function(recipe) {
                var recipeView = new NavItemView({
                    title: recipe.get('title'),
                    slug: recipe.get('slug'),
                    type: 'recipe',
                    className: 'recipeElement'
                });
                that.el.appendChild(recipeView.render().el);
            });
        }
    });

    var IngredientListView = Backbone.View.extend({
        el: $('#ingredientList'),
        render: function() {
            var that = this;
            this.collection.forEach(function(ingredient) {
                var ingredientView = new NavItemView({
                    title: ingredient.get('name'),
                    slug: ingredient.get('slug'),
                    type: 'ingredient',
                    className: 'ingredientElement'
                });
                that.el.appendChild(ingredientView.render().el);
            });
        }
    });

    var IngredientDetailView = Backbone.View.extend({
        el: $('#contentView'),
        template: _.template($('#ingredientDetailView').html()),
        template_recipe: _.template($('#ingredientRecipeView').html()),
        render: function() {
            var that = this;
            $(this.el).html(this.template(this.model.toJSON()));
            _.each(this.model.get('recipes'), function(recipe) {
                $('#pc_recipes tbody', that.el).append( that.template_recipe({
                    title: App.recipeCollection.where({slug: recipe})[0].get('title'),
                    slug: recipe
                }));
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
                new RecipeListView({ collection: App.recipeCollection }).render();
                $.getJSON(PC.ingredientNamesURL, function(res) {
                    App.ingredientCollection = new IngredientCollection(_.map(res.result, function(ingredient) {
                        return new Ingredient({
                            name: ingredient.name,
                            slug: ingredient.slug
                        });
                    }));
                    new IngredientListView({ collection: App.ingredientCollection }).render();
                    Backbone.history.start();
                });
            });
        },

        routes: {
            "recipe/:slug": "getRecipe",
            "ingredient/:slug": "getIngredient",
            '*path':  'defaultRoute'
        },

        getRecipe: function( slug ) {
            var model = App.recipeCollection.where( {slug: slug} )[0];
            model.retrieve(function() {
                new RecipeDetailView( {model: model} ).render();
            });
        },

        getIngredient: function( slug ) {
            var model = App.ingredientCollection.where( {slug: slug} )[0];
            model.retrieve(function() {
                new IngredientDetailView( {model: model} ).render();
            });
        },

        defaultRoute: function(path) {
            var mainView = _.template($('#mainView').html());
            $('#contentView').html(
                mainView({ recipe_count: App.recipeCollection.length })
            );
        }

    });

    // Initialize
    App = {}
    new AppRouter();

});
