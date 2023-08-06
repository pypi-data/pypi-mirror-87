import betamax
import logging


def test_get_component(auth_client, caplog):
    with betamax.Betamax(auth_client).use_cassette('test_warnings.test_get_component'):
        with caplog.at_level(logging.WARNING, "itkdb.core"):
            auth_client.get(
                'getComponent', json={'component': '20USE000000086', 'ignoreme': 'fake'}
            )
            assert "cern-itkpd-main/getComponent/unsupportedKeys" in caplog.text
            assert "ignoreme" in caplog.text
            caplog.clear()
