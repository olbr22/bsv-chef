import pytest
from unittest.mock import MagicMock, patch

from src.controllers.recipecontroller import RecipeController

class TestRecipeControllerGetRecipe:
    @pytest.fixture
    def sut(self):
        mockedDao = MagicMock()
        mockedDao.find.return_value = None
        sut = RecipeController(dao=mockedDao)
        sut.load_recipes = MagicMock()
        sut.load_recipes.return_value = [{'name': 'test', 'diet': 'normal', 'ingredients': ['test']}]
        return sut

    @pytest.mark.unit
    def test_get_recipe_1(self, sut):
        """
        Test case #1 
        """
        with patch('src.controllers.recipecontroller.get_readiness_of_recipes', autospec=True) as mockedreadiness, \
                patch('src.controllers.recipecontroller.random.randint', autospec=True) as mockedrecipeindex:
            mockedreadiness.return_value = None
            mockedrecipeindex.return_value = 0
        
        result = sut.get_recipe('normal', True)
        assert result == {'name': 'test', 'diet': 'normal', 'ingredients': ['test']}

    @pytest.mark.unit
    def test_get_recipe_2(self, sut):
        """
        Test case #2 
        """
        with patch('src.controllers.recipecontroller.get_readiness_of_recipes', autospec=True) as mockedreadiness, \
                patch('src.controllers.recipecontroller.random.randint', autospec=True) as mockedrecipeindex:
            mockedreadiness.return_value = None
            mockedrecipeindex.return_value = 0
        
        result = sut.get_recipe('normal', False)
        assert result == {'name': 'test', 'diet': 'normal', 'ingredients': ['test']}

    @pytest.mark.unit
    def test_get_recipe_3(self, sut):
        """
        Test case #3 
        """
        with patch('src.controllers.recipecontroller.get_readiness_of_recipes', autospec=True) as mockedreadiness, \
                patch('src.controllers.recipecontroller.random.randint', autospec=True) as mockedrecipeindex:
            mockedreadiness.return_value = None
            mockedrecipeindex.return_value = 0
        
        result = sut.get_recipe('normal')
        assert result == None

    @pytest.mark.unit
    def test_get_recipe_4(self, sut):
        """
        Test case #3 
        """
        with patch('src.controllers.recipecontroller.get_readiness_of_recipes', autospec=True) as mockedreadiness, \
                patch('src.controllers.recipecontroller.random.randint', autospec=True) as mockedrecipeindex:
            mockedreadiness.return_value = None
            mockedrecipeindex.return_value = 0
        
        result = sut.get_recipe('rubber',True)
        assert result == None