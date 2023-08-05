import os
import pystmark
import logging
from airflow.utils.email import get_email_address_list
from airflow.models import Variable

log = logging.getLogger(__name__)


def send_email(to, subject, html_content, files=None,
               dryrun=False, cc=None, bcc=None,
               mime_subtype='mixed', **kwargs):
    """
    Send an email with html content using `Postmark`
    To use this plugin:
    1. Update ``email_backend`` property in `[email]`` section in ``airflow.cfg``, i.e.,::
      [email]
      email_backend = airflow_postmark.postmark.send_email
    2. Configure Sendgrid specific environment variables at all Airflow instances:::
      POSTMARK_MAIL_FROM={your-mail-from}
      POSTMARK_API_KEY={your-postmark-api-key}
      or postmark_secret as Airflow Variables i.e. Variable.get('postmark_secret')
    """

    from_email = kwargs.get('from_email') or Variable.get('postmark_from_email') or os.environ.get('POSTMARK_MAIL_FROM')
    to_address = None
    cc_address = None
    bcc_address = None

    if to is not None:
        to_address = get_email_address_list(to)

    if cc is not None:
        cc_address = get_email_address_list(cc)

    if bcc is not None:
        bcc_address = get_email_address_list(bcc)

    message = pystmark.Message(sender=from_email,
                               to=to_address,
                               cc=cc_address,
                               bcc=bcc_address,
                               subject=subject,
                               html=html_content)

    for f in files:
        message.attach_file(f)

    api_key = Variable.get('postmark_secret') or os.environ.get('POSTMARK_API_KEY')

    if dryrun is False:
        res = pystmark.send(message, api_key=api_key)
        try:
            res.raise_for_status()
        except pystmark.UnauthorizedError:
            log.error('Use your real API key')




