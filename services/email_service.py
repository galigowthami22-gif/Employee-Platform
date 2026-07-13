try:
    from fastapi_mail import FastMail, MessageSchema
except ImportError:  # pragma: no cover - optional dependency
    FastMail = None
    MessageSchema = None

from core.mail import conf


async def send_email(email: str, subject: str, body: str):
    if FastMail is None or MessageSchema is None:
        raise RuntimeError("Email service dependency is not available. Install fastapi-mail to enable email sending.")

    message = MessageSchema(subject=subject, recipients=[email], body=body, subtype="html")
    fm = FastMail(conf)
    await fm.send_message(message)