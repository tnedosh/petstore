from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''


def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)


'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''


@pytest.mark.parametrize("status, code, response_status",
                         [("available", 200, "available"), ("pending", 200, "pending"), ("sold", 200, ""),
                          ("", 400, "Invalid pet status {status}")])
def test_find_by_status_200(status, code, response_status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)

    assert response.status_code == code

    response_list = response.json()

    if response.status_code == 400:
        assert response_list["message"] == response_status
    else:
        for el in response_list:
            assert el["status"] == response_status


'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''


@pytest.mark.parametrize("pet_id, code", [(0, 200), (-1, 404), ("abc", 404), ("100", 404), (True, 404)])
def test_get_by_id_404(pet_id, code):
    test_endpoint = f"/pets/{pet_id}"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == code