import betamax
import itkdb


def test_get_image(auth_session):
    with betamax.Betamax(auth_session).use_cassette('test_images.test_get_image'):
        response = auth_session.get(
            'uu-app-binarystore/getBinaryData',
            json={
                'code': 'bc2eccc58366655352582970d3f81bf46f15a48cf0cb98d74e21463f1dc4dcb9'
            },
        )
        assert response
        assert response.status_code == 200
        assert response.headers.get('content-type').startswith('image')


def test_get_image_model(auth_client, tmpdir):
    with betamax.Betamax(auth_client).use_cassette('test_images.test_get_image'):
        image = auth_client.get(
            'uu-app-binarystore/getBinaryData',
            json={
                'code': 'bc2eccc58366655352582970d3f81bf46f15a48cf0cb98d74e21463f1dc4dcb9'
            },
        )
        assert isinstance(image, itkdb.models.Image)
        assert image.filename == 'PB6.CR2'
        assert image.format == 'cr2'
        temp = tmpdir.join("saved_image.cr2")
        nbytes = image.save(filename=temp.strpath)
        assert nbytes == 1166
