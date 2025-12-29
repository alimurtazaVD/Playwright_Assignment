import pytest
from pytest_bdd import scenario

from .steps_automation_store import *


@scenario("../features/scenario_1_dove_brand.feature", "Add newest DOVE product to cart and verify")
@pytest.mark.smoke
@pytest.mark.cross_browser
def test_scenario_1_dove_brand_bdd():
    pass

