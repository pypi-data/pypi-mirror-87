[![NPM version](https://badge.fury.io/js/cdk-changelog-slack-notify.svg)](https://badge.fury.io/js/cdk-changelog-slack-notify)
[![PyPI version](https://badge.fury.io/py/cdk-changelog-slack-notify.svg)](https://badge.fury.io/py/cdk-changelog-slack-notify)
![Release](https://github.com/mikeyangyo/cdk-changelog-slack-notify/workflows/Release/badge.svg)
[![codecov](https://codecov.io/gh/mikeyangyo/cdk-changelog-slack-notify/branch/main/graph/badge.svg?token=MNQ4CKJDLS)](https://codecov.io/gh/mikeyangyo/cdk-changelog-slack-notify)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=grey)
![npm](https://img.shields.io/npm/dt/cdk-changelog-slack-notify?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-changelog-slack-notify?label=pypi&color=blue)

# cdk-changelog-slack-notify

`cdk-changelog-slack-notify` is an AWS CDK construct library that allows you to send slack notification for new changes pushed to CodeCommit with AWS CDK in Typescript or Python.

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_changelog_slack_notify import ChangelogSlackNotify

app = cdk.App()

env = {
    "region": process.env.CDK_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

demo_stack = cdk.Stack(app, "DemoStack", env=env)

ChangelogSlackNotify(test_stack, "ChangelogSlackNotify",
    repository_name="test-repo",
    slack_token="slack-token",
    channel_name="slack-channel-name"
)
```

# Deploy

```sh
cdk deploy
```

# Architecture

![architecture diagram](https://drive.google.com/uc?export=view&id=1icUVmbTXmVqjedLBRF3w2itayQlpjpUV)

# Screenshots

## without changelog:

![without changelog image](https://drive.google.com/uc?export=view&id=1hscxSGuIF93bUAjpjzx5jIbbvLStNHnA)

## with changelog :

![with changelog image](https://drive.google.com/uc?export=view&id=1GruPitrk4_gogl9nhwp71hrnDXFUe3jD)

# Credits

This project a based heavily on work by the following:

* commitizen-tools for [commitizen](https://github.com/commitizen-tools/commitizen)
