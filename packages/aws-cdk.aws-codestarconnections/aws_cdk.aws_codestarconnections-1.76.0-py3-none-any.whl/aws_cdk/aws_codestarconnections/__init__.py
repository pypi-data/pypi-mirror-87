"""
## AWS::CodeStarConnections Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codestarconnections as codestarconnections
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

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnConnection(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codestarconnections.CfnConnection",
):
    """A CloudFormation ``AWS::CodeStarConnections::Connection``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html
    :cloudformationResource: AWS::CodeStarConnections::Connection
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        connection_name: builtins.str,
        host_arn: typing.Optional[builtins.str] = None,
        provider_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::CodeStarConnections::Connection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param connection_name: ``AWS::CodeStarConnections::Connection.ConnectionName``.
        :param host_arn: ``AWS::CodeStarConnections::Connection.HostArn``.
        :param provider_type: ``AWS::CodeStarConnections::Connection.ProviderType``.
        :param tags: ``AWS::CodeStarConnections::Connection.Tags``.
        """
        props = CfnConnectionProps(
            connection_name=connection_name,
            host_arn=host_arn,
            provider_type=provider_type,
            tags=tags,
        )

        jsii.create(CfnConnection, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrConnectionArn")
    def attr_connection_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: ConnectionArn
        """
        return jsii.get(self, "attrConnectionArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrConnectionStatus")
    def attr_connection_status(self) -> builtins.str:
        """
        :cloudformationAttribute: ConnectionStatus
        """
        return jsii.get(self, "attrConnectionStatus")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrOwnerAccountId")
    def attr_owner_account_id(self) -> builtins.str:
        """
        :cloudformationAttribute: OwnerAccountId
        """
        return jsii.get(self, "attrOwnerAccountId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::CodeStarConnections::Connection.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        """``AWS::CodeStarConnections::Connection.ConnectionName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-connectionname
        """
        return jsii.get(self, "connectionName")

    @connection_name.setter # type: ignore
    def connection_name(self, value: builtins.str) -> None:
        jsii.set(self, "connectionName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="hostArn")
    def host_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeStarConnections::Connection.HostArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-hostarn
        """
        return jsii.get(self, "hostArn")

    @host_arn.setter # type: ignore
    def host_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "hostArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="providerType")
    def provider_type(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeStarConnections::Connection.ProviderType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-providertype
        """
        return jsii.get(self, "providerType")

    @provider_type.setter # type: ignore
    def provider_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "providerType", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codestarconnections.CfnConnectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_name": "connectionName",
        "host_arn": "hostArn",
        "provider_type": "providerType",
        "tags": "tags",
    },
)
class CfnConnectionProps:
    def __init__(
        self,
        *,
        connection_name: builtins.str,
        host_arn: typing.Optional[builtins.str] = None,
        provider_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodeStarConnections::Connection``.

        :param connection_name: ``AWS::CodeStarConnections::Connection.ConnectionName``.
        :param host_arn: ``AWS::CodeStarConnections::Connection.HostArn``.
        :param provider_type: ``AWS::CodeStarConnections::Connection.ProviderType``.
        :param tags: ``AWS::CodeStarConnections::Connection.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "connection_name": connection_name,
        }
        if host_arn is not None:
            self._values["host_arn"] = host_arn
        if provider_type is not None:
            self._values["provider_type"] = provider_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connection_name(self) -> builtins.str:
        """``AWS::CodeStarConnections::Connection.ConnectionName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-connectionname
        """
        result = self._values.get("connection_name")
        assert result is not None, "Required property 'connection_name' is missing"
        return result

    @builtins.property
    def host_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeStarConnections::Connection.HostArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-hostarn
        """
        result = self._values.get("host_arn")
        return result

    @builtins.property
    def provider_type(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeStarConnections::Connection.ProviderType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-providertype
        """
        result = self._values.get("provider_type")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::CodeStarConnections::Connection.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnConnection",
    "CfnConnectionProps",
]

publication.publish()
