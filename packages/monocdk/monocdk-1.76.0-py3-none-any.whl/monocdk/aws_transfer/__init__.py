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
class CfnServer(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_transfer.CfnServer",
):
    """A CloudFormation ``AWS::Transfer::Server``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html
    :cloudformationResource: AWS::Transfer::Server
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        certificate: typing.Optional[builtins.str] = None,
        endpoint_details: typing.Optional[typing.Union["CfnServer.EndpointDetailsProperty", _IResolvable_a771d0ef]] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        identity_provider_details: typing.Optional[typing.Union["CfnServer.IdentityProviderDetailsProperty", _IResolvable_a771d0ef]] = None,
        identity_provider_type: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.List[builtins.str]] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::Transfer::Server``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate: ``AWS::Transfer::Server.Certificate``.
        :param endpoint_details: ``AWS::Transfer::Server.EndpointDetails``.
        :param endpoint_type: ``AWS::Transfer::Server.EndpointType``.
        :param identity_provider_details: ``AWS::Transfer::Server.IdentityProviderDetails``.
        :param identity_provider_type: ``AWS::Transfer::Server.IdentityProviderType``.
        :param logging_role: ``AWS::Transfer::Server.LoggingRole``.
        :param protocols: ``AWS::Transfer::Server.Protocols``.
        :param security_policy_name: ``AWS::Transfer::Server.SecurityPolicyName``.
        :param tags: ``AWS::Transfer::Server.Tags``.
        """
        props = CfnServerProps(
            certificate=certificate,
            endpoint_details=endpoint_details,
            endpoint_type=endpoint_type,
            identity_provider_details=identity_provider_details,
            identity_provider_type=identity_provider_type,
            logging_role=logging_role,
            protocols=protocols,
            security_policy_name=security_policy_name,
            tags=tags,
        )

        jsii.create(CfnServer, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrServerId")
    def attr_server_id(self) -> builtins.str:
        """
        :cloudformationAttribute: ServerId
        """
        return jsii.get(self, "attrServerId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::Transfer::Server.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::Server.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-certificate
        """
        return jsii.get(self, "certificate")

    @certificate.setter # type: ignore
    def certificate(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "certificate", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpointDetails")
    def endpoint_details(
        self,
    ) -> typing.Optional[typing.Union["CfnServer.EndpointDetailsProperty", _IResolvable_a771d0ef]]:
        """``AWS::Transfer::Server.EndpointDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointdetails
        """
        return jsii.get(self, "endpointDetails")

    @endpoint_details.setter # type: ignore
    def endpoint_details(
        self,
        value: typing.Optional[typing.Union["CfnServer.EndpointDetailsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "endpointDetails", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::Server.EndpointType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointtype
        """
        return jsii.get(self, "endpointType")

    @endpoint_type.setter # type: ignore
    def endpoint_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "endpointType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identityProviderDetails")
    def identity_provider_details(
        self,
    ) -> typing.Optional[typing.Union["CfnServer.IdentityProviderDetailsProperty", _IResolvable_a771d0ef]]:
        """``AWS::Transfer::Server.IdentityProviderDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityproviderdetails
        """
        return jsii.get(self, "identityProviderDetails")

    @identity_provider_details.setter # type: ignore
    def identity_provider_details(
        self,
        value: typing.Optional[typing.Union["CfnServer.IdentityProviderDetailsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "identityProviderDetails", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="identityProviderType")
    def identity_provider_type(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::Server.IdentityProviderType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityprovidertype
        """
        return jsii.get(self, "identityProviderType")

    @identity_provider_type.setter # type: ignore
    def identity_provider_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "identityProviderType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loggingRole")
    def logging_role(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::Server.LoggingRole``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-loggingrole
        """
        return jsii.get(self, "loggingRole")

    @logging_role.setter # type: ignore
    def logging_role(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "loggingRole", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Transfer::Server.Protocols``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-protocols
        """
        return jsii.get(self, "protocols")

    @protocols.setter # type: ignore
    def protocols(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "protocols", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityPolicyName")
    def security_policy_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::Server.SecurityPolicyName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-securitypolicyname
        """
        return jsii.get(self, "securityPolicyName")

    @security_policy_name.setter # type: ignore
    def security_policy_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "securityPolicyName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnServer.EndpointDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address_allocation_ids": "addressAllocationIds",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
            "vpc_endpoint_id": "vpcEndpointId",
            "vpc_id": "vpcId",
        },
    )
    class EndpointDetailsProperty:
        def __init__(
            self,
            *,
            address_allocation_ids: typing.Optional[typing.List[builtins.str]] = None,
            security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.List[builtins.str]] = None,
            vpc_endpoint_id: typing.Optional[builtins.str] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param address_allocation_ids: ``CfnServer.EndpointDetailsProperty.AddressAllocationIds``.
            :param security_group_ids: ``CfnServer.EndpointDetailsProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnServer.EndpointDetailsProperty.SubnetIds``.
            :param vpc_endpoint_id: ``CfnServer.EndpointDetailsProperty.VpcEndpointId``.
            :param vpc_id: ``CfnServer.EndpointDetailsProperty.VpcId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if address_allocation_ids is not None:
                self._values["address_allocation_ids"] = address_allocation_ids
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids
            if vpc_endpoint_id is not None:
                self._values["vpc_endpoint_id"] = vpc_endpoint_id
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def address_allocation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnServer.EndpointDetailsProperty.AddressAllocationIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-addressallocationids
            """
            result = self._values.get("address_allocation_ids")
            return result

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnServer.EndpointDetailsProperty.SecurityGroupIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-securitygroupids
            """
            result = self._values.get("security_group_ids")
            return result

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnServer.EndpointDetailsProperty.SubnetIds``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-subnetids
            """
            result = self._values.get("subnet_ids")
            return result

        @builtins.property
        def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
            """``CfnServer.EndpointDetailsProperty.VpcEndpointId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-vpcendpointid
            """
            result = self._values.get("vpc_endpoint_id")
            return result

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            """``CfnServer.EndpointDetailsProperty.VpcId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-vpcid
            """
            result = self._values.get("vpc_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnServer.IdentityProviderDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"invocation_role": "invocationRole", "url": "url"},
    )
    class IdentityProviderDetailsProperty:
        def __init__(self, *, invocation_role: builtins.str, url: builtins.str) -> None:
            """
            :param invocation_role: ``CfnServer.IdentityProviderDetailsProperty.InvocationRole``.
            :param url: ``CfnServer.IdentityProviderDetailsProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "invocation_role": invocation_role,
                "url": url,
            }

        @builtins.property
        def invocation_role(self) -> builtins.str:
            """``CfnServer.IdentityProviderDetailsProperty.InvocationRole``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-invocationrole
            """
            result = self._values.get("invocation_role")
            assert result is not None, "Required property 'invocation_role' is missing"
            return result

        @builtins.property
        def url(self) -> builtins.str:
            """``CfnServer.IdentityProviderDetailsProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-url
            """
            result = self._values.get("url")
            assert result is not None, "Required property 'url' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentityProviderDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_transfer.CfnServerProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "endpoint_details": "endpointDetails",
        "endpoint_type": "endpointType",
        "identity_provider_details": "identityProviderDetails",
        "identity_provider_type": "identityProviderType",
        "logging_role": "loggingRole",
        "protocols": "protocols",
        "security_policy_name": "securityPolicyName",
        "tags": "tags",
    },
)
class CfnServerProps:
    def __init__(
        self,
        *,
        certificate: typing.Optional[builtins.str] = None,
        endpoint_details: typing.Optional[typing.Union[CfnServer.EndpointDetailsProperty, _IResolvable_a771d0ef]] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        identity_provider_details: typing.Optional[typing.Union[CfnServer.IdentityProviderDetailsProperty, _IResolvable_a771d0ef]] = None,
        identity_provider_type: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.List[builtins.str]] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Transfer::Server``.

        :param certificate: ``AWS::Transfer::Server.Certificate``.
        :param endpoint_details: ``AWS::Transfer::Server.EndpointDetails``.
        :param endpoint_type: ``AWS::Transfer::Server.EndpointType``.
        :param identity_provider_details: ``AWS::Transfer::Server.IdentityProviderDetails``.
        :param identity_provider_type: ``AWS::Transfer::Server.IdentityProviderType``.
        :param logging_role: ``AWS::Transfer::Server.LoggingRole``.
        :param protocols: ``AWS::Transfer::Server.Protocols``.
        :param security_policy_name: ``AWS::Transfer::Server.SecurityPolicyName``.
        :param tags: ``AWS::Transfer::Server.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if certificate is not None:
            self._values["certificate"] = certificate
        if endpoint_details is not None:
            self._values["endpoint_details"] = endpoint_details
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if identity_provider_details is not None:
            self._values["identity_provider_details"] = identity_provider_details
        if identity_provider_type is not None:
            self._values["identity_provider_type"] = identity_provider_type
        if logging_role is not None:
            self._values["logging_role"] = logging_role
        if protocols is not None:
            self._values["protocols"] = protocols
        if security_policy_name is not None:
            self._values["security_policy_name"] = security_policy_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::Server.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-certificate
        """
        result = self._values.get("certificate")
        return result

    @builtins.property
    def endpoint_details(
        self,
    ) -> typing.Optional[typing.Union[CfnServer.EndpointDetailsProperty, _IResolvable_a771d0ef]]:
        """``AWS::Transfer::Server.EndpointDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointdetails
        """
        result = self._values.get("endpoint_details")
        return result

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::Server.EndpointType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointtype
        """
        result = self._values.get("endpoint_type")
        return result

    @builtins.property
    def identity_provider_details(
        self,
    ) -> typing.Optional[typing.Union[CfnServer.IdentityProviderDetailsProperty, _IResolvable_a771d0ef]]:
        """``AWS::Transfer::Server.IdentityProviderDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityproviderdetails
        """
        result = self._values.get("identity_provider_details")
        return result

    @builtins.property
    def identity_provider_type(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::Server.IdentityProviderType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityprovidertype
        """
        result = self._values.get("identity_provider_type")
        return result

    @builtins.property
    def logging_role(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::Server.LoggingRole``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-loggingrole
        """
        result = self._values.get("logging_role")
        return result

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Transfer::Server.Protocols``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-protocols
        """
        result = self._values.get("protocols")
        return result

    @builtins.property
    def security_policy_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::Server.SecurityPolicyName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-securitypolicyname
        """
        result = self._values.get("security_policy_name")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::Transfer::Server.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnUser(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_transfer.CfnUser",
):
    """A CloudFormation ``AWS::Transfer::User``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html
    :cloudformationResource: AWS::Transfer::User
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        role: builtins.str,
        server_id: builtins.str,
        user_name: builtins.str,
        home_directory: typing.Optional[builtins.str] = None,
        home_directory_mappings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnUser.HomeDirectoryMapEntryProperty", _IResolvable_a771d0ef]]]] = None,
        home_directory_type: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        ssh_public_keys: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::Transfer::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param role: ``AWS::Transfer::User.Role``.
        :param server_id: ``AWS::Transfer::User.ServerId``.
        :param user_name: ``AWS::Transfer::User.UserName``.
        :param home_directory: ``AWS::Transfer::User.HomeDirectory``.
        :param home_directory_mappings: ``AWS::Transfer::User.HomeDirectoryMappings``.
        :param home_directory_type: ``AWS::Transfer::User.HomeDirectoryType``.
        :param policy: ``AWS::Transfer::User.Policy``.
        :param ssh_public_keys: ``AWS::Transfer::User.SshPublicKeys``.
        :param tags: ``AWS::Transfer::User.Tags``.
        """
        props = CfnUserProps(
            role=role,
            server_id=server_id,
            user_name=user_name,
            home_directory=home_directory,
            home_directory_mappings=home_directory_mappings,
            home_directory_type=home_directory_type,
            policy=policy,
            ssh_public_keys=ssh_public_keys,
            tags=tags,
        )

        jsii.create(CfnUser, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrServerId")
    def attr_server_id(self) -> builtins.str:
        """
        :cloudformationAttribute: ServerId
        """
        return jsii.get(self, "attrServerId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrUserName")
    def attr_user_name(self) -> builtins.str:
        """
        :cloudformationAttribute: UserName
        """
        return jsii.get(self, "attrUserName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::Transfer::User.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        """``AWS::Transfer::User.Role``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-role
        """
        return jsii.get(self, "role")

    @role.setter # type: ignore
    def role(self, value: builtins.str) -> None:
        jsii.set(self, "role", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serverId")
    def server_id(self) -> builtins.str:
        """``AWS::Transfer::User.ServerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-serverid
        """
        return jsii.get(self, "serverId")

    @server_id.setter # type: ignore
    def server_id(self, value: builtins.str) -> None:
        jsii.set(self, "serverId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        """``AWS::Transfer::User.UserName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-username
        """
        return jsii.get(self, "userName")

    @user_name.setter # type: ignore
    def user_name(self, value: builtins.str) -> None:
        jsii.set(self, "userName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="homeDirectory")
    def home_directory(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::User.HomeDirectory``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectory
        """
        return jsii.get(self, "homeDirectory")

    @home_directory.setter # type: ignore
    def home_directory(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "homeDirectory", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="homeDirectoryMappings")
    def home_directory_mappings(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnUser.HomeDirectoryMapEntryProperty", _IResolvable_a771d0ef]]]]:
        """``AWS::Transfer::User.HomeDirectoryMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorymappings
        """
        return jsii.get(self, "homeDirectoryMappings")

    @home_directory_mappings.setter # type: ignore
    def home_directory_mappings(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnUser.HomeDirectoryMapEntryProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "homeDirectoryMappings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="homeDirectoryType")
    def home_directory_type(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::User.HomeDirectoryType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorytype
        """
        return jsii.get(self, "homeDirectoryType")

    @home_directory_type.setter # type: ignore
    def home_directory_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "homeDirectoryType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::User.Policy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-policy
        """
        return jsii.get(self, "policy")

    @policy.setter # type: ignore
    def policy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "policy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sshPublicKeys")
    def ssh_public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Transfer::User.SshPublicKeys``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-sshpublickeys
        """
        return jsii.get(self, "sshPublicKeys")

    @ssh_public_keys.setter # type: ignore
    def ssh_public_keys(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "sshPublicKeys", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_transfer.CfnUser.HomeDirectoryMapEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"entry": "entry", "target": "target"},
    )
    class HomeDirectoryMapEntryProperty:
        def __init__(self, *, entry: builtins.str, target: builtins.str) -> None:
            """
            :param entry: ``CfnUser.HomeDirectoryMapEntryProperty.Entry``.
            :param target: ``CfnUser.HomeDirectoryMapEntryProperty.Target``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "entry": entry,
                "target": target,
            }

        @builtins.property
        def entry(self) -> builtins.str:
            """``CfnUser.HomeDirectoryMapEntryProperty.Entry``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html#cfn-transfer-user-homedirectorymapentry-entry
            """
            result = self._values.get("entry")
            assert result is not None, "Required property 'entry' is missing"
            return result

        @builtins.property
        def target(self) -> builtins.str:
            """``CfnUser.HomeDirectoryMapEntryProperty.Target``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html#cfn-transfer-user-homedirectorymapentry-target
            """
            result = self._values.get("target")
            assert result is not None, "Required property 'target' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HomeDirectoryMapEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_transfer.CfnUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "role": "role",
        "server_id": "serverId",
        "user_name": "userName",
        "home_directory": "homeDirectory",
        "home_directory_mappings": "homeDirectoryMappings",
        "home_directory_type": "homeDirectoryType",
        "policy": "policy",
        "ssh_public_keys": "sshPublicKeys",
        "tags": "tags",
    },
)
class CfnUserProps:
    def __init__(
        self,
        *,
        role: builtins.str,
        server_id: builtins.str,
        user_name: builtins.str,
        home_directory: typing.Optional[builtins.str] = None,
        home_directory_mappings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnUser.HomeDirectoryMapEntryProperty, _IResolvable_a771d0ef]]]] = None,
        home_directory_type: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        ssh_public_keys: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Transfer::User``.

        :param role: ``AWS::Transfer::User.Role``.
        :param server_id: ``AWS::Transfer::User.ServerId``.
        :param user_name: ``AWS::Transfer::User.UserName``.
        :param home_directory: ``AWS::Transfer::User.HomeDirectory``.
        :param home_directory_mappings: ``AWS::Transfer::User.HomeDirectoryMappings``.
        :param home_directory_type: ``AWS::Transfer::User.HomeDirectoryType``.
        :param policy: ``AWS::Transfer::User.Policy``.
        :param ssh_public_keys: ``AWS::Transfer::User.SshPublicKeys``.
        :param tags: ``AWS::Transfer::User.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "role": role,
            "server_id": server_id,
            "user_name": user_name,
        }
        if home_directory is not None:
            self._values["home_directory"] = home_directory
        if home_directory_mappings is not None:
            self._values["home_directory_mappings"] = home_directory_mappings
        if home_directory_type is not None:
            self._values["home_directory_type"] = home_directory_type
        if policy is not None:
            self._values["policy"] = policy
        if ssh_public_keys is not None:
            self._values["ssh_public_keys"] = ssh_public_keys
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def role(self) -> builtins.str:
        """``AWS::Transfer::User.Role``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-role
        """
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return result

    @builtins.property
    def server_id(self) -> builtins.str:
        """``AWS::Transfer::User.ServerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-serverid
        """
        result = self._values.get("server_id")
        assert result is not None, "Required property 'server_id' is missing"
        return result

    @builtins.property
    def user_name(self) -> builtins.str:
        """``AWS::Transfer::User.UserName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-username
        """
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return result

    @builtins.property
    def home_directory(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::User.HomeDirectory``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectory
        """
        result = self._values.get("home_directory")
        return result

    @builtins.property
    def home_directory_mappings(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnUser.HomeDirectoryMapEntryProperty, _IResolvable_a771d0ef]]]]:
        """``AWS::Transfer::User.HomeDirectoryMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorymappings
        """
        result = self._values.get("home_directory_mappings")
        return result

    @builtins.property
    def home_directory_type(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::User.HomeDirectoryType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorytype
        """
        result = self._values.get("home_directory_type")
        return result

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        """``AWS::Transfer::User.Policy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-policy
        """
        result = self._values.get("policy")
        return result

    @builtins.property
    def ssh_public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Transfer::User.SshPublicKeys``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-sshpublickeys
        """
        result = self._values.get("ssh_public_keys")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::Transfer::User.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-tags
        """
        result = self._values.get("tags")
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
    "CfnServer",
    "CfnServerProps",
    "CfnUser",
    "CfnUserProps",
]

publication.publish()
