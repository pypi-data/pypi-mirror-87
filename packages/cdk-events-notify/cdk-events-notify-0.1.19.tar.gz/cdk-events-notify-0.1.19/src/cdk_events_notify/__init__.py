"""
[![NPM version](https://badge.fury.io/js/cdk-events-notify.svg)](https://badge.fury.io/js/cdk-events-notify)
[![PyPI version](https://badge.fury.io/py/cdk-events-notify.svg)](https://badge.fury.io/py/cdk-events-notify)
![Release](https://github.com/guan840912/cdk-s3bucket/workflows/Release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-events-notify?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-events-notify?label=pypi&color=blue)

# cdk-events-notify

cdk-events-notify is an AWS CDK construct library that provides you know who login in your aws console.

## Welcome to contribute another event notify case you want.

### Now support

* Line Notify

# You need Line Notify access token

> more see [line notify docs](https://notify-bot.line.me/doc/en/)

![](./images/access-token.png)

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_events_notify import EeventNotify

app = cdk.App()
stack = cdk.Stack(app, "integ-stack", env=env)
EeventNotify(stack, "LineEeventNotify", line_notify_token=process.env.LINE_NOTIFY_TOKEN)
```

### To deploy

```bash
cdk deploy
```

### To destroy

```bash
cdk destroy
```

### Finally

![](./images/line-chat.jpg)

### Overview

![](./images/overview.png)

## More about EventBridge and Lambda

* [EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/aws-events.html)
* [Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)

> Note: Event Bridge can not cross region , if you console sign in not the cdk-events-notify region will not get the evnet in cloudtrail see this [docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/cloudtrail-integration.html#cloudtrail-integration_signin-regions)

## :clap:  Supporters

[![Stargazers repo roster for @guan840912/cdk-events-notify](https://reporoster.com/stars/guan840912/cdk-events-notify)](https://github.com/guan840912/cdk-events-notify/stargazers)
[![Forkers repo roster for @guan840912/cdk-events-notify](https://reporoster.com/forks/guan840912/cdk-events-notify)](https://github.com/guan840912/cdk-events-notify/network/members)
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


class EeventNotify(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-events-notify.EeventNotify",
):
    """
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        line_notify_token: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param line_notify_token: (experimental) Line Notify Token for Lambda send notify permisson.

        :stability: experimental
        """
        props = EventNotifyProps(line_notify_token=line_notify_token)

        jsii.create(EeventNotify, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-events-notify.EventNotifyProps",
    jsii_struct_bases=[],
    name_mapping={"line_notify_token": "lineNotifyToken"},
)
class EventNotifyProps:
    def __init__(
        self,
        *,
        line_notify_token: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param line_notify_token: (experimental) Line Notify Token for Lambda send notify permisson.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if line_notify_token is not None:
            self._values["line_notify_token"] = line_notify_token

    @builtins.property
    def line_notify_token(self) -> typing.Optional[builtins.str]:
        """(experimental) Line Notify Token for Lambda send notify permisson.

        :stability: experimental
        """
        result = self._values.get("line_notify_token")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventNotifyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EeventNotify",
    "EventNotifyProps",
]

publication.publish()
