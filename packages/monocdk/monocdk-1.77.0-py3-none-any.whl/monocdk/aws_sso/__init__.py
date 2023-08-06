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
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnAssignment(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sso.CfnAssignment",
):
    """A CloudFormation ``AWS::SSO::Assignment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html
    :cloudformationResource: AWS::SSO::Assignment
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        permission_set_arn: builtins.str,
        principal_id: builtins.str,
        principal_type: builtins.str,
        target_id: builtins.str,
        target_type: builtins.str,
    ) -> None:
        """Create a new ``AWS::SSO::Assignment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: ``AWS::SSO::Assignment.InstanceArn``.
        :param permission_set_arn: ``AWS::SSO::Assignment.PermissionSetArn``.
        :param principal_id: ``AWS::SSO::Assignment.PrincipalId``.
        :param principal_type: ``AWS::SSO::Assignment.PrincipalType``.
        :param target_id: ``AWS::SSO::Assignment.TargetId``.
        :param target_type: ``AWS::SSO::Assignment.TargetType``.
        """
        props = CfnAssignmentProps(
            instance_arn=instance_arn,
            permission_set_arn=permission_set_arn,
            principal_id=principal_id,
            principal_type=principal_type,
            target_id=target_id,
            target_type=target_type,
        )

        jsii.create(CfnAssignment, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        """``AWS::SSO::Assignment.InstanceArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-instancearn
        """
        return jsii.get(self, "instanceArn")

    @instance_arn.setter # type: ignore
    def instance_arn(self, value: builtins.str) -> None:
        jsii.set(self, "instanceArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="permissionSetArn")
    def permission_set_arn(self) -> builtins.str:
        """``AWS::SSO::Assignment.PermissionSetArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-permissionsetarn
        """
        return jsii.get(self, "permissionSetArn")

    @permission_set_arn.setter # type: ignore
    def permission_set_arn(self, value: builtins.str) -> None:
        jsii.set(self, "permissionSetArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        """``AWS::SSO::Assignment.PrincipalId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-principalid
        """
        return jsii.get(self, "principalId")

    @principal_id.setter # type: ignore
    def principal_id(self, value: builtins.str) -> None:
        jsii.set(self, "principalId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="principalType")
    def principal_type(self) -> builtins.str:
        """``AWS::SSO::Assignment.PrincipalType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-principaltype
        """
        return jsii.get(self, "principalType")

    @principal_type.setter # type: ignore
    def principal_type(self, value: builtins.str) -> None:
        jsii.set(self, "principalType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetId")
    def target_id(self) -> builtins.str:
        """``AWS::SSO::Assignment.TargetId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-targetid
        """
        return jsii.get(self, "targetId")

    @target_id.setter # type: ignore
    def target_id(self, value: builtins.str) -> None:
        jsii.set(self, "targetId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetType")
    def target_type(self) -> builtins.str:
        """``AWS::SSO::Assignment.TargetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-targettype
        """
        return jsii.get(self, "targetType")

    @target_type.setter # type: ignore
    def target_type(self, value: builtins.str) -> None:
        jsii.set(self, "targetType", value)


@jsii.data_type(
    jsii_type="monocdk.aws_sso.CfnAssignmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "permission_set_arn": "permissionSetArn",
        "principal_id": "principalId",
        "principal_type": "principalType",
        "target_id": "targetId",
        "target_type": "targetType",
    },
)
class CfnAssignmentProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        permission_set_arn: builtins.str,
        principal_id: builtins.str,
        principal_type: builtins.str,
        target_id: builtins.str,
        target_type: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::SSO::Assignment``.

        :param instance_arn: ``AWS::SSO::Assignment.InstanceArn``.
        :param permission_set_arn: ``AWS::SSO::Assignment.PermissionSetArn``.
        :param principal_id: ``AWS::SSO::Assignment.PrincipalId``.
        :param principal_type: ``AWS::SSO::Assignment.PrincipalType``.
        :param target_id: ``AWS::SSO::Assignment.TargetId``.
        :param target_type: ``AWS::SSO::Assignment.TargetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "instance_arn": instance_arn,
            "permission_set_arn": permission_set_arn,
            "principal_id": principal_id,
            "principal_type": principal_type,
            "target_id": target_id,
            "target_type": target_type,
        }

    @builtins.property
    def instance_arn(self) -> builtins.str:
        """``AWS::SSO::Assignment.InstanceArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-instancearn
        """
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return result

    @builtins.property
    def permission_set_arn(self) -> builtins.str:
        """``AWS::SSO::Assignment.PermissionSetArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-permissionsetarn
        """
        result = self._values.get("permission_set_arn")
        assert result is not None, "Required property 'permission_set_arn' is missing"
        return result

    @builtins.property
    def principal_id(self) -> builtins.str:
        """``AWS::SSO::Assignment.PrincipalId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-principalid
        """
        result = self._values.get("principal_id")
        assert result is not None, "Required property 'principal_id' is missing"
        return result

    @builtins.property
    def principal_type(self) -> builtins.str:
        """``AWS::SSO::Assignment.PrincipalType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-principaltype
        """
        result = self._values.get("principal_type")
        assert result is not None, "Required property 'principal_type' is missing"
        return result

    @builtins.property
    def target_id(self) -> builtins.str:
        """``AWS::SSO::Assignment.TargetId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-targetid
        """
        result = self._values.get("target_id")
        assert result is not None, "Required property 'target_id' is missing"
        return result

    @builtins.property
    def target_type(self) -> builtins.str:
        """``AWS::SSO::Assignment.TargetType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-targettype
        """
        result = self._values.get("target_type")
        assert result is not None, "Required property 'target_type' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssignmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPermissionSet(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_sso.CfnPermissionSet",
):
    """A CloudFormation ``AWS::SSO::PermissionSet``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html
    :cloudformationResource: AWS::SSO::PermissionSet
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        inline_policy: typing.Optional[builtins.str] = None,
        managed_policies: typing.Optional[typing.List[builtins.str]] = None,
        relay_state_type: typing.Optional[builtins.str] = None,
        session_duration: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::SSO::PermissionSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: ``AWS::SSO::PermissionSet.InstanceArn``.
        :param name: ``AWS::SSO::PermissionSet.Name``.
        :param description: ``AWS::SSO::PermissionSet.Description``.
        :param inline_policy: ``AWS::SSO::PermissionSet.InlinePolicy``.
        :param managed_policies: ``AWS::SSO::PermissionSet.ManagedPolicies``.
        :param relay_state_type: ``AWS::SSO::PermissionSet.RelayStateType``.
        :param session_duration: ``AWS::SSO::PermissionSet.SessionDuration``.
        :param tags: ``AWS::SSO::PermissionSet.Tags``.
        """
        props = CfnPermissionSetProps(
            instance_arn=instance_arn,
            name=name,
            description=description,
            inline_policy=inline_policy,
            managed_policies=managed_policies,
            relay_state_type=relay_state_type,
            session_duration=session_duration,
            tags=tags,
        )

        jsii.create(CfnPermissionSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrPermissionSetArn")
    def attr_permission_set_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: PermissionSetArn
        """
        return jsii.get(self, "attrPermissionSetArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::SSO::PermissionSet.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        """``AWS::SSO::PermissionSet.InstanceArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-instancearn
        """
        return jsii.get(self, "instanceArn")

    @instance_arn.setter # type: ignore
    def instance_arn(self, value: builtins.str) -> None:
        jsii.set(self, "instanceArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::SSO::PermissionSet.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSO::PermissionSet.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="inlinePolicy")
    def inline_policy(self) -> typing.Optional[builtins.str]:
        """``AWS::SSO::PermissionSet.InlinePolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-inlinepolicy
        """
        return jsii.get(self, "inlinePolicy")

    @inline_policy.setter # type: ignore
    def inline_policy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "inlinePolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="managedPolicies")
    def managed_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::SSO::PermissionSet.ManagedPolicies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-managedpolicies
        """
        return jsii.get(self, "managedPolicies")

    @managed_policies.setter # type: ignore
    def managed_policies(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "managedPolicies", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="relayStateType")
    def relay_state_type(self) -> typing.Optional[builtins.str]:
        """``AWS::SSO::PermissionSet.RelayStateType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-relaystatetype
        """
        return jsii.get(self, "relayStateType")

    @relay_state_type.setter # type: ignore
    def relay_state_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "relayStateType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sessionDuration")
    def session_duration(self) -> typing.Optional[builtins.str]:
        """``AWS::SSO::PermissionSet.SessionDuration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-sessionduration
        """
        return jsii.get(self, "sessionDuration")

    @session_duration.setter # type: ignore
    def session_duration(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sessionDuration", value)


@jsii.data_type(
    jsii_type="monocdk.aws_sso.CfnPermissionSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "name": "name",
        "description": "description",
        "inline_policy": "inlinePolicy",
        "managed_policies": "managedPolicies",
        "relay_state_type": "relayStateType",
        "session_duration": "sessionDuration",
        "tags": "tags",
    },
)
class CfnPermissionSetProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        inline_policy: typing.Optional[builtins.str] = None,
        managed_policies: typing.Optional[typing.List[builtins.str]] = None,
        relay_state_type: typing.Optional[builtins.str] = None,
        session_duration: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::SSO::PermissionSet``.

        :param instance_arn: ``AWS::SSO::PermissionSet.InstanceArn``.
        :param name: ``AWS::SSO::PermissionSet.Name``.
        :param description: ``AWS::SSO::PermissionSet.Description``.
        :param inline_policy: ``AWS::SSO::PermissionSet.InlinePolicy``.
        :param managed_policies: ``AWS::SSO::PermissionSet.ManagedPolicies``.
        :param relay_state_type: ``AWS::SSO::PermissionSet.RelayStateType``.
        :param session_duration: ``AWS::SSO::PermissionSet.SessionDuration``.
        :param tags: ``AWS::SSO::PermissionSet.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "instance_arn": instance_arn,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if inline_policy is not None:
            self._values["inline_policy"] = inline_policy
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if relay_state_type is not None:
            self._values["relay_state_type"] = relay_state_type
        if session_duration is not None:
            self._values["session_duration"] = session_duration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_arn(self) -> builtins.str:
        """``AWS::SSO::PermissionSet.InstanceArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-instancearn
        """
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::SSO::PermissionSet.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::SSO::PermissionSet.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def inline_policy(self) -> typing.Optional[builtins.str]:
        """``AWS::SSO::PermissionSet.InlinePolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-inlinepolicy
        """
        result = self._values.get("inline_policy")
        return result

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::SSO::PermissionSet.ManagedPolicies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-managedpolicies
        """
        result = self._values.get("managed_policies")
        return result

    @builtins.property
    def relay_state_type(self) -> typing.Optional[builtins.str]:
        """``AWS::SSO::PermissionSet.RelayStateType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-relaystatetype
        """
        result = self._values.get("relay_state_type")
        return result

    @builtins.property
    def session_duration(self) -> typing.Optional[builtins.str]:
        """``AWS::SSO::PermissionSet.SessionDuration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-sessionduration
        """
        result = self._values.get("session_duration")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::SSO::PermissionSet.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPermissionSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAssignment",
    "CfnAssignmentProps",
    "CfnPermissionSet",
    "CfnPermissionSetProps",
]

publication.publish()
