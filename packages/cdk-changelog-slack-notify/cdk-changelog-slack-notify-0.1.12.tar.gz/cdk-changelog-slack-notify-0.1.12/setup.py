import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-changelog-slack-notify",
    "version": "0.1.12",
    "description": "A JSII construct lib to deploy a service to send new changes pushed to codecommit to slack channel",
    "license": "MIT",
    "url": "https://github.com/mikeyangyo/cdk-changelog-slack-notify.git",
    "long_description_content_type": "text/markdown",
    "author": "mikeyangyo<perryvm06vm06@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mikeyangyo/cdk-changelog-slack-notify.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_changelog_slack_notify",
        "cdk_changelog_slack_notify._jsii"
    ],
    "package_data": {
        "cdk_changelog_slack_notify._jsii": [
            "cdk-changelog-slack-notify@0.1.12.jsii.tgz"
        ],
        "cdk_changelog_slack_notify": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-codecommit>=1.74.0, <2.0.0",
        "aws-cdk.aws-events-targets>=1.74.0, <2.0.0",
        "aws-cdk.aws-iam>=1.74.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.74.0, <2.0.0",
        "aws-cdk.core>=1.74.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.15.0, <2.0.0",
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

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
