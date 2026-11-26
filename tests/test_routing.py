import pytest

# Adjust the function name to match the real code
from backend.services.routing_service import get_routing_department

CATEGORIES = ["Application", "Complaint", "Invoice", "Contract", "Request", "Correspondence"]


@pytest.mark.parametrize("category", CATEGORIES)
def test_every_category_has_department(category):
    department = get_routing_department(category)
    assert isinstance(department, str) and department.strip()
