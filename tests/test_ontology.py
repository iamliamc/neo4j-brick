import pytest

# TODO fix magic numbers
def test_get_brick_classes(sdk_graph_connection, load_test_data):
    classes = sdk_graph_connection.get_brick_classes()
    assert len(classes) == 829

def test_get_brick_relationships(sdk_graph_connection, load_test_data):
    relationships = sdk_graph_connection.get_brick_relationships()
    relationships == 23
