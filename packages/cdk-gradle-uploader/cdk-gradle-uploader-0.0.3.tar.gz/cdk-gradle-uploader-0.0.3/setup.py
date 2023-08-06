import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-gradle-uploader",
    "version": "0.0.3",
    "description": "Uploads new Gradle versions to an S3 bucket",
    "license": "Apache-2.0",
    "url": "https://github.com/stefan.freitag/projen_gradle_uploader.git",
    "long_description_content_type": "text/markdown",
    "author": "Stefan Freitag<stefan.freitag@udo.edu>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/stefan.freitag/projen_gradle_uploader.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_gradle_uploader",
        "cdk_gradle_uploader._jsii"
    ],
    "package_data": {
        "cdk_gradle_uploader._jsii": [
            "Gradle_S3_Uploader@0.0.3.jsii.tgz"
        ],
        "cdk_gradle_uploader": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-events-targets>=1.76.0, <2.0.0",
        "aws-cdk.aws-events>=1.76.0, <2.0.0",
        "aws-cdk.aws-iam>=1.76.0, <2.0.0",
        "aws-cdk.aws-lambda-python>=1.76.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.76.0, <2.0.0",
        "aws-cdk.aws-logs>=1.76.0, <2.0.0",
        "aws-cdk.aws-s3>=1.76.0, <2.0.0",
        "aws-cdk.aws-sns-subscriptions>=1.76.0, <2.0.0",
        "aws-cdk.aws-sns>=1.76.0, <2.0.0",
        "aws-cdk.core>=1.76.0, <2.0.0",
        "constructs>=3.2.0, <4.0.0",
        "jsii>=1.13.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
