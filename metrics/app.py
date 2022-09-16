import json, logging, hmac, hashlib

logger = logging.getLogger(__name__)
secret: str = "Riba123"


def lambda_handler(event, context):
    body = event['body']
    try:
        json.loads(body)
    except ValueError:
        logger.error("Failed to decode json")
        return {
            "body": json.dumps({"error": "json decode failure"}),
            "statusCode": 500
        }

    signature = event['headers'].get('x-hub-signature-256')
    if not validate_secret(signature, body):
        return {
            'statusCode': 403,
            'body': json.dumps({"error": "invalid signature"})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({"message": "Valid message"})
    }


def validate_secret(header_signature, msg):
    if header_signature is None:
        logger.error("Header signature missing")
        return False

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha256':
        logger.error("Header signature not signed with sha256")
        return False

    mac = hmac.new(key=bytes(secret, 'UTF-8'), msg=msg.encode(), digestmod=hashlib.sha256)

    # Get ours vs. theirs
    expected = str(mac.hexdigest())
    received = str(signature)

    # Timing attack secure comparison
    matches = hmac.compare_digest(expected, received)

    if not matches:
        logger.error("Header signature ({}) does not match expected ({})".format(received, expected))

    return matches
