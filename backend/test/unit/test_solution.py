import pytest
from unittest.mock import MagicMock
from src.controllers.recipecontroller import RecipeController

# add your test case implementation here
@pytest.fixture
def sut():
    pantry_items = [
        {"Yeast" : 0},
        {"Flour" : 100},
        {"Sugar" : 3}
    ]
    mocked_dao = MagicMock()
    mocked_dao.get_all.return_value = pantry_items
    rc = RecipeController(items_dao=mocked_dao)
    return rc

@pytest.mark.unit
def test_1(): # does not work as intendent
    mocked_dao = MagicMock()
    mocked_dao.get_all.side_effect = Exception()
    rc = RecipeController(items_dao=mocked_dao)

    with pytest.raises(Exception):
        rc.get_available_items()

@pytest.mark.unit
def test_2():
    pantry_items = [
        {"Yeast" : 0}
    ]
    mocked_dao = MagicMock()
    mocked_dao.get_all.return_value = pantry_items
    rc = RecipeController(items_dao=mocked_dao)
    result = rc.get_available_items(minimum_quantity=10)
    assert result == {}

@pytest.mark.unit
def test_3():
    pantry_items = [
        {"Yeast" : 10},
        {"Sugar" : 9}
    ]
    mocked_dao = MagicMock()
    mocked_dao.get_all.return_value = pantry_items
    rc = RecipeController(items_dao=mocked_dao)
    result = rc.get_available_items(minimum_quantity=10)
    assert result == {"Yeast" : 10}

@pytest.mark.unit
def test_4():
    pantry_items = [
        {"Yeast" : 100},
        {"Sugar" : 9}
    ]
    mocked_dao = MagicMock()
    mocked_dao.get_all.return_value = pantry_items
    rc = RecipeController(items_dao=mocked_dao)
    result = rc.get_available_items(minimum_quantity=99)
    assert result == {"Yeast" : 100}

@pytest.mark.unit
def test_5():
    pantry_items = [
        {"Yeast" : 0}
    ]
    mocked_dao = MagicMock()
    mocked_dao.get_all.return_value = pantry_items
    rc = RecipeController(items_dao=mocked_dao)
    result = rc.get_available_items(minimum_quantity=-1)
    assert result == {}

@pytest.mark.unit
def test_6():
    pantry_items = [
        {"Yeast" : 0}
    ]
    mocked_dao = MagicMock()
    mocked_dao.get_all.return_value = pantry_items
    rc = RecipeController(items_dao=mocked_dao)
    result = rc.get_available_items(minimum_quantity=0)
    assert result == {}
