import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import constructs
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_iam import (
    AddToResourcePolicyResult as _AddToResourcePolicyResult_0fd9d2a9,
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IPrincipal as _IPrincipal_93b48231,
    PolicyDocument as _PolicyDocument_b5de5177,
    PolicyStatement as _PolicyStatement_296fe8a3,
    PrincipalBase as _PrincipalBase_2c3968ff,
    PrincipalPolicyFragment as _PrincipalPolicyFragment_e6a0f9e3,
)


@jsii.data_type(
    jsii_type="monocdk.aws_kms.AliasAttributes",
    jsii_struct_bases=[],
    name_mapping={"alias_name": "aliasName", "alias_target_key": "aliasTargetKey"},
)
class AliasAttributes:
    def __init__(self, *, alias_name: builtins.str, alias_target_key: "IKey") -> None:
        """(experimental) Properties of a reference to an existing KMS Alias.

        :param alias_name: (experimental) Specifies the alias name. This value must begin with alias/ followed by a name (i.e. alias/ExampleAlias)
        :param alias_target_key: (experimental) The customer master key (CMK) to which the Alias refers.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "alias_name": alias_name,
            "alias_target_key": alias_target_key,
        }

    @builtins.property
    def alias_name(self) -> builtins.str:
        """(experimental) Specifies the alias name.

        This value must begin with alias/ followed by a name (i.e. alias/ExampleAlias)

        :stability: experimental
        """
        result = self._values.get("alias_name")
        assert result is not None, "Required property 'alias_name' is missing"
        return result

    @builtins.property
    def alias_target_key(self) -> "IKey":
        """(experimental) The customer master key (CMK) to which the Alias refers.

        :stability: experimental
        """
        result = self._values.get("alias_target_key")
        assert result is not None, "Required property 'alias_target_key' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AliasAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_kms.AliasProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias_name": "aliasName",
        "target_key": "targetKey",
        "removal_policy": "removalPolicy",
    },
)
class AliasProps:
    def __init__(
        self,
        *,
        alias_name: builtins.str,
        target_key: "IKey",
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        """(experimental) Construction properties for a KMS Key Alias object.

        :param alias_name: (experimental) The name of the alias. The name must start with alias followed by a forward slash, such as alias/. You can't specify aliases that begin with alias/AWS. These aliases are reserved.
        :param target_key: (experimental) The ID of the key for which you are creating the alias. Specify the key's globally unique identifier or Amazon Resource Name (ARN). You can't specify another alias.
        :param removal_policy: (experimental) Policy to apply when the alias is removed from this stack. Default: - The alias will be deleted

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "alias_name": alias_name,
            "target_key": target_key,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def alias_name(self) -> builtins.str:
        """(experimental) The name of the alias.

        The name must start with alias followed by a
        forward slash, such as alias/. You can't specify aliases that begin with
        alias/AWS. These aliases are reserved.

        :stability: experimental
        """
        result = self._values.get("alias_name")
        assert result is not None, "Required property 'alias_name' is missing"
        return result

    @builtins.property
    def target_key(self) -> "IKey":
        """(experimental) The ID of the key for which you are creating the alias.

        Specify the key's
        globally unique identifier or Amazon Resource Name (ARN). You can't
        specify another alias.

        :stability: experimental
        """
        result = self._values.get("target_key")
        assert result is not None, "Required property 'target_key' is missing"
        return result

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        """(experimental) Policy to apply when the alias is removed from this stack.

        :default: - The alias will be deleted

        :stability: experimental
        """
        result = self._values.get("removal_policy")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAlias(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kms.CfnAlias",
):
    """A CloudFormation ``AWS::KMS::Alias``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html
    :cloudformationResource: AWS::KMS::Alias
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        alias_name: builtins.str,
        target_key_id: builtins.str,
    ) -> None:
        """Create a new ``AWS::KMS::Alias``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param alias_name: ``AWS::KMS::Alias.AliasName``.
        :param target_key_id: ``AWS::KMS::Alias.TargetKeyId``.
        """
        props = CfnAliasProps(alias_name=alias_name, target_key_id=target_key_id)

        jsii.create(CfnAlias, self, [scope, id, props])

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
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> builtins.str:
        """``AWS::KMS::Alias.AliasName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-aliasname
        """
        return jsii.get(self, "aliasName")

    @alias_name.setter # type: ignore
    def alias_name(self, value: builtins.str) -> None:
        jsii.set(self, "aliasName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetKeyId")
    def target_key_id(self) -> builtins.str:
        """``AWS::KMS::Alias.TargetKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-targetkeyid
        """
        return jsii.get(self, "targetKeyId")

    @target_key_id.setter # type: ignore
    def target_key_id(self, value: builtins.str) -> None:
        jsii.set(self, "targetKeyId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_kms.CfnAliasProps",
    jsii_struct_bases=[],
    name_mapping={"alias_name": "aliasName", "target_key_id": "targetKeyId"},
)
class CfnAliasProps:
    def __init__(
        self,
        *,
        alias_name: builtins.str,
        target_key_id: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::KMS::Alias``.

        :param alias_name: ``AWS::KMS::Alias.AliasName``.
        :param target_key_id: ``AWS::KMS::Alias.TargetKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "alias_name": alias_name,
            "target_key_id": target_key_id,
        }

    @builtins.property
    def alias_name(self) -> builtins.str:
        """``AWS::KMS::Alias.AliasName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-aliasname
        """
        result = self._values.get("alias_name")
        assert result is not None, "Required property 'alias_name' is missing"
        return result

    @builtins.property
    def target_key_id(self) -> builtins.str:
        """``AWS::KMS::Alias.TargetKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-targetkeyid
        """
        result = self._values.get("target_key_id")
        assert result is not None, "Required property 'target_key_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnKey(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kms.CfnKey",
):
    """A CloudFormation ``AWS::KMS::Key``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html
    :cloudformationResource: AWS::KMS::Key
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        key_policy: typing.Any,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        enable_key_rotation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        key_spec: typing.Optional[builtins.str] = None,
        key_usage: typing.Optional[builtins.str] = None,
        pending_window_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::KMS::Key``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param key_policy: ``AWS::KMS::Key.KeyPolicy``.
        :param description: ``AWS::KMS::Key.Description``.
        :param enabled: ``AWS::KMS::Key.Enabled``.
        :param enable_key_rotation: ``AWS::KMS::Key.EnableKeyRotation``.
        :param key_spec: ``AWS::KMS::Key.KeySpec``.
        :param key_usage: ``AWS::KMS::Key.KeyUsage``.
        :param pending_window_in_days: ``AWS::KMS::Key.PendingWindowInDays``.
        :param tags: ``AWS::KMS::Key.Tags``.
        """
        props = CfnKeyProps(
            key_policy=key_policy,
            description=description,
            enabled=enabled,
            enable_key_rotation=enable_key_rotation,
            key_spec=key_spec,
            key_usage=key_usage,
            pending_window_in_days=pending_window_in_days,
            tags=tags,
        )

        jsii.create(CfnKey, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrKeyId")
    def attr_key_id(self) -> builtins.str:
        """
        :cloudformationAttribute: KeyId
        """
        return jsii.get(self, "attrKeyId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::KMS::Key.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyPolicy")
    def key_policy(self) -> typing.Any:
        """``AWS::KMS::Key.KeyPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keypolicy
        """
        return jsii.get(self, "keyPolicy")

    @key_policy.setter # type: ignore
    def key_policy(self, value: typing.Any) -> None:
        jsii.set(self, "keyPolicy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::KMS::Key.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::KMS::Key.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enableKeyRotation")
    def enable_key_rotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::KMS::Key.EnableKeyRotation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enablekeyrotation
        """
        return jsii.get(self, "enableKeyRotation")

    @enable_key_rotation.setter # type: ignore
    def enable_key_rotation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "enableKeyRotation", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keySpec")
    def key_spec(self) -> typing.Optional[builtins.str]:
        """``AWS::KMS::Key.KeySpec``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keyspec
        """
        return jsii.get(self, "keySpec")

    @key_spec.setter # type: ignore
    def key_spec(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "keySpec", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyUsage")
    def key_usage(self) -> typing.Optional[builtins.str]:
        """``AWS::KMS::Key.KeyUsage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keyusage
        """
        return jsii.get(self, "keyUsage")

    @key_usage.setter # type: ignore
    def key_usage(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "keyUsage", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="pendingWindowInDays")
    def pending_window_in_days(self) -> typing.Optional[jsii.Number]:
        """``AWS::KMS::Key.PendingWindowInDays``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-pendingwindowindays
        """
        return jsii.get(self, "pendingWindowInDays")

    @pending_window_in_days.setter # type: ignore
    def pending_window_in_days(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "pendingWindowInDays", value)


@jsii.data_type(
    jsii_type="monocdk.aws_kms.CfnKeyProps",
    jsii_struct_bases=[],
    name_mapping={
        "key_policy": "keyPolicy",
        "description": "description",
        "enabled": "enabled",
        "enable_key_rotation": "enableKeyRotation",
        "key_spec": "keySpec",
        "key_usage": "keyUsage",
        "pending_window_in_days": "pendingWindowInDays",
        "tags": "tags",
    },
)
class CfnKeyProps:
    def __init__(
        self,
        *,
        key_policy: typing.Any,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        enable_key_rotation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        key_spec: typing.Optional[builtins.str] = None,
        key_usage: typing.Optional[builtins.str] = None,
        pending_window_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::KMS::Key``.

        :param key_policy: ``AWS::KMS::Key.KeyPolicy``.
        :param description: ``AWS::KMS::Key.Description``.
        :param enabled: ``AWS::KMS::Key.Enabled``.
        :param enable_key_rotation: ``AWS::KMS::Key.EnableKeyRotation``.
        :param key_spec: ``AWS::KMS::Key.KeySpec``.
        :param key_usage: ``AWS::KMS::Key.KeyUsage``.
        :param pending_window_in_days: ``AWS::KMS::Key.PendingWindowInDays``.
        :param tags: ``AWS::KMS::Key.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "key_policy": key_policy,
        }
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_key_rotation is not None:
            self._values["enable_key_rotation"] = enable_key_rotation
        if key_spec is not None:
            self._values["key_spec"] = key_spec
        if key_usage is not None:
            self._values["key_usage"] = key_usage
        if pending_window_in_days is not None:
            self._values["pending_window_in_days"] = pending_window_in_days
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def key_policy(self) -> typing.Any:
        """``AWS::KMS::Key.KeyPolicy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keypolicy
        """
        result = self._values.get("key_policy")
        assert result is not None, "Required property 'key_policy' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::KMS::Key.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::KMS::Key.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enabled
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def enable_key_rotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::KMS::Key.EnableKeyRotation``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enablekeyrotation
        """
        result = self._values.get("enable_key_rotation")
        return result

    @builtins.property
    def key_spec(self) -> typing.Optional[builtins.str]:
        """``AWS::KMS::Key.KeySpec``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keyspec
        """
        result = self._values.get("key_spec")
        return result

    @builtins.property
    def key_usage(self) -> typing.Optional[builtins.str]:
        """``AWS::KMS::Key.KeyUsage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keyusage
        """
        result = self._values.get("key_usage")
        return result

    @builtins.property
    def pending_window_in_days(self) -> typing.Optional[jsii.Number]:
        """``AWS::KMS::Key.PendingWindowInDays``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-pendingwindowindays
        """
        result = self._values.get("pending_window_in_days")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::KMS::Key.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_kms.IKey")
class IKey(_IResource_8c1dbbbd, typing_extensions.Protocol):
    """(experimental) A KMS Key, either managed by this CDK app, or imported.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IKeyProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        """(experimental) The ARN of the key.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        """(experimental) The ID of the key (the part that looks something like: 1234abcd-12ab-34cd-56ef-1234567890ab).

        :stability: experimental
        :attribute: true
        """
        ...

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: builtins.str) -> "Alias":
        """(experimental) Defines a new alias for the key.

        :param alias: -

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
        allow_no_op: typing.Optional[builtins.bool] = None,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        """(experimental) Adds a statement to the KMS key resource policy.

        :param statement: The policy statement to add.
        :param allow_no_op: If this is set to ``false`` and there is no policy defined (i.e. external key), the operation will fail. Otherwise, it will no-op.

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        """(experimental) Grant the indicated permissions on this key to the given principal.

        :param grantee: -
        :param actions: -

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant decryption permissions using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant encryption permissions using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant encryption and decryption permissions using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        ...


class _IKeyProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore
):
    """(experimental) A KMS Key, either managed by this CDK app, or imported.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_kms.IKey"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        """(experimental) The ARN of the key.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "keyArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        """(experimental) The ID of the key (the part that looks something like: 1234abcd-12ab-34cd-56ef-1234567890ab).

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "keyId")

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: builtins.str) -> "Alias":
        """(experimental) Defines a new alias for the key.

        :param alias: -

        :stability: experimental
        """
        return jsii.invoke(self, "addAlias", [alias])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
        allow_no_op: typing.Optional[builtins.bool] = None,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        """(experimental) Adds a statement to the KMS key resource policy.

        :param statement: The policy statement to add.
        :param allow_no_op: If this is set to ``false`` and there is no policy defined (i.e. external key), the operation will fail. Otherwise, it will no-op.

        :stability: experimental
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement, allow_no_op])

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        """(experimental) Grant the indicated permissions on this key to the given principal.

        :param grantee: -
        :param actions: -

        :stability: experimental
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant decryption permissions using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantDecrypt", [grantee])

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant encryption permissions using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantEncrypt", [grantee])

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant encryption and decryption permissions using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantEncryptDecrypt", [grantee])


