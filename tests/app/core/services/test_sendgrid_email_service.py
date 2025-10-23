import pytest
from unittest.mock import Mock, AsyncMock, patch
from app.core.services.sendgrid_email_service import SendGridEmailService
from app.core.config import settings
import os

@pytest.fixture(autouse=True)
def mock_sendgrid_api_key():
    with patch.dict(os.environ, {"SENDGRID_API_KEY": "SG.test_api_key"}):
        yield

@pytest.mark.asyncio
@patch('sendgrid.SendGridAPIClient')
@patch('app.core.services.sendgrid_email_service.settings')
async def test_sendgrid_email_service_initialization(MockSettings, MockSendGridAPIClient):
    MockSettings.SENDGRID_API_KEY = "SG.test_api_key"
    MockSettings.MAIL_USERNAME = "test@example.com"
    # Test that the service initializes correctly
    service = SendGridEmailService()
    MockSendGridAPIClient.assert_called_once_with("SG.test_api_key")
    assert service.sg is not None
    assert service.sender_email == MockSettings.MAIL_USERNAME

@pytest.mark.asyncio
@patch('sendgrid.SendGridAPIClient')
async def test_send_verification_email(MockSendGridAPIClient):
    # Configure the mock client
    mock_sg_instance = MockSendGridAPIClient.return_value
    mock_sg_instance.client.mail.send.post = AsyncMock(return_value=Mock(status_code=202, body=b'', headers={}))

    service = SendGridEmailService()

    email_to = "test@example.com"
    name = "Test User"
    token = "test_token"

    await service.send_verification_email(email_to, name, token)

    mock_sg_instance.client.mail.send.post.assert_called_once()
    call_args = mock_sg_instance.client.mail.send.post.call_args[1]['request_body']

    assert email_to in call_args['personalizations'][0]['to'][0]['email']
    assert service.sender_email in call_args['from']['email']
    assert "Verify your email" == call_args['subject']
    assert name in call_args['content'][0]['value']
    assert f"http://localhost:8000/users/verificar-email?token={token}" in call_args['content'][0]['value']

@pytest.mark.asyncio
@patch('sendgrid.SendGridAPIClient')
async def test_enviar_email_bienvenida(MockSendGridAPIClient):
    # Configure the mock client
    mock_sg_instance = MockSendGridAPIClient.return_value
    mock_sg_instance.client.mail.send.post = AsyncMock(return_value=Mock(status_code=202, body=b'', headers={}))

    service = SendGridEmailService()

    email_to = "test@example.com"
    name = "Test User"

    await service.enviar_email_bienvenida(email_to, name)

    mock_sg_instance.client.mail.send.post.assert_called_once()
    call_args = mock_sg_instance.client.mail.send.post.call_args[1]['request_body']

    assert email_to in call_args['personalizations'][0]['to'][0]['email']
    assert service.sender_email in call_args['from']['email']
    assert "Welcome!" == call_args['subject']
    assert name in call_args['content'][0]['value']
    assert "Call To Action" not in call_args['content'][0]['value'] # Ensure button is removed

@pytest.mark.asyncio
@patch('sendgrid.SendGridAPIClient')
async def test_send_reset_password_email(MockSendGridAPIClient):
    # Configure the mock client
    mock_sg_instance = MockSendGridAPIClient.return_value
    mock_sg_instance.client.mail.send.post = AsyncMock(return_value=Mock(status_code=202, body=b'', headers={}))

    service = SendGridEmailService()

    email_to = "test@example.com"
    token = "reset_token"

    await service.send_reset_password_email(email_to, token)

    mock_sg_instance.client.mail.send.post.assert_called_once()
    call_args = mock_sg_instance.client.mail.send.post.call_args[1]['request_body']

    assert email_to in call_args['personalizations'][0]['to'][0]['email']
    assert service.sender_email in call_args['from']['email']
    assert "Reset your password" == call_args['subject']
    assert f"http://localhost:8000/users/confirmar-reseteo?token={token}" in call_args['content'][0]['value']
    assert "Reset Password" in call_args['content'][0]['value']

@pytest.mark.asyncio
@patch('sendgrid.SendGridAPIClient')
async def test_enviar_email_rechazo(MockSendGridAPIClient):
    # Configure the mock client
    mock_sg_instance = MockSendGridAPIClient.return_value
    mock_sg_instance.client.mail.send.post = AsyncMock(return_value=Mock(status_code=202, body=b'', headers={}))

    service = SendGridEmailService()

    email_to = "test@example.com"

    await service.enviar_email_rechazo(email_to)

    mock_sg_instance.client.mail.send.post.assert_called_once()
    call_args = mock_sg_instance.client.mail.send.post.call_args[1]['request_body']

    assert email_to in call_args['personalizations'][0]['to'][0]['email']
    assert service.sender_email in call_args['from']['email']
    assert "Your registration was rejected" == call_args['subject']
    assert "We regret to inform you that your registration has been rejected." in call_args['content'][0]['value']
    assert "Call To Action" not in call_args['content'][0]['value'] # Ensure button is removed
