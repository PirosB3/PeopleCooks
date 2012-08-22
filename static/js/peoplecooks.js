// Initialization
$(function() {

    // Create Models
    var Recipe= Backbone.Model.extend({
        url: function() {
            return '/api/recipes/' + this.get('slug');
        }
    });

    var Ingredient = Backbone.Model.extend({
        url: function() {
            return '/api/ingredients/' + this.get('slug');
        }
    });

    // Add cache magic
    var _fetch = function(options) {
        if (this.get('_fetched'))
            return options.success();
        var that = this;
        Backbone.Model.prototype.fetch.call(this, {
            success: function() {
                that.set('_fetched', true);
                options.success();
            },
            error: options.error
        });
    }

    Recipe.prototype.fetch = _fetch;
    Ingredient.prototype.fetch = _fetch;

    // Create Collections
    var RecipeCollection = Backbone.Collection.extend({
        url: '/api/recipes',
        model : Recipe
    });

    var IngredientCollection = Backbone.Collection.extend({
        url: '/api/ingredients',
        model : Ingredient
    });

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
        initialize: function() {
            _.bindAll(this, 'render');
            this.model.on('change', this.render);
        },
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
        initialize: function() {
            _.bindAll(this, 'render');
            this.model.on('change', this.render);
        },
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
            App.recipeCollection = new RecipeCollection();
            App.ingredientCollection = new IngredientCollection();
            App.recipeCollection.fetch({
                success: function() {
                    new RecipeListView({ collection: App.recipeCollection }).render();
                    App.ingredientCollection.fetch({
                        success: function() {
                            new IngredientListView({ collection: App.ingredientCollection }).render();
                            Backbone.history.start();
                        }
                    });
                }
            });
        },

        routes: {
            "recipe/:slug": "getRecipe",
            "ingredient/:slug": "getIngredient",
            '*path':  'defaultRoute'
        },

        getRecipe: function( slug ) {
            var model = App.recipeCollection.where( {slug: slug} )[0];
            model.fetch({
                success: function() {
                    new RecipeDetailView( {model: model} ).render();
                }
            });
        },

        getIngredient: function( slug ) {
            var model = App.ingredientCollection.where( {slug: slug} )[0];
            model.fetch({
                success: function() {
                    new IngredientDetailView( {model: model} ).render();
                }
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
