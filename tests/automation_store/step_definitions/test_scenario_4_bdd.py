import pytest
from pytest_bdd import scenario

from .steps_automation_store import *


@scenario("../features/scenario_4_men_product_starts_with_m.feature", "Add products starting with 'M' from Men section to cart")
@pytest.mark.smoke
@pytest.mark.cross_browser
def test_scenario_4_men_product_starts_with_m_bdd():
    pass

