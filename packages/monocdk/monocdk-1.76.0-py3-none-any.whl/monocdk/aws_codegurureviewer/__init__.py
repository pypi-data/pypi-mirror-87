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
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnRepositoryAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codegurureviewer.CfnRepositoryAssociation",
):
    """A CloudFormation ``AWS::CodeGuruReviewer::RepositoryAssociation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html
    :cloudformationResource: AWS::CodeGuruReviewer::RepositoryAssociation
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        connection_arn: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::CodeGuruReviewer::RepositoryAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::CodeGuruReviewer::RepositoryAssociation.Name``.
        :param type: ``AWS::CodeGuruReviewer::RepositoryAssociation.Type``.
        :param connection_arn: ``AWS::CodeGuruReviewer::RepositoryAssociation.ConnectionArn``.
        :param owner: ``AWS::CodeGuruReviewer::RepositoryAssociation.Owner``.
        """
        props = CfnRepositoryAssociationProps(
            name=name, type=type, connection_arn=connection_arn, owner=owner
        )

        jsii.create(CfnRepositoryAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrAssociationArn")
    def attr_association_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: AssociationArn
        """
        return jsii.get(self, "attrAssociationArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::CodeGuruReviewer::RepositoryAssociation.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """``AWS::CodeGuruReviewer::RepositoryAssociation.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeGuruReviewer::RepositoryAssociation.ConnectionArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-connectionarn
        """
        return jsii.get(self, "connectionArn")

    @connection_arn.setter # type: ignore
    def connection_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "connectionArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="owner")
    def owner(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeGuruReviewer::RepositoryAssociation.Owner``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-owner
        """
        return jsii.get(self, "owner")

    @owner.setter # type: ignore
    def owner(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "owner", value)


@jsii.data_type(
    jsii_type="monocdk.aws_codegurureviewer.CfnRepositoryAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "connection_arn": "connectionArn",
        "owner": "owner",
    },
)
class CfnRepositoryAssociationProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        connection_arn: typing.Optional[builtins.str] = None,
        owner: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodeGuruReviewer::RepositoryAssociation``.

        :param name: ``AWS::CodeGuruReviewer::RepositoryAssociation.Name``.
        :param type: ``AWS::CodeGuruReviewer::RepositoryAssociation.Type``.
        :param connection_arn: ``AWS::CodeGuruReviewer::RepositoryAssociation.ConnectionArn``.
        :param owner: ``AWS::CodeGuruReviewer::RepositoryAssociation.Owner``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if connection_arn is not None:
            self._values["connection_arn"] = connection_arn
        if owner is not None:
            self._values["owner"] = owner

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::CodeGuruReviewer::RepositoryAssociation.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def type(self) -> builtins.str:
        """``AWS::CodeGuruReviewer::RepositoryAssociation.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-type
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def connection_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeGuruReviewer::RepositoryAssociation.ConnectionArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-connectionarn
        """
        result = self._values.get("connection_arn")
        return result

    @builtins.property
    def owner(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeGuruReviewer::RepositoryAssociation.Owner``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codegurureviewer-repositoryassociation.html#cfn-codegurureviewer-repositoryassociation-owner
        """
        result = self._values.get("owner")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnRepositoryAssociation",
    "CfnRepositoryAssociationProps",
]

publication.publish()