@jsii.implements(IKey)
class Key(_Resource_abff4495, metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_kms.Key"):
    """(experimental) Defines a KMS key.

    :stability: experimental
    :resource: AWS::KMS::Key
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        policy: typing.Optional[_PolicyDocument_b5de5177] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        trust_account_identities: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param alias: (experimental) Initial alias to add to the key. More aliases can be added later by calling ``addAlias``. Default: - No alias is added for the key.
        :param description: (experimental) A description of the key. Use a description that helps your users decide whether the key is appropriate for a particular task. Default: - No description.
        :param enabled: (experimental) Indicates whether the key is available for use. Default: - Key is enabled.
        :param enable_key_rotation: (experimental) Indicates whether AWS KMS rotates the key. Default: false
        :param policy: (experimental) Custom policy document to attach to the KMS key. Default: - A policy document with permissions for the account root to administer the key will be created.
        :param removal_policy: (experimental) Whether the encryption key should be retained when it is removed from the Stack. This is useful when one wants to retain access to data that was encrypted with a key that is being retired. Default: RemovalPolicy.Retain
        :param trust_account_identities: (experimental) Whether the key usage can be granted by IAM policies. Setting this to true adds a default statement which delegates key access control completely to the identity's IAM policy (similar to how it works for other AWS resources). Default: false

        :stability: experimental
        """
        props = KeyProps(
            alias=alias,
            description=description,
            enabled=enabled,
            enable_key_rotation=enable_key_rotation,
            policy=policy,
            removal_policy=removal_policy,
            trust_account_identities=trust_account_identities,
        )

        jsii.create(Key, self, [scope, id, props])

    @jsii.member(jsii_name="fromKeyArn")
    @builtins.classmethod
    def from_key_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        key_arn: builtins.str,
    ) -> IKey:
        """(experimental) Import an externally defined KMS Key using its ARN.

        :param scope: the construct that will "own" the imported key.
        :param id: the id of the imported key in the construct tree.
        :param key_arn: the ARN of an existing KMS key.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromKeyArn", [scope, id, key_arn])

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias_name: builtins.str) -> "Alias":
        """(experimental) Defines a new alias for the key.

        :param alias_name: -

        :stability: experimental
        """
        return jsii.invoke(self, "addAlias", [alias_name])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
        allow_no_op: typing.Optional[builtins.bool] = None,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        """(experimental) Adds a statement to the KMS key resource policy.

        :param statement: The policy statement to add.
        :param allow_no_op: If this is set to ``false`` and there is no policy defined (i.e. external key), the operation will fail. Otherwise, it will no-op.

        :stability: experimental
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement, allow_no_op])

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        """(experimental) Grant the indicated permissions on this key to the given principal.

        This modifies both the principal's policy as well as the resource policy,
        since the default CloudFormation setup for KMS keys is that the policy
        must not be empty and so default grants won't work.

        :param grantee: -
        :param actions: -

        :stability: experimental
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant decryption permisisons using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantDecrypt", [grantee])

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant encryption permisisons using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantEncrypt", [grantee])

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant encryption and decryption permisisons using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantEncryptDecrypt", [grantee])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        """(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        """(experimental) The ARN of the key.

        :stability: experimental
        """
        return jsii.get(self, "keyArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        """(experimental) The ID of the key (the part that looks something like: 1234abcd-12ab-34cd-56ef-1234567890ab).

        :stability: experimental
        """
        return jsii.get(self, "keyId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="trustAccountIdentities")
    def _trust_account_identities(self) -> builtins.bool:
        """(experimental) Optional property to control trusting account identities.

        If specified grants will default identity policies instead of to both
        resource and identity policies.

        :stability: experimental
        """
        return jsii.get(self, "trustAccountIdentities")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="policy")
    def _policy(self) -> typing.Optional[_PolicyDocument_b5de5177]:
        """(experimental) Optional policy document that represents the resource policy of this key.

        If specified, addToResourcePolicy can be used to edit this policy.
        Otherwise this method will no-op.

        :stability: experimental
        """
        return jsii.get(self, "policy")


@jsii.data_type(
    jsii_type="monocdk.aws_kms.KeyProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "description": "description",
        "enabled": "enabled",
        "enable_key_rotation": "enableKeyRotation",
        "policy": "policy",
        "removal_policy": "removalPolicy",
        "trust_account_identities": "trustAccountIdentities",
    },
)
class KeyProps:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        policy: typing.Optional[_PolicyDocument_b5de5177] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        trust_account_identities: typing.Optional[builtins.bool] = None,
    ) -> None:
        """(experimental) Construction properties for a KMS Key object.

        :param alias: (experimental) Initial alias to add to the key. More aliases can be added later by calling ``addAlias``. Default: - No alias is added for the key.
        :param description: (experimental) A description of the key. Use a description that helps your users decide whether the key is appropriate for a particular task. Default: - No description.
        :param enabled: (experimental) Indicates whether the key is available for use. Default: - Key is enabled.
        :param enable_key_rotation: (experimental) Indicates whether AWS KMS rotates the key. Default: false
        :param policy: (experimental) Custom policy document to attach to the KMS key. Default: - A policy document with permissions for the account root to administer the key will be created.
        :param removal_policy: (experimental) Whether the encryption key should be retained when it is removed from the Stack. This is useful when one wants to retain access to data that was encrypted with a key that is being retired. Default: RemovalPolicy.Retain
        :param trust_account_identities: (experimental) Whether the key usage can be granted by IAM policies. Setting this to true adds a default statement which delegates key access control completely to the identity's IAM policy (similar to how it works for other AWS resources). Default: false

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_key_rotation is not None:
            self._values["enable_key_rotation"] = enable_key_rotation
        if policy is not None:
            self._values["policy"] = policy
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if trust_account_identities is not None:
            self._values["trust_account_identities"] = trust_account_identities

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        """(experimental) Initial alias to add to the key.

        More aliases can be added later by calling ``addAlias``.

        :default: - No alias is added for the key.

        :stability: experimental
        """
        result = self._values.get("alias")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """(experimental) A description of the key.

        Use a description that helps your users decide
        whether the key is appropriate for a particular task.

        :default: - No description.

        :stability: experimental
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        """(experimental) Indicates whether the key is available for use.

        :default: - Key is enabled.

        :stability: experimental
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def enable_key_rotation(self) -> typing.Optional[builtins.bool]:
        """(experimental) Indicates whether AWS KMS rotates the key.

        :default: false

        :stability: experimental
        """
        result = self._values.get("enable_key_rotation")
        return result

    @builtins.property
    def policy(self) -> typing.Optional[_PolicyDocument_b5de5177]:
        """(experimental) Custom policy document to attach to the KMS key.

        :default:

        - A policy document with permissions for the account root to
        administer the key will be created.

        :stability: experimental
        """
        result = self._values.get("policy")
        return result

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        """(experimental) Whether the encryption key should be retained when it is removed from the Stack.

        This is useful when one wants to
        retain access to data that was encrypted with a key that is being retired.

        :default: RemovalPolicy.Retain

        :stability: experimental
        """
        result = self._values.get("removal_policy")
        return result

    @builtins.property
    def trust_account_identities(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether the key usage can be granted by IAM policies.

        Setting this to true adds a default statement which delegates key
        access control completely to the identity's IAM policy (similar
        to how it works for other AWS resources).

        :default: false

        :see: https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam
        :stability: experimental
        """
        result = self._values.get("trust_account_identities")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ViaServicePrincipal(
    _PrincipalBase_2c3968ff,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kms.ViaServicePrincipal",
):
    """(experimental) A principal to allow access to a key if it's being used through another AWS service.

    :stability: experimental
    """

    def __init__(
        self,
        service_name: builtins.str,
        base_principal: typing.Optional[_IPrincipal_93b48231] = None,
    ) -> None:
        """
        :param service_name: -
        :param base_principal: -

        :stability: experimental
        """
        jsii.create(ViaServicePrincipal, self, [service_name, base_principal])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> _PrincipalPolicyFragment_e6a0f9e3:
        """(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        """
        return jsii.get(self, "policyFragment")


@jsii.interface(jsii_type="monocdk.aws_kms.IAlias")
class IAlias(IKey, typing_extensions.Protocol):
    """(experimental) A KMS Key alias.

    An alias can be used in all places that expect a key.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAliasProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> builtins.str:
        """(experimental) The name of the alias.

        :stability: experimental
        :attribute: true
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="aliasTargetKey")
    def alias_target_key(self) -> IKey:
        """(experimental) The Key to which the Alias refers.

        :stability: experimental
        :attribute: true
        """
        ...


class _IAliasProxy(
    jsii.proxy_for(IKey) # type: ignore
):
    """(experimental) A KMS Key alias.

    An alias can be used in all places that expect a key.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_kms.IAlias"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> builtins.str:
        """(experimental) The name of the alias.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "aliasName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="aliasTargetKey")
    def alias_target_key(self) -> IKey:
        """(experimental) The Key to which the Alias refers.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "aliasTargetKey")


@jsii.implements(IAlias)
class Alias(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kms.Alias",
):
    """(experimental) Defines a display name for a customer master key (CMK) in AWS Key Management Service (AWS KMS).

    Using an alias to refer to a key can help you simplify key
    management. For example, when rotating keys, you can just update the alias
    mapping instead of tracking and changing key IDs. For more information, see
    Working with Aliases in the AWS Key Management Service Developer Guide.

    You can also add an alias for a key by calling ``key.addAlias(alias)``.

    :stability: experimental
    :resource: AWS::KMS::Alias
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        alias_name: builtins.str,
        target_key: IKey,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param alias_name: (experimental) The name of the alias. The name must start with alias followed by a forward slash, such as alias/. You can't specify aliases that begin with alias/AWS. These aliases are reserved.
        :param target_key: (experimental) The ID of the key for which you are creating the alias. Specify the key's globally unique identifier or Amazon Resource Name (ARN). You can't specify another alias.
        :param removal_policy: (experimental) Policy to apply when the alias is removed from this stack. Default: - The alias will be deleted

        :stability: experimental
        """
        props = AliasProps(
            alias_name=alias_name, target_key=target_key, removal_policy=removal_policy
        )

        jsii.create(Alias, self, [scope, id, props])

    @jsii.member(jsii_name="fromAliasAttributes")
    @builtins.classmethod
    def from_alias_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        alias_name: builtins.str,
        alias_target_key: IKey,
    ) -> IAlias:
        """(experimental) Import an existing KMS Alias defined outside the CDK app.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param alias_name: (experimental) Specifies the alias name. This value must begin with alias/ followed by a name (i.e. alias/ExampleAlias)
        :param alias_target_key: (experimental) The customer master key (CMK) to which the Alias refers.

        :stability: experimental
        """
        attrs = AliasAttributes(
            alias_name=alias_name, alias_target_key=alias_target_key
        )

        return jsii.sinvoke(cls, "fromAliasAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromAliasName")
    @builtins.classmethod
    def from_alias_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        alias_name: builtins.str,
    ) -> IAlias:
        """(experimental) Import an existing KMS Alias defined outside the CDK app, by the alias name.

        This method should be used
        instead of 'fromAliasAttributes' when the underlying KMS Key ARN is not available.
        This Alias will not have a direct reference to the KMS Key, so addAlias and grant* methods are not supported.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param alias_name: The full name of the KMS Alias (e.g., 'alias/aws/s3', 'alias/myKeyAlias').

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromAliasName", [scope, id, alias_name])

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias: builtins.str) -> "Alias":
        """(experimental) Defines a new alias for the key.

        :param alias: -

        :stability: experimental
        """
        return jsii.invoke(self, "addAlias", [alias])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _PolicyStatement_296fe8a3,
        allow_no_op: typing.Optional[builtins.bool] = None,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        """(experimental) Adds a statement to the KMS key resource policy.

        :param statement: -
        :param allow_no_op: -

        :stability: experimental
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement, allow_no_op])

    @jsii.member(jsii_name="generatePhysicalName")
    def _generate_physical_name(self) -> builtins.str:
        """
        :stability: experimental
        """
        return jsii.invoke(self, "generatePhysicalName", [])

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        """(experimental) Grant the indicated permissions on this key to the given principal.

        :param grantee: -
        :param actions: -

        :stability: experimental
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantDecrypt")
    def grant_decrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant decryption permissions using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantDecrypt", [grantee])

    @jsii.member(jsii_name="grantEncrypt")
    def grant_encrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant encryption permissions using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantEncrypt", [grantee])

    @jsii.member(jsii_name="grantEncryptDecrypt")
    def grant_encrypt_decrypt(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        """(experimental) Grant encryption and decryption permissions using this key to the given principal.

        :param grantee: -

        :stability: experimental
        """
        return jsii.invoke(self, "grantEncryptDecrypt", [grantee])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> builtins.str:
        """(experimental) The name of the alias.

        :stability: experimental
        """
        return jsii.get(self, "aliasName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="aliasTargetKey")
    def alias_target_key(self) -> IKey:
        """(experimental) The Key to which the Alias refers.

        :stability: experimental
        """
        return jsii.get(self, "aliasTargetKey")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        """(experimental) The ARN of the key.

        :stability: experimental
        """
        return jsii.get(self, "keyArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        """(experimental) The ID of the key (the part that looks something like: 1234abcd-12ab-34cd-56ef-1234567890ab).

        :stability: experimental
        """
        return jsii.get(self, "keyId")


__all__ = [
    "Alias",
    "AliasAttributes",
    "AliasProps",
    "CfnAlias",
    "CfnAliasProps",
    "CfnKey",
    "CfnKeyProps",
    "IAlias",
    "IKey",
    "Key",
    "KeyProps",
    "ViaServicePrincipal",
]

publication.publish()
