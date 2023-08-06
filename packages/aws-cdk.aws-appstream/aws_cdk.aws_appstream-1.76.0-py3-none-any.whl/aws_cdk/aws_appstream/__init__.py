"""
## Amazon AppStream 2.0 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_appstream as appstream
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
class CfnDirectoryConfig(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfig",
):
    """A CloudFormation ``AWS::AppStream::DirectoryConfig``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html
    :cloudformationResource: AWS::AppStream::DirectoryConfig
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        directory_name: builtins.str,
        organizational_unit_distinguished_names: typing.List[builtins.str],
        service_account_credentials: typing.Union[aws_cdk.core.IResolvable, "CfnDirectoryConfig.ServiceAccountCredentialsProperty"],
    ) -> None:
        """Create a new ``AWS::AppStream::DirectoryConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param directory_name: ``AWS::AppStream::DirectoryConfig.DirectoryName``.
        :param organizational_unit_distinguished_names: ``AWS::AppStream::DirectoryConfig.OrganizationalUnitDistinguishedNames``.
        :param service_account_credentials: ``AWS::AppStream::DirectoryConfig.ServiceAccountCredentials``.
        """
        props = CfnDirectoryConfigProps(
            directory_name=directory_name,
            organizational_unit_distinguished_names=organizational_unit_distinguished_names,
            service_account_credentials=service_account_credentials,
        )

        jsii.create(CfnDirectoryConfig, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="directoryName")
    def directory_name(self) -> builtins.str:
        """``AWS::AppStream::DirectoryConfig.DirectoryName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-directoryname
        """
        return jsii.get(self, "directoryName")

    @directory_name.setter # type: ignore
    def directory_name(self, value: builtins.str) -> None:
        jsii.set(self, "directoryName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="organizationalUnitDistinguishedNames")
    def organizational_unit_distinguished_names(self) -> typing.List[builtins.str]:
        """``AWS::AppStream::DirectoryConfig.OrganizationalUnitDistinguishedNames``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-organizationalunitdistinguishednames
        """
        return jsii.get(self, "organizationalUnitDistinguishedNames")

    @organizational_unit_distinguished_names.setter # type: ignore
    def organizational_unit_distinguished_names(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        jsii.set(self, "organizationalUnitDistinguishedNames", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serviceAccountCredentials")
    def service_account_credentials(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnDirectoryConfig.ServiceAccountCredentialsProperty"]:
        """``AWS::AppStream::DirectoryConfig.ServiceAccountCredentials``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-serviceaccountcredentials
        """
        return jsii.get(self, "serviceAccountCredentials")

    @service_account_credentials.setter # type: ignore
    def service_account_credentials(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnDirectoryConfig.ServiceAccountCredentialsProperty"],
    ) -> None:
        jsii.set(self, "serviceAccountCredentials", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfig.ServiceAccountCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_name": "accountName",
            "account_password": "accountPassword",
        },
    )
    class ServiceAccountCredentialsProperty:
        def __init__(
            self,
            *,
            account_name: builtins.str,
            account_password: builtins.str,
        ) -> None:
            """
            :param account_name: ``CfnDirectoryConfig.ServiceAccountCredentialsProperty.AccountName``.
            :param account_password: ``CfnDirectoryConfig.ServiceAccountCredentialsProperty.AccountPassword``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "account_name": account_name,
                "account_password": account_password,
            }

        @builtins.property
        def account_name(self) -> builtins.str:
            """``CfnDirectoryConfig.ServiceAccountCredentialsProperty.AccountName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html#cfn-appstream-directoryconfig-serviceaccountcredentials-accountname
            """
            result = self._values.get("account_name")
            assert result is not None, "Required property 'account_name' is missing"
            return result

        @builtins.property
        def account_password(self) -> builtins.str:
            """``CfnDirectoryConfig.ServiceAccountCredentialsProperty.AccountPassword``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html#cfn-appstream-directoryconfig-serviceaccountcredentials-accountpassword
            """
            result = self._values.get("account_password")
            assert result is not None, "Required property 'account_password' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceAccountCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "directory_name": "directoryName",
        "organizational_unit_distinguished_names": "organizationalUnitDistinguishedNames",
        "service_account_credentials": "serviceAccountCredentials",
    },
)
class CfnDirectoryConfigProps:
    def __init__(
        self,
        *,
        directory_name: builtins.str,
        organizational_unit_distinguished_names: typing.List[builtins.str],
        service_account_credentials: typing.Union[aws_cdk.core.IResolvable, CfnDirectoryConfig.ServiceAccountCredentialsProperty],
    ) -> None:
        """Properties for defining a ``AWS::AppStream::DirectoryConfig``.

        :param directory_name: ``AWS::AppStream::DirectoryConfig.DirectoryName``.
        :param organizational_unit_distinguished_names: ``AWS::AppStream::DirectoryConfig.OrganizationalUnitDistinguishedNames``.
        :param service_account_credentials: ``AWS::AppStream::DirectoryConfig.ServiceAccountCredentials``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "directory_name": directory_name,
            "organizational_unit_distinguished_names": organizational_unit_distinguished_names,
            "service_account_credentials": service_account_credentials,
        }

    @builtins.property
    def directory_name(self) -> builtins.str:
        """``AWS::AppStream::DirectoryConfig.DirectoryName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-directoryname
        """
        result = self._values.get("directory_name")
        assert result is not None, "Required property 'directory_name' is missing"
        return result

    @builtins.property
    def organizational_unit_distinguished_names(self) -> typing.List[builtins.str]:
        """``AWS::AppStream::DirectoryConfig.OrganizationalUnitDistinguishedNames``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-organizationalunitdistinguishednames
        """
        result = self._values.get("organizational_unit_distinguished_names")
        assert result is not None, "Required property 'organizational_unit_distinguished_names' is missing"
        return result

    @builtins.property
    def service_account_credentials(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnDirectoryConfig.ServiceAccountCredentialsProperty]:
        """``AWS::AppStream::DirectoryConfig.ServiceAccountCredentials``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-serviceaccountcredentials
        """
        result = self._values.get("service_account_credentials")
        assert result is not None, "Required property 'service_account_credentials' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDirectoryConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnFleet(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnFleet",
):
    """A CloudFormation ``AWS::AppStream::Fleet``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html
    :cloudformationResource: AWS::AppStream::Fleet
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        compute_capacity: typing.Union["CfnFleet.ComputeCapacityProperty", aws_cdk.core.IResolvable],
        instance_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.DomainJoinInfoProperty"]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
        stream_view: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        vpc_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.VpcConfigProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::AppStream::Fleet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param compute_capacity: ``AWS::AppStream::Fleet.ComputeCapacity``.
        :param instance_type: ``AWS::AppStream::Fleet.InstanceType``.
        :param name: ``AWS::AppStream::Fleet.Name``.
        :param description: ``AWS::AppStream::Fleet.Description``.
        :param disconnect_timeout_in_seconds: ``AWS::AppStream::Fleet.DisconnectTimeoutInSeconds``.
        :param display_name: ``AWS::AppStream::Fleet.DisplayName``.
        :param domain_join_info: ``AWS::AppStream::Fleet.DomainJoinInfo``.
        :param enable_default_internet_access: ``AWS::AppStream::Fleet.EnableDefaultInternetAccess``.
        :param fleet_type: ``AWS::AppStream::Fleet.FleetType``.
        :param iam_role_arn: ``AWS::AppStream::Fleet.IamRoleArn``.
        :param idle_disconnect_timeout_in_seconds: ``AWS::AppStream::Fleet.IdleDisconnectTimeoutInSeconds``.
        :param image_arn: ``AWS::AppStream::Fleet.ImageArn``.
        :param image_name: ``AWS::AppStream::Fleet.ImageName``.
        :param max_user_duration_in_seconds: ``AWS::AppStream::Fleet.MaxUserDurationInSeconds``.
        :param stream_view: ``AWS::AppStream::Fleet.StreamView``.
        :param tags: ``AWS::AppStream::Fleet.Tags``.
        :param vpc_config: ``AWS::AppStream::Fleet.VpcConfig``.
        """
        props = CfnFleetProps(
            compute_capacity=compute_capacity,
            instance_type=instance_type,
            name=name,
            description=description,
            disconnect_timeout_in_seconds=disconnect_timeout_in_seconds,
            display_name=display_name,
            domain_join_info=domain_join_info,
            enable_default_internet_access=enable_default_internet_access,
            fleet_type=fleet_type,
            iam_role_arn=iam_role_arn,
            idle_disconnect_timeout_in_seconds=idle_disconnect_timeout_in_seconds,
            image_arn=image_arn,
            image_name=image_name,
            max_user_duration_in_seconds=max_user_duration_in_seconds,
            stream_view=stream_view,
            tags=tags,
            vpc_config=vpc_config,
        )

        jsii.create(CfnFleet, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::AppStream::Fleet.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="computeCapacity")
    def compute_capacity(
        self,
    ) -> typing.Union["CfnFleet.ComputeCapacityProperty", aws_cdk.core.IResolvable]:
        """``AWS::AppStream::Fleet.ComputeCapacity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-computecapacity
        """
        return jsii.get(self, "computeCapacity")

    @compute_capacity.setter # type: ignore
    def compute_capacity(
        self,
        value: typing.Union["CfnFleet.ComputeCapacityProperty", aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "computeCapacity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        """``AWS::AppStream::Fleet.InstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-instancetype
        """
        return jsii.get(self, "instanceType")

    @instance_type.setter # type: ignore
    def instance_type(self, value: builtins.str) -> None:
        jsii.set(self, "instanceType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::AppStream::Fleet.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="disconnectTimeoutInSeconds")
    def disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::AppStream::Fleet.DisconnectTimeoutInSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-disconnecttimeoutinseconds
        """
        return jsii.get(self, "disconnectTimeoutInSeconds")

    @disconnect_timeout_in_seconds.setter # type: ignore
    def disconnect_timeout_in_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "disconnectTimeoutInSeconds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.DisplayName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-displayname
        """
        return jsii.get(self, "displayName")

    @display_name.setter # type: ignore
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "displayName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainJoinInfo")
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.DomainJoinInfoProperty"]]:
        """``AWS::AppStream::Fleet.DomainJoinInfo``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-domainjoininfo
        """
        return jsii.get(self, "domainJoinInfo")

    @domain_join_info.setter # type: ignore
    def domain_join_info(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.DomainJoinInfoProperty"]],
    ) -> None:
        jsii.set(self, "domainJoinInfo", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enableDefaultInternetAccess")
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AppStream::Fleet.EnableDefaultInternetAccess``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-enabledefaultinternetaccess
        """
        return jsii.get(self, "enableDefaultInternetAccess")

    @enable_default_internet_access.setter # type: ignore
    def enable_default_internet_access(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "enableDefaultInternetAccess", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="fleetType")
    def fleet_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.FleetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-fleettype
        """
        return jsii.get(self, "fleetType")

    @fleet_type.setter # type: ignore
    def fleet_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "fleetType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.IamRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-iamrolearn
        """
        return jsii.get(self, "iamRoleArn")

    @iam_role_arn.setter # type: ignore
    def iam_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "iamRoleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="idleDisconnectTimeoutInSeconds")
    def idle_disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::AppStream::Fleet.IdleDisconnectTimeoutInSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-idledisconnecttimeoutinseconds
        """
        return jsii.get(self, "idleDisconnectTimeoutInSeconds")

    @idle_disconnect_timeout_in_seconds.setter # type: ignore
    def idle_disconnect_timeout_in_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "idleDisconnectTimeoutInSeconds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageArn")
    def image_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.ImageArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagearn
        """
        return jsii.get(self, "imageArn")

    @image_arn.setter # type: ignore
    def image_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "imageArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.ImageName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagename
        """
        return jsii.get(self, "imageName")

    @image_name.setter # type: ignore
    def image_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "imageName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxUserDurationInSeconds")
    def max_user_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::AppStream::Fleet.MaxUserDurationInSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-maxuserdurationinseconds
        """
        return jsii.get(self, "maxUserDurationInSeconds")

    @max_user_duration_in_seconds.setter # type: ignore
    def max_user_duration_in_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxUserDurationInSeconds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="streamView")
    def stream_view(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.StreamView``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-streamview
        """
        return jsii.get(self, "streamView")

    @stream_view.setter # type: ignore
    def stream_view(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "streamView", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.VpcConfigProperty"]]:
        """``AWS::AppStream::Fleet.VpcConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-vpcconfig
        """
        return jsii.get(self, "vpcConfig")

    @vpc_config.setter # type: ignore
    def vpc_config(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.VpcConfigProperty"]],
    ) -> None:
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnFleet.ComputeCapacityProperty",
        jsii_struct_bases=[],
        name_mapping={"desired_instances": "desiredInstances"},
    )
    class ComputeCapacityProperty:
        def __init__(self, *, desired_instances: jsii.Number) -> None:
            """
            :param desired_instances: ``CfnFleet.ComputeCapacityProperty.DesiredInstances``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-computecapacity.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "desired_instances": desired_instances,
            }

        @builtins.property
        def desired_instances(self) -> jsii.Number:
            """``CfnFleet.ComputeCapacityProperty.DesiredInstances``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-computecapacity.html#cfn-appstream-fleet-computecapacity-desiredinstances
            """
            result = self._values.get("desired_instances")
            assert result is not None, "Required property 'desired_instances' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeCapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnFleet.DomainJoinInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
        },
    )
    class DomainJoinInfoProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[builtins.str] = None,
            organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param directory_name: ``CfnFleet.DomainJoinInfoProperty.DirectoryName``.
            :param organizational_unit_distinguished_name: ``CfnFleet.DomainJoinInfoProperty.OrganizationalUnitDistinguishedName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if organizational_unit_distinguished_name is not None:
                self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name

        @builtins.property
        def directory_name(self) -> typing.Optional[builtins.str]:
            """``CfnFleet.DomainJoinInfoProperty.DirectoryName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html#cfn-appstream-fleet-domainjoininfo-directoryname
            """
            result = self._values.get("directory_name")
            return result

        @builtins.property
        def organizational_unit_distinguished_name(
            self,
        ) -> typing.Optional[builtins.str]:
            """``CfnFleet.DomainJoinInfoProperty.OrganizationalUnitDistinguishedName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html#cfn-appstream-fleet-domainjoininfo-organizationalunitdistinguishedname
            """
            result = self._values.get("organizational_unit_distinguished_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainJoinInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnFleet.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param security_group_ids: ``CfnFleet.VpcConfigProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnFleet.VpcConfigProperty.SubnetIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnFleet.VpcConfigProperty.SecurityGroupIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html#cfn-appstream-fleet-vpcconfig-securitygroupids
            """
            result = self._values.get("security_group_ids")
            return result

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnFleet.VpcConfigProperty.SubnetIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html#cfn-appstream-fleet-vpcconfig-subnetids
            """
            result = self._values.get("subnet_ids")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnFleetProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_capacity": "computeCapacity",
        "instance_type": "instanceType",
        "name": "name",
        "description": "description",
        "disconnect_timeout_in_seconds": "disconnectTimeoutInSeconds",
        "display_name": "displayName",
        "domain_join_info": "domainJoinInfo",
        "enable_default_internet_access": "enableDefaultInternetAccess",
        "fleet_type": "fleetType",
        "iam_role_arn": "iamRoleArn",
        "idle_disconnect_timeout_in_seconds": "idleDisconnectTimeoutInSeconds",
        "image_arn": "imageArn",
        "image_name": "imageName",
        "max_user_duration_in_seconds": "maxUserDurationInSeconds",
        "stream_view": "streamView",
        "tags": "tags",
        "vpc_config": "vpcConfig",
    },
)
class CfnFleetProps:
    def __init__(
        self,
        *,
        compute_capacity: typing.Union[CfnFleet.ComputeCapacityProperty, aws_cdk.core.IResolvable],
        instance_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFleet.DomainJoinInfoProperty]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
        stream_view: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        vpc_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFleet.VpcConfigProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::AppStream::Fleet``.

        :param compute_capacity: ``AWS::AppStream::Fleet.ComputeCapacity``.
        :param instance_type: ``AWS::AppStream::Fleet.InstanceType``.
        :param name: ``AWS::AppStream::Fleet.Name``.
        :param description: ``AWS::AppStream::Fleet.Description``.
        :param disconnect_timeout_in_seconds: ``AWS::AppStream::Fleet.DisconnectTimeoutInSeconds``.
        :param display_name: ``AWS::AppStream::Fleet.DisplayName``.
        :param domain_join_info: ``AWS::AppStream::Fleet.DomainJoinInfo``.
        :param enable_default_internet_access: ``AWS::AppStream::Fleet.EnableDefaultInternetAccess``.
        :param fleet_type: ``AWS::AppStream::Fleet.FleetType``.
        :param iam_role_arn: ``AWS::AppStream::Fleet.IamRoleArn``.
        :param idle_disconnect_timeout_in_seconds: ``AWS::AppStream::Fleet.IdleDisconnectTimeoutInSeconds``.
        :param image_arn: ``AWS::AppStream::Fleet.ImageArn``.
        :param image_name: ``AWS::AppStream::Fleet.ImageName``.
        :param max_user_duration_in_seconds: ``AWS::AppStream::Fleet.MaxUserDurationInSeconds``.
        :param stream_view: ``AWS::AppStream::Fleet.StreamView``.
        :param tags: ``AWS::AppStream::Fleet.Tags``.
        :param vpc_config: ``AWS::AppStream::Fleet.VpcConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "compute_capacity": compute_capacity,
            "instance_type": instance_type,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if disconnect_timeout_in_seconds is not None:
            self._values["disconnect_timeout_in_seconds"] = disconnect_timeout_in_seconds
        if display_name is not None:
            self._values["display_name"] = display_name
        if domain_join_info is not None:
            self._values["domain_join_info"] = domain_join_info
        if enable_default_internet_access is not None:
            self._values["enable_default_internet_access"] = enable_default_internet_access
        if fleet_type is not None:
            self._values["fleet_type"] = fleet_type
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if idle_disconnect_timeout_in_seconds is not None:
            self._values["idle_disconnect_timeout_in_seconds"] = idle_disconnect_timeout_in_seconds
        if image_arn is not None:
            self._values["image_arn"] = image_arn
        if image_name is not None:
            self._values["image_name"] = image_name
        if max_user_duration_in_seconds is not None:
            self._values["max_user_duration_in_seconds"] = max_user_duration_in_seconds
        if stream_view is not None:
            self._values["stream_view"] = stream_view
        if tags is not None:
            self._values["tags"] = tags
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def compute_capacity(
        self,
    ) -> typing.Union[CfnFleet.ComputeCapacityProperty, aws_cdk.core.IResolvable]:
        """``AWS::AppStream::Fleet.ComputeCapacity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-computecapacity
        """
        result = self._values.get("compute_capacity")
        assert result is not None, "Required property 'compute_capacity' is missing"
        return result

    @builtins.property
    def instance_type(self) -> builtins.str:
        """``AWS::AppStream::Fleet.InstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-instancetype
        """
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::AppStream::Fleet.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::AppStream::Fleet.DisconnectTimeoutInSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-disconnecttimeoutinseconds
        """
        result = self._values.get("disconnect_timeout_in_seconds")
        return result

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.DisplayName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-displayname
        """
        result = self._values.get("display_name")
        return result

    @builtins.property
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFleet.DomainJoinInfoProperty]]:
        """``AWS::AppStream::Fleet.DomainJoinInfo``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-domainjoininfo
        """
        result = self._values.get("domain_join_info")
        return result

    @builtins.property
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AppStream::Fleet.EnableDefaultInternetAccess``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-enabledefaultinternetaccess
        """
        result = self._values.get("enable_default_internet_access")
        return result

    @builtins.property
    def fleet_type(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.FleetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-fleettype
        """
        result = self._values.get("fleet_type")
        return result

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.IamRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-iamrolearn
        """
        result = self._values.get("iam_role_arn")
        return result

    @builtins.property
    def idle_disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::AppStream::Fleet.IdleDisconnectTimeoutInSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-idledisconnecttimeoutinseconds
        """
        result = self._values.get("idle_disconnect_timeout_in_seconds")
        return result

    @builtins.property
    def image_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.ImageArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagearn
        """
        result = self._values.get("image_arn")
        return result

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.ImageName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagename
        """
        result = self._values.get("image_name")
        return result

    @builtins.property
    def max_user_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::AppStream::Fleet.MaxUserDurationInSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-maxuserdurationinseconds
        """
        result = self._values.get("max_user_duration_in_seconds")
        return result

    @builtins.property
    def stream_view(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Fleet.StreamView``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-streamview
        """
        result = self._values.get("stream_view")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::AppStream::Fleet.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFleet.VpcConfigProperty]]:
        """``AWS::AppStream::Fleet.VpcConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-vpcconfig
        """
        result = self._values.get("vpc_config")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnImageBuilder(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder",
):
    """A CloudFormation ``AWS::AppStream::ImageBuilder``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html
    :cloudformationResource: AWS::AppStream::ImageBuilder
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        instance_type: builtins.str,
        name: builtins.str,
        access_endpoints: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnImageBuilder.AccessEndpointProperty"]]]] = None,
        appstream_agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnImageBuilder.DomainJoinInfoProperty"]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        vpc_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnImageBuilder.VpcConfigProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::AppStream::ImageBuilder``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_type: ``AWS::AppStream::ImageBuilder.InstanceType``.
        :param name: ``AWS::AppStream::ImageBuilder.Name``.
        :param access_endpoints: ``AWS::AppStream::ImageBuilder.AccessEndpoints``.
        :param appstream_agent_version: ``AWS::AppStream::ImageBuilder.AppstreamAgentVersion``.
        :param description: ``AWS::AppStream::ImageBuilder.Description``.
        :param display_name: ``AWS::AppStream::ImageBuilder.DisplayName``.
        :param domain_join_info: ``AWS::AppStream::ImageBuilder.DomainJoinInfo``.
        :param enable_default_internet_access: ``AWS::AppStream::ImageBuilder.EnableDefaultInternetAccess``.
        :param iam_role_arn: ``AWS::AppStream::ImageBuilder.IamRoleArn``.
        :param image_arn: ``AWS::AppStream::ImageBuilder.ImageArn``.
        :param image_name: ``AWS::AppStream::ImageBuilder.ImageName``.
        :param tags: ``AWS::AppStream::ImageBuilder.Tags``.
        :param vpc_config: ``AWS::AppStream::ImageBuilder.VpcConfig``.
        """
        props = CfnImageBuilderProps(
            instance_type=instance_type,
            name=name,
            access_endpoints=access_endpoints,
            appstream_agent_version=appstream_agent_version,
            description=description,
            display_name=display_name,
            domain_join_info=domain_join_info,
            enable_default_internet_access=enable_default_internet_access,
            iam_role_arn=iam_role_arn,
            image_arn=image_arn,
            image_name=image_name,
            tags=tags,
            vpc_config=vpc_config,
        )

        jsii.create(CfnImageBuilder, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrStreamingUrl")
    def attr_streaming_url(self) -> builtins.str:
        """
        :cloudformationAttribute: StreamingUrl
        """
        return jsii.get(self, "attrStreamingUrl")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::AppStream::ImageBuilder.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        """``AWS::AppStream::ImageBuilder.InstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-instancetype
        """
        return jsii.get(self, "instanceType")

    @instance_type.setter # type: ignore
    def instance_type(self, value: builtins.str) -> None:
        jsii.set(self, "instanceType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::AppStream::ImageBuilder.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="accessEndpoints")
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnImageBuilder.AccessEndpointProperty"]]]]:
        """``AWS::AppStream::ImageBuilder.AccessEndpoints``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-accessendpoints
        """
        return jsii.get(self, "accessEndpoints")

    @access_endpoints.setter # type: ignore
    def access_endpoints(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnImageBuilder.AccessEndpointProperty"]]]],
    ) -> None:
        jsii.set(self, "accessEndpoints", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="appstreamAgentVersion")
    def appstream_agent_version(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.AppstreamAgentVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-appstreamagentversion
        """
        return jsii.get(self, "appstreamAgentVersion")

    @appstream_agent_version.setter # type: ignore
    def appstream_agent_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "appstreamAgentVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.DisplayName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-displayname
        """
        return jsii.get(self, "displayName")

    @display_name.setter # type: ignore
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "displayName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainJoinInfo")
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnImageBuilder.DomainJoinInfoProperty"]]:
        """``AWS::AppStream::ImageBuilder.DomainJoinInfo``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-domainjoininfo
        """
        return jsii.get(self, "domainJoinInfo")

    @domain_join_info.setter # type: ignore
    def domain_join_info(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnImageBuilder.DomainJoinInfoProperty"]],
    ) -> None:
        jsii.set(self, "domainJoinInfo", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enableDefaultInternetAccess")
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AppStream::ImageBuilder.EnableDefaultInternetAccess``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-enabledefaultinternetaccess
        """
        return jsii.get(self, "enableDefaultInternetAccess")

    @enable_default_internet_access.setter # type: ignore
    def enable_default_internet_access(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "enableDefaultInternetAccess", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.IamRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-iamrolearn
        """
        return jsii.get(self, "iamRoleArn")

    @iam_role_arn.setter # type: ignore
    def iam_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "iamRoleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageArn")
    def image_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.ImageArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagearn
        """
        return jsii.get(self, "imageArn")

    @image_arn.setter # type: ignore
    def image_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "imageArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.ImageName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagename
        """
        return jsii.get(self, "imageName")

    @image_name.setter # type: ignore
    def image_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "imageName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnImageBuilder.VpcConfigProperty"]]:
        """``AWS::AppStream::ImageBuilder.VpcConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-vpcconfig
        """
        return jsii.get(self, "vpcConfig")

    @vpc_config.setter # type: ignore
    def vpc_config(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnImageBuilder.VpcConfigProperty"]],
    ) -> None:
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder.AccessEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint_type": "endpointType", "vpce_id": "vpceId"},
    )
    class AccessEndpointProperty:
        def __init__(
            self,
            *,
            endpoint_type: builtins.str,
            vpce_id: builtins.str,
        ) -> None:
            """
            :param endpoint_type: ``CfnImageBuilder.AccessEndpointProperty.EndpointType``.
            :param vpce_id: ``CfnImageBuilder.AccessEndpointProperty.VpceId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-accessendpoint.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "endpoint_type": endpoint_type,
                "vpce_id": vpce_id,
            }

        @builtins.property
        def endpoint_type(self) -> builtins.str:
            """``CfnImageBuilder.AccessEndpointProperty.EndpointType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-accessendpoint.html#cfn-appstream-imagebuilder-accessendpoint-endpointtype
            """
            result = self._values.get("endpoint_type")
            assert result is not None, "Required property 'endpoint_type' is missing"
            return result

        @builtins.property
        def vpce_id(self) -> builtins.str:
            """``CfnImageBuilder.AccessEndpointProperty.VpceId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-accessendpoint.html#cfn-appstream-imagebuilder-accessendpoint-vpceid
            """
            result = self._values.get("vpce_id")
            assert result is not None, "Required property 'vpce_id' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder.DomainJoinInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
        },
    )
    class DomainJoinInfoProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[builtins.str] = None,
            organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param directory_name: ``CfnImageBuilder.DomainJoinInfoProperty.DirectoryName``.
            :param organizational_unit_distinguished_name: ``CfnImageBuilder.DomainJoinInfoProperty.OrganizationalUnitDistinguishedName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if organizational_unit_distinguished_name is not None:
                self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name

        @builtins.property
        def directory_name(self) -> typing.Optional[builtins.str]:
            """``CfnImageBuilder.DomainJoinInfoProperty.DirectoryName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html#cfn-appstream-imagebuilder-domainjoininfo-directoryname
            """
            result = self._values.get("directory_name")
            return result

        @builtins.property
        def organizational_unit_distinguished_name(
            self,
        ) -> typing.Optional[builtins.str]:
            """``CfnImageBuilder.DomainJoinInfoProperty.OrganizationalUnitDistinguishedName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html#cfn-appstream-imagebuilder-domainjoininfo-organizationalunitdistinguishedname
            """
            result = self._values.get("organizational_unit_distinguished_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainJoinInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param security_group_ids: ``CfnImageBuilder.VpcConfigProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnImageBuilder.VpcConfigProperty.SubnetIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnImageBuilder.VpcConfigProperty.SecurityGroupIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html#cfn-appstream-imagebuilder-vpcconfig-securitygroupids
            """
            result = self._values.get("security_group_ids")
            return result

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnImageBuilder.VpcConfigProperty.SubnetIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html#cfn-appstream-imagebuilder-vpcconfig-subnetids
            """
            result = self._values.get("subnet_ids")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnImageBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "name": "name",
        "access_endpoints": "accessEndpoints",
        "appstream_agent_version": "appstreamAgentVersion",
        "description": "description",
        "display_name": "displayName",
        "domain_join_info": "domainJoinInfo",
        "enable_default_internet_access": "enableDefaultInternetAccess",
        "iam_role_arn": "iamRoleArn",
        "image_arn": "imageArn",
        "image_name": "imageName",
        "tags": "tags",
        "vpc_config": "vpcConfig",
    },
)
class CfnImageBuilderProps:
    def __init__(
        self,
        *,
        instance_type: builtins.str,
        name: builtins.str,
        access_endpoints: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnImageBuilder.AccessEndpointProperty]]]] = None,
        appstream_agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnImageBuilder.DomainJoinInfoProperty]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        vpc_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnImageBuilder.VpcConfigProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::AppStream::ImageBuilder``.

        :param instance_type: ``AWS::AppStream::ImageBuilder.InstanceType``.
        :param name: ``AWS::AppStream::ImageBuilder.Name``.
        :param access_endpoints: ``AWS::AppStream::ImageBuilder.AccessEndpoints``.
        :param appstream_agent_version: ``AWS::AppStream::ImageBuilder.AppstreamAgentVersion``.
        :param description: ``AWS::AppStream::ImageBuilder.Description``.
        :param display_name: ``AWS::AppStream::ImageBuilder.DisplayName``.
        :param domain_join_info: ``AWS::AppStream::ImageBuilder.DomainJoinInfo``.
        :param enable_default_internet_access: ``AWS::AppStream::ImageBuilder.EnableDefaultInternetAccess``.
        :param iam_role_arn: ``AWS::AppStream::ImageBuilder.IamRoleArn``.
        :param image_arn: ``AWS::AppStream::ImageBuilder.ImageArn``.
        :param image_name: ``AWS::AppStream::ImageBuilder.ImageName``.
        :param tags: ``AWS::AppStream::ImageBuilder.Tags``.
        :param vpc_config: ``AWS::AppStream::ImageBuilder.VpcConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "instance_type": instance_type,
            "name": name,
        }
        if access_endpoints is not None:
            self._values["access_endpoints"] = access_endpoints
        if appstream_agent_version is not None:
            self._values["appstream_agent_version"] = appstream_agent_version
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if domain_join_info is not None:
            self._values["domain_join_info"] = domain_join_info
        if enable_default_internet_access is not None:
            self._values["enable_default_internet_access"] = enable_default_internet_access
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if image_arn is not None:
            self._values["image_arn"] = image_arn
        if image_name is not None:
            self._values["image_name"] = image_name
        if tags is not None:
            self._values["tags"] = tags
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def instance_type(self) -> builtins.str:
        """``AWS::AppStream::ImageBuilder.InstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-instancetype
        """
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::AppStream::ImageBuilder.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnImageBuilder.AccessEndpointProperty]]]]:
        """``AWS::AppStream::ImageBuilder.AccessEndpoints``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-accessendpoints
        """
        result = self._values.get("access_endpoints")
        return result

    @builtins.property
    def appstream_agent_version(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.AppstreamAgentVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-appstreamagentversion
        """
        result = self._values.get("appstream_agent_version")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.DisplayName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-displayname
        """
        result = self._values.get("display_name")
        return result

    @builtins.property
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnImageBuilder.DomainJoinInfoProperty]]:
        """``AWS::AppStream::ImageBuilder.DomainJoinInfo``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-domainjoininfo
        """
        result = self._values.get("domain_join_info")
        return result

    @builtins.property
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AppStream::ImageBuilder.EnableDefaultInternetAccess``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-enabledefaultinternetaccess
        """
        result = self._values.get("enable_default_internet_access")
        return result

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.IamRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-iamrolearn
        """
        result = self._values.get("iam_role_arn")
        return result

    @builtins.property
    def image_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.ImageArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagearn
        """
        result = self._values.get("image_arn")
        return result

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::ImageBuilder.ImageName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagename
        """
        result = self._values.get("image_name")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::AppStream::ImageBuilder.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnImageBuilder.VpcConfigProperty]]:
        """``AWS::AppStream::ImageBuilder.VpcConfig``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-vpcconfig
        """
        result = self._values.get("vpc_config")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnImageBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStack(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnStack",
):
    """A CloudFormation ``AWS::AppStream::Stack``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html
    :cloudformationResource: AWS::AppStream::Stack
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        access_endpoints: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.AccessEndpointProperty"]]]] = None,
        application_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.ApplicationSettingsProperty"]] = None,
        attributes_to_delete: typing.Optional[typing.List[builtins.str]] = None,
        delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        embed_host_domains: typing.Optional[typing.List[builtins.str]] = None,
        feedback_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        storage_connectors: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.StorageConnectorProperty"]]]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        user_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.UserSettingProperty"]]]] = None,
    ) -> None:
        """Create a new ``AWS::AppStream::Stack``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_endpoints: ``AWS::AppStream::Stack.AccessEndpoints``.
        :param application_settings: ``AWS::AppStream::Stack.ApplicationSettings``.
        :param attributes_to_delete: ``AWS::AppStream::Stack.AttributesToDelete``.
        :param delete_storage_connectors: ``AWS::AppStream::Stack.DeleteStorageConnectors``.
        :param description: ``AWS::AppStream::Stack.Description``.
        :param display_name: ``AWS::AppStream::Stack.DisplayName``.
        :param embed_host_domains: ``AWS::AppStream::Stack.EmbedHostDomains``.
        :param feedback_url: ``AWS::AppStream::Stack.FeedbackURL``.
        :param name: ``AWS::AppStream::Stack.Name``.
        :param redirect_url: ``AWS::AppStream::Stack.RedirectURL``.
        :param storage_connectors: ``AWS::AppStream::Stack.StorageConnectors``.
        :param tags: ``AWS::AppStream::Stack.Tags``.
        :param user_settings: ``AWS::AppStream::Stack.UserSettings``.
        """
        props = CfnStackProps(
            access_endpoints=access_endpoints,
            application_settings=application_settings,
            attributes_to_delete=attributes_to_delete,
            delete_storage_connectors=delete_storage_connectors,
            description=description,
            display_name=display_name,
            embed_host_domains=embed_host_domains,
            feedback_url=feedback_url,
            name=name,
            redirect_url=redirect_url,
            storage_connectors=storage_connectors,
            tags=tags,
            user_settings=user_settings,
        )

        jsii.create(CfnStack, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::AppStream::Stack.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="accessEndpoints")
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.AccessEndpointProperty"]]]]:
        """``AWS::AppStream::Stack.AccessEndpoints``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-accessendpoints
        """
        return jsii.get(self, "accessEndpoints")

    @access_endpoints.setter # type: ignore
    def access_endpoints(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.AccessEndpointProperty"]]]],
    ) -> None:
        jsii.set(self, "accessEndpoints", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="applicationSettings")
    def application_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.ApplicationSettingsProperty"]]:
        """``AWS::AppStream::Stack.ApplicationSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-applicationsettings
        """
        return jsii.get(self, "applicationSettings")

    @application_settings.setter # type: ignore
    def application_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.ApplicationSettingsProperty"]],
    ) -> None:
        jsii.set(self, "applicationSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attributesToDelete")
    def attributes_to_delete(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AppStream::Stack.AttributesToDelete``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-attributestodelete
        """
        return jsii.get(self, "attributesToDelete")

    @attributes_to_delete.setter # type: ignore
    def attributes_to_delete(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "attributesToDelete", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deleteStorageConnectors")
    def delete_storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AppStream::Stack.DeleteStorageConnectors``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-deletestorageconnectors
        """
        return jsii.get(self, "deleteStorageConnectors")

    @delete_storage_connectors.setter # type: ignore
    def delete_storage_connectors(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "deleteStorageConnectors", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Stack.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Stack.DisplayName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-displayname
        """
        return jsii.get(self, "displayName")

    @display_name.setter # type: ignore
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "displayName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="embedHostDomains")
    def embed_host_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AppStream::Stack.EmbedHostDomains``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-embedhostdomains
        """
        return jsii.get(self, "embedHostDomains")

    @embed_host_domains.setter # type: ignore
    def embed_host_domains(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "embedHostDomains", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="feedbackUrl")
    def feedback_url(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Stack.FeedbackURL``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-feedbackurl
        """
        return jsii.get(self, "feedbackUrl")

    @feedback_url.setter # type: ignore
    def feedback_url(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "feedbackUrl", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Stack.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="redirectUrl")
    def redirect_url(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Stack.RedirectURL``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-redirecturl
        """
        return jsii.get(self, "redirectUrl")

    @redirect_url.setter # type: ignore
    def redirect_url(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "redirectUrl", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="storageConnectors")
    def storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.StorageConnectorProperty"]]]]:
        """``AWS::AppStream::Stack.StorageConnectors``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-storageconnectors
        """
        return jsii.get(self, "storageConnectors")

    @storage_connectors.setter # type: ignore
    def storage_connectors(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.StorageConnectorProperty"]]]],
    ) -> None:
        jsii.set(self, "storageConnectors", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userSettings")
    def user_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.UserSettingProperty"]]]]:
        """``AWS::AppStream::Stack.UserSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-usersettings
        """
        return jsii.get(self, "userSettings")

    @user_settings.setter # type: ignore
    def user_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.UserSettingProperty"]]]],
    ) -> None:
        jsii.set(self, "userSettings", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnStack.AccessEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint_type": "endpointType", "vpce_id": "vpceId"},
    )
    class AccessEndpointProperty:
        def __init__(
            self,
            *,
            endpoint_type: builtins.str,
            vpce_id: builtins.str,
        ) -> None:
            """
            :param endpoint_type: ``CfnStack.AccessEndpointProperty.EndpointType``.
            :param vpce_id: ``CfnStack.AccessEndpointProperty.VpceId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-accessendpoint.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "endpoint_type": endpoint_type,
                "vpce_id": vpce_id,
            }

        @builtins.property
        def endpoint_type(self) -> builtins.str:
            """``CfnStack.AccessEndpointProperty.EndpointType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-accessendpoint.html#cfn-appstream-stack-accessendpoint-endpointtype
            """
            result = self._values.get("endpoint_type")
            assert result is not None, "Required property 'endpoint_type' is missing"
            return result

        @builtins.property
        def vpce_id(self) -> builtins.str:
            """``CfnStack.AccessEndpointProperty.VpceId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-accessendpoint.html#cfn-appstream-stack-accessendpoint-vpceid
            """
            result = self._values.get("vpce_id")
            assert result is not None, "Required property 'vpce_id' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnStack.ApplicationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "settings_group": "settingsGroup"},
    )
    class ApplicationSettingsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
            settings_group: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param enabled: ``CfnStack.ApplicationSettingsProperty.Enabled``.
            :param settings_group: ``CfnStack.ApplicationSettingsProperty.SettingsGroup``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "enabled": enabled,
            }
            if settings_group is not None:
                self._values["settings_group"] = settings_group

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
            """``CfnStack.ApplicationSettingsProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html#cfn-appstream-stack-applicationsettings-enabled
            """
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return result

        @builtins.property
        def settings_group(self) -> typing.Optional[builtins.str]:
            """``CfnStack.ApplicationSettingsProperty.SettingsGroup``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html#cfn-appstream-stack-applicationsettings-settingsgroup
            """
            result = self._values.get("settings_group")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnStack.StorageConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_type": "connectorType",
            "domains": "domains",
            "resource_identifier": "resourceIdentifier",
        },
    )
    class StorageConnectorProperty:
        def __init__(
            self,
            *,
            connector_type: builtins.str,
            domains: typing.Optional[typing.List[builtins.str]] = None,
            resource_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param connector_type: ``CfnStack.StorageConnectorProperty.ConnectorType``.
            :param domains: ``CfnStack.StorageConnectorProperty.Domains``.
            :param resource_identifier: ``CfnStack.StorageConnectorProperty.ResourceIdentifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "connector_type": connector_type,
            }
            if domains is not None:
                self._values["domains"] = domains
            if resource_identifier is not None:
                self._values["resource_identifier"] = resource_identifier

        @builtins.property
        def connector_type(self) -> builtins.str:
            """``CfnStack.StorageConnectorProperty.ConnectorType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-connectortype
            """
            result = self._values.get("connector_type")
            assert result is not None, "Required property 'connector_type' is missing"
            return result

        @builtins.property
        def domains(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnStack.StorageConnectorProperty.Domains``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-domains
            """
            result = self._values.get("domains")
            return result

        @builtins.property
        def resource_identifier(self) -> typing.Optional[builtins.str]:
            """``CfnStack.StorageConnectorProperty.ResourceIdentifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-resourceidentifier
            """
            result = self._values.get("resource_identifier")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnStack.UserSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "permission": "permission"},
    )
    class UserSettingProperty:
        def __init__(self, *, action: builtins.str, permission: builtins.str) -> None:
            """
            :param action: ``CfnStack.UserSettingProperty.Action``.
            :param permission: ``CfnStack.UserSettingProperty.Permission``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "action": action,
                "permission": permission,
            }

        @builtins.property
        def action(self) -> builtins.str:
            """``CfnStack.UserSettingProperty.Action``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html#cfn-appstream-stack-usersetting-action
            """
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return result

        @builtins.property
        def permission(self) -> builtins.str:
            """``CfnStack.UserSettingProperty.Permission``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html#cfn-appstream-stack-usersetting-permission
            """
            result = self._values.get("permission")
            assert result is not None, "Required property 'permission' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStackFleetAssociation(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnStackFleetAssociation",
):
    """A CloudFormation ``AWS::AppStream::StackFleetAssociation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html
    :cloudformationResource: AWS::AppStream::StackFleetAssociation
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        fleet_name: builtins.str,
        stack_name: builtins.str,
    ) -> None:
        """Create a new ``AWS::AppStream::StackFleetAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param fleet_name: ``AWS::AppStream::StackFleetAssociation.FleetName``.
        :param stack_name: ``AWS::AppStream::StackFleetAssociation.StackName``.
        """
        props = CfnStackFleetAssociationProps(
            fleet_name=fleet_name, stack_name=stack_name
        )

        jsii.create(CfnStackFleetAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="fleetName")
    def fleet_name(self) -> builtins.str:
        """``AWS::AppStream::StackFleetAssociation.FleetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-fleetname
        """
        return jsii.get(self, "fleetName")

    @fleet_name.setter # type: ignore
    def fleet_name(self, value: builtins.str) -> None:
        jsii.set(self, "fleetName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        """``AWS::AppStream::StackFleetAssociation.StackName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-stackname
        """
        return jsii.get(self, "stackName")

    @stack_name.setter # type: ignore
    def stack_name(self, value: builtins.str) -> None:
        jsii.set(self, "stackName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnStackFleetAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"fleet_name": "fleetName", "stack_name": "stackName"},
)
class CfnStackFleetAssociationProps:
    def __init__(self, *, fleet_name: builtins.str, stack_name: builtins.str) -> None:
        """Properties for defining a ``AWS::AppStream::StackFleetAssociation``.

        :param fleet_name: ``AWS::AppStream::StackFleetAssociation.FleetName``.
        :param stack_name: ``AWS::AppStream::StackFleetAssociation.StackName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "fleet_name": fleet_name,
            "stack_name": stack_name,
        }

    @builtins.property
    def fleet_name(self) -> builtins.str:
        """``AWS::AppStream::StackFleetAssociation.FleetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-fleetname
        """
        result = self._values.get("fleet_name")
        assert result is not None, "Required property 'fleet_name' is missing"
        return result

    @builtins.property
    def stack_name(self) -> builtins.str:
        """``AWS::AppStream::StackFleetAssociation.StackName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-stackname
        """
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackFleetAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_endpoints": "accessEndpoints",
        "application_settings": "applicationSettings",
        "attributes_to_delete": "attributesToDelete",
        "delete_storage_connectors": "deleteStorageConnectors",
        "description": "description",
        "display_name": "displayName",
        "embed_host_domains": "embedHostDomains",
        "feedback_url": "feedbackUrl",
        "name": "name",
        "redirect_url": "redirectUrl",
        "storage_connectors": "storageConnectors",
        "tags": "tags",
        "user_settings": "userSettings",
    },
)
class CfnStackProps:
    def __init__(
        self,
        *,
        access_endpoints: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStack.AccessEndpointProperty]]]] = None,
        application_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStack.ApplicationSettingsProperty]] = None,
        attributes_to_delete: typing.Optional[typing.List[builtins.str]] = None,
        delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        embed_host_domains: typing.Optional[typing.List[builtins.str]] = None,
        feedback_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        storage_connectors: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStack.StorageConnectorProperty]]]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        user_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStack.UserSettingProperty]]]] = None,
    ) -> None:
        """Properties for defining a ``AWS::AppStream::Stack``.

        :param access_endpoints: ``AWS::AppStream::Stack.AccessEndpoints``.
        :param application_settings: ``AWS::AppStream::Stack.ApplicationSettings``.
        :param attributes_to_delete: ``AWS::AppStream::Stack.AttributesToDelete``.
        :param delete_storage_connectors: ``AWS::AppStream::Stack.DeleteStorageConnectors``.
        :param description: ``AWS::AppStream::Stack.Description``.
        :param display_name: ``AWS::AppStream::Stack.DisplayName``.
        :param embed_host_domains: ``AWS::AppStream::Stack.EmbedHostDomains``.
        :param feedback_url: ``AWS::AppStream::Stack.FeedbackURL``.
        :param name: ``AWS::AppStream::Stack.Name``.
        :param redirect_url: ``AWS::AppStream::Stack.RedirectURL``.
        :param storage_connectors: ``AWS::AppStream::Stack.StorageConnectors``.
        :param tags: ``AWS::AppStream::Stack.Tags``.
        :param user_settings: ``AWS::AppStream::Stack.UserSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if access_endpoints is not None:
            self._values["access_endpoints"] = access_endpoints
        if application_settings is not None:
            self._values["application_settings"] = application_settings
        if attributes_to_delete is not None:
            self._values["attributes_to_delete"] = attributes_to_delete
        if delete_storage_connectors is not None:
            self._values["delete_storage_connectors"] = delete_storage_connectors
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if embed_host_domains is not None:
            self._values["embed_host_domains"] = embed_host_domains
        if feedback_url is not None:
            self._values["feedback_url"] = feedback_url
        if name is not None:
            self._values["name"] = name
        if redirect_url is not None:
            self._values["redirect_url"] = redirect_url
        if storage_connectors is not None:
            self._values["storage_connectors"] = storage_connectors
        if tags is not None:
            self._values["tags"] = tags
        if user_settings is not None:
            self._values["user_settings"] = user_settings

    @builtins.property
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStack.AccessEndpointProperty]]]]:
        """``AWS::AppStream::Stack.AccessEndpoints``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-accessendpoints
        """
        result = self._values.get("access_endpoints")
        return result

    @builtins.property
    def application_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStack.ApplicationSettingsProperty]]:
        """``AWS::AppStream::Stack.ApplicationSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-applicationsettings
        """
        result = self._values.get("application_settings")
        return result

    @builtins.property
    def attributes_to_delete(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AppStream::Stack.AttributesToDelete``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-attributestodelete
        """
        result = self._values.get("attributes_to_delete")
        return result

    @builtins.property
    def delete_storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AppStream::Stack.DeleteStorageConnectors``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-deletestorageconnectors
        """
        result = self._values.get("delete_storage_connectors")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Stack.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Stack.DisplayName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-displayname
        """
        result = self._values.get("display_name")
        return result

    @builtins.property
    def embed_host_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::AppStream::Stack.EmbedHostDomains``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-embedhostdomains
        """
        result = self._values.get("embed_host_domains")
        return result

    @builtins.property
    def feedback_url(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Stack.FeedbackURL``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-feedbackurl
        """
        result = self._values.get("feedback_url")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Stack.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def redirect_url(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::Stack.RedirectURL``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-redirecturl
        """
        result = self._values.get("redirect_url")
        return result

    @builtins.property
    def storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStack.StorageConnectorProperty]]]]:
        """``AWS::AppStream::Stack.StorageConnectors``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-storageconnectors
        """
        result = self._values.get("storage_connectors")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::AppStream::Stack.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def user_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStack.UserSettingProperty]]]]:
        """``AWS::AppStream::Stack.UserSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-usersettings
        """
        result = self._values.get("user_settings")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStackUserAssociation(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnStackUserAssociation",
):
    """A CloudFormation ``AWS::AppStream::StackUserAssociation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html
    :cloudformationResource: AWS::AppStream::StackUserAssociation
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        authentication_type: builtins.str,
        stack_name: builtins.str,
        user_name: builtins.str,
        send_email_notification: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
    ) -> None:
        """Create a new ``AWS::AppStream::StackUserAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param authentication_type: ``AWS::AppStream::StackUserAssociation.AuthenticationType``.
        :param stack_name: ``AWS::AppStream::StackUserAssociation.StackName``.
        :param user_name: ``AWS::AppStream::StackUserAssociation.UserName``.
        :param send_email_notification: ``AWS::AppStream::StackUserAssociation.SendEmailNotification``.
        """
        props = CfnStackUserAssociationProps(
            authentication_type=authentication_type,
            stack_name=stack_name,
            user_name=user_name,
            send_email_notification=send_email_notification,
        )

        jsii.create(CfnStackUserAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        """``AWS::AppStream::StackUserAssociation.AuthenticationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-authenticationtype
        """
        return jsii.get(self, "authenticationType")

    @authentication_type.setter # type: ignore
    def authentication_type(self, value: builtins.str) -> None:
        jsii.set(self, "authenticationType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        """``AWS::AppStream::StackUserAssociation.StackName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-stackname
        """
        return jsii.get(self, "stackName")

    @stack_name.setter # type: ignore
    def stack_name(self, value: builtins.str) -> None:
        jsii.set(self, "stackName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        """``AWS::AppStream::StackUserAssociation.UserName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-username
        """
        return jsii.get(self, "userName")

    @user_name.setter # type: ignore
    def user_name(self, value: builtins.str) -> None:
        jsii.set(self, "userName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sendEmailNotification")
    def send_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AppStream::StackUserAssociation.SendEmailNotification``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-sendemailnotification
        """
        return jsii.get(self, "sendEmailNotification")

    @send_email_notification.setter # type: ignore
    def send_email_notification(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "sendEmailNotification", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnStackUserAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_type": "authenticationType",
        "stack_name": "stackName",
        "user_name": "userName",
        "send_email_notification": "sendEmailNotification",
    },
)
class CfnStackUserAssociationProps:
    def __init__(
        self,
        *,
        authentication_type: builtins.str,
        stack_name: builtins.str,
        user_name: builtins.str,
        send_email_notification: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
    ) -> None:
        """Properties for defining a ``AWS::AppStream::StackUserAssociation``.

        :param authentication_type: ``AWS::AppStream::StackUserAssociation.AuthenticationType``.
        :param stack_name: ``AWS::AppStream::StackUserAssociation.StackName``.
        :param user_name: ``AWS::AppStream::StackUserAssociation.UserName``.
        :param send_email_notification: ``AWS::AppStream::StackUserAssociation.SendEmailNotification``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "authentication_type": authentication_type,
            "stack_name": stack_name,
            "user_name": user_name,
        }
        if send_email_notification is not None:
            self._values["send_email_notification"] = send_email_notification

    @builtins.property
    def authentication_type(self) -> builtins.str:
        """``AWS::AppStream::StackUserAssociation.AuthenticationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-authenticationtype
        """
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return result

    @builtins.property
    def stack_name(self) -> builtins.str:
        """``AWS::AppStream::StackUserAssociation.StackName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-stackname
        """
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return result

    @builtins.property
    def user_name(self) -> builtins.str:
        """``AWS::AppStream::StackUserAssociation.UserName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-username
        """
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return result

    @builtins.property
    def send_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::AppStream::StackUserAssociation.SendEmailNotification``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-sendemailnotification
        """
        result = self._values.get("send_email_notification")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackUserAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUser(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnUser",
):
    """A CloudFormation ``AWS::AppStream::User``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html
    :cloudformationResource: AWS::AppStream::User
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        authentication_type: builtins.str,
        user_name: builtins.str,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        message_action: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::AppStream::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param authentication_type: ``AWS::AppStream::User.AuthenticationType``.
        :param user_name: ``AWS::AppStream::User.UserName``.
        :param first_name: ``AWS::AppStream::User.FirstName``.
        :param last_name: ``AWS::AppStream::User.LastName``.
        :param message_action: ``AWS::AppStream::User.MessageAction``.
        """
        props = CfnUserProps(
            authentication_type=authentication_type,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            message_action=message_action,
        )

        jsii.create(CfnUser, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        """``AWS::AppStream::User.AuthenticationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-authenticationtype
        """
        return jsii.get(self, "authenticationType")

    @authentication_type.setter # type: ignore
    def authentication_type(self, value: builtins.str) -> None:
        jsii.set(self, "authenticationType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        """``AWS::AppStream::User.UserName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-username
        """
        return jsii.get(self, "userName")

    @user_name.setter # type: ignore
    def user_name(self, value: builtins.str) -> None:
        jsii.set(self, "userName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::User.FirstName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-firstname
        """
        return jsii.get(self, "firstName")

    @first_name.setter # type: ignore
    def first_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "firstName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::User.LastName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-lastname
        """
        return jsii.get(self, "lastName")

    @last_name.setter # type: ignore
    def last_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "lastName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="messageAction")
    def message_action(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::User.MessageAction``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-messageaction
        """
        return jsii.get(self, "messageAction")

    @message_action.setter # type: ignore
    def message_action(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "messageAction", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_type": "authenticationType",
        "user_name": "userName",
        "first_name": "firstName",
        "last_name": "lastName",
        "message_action": "messageAction",
    },
)
class CfnUserProps:
    def __init__(
        self,
        *,
        authentication_type: builtins.str,
        user_name: builtins.str,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        message_action: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::AppStream::User``.

        :param authentication_type: ``AWS::AppStream::User.AuthenticationType``.
        :param user_name: ``AWS::AppStream::User.UserName``.
        :param first_name: ``AWS::AppStream::User.FirstName``.
        :param last_name: ``AWS::AppStream::User.LastName``.
        :param message_action: ``AWS::AppStream::User.MessageAction``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "authentication_type": authentication_type,
            "user_name": user_name,
        }
        if first_name is not None:
            self._values["first_name"] = first_name
        if last_name is not None:
            self._values["last_name"] = last_name
        if message_action is not None:
            self._values["message_action"] = message_action

    @builtins.property
    def authentication_type(self) -> builtins.str:
        """``AWS::AppStream::User.AuthenticationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-authenticationtype
        """
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return result

    @builtins.property
    def user_name(self) -> builtins.str:
        """``AWS::AppStream::User.UserName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-username
        """
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return result

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::User.FirstName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-firstname
        """
        result = self._values.get("first_name")
        return result

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::User.LastName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-lastname
        """
        result = self._values.get("last_name")
        return result

    @builtins.property
    def message_action(self) -> typing.Optional[builtins.str]:
        """``AWS::AppStream::User.MessageAction``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-messageaction
        """
        result = self._values.get("message_action")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDirectoryConfig",
    "CfnDirectoryConfigProps",
    "CfnFleet",
    "CfnFleetProps",
    "CfnImageBuilder",
    "CfnImageBuilderProps",
    "CfnStack",
    "CfnStackFleetAssociation",
    "CfnStackFleetAssociationProps",
    "CfnStackProps",
    "CfnStackUserAssociation",
    "CfnStackUserAssociationProps",
    "CfnUser",
    "CfnUserProps",
]

publication.publish()
