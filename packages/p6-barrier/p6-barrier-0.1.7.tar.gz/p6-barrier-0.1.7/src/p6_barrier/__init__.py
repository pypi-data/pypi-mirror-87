"""
P6Barrier is an `AWS CDK Construct` that deploys a `Custom Resource` which
will poll until `AWS Lambda Function` `isReady` returns true. Ideal for running
code AFTER an `RDS` or `EKS` is ready.

# P6Barrier

* [P6Barrier](#p6barrier)

  * [Badges](#badges)
  * [Distributions](#distributions)
  * [Summary](#summary)

    * [Usage](#usage)
    * [Example 1 - External Lambda](#example-1---external-lambda)
    * [Example 2 - CDK Lambda (same stack)](#example-2---cdk-lambda-same-stack)
  * [Contributing](#contributing)
  * [Code of Conduct](#code-of-conduct)
  * [Changes](#changes)
  * [Authors](#authors)

## Badges

[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/p6m7g8/p6-barrier)
![Build](https://github.com/p6m7g8/p6-barrier/workflows/Build/badge.svg)
![Release](https://github.com/p6m7g8/p6-barrier/workflows/Release/badge.svg)
[![Mergify](https://img.shields.io/endpoint.svg?url=https://gh.mergify.io/badges/p6m7g8/p6-barrier/&style=flat)](https://mergify.io)

## Distributions

[![npm version](https://badge.fury.io/js/p6-barrier!.svg)](https://badge.fury.io/js/p6-barrier)
[![PyPI version](https://badge.fury.io/py/p6-barrier!.svg)](https://badge.fury.io/py/p6-barrier)
[![NuGet version](https://badge.fury.io/nu/P6m7g8.P6Namer.svg)](https://badge.fury.io/nu/P6m7g8.P6Namer)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/P6m7g8.P6Namer/P6Namer/badge.svg)](https://maven-badges.herokuapp.com/maven-central/P6m7g8.P6Namer/P6Namer)

## Summary

Use this to wait for an `RDS` or for that matter anything to become ready.

This deploys a Custom Resource which is obviously backed by an `AWS Lambda`.
This `lambda` calls the `lambda` with `Arn` `functionArn`.

This function should return the string 'True' if the resource is ready.
Otherwise 'False'.  This function must be provided by you and is custom
for your needs.

This is abstracted from `@aws-cdk/aws-eks/cluster.ts` where a `Custom Resource`
which makes an `SSM Parameter` is used as a barrier for `Resources` to depend
on until the `EKS` Cluster is ready for `Helm` to be run via an `addHelmChart`

### Usage

### Example 1 - External Lambda

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from p6_barrier import P6Barrier

P6Barrier(self, "p6-barrier",
    name="some_useful_name",
    dependencies=[dep1, dep2],
    function="functionArn"
)
```

### Example 2 - CDK Lambda (same stack)

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from p6_barrier import P6Barrier

is_ready = lambda_.Function(self, "isReady",
    runtime=lambda_.Runtime.PYTHON_3_8,
    timeout=Duration.minutes(15),
    tracing=lambda_.Tracing.ACTIVE,
    handler="index.handler",
    code=lambda_.Code.from_asset(path.join(__dirname, "../resources/lambda/isReady"))
)

P6Barrier(self, "p6-barrier",
    name="some_useful_name",
    dependencies=[dep1, dep2],
    function=is_ready.function_arn
)
```

## Contributing

* [How to Contribute](CONTRIBUTING.md)

## Code of Conduct

* [Code of Conduct](CODE_OF_CONDUCT.md)

## Changes

* [Change Log](CHANGELOG.md)

## Authors

Philip M. Gollucci [pgollucci@p6m7g8.com](mailto:pgollucci@p6m7g8.com)
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


@jsii.interface(jsii_type="p6-barrier.IP6BarrierProps")
class IP6BarrierProps(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IP6BarrierPropsProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List[aws_cdk.core.Construct]:
        ...

    @dependencies.setter # type: ignore
    def dependencies(self, value: typing.List[aws_cdk.core.Construct]) -> None:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="function")
    def function(self) -> builtins.str:
        ...

    @function.setter # type: ignore
    def function(self, value: builtins.str) -> None:
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        ...

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        ...


class _IP6BarrierPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "p6-barrier.IP6BarrierProps"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List[aws_cdk.core.Construct]:
        return jsii.get(self, "dependencies")

    @dependencies.setter # type: ignore
    def dependencies(self, value: typing.List[aws_cdk.core.Construct]) -> None:
        jsii.set(self, "dependencies", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="function")
    def function(self) -> builtins.str:
        return jsii.get(self, "function")

    @function.setter # type: ignore
    def function(self, value: builtins.str) -> None:
        jsii.set(self, "function", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)


class P6Barrier(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="p6-barrier.P6Barrier",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: IP6BarrierProps,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        """
        jsii.create(P6Barrier, self, [scope, id, props])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, dependencies: typing.List[aws_cdk.core.Construct]) -> None:
        """
        :param dependencies: -
        """
        return jsii.invoke(self, "addDependency", [dependencies])


__all__ = [
    "IP6BarrierProps",
    "P6Barrier",
]

publication.publish()
