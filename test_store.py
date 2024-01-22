from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''


def create_order():
    create_endpoint = "/store/order"
    data = {
        "pet_id": 0
    }

    create_response = api_helpers.post_api_data(create_endpoint, data)
    order_id = create_response.json()["id"]

    return order_id


@pytest.mark.parametrize("order_id, code, message",
                         [("038b4a7c-e6eb-4069-9f75-46cf152c3e55", 404, "Order not found"),
                          (create_order(), 200, "Order and pet status updated successfully")])
def test_patch_order_by_id(order_id, code, message):
    update_endpoint = f"/store/order/{order_id}"
    new_data = {
        "status": "sold"
    }

    response = api_helpers.patch_api_data(update_endpoint, new_data)

    assert response.status_code == code
    assert response.json()["message"] == message
