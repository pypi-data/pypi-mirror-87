import itkdb


def test_urljoin(auth_session):
    assert (
        auth_session._normalize_url('/resource/')
        == 'https://itkpd-test.unicorncollege.cz/resource/'
    )
    assert (
        auth_session._normalize_url('resource/')
        == 'https://itkpd-test.unicorncollege.cz/resource/'
    )
    assert (
        auth_session._normalize_url('/resource')
        == 'https://itkpd-test.unicorncollege.cz/resource'
    )
    assert (
        auth_session._normalize_url('resource')
        == 'https://itkpd-test.unicorncollege.cz/resource'
    )
    assert (
        auth_session._normalize_url('https://itkpd-test.unicorncollege.cz/resource')
        == 'https://itkpd-test.unicorncollege.cz/resource'
    )
    assert (
        auth_session._normalize_url('https://google.com/resource')
        == 'https://google.com/resource'
    )


def test_expires_after(auth_user):
    assert itkdb.core.Session(expires_after=dict(days=1))
