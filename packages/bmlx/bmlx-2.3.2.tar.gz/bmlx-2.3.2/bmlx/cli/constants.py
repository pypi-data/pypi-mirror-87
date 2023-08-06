BMLX_CONFIG_FILE = "bmlx.yml"

BMLX_PIPELINE_ENTRY = "pipeline.py"

ARTIFACT_STORAGE_BASE_PATH = "s3://bmlx-pipeline/artifacts"

S3_CEPH_STORAGE_MAP = {
    "bmlx-pipeline": {
        "endpoint": "http://fs-ceph-hk.bigo.sg",
        "access_key": "2TWCN3YQPJ8SOVCWIPAB",
        "secret_key": "JwEqpvgeYuFF9OvGR4OOW9A2evKOGFAkdKjr5R7Z",
    },
    "mlpipeline": {
        "endpoint": "http://file-aihk.bigo.sg",
        "access_key": "B7XONTSFOJT6BSU2E54K",
        "secret_key": "9Rr1g3GChpoYtnrq8oC0ULVurKd7152RafdZtFkj",
    },
    "mlpipeline-test": {
        "endpoint": "http://fs-ceph-hk.bigo.sg",
        "access_key": "12M1WDPCLDDB2O8J4HW4",
        "secret_key": "GlW73eIZNWVwFvAVDxcZmUjL4xkATdr9ToSq8dKZ",
    },
}