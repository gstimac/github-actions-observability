import hashlib
import hmac
import logging

logger = logging.getLogger(__name__)


def validate_secret(header_signature: str, msg: str, secret: str) -> bool:
    if header_signature is None:
        logger.error("Header signature missing", stack_info=True)
        return False

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha256':
        logger.error("Header signature not signed with sha256", stack_info=True)
        return False

    mac = hmac.new(key=bytes(secret, 'UTF-8'), msg=msg.encode(), digestmod=hashlib.sha256)

    # Get ours vs. theirs
    expected = str(mac.hexdigest())
    received = str(signature)

    # Timing attack secure comparison
    matches = hmac.compare_digest(expected, received)

    if not matches:
        logger.error("Header signature ({}) does not match expected ({})".format(received, expected), stack_info=True)

    return matches
