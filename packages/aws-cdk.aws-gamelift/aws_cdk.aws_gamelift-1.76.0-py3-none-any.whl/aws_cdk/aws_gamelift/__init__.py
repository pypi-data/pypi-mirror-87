"""
## Amazon GameLift Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
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
class CfnAlias(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-gamelift.CfnAlias",
):
    """A CloudFormation ``AWS::GameLift::Alias``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html
    :cloudformationResource: AWS::GameLift::Alias
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        routing_strategy: typing.Union[aws_cdk.core.IResolvable, "CfnAlias.RoutingStrategyProperty"],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::GameLift::Alias``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::GameLift::Alias.Name``.
        :param routing_strategy: ``AWS::GameLift::Alias.RoutingStrategy``.
        :param description: ``AWS::GameLift::Alias.Description``.
        """
        props = CfnAliasProps(
            name=name, routing_strategy=routing_strategy, description=description
        )

        jsii.create(CfnAlias, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrAliasId")
    def attr_alias_id(self) -> builtins.str:
        """
        :cloudformationAttribute: AliasId
        """
        return jsii.get(self, "attrAliasId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::GameLift::Alias.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="routingStrategy")
    def routing_strategy(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnAlias.RoutingStrategyProperty"]:
        """``AWS::GameLift::Alias.RoutingStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-routingstrategy
        """
        return jsii.get(self, "routingStrategy")

    @routing_strategy.setter # type: ignore
    def routing_strategy(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnAlias.RoutingStrategyProperty"],
    ) -> None:
        jsii.set(self, "routingStrategy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Alias.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnAlias.RoutingStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"fleet_id": "fleetId", "message": "message", "type": "type"},
    )
    class RoutingStrategyProperty:
        def __init__(
            self,
            *,
            fleet_id: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param fleet_id: ``CfnAlias.RoutingStrategyProperty.FleetId``.
            :param message: ``CfnAlias.RoutingStrategyProperty.Message``.
            :param type: ``CfnAlias.RoutingStrategyProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if fleet_id is not None:
                self._values["fleet_id"] = fleet_id
            if message is not None:
                self._values["message"] = message
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def fleet_id(self) -> typing.Optional[builtins.str]:
            """``CfnAlias.RoutingStrategyProperty.FleetId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html#cfn-gamelift-alias-routingstrategy-fleetid
            """
            result = self._values.get("fleet_id")
            return result

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            """``CfnAlias.RoutingStrategyProperty.Message``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html#cfn-gamelift-alias-routingstrategy-message
            """
            result = self._values.get("message")
            return result

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            """``CfnAlias.RoutingStrategyProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html#cfn-gamelift-alias-routingstrategy-type
            """
            result = self._values.get("type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoutingStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-gamelift.CfnAliasProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "routing_strategy": "routingStrategy",
        "description": "description",
    },
)
class CfnAliasProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        routing_strategy: typing.Union[aws_cdk.core.IResolvable, CfnAlias.RoutingStrategyProperty],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::GameLift::Alias``.

        :param name: ``AWS::GameLift::Alias.Name``.
        :param routing_strategy: ``AWS::GameLift::Alias.RoutingStrategy``.
        :param description: ``AWS::GameLift::Alias.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "routing_strategy": routing_strategy,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::GameLift::Alias.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def routing_strategy(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnAlias.RoutingStrategyProperty]:
        """``AWS::GameLift::Alias.RoutingStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-routingstrategy
        """
        result = self._values.get("routing_strategy")
        assert result is not None, "Required property 'routing_strategy' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Alias.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-description
        """
        result = self._values.get("description")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnBuild(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-gamelift.CfnBuild",
):
    """A CloudFormation ``AWS::GameLift::Build``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html
    :cloudformationResource: AWS::GameLift::Build
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: typing.Optional[builtins.str] = None,
        operating_system: typing.Optional[builtins.str] = None,
        storage_location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnBuild.S3LocationProperty"]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::GameLift::Build``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::GameLift::Build.Name``.
        :param operating_system: ``AWS::GameLift::Build.OperatingSystem``.
        :param storage_location: ``AWS::GameLift::Build.StorageLocation``.
        :param version: ``AWS::GameLift::Build.Version``.
        """
        props = CfnBuildProps(
            name=name,
            operating_system=operating_system,
            storage_location=storage_location,
            version=version,
        )

        jsii.create(CfnBuild, self, [scope, id, props])

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
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Build.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Build.OperatingSystem``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-operatingsystem
        """
        return jsii.get(self, "operatingSystem")

    @operating_system.setter # type: ignore
    def operating_system(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "operatingSystem", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="storageLocation")
    def storage_location(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnBuild.S3LocationProperty"]]:
        """``AWS::GameLift::Build.StorageLocation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-storagelocation
        """
        return jsii.get(self, "storageLocation")

    @storage_location.setter # type: ignore
    def storage_location(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnBuild.S3LocationProperty"]],
    ) -> None:
        jsii.set(self, "storageLocation", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Build.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-version
        """
        return jsii.get(self, "version")

    @version.setter # type: ignore
    def version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnBuild.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key": "key",
            "role_arn": "roleArn",
            "object_version": "objectVersion",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            role_arn: builtins.str,
            object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket: ``CfnBuild.S3LocationProperty.Bucket``.
            :param key: ``CfnBuild.S3LocationProperty.Key``.
            :param role_arn: ``CfnBuild.S3LocationProperty.RoleArn``.
            :param object_version: ``CfnBuild.S3LocationProperty.ObjectVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
                "key": key,
                "role_arn": role_arn,
            }
            if object_version is not None:
                self._values["object_version"] = object_version

        @builtins.property
        def bucket(self) -> builtins.str:
            """``CfnBuild.S3LocationProperty.Bucket``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html#cfn-gamelift-build-storage-bucket
            """
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return result

        @builtins.property
        def key(self) -> builtins.str:
            """``CfnBuild.S3LocationProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html#cfn-gamelift-build-storage-key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def role_arn(self) -> builtins.str:
            """``CfnBuild.S3LocationProperty.RoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html#cfn-gamelift-build-storage-rolearn
            """
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return result

        @builtins.property
        def object_version(self) -> typing.Optional[builtins.str]:
            """``CfnBuild.S3LocationProperty.ObjectVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html#cfn-gamelift-build-object-verison
            """
            result = self._values.get("object_version")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-gamelift.CfnBuildProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "operating_system": "operatingSystem",
        "storage_location": "storageLocation",
        "version": "version",
    },
)
class CfnBuildProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        operating_system: typing.Optional[builtins.str] = None,
        storage_location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnBuild.S3LocationProperty]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::GameLift::Build``.

        :param name: ``AWS::GameLift::Build.Name``.
        :param operating_system: ``AWS::GameLift::Build.OperatingSystem``.
        :param storage_location: ``AWS::GameLift::Build.StorageLocation``.
        :param version: ``AWS::GameLift::Build.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if operating_system is not None:
            self._values["operating_system"] = operating_system
        if storage_location is not None:
            self._values["storage_location"] = storage_location
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Build.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Build.OperatingSystem``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-operatingsystem
        """
        result = self._values.get("operating_system")
        return result

    @builtins.property
    def storage_location(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnBuild.S3LocationProperty]]:
        """``AWS::GameLift::Build.StorageLocation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-storagelocation
        """
        result = self._values.get("storage_location")
        return result

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Build.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-version
        """
        result = self._values.get("version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBuildProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnFleet(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-gamelift.CfnFleet",
):
    """A CloudFormation ``AWS::GameLift::Fleet``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html
    :cloudformationResource: AWS::GameLift::Fleet
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        ec2_instance_type: builtins.str,
        name: builtins.str,
        build_id: typing.Optional[builtins.str] = None,
        certificate_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.CertificateConfigurationProperty"]] = None,
        description: typing.Optional[builtins.str] = None,
        desired_ec2_instances: typing.Optional[jsii.Number] = None,
        ec2_inbound_permissions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.IpPermissionProperty"]]]] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        instance_role_arn: typing.Optional[builtins.str] = None,
        log_paths: typing.Optional[typing.List[builtins.str]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        metric_groups: typing.Optional[typing.List[builtins.str]] = None,
        min_size: typing.Optional[jsii.Number] = None,
        new_game_session_protection_policy: typing.Optional[builtins.str] = None,
        peer_vpc_aws_account_id: typing.Optional[builtins.str] = None,
        peer_vpc_id: typing.Optional[builtins.str] = None,
        resource_creation_limit_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.ResourceCreationLimitPolicyProperty"]] = None,
        runtime_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.RuntimeConfigurationProperty"]] = None,
        script_id: typing.Optional[builtins.str] = None,
        server_launch_parameters: typing.Optional[builtins.str] = None,
        server_launch_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::GameLift::Fleet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param ec2_instance_type: ``AWS::GameLift::Fleet.EC2InstanceType``.
        :param name: ``AWS::GameLift::Fleet.Name``.
        :param build_id: ``AWS::GameLift::Fleet.BuildId``.
        :param certificate_configuration: ``AWS::GameLift::Fleet.CertificateConfiguration``.
        :param description: ``AWS::GameLift::Fleet.Description``.
        :param desired_ec2_instances: ``AWS::GameLift::Fleet.DesiredEC2Instances``.
        :param ec2_inbound_permissions: ``AWS::GameLift::Fleet.EC2InboundPermissions``.
        :param fleet_type: ``AWS::GameLift::Fleet.FleetType``.
        :param instance_role_arn: ``AWS::GameLift::Fleet.InstanceRoleARN``.
        :param log_paths: ``AWS::GameLift::Fleet.LogPaths``.
        :param max_size: ``AWS::GameLift::Fleet.MaxSize``.
        :param metric_groups: ``AWS::GameLift::Fleet.MetricGroups``.
        :param min_size: ``AWS::GameLift::Fleet.MinSize``.
        :param new_game_session_protection_policy: ``AWS::GameLift::Fleet.NewGameSessionProtectionPolicy``.
        :param peer_vpc_aws_account_id: ``AWS::GameLift::Fleet.PeerVpcAwsAccountId``.
        :param peer_vpc_id: ``AWS::GameLift::Fleet.PeerVpcId``.
        :param resource_creation_limit_policy: ``AWS::GameLift::Fleet.ResourceCreationLimitPolicy``.
        :param runtime_configuration: ``AWS::GameLift::Fleet.RuntimeConfiguration``.
        :param script_id: ``AWS::GameLift::Fleet.ScriptId``.
        :param server_launch_parameters: ``AWS::GameLift::Fleet.ServerLaunchParameters``.
        :param server_launch_path: ``AWS::GameLift::Fleet.ServerLaunchPath``.
        """
        props = CfnFleetProps(
            ec2_instance_type=ec2_instance_type,
            name=name,
            build_id=build_id,
            certificate_configuration=certificate_configuration,
            description=description,
            desired_ec2_instances=desired_ec2_instances,
            ec2_inbound_permissions=ec2_inbound_permissions,
            fleet_type=fleet_type,
            instance_role_arn=instance_role_arn,
            log_paths=log_paths,
            max_size=max_size,
            metric_groups=metric_groups,
            min_size=min_size,
            new_game_session_protection_policy=new_game_session_protection_policy,
            peer_vpc_aws_account_id=peer_vpc_aws_account_id,
            peer_vpc_id=peer_vpc_id,
            resource_creation_limit_policy=resource_creation_limit_policy,
            runtime_configuration=runtime_configuration,
            script_id=script_id,
            server_launch_parameters=server_launch_parameters,
            server_launch_path=server_launch_path,
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
    @jsii.member(jsii_name="ec2InstanceType")
    def ec2_instance_type(self) -> builtins.str:
        """``AWS::GameLift::Fleet.EC2InstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-ec2instancetype
        """
        return jsii.get(self, "ec2InstanceType")

    @ec2_instance_type.setter # type: ignore
    def ec2_instance_type(self, value: builtins.str) -> None:
        jsii.set(self, "ec2InstanceType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::GameLift::Fleet.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="buildId")
    def build_id(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.BuildId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-buildid
        """
        return jsii.get(self, "buildId")

    @build_id.setter # type: ignore
    def build_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "buildId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateConfiguration")
    def certificate_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.CertificateConfigurationProperty"]]:
        """``AWS::GameLift::Fleet.CertificateConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-certificateconfiguration
        """
        return jsii.get(self, "certificateConfiguration")

    @certificate_configuration.setter # type: ignore
    def certificate_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.CertificateConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "certificateConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="desiredEc2Instances")
    def desired_ec2_instances(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::Fleet.DesiredEC2Instances``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-desiredec2instances
        """
        return jsii.get(self, "desiredEc2Instances")

    @desired_ec2_instances.setter # type: ignore
    def desired_ec2_instances(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "desiredEc2Instances", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ec2InboundPermissions")
    def ec2_inbound_permissions(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.IpPermissionProperty"]]]]:
        """``AWS::GameLift::Fleet.EC2InboundPermissions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-ec2inboundpermissions
        """
        return jsii.get(self, "ec2InboundPermissions")

    @ec2_inbound_permissions.setter # type: ignore
    def ec2_inbound_permissions(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.IpPermissionProperty"]]]],
    ) -> None:
        jsii.set(self, "ec2InboundPermissions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="fleetType")
    def fleet_type(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.FleetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-fleettype
        """
        return jsii.get(self, "fleetType")

    @fleet_type.setter # type: ignore
    def fleet_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "fleetType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceRoleArn")
    def instance_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.InstanceRoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-instancerolearn
        """
        return jsii.get(self, "instanceRoleArn")

    @instance_role_arn.setter # type: ignore
    def instance_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "instanceRoleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="logPaths")
    def log_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::GameLift::Fleet.LogPaths``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-logpaths
        """
        return jsii.get(self, "logPaths")

    @log_paths.setter # type: ignore
    def log_paths(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "logPaths", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxSize")
    def max_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::Fleet.MaxSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-maxsize
        """
        return jsii.get(self, "maxSize")

    @max_size.setter # type: ignore
    def max_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxSize", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="metricGroups")
    def metric_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::GameLift::Fleet.MetricGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-metricgroups
        """
        return jsii.get(self, "metricGroups")

    @metric_groups.setter # type: ignore
    def metric_groups(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "metricGroups", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="minSize")
    def min_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::Fleet.MinSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-minsize
        """
        return jsii.get(self, "minSize")

    @min_size.setter # type: ignore
    def min_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "minSize", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="newGameSessionProtectionPolicy")
    def new_game_session_protection_policy(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.NewGameSessionProtectionPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-newgamesessionprotectionpolicy
        """
        return jsii.get(self, "newGameSessionProtectionPolicy")

    @new_game_session_protection_policy.setter # type: ignore
    def new_game_session_protection_policy(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "newGameSessionProtectionPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="peerVpcAwsAccountId")
    def peer_vpc_aws_account_id(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.PeerVpcAwsAccountId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-peervpcawsaccountid
        """
        return jsii.get(self, "peerVpcAwsAccountId")

    @peer_vpc_aws_account_id.setter # type: ignore
    def peer_vpc_aws_account_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "peerVpcAwsAccountId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="peerVpcId")
    def peer_vpc_id(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.PeerVpcId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-peervpcid
        """
        return jsii.get(self, "peerVpcId")

    @peer_vpc_id.setter # type: ignore
    def peer_vpc_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "peerVpcId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resourceCreationLimitPolicy")
    def resource_creation_limit_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.ResourceCreationLimitPolicyProperty"]]:
        """``AWS::GameLift::Fleet.ResourceCreationLimitPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-resourcecreationlimitpolicy
        """
        return jsii.get(self, "resourceCreationLimitPolicy")

    @resource_creation_limit_policy.setter # type: ignore
    def resource_creation_limit_policy(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.ResourceCreationLimitPolicyProperty"]],
    ) -> None:
        jsii.set(self, "resourceCreationLimitPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="runtimeConfiguration")
    def runtime_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.RuntimeConfigurationProperty"]]:
        """``AWS::GameLift::Fleet.RuntimeConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-runtimeconfiguration
        """
        return jsii.get(self, "runtimeConfiguration")

    @runtime_configuration.setter # type: ignore
    def runtime_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.RuntimeConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "runtimeConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scriptId")
    def script_id(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.ScriptId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-scriptid
        """
        return jsii.get(self, "scriptId")

    @script_id.setter # type: ignore
    def script_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "scriptId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serverLaunchParameters")
    def server_launch_parameters(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.ServerLaunchParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-serverlaunchparameters
        """
        return jsii.get(self, "serverLaunchParameters")

    @server_launch_parameters.setter # type: ignore
    def server_launch_parameters(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "serverLaunchParameters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serverLaunchPath")
    def server_launch_path(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.ServerLaunchPath``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-serverlaunchpath
        """
        return jsii.get(self, "serverLaunchPath")

    @server_launch_path.setter # type: ignore
    def server_launch_path(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "serverLaunchPath", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnFleet.CertificateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"certificate_type": "certificateType"},
    )
    class CertificateConfigurationProperty:
        def __init__(self, *, certificate_type: builtins.str) -> None:
            """
            :param certificate_type: ``CfnFleet.CertificateConfigurationProperty.CertificateType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-certificateconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "certificate_type": certificate_type,
            }

        @builtins.property
        def certificate_type(self) -> builtins.str:
            """``CfnFleet.CertificateConfigurationProperty.CertificateType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-certificateconfiguration.html#cfn-gamelift-fleet-certificateconfiguration-certificatetype
            """
            result = self._values.get("certificate_type")
            assert result is not None, "Required property 'certificate_type' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnFleet.IpPermissionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "from_port": "fromPort",
            "ip_range": "ipRange",
            "protocol": "protocol",
            "to_port": "toPort",
        },
    )
    class IpPermissionProperty:
        def __init__(
            self,
            *,
            from_port: jsii.Number,
            ip_range: builtins.str,
            protocol: builtins.str,
            to_port: jsii.Number,
        ) -> None:
            """
            :param from_port: ``CfnFleet.IpPermissionProperty.FromPort``.
            :param ip_range: ``CfnFleet.IpPermissionProperty.IpRange``.
            :param protocol: ``CfnFleet.IpPermissionProperty.Protocol``.
            :param to_port: ``CfnFleet.IpPermissionProperty.ToPort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ec2inboundpermission.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "from_port": from_port,
                "ip_range": ip_range,
                "protocol": protocol,
                "to_port": to_port,
            }

        @builtins.property
        def from_port(self) -> jsii.Number:
            """``CfnFleet.IpPermissionProperty.FromPort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ec2inboundpermission.html#cfn-gamelift-fleet-ec2inboundpermissions-fromport
            """
            result = self._values.get("from_port")
            assert result is not None, "Required property 'from_port' is missing"
            return result

        @builtins.property
        def ip_range(self) -> builtins.str:
            """``CfnFleet.IpPermissionProperty.IpRange``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ec2inboundpermission.html#cfn-gamelift-fleet-ec2inboundpermissions-iprange
            """
            result = self._values.get("ip_range")
            assert result is not None, "Required property 'ip_range' is missing"
            return result

        @builtins.property
        def protocol(self) -> builtins.str:
            """``CfnFleet.IpPermissionProperty.Protocol``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ec2inboundpermission.html#cfn-gamelift-fleet-ec2inboundpermissions-protocol
            """
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return result

        @builtins.property
        def to_port(self) -> jsii.Number:
            """``CfnFleet.IpPermissionProperty.ToPort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ec2inboundpermission.html#cfn-gamelift-fleet-ec2inboundpermissions-toport
            """
            result = self._values.get("to_port")
            assert result is not None, "Required property 'to_port' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IpPermissionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnFleet.ResourceCreationLimitPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "new_game_sessions_per_creator": "newGameSessionsPerCreator",
            "policy_period_in_minutes": "policyPeriodInMinutes",
        },
    )
    class ResourceCreationLimitPolicyProperty:
        def __init__(
            self,
            *,
            new_game_sessions_per_creator: typing.Optional[jsii.Number] = None,
            policy_period_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param new_game_sessions_per_creator: ``CfnFleet.ResourceCreationLimitPolicyProperty.NewGameSessionsPerCreator``.
            :param policy_period_in_minutes: ``CfnFleet.ResourceCreationLimitPolicyProperty.PolicyPeriodInMinutes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-resourcecreationlimitpolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if new_game_sessions_per_creator is not None:
                self._values["new_game_sessions_per_creator"] = new_game_sessions_per_creator
            if policy_period_in_minutes is not None:
                self._values["policy_period_in_minutes"] = policy_period_in_minutes

        @builtins.property
        def new_game_sessions_per_creator(self) -> typing.Optional[jsii.Number]:
            """``CfnFleet.ResourceCreationLimitPolicyProperty.NewGameSessionsPerCreator``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-resourcecreationlimitpolicy.html#cfn-gamelift-fleet-resourcecreationlimitpolicy-newgamesessionspercreator
            """
            result = self._values.get("new_game_sessions_per_creator")
            return result

        @builtins.property
        def policy_period_in_minutes(self) -> typing.Optional[jsii.Number]:
            """``CfnFleet.ResourceCreationLimitPolicyProperty.PolicyPeriodInMinutes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-resourcecreationlimitpolicy.html#cfn-gamelift-fleet-resourcecreationlimitpolicy-policyperiodinminutes
            """
            result = self._values.get("policy_period_in_minutes")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceCreationLimitPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnFleet.RuntimeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "game_session_activation_timeout_seconds": "gameSessionActivationTimeoutSeconds",
            "max_concurrent_game_session_activations": "maxConcurrentGameSessionActivations",
            "server_processes": "serverProcesses",
        },
    )
    class RuntimeConfigurationProperty:
        def __init__(
            self,
            *,
            game_session_activation_timeout_seconds: typing.Optional[jsii.Number] = None,
            max_concurrent_game_session_activations: typing.Optional[jsii.Number] = None,
            server_processes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.ServerProcessProperty"]]]] = None,
        ) -> None:
            """
            :param game_session_activation_timeout_seconds: ``CfnFleet.RuntimeConfigurationProperty.GameSessionActivationTimeoutSeconds``.
            :param max_concurrent_game_session_activations: ``CfnFleet.RuntimeConfigurationProperty.MaxConcurrentGameSessionActivations``.
            :param server_processes: ``CfnFleet.RuntimeConfigurationProperty.ServerProcesses``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-runtimeconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if game_session_activation_timeout_seconds is not None:
                self._values["game_session_activation_timeout_seconds"] = game_session_activation_timeout_seconds
            if max_concurrent_game_session_activations is not None:
                self._values["max_concurrent_game_session_activations"] = max_concurrent_game_session_activations
            if server_processes is not None:
                self._values["server_processes"] = server_processes

        @builtins.property
        def game_session_activation_timeout_seconds(
            self,
        ) -> typing.Optional[jsii.Number]:
            """``CfnFleet.RuntimeConfigurationProperty.GameSessionActivationTimeoutSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-runtimeconfiguration.html#cfn-gamelift-fleet-runtimeconfiguration-gamesessionactivationtimeoutseconds
            """
            result = self._values.get("game_session_activation_timeout_seconds")
            return result

        @builtins.property
        def max_concurrent_game_session_activations(
            self,
        ) -> typing.Optional[jsii.Number]:
            """``CfnFleet.RuntimeConfigurationProperty.MaxConcurrentGameSessionActivations``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-runtimeconfiguration.html#cfn-gamelift-fleet-runtimeconfiguration-maxconcurrentgamesessionactivations
            """
            result = self._values.get("max_concurrent_game_session_activations")
            return result

        @builtins.property
        def server_processes(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnFleet.ServerProcessProperty"]]]]:
            """``CfnFleet.RuntimeConfigurationProperty.ServerProcesses``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-runtimeconfiguration.html#cfn-gamelift-fleet-runtimeconfiguration-serverprocesses
            """
            result = self._values.get("server_processes")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuntimeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnFleet.ServerProcessProperty",
        jsii_struct_bases=[],
        name_mapping={
            "concurrent_executions": "concurrentExecutions",
            "launch_path": "launchPath",
            "parameters": "parameters",
        },
    )
    class ServerProcessProperty:
        def __init__(
            self,
            *,
            concurrent_executions: jsii.Number,
            launch_path: builtins.str,
            parameters: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param concurrent_executions: ``CfnFleet.ServerProcessProperty.ConcurrentExecutions``.
            :param launch_path: ``CfnFleet.ServerProcessProperty.LaunchPath``.
            :param parameters: ``CfnFleet.ServerProcessProperty.Parameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-serverprocess.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "concurrent_executions": concurrent_executions,
                "launch_path": launch_path,
            }
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def concurrent_executions(self) -> jsii.Number:
            """``CfnFleet.ServerProcessProperty.ConcurrentExecutions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-serverprocess.html#cfn-gamelift-fleet-serverprocess-concurrentexecutions
            """
            result = self._values.get("concurrent_executions")
            assert result is not None, "Required property 'concurrent_executions' is missing"
            return result

        @builtins.property
        def launch_path(self) -> builtins.str:
            """``CfnFleet.ServerProcessProperty.LaunchPath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-serverprocess.html#cfn-gamelift-fleet-serverprocess-launchpath
            """
            result = self._values.get("launch_path")
            assert result is not None, "Required property 'launch_path' is missing"
            return result

        @builtins.property
        def parameters(self) -> typing.Optional[builtins.str]:
            """``CfnFleet.ServerProcessProperty.Parameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-serverprocess.html#cfn-gamelift-fleet-serverprocess-parameters
            """
            result = self._values.get("parameters")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerProcessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-gamelift.CfnFleetProps",
    jsii_struct_bases=[],
    name_mapping={
        "ec2_instance_type": "ec2InstanceType",
        "name": "name",
        "build_id": "buildId",
        "certificate_configuration": "certificateConfiguration",
        "description": "description",
        "desired_ec2_instances": "desiredEc2Instances",
        "ec2_inbound_permissions": "ec2InboundPermissions",
        "fleet_type": "fleetType",
        "instance_role_arn": "instanceRoleArn",
        "log_paths": "logPaths",
        "max_size": "maxSize",
        "metric_groups": "metricGroups",
        "min_size": "minSize",
        "new_game_session_protection_policy": "newGameSessionProtectionPolicy",
        "peer_vpc_aws_account_id": "peerVpcAwsAccountId",
        "peer_vpc_id": "peerVpcId",
        "resource_creation_limit_policy": "resourceCreationLimitPolicy",
        "runtime_configuration": "runtimeConfiguration",
        "script_id": "scriptId",
        "server_launch_parameters": "serverLaunchParameters",
        "server_launch_path": "serverLaunchPath",
    },
)
class CfnFleetProps:
    def __init__(
        self,
        *,
        ec2_instance_type: builtins.str,
        name: builtins.str,
        build_id: typing.Optional[builtins.str] = None,
        certificate_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFleet.CertificateConfigurationProperty]] = None,
        description: typing.Optional[builtins.str] = None,
        desired_ec2_instances: typing.Optional[jsii.Number] = None,
        ec2_inbound_permissions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnFleet.IpPermissionProperty]]]] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        instance_role_arn: typing.Optional[builtins.str] = None,
        log_paths: typing.Optional[typing.List[builtins.str]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        metric_groups: typing.Optional[typing.List[builtins.str]] = None,
        min_size: typing.Optional[jsii.Number] = None,
        new_game_session_protection_policy: typing.Optional[builtins.str] = None,
        peer_vpc_aws_account_id: typing.Optional[builtins.str] = None,
        peer_vpc_id: typing.Optional[builtins.str] = None,
        resource_creation_limit_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFleet.ResourceCreationLimitPolicyProperty]] = None,
        runtime_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFleet.RuntimeConfigurationProperty]] = None,
        script_id: typing.Optional[builtins.str] = None,
        server_launch_parameters: typing.Optional[builtins.str] = None,
        server_launch_path: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::GameLift::Fleet``.

        :param ec2_instance_type: ``AWS::GameLift::Fleet.EC2InstanceType``.
        :param name: ``AWS::GameLift::Fleet.Name``.
        :param build_id: ``AWS::GameLift::Fleet.BuildId``.
        :param certificate_configuration: ``AWS::GameLift::Fleet.CertificateConfiguration``.
        :param description: ``AWS::GameLift::Fleet.Description``.
        :param desired_ec2_instances: ``AWS::GameLift::Fleet.DesiredEC2Instances``.
        :param ec2_inbound_permissions: ``AWS::GameLift::Fleet.EC2InboundPermissions``.
        :param fleet_type: ``AWS::GameLift::Fleet.FleetType``.
        :param instance_role_arn: ``AWS::GameLift::Fleet.InstanceRoleARN``.
        :param log_paths: ``AWS::GameLift::Fleet.LogPaths``.
        :param max_size: ``AWS::GameLift::Fleet.MaxSize``.
        :param metric_groups: ``AWS::GameLift::Fleet.MetricGroups``.
        :param min_size: ``AWS::GameLift::Fleet.MinSize``.
        :param new_game_session_protection_policy: ``AWS::GameLift::Fleet.NewGameSessionProtectionPolicy``.
        :param peer_vpc_aws_account_id: ``AWS::GameLift::Fleet.PeerVpcAwsAccountId``.
        :param peer_vpc_id: ``AWS::GameLift::Fleet.PeerVpcId``.
        :param resource_creation_limit_policy: ``AWS::GameLift::Fleet.ResourceCreationLimitPolicy``.
        :param runtime_configuration: ``AWS::GameLift::Fleet.RuntimeConfiguration``.
        :param script_id: ``AWS::GameLift::Fleet.ScriptId``.
        :param server_launch_parameters: ``AWS::GameLift::Fleet.ServerLaunchParameters``.
        :param server_launch_path: ``AWS::GameLift::Fleet.ServerLaunchPath``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "ec2_instance_type": ec2_instance_type,
            "name": name,
        }
        if build_id is not None:
            self._values["build_id"] = build_id
        if certificate_configuration is not None:
            self._values["certificate_configuration"] = certificate_configuration
        if description is not None:
            self._values["description"] = description
        if desired_ec2_instances is not None:
            self._values["desired_ec2_instances"] = desired_ec2_instances
        if ec2_inbound_permissions is not None:
            self._values["ec2_inbound_permissions"] = ec2_inbound_permissions
        if fleet_type is not None:
            self._values["fleet_type"] = fleet_type
        if instance_role_arn is not None:
            self._values["instance_role_arn"] = instance_role_arn
        if log_paths is not None:
            self._values["log_paths"] = log_paths
        if max_size is not None:
            self._values["max_size"] = max_size
        if metric_groups is not None:
            self._values["metric_groups"] = metric_groups
        if min_size is not None:
            self._values["min_size"] = min_size
        if new_game_session_protection_policy is not None:
            self._values["new_game_session_protection_policy"] = new_game_session_protection_policy
        if peer_vpc_aws_account_id is not None:
            self._values["peer_vpc_aws_account_id"] = peer_vpc_aws_account_id
        if peer_vpc_id is not None:
            self._values["peer_vpc_id"] = peer_vpc_id
        if resource_creation_limit_policy is not None:
            self._values["resource_creation_limit_policy"] = resource_creation_limit_policy
        if runtime_configuration is not None:
            self._values["runtime_configuration"] = runtime_configuration
        if script_id is not None:
            self._values["script_id"] = script_id
        if server_launch_parameters is not None:
            self._values["server_launch_parameters"] = server_launch_parameters
        if server_launch_path is not None:
            self._values["server_launch_path"] = server_launch_path

    @builtins.property
    def ec2_instance_type(self) -> builtins.str:
        """``AWS::GameLift::Fleet.EC2InstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-ec2instancetype
        """
        result = self._values.get("ec2_instance_type")
        assert result is not None, "Required property 'ec2_instance_type' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::GameLift::Fleet.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def build_id(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.BuildId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-buildid
        """
        result = self._values.get("build_id")
        return result

    @builtins.property
    def certificate_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFleet.CertificateConfigurationProperty]]:
        """``AWS::GameLift::Fleet.CertificateConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-certificateconfiguration
        """
        result = self._values.get("certificate_configuration")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def desired_ec2_instances(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::Fleet.DesiredEC2Instances``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-desiredec2instances
        """
        result = self._values.get("desired_ec2_instances")
        return result

    @builtins.property
    def ec2_inbound_permissions(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnFleet.IpPermissionProperty]]]]:
        """``AWS::GameLift::Fleet.EC2InboundPermissions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-ec2inboundpermissions
        """
        result = self._values.get("ec2_inbound_permissions")
        return result

    @builtins.property
    def fleet_type(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.FleetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-fleettype
        """
        result = self._values.get("fleet_type")
        return result

    @builtins.property
    def instance_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.InstanceRoleARN``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-instancerolearn
        """
        result = self._values.get("instance_role_arn")
        return result

    @builtins.property
    def log_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::GameLift::Fleet.LogPaths``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-logpaths
        """
        result = self._values.get("log_paths")
        return result

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::Fleet.MaxSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-maxsize
        """
        result = self._values.get("max_size")
        return result

    @builtins.property
    def metric_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::GameLift::Fleet.MetricGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-metricgroups
        """
        result = self._values.get("metric_groups")
        return result

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::Fleet.MinSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-minsize
        """
        result = self._values.get("min_size")
        return result

    @builtins.property
    def new_game_session_protection_policy(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.NewGameSessionProtectionPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-newgamesessionprotectionpolicy
        """
        result = self._values.get("new_game_session_protection_policy")
        return result

    @builtins.property
    def peer_vpc_aws_account_id(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.PeerVpcAwsAccountId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-peervpcawsaccountid
        """
        result = self._values.get("peer_vpc_aws_account_id")
        return result

    @builtins.property
    def peer_vpc_id(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.PeerVpcId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-peervpcid
        """
        result = self._values.get("peer_vpc_id")
        return result

    @builtins.property
    def resource_creation_limit_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFleet.ResourceCreationLimitPolicyProperty]]:
        """``AWS::GameLift::Fleet.ResourceCreationLimitPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-resourcecreationlimitpolicy
        """
        result = self._values.get("resource_creation_limit_policy")
        return result

    @builtins.property
    def runtime_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnFleet.RuntimeConfigurationProperty]]:
        """``AWS::GameLift::Fleet.RuntimeConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-runtimeconfiguration
        """
        result = self._values.get("runtime_configuration")
        return result

    @builtins.property
    def script_id(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.ScriptId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-scriptid
        """
        result = self._values.get("script_id")
        return result

    @builtins.property
    def server_launch_parameters(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.ServerLaunchParameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-serverlaunchparameters
        """
        result = self._values.get("server_launch_parameters")
        return result

    @builtins.property
    def server_launch_path(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Fleet.ServerLaunchPath``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-serverlaunchpath
        """
        result = self._values.get("server_launch_path")
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
class CfnGameServerGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-gamelift.CfnGameServerGroup",
):
    """A CloudFormation ``AWS::GameLift::GameServerGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html
    :cloudformationResource: AWS::GameLift::GameServerGroup
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        game_server_group_name: builtins.str,
        instance_definitions: typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.InstanceDefinitionsProperty"],
        launch_template: typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.LaunchTemplateProperty"],
        role_arn: builtins.str,
        auto_scaling_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.AutoScalingPolicyProperty"]] = None,
        balancing_strategy: typing.Optional[builtins.str] = None,
        delete_option: typing.Optional[builtins.str] = None,
        game_server_protection_policy: typing.Optional[builtins.str] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        tags: typing.Optional["CfnGameServerGroup.TagsProperty"] = None,
        vpc_subnets: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.VpcSubnetsProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::GameLift::GameServerGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param game_server_group_name: ``AWS::GameLift::GameServerGroup.GameServerGroupName``.
        :param instance_definitions: ``AWS::GameLift::GameServerGroup.InstanceDefinitions``.
        :param launch_template: ``AWS::GameLift::GameServerGroup.LaunchTemplate``.
        :param role_arn: ``AWS::GameLift::GameServerGroup.RoleArn``.
        :param auto_scaling_policy: ``AWS::GameLift::GameServerGroup.AutoScalingPolicy``.
        :param balancing_strategy: ``AWS::GameLift::GameServerGroup.BalancingStrategy``.
        :param delete_option: ``AWS::GameLift::GameServerGroup.DeleteOption``.
        :param game_server_protection_policy: ``AWS::GameLift::GameServerGroup.GameServerProtectionPolicy``.
        :param max_size: ``AWS::GameLift::GameServerGroup.MaxSize``.
        :param min_size: ``AWS::GameLift::GameServerGroup.MinSize``.
        :param tags: ``AWS::GameLift::GameServerGroup.Tags``.
        :param vpc_subnets: ``AWS::GameLift::GameServerGroup.VpcSubnets``.
        """
        props = CfnGameServerGroupProps(
            game_server_group_name=game_server_group_name,
            instance_definitions=instance_definitions,
            launch_template=launch_template,
            role_arn=role_arn,
            auto_scaling_policy=auto_scaling_policy,
            balancing_strategy=balancing_strategy,
            delete_option=delete_option,
            game_server_protection_policy=game_server_protection_policy,
            max_size=max_size,
            min_size=min_size,
            tags=tags,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(CfnGameServerGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrAutoScalingGroupArn")
    def attr_auto_scaling_group_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: AutoScalingGroupArn
        """
        return jsii.get(self, "attrAutoScalingGroupArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrGameServerGroupArn")
    def attr_game_server_group_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: GameServerGroupArn
        """
        return jsii.get(self, "attrGameServerGroupArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::GameLift::GameServerGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gameServerGroupName")
    def game_server_group_name(self) -> builtins.str:
        """``AWS::GameLift::GameServerGroup.GameServerGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-gameservergroupname
        """
        return jsii.get(self, "gameServerGroupName")

    @game_server_group_name.setter # type: ignore
    def game_server_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "gameServerGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceDefinitions")
    def instance_definitions(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.InstanceDefinitionsProperty"]:
        """``AWS::GameLift::GameServerGroup.InstanceDefinitions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-instancedefinitions
        """
        return jsii.get(self, "instanceDefinitions")

    @instance_definitions.setter # type: ignore
    def instance_definitions(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.InstanceDefinitionsProperty"],
    ) -> None:
        jsii.set(self, "instanceDefinitions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.LaunchTemplateProperty"]:
        """``AWS::GameLift::GameServerGroup.LaunchTemplate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-launchtemplate
        """
        return jsii.get(self, "launchTemplate")

    @launch_template.setter # type: ignore
    def launch_template(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.LaunchTemplateProperty"],
    ) -> None:
        jsii.set(self, "launchTemplate", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        """``AWS::GameLift::GameServerGroup.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter # type: ignore
    def role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoScalingPolicy")
    def auto_scaling_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.AutoScalingPolicyProperty"]]:
        """``AWS::GameLift::GameServerGroup.AutoScalingPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-autoscalingpolicy
        """
        return jsii.get(self, "autoScalingPolicy")

    @auto_scaling_policy.setter # type: ignore
    def auto_scaling_policy(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.AutoScalingPolicyProperty"]],
    ) -> None:
        jsii.set(self, "autoScalingPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="balancingStrategy")
    def balancing_strategy(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::GameServerGroup.BalancingStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-balancingstrategy
        """
        return jsii.get(self, "balancingStrategy")

    @balancing_strategy.setter # type: ignore
    def balancing_strategy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "balancingStrategy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deleteOption")
    def delete_option(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::GameServerGroup.DeleteOption``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-deleteoption
        """
        return jsii.get(self, "deleteOption")

    @delete_option.setter # type: ignore
    def delete_option(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "deleteOption", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gameServerProtectionPolicy")
    def game_server_protection_policy(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::GameServerGroup.GameServerProtectionPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-gameserverprotectionpolicy
        """
        return jsii.get(self, "gameServerProtectionPolicy")

    @game_server_protection_policy.setter # type: ignore
    def game_server_protection_policy(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "gameServerProtectionPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxSize")
    def max_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::GameServerGroup.MaxSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-maxsize
        """
        return jsii.get(self, "maxSize")

    @max_size.setter # type: ignore
    def max_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxSize", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="minSize")
    def min_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::GameServerGroup.MinSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-minsize
        """
        return jsii.get(self, "minSize")

    @min_size.setter # type: ignore
    def min_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "minSize", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcSubnets")
    def vpc_subnets(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.VpcSubnetsProperty"]]:
        """``AWS::GameLift::GameServerGroup.VpcSubnets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-vpcsubnets
        """
        return jsii.get(self, "vpcSubnets")

    @vpc_subnets.setter # type: ignore
    def vpc_subnets(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.VpcSubnetsProperty"]],
    ) -> None:
        jsii.set(self, "vpcSubnets", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnGameServerGroup.AutoScalingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_tracking_configuration": "targetTrackingConfiguration",
            "estimated_instance_warmup": "estimatedInstanceWarmup",
        },
    )
    class AutoScalingPolicyProperty:
        def __init__(
            self,
            *,
            target_tracking_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.TargetTrackingConfigurationProperty"],
            estimated_instance_warmup: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param target_tracking_configuration: ``CfnGameServerGroup.AutoScalingPolicyProperty.TargetTrackingConfiguration``.
            :param estimated_instance_warmup: ``CfnGameServerGroup.AutoScalingPolicyProperty.EstimatedInstanceWarmup``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-autoscalingpolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "target_tracking_configuration": target_tracking_configuration,
            }
            if estimated_instance_warmup is not None:
                self._values["estimated_instance_warmup"] = estimated_instance_warmup

        @builtins.property
        def target_tracking_configuration(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.TargetTrackingConfigurationProperty"]:
            """``CfnGameServerGroup.AutoScalingPolicyProperty.TargetTrackingConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-autoscalingpolicy.html#cfn-gamelift-gameservergroup-autoscalingpolicy-targettrackingconfiguration
            """
            result = self._values.get("target_tracking_configuration")
            assert result is not None, "Required property 'target_tracking_configuration' is missing"
            return result

        @builtins.property
        def estimated_instance_warmup(self) -> typing.Optional[jsii.Number]:
            """``CfnGameServerGroup.AutoScalingPolicyProperty.EstimatedInstanceWarmup``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-autoscalingpolicy.html#cfn-gamelift-gameservergroup-autoscalingpolicy-estimatedinstancewarmup
            """
            result = self._values.get("estimated_instance_warmup")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnGameServerGroup.InstanceDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_type": "instanceType",
            "weighted_capacity": "weightedCapacity",
        },
    )
    class InstanceDefinitionProperty:
        def __init__(
            self,
            *,
            instance_type: builtins.str,
            weighted_capacity: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param instance_type: ``CfnGameServerGroup.InstanceDefinitionProperty.InstanceType``.
            :param weighted_capacity: ``CfnGameServerGroup.InstanceDefinitionProperty.WeightedCapacity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-instancedefinition.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "instance_type": instance_type,
            }
            if weighted_capacity is not None:
                self._values["weighted_capacity"] = weighted_capacity

        @builtins.property
        def instance_type(self) -> builtins.str:
            """``CfnGameServerGroup.InstanceDefinitionProperty.InstanceType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-instancedefinition.html#cfn-gamelift-gameservergroup-instancedefinition-instancetype
            """
            result = self._values.get("instance_type")
            assert result is not None, "Required property 'instance_type' is missing"
            return result

        @builtins.property
        def weighted_capacity(self) -> typing.Optional[builtins.str]:
            """``CfnGameServerGroup.InstanceDefinitionProperty.WeightedCapacity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-instancedefinition.html#cfn-gamelift-gameservergroup-instancedefinition-weightedcapacity
            """
            result = self._values.get("weighted_capacity")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnGameServerGroup.InstanceDefinitionsProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_definitions": "instanceDefinitions"},
    )
    class InstanceDefinitionsProperty:
        def __init__(
            self,
            *,
            instance_definitions: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.InstanceDefinitionProperty"]]]] = None,
        ) -> None:
            """
            :param instance_definitions: ``CfnGameServerGroup.InstanceDefinitionsProperty.InstanceDefinitions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-instancedefinitions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if instance_definitions is not None:
                self._values["instance_definitions"] = instance_definitions

        @builtins.property
        def instance_definitions(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnGameServerGroup.InstanceDefinitionProperty"]]]]:
            """``CfnGameServerGroup.InstanceDefinitionsProperty.InstanceDefinitions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-instancedefinitions.html#cfn-gamelift-gameservergroup-instancedefinitions-instancedefinitions
            """
            result = self._values.get("instance_definitions")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceDefinitionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnGameServerGroup.LaunchTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_template_id": "launchTemplateId",
            "launch_template_name": "launchTemplateName",
            "version": "version",
        },
    )
    class LaunchTemplateProperty:
        def __init__(
            self,
            *,
            launch_template_id: typing.Optional[builtins.str] = None,
            launch_template_name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param launch_template_id: ``CfnGameServerGroup.LaunchTemplateProperty.LaunchTemplateId``.
            :param launch_template_name: ``CfnGameServerGroup.LaunchTemplateProperty.LaunchTemplateName``.
            :param version: ``CfnGameServerGroup.LaunchTemplateProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-launchtemplate.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if launch_template_id is not None:
                self._values["launch_template_id"] = launch_template_id
            if launch_template_name is not None:
                self._values["launch_template_name"] = launch_template_name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def launch_template_id(self) -> typing.Optional[builtins.str]:
            """``CfnGameServerGroup.LaunchTemplateProperty.LaunchTemplateId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-launchtemplate.html#cfn-gamelift-gameservergroup-launchtemplate-launchtemplateid
            """
            result = self._values.get("launch_template_id")
            return result

        @builtins.property
        def launch_template_name(self) -> typing.Optional[builtins.str]:
            """``CfnGameServerGroup.LaunchTemplateProperty.LaunchTemplateName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-launchtemplate.html#cfn-gamelift-gameservergroup-launchtemplate-launchtemplatename
            """
            result = self._values.get("launch_template_name")
            return result

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            """``CfnGameServerGroup.LaunchTemplateProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-launchtemplate.html#cfn-gamelift-gameservergroup-launchtemplate-version
            """
            result = self._values.get("version")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnGameServerGroup.TagsProperty",
        jsii_struct_bases=[],
        name_mapping={"tags": "tags"},
    )
    class TagsProperty:
        def __init__(
            self,
            *,
            tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        ) -> None:
            """
            :param tags: ``CfnGameServerGroup.TagsProperty.Tags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-tags.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
            """``CfnGameServerGroup.TagsProperty.Tags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-tags.html#cfn-gamelift-gameservergroup-tags-tags
            """
            result = self._values.get("tags")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnGameServerGroup.TargetTrackingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"target_value": "targetValue"},
    )
    class TargetTrackingConfigurationProperty:
        def __init__(self, *, target_value: jsii.Number) -> None:
            """
            :param target_value: ``CfnGameServerGroup.TargetTrackingConfigurationProperty.TargetValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-targettrackingconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "target_value": target_value,
            }

        @builtins.property
        def target_value(self) -> jsii.Number:
            """``CfnGameServerGroup.TargetTrackingConfigurationProperty.TargetValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-targettrackingconfiguration.html#cfn-gamelift-gameservergroup-targettrackingconfiguration-targetvalue
            """
            result = self._values.get("target_value")
            assert result is not None, "Required property 'target_value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTrackingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnGameServerGroup.VpcSubnetsProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_subnets": "vpcSubnets"},
    )
    class VpcSubnetsProperty:
        def __init__(
            self,
            *,
            vpc_subnets: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param vpc_subnets: ``CfnGameServerGroup.VpcSubnetsProperty.VpcSubnets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-vpcsubnets.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if vpc_subnets is not None:
                self._values["vpc_subnets"] = vpc_subnets

        @builtins.property
        def vpc_subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnGameServerGroup.VpcSubnetsProperty.VpcSubnets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gameservergroup-vpcsubnets.html#cfn-gamelift-gameservergroup-vpcsubnets-vpcsubnets
            """
            result = self._values.get("vpc_subnets")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcSubnetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-gamelift.CfnGameServerGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "game_server_group_name": "gameServerGroupName",
        "instance_definitions": "instanceDefinitions",
        "launch_template": "launchTemplate",
        "role_arn": "roleArn",
        "auto_scaling_policy": "autoScalingPolicy",
        "balancing_strategy": "balancingStrategy",
        "delete_option": "deleteOption",
        "game_server_protection_policy": "gameServerProtectionPolicy",
        "max_size": "maxSize",
        "min_size": "minSize",
        "tags": "tags",
        "vpc_subnets": "vpcSubnets",
    },
)
class CfnGameServerGroupProps:
    def __init__(
        self,
        *,
        game_server_group_name: builtins.str,
        instance_definitions: typing.Union[aws_cdk.core.IResolvable, CfnGameServerGroup.InstanceDefinitionsProperty],
        launch_template: typing.Union[aws_cdk.core.IResolvable, CfnGameServerGroup.LaunchTemplateProperty],
        role_arn: builtins.str,
        auto_scaling_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnGameServerGroup.AutoScalingPolicyProperty]] = None,
        balancing_strategy: typing.Optional[builtins.str] = None,
        delete_option: typing.Optional[builtins.str] = None,
        game_server_protection_policy: typing.Optional[builtins.str] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[CfnGameServerGroup.TagsProperty] = None,
        vpc_subnets: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnGameServerGroup.VpcSubnetsProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::GameLift::GameServerGroup``.

        :param game_server_group_name: ``AWS::GameLift::GameServerGroup.GameServerGroupName``.
        :param instance_definitions: ``AWS::GameLift::GameServerGroup.InstanceDefinitions``.
        :param launch_template: ``AWS::GameLift::GameServerGroup.LaunchTemplate``.
        :param role_arn: ``AWS::GameLift::GameServerGroup.RoleArn``.
        :param auto_scaling_policy: ``AWS::GameLift::GameServerGroup.AutoScalingPolicy``.
        :param balancing_strategy: ``AWS::GameLift::GameServerGroup.BalancingStrategy``.
        :param delete_option: ``AWS::GameLift::GameServerGroup.DeleteOption``.
        :param game_server_protection_policy: ``AWS::GameLift::GameServerGroup.GameServerProtectionPolicy``.
        :param max_size: ``AWS::GameLift::GameServerGroup.MaxSize``.
        :param min_size: ``AWS::GameLift::GameServerGroup.MinSize``.
        :param tags: ``AWS::GameLift::GameServerGroup.Tags``.
        :param vpc_subnets: ``AWS::GameLift::GameServerGroup.VpcSubnets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html
        """
        if isinstance(tags, dict):
            tags = CfnGameServerGroup.TagsProperty(**tags)
        self._values: typing.Dict[str, typing.Any] = {
            "game_server_group_name": game_server_group_name,
            "instance_definitions": instance_definitions,
            "launch_template": launch_template,
            "role_arn": role_arn,
        }
        if auto_scaling_policy is not None:
            self._values["auto_scaling_policy"] = auto_scaling_policy
        if balancing_strategy is not None:
            self._values["balancing_strategy"] = balancing_strategy
        if delete_option is not None:
            self._values["delete_option"] = delete_option
        if game_server_protection_policy is not None:
            self._values["game_server_protection_policy"] = game_server_protection_policy
        if max_size is not None:
            self._values["max_size"] = max_size
        if min_size is not None:
            self._values["min_size"] = min_size
        if tags is not None:
            self._values["tags"] = tags
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def game_server_group_name(self) -> builtins.str:
        """``AWS::GameLift::GameServerGroup.GameServerGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-gameservergroupname
        """
        result = self._values.get("game_server_group_name")
        assert result is not None, "Required property 'game_server_group_name' is missing"
        return result

    @builtins.property
    def instance_definitions(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnGameServerGroup.InstanceDefinitionsProperty]:
        """``AWS::GameLift::GameServerGroup.InstanceDefinitions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-instancedefinitions
        """
        result = self._values.get("instance_definitions")
        assert result is not None, "Required property 'instance_definitions' is missing"
        return result

    @builtins.property
    def launch_template(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnGameServerGroup.LaunchTemplateProperty]:
        """``AWS::GameLift::GameServerGroup.LaunchTemplate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-launchtemplate
        """
        result = self._values.get("launch_template")
        assert result is not None, "Required property 'launch_template' is missing"
        return result

    @builtins.property
    def role_arn(self) -> builtins.str:
        """``AWS::GameLift::GameServerGroup.RoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-rolearn
        """
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return result

    @builtins.property
    def auto_scaling_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnGameServerGroup.AutoScalingPolicyProperty]]:
        """``AWS::GameLift::GameServerGroup.AutoScalingPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-autoscalingpolicy
        """
        result = self._values.get("auto_scaling_policy")
        return result

    @builtins.property
    def balancing_strategy(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::GameServerGroup.BalancingStrategy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-balancingstrategy
        """
        result = self._values.get("balancing_strategy")
        return result

    @builtins.property
    def delete_option(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::GameServerGroup.DeleteOption``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-deleteoption
        """
        result = self._values.get("delete_option")
        return result

    @builtins.property
    def game_server_protection_policy(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::GameServerGroup.GameServerProtectionPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-gameserverprotectionpolicy
        """
        result = self._values.get("game_server_protection_policy")
        return result

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::GameServerGroup.MaxSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-maxsize
        """
        result = self._values.get("max_size")
        return result

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::GameServerGroup.MinSize``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-minsize
        """
        result = self._values.get("min_size")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[CfnGameServerGroup.TagsProperty]:
        """``AWS::GameLift::GameServerGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def vpc_subnets(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnGameServerGroup.VpcSubnetsProperty]]:
        """``AWS::GameLift::GameServerGroup.VpcSubnets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gameservergroup.html#cfn-gamelift-gameservergroup-vpcsubnets
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGameServerGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnGameSessionQueue(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-gamelift.CfnGameSessionQueue",
):
    """A CloudFormation ``AWS::GameLift::GameSessionQueue``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html
    :cloudformationResource: AWS::GameLift::GameSessionQueue
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        destinations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnGameSessionQueue.DestinationProperty"]]]] = None,
        player_latency_policies: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnGameSessionQueue.PlayerLatencyPolicyProperty"]]]] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Create a new ``AWS::GameLift::GameSessionQueue``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::GameLift::GameSessionQueue.Name``.
        :param destinations: ``AWS::GameLift::GameSessionQueue.Destinations``.
        :param player_latency_policies: ``AWS::GameLift::GameSessionQueue.PlayerLatencyPolicies``.
        :param timeout_in_seconds: ``AWS::GameLift::GameSessionQueue.TimeoutInSeconds``.
        """
        props = CfnGameSessionQueueProps(
            name=name,
            destinations=destinations,
            player_latency_policies=player_latency_policies,
            timeout_in_seconds=timeout_in_seconds,
        )

        jsii.create(CfnGameSessionQueue, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        """
        :cloudformationAttribute: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::GameLift::GameSessionQueue.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="destinations")
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnGameSessionQueue.DestinationProperty"]]]]:
        """``AWS::GameLift::GameSessionQueue.Destinations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-destinations
        """
        return jsii.get(self, "destinations")

    @destinations.setter # type: ignore
    def destinations(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnGameSessionQueue.DestinationProperty"]]]],
    ) -> None:
        jsii.set(self, "destinations", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="playerLatencyPolicies")
    def player_latency_policies(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnGameSessionQueue.PlayerLatencyPolicyProperty"]]]]:
        """``AWS::GameLift::GameSessionQueue.PlayerLatencyPolicies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-playerlatencypolicies
        """
        return jsii.get(self, "playerLatencyPolicies")

    @player_latency_policies.setter # type: ignore
    def player_latency_policies(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnGameSessionQueue.PlayerLatencyPolicyProperty"]]]],
    ) -> None:
        jsii.set(self, "playerLatencyPolicies", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="timeoutInSeconds")
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::GameSessionQueue.TimeoutInSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-timeoutinseconds
        """
        return jsii.get(self, "timeoutInSeconds")

    @timeout_in_seconds.setter # type: ignore
    def timeout_in_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeoutInSeconds", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnGameSessionQueue.DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"destination_arn": "destinationArn"},
    )
    class DestinationProperty:
        def __init__(
            self,
            *,
            destination_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param destination_arn: ``CfnGameSessionQueue.DestinationProperty.DestinationArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-destination.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if destination_arn is not None:
                self._values["destination_arn"] = destination_arn

        @builtins.property
        def destination_arn(self) -> typing.Optional[builtins.str]:
            """``CfnGameSessionQueue.DestinationProperty.DestinationArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-destination.html#cfn-gamelift-gamesessionqueue-destination-destinationarn
            """
            result = self._values.get("destination_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnGameSessionQueue.PlayerLatencyPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_individual_player_latency_milliseconds": "maximumIndividualPlayerLatencyMilliseconds",
            "policy_duration_seconds": "policyDurationSeconds",
        },
    )
    class PlayerLatencyPolicyProperty:
        def __init__(
            self,
            *,
            maximum_individual_player_latency_milliseconds: typing.Optional[jsii.Number] = None,
            policy_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param maximum_individual_player_latency_milliseconds: ``CfnGameSessionQueue.PlayerLatencyPolicyProperty.MaximumIndividualPlayerLatencyMilliseconds``.
            :param policy_duration_seconds: ``CfnGameSessionQueue.PlayerLatencyPolicyProperty.PolicyDurationSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-playerlatencypolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if maximum_individual_player_latency_milliseconds is not None:
                self._values["maximum_individual_player_latency_milliseconds"] = maximum_individual_player_latency_milliseconds
            if policy_duration_seconds is not None:
                self._values["policy_duration_seconds"] = policy_duration_seconds

        @builtins.property
        def maximum_individual_player_latency_milliseconds(
            self,
        ) -> typing.Optional[jsii.Number]:
            """``CfnGameSessionQueue.PlayerLatencyPolicyProperty.MaximumIndividualPlayerLatencyMilliseconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-playerlatencypolicy.html#cfn-gamelift-gamesessionqueue-playerlatencypolicy-maximumindividualplayerlatencymilliseconds
            """
            result = self._values.get("maximum_individual_player_latency_milliseconds")
            return result

        @builtins.property
        def policy_duration_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnGameSessionQueue.PlayerLatencyPolicyProperty.PolicyDurationSeconds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-gamesessionqueue-playerlatencypolicy.html#cfn-gamelift-gamesessionqueue-playerlatencypolicy-policydurationseconds
            """
            result = self._values.get("policy_duration_seconds")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlayerLatencyPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-gamelift.CfnGameSessionQueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "destinations": "destinations",
        "player_latency_policies": "playerLatencyPolicies",
        "timeout_in_seconds": "timeoutInSeconds",
    },
)
class CfnGameSessionQueueProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        destinations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnGameSessionQueue.DestinationProperty]]]] = None,
        player_latency_policies: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnGameSessionQueue.PlayerLatencyPolicyProperty]]]] = None,
        timeout_in_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for defining a ``AWS::GameLift::GameSessionQueue``.

        :param name: ``AWS::GameLift::GameSessionQueue.Name``.
        :param destinations: ``AWS::GameLift::GameSessionQueue.Destinations``.
        :param player_latency_policies: ``AWS::GameLift::GameSessionQueue.PlayerLatencyPolicies``.
        :param timeout_in_seconds: ``AWS::GameLift::GameSessionQueue.TimeoutInSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if destinations is not None:
            self._values["destinations"] = destinations
        if player_latency_policies is not None:
            self._values["player_latency_policies"] = player_latency_policies
        if timeout_in_seconds is not None:
            self._values["timeout_in_seconds"] = timeout_in_seconds

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::GameLift::GameSessionQueue.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnGameSessionQueue.DestinationProperty]]]]:
        """``AWS::GameLift::GameSessionQueue.Destinations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-destinations
        """
        result = self._values.get("destinations")
        return result

    @builtins.property
    def player_latency_policies(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnGameSessionQueue.PlayerLatencyPolicyProperty]]]]:
        """``AWS::GameLift::GameSessionQueue.PlayerLatencyPolicies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-playerlatencypolicies
        """
        result = self._values.get("player_latency_policies")
        return result

    @builtins.property
    def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::GameSessionQueue.TimeoutInSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-gamesessionqueue.html#cfn-gamelift-gamesessionqueue-timeoutinseconds
        """
        result = self._values.get("timeout_in_seconds")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGameSessionQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMatchmakingConfiguration(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-gamelift.CfnMatchmakingConfiguration",
):
    """A CloudFormation ``AWS::GameLift::MatchmakingConfiguration``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html
    :cloudformationResource: AWS::GameLift::MatchmakingConfiguration
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        acceptance_required: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        name: builtins.str,
        request_timeout_seconds: jsii.Number,
        rule_set_name: builtins.str,
        acceptance_timeout_seconds: typing.Optional[jsii.Number] = None,
        additional_player_count: typing.Optional[jsii.Number] = None,
        backfill_mode: typing.Optional[builtins.str] = None,
        custom_event_data: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        flex_match_mode: typing.Optional[builtins.str] = None,
        game_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMatchmakingConfiguration.GamePropertyProperty"]]]] = None,
        game_session_data: typing.Optional[builtins.str] = None,
        game_session_queue_arns: typing.Optional[typing.List[builtins.str]] = None,
        notification_target: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::GameLift::MatchmakingConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param acceptance_required: ``AWS::GameLift::MatchmakingConfiguration.AcceptanceRequired``.
        :param name: ``AWS::GameLift::MatchmakingConfiguration.Name``.
        :param request_timeout_seconds: ``AWS::GameLift::MatchmakingConfiguration.RequestTimeoutSeconds``.
        :param rule_set_name: ``AWS::GameLift::MatchmakingConfiguration.RuleSetName``.
        :param acceptance_timeout_seconds: ``AWS::GameLift::MatchmakingConfiguration.AcceptanceTimeoutSeconds``.
        :param additional_player_count: ``AWS::GameLift::MatchmakingConfiguration.AdditionalPlayerCount``.
        :param backfill_mode: ``AWS::GameLift::MatchmakingConfiguration.BackfillMode``.
        :param custom_event_data: ``AWS::GameLift::MatchmakingConfiguration.CustomEventData``.
        :param description: ``AWS::GameLift::MatchmakingConfiguration.Description``.
        :param flex_match_mode: ``AWS::GameLift::MatchmakingConfiguration.FlexMatchMode``.
        :param game_properties: ``AWS::GameLift::MatchmakingConfiguration.GameProperties``.
        :param game_session_data: ``AWS::GameLift::MatchmakingConfiguration.GameSessionData``.
        :param game_session_queue_arns: ``AWS::GameLift::MatchmakingConfiguration.GameSessionQueueArns``.
        :param notification_target: ``AWS::GameLift::MatchmakingConfiguration.NotificationTarget``.
        """
        props = CfnMatchmakingConfigurationProps(
            acceptance_required=acceptance_required,
            name=name,
            request_timeout_seconds=request_timeout_seconds,
            rule_set_name=rule_set_name,
            acceptance_timeout_seconds=acceptance_timeout_seconds,
            additional_player_count=additional_player_count,
            backfill_mode=backfill_mode,
            custom_event_data=custom_event_data,
            description=description,
            flex_match_mode=flex_match_mode,
            game_properties=game_properties,
            game_session_data=game_session_data,
            game_session_queue_arns=game_session_queue_arns,
            notification_target=notification_target,
        )

        jsii.create(CfnMatchmakingConfiguration, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        """
        :cloudformationAttribute: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="acceptanceRequired")
    def acceptance_required(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::GameLift::MatchmakingConfiguration.AcceptanceRequired``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-acceptancerequired
        """
        return jsii.get(self, "acceptanceRequired")

    @acceptance_required.setter # type: ignore
    def acceptance_required(
        self,
        value: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "acceptanceRequired", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::GameLift::MatchmakingConfiguration.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="requestTimeoutSeconds")
    def request_timeout_seconds(self) -> jsii.Number:
        """``AWS::GameLift::MatchmakingConfiguration.RequestTimeoutSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-requesttimeoutseconds
        """
        return jsii.get(self, "requestTimeoutSeconds")

    @request_timeout_seconds.setter # type: ignore
    def request_timeout_seconds(self, value: jsii.Number) -> None:
        jsii.set(self, "requestTimeoutSeconds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleSetName")
    def rule_set_name(self) -> builtins.str:
        """``AWS::GameLift::MatchmakingConfiguration.RuleSetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-rulesetname
        """
        return jsii.get(self, "ruleSetName")

    @rule_set_name.setter # type: ignore
    def rule_set_name(self, value: builtins.str) -> None:
        jsii.set(self, "ruleSetName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="acceptanceTimeoutSeconds")
    def acceptance_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::MatchmakingConfiguration.AcceptanceTimeoutSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-acceptancetimeoutseconds
        """
        return jsii.get(self, "acceptanceTimeoutSeconds")

    @acceptance_timeout_seconds.setter # type: ignore
    def acceptance_timeout_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "acceptanceTimeoutSeconds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="additionalPlayerCount")
    def additional_player_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::MatchmakingConfiguration.AdditionalPlayerCount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-additionalplayercount
        """
        return jsii.get(self, "additionalPlayerCount")

    @additional_player_count.setter # type: ignore
    def additional_player_count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "additionalPlayerCount", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="backfillMode")
    def backfill_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.BackfillMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-backfillmode
        """
        return jsii.get(self, "backfillMode")

    @backfill_mode.setter # type: ignore
    def backfill_mode(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "backfillMode", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="customEventData")
    def custom_event_data(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.CustomEventData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-customeventdata
        """
        return jsii.get(self, "customEventData")

    @custom_event_data.setter # type: ignore
    def custom_event_data(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "customEventData", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="flexMatchMode")
    def flex_match_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.FlexMatchMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-flexmatchmode
        """
        return jsii.get(self, "flexMatchMode")

    @flex_match_mode.setter # type: ignore
    def flex_match_mode(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "flexMatchMode", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gameProperties")
    def game_properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMatchmakingConfiguration.GamePropertyProperty"]]]]:
        """``AWS::GameLift::MatchmakingConfiguration.GameProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-gameproperties
        """
        return jsii.get(self, "gameProperties")

    @game_properties.setter # type: ignore
    def game_properties(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMatchmakingConfiguration.GamePropertyProperty"]]]],
    ) -> None:
        jsii.set(self, "gameProperties", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gameSessionData")
    def game_session_data(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.GameSessionData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-gamesessiondata
        """
        return jsii.get(self, "gameSessionData")

    @game_session_data.setter # type: ignore
    def game_session_data(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "gameSessionData", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gameSessionQueueArns")
    def game_session_queue_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::GameLift::MatchmakingConfiguration.GameSessionQueueArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-gamesessionqueuearns
        """
        return jsii.get(self, "gameSessionQueueArns")

    @game_session_queue_arns.setter # type: ignore
    def game_session_queue_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "gameSessionQueueArns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="notificationTarget")
    def notification_target(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.NotificationTarget``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-notificationtarget
        """
        return jsii.get(self, "notificationTarget")

    @notification_target.setter # type: ignore
    def notification_target(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "notificationTarget", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnMatchmakingConfiguration.GamePropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class GamePropertyProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            """
            :param key: ``CfnMatchmakingConfiguration.GamePropertyProperty.Key``.
            :param value: ``CfnMatchmakingConfiguration.GamePropertyProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-matchmakingconfiguration-gameproperty.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            """``CfnMatchmakingConfiguration.GamePropertyProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-matchmakingconfiguration-gameproperty.html#cfn-gamelift-matchmakingconfiguration-gameproperty-key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnMatchmakingConfiguration.GamePropertyProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-matchmakingconfiguration-gameproperty.html#cfn-gamelift-matchmakingconfiguration-gameproperty-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GamePropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-gamelift.CfnMatchmakingConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "acceptance_required": "acceptanceRequired",
        "name": "name",
        "request_timeout_seconds": "requestTimeoutSeconds",
        "rule_set_name": "ruleSetName",
        "acceptance_timeout_seconds": "acceptanceTimeoutSeconds",
        "additional_player_count": "additionalPlayerCount",
        "backfill_mode": "backfillMode",
        "custom_event_data": "customEventData",
        "description": "description",
        "flex_match_mode": "flexMatchMode",
        "game_properties": "gameProperties",
        "game_session_data": "gameSessionData",
        "game_session_queue_arns": "gameSessionQueueArns",
        "notification_target": "notificationTarget",
    },
)
class CfnMatchmakingConfigurationProps:
    def __init__(
        self,
        *,
        acceptance_required: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        name: builtins.str,
        request_timeout_seconds: jsii.Number,
        rule_set_name: builtins.str,
        acceptance_timeout_seconds: typing.Optional[jsii.Number] = None,
        additional_player_count: typing.Optional[jsii.Number] = None,
        backfill_mode: typing.Optional[builtins.str] = None,
        custom_event_data: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        flex_match_mode: typing.Optional[builtins.str] = None,
        game_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnMatchmakingConfiguration.GamePropertyProperty]]]] = None,
        game_session_data: typing.Optional[builtins.str] = None,
        game_session_queue_arns: typing.Optional[typing.List[builtins.str]] = None,
        notification_target: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::GameLift::MatchmakingConfiguration``.

        :param acceptance_required: ``AWS::GameLift::MatchmakingConfiguration.AcceptanceRequired``.
        :param name: ``AWS::GameLift::MatchmakingConfiguration.Name``.
        :param request_timeout_seconds: ``AWS::GameLift::MatchmakingConfiguration.RequestTimeoutSeconds``.
        :param rule_set_name: ``AWS::GameLift::MatchmakingConfiguration.RuleSetName``.
        :param acceptance_timeout_seconds: ``AWS::GameLift::MatchmakingConfiguration.AcceptanceTimeoutSeconds``.
        :param additional_player_count: ``AWS::GameLift::MatchmakingConfiguration.AdditionalPlayerCount``.
        :param backfill_mode: ``AWS::GameLift::MatchmakingConfiguration.BackfillMode``.
        :param custom_event_data: ``AWS::GameLift::MatchmakingConfiguration.CustomEventData``.
        :param description: ``AWS::GameLift::MatchmakingConfiguration.Description``.
        :param flex_match_mode: ``AWS::GameLift::MatchmakingConfiguration.FlexMatchMode``.
        :param game_properties: ``AWS::GameLift::MatchmakingConfiguration.GameProperties``.
        :param game_session_data: ``AWS::GameLift::MatchmakingConfiguration.GameSessionData``.
        :param game_session_queue_arns: ``AWS::GameLift::MatchmakingConfiguration.GameSessionQueueArns``.
        :param notification_target: ``AWS::GameLift::MatchmakingConfiguration.NotificationTarget``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "acceptance_required": acceptance_required,
            "name": name,
            "request_timeout_seconds": request_timeout_seconds,
            "rule_set_name": rule_set_name,
        }
        if acceptance_timeout_seconds is not None:
            self._values["acceptance_timeout_seconds"] = acceptance_timeout_seconds
        if additional_player_count is not None:
            self._values["additional_player_count"] = additional_player_count
        if backfill_mode is not None:
            self._values["backfill_mode"] = backfill_mode
        if custom_event_data is not None:
            self._values["custom_event_data"] = custom_event_data
        if description is not None:
            self._values["description"] = description
        if flex_match_mode is not None:
            self._values["flex_match_mode"] = flex_match_mode
        if game_properties is not None:
            self._values["game_properties"] = game_properties
        if game_session_data is not None:
            self._values["game_session_data"] = game_session_data
        if game_session_queue_arns is not None:
            self._values["game_session_queue_arns"] = game_session_queue_arns
        if notification_target is not None:
            self._values["notification_target"] = notification_target

    @builtins.property
    def acceptance_required(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::GameLift::MatchmakingConfiguration.AcceptanceRequired``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-acceptancerequired
        """
        result = self._values.get("acceptance_required")
        assert result is not None, "Required property 'acceptance_required' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::GameLift::MatchmakingConfiguration.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def request_timeout_seconds(self) -> jsii.Number:
        """``AWS::GameLift::MatchmakingConfiguration.RequestTimeoutSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-requesttimeoutseconds
        """
        result = self._values.get("request_timeout_seconds")
        assert result is not None, "Required property 'request_timeout_seconds' is missing"
        return result

    @builtins.property
    def rule_set_name(self) -> builtins.str:
        """``AWS::GameLift::MatchmakingConfiguration.RuleSetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-rulesetname
        """
        result = self._values.get("rule_set_name")
        assert result is not None, "Required property 'rule_set_name' is missing"
        return result

    @builtins.property
    def acceptance_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::MatchmakingConfiguration.AcceptanceTimeoutSeconds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-acceptancetimeoutseconds
        """
        result = self._values.get("acceptance_timeout_seconds")
        return result

    @builtins.property
    def additional_player_count(self) -> typing.Optional[jsii.Number]:
        """``AWS::GameLift::MatchmakingConfiguration.AdditionalPlayerCount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-additionalplayercount
        """
        result = self._values.get("additional_player_count")
        return result

    @builtins.property
    def backfill_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.BackfillMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-backfillmode
        """
        result = self._values.get("backfill_mode")
        return result

    @builtins.property
    def custom_event_data(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.CustomEventData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-customeventdata
        """
        result = self._values.get("custom_event_data")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def flex_match_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.FlexMatchMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-flexmatchmode
        """
        result = self._values.get("flex_match_mode")
        return result

    @builtins.property
    def game_properties(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnMatchmakingConfiguration.GamePropertyProperty]]]]:
        """``AWS::GameLift::MatchmakingConfiguration.GameProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-gameproperties
        """
        result = self._values.get("game_properties")
        return result

    @builtins.property
    def game_session_data(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.GameSessionData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-gamesessiondata
        """
        result = self._values.get("game_session_data")
        return result

    @builtins.property
    def game_session_queue_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::GameLift::MatchmakingConfiguration.GameSessionQueueArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-gamesessionqueuearns
        """
        result = self._values.get("game_session_queue_arns")
        return result

    @builtins.property
    def notification_target(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::MatchmakingConfiguration.NotificationTarget``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingconfiguration.html#cfn-gamelift-matchmakingconfiguration-notificationtarget
        """
        result = self._values.get("notification_target")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMatchmakingConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMatchmakingRuleSet(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-gamelift.CfnMatchmakingRuleSet",
):
    """A CloudFormation ``AWS::GameLift::MatchmakingRuleSet``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingruleset.html
    :cloudformationResource: AWS::GameLift::MatchmakingRuleSet
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        rule_set_body: builtins.str,
    ) -> None:
        """Create a new ``AWS::GameLift::MatchmakingRuleSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::GameLift::MatchmakingRuleSet.Name``.
        :param rule_set_body: ``AWS::GameLift::MatchmakingRuleSet.RuleSetBody``.
        """
        props = CfnMatchmakingRuleSetProps(name=name, rule_set_body=rule_set_body)

        jsii.create(CfnMatchmakingRuleSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        """
        :cloudformationAttribute: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::GameLift::MatchmakingRuleSet.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingruleset.html#cfn-gamelift-matchmakingruleset-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleSetBody")
    def rule_set_body(self) -> builtins.str:
        """``AWS::GameLift::MatchmakingRuleSet.RuleSetBody``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingruleset.html#cfn-gamelift-matchmakingruleset-rulesetbody
        """
        return jsii.get(self, "ruleSetBody")

    @rule_set_body.setter # type: ignore
    def rule_set_body(self, value: builtins.str) -> None:
        jsii.set(self, "ruleSetBody", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-gamelift.CfnMatchmakingRuleSetProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "rule_set_body": "ruleSetBody"},
)
class CfnMatchmakingRuleSetProps:
    def __init__(self, *, name: builtins.str, rule_set_body: builtins.str) -> None:
        """Properties for defining a ``AWS::GameLift::MatchmakingRuleSet``.

        :param name: ``AWS::GameLift::MatchmakingRuleSet.Name``.
        :param rule_set_body: ``AWS::GameLift::MatchmakingRuleSet.RuleSetBody``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingruleset.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "rule_set_body": rule_set_body,
        }

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::GameLift::MatchmakingRuleSet.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingruleset.html#cfn-gamelift-matchmakingruleset-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def rule_set_body(self) -> builtins.str:
        """``AWS::GameLift::MatchmakingRuleSet.RuleSetBody``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-matchmakingruleset.html#cfn-gamelift-matchmakingruleset-rulesetbody
        """
        result = self._values.get("rule_set_body")
        assert result is not None, "Required property 'rule_set_body' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMatchmakingRuleSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnScript(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-gamelift.CfnScript",
):
    """A CloudFormation ``AWS::GameLift::Script``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html
    :cloudformationResource: AWS::GameLift::Script
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        storage_location: typing.Union[aws_cdk.core.IResolvable, "CfnScript.S3LocationProperty"],
        name: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::GameLift::Script``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param storage_location: ``AWS::GameLift::Script.StorageLocation``.
        :param name: ``AWS::GameLift::Script.Name``.
        :param version: ``AWS::GameLift::Script.Version``.
        """
        props = CfnScriptProps(
            storage_location=storage_location, name=name, version=version
        )

        jsii.create(CfnScript, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        """
        :cloudformationAttribute: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="storageLocation")
    def storage_location(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnScript.S3LocationProperty"]:
        """``AWS::GameLift::Script.StorageLocation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html#cfn-gamelift-script-storagelocation
        """
        return jsii.get(self, "storageLocation")

    @storage_location.setter # type: ignore
    def storage_location(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnScript.S3LocationProperty"],
    ) -> None:
        jsii.set(self, "storageLocation", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Script.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html#cfn-gamelift-script-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Script.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html#cfn-gamelift-script-version
        """
        return jsii.get(self, "version")

    @version.setter # type: ignore
    def version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-gamelift.CfnScript.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key": "key",
            "role_arn": "roleArn",
            "object_version": "objectVersion",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            role_arn: builtins.str,
            object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket: ``CfnScript.S3LocationProperty.Bucket``.
            :param key: ``CfnScript.S3LocationProperty.Key``.
            :param role_arn: ``CfnScript.S3LocationProperty.RoleArn``.
            :param object_version: ``CfnScript.S3LocationProperty.ObjectVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-script-s3location.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
                "key": key,
                "role_arn": role_arn,
            }
            if object_version is not None:
                self._values["object_version"] = object_version

        @builtins.property
        def bucket(self) -> builtins.str:
            """``CfnScript.S3LocationProperty.Bucket``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-script-s3location.html#cfn-gamelift-script-s3location-bucket
            """
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return result

        @builtins.property
        def key(self) -> builtins.str:
            """``CfnScript.S3LocationProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-script-s3location.html#cfn-gamelift-script-s3location-key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def role_arn(self) -> builtins.str:
            """``CfnScript.S3LocationProperty.RoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-script-s3location.html#cfn-gamelift-script-s3location-rolearn
            """
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return result

        @builtins.property
        def object_version(self) -> typing.Optional[builtins.str]:
            """``CfnScript.S3LocationProperty.ObjectVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-script-s3location.html#cfn-gamelift-script-s3location-objectversion
            """
            result = self._values.get("object_version")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-gamelift.CfnScriptProps",
    jsii_struct_bases=[],
    name_mapping={
        "storage_location": "storageLocation",
        "name": "name",
        "version": "version",
    },
)
class CfnScriptProps:
    def __init__(
        self,
        *,
        storage_location: typing.Union[aws_cdk.core.IResolvable, CfnScript.S3LocationProperty],
        name: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::GameLift::Script``.

        :param storage_location: ``AWS::GameLift::Script.StorageLocation``.
        :param name: ``AWS::GameLift::Script.Name``.
        :param version: ``AWS::GameLift::Script.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "storage_location": storage_location,
        }
        if name is not None:
            self._values["name"] = name
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def storage_location(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnScript.S3LocationProperty]:
        """``AWS::GameLift::Script.StorageLocation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html#cfn-gamelift-script-storagelocation
        """
        result = self._values.get("storage_location")
        assert result is not None, "Required property 'storage_location' is missing"
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Script.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html#cfn-gamelift-script-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        """``AWS::GameLift::Script.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-script.html#cfn-gamelift-script-version
        """
        result = self._values.get("version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScriptProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAlias",
    "CfnAliasProps",
    "CfnBuild",
    "CfnBuildProps",
    "CfnFleet",
    "CfnFleetProps",
    "CfnGameServerGroup",
    "CfnGameServerGroupProps",
    "CfnGameSessionQueue",
    "CfnGameSessionQueueProps",
    "CfnMatchmakingConfiguration",
    "CfnMatchmakingConfigurationProps",
    "CfnMatchmakingRuleSet",
    "CfnMatchmakingRuleSetProps",
    "CfnScript",
    "CfnScriptProps",
]

publication.publish()
