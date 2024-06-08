from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    # responsavel por ser executado DEPOIS de cada test.

    # O IS É RESPONSAVEL POR CHECAR ENDEREÇO DE MEMORIA.
    def test_recipe_home_view_function_is_correct(self):
        # VERIFICANDO SE A VIEW QUE ESTA SENDO TESTADA É A MESMA QUE VIEW.HOME
        # USANDO O 'IS'
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_load_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_show_no_recipe_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        # COLOCANDO AS REPONSE EM 'STRING' COM O DECODE UTF-8 PORQUE
        # ELA VEM BITES. b'
        self.assertIn(
            '<h1>No recipes found here </h1>',
            response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        # Reverse pegando direto da view
        response = self.client.get(reverse('recipes:home'))
        # decodoficando a response que vem em bytes
        content = response.content.decode('utf-8')
        # response do contexto
        response_context_recipes = response.context['recipes']
        # Check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                       kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        # response_context_recipes = response.context['recipes']
        self.assertIn(needed_title, content)
        # self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_details_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_return_404_if_no_recipes(self):
        # BUSCANDO UM INDICE QUE EU TENHO CERTEZA QUE NAO EXISTE PARA ELE
        # RETORNAR '404'
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)
    
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
        