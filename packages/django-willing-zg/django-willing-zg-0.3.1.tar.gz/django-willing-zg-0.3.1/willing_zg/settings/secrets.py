import os
import json
import boto3


def get_secret(secret_arn):
    """Create a Secrets Manager client"""
    client = boto3.client("secretsmanager")
    get_secret_value_response = client.get_secret_value(SecretId=secret_arn)
    return get_secret_value_response


if "DATABASE_SECRET" in os.environ:
    db_secret = json.loads(get_secret(os.environ["DATABASE_SECRET"])["SecretString"])

    db_username = db_secret["username"]
    db_password = db_secret["password"]
    db_host = db_secret["host"]
    db_port = str(db_secret["port"])
    db_clusterid = db_secret["dbClusterIdentifier"]

    db_url = f"postgres://{db_username}:{db_password}@{db_host}:{db_port}/{db_clusterid}"
    os.environ["DATABASE_URL"] = db_url

if "DJANGO_EMAIL_HOST_PASSWORD" in os.environ:
    django_password = json.loads(
        get_secret(os.environ["DJANGO_EMAIL_HOST_PASSWORD"])["SecretString"]
    )
    EMAIL_HOST_PASSWORD = django_password["DJANGO_EMAIL_HOST_PASSWORD"]
