import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverEndpoint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverEndpoint",
):
    """A CloudFormation ``AWS::Route53Resolver::ResolverEndpoint``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html
    :cloudformationResource: AWS::Route53Resolver::ResolverEndpoint
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        direction: builtins.str,
        ip_addresses: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverEndpoint.IpAddressRequestProperty", _IResolvable_a771d0ef]]],
        security_group_ids: typing.List[builtins.str],
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::Route53Resolver::ResolverEndpoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param direction: ``AWS::Route53Resolver::ResolverEndpoint.Direction``.
        :param ip_addresses: ``AWS::Route53Resolver::ResolverEndpoint.IpAddresses``.
        :param security_group_ids: ``AWS::Route53Resolver::ResolverEndpoint.SecurityGroupIds``.
        :param name: ``AWS::Route53Resolver::ResolverEndpoint.Name``.
        :param tags: ``AWS::Route53Resolver::ResolverEndpoint.Tags``.
        """
        props = CfnResolverEndpointProps(
            direction=direction,
            ip_addresses=ip_addresses,
            security_group_ids=security_group_ids,
            name=name,
            tags=tags,
        )

        jsii.create(CfnResolverEndpoint, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
    @jsii.member(jsii_name="attrDirection")
    def attr_direction(self) -> builtins.str:
        """
        :cloudformationAttribute: Direction
        """
        return jsii.get(self, "attrDirection")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrHostVpcId")
    def attr_host_vpc_id(self) -> builtins.str:
        """
        :cloudformationAttribute: HostVPCId
        """
        return jsii.get(self, "attrHostVpcId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrIpAddressCount")
    def attr_ip_address_count(self) -> builtins.str:
        """
        :cloudformationAttribute: IpAddressCount
        """
        return jsii.get(self, "attrIpAddressCount")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        """
        :cloudformationAttribute: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrResolverEndpointId")
    def attr_resolver_endpoint_id(self) -> builtins.str:
        """
        :cloudformationAttribute: ResolverEndpointId
        """
        return jsii.get(self, "attrResolverEndpointId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::Route53Resolver::ResolverEndpoint.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        """``AWS::Route53Resolver::ResolverEndpoint.Direction``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-direction
        """
        return jsii.get(self, "direction")

    @direction.setter # type: ignore
    def direction(self, value: builtins.str) -> None:
        jsii.set(self, "direction", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverEndpoint.IpAddressRequestProperty", _IResolvable_a771d0ef]]]:
        """``AWS::Route53Resolver::ResolverEndpoint.IpAddresses``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-ipaddresses
        """
        return jsii.get(self, "ipAddresses")

    @ip_addresses.setter # type: ignore
    def ip_addresses(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverEndpoint.IpAddressRequestProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "ipAddresses", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        """``AWS::Route53Resolver::ResolverEndpoint.SecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-securitygroupids
        """
        return jsii.get(self, "securityGroupIds")

    @security_group_ids.setter # type: ignore
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "securityGroupIds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverEndpoint.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_route53resolver.CfnResolverEndpoint.IpAddressRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"subnet_id": "subnetId", "ip": "ip"},
    )
    class IpAddressRequestProperty:
        def __init__(
            self,
            *,
            subnet_id: builtins.str,
            ip: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param subnet_id: ``CfnResolverEndpoint.IpAddressRequestProperty.SubnetId``.
            :param ip: ``CfnResolverEndpoint.IpAddressRequestProperty.Ip``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverendpoint-ipaddressrequest.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "subnet_id": subnet_id,
            }
            if ip is not None:
                self._values["ip"] = ip

        @builtins.property
        def subnet_id(self) -> builtins.str:
            """``CfnResolverEndpoint.IpAddressRequestProperty.SubnetId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverendpoint-ipaddressrequest.html#cfn-route53resolver-resolverendpoint-ipaddressrequest-subnetid
            """
            result = self._values.get("subnet_id")
            assert result is not None, "Required property 'subnet_id' is missing"
            return result

        @builtins.property
        def ip(self) -> typing.Optional[builtins.str]:
            """``CfnResolverEndpoint.IpAddressRequestProperty.Ip``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverendpoint-ipaddressrequest.html#cfn-route53resolver-resolverendpoint-ipaddressrequest-ip
            """
            result = self._values.get("ip")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IpAddressRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "direction": "direction",
        "ip_addresses": "ipAddresses",
        "security_group_ids": "securityGroupIds",
        "name": "name",
        "tags": "tags",
    },
)
class CfnResolverEndpointProps:
    def __init__(
        self,
        *,
        direction: builtins.str,
        ip_addresses: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResolverEndpoint.IpAddressRequestProperty, _IResolvable_a771d0ef]]],
        security_group_ids: typing.List[builtins.str],
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Route53Resolver::ResolverEndpoint``.

        :param direction: ``AWS::Route53Resolver::ResolverEndpoint.Direction``.
        :param ip_addresses: ``AWS::Route53Resolver::ResolverEndpoint.IpAddresses``.
        :param security_group_ids: ``AWS::Route53Resolver::ResolverEndpoint.SecurityGroupIds``.
        :param name: ``AWS::Route53Resolver::ResolverEndpoint.Name``.
        :param tags: ``AWS::Route53Resolver::ResolverEndpoint.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "direction": direction,
            "ip_addresses": ip_addresses,
            "security_group_ids": security_group_ids,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def direction(self) -> builtins.str:
        """``AWS::Route53Resolver::ResolverEndpoint.Direction``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-direction
        """
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return result

    @builtins.property
    def ip_addresses(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResolverEndpoint.IpAddressRequestProperty, _IResolvable_a771d0ef]]]:
        """``AWS::Route53Resolver::ResolverEndpoint.IpAddresses``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-ipaddresses
        """
        result = self._values.get("ip_addresses")
        assert result is not None, "Required property 'ip_addresses' is missing"
        return result

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        """``AWS::Route53Resolver::ResolverEndpoint.SecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-securitygroupids
        """
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverEndpoint.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::Route53Resolver::ResolverEndpoint.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverQueryLoggingConfig(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverQueryLoggingConfig",
):
    """A CloudFormation ``AWS::Route53Resolver::ResolverQueryLoggingConfig``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html
    :cloudformationResource: AWS::Route53Resolver::ResolverQueryLoggingConfig
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        destination_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Route53Resolver::ResolverQueryLoggingConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_arn: ``AWS::Route53Resolver::ResolverQueryLoggingConfig.DestinationArn``.
        :param name: ``AWS::Route53Resolver::ResolverQueryLoggingConfig.Name``.
        """
        props = CfnResolverQueryLoggingConfigProps(
            destination_arn=destination_arn, name=name
        )

        jsii.create(CfnResolverQueryLoggingConfig, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
    @jsii.member(jsii_name="attrAssociationCount")
    def attr_association_count(self) -> jsii.Number:
        """
        :cloudformationAttribute: AssociationCount
        """
        return jsii.get(self, "attrAssociationCount")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        """
        :cloudformationAttribute: CreationTime
        """
        return jsii.get(self, "attrCreationTime")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrCreatorRequestId")
    def attr_creator_request_id(self) -> builtins.str:
        """
        :cloudformationAttribute: CreatorRequestId
        """
        return jsii.get(self, "attrCreatorRequestId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        """
        :cloudformationAttribute: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrOwnerId")
    def attr_owner_id(self) -> builtins.str:
        """
        :cloudformationAttribute: OwnerId
        """
        return jsii.get(self, "attrOwnerId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrShareStatus")
    def attr_share_status(self) -> builtins.str:
        """
        :cloudformationAttribute: ShareStatus
        """
        return jsii.get(self, "attrShareStatus")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        """
        :cloudformationAttribute: Status
        """
        return jsii.get(self, "attrStatus")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverQueryLoggingConfig.DestinationArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html#cfn-route53resolver-resolverqueryloggingconfig-destinationarn
        """
        return jsii.get(self, "destinationArn")

    @destination_arn.setter # type: ignore
    def destination_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "destinationArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverQueryLoggingConfig.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html#cfn-route53resolver-resolverqueryloggingconfig-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverQueryLoggingConfigAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverQueryLoggingConfigAssociation",
):
    """A CloudFormation ``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html
    :cloudformationResource: AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        resolver_query_log_config_id: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resolver_query_log_config_id: ``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation.ResolverQueryLogConfigId``.
        :param resource_id: ``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation.ResourceId``.
        """
        props = CfnResolverQueryLoggingConfigAssociationProps(
            resolver_query_log_config_id=resolver_query_log_config_id,
            resource_id=resource_id,
        )

        jsii.create(CfnResolverQueryLoggingConfigAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        """
        :cloudformationAttribute: CreationTime
        """
        return jsii.get(self, "attrCreationTime")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrError")
    def attr_error(self) -> builtins.str:
        """
        :cloudformationAttribute: Error
        """
        return jsii.get(self, "attrError")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrErrorMessage")
    def attr_error_message(self) -> builtins.str:
        """
        :cloudformationAttribute: ErrorMessage
        """
        return jsii.get(self, "attrErrorMessage")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        """
        :cloudformationAttribute: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        """
        :cloudformationAttribute: Status
        """
        return jsii.get(self, "attrStatus")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resolverQueryLogConfigId")
    def resolver_query_log_config_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation.ResolverQueryLogConfigId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html#cfn-route53resolver-resolverqueryloggingconfigassociation-resolverquerylogconfigid
        """
        return jsii.get(self, "resolverQueryLogConfigId")

    @resolver_query_log_config_id.setter # type: ignore
    def resolver_query_log_config_id(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "resolverQueryLogConfigId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation.ResourceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html#cfn-route53resolver-resolverqueryloggingconfigassociation-resourceid
        """
        return jsii.get(self, "resourceId")

    @resource_id.setter # type: ignore
    def resource_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "resourceId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverQueryLoggingConfigAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "resolver_query_log_config_id": "resolverQueryLogConfigId",
        "resource_id": "resourceId",
    },
)
class CfnResolverQueryLoggingConfigAssociationProps:
    def __init__(
        self,
        *,
        resolver_query_log_config_id: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation``.

        :param resolver_query_log_config_id: ``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation.ResolverQueryLogConfigId``.
        :param resource_id: ``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation.ResourceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if resolver_query_log_config_id is not None:
            self._values["resolver_query_log_config_id"] = resolver_query_log_config_id
        if resource_id is not None:
            self._values["resource_id"] = resource_id

    @builtins.property
    def resolver_query_log_config_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation.ResolverQueryLogConfigId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html#cfn-route53resolver-resolverqueryloggingconfigassociation-resolverquerylogconfigid
        """
        result = self._values.get("resolver_query_log_config_id")
        return result

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation.ResourceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html#cfn-route53resolver-resolverqueryloggingconfigassociation-resourceid
        """
        result = self._values.get("resource_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverQueryLoggingConfigAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverQueryLoggingConfigProps",
    jsii_struct_bases=[],
    name_mapping={"destination_arn": "destinationArn", "name": "name"},
)
class CfnResolverQueryLoggingConfigProps:
    def __init__(
        self,
        *,
        destination_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Route53Resolver::ResolverQueryLoggingConfig``.

        :param destination_arn: ``AWS::Route53Resolver::ResolverQueryLoggingConfig.DestinationArn``.
        :param name: ``AWS::Route53Resolver::ResolverQueryLoggingConfig.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if destination_arn is not None:
            self._values["destination_arn"] = destination_arn
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def destination_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverQueryLoggingConfig.DestinationArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html#cfn-route53resolver-resolverqueryloggingconfig-destinationarn
        """
        result = self._values.get("destination_arn")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverQueryLoggingConfig.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html#cfn-route53resolver-resolverqueryloggingconfig-name
        """
        result = self._values.get("name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverQueryLoggingConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverRule(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverRule",
):
    """A CloudFormation ``AWS::Route53Resolver::ResolverRule``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html
    :cloudformationResource: AWS::Route53Resolver::ResolverRule
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        domain_name: builtins.str,
        rule_type: builtins.str,
        name: typing.Optional[builtins.str] = None,
        resolver_endpoint_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        target_ips: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverRule.TargetAddressProperty", _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        """Create a new ``AWS::Route53Resolver::ResolverRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: ``AWS::Route53Resolver::ResolverRule.DomainName``.
        :param rule_type: ``AWS::Route53Resolver::ResolverRule.RuleType``.
        :param name: ``AWS::Route53Resolver::ResolverRule.Name``.
        :param resolver_endpoint_id: ``AWS::Route53Resolver::ResolverRule.ResolverEndpointId``.
        :param tags: ``AWS::Route53Resolver::ResolverRule.Tags``.
        :param target_ips: ``AWS::Route53Resolver::ResolverRule.TargetIps``.
        """
        props = CfnResolverRuleProps(
            domain_name=domain_name,
            rule_type=rule_type,
            name=name,
            resolver_endpoint_id=resolver_endpoint_id,
            tags=tags,
            target_ips=target_ips,
        )

        jsii.create(CfnResolverRule, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        """
        :cloudformationAttribute: DomainName
        """
        return jsii.get(self, "attrDomainName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        """
        :cloudformationAttribute: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrResolverEndpointId")
    def attr_resolver_endpoint_id(self) -> builtins.str:
        """
        :cloudformationAttribute: ResolverEndpointId
        """
        return jsii.get(self, "attrResolverEndpointId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrResolverRuleId")
    def attr_resolver_rule_id(self) -> builtins.str:
        """
        :cloudformationAttribute: ResolverRuleId
        """
        return jsii.get(self, "attrResolverRuleId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrTargetIps")
    def attr_target_ips(self) -> builtins.str:
        """
        :cloudformationAttribute: TargetIps
        """
        return jsii.get(self, "attrTargetIps")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::Route53Resolver::ResolverRule.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        """``AWS::Route53Resolver::ResolverRule.DomainName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter # type: ignore
    def domain_name(self, value: builtins.str) -> None:
        jsii.set(self, "domainName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleType")
    def rule_type(self) -> builtins.str:
        """``AWS::Route53Resolver::ResolverRule.RuleType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-ruletype
        """
        return jsii.get(self, "ruleType")

    @rule_type.setter # type: ignore
    def rule_type(self, value: builtins.str) -> None:
        jsii.set(self, "ruleType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverRule.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resolverEndpointId")
    def resolver_endpoint_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverRule.ResolverEndpointId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-resolverendpointid
        """
        return jsii.get(self, "resolverEndpointId")

    @resolver_endpoint_id.setter # type: ignore
    def resolver_endpoint_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "resolverEndpointId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetIps")
    def target_ips(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverRule.TargetAddressProperty", _IResolvable_a771d0ef]]]]:
        """``AWS::Route53Resolver::ResolverRule.TargetIps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-targetips
        """
        return jsii.get(self, "targetIps")

    @target_ips.setter # type: ignore
    def target_ips(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverRule.TargetAddressProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "targetIps", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_route53resolver.CfnResolverRule.TargetAddressProperty",
        jsii_struct_bases=[],
        name_mapping={"ip": "ip", "port": "port"},
    )
    class TargetAddressProperty:
        def __init__(
            self,
            *,
            ip: builtins.str,
            port: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param ip: ``CfnResolverRule.TargetAddressProperty.Ip``.
            :param port: ``CfnResolverRule.TargetAddressProperty.Port``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "ip": ip,
            }
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def ip(self) -> builtins.str:
            """``CfnResolverRule.TargetAddressProperty.Ip``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html#cfn-route53resolver-resolverrule-targetaddress-ip
            """
            result = self._values.get("ip")
            assert result is not None, "Required property 'ip' is missing"
            return result

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            """``CfnResolverRule.TargetAddressProperty.Port``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html#cfn-route53resolver-resolverrule-targetaddress-port
            """
            result = self._values.get("port")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetAddressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverRuleAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverRuleAssociation",
):
    """A CloudFormation ``AWS::Route53Resolver::ResolverRuleAssociation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html
    :cloudformationResource: AWS::Route53Resolver::ResolverRuleAssociation
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        resolver_rule_id: builtins.str,
        vpc_id: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Route53Resolver::ResolverRuleAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resolver_rule_id: ``AWS::Route53Resolver::ResolverRuleAssociation.ResolverRuleId``.
        :param vpc_id: ``AWS::Route53Resolver::ResolverRuleAssociation.VPCId``.
        :param name: ``AWS::Route53Resolver::ResolverRuleAssociation.Name``.
        """
        props = CfnResolverRuleAssociationProps(
            resolver_rule_id=resolver_rule_id, vpc_id=vpc_id, name=name
        )

        jsii.create(CfnResolverRuleAssociation, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
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
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        """
        :cloudformationAttribute: Name
        """
        return jsii.get(self, "attrName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrResolverRuleAssociationId")
    def attr_resolver_rule_association_id(self) -> builtins.str:
        """
        :cloudformationAttribute: ResolverRuleAssociationId
        """
        return jsii.get(self, "attrResolverRuleAssociationId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrResolverRuleId")
    def attr_resolver_rule_id(self) -> builtins.str:
        """
        :cloudformationAttribute: ResolverRuleId
        """
        return jsii.get(self, "attrResolverRuleId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrVpcId")
    def attr_vpc_id(self) -> builtins.str:
        """
        :cloudformationAttribute: VPCId
        """
        return jsii.get(self, "attrVpcId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resolverRuleId")
    def resolver_rule_id(self) -> builtins.str:
        """``AWS::Route53Resolver::ResolverRuleAssociation.ResolverRuleId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-resolverruleid
        """
        return jsii.get(self, "resolverRuleId")

    @resolver_rule_id.setter # type: ignore
    def resolver_rule_id(self, value: builtins.str) -> None:
        jsii.set(self, "resolverRuleId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        """``AWS::Route53Resolver::ResolverRuleAssociation.VPCId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-vpcid
        """
        return jsii.get(self, "vpcId")

    @vpc_id.setter # type: ignore
    def vpc_id(self, value: builtins.str) -> None:
        jsii.set(self, "vpcId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverRuleAssociation.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverRuleAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "resolver_rule_id": "resolverRuleId",
        "vpc_id": "vpcId",
        "name": "name",
    },
)
class CfnResolverRuleAssociationProps:
    def __init__(
        self,
        *,
        resolver_rule_id: builtins.str,
        vpc_id: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Route53Resolver::ResolverRuleAssociation``.

        :param resolver_rule_id: ``AWS::Route53Resolver::ResolverRuleAssociation.ResolverRuleId``.
        :param vpc_id: ``AWS::Route53Resolver::ResolverRuleAssociation.VPCId``.
        :param name: ``AWS::Route53Resolver::ResolverRuleAssociation.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "resolver_rule_id": resolver_rule_id,
            "vpc_id": vpc_id,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def resolver_rule_id(self) -> builtins.str:
        """``AWS::Route53Resolver::ResolverRuleAssociation.ResolverRuleId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-resolverruleid
        """
        result = self._values.get("resolver_rule_id")
        assert result is not None, "Required property 'resolver_rule_id' is missing"
        return result

    @builtins.property
    def vpc_id(self) -> builtins.str:
        """``AWS::Route53Resolver::ResolverRuleAssociation.VPCId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-vpcid
        """
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverRuleAssociation.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-name
        """
        result = self._values.get("name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverRuleAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "rule_type": "ruleType",
        "name": "name",
        "resolver_endpoint_id": "resolverEndpointId",
        "tags": "tags",
        "target_ips": "targetIps",
    },
)
class CfnResolverRuleProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        rule_type: builtins.str,
        name: typing.Optional[builtins.str] = None,
        resolver_endpoint_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        target_ips: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResolverRule.TargetAddressProperty, _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Route53Resolver::ResolverRule``.

        :param domain_name: ``AWS::Route53Resolver::ResolverRule.DomainName``.
        :param rule_type: ``AWS::Route53Resolver::ResolverRule.RuleType``.
        :param name: ``AWS::Route53Resolver::ResolverRule.Name``.
        :param resolver_endpoint_id: ``AWS::Route53Resolver::ResolverRule.ResolverEndpointId``.
        :param tags: ``AWS::Route53Resolver::ResolverRule.Tags``.
        :param target_ips: ``AWS::Route53Resolver::ResolverRule.TargetIps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
            "rule_type": rule_type,
        }
        if name is not None:
            self._values["name"] = name
        if resolver_endpoint_id is not None:
            self._values["resolver_endpoint_id"] = resolver_endpoint_id
        if tags is not None:
            self._values["tags"] = tags
        if target_ips is not None:
            self._values["target_ips"] = target_ips

    @builtins.property
    def domain_name(self) -> builtins.str:
        """``AWS::Route53Resolver::ResolverRule.DomainName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-domainname
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    @builtins.property
    def rule_type(self) -> builtins.str:
        """``AWS::Route53Resolver::ResolverRule.RuleType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-ruletype
        """
        result = self._values.get("rule_type")
        assert result is not None, "Required property 'rule_type' is missing"
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverRule.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-name
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def resolver_endpoint_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Route53Resolver::ResolverRule.ResolverEndpointId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-resolverendpointid
        """
        result = self._values.get("resolver_endpoint_id")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::Route53Resolver::ResolverRule.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def target_ips(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResolverRule.TargetAddressProperty, _IResolvable_a771d0ef]]]]:
        """``AWS::Route53Resolver::ResolverRule.TargetIps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-targetips
        """
        result = self._values.get("target_ips")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnResolverEndpoint",
    "CfnResolverEndpointProps",
    "CfnResolverQueryLoggingConfig",
    "CfnResolverQueryLoggingConfigAssociation",
    "CfnResolverQueryLoggingConfigAssociationProps",
    "CfnResolverQueryLoggingConfigProps",
    "CfnResolverRule",
    "CfnResolverRuleAssociation",
    "CfnResolverRuleAssociationProps",
    "CfnResolverRuleProps",
]

publication.publish()
