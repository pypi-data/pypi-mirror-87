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
class CfnResourceShare(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ram.CfnResourceShare",
):
    """A CloudFormation ``AWS::RAM::ResourceShare``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html
    :cloudformationResource: AWS::RAM::ResourceShare
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        allow_external_principals: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        principals: typing.Optional[typing.List[builtins.str]] = None,
        resource_arns: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::RAM::ResourceShare``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::RAM::ResourceShare.Name``.
        :param allow_external_principals: ``AWS::RAM::ResourceShare.AllowExternalPrincipals``.
        :param principals: ``AWS::RAM::ResourceShare.Principals``.
        :param resource_arns: ``AWS::RAM::ResourceShare.ResourceArns``.
        :param tags: ``AWS::RAM::ResourceShare.Tags``.
        """
        props = CfnResourceShareProps(
            name=name,
            allow_external_principals=allow_external_principals,
            principals=principals,
            resource_arns=resource_arns,
            tags=tags,
        )

        jsii.create(CfnResourceShare, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::RAM::ResourceShare.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::RAM::ResourceShare.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowExternalPrincipals")
    def allow_external_principals(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::RAM::ResourceShare.AllowExternalPrincipals``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-allowexternalprincipals
        """
        return jsii.get(self, "allowExternalPrincipals")

    @allow_external_principals.setter # type: ignore
    def allow_external_principals(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "allowExternalPrincipals", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::RAM::ResourceShare.Principals``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-principals
        """
        return jsii.get(self, "principals")

    @principals.setter # type: ignore
    def principals(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "principals", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resourceArns")
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::RAM::ResourceShare.ResourceArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-resourcearns
        """
        return jsii.get(self, "resourceArns")

    @resource_arns.setter # type: ignore
    def resource_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "resourceArns", value)


@jsii.data_type(
    jsii_type="monocdk.aws_ram.CfnResourceShareProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_external_principals": "allowExternalPrincipals",
        "principals": "principals",
        "resource_arns": "resourceArns",
        "tags": "tags",
    },
)
class CfnResourceShareProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_external_principals: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        principals: typing.Optional[typing.List[builtins.str]] = None,
        resource_arns: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::RAM::ResourceShare``.

        :param name: ``AWS::RAM::ResourceShare.Name``.
        :param allow_external_principals: ``AWS::RAM::ResourceShare.AllowExternalPrincipals``.
        :param principals: ``AWS::RAM::ResourceShare.Principals``.
        :param resource_arns: ``AWS::RAM::ResourceShare.ResourceArns``.
        :param tags: ``AWS::RAM::ResourceShare.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if allow_external_principals is not None:
            self._values["allow_external_principals"] = allow_external_principals
        if principals is not None:
            self._values["principals"] = principals
        if resource_arns is not None:
            self._values["resource_arns"] = resource_arns
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::RAM::ResourceShare.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def allow_external_principals(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::RAM::ResourceShare.AllowExternalPrincipals``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-allowexternalprincipals
        """
        result = self._values.get("allow_external_principals")
        return result

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::RAM::ResourceShare.Principals``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-principals
        """
        result = self._values.get("principals")
        return result

    @builtins.property
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::RAM::ResourceShare.ResourceArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-resourcearns
        """
        result = self._values.get("resource_arns")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::RAM::ResourceShare.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnResourceShare",
    "CfnResourceShareProps",
]

publication.publish()
