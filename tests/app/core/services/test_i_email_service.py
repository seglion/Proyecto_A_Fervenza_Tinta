import pytest
from abc import ABC
from app.core.services.i_email_service import IEmailService

def test_email_service_interface_file_exists():
    """
    Tests if the email service interface file exists.
    """
    try:
        from app.core.services import i_email_service
    except ImportError:
        pytest.fail("Email service interface file does not exist: src/app/core/services/i_email_service.py")

def test_email_service_interface_class_exists():
    """
    Tests if the IEmailService class exists in the interface file and is an ABC.
    """
    try:
        from app.core.services.i_email_service import IEmailService
        assert issubclass(IEmailService, ABC)
    except ImportError:
        pytest.fail("IEmailService class does not exist in i_email_service.py")

def test_iemailservice_has_send_verification_email_method():
    """
    Tests if the IEmailService interface has a 'send_verification_email' abstract method.
    """
    assert hasattr(IEmailService, 'send_verification_email')
    assert 'email' in IEmailService.send_verification_email.__annotations__
    assert IEmailService.send_verification_email.__annotations__['email'] == str
    assert 'token' in IEmailService.send_verification_email.__annotations__
    assert IEmailService.send_verification_email.__annotations__['token'] == str
    assert IEmailService.send_verification_email.__annotations__['return'] == None
