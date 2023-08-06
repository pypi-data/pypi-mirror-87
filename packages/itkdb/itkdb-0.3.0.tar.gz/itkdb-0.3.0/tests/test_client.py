import itkdb
import betamax
import math


def test_client(auth_user):
    assert itkdb.Client(user=auth_user)


def test_client_pagination(auth_client):
    with betamax.Betamax(auth_client).use_cassette('test_institution.test_pagination'):
        response = auth_client.get(
            'listInstitutions', json={'pageInfo': {'pageSize': 5}}
        )
        assert isinstance(response, itkdb.responses.PagedResponse)
        institutes = list(response)
        assert institutes
        assert response.total == 120
        assert len(institutes) == 120
        assert response.limit == 120
        assert response.yielded == 120
        assert response.page_size == 5
        assert response.page_index == math.ceil(120.0 / 5.0) - 1  # 23


# NB: use the same pageSize to make sure we get the same pagination
def test_client_pagination_with_limit(auth_client):
    with betamax.Betamax(auth_client).use_cassette('test_institution.test_pagination'):
        response = auth_client.get(
            'listInstitutions', json={'pageInfo': {'pageSize': 5}}, limit=23
        )
        assert isinstance(response, itkdb.responses.PagedResponse)
        institutes = list(response)
        assert institutes
        assert response.total == 120
        assert len(institutes) == 23
        assert response.limit == 23
        assert response.yielded == 23
        assert response.page_size == 5
        assert response.page_index == math.ceil(23.0 / 5.0) - 1  # 4


# NB: pytest parameterize this
def test_get_component_info_serial(auth_client):
    with betamax.Betamax(auth_client).use_cassette(
        'test_components.test_get_component_info_serial'
    ):
        response = auth_client.get('getComponent', json={'component': '20USE000000086'})
        assert isinstance(response, dict)
