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
class CfnFirewall(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_networkfirewall.CfnFirewall",
):
    """A CloudFormation ``AWS::NetworkFirewall::Firewall``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html
    :cloudformationResource: AWS::NetworkFirewall::Firewall
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        firewall_name: builtins.str,
        firewall_policy_arn: builtins.str,
        subnet_mappings: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewall.SubnetMappingProperty", _IResolvable_a771d0ef]]],
        vpc_id: builtins.str,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional["CfnFirewall.TagsProperty"] = None,
    ) -> None:
        """Create a new ``AWS::NetworkFirewall::Firewall``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param firewall_name: ``AWS::NetworkFirewall::Firewall.FirewallName``.
        :param firewall_policy_arn: ``AWS::NetworkFirewall::Firewall.FirewallPolicyArn``.
        :param subnet_mappings: ``AWS::NetworkFirewall::Firewall.SubnetMappings``.
        :param vpc_id: ``AWS::NetworkFirewall::Firewall.VpcId``.
        :param delete_protection: ``AWS::NetworkFirewall::Firewall.DeleteProtection``.
        :param description: ``AWS::NetworkFirewall::Firewall.Description``.
        :param firewall_policy_change_protection: ``AWS::NetworkFirewall::Firewall.FirewallPolicyChangeProtection``.
        :param subnet_change_protection: ``AWS::NetworkFirewall::Firewall.SubnetChangeProtection``.
        :param tags: ``AWS::NetworkFirewall::Firewall.Tags``.
        """
        props = CfnFirewallProps(
            firewall_name=firewall_name,
            firewall_policy_arn=firewall_policy_arn,
            subnet_mappings=subnet_mappings,
            vpc_id=vpc_id,
            delete_protection=delete_protection,
            description=description,
            firewall_policy_change_protection=firewall_policy_change_protection,
            subnet_change_protection=subnet_change_protection,
            tags=tags,
        )

        jsii.create(CfnFirewall, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrEndpointIds")
    def attr_endpoint_ids(self) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: EndpointIds
        """
        return jsii.get(self, "attrEndpointIds")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrFirewallArn")
    def attr_firewall_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: FirewallArn
        """
        return jsii.get(self, "attrFirewallArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrFirewallId")
    def attr_firewall_id(self) -> builtins.str:
        """
        :cloudformationAttribute: FirewallId
        """
        return jsii.get(self, "attrFirewallId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::NetworkFirewall::Firewall.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="firewallName")
    def firewall_name(self) -> builtins.str:
        """``AWS::NetworkFirewall::Firewall.FirewallName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallname
        """
        return jsii.get(self, "firewallName")

    @firewall_name.setter # type: ignore
    def firewall_name(self, value: builtins.str) -> None:
        jsii.set(self, "firewallName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="firewallPolicyArn")
    def firewall_policy_arn(self) -> builtins.str:
        """``AWS::NetworkFirewall::Firewall.FirewallPolicyArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicyarn
        """
        return jsii.get(self, "firewallPolicyArn")

    @firewall_policy_arn.setter # type: ignore
    def firewall_policy_arn(self, value: builtins.str) -> None:
        jsii.set(self, "firewallPolicyArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnetMappings")
    def subnet_mappings(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewall.SubnetMappingProperty", _IResolvable_a771d0ef]]]:
        """``AWS::NetworkFirewall::Firewall.SubnetMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetmappings
        """
        return jsii.get(self, "subnetMappings")

    @subnet_mappings.setter # type: ignore
    def subnet_mappings(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewall.SubnetMappingProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "subnetMappings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        """``AWS::NetworkFirewall::Firewall.VpcId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-vpcid
        """
        return jsii.get(self, "vpcId")

    @vpc_id.setter # type: ignore
    def vpc_id(self, value: builtins.str) -> None:
        jsii.set(self, "vpcId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deleteProtection")
    def delete_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::NetworkFirewall::Firewall.DeleteProtection``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-deleteprotection
        """
        return jsii.get(self, "deleteProtection")

    @delete_protection.setter # type: ignore
    def delete_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "deleteProtection", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkFirewall::Firewall.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="firewallPolicyChangeProtection")
    def firewall_policy_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::NetworkFirewall::Firewall.FirewallPolicyChangeProtection``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicychangeprotection
        """
        return jsii.get(self, "firewallPolicyChangeProtection")

    @firewall_policy_change_protection.setter # type: ignore
    def firewall_policy_change_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "firewallPolicyChangeProtection", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnetChangeProtection")
    def subnet_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::NetworkFirewall::Firewall.SubnetChangeProtection``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetchangeprotection
        """
        return jsii.get(self, "subnetChangeProtection")

    @subnet_change_protection.setter # type: ignore
    def subnet_change_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "subnetChangeProtection", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewall.SubnetMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"subnet_id": "subnetId"},
    )
    class SubnetMappingProperty:
        def __init__(self, *, subnet_id: builtins.str) -> None:
            """
            :param subnet_id: ``CfnFirewall.SubnetMappingProperty.SubnetId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewall-subnetmapping.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "subnet_id": subnet_id,
            }

        @builtins.property
        def subnet_id(self) -> builtins.str:
            """``CfnFirewall.SubnetMappingProperty.SubnetId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewall-subnetmapping.html#cfn-networkfirewall-firewall-subnetmapping-subnetid
            """
            result = self._values.get("subnet_id")
            assert result is not None, "Required property 'subnet_id' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubnetMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewall.TagsProperty",
        jsii_struct_bases=[],
        name_mapping={"tags": "tags"},
    )
    class TagsProperty:
        def __init__(
            self,
            *,
            tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        ) -> None:
            """
            :param tags: ``CfnFirewall.TagsProperty.Tags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewall-tags.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
            """``CfnFirewall.TagsProperty.Tags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewall-tags.html#cfn-networkfirewall-firewall-tags-tags
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


@jsii.implements(_IInspectable_82c04a63)
class CfnFirewallPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy",
):
    """A CloudFormation ``AWS::NetworkFirewall::FirewallPolicy``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html
    :cloudformationResource: AWS::NetworkFirewall::FirewallPolicy
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        firewall_policy: typing.Union["CfnFirewallPolicy.FirewallPolicyProperty", _IResolvable_a771d0ef],
        firewall_policy_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional["CfnFirewallPolicy.TagsProperty"] = None,
    ) -> None:
        """Create a new ``AWS::NetworkFirewall::FirewallPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param firewall_policy: ``AWS::NetworkFirewall::FirewallPolicy.FirewallPolicy``.
        :param firewall_policy_name: ``AWS::NetworkFirewall::FirewallPolicy.FirewallPolicyName``.
        :param description: ``AWS::NetworkFirewall::FirewallPolicy.Description``.
        :param tags: ``AWS::NetworkFirewall::FirewallPolicy.Tags``.
        """
        props = CfnFirewallPolicyProps(
            firewall_policy=firewall_policy,
            firewall_policy_name=firewall_policy_name,
            description=description,
            tags=tags,
        )

        jsii.create(CfnFirewallPolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrFirewallPolicyArn")
    def attr_firewall_policy_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: FirewallPolicyArn
        """
        return jsii.get(self, "attrFirewallPolicyArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrFirewallPolicyId")
    def attr_firewall_policy_id(self) -> builtins.str:
        """
        :cloudformationAttribute: FirewallPolicyId
        """
        return jsii.get(self, "attrFirewallPolicyId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::NetworkFirewall::FirewallPolicy.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="firewallPolicy")
    def firewall_policy(
        self,
    ) -> typing.Union["CfnFirewallPolicy.FirewallPolicyProperty", _IResolvable_a771d0ef]:
        """``AWS::NetworkFirewall::FirewallPolicy.FirewallPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy
        """
        return jsii.get(self, "firewallPolicy")

    @firewall_policy.setter # type: ignore
    def firewall_policy(
        self,
        value: typing.Union["CfnFirewallPolicy.FirewallPolicyProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "firewallPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="firewallPolicyName")
    def firewall_policy_name(self) -> builtins.str:
        """``AWS::NetworkFirewall::FirewallPolicy.FirewallPolicyName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicyname
        """
        return jsii.get(self, "firewallPolicyName")

    @firewall_policy_name.setter # type: ignore
    def firewall_policy_name(self, value: builtins.str) -> None:
        jsii.set(self, "firewallPolicyName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkFirewall::FirewallPolicy.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.ActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"publish_metric_action": "publishMetricAction"},
    )
    class ActionDefinitionProperty:
        def __init__(
            self,
            *,
            publish_metric_action: typing.Optional[typing.Union["CfnFirewallPolicy.PublishMetricActionProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param publish_metric_action: ``CfnFirewallPolicy.ActionDefinitionProperty.PublishMetricAction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-actiondefinition.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if publish_metric_action is not None:
                self._values["publish_metric_action"] = publish_metric_action

        @builtins.property
        def publish_metric_action(
            self,
        ) -> typing.Optional[typing.Union["CfnFirewallPolicy.PublishMetricActionProperty", _IResolvable_a771d0ef]]:
            """``CfnFirewallPolicy.ActionDefinitionProperty.PublishMetricAction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-actiondefinition.html#cfn-networkfirewall-firewallpolicy-actiondefinition-publishmetricaction
            """
            result = self._values.get("publish_metric_action")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.CustomActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_definition": "actionDefinition",
            "action_name": "actionName",
        },
    )
    class CustomActionProperty:
        def __init__(
            self,
            *,
            action_definition: typing.Union["CfnFirewallPolicy.ActionDefinitionProperty", _IResolvable_a771d0ef],
            action_name: builtins.str,
        ) -> None:
            """
            :param action_definition: ``CfnFirewallPolicy.CustomActionProperty.ActionDefinition``.
            :param action_name: ``CfnFirewallPolicy.CustomActionProperty.ActionName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customaction.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "action_definition": action_definition,
                "action_name": action_name,
            }

        @builtins.property
        def action_definition(
            self,
        ) -> typing.Union["CfnFirewallPolicy.ActionDefinitionProperty", _IResolvable_a771d0ef]:
            """``CfnFirewallPolicy.CustomActionProperty.ActionDefinition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customaction.html#cfn-networkfirewall-firewallpolicy-customaction-actiondefinition
            """
            result = self._values.get("action_definition")
            assert result is not None, "Required property 'action_definition' is missing"
            return result

        @builtins.property
        def action_name(self) -> builtins.str:
            """``CfnFirewallPolicy.CustomActionProperty.ActionName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customaction.html#cfn-networkfirewall-firewallpolicy-customaction-actionname
            """
            result = self._values.get("action_name")
            assert result is not None, "Required property 'action_name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.CustomActionsProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_actions": "customActions"},
    )
    class CustomActionsProperty:
        def __init__(
            self,
            *,
            custom_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.CustomActionProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param custom_actions: ``CfnFirewallPolicy.CustomActionsProperty.CustomActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customactions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if custom_actions is not None:
                self._values["custom_actions"] = custom_actions

        @builtins.property
        def custom_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.CustomActionProperty", _IResolvable_a771d0ef]]]]:
            """``CfnFirewallPolicy.CustomActionsProperty.CustomActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customactions.html#cfn-networkfirewall-firewallpolicy-customactions-customactions
            """
            result = self._values.get("custom_actions")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, value: builtins.str) -> None:
            """
            :param value: ``CfnFirewallPolicy.DimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-dimension.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnFirewallPolicy.DimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-dimension.html#cfn-networkfirewall-firewallpolicy-dimension-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.DimensionsProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions"},
    )
    class DimensionsProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.DimensionProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param dimensions: ``CfnFirewallPolicy.DimensionsProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-dimensions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.DimensionProperty", _IResolvable_a771d0ef]]]]:
            """``CfnFirewallPolicy.DimensionsProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-dimensions.html#cfn-networkfirewall-firewallpolicy-dimensions-dimensions
            """
            result = self._values.get("dimensions")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.FirewallPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "stateless_default_actions": "statelessDefaultActions",
            "stateless_fragment_default_actions": "statelessFragmentDefaultActions",
            "stateful_rule_group_references": "statefulRuleGroupReferences",
            "stateless_custom_actions": "statelessCustomActions",
            "stateless_rule_group_references": "statelessRuleGroupReferences",
        },
    )
    class FirewallPolicyProperty:
        def __init__(
            self,
            *,
            stateless_default_actions: typing.Union["CfnFirewallPolicy.StatelessActionsProperty", _IResolvable_a771d0ef],
            stateless_fragment_default_actions: typing.Union["CfnFirewallPolicy.StatelessActionsProperty", _IResolvable_a771d0ef],
            stateful_rule_group_references: typing.Optional[typing.Union["CfnFirewallPolicy.StatefulRuleGroupReferencesProperty", _IResolvable_a771d0ef]] = None,
            stateless_custom_actions: typing.Optional[typing.Union["CfnFirewallPolicy.CustomActionsProperty", _IResolvable_a771d0ef]] = None,
            stateless_rule_group_references: typing.Optional[typing.Union["CfnFirewallPolicy.StatelessRuleGroupReferencesProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param stateless_default_actions: ``CfnFirewallPolicy.FirewallPolicyProperty.StatelessDefaultActions``.
            :param stateless_fragment_default_actions: ``CfnFirewallPolicy.FirewallPolicyProperty.StatelessFragmentDefaultActions``.
            :param stateful_rule_group_references: ``CfnFirewallPolicy.FirewallPolicyProperty.StatefulRuleGroupReferences``.
            :param stateless_custom_actions: ``CfnFirewallPolicy.FirewallPolicyProperty.StatelessCustomActions``.
            :param stateless_rule_group_references: ``CfnFirewallPolicy.FirewallPolicyProperty.StatelessRuleGroupReferences``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "stateless_default_actions": stateless_default_actions,
                "stateless_fragment_default_actions": stateless_fragment_default_actions,
            }
            if stateful_rule_group_references is not None:
                self._values["stateful_rule_group_references"] = stateful_rule_group_references
            if stateless_custom_actions is not None:
                self._values["stateless_custom_actions"] = stateless_custom_actions
            if stateless_rule_group_references is not None:
                self._values["stateless_rule_group_references"] = stateless_rule_group_references

        @builtins.property
        def stateless_default_actions(
            self,
        ) -> typing.Union["CfnFirewallPolicy.StatelessActionsProperty", _IResolvable_a771d0ef]:
            """``CfnFirewallPolicy.FirewallPolicyProperty.StatelessDefaultActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelessdefaultactions
            """
            result = self._values.get("stateless_default_actions")
            assert result is not None, "Required property 'stateless_default_actions' is missing"
            return result

        @builtins.property
        def stateless_fragment_default_actions(
            self,
        ) -> typing.Union["CfnFirewallPolicy.StatelessActionsProperty", _IResolvable_a771d0ef]:
            """``CfnFirewallPolicy.FirewallPolicyProperty.StatelessFragmentDefaultActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelessfragmentdefaultactions
            """
            result = self._values.get("stateless_fragment_default_actions")
            assert result is not None, "Required property 'stateless_fragment_default_actions' is missing"
            return result

        @builtins.property
        def stateful_rule_group_references(
            self,
        ) -> typing.Optional[typing.Union["CfnFirewallPolicy.StatefulRuleGroupReferencesProperty", _IResolvable_a771d0ef]]:
            """``CfnFirewallPolicy.FirewallPolicyProperty.StatefulRuleGroupReferences``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statefulrulegroupreferences
            """
            result = self._values.get("stateful_rule_group_references")
            return result

        @builtins.property
        def stateless_custom_actions(
            self,
        ) -> typing.Optional[typing.Union["CfnFirewallPolicy.CustomActionsProperty", _IResolvable_a771d0ef]]:
            """``CfnFirewallPolicy.FirewallPolicyProperty.StatelessCustomActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelesscustomactions
            """
            result = self._values.get("stateless_custom_actions")
            return result

        @builtins.property
        def stateless_rule_group_references(
            self,
        ) -> typing.Optional[typing.Union["CfnFirewallPolicy.StatelessRuleGroupReferencesProperty", _IResolvable_a771d0ef]]:
            """``CfnFirewallPolicy.FirewallPolicyProperty.StatelessRuleGroupReferences``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelessrulegroupreferences
            """
            result = self._values.get("stateless_rule_group_references")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirewallPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.PublishMetricActionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions"},
    )
    class PublishMetricActionProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Union["CfnFirewallPolicy.DimensionsProperty", _IResolvable_a771d0ef],
        ) -> None:
            """
            :param dimensions: ``CfnFirewallPolicy.PublishMetricActionProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-publishmetricaction.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "dimensions": dimensions,
            }

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Union["CfnFirewallPolicy.DimensionsProperty", _IResolvable_a771d0ef]:
            """``CfnFirewallPolicy.PublishMetricActionProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-publishmetricaction.html#cfn-networkfirewall-firewallpolicy-publishmetricaction-dimensions
            """
            result = self._values.get("dimensions")
            assert result is not None, "Required property 'dimensions' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublishMetricActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class StatefulRuleGroupReferenceProperty:
        def __init__(self, *, resource_arn: builtins.str) -> None:
            """
            :param resource_arn: ``CfnFirewallPolicy.StatefulRuleGroupReferenceProperty.ResourceArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            """``CfnFirewallPolicy.StatefulRuleGroupReferenceProperty.ResourceArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupreference-resourcearn
            """
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleGroupReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.StatefulRuleGroupReferencesProperty",
        jsii_struct_bases=[],
        name_mapping={"stateful_rule_group_references": "statefulRuleGroupReferences"},
    )
    class StatefulRuleGroupReferencesProperty:
        def __init__(
            self,
            *,
            stateful_rule_group_references: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.StatefulRuleGroupReferenceProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param stateful_rule_group_references: ``CfnFirewallPolicy.StatefulRuleGroupReferencesProperty.StatefulRuleGroupReferences``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreferences.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if stateful_rule_group_references is not None:
                self._values["stateful_rule_group_references"] = stateful_rule_group_references

        @builtins.property
        def stateful_rule_group_references(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.StatefulRuleGroupReferenceProperty", _IResolvable_a771d0ef]]]]:
            """``CfnFirewallPolicy.StatefulRuleGroupReferencesProperty.StatefulRuleGroupReferences``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreferences.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupreferences-statefulrulegroupreferences
            """
            result = self._values.get("stateful_rule_group_references")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleGroupReferencesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.StatelessActionsProperty",
        jsii_struct_bases=[],
        name_mapping={"stateless_actions": "statelessActions"},
    )
    class StatelessActionsProperty:
        def __init__(
            self,
            *,
            stateless_actions: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param stateless_actions: ``CfnFirewallPolicy.StatelessActionsProperty.StatelessActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessactions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if stateless_actions is not None:
                self._values["stateless_actions"] = stateless_actions

        @builtins.property
        def stateless_actions(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnFirewallPolicy.StatelessActionsProperty.StatelessActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessactions.html#cfn-networkfirewall-firewallpolicy-statelessactions-statelessactions
            """
            result = self._values.get("stateless_actions")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "resource_arn": "resourceArn"},
    )
    class StatelessRuleGroupReferenceProperty:
        def __init__(
            self,
            *,
            priority: jsii.Number,
            resource_arn: builtins.str,
        ) -> None:
            """
            :param priority: ``CfnFirewallPolicy.StatelessRuleGroupReferenceProperty.Priority``.
            :param resource_arn: ``CfnFirewallPolicy.StatelessRuleGroupReferenceProperty.ResourceArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessrulegroupreference.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "priority": priority,
                "resource_arn": resource_arn,
            }

        @builtins.property
        def priority(self) -> jsii.Number:
            """``CfnFirewallPolicy.StatelessRuleGroupReferenceProperty.Priority``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statelessrulegroupreference-priority
            """
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return result

        @builtins.property
        def resource_arn(self) -> builtins.str:
            """``CfnFirewallPolicy.StatelessRuleGroupReferenceProperty.ResourceArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statelessrulegroupreference-resourcearn
            """
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRuleGroupReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.StatelessRuleGroupReferencesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "stateless_rule_group_references": "statelessRuleGroupReferences",
        },
    )
    class StatelessRuleGroupReferencesProperty:
        def __init__(
            self,
            *,
            stateless_rule_group_references: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.StatelessRuleGroupReferenceProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param stateless_rule_group_references: ``CfnFirewallPolicy.StatelessRuleGroupReferencesProperty.StatelessRuleGroupReferences``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessrulegroupreferences.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if stateless_rule_group_references is not None:
                self._values["stateless_rule_group_references"] = stateless_rule_group_references

        @builtins.property
        def stateless_rule_group_references(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.StatelessRuleGroupReferenceProperty", _IResolvable_a771d0ef]]]]:
            """``CfnFirewallPolicy.StatelessRuleGroupReferencesProperty.StatelessRuleGroupReferences``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessrulegroupreferences.html#cfn-networkfirewall-firewallpolicy-statelessrulegroupreferences-statelessrulegroupreferences
            """
            result = self._values.get("stateless_rule_group_references")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRuleGroupReferencesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.TagsProperty",
        jsii_struct_bases=[],
        name_mapping={"tags": "tags"},
    )
    class TagsProperty:
        def __init__(
            self,
            *,
            tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        ) -> None:
            """
            :param tags: ``CfnFirewallPolicy.TagsProperty.Tags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-tags.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
            """``CfnFirewallPolicy.TagsProperty.Tags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-tags.html#cfn-networkfirewall-firewallpolicy-tags-tags
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
    jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "firewall_policy": "firewallPolicy",
        "firewall_policy_name": "firewallPolicyName",
        "description": "description",
        "tags": "tags",
    },
)
class CfnFirewallPolicyProps:
    def __init__(
        self,
        *,
        firewall_policy: typing.Union[CfnFirewallPolicy.FirewallPolicyProperty, _IResolvable_a771d0ef],
        firewall_policy_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[CfnFirewallPolicy.TagsProperty] = None,
    ) -> None:
        """Properties for defining a ``AWS::NetworkFirewall::FirewallPolicy``.

        :param firewall_policy: ``AWS::NetworkFirewall::FirewallPolicy.FirewallPolicy``.
        :param firewall_policy_name: ``AWS::NetworkFirewall::FirewallPolicy.FirewallPolicyName``.
        :param description: ``AWS::NetworkFirewall::FirewallPolicy.Description``.
        :param tags: ``AWS::NetworkFirewall::FirewallPolicy.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html
        """
        if isinstance(tags, dict):
            tags = CfnFirewallPolicy.TagsProperty(**tags)
        self._values: typing.Dict[str, typing.Any] = {
            "firewall_policy": firewall_policy,
            "firewall_policy_name": firewall_policy_name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def firewall_policy(
        self,
    ) -> typing.Union[CfnFirewallPolicy.FirewallPolicyProperty, _IResolvable_a771d0ef]:
        """``AWS::NetworkFirewall::FirewallPolicy.FirewallPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy
        """
        result = self._values.get("firewall_policy")
        assert result is not None, "Required property 'firewall_policy' is missing"
        return result

    @builtins.property
    def firewall_policy_name(self) -> builtins.str:
        """``AWS::NetworkFirewall::FirewallPolicy.FirewallPolicyName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicyname
        """
        result = self._values.get("firewall_policy_name")
        assert result is not None, "Required property 'firewall_policy_name' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkFirewall::FirewallPolicy.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[CfnFirewallPolicy.TagsProperty]:
        """``AWS::NetworkFirewall::FirewallPolicy.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_networkfirewall.CfnFirewallProps",
    jsii_struct_bases=[],
    name_mapping={
        "firewall_name": "firewallName",
        "firewall_policy_arn": "firewallPolicyArn",
        "subnet_mappings": "subnetMappings",
        "vpc_id": "vpcId",
        "delete_protection": "deleteProtection",
        "description": "description",
        "firewall_policy_change_protection": "firewallPolicyChangeProtection",
        "subnet_change_protection": "subnetChangeProtection",
        "tags": "tags",
    },
)
class CfnFirewallProps:
    def __init__(
        self,
        *,
        firewall_name: builtins.str,
        firewall_policy_arn: builtins.str,
        subnet_mappings: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFirewall.SubnetMappingProperty, _IResolvable_a771d0ef]]],
        vpc_id: builtins.str,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[CfnFirewall.TagsProperty] = None,
    ) -> None:
        """Properties for defining a ``AWS::NetworkFirewall::Firewall``.

        :param firewall_name: ``AWS::NetworkFirewall::Firewall.FirewallName``.
        :param firewall_policy_arn: ``AWS::NetworkFirewall::Firewall.FirewallPolicyArn``.
        :param subnet_mappings: ``AWS::NetworkFirewall::Firewall.SubnetMappings``.
        :param vpc_id: ``AWS::NetworkFirewall::Firewall.VpcId``.
        :param delete_protection: ``AWS::NetworkFirewall::Firewall.DeleteProtection``.
        :param description: ``AWS::NetworkFirewall::Firewall.Description``.
        :param firewall_policy_change_protection: ``AWS::NetworkFirewall::Firewall.FirewallPolicyChangeProtection``.
        :param subnet_change_protection: ``AWS::NetworkFirewall::Firewall.SubnetChangeProtection``.
        :param tags: ``AWS::NetworkFirewall::Firewall.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html
        """
        if isinstance(tags, dict):
            tags = CfnFirewall.TagsProperty(**tags)
        self._values: typing.Dict[str, typing.Any] = {
            "firewall_name": firewall_name,
            "firewall_policy_arn": firewall_policy_arn,
            "subnet_mappings": subnet_mappings,
            "vpc_id": vpc_id,
        }
        if delete_protection is not None:
            self._values["delete_protection"] = delete_protection
        if description is not None:
            self._values["description"] = description
        if firewall_policy_change_protection is not None:
            self._values["firewall_policy_change_protection"] = firewall_policy_change_protection
        if subnet_change_protection is not None:
            self._values["subnet_change_protection"] = subnet_change_protection
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def firewall_name(self) -> builtins.str:
        """``AWS::NetworkFirewall::Firewall.FirewallName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallname
        """
        result = self._values.get("firewall_name")
        assert result is not None, "Required property 'firewall_name' is missing"
        return result

    @builtins.property
    def firewall_policy_arn(self) -> builtins.str:
        """``AWS::NetworkFirewall::Firewall.FirewallPolicyArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicyarn
        """
        result = self._values.get("firewall_policy_arn")
        assert result is not None, "Required property 'firewall_policy_arn' is missing"
        return result

    @builtins.property
    def subnet_mappings(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFirewall.SubnetMappingProperty, _IResolvable_a771d0ef]]]:
        """``AWS::NetworkFirewall::Firewall.SubnetMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetmappings
        """
        result = self._values.get("subnet_mappings")
        assert result is not None, "Required property 'subnet_mappings' is missing"
        return result

    @builtins.property
    def vpc_id(self) -> builtins.str:
        """``AWS::NetworkFirewall::Firewall.VpcId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-vpcid
        """
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return result

    @builtins.property
    def delete_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::NetworkFirewall::Firewall.DeleteProtection``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-deleteprotection
        """
        result = self._values.get("delete_protection")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkFirewall::Firewall.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def firewall_policy_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::NetworkFirewall::Firewall.FirewallPolicyChangeProtection``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicychangeprotection
        """
        result = self._values.get("firewall_policy_change_protection")
        return result

    @builtins.property
    def subnet_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::NetworkFirewall::Firewall.SubnetChangeProtection``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetchangeprotection
        """
        result = self._values.get("subnet_change_protection")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[CfnFirewall.TagsProperty]:
        """``AWS::NetworkFirewall::Firewall.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLoggingConfiguration(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_networkfirewall.CfnLoggingConfiguration",
):
    """A CloudFormation ``AWS::NetworkFirewall::LoggingConfiguration``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html
    :cloudformationResource: AWS::NetworkFirewall::LoggingConfiguration
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        logging_configuration: typing.Union["CfnLoggingConfiguration.LoggingConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        """Create a new ``AWS::NetworkFirewall::LoggingConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param logging_configuration: ``AWS::NetworkFirewall::LoggingConfiguration.LoggingConfiguration``.
        """
        props = CfnLoggingConfigurationProps(
            logging_configuration=logging_configuration
        )

        jsii.create(CfnLoggingConfiguration, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrFirewallArn")
    def attr_firewall_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: FirewallArn
        """
        return jsii.get(self, "attrFirewallArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrFirewallName")
    def attr_firewall_name(self) -> builtins.str:
        """
        :cloudformationAttribute: FirewallName
        """
        return jsii.get(self, "attrFirewallName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loggingConfiguration")
    def logging_configuration(
        self,
    ) -> typing.Union["CfnLoggingConfiguration.LoggingConfigurationProperty", _IResolvable_a771d0ef]:
        """``AWS::NetworkFirewall::LoggingConfiguration.LoggingConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-loggingconfiguration
        """
        return jsii.get(self, "loggingConfiguration")

    @logging_configuration.setter # type: ignore
    def logging_configuration(
        self,
        value: typing.Union["CfnLoggingConfiguration.LoggingConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "loggingConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnLoggingConfiguration.LogDestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_destination": "logDestination",
            "log_destination_type": "logDestinationType",
            "log_type": "logType",
        },
    )
    class LogDestinationConfigProperty:
        def __init__(
            self,
            *,
            log_destination: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]],
            log_destination_type: builtins.str,
            log_type: builtins.str,
        ) -> None:
            """
            :param log_destination: ``CfnLoggingConfiguration.LogDestinationConfigProperty.LogDestination``.
            :param log_destination_type: ``CfnLoggingConfiguration.LogDestinationConfigProperty.LogDestinationType``.
            :param log_type: ``CfnLoggingConfiguration.LogDestinationConfigProperty.LogType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "log_destination": log_destination,
                "log_destination_type": log_destination_type,
                "log_type": log_type,
            }

        @builtins.property
        def log_destination(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]:
            """``CfnLoggingConfiguration.LogDestinationConfigProperty.LogDestination``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html#cfn-networkfirewall-loggingconfiguration-logdestinationconfig-logdestination
            """
            result = self._values.get("log_destination")
            assert result is not None, "Required property 'log_destination' is missing"
            return result

        @builtins.property
        def log_destination_type(self) -> builtins.str:
            """``CfnLoggingConfiguration.LogDestinationConfigProperty.LogDestinationType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html#cfn-networkfirewall-loggingconfiguration-logdestinationconfig-logdestinationtype
            """
            result = self._values.get("log_destination_type")
            assert result is not None, "Required property 'log_destination_type' is missing"
            return result

        @builtins.property
        def log_type(self) -> builtins.str:
            """``CfnLoggingConfiguration.LogDestinationConfigProperty.LogType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html#cfn-networkfirewall-loggingconfiguration-logdestinationconfig-logtype
            """
            result = self._values.get("log_type")
            assert result is not None, "Required property 'log_type' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnLoggingConfiguration.LogDestinationConfigsProperty",
        jsii_struct_bases=[],
        name_mapping={"log_destination_configs": "logDestinationConfigs"},
    )
    class LogDestinationConfigsProperty:
        def __init__(
            self,
            *,
            log_destination_configs: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoggingConfiguration.LogDestinationConfigProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param log_destination_configs: ``CfnLoggingConfiguration.LogDestinationConfigsProperty.LogDestinationConfigs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfigs.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if log_destination_configs is not None:
                self._values["log_destination_configs"] = log_destination_configs

        @builtins.property
        def log_destination_configs(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoggingConfiguration.LogDestinationConfigProperty", _IResolvable_a771d0ef]]]]:
            """``CfnLoggingConfiguration.LogDestinationConfigsProperty.LogDestinationConfigs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfigs.html#cfn-networkfirewall-loggingconfiguration-logdestinationconfigs-logdestinationconfigs
            """
            result = self._values.get("log_destination_configs")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDestinationConfigsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnLoggingConfiguration.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_destination_configs": "logDestinationConfigs"},
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            log_destination_configs: typing.Union["CfnLoggingConfiguration.LogDestinationConfigsProperty", _IResolvable_a771d0ef],
        ) -> None:
            """
            :param log_destination_configs: ``CfnLoggingConfiguration.LoggingConfigurationProperty.LogDestinationConfigs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-loggingconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "log_destination_configs": log_destination_configs,
            }

        @builtins.property
        def log_destination_configs(
            self,
        ) -> typing.Union["CfnLoggingConfiguration.LogDestinationConfigsProperty", _IResolvable_a771d0ef]:
            """``CfnLoggingConfiguration.LoggingConfigurationProperty.LogDestinationConfigs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-loggingconfiguration-logdestinationconfigs
            """
            result = self._values.get("log_destination_configs")
            assert result is not None, "Required property 'log_destination_configs' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_networkfirewall.CfnLoggingConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={"logging_configuration": "loggingConfiguration"},
)
class CfnLoggingConfigurationProps:
    def __init__(
        self,
        *,
        logging_configuration: typing.Union[CfnLoggingConfiguration.LoggingConfigurationProperty, _IResolvable_a771d0ef],
    ) -> None:
        """Properties for defining a ``AWS::NetworkFirewall::LoggingConfiguration``.

        :param logging_configuration: ``AWS::NetworkFirewall::LoggingConfiguration.LoggingConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "logging_configuration": logging_configuration,
        }

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Union[CfnLoggingConfiguration.LoggingConfigurationProperty, _IResolvable_a771d0ef]:
        """``AWS::NetworkFirewall::LoggingConfiguration.LoggingConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-loggingconfiguration
        """
        result = self._values.get("logging_configuration")
        assert result is not None, "Required property 'logging_configuration' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoggingConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRuleGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup",
):
    """A CloudFormation ``AWS::NetworkFirewall::RuleGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html
    :cloudformationResource: AWS::NetworkFirewall::RuleGroup
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        capacity: jsii.Number,
        rule_group_name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        rule_group: typing.Optional[typing.Union["CfnRuleGroup.RuleGroupProperty", _IResolvable_a771d0ef]] = None,
        rule_group_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional["CfnRuleGroup.TagsProperty"] = None,
    ) -> None:
        """Create a new ``AWS::NetworkFirewall::RuleGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param capacity: ``AWS::NetworkFirewall::RuleGroup.Capacity``.
        :param rule_group_name: ``AWS::NetworkFirewall::RuleGroup.RuleGroupName``.
        :param type: ``AWS::NetworkFirewall::RuleGroup.Type``.
        :param description: ``AWS::NetworkFirewall::RuleGroup.Description``.
        :param rule_group: ``AWS::NetworkFirewall::RuleGroup.RuleGroup``.
        :param rule_group_id: ``AWS::NetworkFirewall::RuleGroup.RuleGroupId``.
        :param tags: ``AWS::NetworkFirewall::RuleGroup.Tags``.
        """
        props = CfnRuleGroupProps(
            capacity=capacity,
            rule_group_name=rule_group_name,
            type=type,
            description=description,
            rule_group=rule_group,
            rule_group_id=rule_group_id,
            tags=tags,
        )

        jsii.create(CfnRuleGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrRuleGroupArn")
    def attr_rule_group_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: RuleGroupArn
        """
        return jsii.get(self, "attrRuleGroupArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::NetworkFirewall::RuleGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        """``AWS::NetworkFirewall::RuleGroup.Capacity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-capacity
        """
        return jsii.get(self, "capacity")

    @capacity.setter # type: ignore
    def capacity(self, value: jsii.Number) -> None:
        jsii.set(self, "capacity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleGroupName")
    def rule_group_name(self) -> builtins.str:
        """``AWS::NetworkFirewall::RuleGroup.RuleGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroupname
        """
        return jsii.get(self, "ruleGroupName")

    @rule_group_name.setter # type: ignore
    def rule_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "ruleGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """``AWS::NetworkFirewall::RuleGroup.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkFirewall::RuleGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleGroup")
    def rule_group(
        self,
    ) -> typing.Optional[typing.Union["CfnRuleGroup.RuleGroupProperty", _IResolvable_a771d0ef]]:
        """``AWS::NetworkFirewall::RuleGroup.RuleGroup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup
        """
        return jsii.get(self, "ruleGroup")

    @rule_group.setter # type: ignore
    def rule_group(
        self,
        value: typing.Optional[typing.Union["CfnRuleGroup.RuleGroupProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "ruleGroup", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ruleGroupId")
    def rule_group_id(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkFirewall::RuleGroup.RuleGroupId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroupid
        """
        return jsii.get(self, "ruleGroupId")

    @rule_group_id.setter # type: ignore
    def rule_group_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ruleGroupId", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.ActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"publish_metric_action": "publishMetricAction"},
    )
    class ActionDefinitionProperty:
        def __init__(
            self,
            *,
            publish_metric_action: typing.Optional[typing.Union["CfnRuleGroup.PublishMetricActionProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param publish_metric_action: ``CfnRuleGroup.ActionDefinitionProperty.PublishMetricAction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-actiondefinition.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if publish_metric_action is not None:
                self._values["publish_metric_action"] = publish_metric_action

        @builtins.property
        def publish_metric_action(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.PublishMetricActionProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.ActionDefinitionProperty.PublishMetricAction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-actiondefinition.html#cfn-networkfirewall-rulegroup-actiondefinition-publishmetricaction
            """
            result = self._values.get("publish_metric_action")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.AddressProperty",
        jsii_struct_bases=[],
        name_mapping={"address_definition": "addressDefinition"},
    )
    class AddressProperty:
        def __init__(self, *, address_definition: builtins.str) -> None:
            """
            :param address_definition: ``CfnRuleGroup.AddressProperty.AddressDefinition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-address.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "address_definition": address_definition,
            }

        @builtins.property
        def address_definition(self) -> builtins.str:
            """``CfnRuleGroup.AddressProperty.AddressDefinition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-address.html#cfn-networkfirewall-rulegroup-address-addressdefinition
            """
            result = self._values.get("address_definition")
            assert result is not None, "Required property 'address_definition' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.AddressesProperty",
        jsii_struct_bases=[],
        name_mapping={"addresses": "addresses"},
    )
    class AddressesProperty:
        def __init__(
            self,
            *,
            addresses: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.AddressProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param addresses: ``CfnRuleGroup.AddressesProperty.Addresses``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-addresses.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if addresses is not None:
                self._values["addresses"] = addresses

        @builtins.property
        def addresses(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.AddressProperty", _IResolvable_a771d0ef]]]]:
            """``CfnRuleGroup.AddressesProperty.Addresses``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-addresses.html#cfn-networkfirewall-rulegroup-addresses-addresses
            """
            result = self._values.get("addresses")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddressesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.CustomActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_definition": "actionDefinition",
            "action_name": "actionName",
        },
    )
    class CustomActionProperty:
        def __init__(
            self,
            *,
            action_definition: typing.Union["CfnRuleGroup.ActionDefinitionProperty", _IResolvable_a771d0ef],
            action_name: builtins.str,
        ) -> None:
            """
            :param action_definition: ``CfnRuleGroup.CustomActionProperty.ActionDefinition``.
            :param action_name: ``CfnRuleGroup.CustomActionProperty.ActionName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customaction.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "action_definition": action_definition,
                "action_name": action_name,
            }

        @builtins.property
        def action_definition(
            self,
        ) -> typing.Union["CfnRuleGroup.ActionDefinitionProperty", _IResolvable_a771d0ef]:
            """``CfnRuleGroup.CustomActionProperty.ActionDefinition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customaction.html#cfn-networkfirewall-rulegroup-customaction-actiondefinition
            """
            result = self._values.get("action_definition")
            assert result is not None, "Required property 'action_definition' is missing"
            return result

        @builtins.property
        def action_name(self) -> builtins.str:
            """``CfnRuleGroup.CustomActionProperty.ActionName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customaction.html#cfn-networkfirewall-rulegroup-customaction-actionname
            """
            result = self._values.get("action_name")
            assert result is not None, "Required property 'action_name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.CustomActionsProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_actions": "customActions"},
    )
    class CustomActionsProperty:
        def __init__(
            self,
            *,
            custom_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.CustomActionProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param custom_actions: ``CfnRuleGroup.CustomActionsProperty.CustomActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customactions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if custom_actions is not None:
                self._values["custom_actions"] = custom_actions

        @builtins.property
        def custom_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.CustomActionProperty", _IResolvable_a771d0ef]]]]:
            """``CfnRuleGroup.CustomActionsProperty.CustomActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customactions.html#cfn-networkfirewall-rulegroup-customactions-customactions
            """
            result = self._values.get("custom_actions")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, value: builtins.str) -> None:
            """
            :param value: ``CfnRuleGroup.DimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-dimension.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnRuleGroup.DimensionProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-dimension.html#cfn-networkfirewall-rulegroup-dimension-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.DimensionsProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions"},
    )
    class DimensionsProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.DimensionProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param dimensions: ``CfnRuleGroup.DimensionsProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-dimensions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.DimensionProperty", _IResolvable_a771d0ef]]]]:
            """``CfnRuleGroup.DimensionsProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-dimensions.html#cfn-networkfirewall-rulegroup-dimensions-dimensions
            """
            result = self._values.get("dimensions")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.FlagsProperty",
        jsii_struct_bases=[],
        name_mapping={"flags": "flags"},
    )
    class FlagsProperty:
        def __init__(
            self,
            *,
            flags: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param flags: ``CfnRuleGroup.FlagsProperty.Flags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-flags.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if flags is not None:
                self._values["flags"] = flags

        @builtins.property
        def flags(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnRuleGroup.FlagsProperty.Flags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-flags.html#cfn-networkfirewall-rulegroup-flags-flags
            """
            result = self._values.get("flags")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlagsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.HeaderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "destination_port": "destinationPort",
            "direction": "direction",
            "protocol": "protocol",
            "source": "source",
            "source_port": "sourcePort",
        },
    )
    class HeaderProperty:
        def __init__(
            self,
            *,
            destination: builtins.str,
            destination_port: builtins.str,
            direction: builtins.str,
            protocol: builtins.str,
            source: builtins.str,
            source_port: builtins.str,
        ) -> None:
            """
            :param destination: ``CfnRuleGroup.HeaderProperty.Destination``.
            :param destination_port: ``CfnRuleGroup.HeaderProperty.DestinationPort``.
            :param direction: ``CfnRuleGroup.HeaderProperty.Direction``.
            :param protocol: ``CfnRuleGroup.HeaderProperty.Protocol``.
            :param source: ``CfnRuleGroup.HeaderProperty.Source``.
            :param source_port: ``CfnRuleGroup.HeaderProperty.SourcePort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "destination": destination,
                "destination_port": destination_port,
                "direction": direction,
                "protocol": protocol,
                "source": source,
                "source_port": source_port,
            }

        @builtins.property
        def destination(self) -> builtins.str:
            """``CfnRuleGroup.HeaderProperty.Destination``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-destination
            """
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return result

        @builtins.property
        def destination_port(self) -> builtins.str:
            """``CfnRuleGroup.HeaderProperty.DestinationPort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-destinationport
            """
            result = self._values.get("destination_port")
            assert result is not None, "Required property 'destination_port' is missing"
            return result

        @builtins.property
        def direction(self) -> builtins.str:
            """``CfnRuleGroup.HeaderProperty.Direction``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-direction
            """
            result = self._values.get("direction")
            assert result is not None, "Required property 'direction' is missing"
            return result

        @builtins.property
        def protocol(self) -> builtins.str:
            """``CfnRuleGroup.HeaderProperty.Protocol``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-protocol
            """
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return result

        @builtins.property
        def source(self) -> builtins.str:
            """``CfnRuleGroup.HeaderProperty.Source``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-source
            """
            result = self._values.get("source")
            assert result is not None, "Required property 'source' is missing"
            return result

        @builtins.property
        def source_port(self) -> builtins.str:
            """``CfnRuleGroup.HeaderProperty.SourcePort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-sourceport
            """
            result = self._values.get("source_port")
            assert result is not None, "Required property 'source_port' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.interface(jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.IPSetProperty")
    class IPSetProperty(typing_extensions.Protocol):
        """
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipset.html
        """

        @builtins.staticmethod
        def __jsii_proxy_class__():
            return _IPSetPropertyProxy

        @builtins.property # type: ignore
        @jsii.member(jsii_name="definition")
        def definition(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.VariableDefinitionListProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.IPSetProperty.Definition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipset.html#cfn-networkfirewall-rulegroup-ipset-definition
            """
            ...


    class _IPSetPropertyProxy:
        """
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipset.html
        """

        __jsii_type__: typing.ClassVar[str] = "monocdk.aws_networkfirewall.CfnRuleGroup.IPSetProperty"

        @builtins.property # type: ignore
        @jsii.member(jsii_name="definition")
        def definition(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.VariableDefinitionListProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.IPSetProperty.Definition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipset.html#cfn-networkfirewall-rulegroup-ipset-definition
            """
            return jsii.get(self, "definition")

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.MatchAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_ports": "destinationPorts",
            "destinations": "destinations",
            "protocols": "protocols",
            "source_ports": "sourcePorts",
            "sources": "sources",
            "tcp_flags": "tcpFlags",
        },
    )
    class MatchAttributesProperty:
        def __init__(
            self,
            *,
            destination_ports: typing.Optional[typing.Union["CfnRuleGroup.PortRangesProperty", _IResolvable_a771d0ef]] = None,
            destinations: typing.Optional[typing.Union["CfnRuleGroup.AddressesProperty", _IResolvable_a771d0ef]] = None,
            protocols: typing.Optional[typing.Union["CfnRuleGroup.ProtocolNumbersProperty", _IResolvable_a771d0ef]] = None,
            source_ports: typing.Optional[typing.Union["CfnRuleGroup.PortRangesProperty", _IResolvable_a771d0ef]] = None,
            sources: typing.Optional[typing.Union["CfnRuleGroup.AddressesProperty", _IResolvable_a771d0ef]] = None,
            tcp_flags: typing.Optional[typing.Union["CfnRuleGroup.TCPFlagsProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param destination_ports: ``CfnRuleGroup.MatchAttributesProperty.DestinationPorts``.
            :param destinations: ``CfnRuleGroup.MatchAttributesProperty.Destinations``.
            :param protocols: ``CfnRuleGroup.MatchAttributesProperty.Protocols``.
            :param source_ports: ``CfnRuleGroup.MatchAttributesProperty.SourcePorts``.
            :param sources: ``CfnRuleGroup.MatchAttributesProperty.Sources``.
            :param tcp_flags: ``CfnRuleGroup.MatchAttributesProperty.TCPFlags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if destination_ports is not None:
                self._values["destination_ports"] = destination_ports
            if destinations is not None:
                self._values["destinations"] = destinations
            if protocols is not None:
                self._values["protocols"] = protocols
            if source_ports is not None:
                self._values["source_ports"] = source_ports
            if sources is not None:
                self._values["sources"] = sources
            if tcp_flags is not None:
                self._values["tcp_flags"] = tcp_flags

        @builtins.property
        def destination_ports(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.PortRangesProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.MatchAttributesProperty.DestinationPorts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-destinationports
            """
            result = self._values.get("destination_ports")
            return result

        @builtins.property
        def destinations(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.AddressesProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.MatchAttributesProperty.Destinations``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-destinations
            """
            result = self._values.get("destinations")
            return result

        @builtins.property
        def protocols(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.ProtocolNumbersProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.MatchAttributesProperty.Protocols``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-protocols
            """
            result = self._values.get("protocols")
            return result

        @builtins.property
        def source_ports(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.PortRangesProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.MatchAttributesProperty.SourcePorts``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-sourceports
            """
            result = self._values.get("source_ports")
            return result

        @builtins.property
        def sources(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.AddressesProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.MatchAttributesProperty.Sources``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-sources
            """
            result = self._values.get("sources")
            return result

        @builtins.property
        def tcp_flags(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.TCPFlagsProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.MatchAttributesProperty.TCPFlags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-tcpflags
            """
            result = self._values.get("tcp_flags")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.PortRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"from_port": "fromPort", "to_port": "toPort"},
    )
    class PortRangeProperty:
        def __init__(self, *, from_port: jsii.Number, to_port: jsii.Number) -> None:
            """
            :param from_port: ``CfnRuleGroup.PortRangeProperty.FromPort``.
            :param to_port: ``CfnRuleGroup.PortRangeProperty.ToPort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portrange.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "from_port": from_port,
                "to_port": to_port,
            }

        @builtins.property
        def from_port(self) -> jsii.Number:
            """``CfnRuleGroup.PortRangeProperty.FromPort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portrange.html#cfn-networkfirewall-rulegroup-portrange-fromport
            """
            result = self._values.get("from_port")
            assert result is not None, "Required property 'from_port' is missing"
            return result

        @builtins.property
        def to_port(self) -> jsii.Number:
            """``CfnRuleGroup.PortRangeProperty.ToPort``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portrange.html#cfn-networkfirewall-rulegroup-portrange-toport
            """
            result = self._values.get("to_port")
            assert result is not None, "Required property 'to_port' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.PortRangesProperty",
        jsii_struct_bases=[],
        name_mapping={"port_ranges": "portRanges"},
    )
    class PortRangesProperty:
        def __init__(
            self,
            *,
            port_ranges: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.PortRangeProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param port_ranges: ``CfnRuleGroup.PortRangesProperty.PortRanges``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portranges.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if port_ranges is not None:
                self._values["port_ranges"] = port_ranges

        @builtins.property
        def port_ranges(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.PortRangeProperty", _IResolvable_a771d0ef]]]]:
            """``CfnRuleGroup.PortRangesProperty.PortRanges``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portranges.html#cfn-networkfirewall-rulegroup-portranges-portranges
            """
            result = self._values.get("port_ranges")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortRangesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.PortSetProperty",
        jsii_struct_bases=[],
        name_mapping={"definition": "definition"},
    )
    class PortSetProperty:
        def __init__(
            self,
            *,
            definition: typing.Optional[typing.Union["CfnRuleGroup.VariableDefinitionListProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param definition: ``CfnRuleGroup.PortSetProperty.Definition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portset.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if definition is not None:
                self._values["definition"] = definition

        @builtins.property
        def definition(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.VariableDefinitionListProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.PortSetProperty.Definition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portset.html#cfn-networkfirewall-rulegroup-portset-definition
            """
            result = self._values.get("definition")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.ProtocolNumbersProperty",
        jsii_struct_bases=[],
        name_mapping={"protocol_numbers": "protocolNumbers"},
    )
    class ProtocolNumbersProperty:
        def __init__(
            self,
            *,
            protocol_numbers: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[jsii.Number]]] = None,
        ) -> None:
            """
            :param protocol_numbers: ``CfnRuleGroup.ProtocolNumbersProperty.ProtocolNumbers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-protocolnumbers.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if protocol_numbers is not None:
                self._values["protocol_numbers"] = protocol_numbers

        @builtins.property
        def protocol_numbers(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[jsii.Number]]]:
            """``CfnRuleGroup.ProtocolNumbersProperty.ProtocolNumbers``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-protocolnumbers.html#cfn-networkfirewall-rulegroup-protocolnumbers-protocolnumbers
            """
            result = self._values.get("protocol_numbers")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtocolNumbersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.PublishMetricActionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions"},
    )
    class PublishMetricActionProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Union["CfnRuleGroup.DimensionsProperty", _IResolvable_a771d0ef],
        ) -> None:
            """
            :param dimensions: ``CfnRuleGroup.PublishMetricActionProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-publishmetricaction.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "dimensions": dimensions,
            }

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Union["CfnRuleGroup.DimensionsProperty", _IResolvable_a771d0ef]:
            """``CfnRuleGroup.PublishMetricActionProperty.Dimensions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-publishmetricaction.html#cfn-networkfirewall-rulegroup-publishmetricaction-dimensions
            """
            result = self._values.get("dimensions")
            assert result is not None, "Required property 'dimensions' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublishMetricActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RuleDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"actions": "actions", "match_attributes": "matchAttributes"},
    )
    class RuleDefinitionProperty:
        def __init__(
            self,
            *,
            actions: typing.List[builtins.str],
            match_attributes: typing.Union["CfnRuleGroup.MatchAttributesProperty", _IResolvable_a771d0ef],
        ) -> None:
            """
            :param actions: ``CfnRuleGroup.RuleDefinitionProperty.Actions``.
            :param match_attributes: ``CfnRuleGroup.RuleDefinitionProperty.MatchAttributes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruledefinition.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "actions": actions,
                "match_attributes": match_attributes,
            }

        @builtins.property
        def actions(self) -> typing.List[builtins.str]:
            """``CfnRuleGroup.RuleDefinitionProperty.Actions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruledefinition.html#cfn-networkfirewall-rulegroup-ruledefinition-actions
            """
            result = self._values.get("actions")
            assert result is not None, "Required property 'actions' is missing"
            return result

        @builtins.property
        def match_attributes(
            self,
        ) -> typing.Union["CfnRuleGroup.MatchAttributesProperty", _IResolvable_a771d0ef]:
            """``CfnRuleGroup.RuleDefinitionProperty.MatchAttributes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruledefinition.html#cfn-networkfirewall-rulegroup-ruledefinition-matchattributes
            """
            result = self._values.get("match_attributes")
            assert result is not None, "Required property 'match_attributes' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RuleGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rules_source": "rulesSource",
            "rule_variables": "ruleVariables",
        },
    )
    class RuleGroupProperty:
        def __init__(
            self,
            *,
            rules_source: typing.Union["CfnRuleGroup.RulesSourceProperty", _IResolvable_a771d0ef],
            rule_variables: typing.Optional[typing.Union["CfnRuleGroup.RuleVariablesProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param rules_source: ``CfnRuleGroup.RuleGroupProperty.RulesSource``.
            :param rule_variables: ``CfnRuleGroup.RuleGroupProperty.RuleVariables``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "rules_source": rules_source,
            }
            if rule_variables is not None:
                self._values["rule_variables"] = rule_variables

        @builtins.property
        def rules_source(
            self,
        ) -> typing.Union["CfnRuleGroup.RulesSourceProperty", _IResolvable_a771d0ef]:
            """``CfnRuleGroup.RuleGroupProperty.RulesSource``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-rulessource
            """
            result = self._values.get("rules_source")
            assert result is not None, "Required property 'rules_source' is missing"
            return result

        @builtins.property
        def rule_variables(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.RuleVariablesProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.RuleGroupProperty.RuleVariables``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-rulevariables
            """
            result = self._values.get("rule_variables")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RuleOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"keyword": "keyword", "settings": "settings"},
    )
    class RuleOptionProperty:
        def __init__(
            self,
            *,
            keyword: builtins.str,
            settings: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param keyword: ``CfnRuleGroup.RuleOptionProperty.Keyword``.
            :param settings: ``CfnRuleGroup.RuleOptionProperty.Settings``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruleoption.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "keyword": keyword,
            }
            if settings is not None:
                self._values["settings"] = settings

        @builtins.property
        def keyword(self) -> builtins.str:
            """``CfnRuleGroup.RuleOptionProperty.Keyword``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruleoption.html#cfn-networkfirewall-rulegroup-ruleoption-keyword
            """
            result = self._values.get("keyword")
            assert result is not None, "Required property 'keyword' is missing"
            return result

        @builtins.property
        def settings(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnRuleGroup.RuleOptionProperty.Settings``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruleoption.html#cfn-networkfirewall-rulegroup-ruleoption-settings
            """
            result = self._values.get("settings")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RuleOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"rule_options": "ruleOptions"},
    )
    class RuleOptionsProperty:
        def __init__(
            self,
            *,
            rule_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.RuleOptionProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param rule_options: ``CfnRuleGroup.RuleOptionsProperty.RuleOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruleoptions.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if rule_options is not None:
                self._values["rule_options"] = rule_options

        @builtins.property
        def rule_options(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.RuleOptionProperty", _IResolvable_a771d0ef]]]]:
            """``CfnRuleGroup.RuleOptionsProperty.RuleOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruleoptions.html#cfn-networkfirewall-rulegroup-ruleoptions-ruleoptions
            """
            result = self._values.get("rule_options")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RuleVariablesProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_sets": "ipSets", "port_sets": "portSets"},
    )
    class RuleVariablesProperty:
        def __init__(
            self,
            *,
            ip_sets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRuleGroup.IPSetProperty", _IResolvable_a771d0ef]]]] = None,
            port_sets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRuleGroup.PortSetProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param ip_sets: ``CfnRuleGroup.RuleVariablesProperty.IPSets``.
            :param port_sets: ``CfnRuleGroup.RuleVariablesProperty.PortSets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if ip_sets is not None:
                self._values["ip_sets"] = ip_sets
            if port_sets is not None:
                self._values["port_sets"] = port_sets

        @builtins.property
        def ip_sets(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRuleGroup.IPSetProperty", _IResolvable_a771d0ef]]]]:
            """``CfnRuleGroup.RuleVariablesProperty.IPSets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html#cfn-networkfirewall-rulegroup-rulevariables-ipsets
            """
            result = self._values.get("ip_sets")
            return result

        @builtins.property
        def port_sets(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRuleGroup.PortSetProperty", _IResolvable_a771d0ef]]]]:
            """``CfnRuleGroup.RuleVariablesProperty.PortSets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html#cfn-networkfirewall-rulegroup-rulevariables-portsets
            """
            result = self._values.get("port_sets")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleVariablesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RulesSourceListProperty",
        jsii_struct_bases=[],
        name_mapping={
            "generated_rules_type": "generatedRulesType",
            "targets": "targets",
            "target_types": "targetTypes",
        },
    )
    class RulesSourceListProperty:
        def __init__(
            self,
            *,
            generated_rules_type: builtins.str,
            targets: typing.List[builtins.str],
            target_types: typing.Union["CfnRuleGroup.TargetTypesProperty", _IResolvable_a771d0ef],
        ) -> None:
            """
            :param generated_rules_type: ``CfnRuleGroup.RulesSourceListProperty.GeneratedRulesType``.
            :param targets: ``CfnRuleGroup.RulesSourceListProperty.Targets``.
            :param target_types: ``CfnRuleGroup.RulesSourceListProperty.TargetTypes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "generated_rules_type": generated_rules_type,
                "targets": targets,
                "target_types": target_types,
            }

        @builtins.property
        def generated_rules_type(self) -> builtins.str:
            """``CfnRuleGroup.RulesSourceListProperty.GeneratedRulesType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html#cfn-networkfirewall-rulegroup-rulessourcelist-generatedrulestype
            """
            result = self._values.get("generated_rules_type")
            assert result is not None, "Required property 'generated_rules_type' is missing"
            return result

        @builtins.property
        def targets(self) -> typing.List[builtins.str]:
            """``CfnRuleGroup.RulesSourceListProperty.Targets``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html#cfn-networkfirewall-rulegroup-rulessourcelist-targets
            """
            result = self._values.get("targets")
            assert result is not None, "Required property 'targets' is missing"
            return result

        @builtins.property
        def target_types(
            self,
        ) -> typing.Union["CfnRuleGroup.TargetTypesProperty", _IResolvable_a771d0ef]:
            """``CfnRuleGroup.RulesSourceListProperty.TargetTypes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html#cfn-networkfirewall-rulegroup-rulessourcelist-targettypes
            """
            result = self._values.get("target_types")
            assert result is not None, "Required property 'target_types' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RulesSourceListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RulesSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rules_source_list": "rulesSourceList",
            "rules_string": "rulesString",
            "stateful_rules": "statefulRules",
            "stateless_rules_and_custom_actions": "statelessRulesAndCustomActions",
        },
    )
    class RulesSourceProperty:
        def __init__(
            self,
            *,
            rules_source_list: typing.Optional[typing.Union["CfnRuleGroup.RulesSourceListProperty", _IResolvable_a771d0ef]] = None,
            rules_string: typing.Optional[builtins.str] = None,
            stateful_rules: typing.Optional[typing.Union["CfnRuleGroup.StatefulRulesProperty", _IResolvable_a771d0ef]] = None,
            stateless_rules_and_custom_actions: typing.Optional[typing.Union["CfnRuleGroup.StatelessRulesAndCustomActionsProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param rules_source_list: ``CfnRuleGroup.RulesSourceProperty.RulesSourceList``.
            :param rules_string: ``CfnRuleGroup.RulesSourceProperty.RulesString``.
            :param stateful_rules: ``CfnRuleGroup.RulesSourceProperty.StatefulRules``.
            :param stateless_rules_and_custom_actions: ``CfnRuleGroup.RulesSourceProperty.StatelessRulesAndCustomActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if rules_source_list is not None:
                self._values["rules_source_list"] = rules_source_list
            if rules_string is not None:
                self._values["rules_string"] = rules_string
            if stateful_rules is not None:
                self._values["stateful_rules"] = stateful_rules
            if stateless_rules_and_custom_actions is not None:
                self._values["stateless_rules_and_custom_actions"] = stateless_rules_and_custom_actions

        @builtins.property
        def rules_source_list(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.RulesSourceListProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.RulesSourceProperty.RulesSourceList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-rulessourcelist
            """
            result = self._values.get("rules_source_list")
            return result

        @builtins.property
        def rules_string(self) -> typing.Optional[builtins.str]:
            """``CfnRuleGroup.RulesSourceProperty.RulesString``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-rulesstring
            """
            result = self._values.get("rules_string")
            return result

        @builtins.property
        def stateful_rules(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.StatefulRulesProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.RulesSourceProperty.StatefulRules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-statefulrules
            """
            result = self._values.get("stateful_rules")
            return result

        @builtins.property
        def stateless_rules_and_custom_actions(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.StatelessRulesAndCustomActionsProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.RulesSourceProperty.StatelessRulesAndCustomActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-statelessrulesandcustomactions
            """
            result = self._values.get("stateless_rules_and_custom_actions")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RulesSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.StatefulRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "header": "header",
            "rule_options": "ruleOptions",
        },
    )
    class StatefulRuleProperty:
        def __init__(
            self,
            *,
            action: builtins.str,
            header: typing.Union["CfnRuleGroup.HeaderProperty", _IResolvable_a771d0ef],
            rule_options: typing.Union["CfnRuleGroup.RuleOptionsProperty", _IResolvable_a771d0ef],
        ) -> None:
            """
            :param action: ``CfnRuleGroup.StatefulRuleProperty.Action``.
            :param header: ``CfnRuleGroup.StatefulRuleProperty.Header``.
            :param rule_options: ``CfnRuleGroup.StatefulRuleProperty.RuleOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "action": action,
                "header": header,
                "rule_options": rule_options,
            }

        @builtins.property
        def action(self) -> builtins.str:
            """``CfnRuleGroup.StatefulRuleProperty.Action``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html#cfn-networkfirewall-rulegroup-statefulrule-action
            """
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return result

        @builtins.property
        def header(
            self,
        ) -> typing.Union["CfnRuleGroup.HeaderProperty", _IResolvable_a771d0ef]:
            """``CfnRuleGroup.StatefulRuleProperty.Header``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html#cfn-networkfirewall-rulegroup-statefulrule-header
            """
            result = self._values.get("header")
            assert result is not None, "Required property 'header' is missing"
            return result

        @builtins.property
        def rule_options(
            self,
        ) -> typing.Union["CfnRuleGroup.RuleOptionsProperty", _IResolvable_a771d0ef]:
            """``CfnRuleGroup.StatefulRuleProperty.RuleOptions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html#cfn-networkfirewall-rulegroup-statefulrule-ruleoptions
            """
            result = self._values.get("rule_options")
            assert result is not None, "Required property 'rule_options' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.StatefulRulesProperty",
        jsii_struct_bases=[],
        name_mapping={"stateful_rules": "statefulRules"},
    )
    class StatefulRulesProperty:
        def __init__(
            self,
            *,
            stateful_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatefulRuleProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param stateful_rules: ``CfnRuleGroup.StatefulRulesProperty.StatefulRules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrules.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if stateful_rules is not None:
                self._values["stateful_rules"] = stateful_rules

        @builtins.property
        def stateful_rules(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatefulRuleProperty", _IResolvable_a771d0ef]]]]:
            """``CfnRuleGroup.StatefulRulesProperty.StatefulRules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrules.html#cfn-networkfirewall-rulegroup-statefulrules-statefulrules
            """
            result = self._values.get("stateful_rules")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRulesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.StatelessRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "rule_definition": "ruleDefinition"},
    )
    class StatelessRuleProperty:
        def __init__(
            self,
            *,
            priority: jsii.Number,
            rule_definition: typing.Union["CfnRuleGroup.RuleDefinitionProperty", _IResolvable_a771d0ef],
        ) -> None:
            """
            :param priority: ``CfnRuleGroup.StatelessRuleProperty.Priority``.
            :param rule_definition: ``CfnRuleGroup.StatelessRuleProperty.RuleDefinition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrule.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "priority": priority,
                "rule_definition": rule_definition,
            }

        @builtins.property
        def priority(self) -> jsii.Number:
            """``CfnRuleGroup.StatelessRuleProperty.Priority``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrule.html#cfn-networkfirewall-rulegroup-statelessrule-priority
            """
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return result

        @builtins.property
        def rule_definition(
            self,
        ) -> typing.Union["CfnRuleGroup.RuleDefinitionProperty", _IResolvable_a771d0ef]:
            """``CfnRuleGroup.StatelessRuleProperty.RuleDefinition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrule.html#cfn-networkfirewall-rulegroup-statelessrule-ruledefinition
            """
            result = self._values.get("rule_definition")
            assert result is not None, "Required property 'rule_definition' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.StatelessRulesAndCustomActionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "stateless_rules": "statelessRules",
            "custom_actions": "customActions",
        },
    )
    class StatelessRulesAndCustomActionsProperty:
        def __init__(
            self,
            *,
            stateless_rules: typing.Union["CfnRuleGroup.StatelessRulesProperty", _IResolvable_a771d0ef],
            custom_actions: typing.Optional[typing.Union["CfnRuleGroup.CustomActionsProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param stateless_rules: ``CfnRuleGroup.StatelessRulesAndCustomActionsProperty.StatelessRules``.
            :param custom_actions: ``CfnRuleGroup.StatelessRulesAndCustomActionsProperty.CustomActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrulesandcustomactions.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "stateless_rules": stateless_rules,
            }
            if custom_actions is not None:
                self._values["custom_actions"] = custom_actions

        @builtins.property
        def stateless_rules(
            self,
        ) -> typing.Union["CfnRuleGroup.StatelessRulesProperty", _IResolvable_a771d0ef]:
            """``CfnRuleGroup.StatelessRulesAndCustomActionsProperty.StatelessRules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrulesandcustomactions.html#cfn-networkfirewall-rulegroup-statelessrulesandcustomactions-statelessrules
            """
            result = self._values.get("stateless_rules")
            assert result is not None, "Required property 'stateless_rules' is missing"
            return result

        @builtins.property
        def custom_actions(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.CustomActionsProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.StatelessRulesAndCustomActionsProperty.CustomActions``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrulesandcustomactions.html#cfn-networkfirewall-rulegroup-statelessrulesandcustomactions-customactions
            """
            result = self._values.get("custom_actions")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRulesAndCustomActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.StatelessRulesProperty",
        jsii_struct_bases=[],
        name_mapping={"stateless_rules": "statelessRules"},
    )
    class StatelessRulesProperty:
        def __init__(
            self,
            *,
            stateless_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatelessRuleProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param stateless_rules: ``CfnRuleGroup.StatelessRulesProperty.StatelessRules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrules.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if stateless_rules is not None:
                self._values["stateless_rules"] = stateless_rules

        @builtins.property
        def stateless_rules(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatelessRuleProperty", _IResolvable_a771d0ef]]]]:
            """``CfnRuleGroup.StatelessRulesProperty.StatelessRules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrules.html#cfn-networkfirewall-rulegroup-statelessrules-statelessrules
            """
            result = self._values.get("stateless_rules")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRulesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.TCPFlagFieldProperty",
        jsii_struct_bases=[],
        name_mapping={"flags": "flags", "masks": "masks"},
    )
    class TCPFlagFieldProperty:
        def __init__(
            self,
            *,
            flags: typing.Union["CfnRuleGroup.FlagsProperty", _IResolvable_a771d0ef],
            masks: typing.Optional[typing.Union["CfnRuleGroup.FlagsProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param flags: ``CfnRuleGroup.TCPFlagFieldProperty.Flags``.
            :param masks: ``CfnRuleGroup.TCPFlagFieldProperty.Masks``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tcpflagfield.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "flags": flags,
            }
            if masks is not None:
                self._values["masks"] = masks

        @builtins.property
        def flags(
            self,
        ) -> typing.Union["CfnRuleGroup.FlagsProperty", _IResolvable_a771d0ef]:
            """``CfnRuleGroup.TCPFlagFieldProperty.Flags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tcpflagfield.html#cfn-networkfirewall-rulegroup-tcpflagfield-flags
            """
            result = self._values.get("flags")
            assert result is not None, "Required property 'flags' is missing"
            return result

        @builtins.property
        def masks(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.FlagsProperty", _IResolvable_a771d0ef]]:
            """``CfnRuleGroup.TCPFlagFieldProperty.Masks``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tcpflagfield.html#cfn-networkfirewall-rulegroup-tcpflagfield-masks
            """
            result = self._values.get("masks")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TCPFlagFieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.TCPFlagsProperty",
        jsii_struct_bases=[],
        name_mapping={"tcp_flags": "tcpFlags"},
    )
    class TCPFlagsProperty:
        def __init__(
            self,
            *,
            tcp_flags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TCPFlagFieldProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            """
            :param tcp_flags: ``CfnRuleGroup.TCPFlagsProperty.TCPFlags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tcpflags.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if tcp_flags is not None:
                self._values["tcp_flags"] = tcp_flags

        @builtins.property
        def tcp_flags(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TCPFlagFieldProperty", _IResolvable_a771d0ef]]]]:
            """``CfnRuleGroup.TCPFlagsProperty.TCPFlags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tcpflags.html#cfn-networkfirewall-rulegroup-tcpflags-tcpflags
            """
            result = self._values.get("tcp_flags")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TCPFlagsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.TagsProperty",
        jsii_struct_bases=[],
        name_mapping={"tags": "tags"},
    )
    class TagsProperty:
        def __init__(
            self,
            *,
            tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        ) -> None:
            """
            :param tags: ``CfnRuleGroup.TagsProperty.Tags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tags.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
            """``CfnRuleGroup.TagsProperty.Tags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tags.html#cfn-networkfirewall-rulegroup-tags-tags
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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.TargetTypesProperty",
        jsii_struct_bases=[],
        name_mapping={"target_types": "targetTypes"},
    )
    class TargetTypesProperty:
        def __init__(
            self,
            *,
            target_types: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param target_types: ``CfnRuleGroup.TargetTypesProperty.TargetTypes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-targettypes.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if target_types is not None:
                self._values["target_types"] = target_types

        @builtins.property
        def target_types(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnRuleGroup.TargetTypesProperty.TargetTypes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-targettypes.html#cfn-networkfirewall-rulegroup-targettypes-targettypes
            """
            result = self._values.get("target_types")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetTypesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.VariableDefinitionListProperty",
        jsii_struct_bases=[],
        name_mapping={"variable_definition_list": "variableDefinitionList"},
    )
    class VariableDefinitionListProperty:
        def __init__(
            self,
            *,
            variable_definition_list: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param variable_definition_list: ``CfnRuleGroup.VariableDefinitionListProperty.VariableDefinitionList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-variabledefinitionlist.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if variable_definition_list is not None:
                self._values["variable_definition_list"] = variable_definition_list

        @builtins.property
        def variable_definition_list(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnRuleGroup.VariableDefinitionListProperty.VariableDefinitionList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-variabledefinitionlist.html#cfn-networkfirewall-rulegroup-variabledefinitionlist-variabledefinitionlist
            """
            result = self._values.get("variable_definition_list")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VariableDefinitionListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_networkfirewall.CfnRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "rule_group_name": "ruleGroupName",
        "type": "type",
        "description": "description",
        "rule_group": "ruleGroup",
        "rule_group_id": "ruleGroupId",
        "tags": "tags",
    },
)
class CfnRuleGroupProps:
    def __init__(
        self,
        *,
        capacity: jsii.Number,
        rule_group_name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        rule_group: typing.Optional[typing.Union[CfnRuleGroup.RuleGroupProperty, _IResolvable_a771d0ef]] = None,
        rule_group_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[CfnRuleGroup.TagsProperty] = None,
    ) -> None:
        """Properties for defining a ``AWS::NetworkFirewall::RuleGroup``.

        :param capacity: ``AWS::NetworkFirewall::RuleGroup.Capacity``.
        :param rule_group_name: ``AWS::NetworkFirewall::RuleGroup.RuleGroupName``.
        :param type: ``AWS::NetworkFirewall::RuleGroup.Type``.
        :param description: ``AWS::NetworkFirewall::RuleGroup.Description``.
        :param rule_group: ``AWS::NetworkFirewall::RuleGroup.RuleGroup``.
        :param rule_group_id: ``AWS::NetworkFirewall::RuleGroup.RuleGroupId``.
        :param tags: ``AWS::NetworkFirewall::RuleGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html
        """
        if isinstance(tags, dict):
            tags = CfnRuleGroup.TagsProperty(**tags)
        self._values: typing.Dict[str, typing.Any] = {
            "capacity": capacity,
            "rule_group_name": rule_group_name,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if rule_group is not None:
            self._values["rule_group"] = rule_group
        if rule_group_id is not None:
            self._values["rule_group_id"] = rule_group_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def capacity(self) -> jsii.Number:
        """``AWS::NetworkFirewall::RuleGroup.Capacity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-capacity
        """
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return result

    @builtins.property
    def rule_group_name(self) -> builtins.str:
        """``AWS::NetworkFirewall::RuleGroup.RuleGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroupname
        """
        result = self._values.get("rule_group_name")
        assert result is not None, "Required property 'rule_group_name' is missing"
        return result

    @builtins.property
    def type(self) -> builtins.str:
        """``AWS::NetworkFirewall::RuleGroup.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-type
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkFirewall::RuleGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def rule_group(
        self,
    ) -> typing.Optional[typing.Union[CfnRuleGroup.RuleGroupProperty, _IResolvable_a771d0ef]]:
        """``AWS::NetworkFirewall::RuleGroup.RuleGroup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup
        """
        result = self._values.get("rule_group")
        return result

    @builtins.property
    def rule_group_id(self) -> typing.Optional[builtins.str]:
        """``AWS::NetworkFirewall::RuleGroup.RuleGroupId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroupid
        """
        result = self._values.get("rule_group_id")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[CfnRuleGroup.TagsProperty]:
        """``AWS::NetworkFirewall::RuleGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnFirewall",
    "CfnFirewallPolicy",
    "CfnFirewallPolicyProps",
    "CfnFirewallProps",
    "CfnLoggingConfiguration",
    "CfnLoggingConfigurationProps",
    "CfnRuleGroup",
    "CfnRuleGroupProps",
]

publication.publish()
