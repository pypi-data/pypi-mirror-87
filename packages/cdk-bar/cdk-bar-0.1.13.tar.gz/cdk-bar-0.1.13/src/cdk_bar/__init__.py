"""
[![NPM version](https://badge.fury.io/js/cdk-bar.svg)](https://badge.fury.io/js/cdk-bar)
[![PyPI version](https://badge.fury.io/py/cdk-bar.svg)](https://badge.fury.io/py/cdk-bar)
![Release](https://github.com/aws-samples/aws-cdk-for-k3scluster/workflows/Release/badge.svg)

# cdk-bar

A demo construct library created with `Projen` :-)

# sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()

stack = cdk.Stack(app, "my-demo-stack")

Bar(stack, "MyBar")
```
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

import aws_cdk.aws_ec2
import aws_cdk.core


class Bar(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-bar.Bar"):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: 
        """
        props = BarProps(vpc=vpc)

        jsii.create(Bar, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return jsii.get(self, "endpoint")


@jsii.data_type(
    jsii_type="cdk-bar.BarProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc"},
)
class BarProps:
    def __init__(self, *, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None) -> None:
        """
        :param vpc: 
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BarProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Bar",
    "BarProps",
]

publication.publish()
