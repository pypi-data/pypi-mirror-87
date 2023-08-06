import betamax


def test_get(auth_session):
    with betamax.Betamax(auth_session).use_cassette('test_components.test_get'):
        response = auth_session.get('listComponentTypes', json={'project': 'S'})
        assert response.status_code == 200
        response = response.json()
        assert response
        assert 'pageItemList' in response
        assert 'pageInfo' in response
        assert 'uuAppErrorMap' in response


def test_list_componentsv1(auth_session):
    with betamax.Betamax(auth_session).use_cassette(
        'test_components.test_list_componentsv1'
    ):
        response = auth_session.get('listComponents', json={'project': 'S'})
        assert response.status_code == 200
        response = response.json()
        assert response
        assert 'pageItemList' in response
        assert 'pageInfo' in response
        assert 'uuAppErrorMap' in response


def test_list_components_componentTypev1(auth_session):
    with betamax.Betamax(auth_session).use_cassette(
        'test_components.test_list_components_componentTypev1'
    ):
        response = auth_session.get(
            'listComponents', json={'project': 'S', 'componentType': 'HYBRID'}
        )
        assert response.status_code == 200
        response = response.json()
        assert response
        assert 'pageItemList' in response
        assert 'pageInfo' in response
        assert 'uuAppErrorMap' in response


def test_list_componentsv2(auth_session):
    with betamax.Betamax(auth_session).use_cassette(
        'test_components.test_list_componentsv2'
    ):
        response = auth_session.get(
            'listComponents', json={'filterMap': {'project': 'S'}}
        )
        assert response.status_code == 200
        response = response.json()
        assert response
        assert 'itemList' in response
        assert 'pageInfo' in response
        assert 'uuAppErrorMap' in response


def test_list_components_componentTypev2(auth_session):
    with betamax.Betamax(auth_session).use_cassette(
        'test_components.test_list_components_componentTypev2'
    ):
        response = auth_session.get(
            'listComponents',
            json={'filterMap': {'project': 'S', 'componentType': 'HYBRID'}},
        )
        assert response.status_code == 200
        response = response.json()
        assert response
        assert 'itemList' in response
        assert 'pageInfo' in response
        assert 'uuAppErrorMap' in response


# NB: pytest parameterize this
def test_get_component_info_serial(auth_session):
    with betamax.Betamax(auth_session).use_cassette(
        'test_components.test_get_component_info_serial'
    ):
        response = auth_session.get(
            'getComponent', json={'component': '20USE000000086'}
        )
        assert response.status_code == 200
        response = response.json()
        assert response
        assert 'uuAppErrorMap' in response


def test_get_component_info_code(auth_session):
    with betamax.Betamax(auth_session).use_cassette(
        'test_components.test_get_component_info_code'
    ):
        response = auth_session.get(
            'getComponent', json={'component': '54f134b9975bebc851c4671d0ccbb489'}
        )
        assert response.status_code == 200
        response = response.json()
        assert response
        assert 'uuAppErrorMap' in response


def test_get_component_bulk(auth_session):
    with betamax.Betamax(auth_session).use_cassette(
        'test_components.test_get_component_bulk'
    ):
        response = auth_session.get(
            'getComponentBulk', json={'component': ['54f134b9975bebc851c4671d0ccbb489']}
        )
        assert response.status_code == 200
        response = response.json()
        assert response
        assert 'uuAppErrorMap' in response
        assert 'pageInfo' not in response
        assert 'itemList' in response


def test_get_component_bulk_client(auth_client):
    with betamax.Betamax(auth_client).use_cassette(
        'test_components.test_get_component_bulk'
    ):
        response = auth_client.get(
            'getComponentBulk', json={'component': ['54f134b9975bebc851c4671d0ccbb489']}
        )
        assert response
        assert isinstance(response, list)


def test_add_comment(tmpdir, auth_session):
    with betamax.Betamax(auth_session).use_cassette('test_components.test_add_comment'):
        component = '20USE000000086'
        message = "this is a test message"
        data = {'component': component, 'comments': [message]}
        response = auth_session.post('createComponentComment', json=data)
        assert response.status_code == 200
        response = response.json()
        assert response
        assert 'component' in response
        assert 'uuAppErrorMap' in response
        assert 'serialNumber' in response['component']
        assert response['component']['serialNumber'] == '20USE000000086'
        assert 'comments' in response['component']
        assert len(response['component']['comments']) > 0

        foundComment = False
        for comment in response['component']['comments']:
            if comment['comment'] == message:
                foundComment = True
                break

        assert foundComment
