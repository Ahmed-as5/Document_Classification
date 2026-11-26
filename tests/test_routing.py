import pytest

from backend.main import DEFAULT_DEPARTMENT, DEPARTMENT_MAP, get_routing_department


@pytest.mark.parametrize(("label", "department"), DEPARTMENT_MAP.items())
def test_known_labels_route_to_their_department(label, department):
    assert get_routing_department(label.upper()) == department


def test_unknown_label_uses_default_department():
    assert get_routing_department("unknown") == DEFAULT_DEPARTMENT
