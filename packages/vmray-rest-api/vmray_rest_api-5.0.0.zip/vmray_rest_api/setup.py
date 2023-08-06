import glob, sys


class IncompatibleVersionOfSetupTools(Exception):
    pass

try:
    from setuptools import find_namespace_packages, setup
except ImportError as e:
    pip_cmd = "{} -m pip".format(sys.executable)
    raise IncompatibleVersionOfSetupTools(f"Incompatible version of setuptools.\n{pip_cmd} install setuptools --upgrade")


EXAMPLE_SCRIPTS = list(glob.glob("examples/*.py"))


setup(
    # metadata
    name="vmray_rest_api",
    version="5.0.0",
    url="https://www.vmray.com",
    author="VMRay",
    author_email="info@vmray.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    license="MIT",
    description="Python client library for the VMRay REST API",

    # options
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "six",
        "urllib3",
    ],
    packages=find_namespace_packages(include=["vmray.*"]),
    scripts=EXAMPLE_SCRIPTS,
    data_files=[
        ("", ["LICENSE", "README.md"]),
    ],
    zip_safe=False,
)
