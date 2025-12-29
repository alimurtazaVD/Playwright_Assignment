import pytest
from pytest_bdd import scenario

from .steps_automation_store import *


@scenario("../features/scenario_2_apparel_shoes.feature", "Add T-shirts and two highest priced shoes to cart")
@pytest.mark.smoke
@pytest.mark.cross_browser
def test_scenario_2_apparel_shoes_bdd():
    pass

