def make_required_install_packages():
    return [
        "click==7.0",
        "protobuf>=3.12,<4",
        "pyyaml>=5.1",
        "six>=1.10,<2",
        "docker>=4,<5",
        "versioneer==0.18",
        "kubernetes==10.0.0",
        "pyarrow==0.16.0",
        "kfp>=0.2.4.1,<0.2.6",
        "urllib3<1.25,>=1.15",
        "google-auth<2.0dev,>=1.18.0",
        "bmlx-metadata==1.0.4",
        "bs4>=0.0.1",
        "tabulate==0.8.3",
        "pip-api==0.0.14",
        "pre-commit==2.4.0",
        "minio==5.0.10",
    ]


def make_required_test_packages():
    """Prepare extra packages needed for 'python setup.py test'."""
    return [
        "click==7.0",
        "protobuf>=3.12,<4",
        "pyyaml>=5.1",
        "six>=1.10,<2",
        "docker>=4,<5",
        "versioneer==0.18",
        "kubernetes==10.0.0",
        "pyarrow==0.16.0",
        "kfp>=0.2.4.1,<0.2.6",
        "urllib3<1.25,>=1.15",
        "minio==5.0.10",
    ]


def make_extra_packages_docker_image():
    return [
        "python-snappy>=0.5,<0.6",
    ]


def make_all_dependency_packages():
    return make_required_test_packages() + make_extra_packages_docker_image()
