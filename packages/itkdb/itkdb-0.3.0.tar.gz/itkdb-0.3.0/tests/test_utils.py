import itkdb.utilities
import requests


def test_build_url_utils(mocker):
    request = mocker.MagicMock()
    request.url = 'https://itkpd-test.unicorncollege.cz/createTestRunAttachment'
    request.body = b'abytestring'
    assert (
        itkdb.caching.utils.build_url(request)
        == 'https://itkpd-test.unicorncollege.cz/createTestRunAttachment?&body=abytestring'
    )


def test_pretty_print():
    request = requests.Request(
        'POST',
        'https://stackoverflow.com',
        headers={'User-Agent': 'Test'},
        json={"hello": "world"},
    )
    text = itkdb.utilities.pretty_print(request)
    assert (
        text
        == 'POST / HTTP/1.1\r\nUser-Agent: Test\r\nContent-Length: 18\r\nContent-Type: application/json\r\n\r\n{"hello": "world"}'
    )
