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
