"""
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
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


class ChangelogSlackNotify(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-changelog-slack-notify.ChangelogSlackNotify",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        channel_name: builtins.str,
        repository_name: builtins.str,
        slack_token: builtins.str,
        breaking_change_type_display_name: typing.Optional[builtins.str] = None,
        changelog_path: typing.Optional[builtins.str] = None,
        feature_type_display_name: typing.Optional[builtins.str] = None,
        fix_type_display_name: typing.Optional[builtins.str] = None,
        from_exist_repository: typing.Optional[builtins.bool] = None,
        performance_type_display_name: typing.Optional[builtins.str] = None,
        tracking_branches: typing.Optional[typing.List[builtins.str]] = None,
        undefined_type_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param channel_name: Slack channel name for sending message.
        :param repository_name: repository name to track.
        :param slack_token: Slack secret token for sending message.
        :param breaking_change_type_display_name: Display name in notification message for breaking changes. Default: - If this value is *not* set, considers to BREAKING CHANGES
        :param changelog_path: Path of changelog file in repository. Default: - If this value is *not* set, considers to read commits push in master on this time to build notification message
        :param feature_type_display_name: Display name in notification message for feature changes. Default: - If this value is *not* set, considers to New Features
        :param fix_type_display_name: Display name in notification message for fix changes. Default: - If this value is *not* set, considers to Bugs Fixed
        :param from_exist_repository: set True to use $repositoryName to find exist repository. on the other hand, create a repository named $repositoryName Default: - If this value is *not* set, considers to false
        :param performance_type_display_name: Display name in notification message for performance improvement changes. Default: - If this value is *not* set, considers to Performance Improvement
        :param tracking_branches: Branches which were tracking to send notification message. Default: - If this value is *not* set, considers to track master branch
        :param undefined_type_display_name: Display name in notification message for undefined type changes. Default: - If this value is *not* set, considers to Others
        """
        props = ChangelogSlackNotifyProps(
            channel_name=channel_name,
            repository_name=repository_name,
            slack_token=slack_token,
            breaking_change_type_display_name=breaking_change_type_display_name,
            changelog_path=changelog_path,
            feature_type_display_name=feature_type_display_name,
            fix_type_display_name=fix_type_display_name,
            from_exist_repository=from_exist_repository,
            performance_type_display_name=performance_type_display_name,
            tracking_branches=tracking_branches,
            undefined_type_display_name=undefined_type_display_name,
        )

        jsii.create(ChangelogSlackNotify, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-changelog-slack-notify.ChangelogSlackNotifyProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_name": "channelName",
        "repository_name": "repositoryName",
        "slack_token": "slackToken",
        "breaking_change_type_display_name": "breakingChangeTypeDisplayName",
        "changelog_path": "changelogPath",
        "feature_type_display_name": "featureTypeDisplayName",
        "fix_type_display_name": "fixTypeDisplayName",
        "from_exist_repository": "fromExistRepository",
        "performance_type_display_name": "performanceTypeDisplayName",
        "tracking_branches": "trackingBranches",
        "undefined_type_display_name": "undefinedTypeDisplayName",
    },
)
class ChangelogSlackNotifyProps:
    def __init__(
        self,
        *,
        channel_name: builtins.str,
        repository_name: builtins.str,
        slack_token: builtins.str,
        breaking_change_type_display_name: typing.Optional[builtins.str] = None,
        changelog_path: typing.Optional[builtins.str] = None,
        feature_type_display_name: typing.Optional[builtins.str] = None,
        fix_type_display_name: typing.Optional[builtins.str] = None,
        from_exist_repository: typing.Optional[builtins.bool] = None,
        performance_type_display_name: typing.Optional[builtins.str] = None,
        tracking_branches: typing.Optional[typing.List[builtins.str]] = None,
        undefined_type_display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param channel_name: Slack channel name for sending message.
        :param repository_name: repository name to track.
        :param slack_token: Slack secret token for sending message.
        :param breaking_change_type_display_name: Display name in notification message for breaking changes. Default: - If this value is *not* set, considers to BREAKING CHANGES
        :param changelog_path: Path of changelog file in repository. Default: - If this value is *not* set, considers to read commits push in master on this time to build notification message
        :param feature_type_display_name: Display name in notification message for feature changes. Default: - If this value is *not* set, considers to New Features
        :param fix_type_display_name: Display name in notification message for fix changes. Default: - If this value is *not* set, considers to Bugs Fixed
        :param from_exist_repository: set True to use $repositoryName to find exist repository. on the other hand, create a repository named $repositoryName Default: - If this value is *not* set, considers to false
        :param performance_type_display_name: Display name in notification message for performance improvement changes. Default: - If this value is *not* set, considers to Performance Improvement
        :param tracking_branches: Branches which were tracking to send notification message. Default: - If this value is *not* set, considers to track master branch
        :param undefined_type_display_name: Display name in notification message for undefined type changes. Default: - If this value is *not* set, considers to Others
        """
        self._values: typing.Dict[str, typing.Any] = {
            "channel_name": channel_name,
            "repository_name": repository_name,
            "slack_token": slack_token,
        }
        if breaking_change_type_display_name is not None:
            self._values["breaking_change_type_display_name"] = breaking_change_type_display_name
        if changelog_path is not None:
            self._values["changelog_path"] = changelog_path
        if feature_type_display_name is not None:
            self._values["feature_type_display_name"] = feature_type_display_name
        if fix_type_display_name is not None:
            self._values["fix_type_display_name"] = fix_type_display_name
        if from_exist_repository is not None:
            self._values["from_exist_repository"] = from_exist_repository
        if performance_type_display_name is not None:
            self._values["performance_type_display_name"] = performance_type_display_name
        if tracking_branches is not None:
            self._values["tracking_branches"] = tracking_branches
        if undefined_type_display_name is not None:
            self._values["undefined_type_display_name"] = undefined_type_display_name

    @builtins.property
    def channel_name(self) -> builtins.str:
        """Slack channel name for sending message."""
        result = self._values.get("channel_name")
        assert result is not None, "Required property 'channel_name' is missing"
        return result

    @builtins.property
    def repository_name(self) -> builtins.str:
        """repository name to track."""
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return result

    @builtins.property
    def slack_token(self) -> builtins.str:
        """Slack secret token for sending message."""
        result = self._values.get("slack_token")
        assert result is not None, "Required property 'slack_token' is missing"
        return result

    @builtins.property
    def breaking_change_type_display_name(self) -> typing.Optional[builtins.str]:
        """Display name in notification message for breaking changes.

        :default: - If this value is *not* set, considers to BREAKING CHANGES
        """
        result = self._values.get("breaking_change_type_display_name")
        return result

    @builtins.property
    def changelog_path(self) -> typing.Optional[builtins.str]:
        """Path of changelog file in repository.

        :default:

        - If this value is *not* set,
        considers to read commits push in master on this time to build notification message
        """
        result = self._values.get("changelog_path")
        return result

    @builtins.property
    def feature_type_display_name(self) -> typing.Optional[builtins.str]:
        """Display name in notification message for feature changes.

        :default: - If this value is *not* set, considers to New Features
        """
        result = self._values.get("feature_type_display_name")
        return result

    @builtins.property
    def fix_type_display_name(self) -> typing.Optional[builtins.str]:
        """Display name in notification message for fix changes.

        :default: - If this value is *not* set, considers to Bugs Fixed
        """
        result = self._values.get("fix_type_display_name")
        return result

    @builtins.property
    def from_exist_repository(self) -> typing.Optional[builtins.bool]:
        """set True to use $repositoryName to find exist repository.

        on the other hand, create a repository named $repositoryName

        :default: - If this value is *not* set, considers to false
        """
        result = self._values.get("from_exist_repository")
        return result

    @builtins.property
    def performance_type_display_name(self) -> typing.Optional[builtins.str]:
        """Display name in notification message for performance improvement changes.

        :default: - If this value is *not* set, considers to Performance Improvement
        """
        result = self._values.get("performance_type_display_name")
        return result

    @builtins.property
    def tracking_branches(self) -> typing.Optional[typing.List[builtins.str]]:
        """Branches which were tracking to send notification message.

        :default: - If this value is *not* set, considers to track master branch
        """
        result = self._values.get("tracking_branches")
        return result

    @builtins.property
    def undefined_type_display_name(self) -> typing.Optional[builtins.str]:
        """Display name in notification message for undefined type changes.

        :default: - If this value is *not* set, considers to Others
        """
        result = self._values.get("undefined_type_display_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChangelogSlackNotifyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ChangelogSlackNotify",
    "ChangelogSlackNotifyProps",
]

publication.publish()
