from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views


class RecipeViewsTest(TestCase):
    #VERIFICANDO SE A VIEW QUE ESTA SENDO TESTADA É A MESMA QUE VIEW.HOME USANDO O 'IS'
    #O IS É RESPONSAVEL POR CHECAR ENDEREÇO DE MEMORIA.
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
        
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)
        
    def test_recipe_details_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)