import boto3

UPLOADER_AWS_ACCESS_KEY = "AKIAIWVOACB2K2TRS44Q"
UPLOADER_AWS_SECRET_KEY = "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"

session = boto3.Session(
    aws_access_key_id="AKIAIWVOACB2K2TRS44Q",
    aws_secret_access_key="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",
)

resource = boto3.resource(
    's3',
    aws_access_key_id="AKIAIWVOACB2K2TRS44Q",
    aws_secret_access_key="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",
    region_name="us-west-2"
)

client = boto3.client(
    's3',
    aws_access_key_id="AKIAIWVOACB2K2TRS44Q",
    aws_secret_access_key="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",
    region_name="us-west-2"
)
