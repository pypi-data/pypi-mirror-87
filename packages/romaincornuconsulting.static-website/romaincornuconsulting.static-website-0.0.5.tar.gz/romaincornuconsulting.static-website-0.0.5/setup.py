import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = "0.0.5"

setuptools.setup(
    name="romaincornuconsulting.static-website",
    version=__version__,

    description="Static website",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Romain CORNU",
    author_email="consulting@romaincornu.com",

    packages=setuptools.find_packages(),

    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws-events",
        "aws-cdk.aws-events-targets",
        "aws-cdk.aws-certificatemanager",
        "aws-cdk.aws-cloudfront",
        "aws-cdk.aws-route53",
        "aws-cdk.aws-route53-targets",
        "aws-cdk.aws-s3",
        "aws-cdk.aws-s3-deployment",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)