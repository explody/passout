import os
import passout
import pytest


def verify_prod_service1(po):
    assert po.username == 'prod_user'
    assert po.password == "%0987654321"
    assert po.get('url') == 'https://prod.myservice.com'
    assert po.username == po.user()
    assert po.password == po.creds()


def verify_dev_service1(po):
    assert po.username == 'dev_user'
    assert po.password == "^1234567890"
    assert po.get('url') == 'https://dev.myservice.com'
    assert po.username == po.user()
    assert po.password == po.creds()


def verify_prod_service2(po):
    assert po.username == 'prod_user2'
    assert po.password == "abcdefghij!"
    assert po.get('url') == 'https://prod.myservice2.com'
    assert po.username == po.user()
    assert po.password == po.creds()


def verify_dev_service2(po):
    assert po.username == 'dev_user2'
    assert po.password == "klmnopqrst"
    assert po.get('url') == 'https://dev.myservice2.com'
    assert po.username == po.user()
    assert po.password == po.creds()


def reset_env():
    for k in ['PASSOUT_SVC', 'PASSOUT_ENV', 'PASSOUT_PATH']:
        os.environ.pop(k, None)


def test_simple_load():
    po = passout.PassOut('testservice', 'production', 'passout/test')
    verify_prod_service1(po)


def test_get_env():
    po = passout.PassOut('testservice', 'production', 'passout/test')
    assert po.env == 'production'


def test_switch_service_env():
    po = passout.PassOut('testservice', 'production', 'passout/test')
    verify_prod_service1(po)

    po.env = 'development'
    verify_dev_service1(po)


def test_switch_service():
    po = passout.PassOut('testservice', 'production', 'passout/test')
    verify_prod_service1(po)

    po.svc = 'testservice2'
    verify_prod_service2(po)


def test_switch_service_and_env():
    po = passout.PassOut('testservice', 'production', 'passout/test')
    verify_prod_service1(po)

    po.svc = 'testservice2'
    po.env = 'development'
    verify_dev_service2(po)


def test_switch_service_back_and_forth():
    po = passout.PassOut('testservice', 'production', 'passout/test')
    verify_prod_service1(po)

    po.svc = 'testservice2'
    verify_prod_service2(po)

    po.svc = 'testservice'
    po.env = 'development'
    verify_dev_service1(po)


def test_environment_vars():
    os.environ['PASSOUT_SVC'] = 'testservice'
    os.environ['PASSOUT_ENV'] = 'production'
    os.environ['PASSOUT_PATH'] = 'passout/test'
    po = passout.PassOut()
    verify_prod_service1(po)
    reset_env()


def test_environment_vars_default_service_env():
    os.environ['PASSOUT_SVC'] = 'testservice'
    os.environ['PASSOUT_PATH'] = 'passout/test'
    po = passout.PassOut()
    verify_dev_service1(po)
    reset_env()


def test_service_dump():
    po = passout.PassOut('testservice', 'production', 'passout/test')
    svc_dict = po.dumpsvc()

    assert type(svc_dict) == dict
    assert svc_dict['username'] == 'prod_user'
    assert svc_dict['password'] == "%0987654321"
    assert svc_dict['url'] == 'https://prod.myservice.com'


def test_bad_path():
    with pytest.raises(
        passout.PassOutNoServiceFile,
        match=r"PassOutNoServiceFile:.*doesnotexist.*"
    ):
        passout.PassOut('testservice', 'production', 'doesnotexist')


def test_no_service():
    with pytest.raises(
        passout.PassOutNoService,
        match=r"PassOutNoService: service not passed*"
    ):
        passout.PassOut()


def test_bad_service():
    with pytest.raises(
        passout.PassOutNoServiceFile,
        match=r"PassOutNoServiceFile:.*nonexistant_service.yml"
    ):
        passout.PassOut('nonexistant_service', 'production', 'passout/test')


def test_bad_env():
    with pytest.raises(
        passout.PassOutNoEnvironmentData,
        match=r"PassOutNoEnvironmentData:.*nonexistant_env"
    ):
        passout.PassOut('testservice', 'nonexistant_env', 'passout/test')


def test_bad_get():
    po = passout.PassOut('testservice', 'production', 'passout/test')
    assert not po.get('nonexistant_key')


def test_write_username_fails():
    po = passout.PassOut('testservice', 'production', 'passout/test')
    with pytest.raises(AttributeError):
        po.username = 'shouldfail'


def test_write_password_fails():
    po = passout.PassOut('testservice', 'production', 'passout/test')
    with pytest.raises(AttributeError):
        po.password = 'shouldfail'