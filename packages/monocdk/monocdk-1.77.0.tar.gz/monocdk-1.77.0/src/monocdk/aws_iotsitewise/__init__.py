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
class CfnAsset(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotsitewise.CfnAsset",
):
    """A CloudFormation ``AWS::IoTSiteWise::Asset``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html
    :cloudformationResource: AWS::IoTSiteWise::Asset
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        asset_model_id: builtins.str,
        asset_name: builtins.str,
        asset_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetHierarchyProperty", _IResolvable_a771d0ef]]]] = None,
        asset_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetPropertyProperty", _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::IoTSiteWise::Asset``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param asset_model_id: ``AWS::IoTSiteWise::Asset.AssetModelId``.
        :param asset_name: ``AWS::IoTSiteWise::Asset.AssetName``.
        :param asset_hierarchies: ``AWS::IoTSiteWise::Asset.AssetHierarchies``.
        :param asset_properties: ``AWS::IoTSiteWise::Asset.AssetProperties``.
        :param tags: ``AWS::IoTSiteWise::Asset.Tags``.
        """
        props = CfnAssetProps(
            asset_model_id=asset_model_id,
            asset_name=asset_name,
            asset_hierarchies=asset_hierarchies,
            asset_properties=asset_properties,
            tags=tags,
        )

        jsii.create(CfnAsset, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrAssetArn")
    def attr_asset_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: AssetArn
        """
        return jsii.get(self, "attrAssetArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrAssetId")
    def attr_asset_id(self) -> builtins.str:
        """
        :cloudformationAttribute: AssetId
        """
        return jsii.get(self, "attrAssetId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::IoTSiteWise::Asset.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="assetModelId")
    def asset_model_id(self) -> builtins.str:
        """``AWS::IoTSiteWise::Asset.AssetModelId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetmodelid
        """
        return jsii.get(self, "assetModelId")

    @asset_model_id.setter # type: ignore
    def asset_model_id(self, value: builtins.str) -> None:
        jsii.set(self, "assetModelId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="assetName")
    def asset_name(self) -> builtins.str:
        """``AWS::IoTSiteWise::Asset.AssetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetname
        """
        return jsii.get(self, "assetName")

    @asset_name.setter # type: ignore
    def asset_name(self, value: builtins.str) -> None:
        jsii.set(self, "assetName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="assetHierarchies")
    def asset_hierarchies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetHierarchyProperty", _IResolvable_a771d0ef]]]]:
        """``AWS::IoTSiteWise::Asset.AssetHierarchies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assethierarchies
        """
        return jsii.get(self, "assetHierarchies")

    @asset_hierarchies.setter # type: ignore
    def asset_hierarchies(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetHierarchyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "assetHierarchies", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="assetProperties")
    def asset_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetPropertyProperty", _IResolvable_a771d0ef]]]]:
        """``AWS::IoTSiteWise::Asset.AssetProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetproperties
        """
        return jsii.get(self, "assetProperties")

    @asset_properties.setter # type: ignore
    def asset_properties(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAsset.AssetPropertyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "assetProperties", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAsset.AssetHierarchyProperty",
        jsii_struct_bases=[],
        name_mapping={"child_asset_id": "childAssetId", "logical_id": "logicalId"},
    )
    class AssetHierarchyProperty:
        def __init__(
            self,
            *,
            child_asset_id: builtins.str,
            logical_id: builtins.str,
        ) -> None:
            """
            :param child_asset_id: ``CfnAsset.AssetHierarchyProperty.ChildAssetId``.
            :param logical_id: ``CfnAsset.AssetHierarchyProperty.LogicalId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assethierarchy.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "child_asset_id": child_asset_id,
                "logical_id": logical_id,
            }

        @builtins.property
        def child_asset_id(self) -> builtins.str:
            """``CfnAsset.AssetHierarchyProperty.ChildAssetId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assethierarchy.html#cfn-iotsitewise-asset-assethierarchy-childassetid
            """
            result = self._values.get("child_asset_id")
            assert result is not None, "Required property 'child_asset_id' is missing"
            return result

        @builtins.property
        def logical_id(self) -> builtins.str:
            """``CfnAsset.AssetHierarchyProperty.LogicalId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assethierarchy.html#cfn-iotsitewise-asset-assethierarchy-logicalid
            """
            result = self._values.get("logical_id")
            assert result is not None, "Required property 'logical_id' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetHierarchyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAsset.AssetPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "logical_id": "logicalId",
            "alias": "alias",
            "notification_state": "notificationState",
        },
    )
    class AssetPropertyProperty:
        def __init__(
            self,
            *,
            logical_id: builtins.str,
            alias: typing.Optional[builtins.str] = None,
            notification_state: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param logical_id: ``CfnAsset.AssetPropertyProperty.LogicalId``.
            :param alias: ``CfnAsset.AssetPropertyProperty.Alias``.
            :param notification_state: ``CfnAsset.AssetPropertyProperty.NotificationState``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "logical_id": logical_id,
            }
            if alias is not None:
                self._values["alias"] = alias
            if notification_state is not None:
                self._values["notification_state"] = notification_state

        @builtins.property
        def logical_id(self) -> builtins.str:
            """``CfnAsset.AssetPropertyProperty.LogicalId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-logicalid
            """
            result = self._values.get("logical_id")
            assert result is not None, "Required property 'logical_id' is missing"
            return result

        @builtins.property
        def alias(self) -> typing.Optional[builtins.str]:
            """``CfnAsset.AssetPropertyProperty.Alias``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-alias
            """
            result = self._values.get("alias")
            return result

        @builtins.property
        def notification_state(self) -> typing.Optional[builtins.str]:
            """``CfnAsset.AssetPropertyProperty.NotificationState``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-notificationstate
            """
            result = self._values.get("notification_state")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnAssetModel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotsitewise.CfnAssetModel",
):
    """A CloudFormation ``AWS::IoTSiteWise::AssetModel``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html
    :cloudformationResource: AWS::IoTSiteWise::AssetModel
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        asset_model_name: builtins.str,
        asset_model_description: typing.Optional[builtins.str] = None,
        asset_model_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelHierarchyProperty", _IResolvable_a771d0ef]]]] = None,
        asset_model_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelPropertyProperty", _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::IoTSiteWise::AssetModel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param asset_model_name: ``AWS::IoTSiteWise::AssetModel.AssetModelName``.
        :param asset_model_description: ``AWS::IoTSiteWise::AssetModel.AssetModelDescription``.
        :param asset_model_hierarchies: ``AWS::IoTSiteWise::AssetModel.AssetModelHierarchies``.
        :param asset_model_properties: ``AWS::IoTSiteWise::AssetModel.AssetModelProperties``.
        :param tags: ``AWS::IoTSiteWise::AssetModel.Tags``.
        """
        props = CfnAssetModelProps(
            asset_model_name=asset_model_name,
            asset_model_description=asset_model_description,
            asset_model_hierarchies=asset_model_hierarchies,
            asset_model_properties=asset_model_properties,
            tags=tags,
        )

        jsii.create(CfnAssetModel, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrAssetModelArn")
    def attr_asset_model_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: AssetModelArn
        """
        return jsii.get(self, "attrAssetModelArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrAssetModelId")
    def attr_asset_model_id(self) -> builtins.str:
        """
        :cloudformationAttribute: AssetModelId
        """
        return jsii.get(self, "attrAssetModelId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::IoTSiteWise::AssetModel.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="assetModelName")
    def asset_model_name(self) -> builtins.str:
        """``AWS::IoTSiteWise::AssetModel.AssetModelName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelname
        """
        return jsii.get(self, "assetModelName")

    @asset_model_name.setter # type: ignore
    def asset_model_name(self, value: builtins.str) -> None:
        jsii.set(self, "assetModelName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="assetModelDescription")
    def asset_model_description(self) -> typing.Optional[builtins.str]:
        """``AWS::IoTSiteWise::AssetModel.AssetModelDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodeldescription
        """
        return jsii.get(self, "assetModelDescription")

    @asset_model_description.setter # type: ignore
    def asset_model_description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "assetModelDescription", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="assetModelHierarchies")
    def asset_model_hierarchies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelHierarchyProperty", _IResolvable_a771d0ef]]]]:
        """``AWS::IoTSiteWise::AssetModel.AssetModelHierarchies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelhierarchies
        """
        return jsii.get(self, "assetModelHierarchies")

    @asset_model_hierarchies.setter # type: ignore
    def asset_model_hierarchies(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelHierarchyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "assetModelHierarchies", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="assetModelProperties")
    def asset_model_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelPropertyProperty", _IResolvable_a771d0ef]]]]:
        """``AWS::IoTSiteWise::AssetModel.AssetModelProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelproperties
        """
        return jsii.get(self, "assetModelProperties")

    @asset_model_properties.setter # type: ignore
    def asset_model_properties(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.AssetModelPropertyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "assetModelProperties", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.AssetModelHierarchyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "child_asset_model_id": "childAssetModelId",
            "logical_id": "logicalId",
            "name": "name",
        },
    )
    class AssetModelHierarchyProperty:
        def __init__(
            self,
            *,
            child_asset_model_id: builtins.str,
            logical_id: builtins.str,
            name: builtins.str,
        ) -> None:
            """
            :param child_asset_model_id: ``CfnAssetModel.AssetModelHierarchyProperty.ChildAssetModelId``.
            :param logical_id: ``CfnAssetModel.AssetModelHierarchyProperty.LogicalId``.
            :param name: ``CfnAssetModel.AssetModelHierarchyProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "child_asset_model_id": child_asset_model_id,
                "logical_id": logical_id,
                "name": name,
            }

        @builtins.property
        def child_asset_model_id(self) -> builtins.str:
            """``CfnAssetModel.AssetModelHierarchyProperty.ChildAssetModelId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html#cfn-iotsitewise-assetmodel-assetmodelhierarchy-childassetmodelid
            """
            result = self._values.get("child_asset_model_id")
            assert result is not None, "Required property 'child_asset_model_id' is missing"
            return result

        @builtins.property
        def logical_id(self) -> builtins.str:
            """``CfnAssetModel.AssetModelHierarchyProperty.LogicalId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html#cfn-iotsitewise-assetmodel-assetmodelhierarchy-logicalid
            """
            result = self._values.get("logical_id")
            assert result is not None, "Required property 'logical_id' is missing"
            return result

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnAssetModel.AssetModelHierarchyProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html#cfn-iotsitewise-assetmodel-assetmodelhierarchy-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetModelHierarchyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.AssetModelPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_type": "dataType",
            "logical_id": "logicalId",
            "name": "name",
            "type": "type",
            "unit": "unit",
        },
    )
    class AssetModelPropertyProperty:
        def __init__(
            self,
            *,
            data_type: builtins.str,
            logical_id: builtins.str,
            name: builtins.str,
            type: typing.Union["CfnAssetModel.PropertyTypeProperty", _IResolvable_a771d0ef],
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param data_type: ``CfnAssetModel.AssetModelPropertyProperty.DataType``.
            :param logical_id: ``CfnAssetModel.AssetModelPropertyProperty.LogicalId``.
            :param name: ``CfnAssetModel.AssetModelPropertyProperty.Name``.
            :param type: ``CfnAssetModel.AssetModelPropertyProperty.Type``.
            :param unit: ``CfnAssetModel.AssetModelPropertyProperty.Unit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "data_type": data_type,
                "logical_id": logical_id,
                "name": name,
                "type": type,
            }
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def data_type(self) -> builtins.str:
            """``CfnAssetModel.AssetModelPropertyProperty.DataType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-datatype
            """
            result = self._values.get("data_type")
            assert result is not None, "Required property 'data_type' is missing"
            return result

        @builtins.property
        def logical_id(self) -> builtins.str:
            """``CfnAssetModel.AssetModelPropertyProperty.LogicalId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-logicalid
            """
            result = self._values.get("logical_id")
            assert result is not None, "Required property 'logical_id' is missing"
            return result

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnAssetModel.AssetModelPropertyProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def type(
            self,
        ) -> typing.Union["CfnAssetModel.PropertyTypeProperty", _IResolvable_a771d0ef]:
            """``CfnAssetModel.AssetModelPropertyProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            """``CfnAssetModel.AssetModelPropertyProperty.Unit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-unit
            """
            result = self._values.get("unit")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetModelPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.AttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value": "defaultValue"},
    )
    class AttributeProperty:
        def __init__(
            self,
            *,
            default_value: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param default_value: ``CfnAssetModel.AttributeProperty.DefaultValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-attribute.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if default_value is not None:
                self._values["default_value"] = default_value

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            """``CfnAssetModel.AttributeProperty.DefaultValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-attribute.html#cfn-iotsitewise-assetmodel-attribute-defaultvalue
            """
            result = self._values.get("default_value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.ExpressionVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class ExpressionVariableProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            value: typing.Union["CfnAssetModel.VariableValueProperty", _IResolvable_a771d0ef],
        ) -> None:
            """
            :param name: ``CfnAssetModel.ExpressionVariableProperty.Name``.
            :param value: ``CfnAssetModel.ExpressionVariableProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-expressionvariable.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnAssetModel.ExpressionVariableProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-expressionvariable.html#cfn-iotsitewise-assetmodel-expressionvariable-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def value(
            self,
        ) -> typing.Union["CfnAssetModel.VariableValueProperty", _IResolvable_a771d0ef]:
            """``CfnAssetModel.ExpressionVariableProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-expressionvariable.html#cfn-iotsitewise-assetmodel-expressionvariable-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExpressionVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.MetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "variables": "variables",
            "window": "window",
        },
    )
    class MetricProperty:
        def __init__(
            self,
            *,
            expression: builtins.str,
            variables: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.ExpressionVariableProperty", _IResolvable_a771d0ef]]],
            window: typing.Union["CfnAssetModel.MetricWindowProperty", _IResolvable_a771d0ef],
        ) -> None:
            """
            :param expression: ``CfnAssetModel.MetricProperty.Expression``.
            :param variables: ``CfnAssetModel.MetricProperty.Variables``.
            :param window: ``CfnAssetModel.MetricProperty.Window``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "expression": expression,
                "variables": variables,
                "window": window,
            }

        @builtins.property
        def expression(self) -> builtins.str:
            """``CfnAssetModel.MetricProperty.Expression``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html#cfn-iotsitewise-assetmodel-metric-expression
            """
            result = self._values.get("expression")
            assert result is not None, "Required property 'expression' is missing"
            return result

        @builtins.property
        def variables(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.ExpressionVariableProperty", _IResolvable_a771d0ef]]]:
            """``CfnAssetModel.MetricProperty.Variables``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html#cfn-iotsitewise-assetmodel-metric-variables
            """
            result = self._values.get("variables")
            assert result is not None, "Required property 'variables' is missing"
            return result

        @builtins.property
        def window(
            self,
        ) -> typing.Union["CfnAssetModel.MetricWindowProperty", _IResolvable_a771d0ef]:
            """``CfnAssetModel.MetricProperty.Window``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html#cfn-iotsitewise-assetmodel-metric-window
            """
            result = self._values.get("window")
            assert result is not None, "Required property 'window' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.MetricWindowProperty",
        jsii_struct_bases=[],
        name_mapping={"tumbling": "tumbling"},
    )
    class MetricWindowProperty:
        def __init__(
            self,
            *,
            tumbling: typing.Optional[typing.Union["CfnAssetModel.TumblingWindowProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param tumbling: ``CfnAssetModel.MetricWindowProperty.Tumbling``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metricwindow.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if tumbling is not None:
                self._values["tumbling"] = tumbling

        @builtins.property
        def tumbling(
            self,
        ) -> typing.Optional[typing.Union["CfnAssetModel.TumblingWindowProperty", _IResolvable_a771d0ef]]:
            """``CfnAssetModel.MetricWindowProperty.Tumbling``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metricwindow.html#cfn-iotsitewise-assetmodel-metricwindow-tumbling
            """
            result = self._values.get("tumbling")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.PropertyTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type_name": "typeName",
            "attribute": "attribute",
            "metric": "metric",
            "transform": "transform",
        },
    )
    class PropertyTypeProperty:
        def __init__(
            self,
            *,
            type_name: builtins.str,
            attribute: typing.Optional[typing.Union["CfnAssetModel.AttributeProperty", _IResolvable_a771d0ef]] = None,
            metric: typing.Optional[typing.Union["CfnAssetModel.MetricProperty", _IResolvable_a771d0ef]] = None,
            transform: typing.Optional[typing.Union["CfnAssetModel.TransformProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param type_name: ``CfnAssetModel.PropertyTypeProperty.TypeName``.
            :param attribute: ``CfnAssetModel.PropertyTypeProperty.Attribute``.
            :param metric: ``CfnAssetModel.PropertyTypeProperty.Metric``.
            :param transform: ``CfnAssetModel.PropertyTypeProperty.Transform``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type_name": type_name,
            }
            if attribute is not None:
                self._values["attribute"] = attribute
            if metric is not None:
                self._values["metric"] = metric
            if transform is not None:
                self._values["transform"] = transform

        @builtins.property
        def type_name(self) -> builtins.str:
            """``CfnAssetModel.PropertyTypeProperty.TypeName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-typename
            """
            result = self._values.get("type_name")
            assert result is not None, "Required property 'type_name' is missing"
            return result

        @builtins.property
        def attribute(
            self,
        ) -> typing.Optional[typing.Union["CfnAssetModel.AttributeProperty", _IResolvable_a771d0ef]]:
            """``CfnAssetModel.PropertyTypeProperty.Attribute``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-attribute
            """
            result = self._values.get("attribute")
            return result

        @builtins.property
        def metric(
            self,
        ) -> typing.Optional[typing.Union["CfnAssetModel.MetricProperty", _IResolvable_a771d0ef]]:
            """``CfnAssetModel.PropertyTypeProperty.Metric``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-metric
            """
            result = self._values.get("metric")
            return result

        @builtins.property
        def transform(
            self,
        ) -> typing.Optional[typing.Union["CfnAssetModel.TransformProperty", _IResolvable_a771d0ef]]:
            """``CfnAssetModel.PropertyTypeProperty.Transform``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-transform
            """
            result = self._values.get("transform")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.TransformProperty",
        jsii_struct_bases=[],
        name_mapping={"expression": "expression", "variables": "variables"},
    )
    class TransformProperty:
        def __init__(
            self,
            *,
            expression: builtins.str,
            variables: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.ExpressionVariableProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            """
            :param expression: ``CfnAssetModel.TransformProperty.Expression``.
            :param variables: ``CfnAssetModel.TransformProperty.Variables``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-transform.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "expression": expression,
                "variables": variables,
            }

        @builtins.property
        def expression(self) -> builtins.str:
            """``CfnAssetModel.TransformProperty.Expression``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-transform.html#cfn-iotsitewise-assetmodel-transform-expression
            """
            result = self._values.get("expression")
            assert result is not None, "Required property 'expression' is missing"
            return result

        @builtins.property
        def variables(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssetModel.ExpressionVariableProperty", _IResolvable_a771d0ef]]]:
            """``CfnAssetModel.TransformProperty.Variables``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-transform.html#cfn-iotsitewise-assetmodel-transform-variables
            """
            result = self._values.get("variables")
            assert result is not None, "Required property 'variables' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransformProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.TumblingWindowProperty",
        jsii_struct_bases=[],
        name_mapping={"interval": "interval"},
    )
    class TumblingWindowProperty:
        def __init__(self, *, interval: builtins.str) -> None:
            """
            :param interval: ``CfnAssetModel.TumblingWindowProperty.Interval``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-tumblingwindow.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "interval": interval,
            }

        @builtins.property
        def interval(self) -> builtins.str:
            """``CfnAssetModel.TumblingWindowProperty.Interval``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-tumblingwindow.html#cfn-iotsitewise-assetmodel-tumblingwindow-interval
            """
            result = self._values.get("interval")
            assert result is not None, "Required property 'interval' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TumblingWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnAssetModel.VariableValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "property_logical_id": "propertyLogicalId",
            "hierarchy_logical_id": "hierarchyLogicalId",
        },
    )
    class VariableValueProperty:
        def __init__(
            self,
            *,
            property_logical_id: builtins.str,
            hierarchy_logical_id: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param property_logical_id: ``CfnAssetModel.VariableValueProperty.PropertyLogicalId``.
            :param hierarchy_logical_id: ``CfnAssetModel.VariableValueProperty.HierarchyLogicalId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "property_logical_id": property_logical_id,
            }
            if hierarchy_logical_id is not None:
                self._values["hierarchy_logical_id"] = hierarchy_logical_id

        @builtins.property
        def property_logical_id(self) -> builtins.str:
            """``CfnAssetModel.VariableValueProperty.PropertyLogicalId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html#cfn-iotsitewise-assetmodel-variablevalue-propertylogicalid
            """
            result = self._values.get("property_logical_id")
            assert result is not None, "Required property 'property_logical_id' is missing"
            return result

        @builtins.property
        def hierarchy_logical_id(self) -> typing.Optional[builtins.str]:
            """``CfnAssetModel.VariableValueProperty.HierarchyLogicalId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html#cfn-iotsitewise-assetmodel-variablevalue-hierarchylogicalid
            """
            result = self._values.get("hierarchy_logical_id")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VariableValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotsitewise.CfnAssetModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "asset_model_name": "assetModelName",
        "asset_model_description": "assetModelDescription",
        "asset_model_hierarchies": "assetModelHierarchies",
        "asset_model_properties": "assetModelProperties",
        "tags": "tags",
    },
)
class CfnAssetModelProps:
    def __init__(
        self,
        *,
        asset_model_name: builtins.str,
        asset_model_description: typing.Optional[builtins.str] = None,
        asset_model_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelHierarchyProperty, _IResolvable_a771d0ef]]]] = None,
        asset_model_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelPropertyProperty, _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::IoTSiteWise::AssetModel``.

        :param asset_model_name: ``AWS::IoTSiteWise::AssetModel.AssetModelName``.
        :param asset_model_description: ``AWS::IoTSiteWise::AssetModel.AssetModelDescription``.
        :param asset_model_hierarchies: ``AWS::IoTSiteWise::AssetModel.AssetModelHierarchies``.
        :param asset_model_properties: ``AWS::IoTSiteWise::AssetModel.AssetModelProperties``.
        :param tags: ``AWS::IoTSiteWise::AssetModel.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "asset_model_name": asset_model_name,
        }
        if asset_model_description is not None:
            self._values["asset_model_description"] = asset_model_description
        if asset_model_hierarchies is not None:
            self._values["asset_model_hierarchies"] = asset_model_hierarchies
        if asset_model_properties is not None:
            self._values["asset_model_properties"] = asset_model_properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def asset_model_name(self) -> builtins.str:
        """``AWS::IoTSiteWise::AssetModel.AssetModelName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelname
        """
        result = self._values.get("asset_model_name")
        assert result is not None, "Required property 'asset_model_name' is missing"
        return result

    @builtins.property
    def asset_model_description(self) -> typing.Optional[builtins.str]:
        """``AWS::IoTSiteWise::AssetModel.AssetModelDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodeldescription
        """
        result = self._values.get("asset_model_description")
        return result

    @builtins.property
    def asset_model_hierarchies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelHierarchyProperty, _IResolvable_a771d0ef]]]]:
        """``AWS::IoTSiteWise::AssetModel.AssetModelHierarchies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelhierarchies
        """
        result = self._values.get("asset_model_hierarchies")
        return result

    @builtins.property
    def asset_model_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssetModel.AssetModelPropertyProperty, _IResolvable_a771d0ef]]]]:
        """``AWS::IoTSiteWise::AssetModel.AssetModelProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelproperties
        """
        result = self._values.get("asset_model_properties")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::IoTSiteWise::AssetModel.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssetModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iotsitewise.CfnAssetProps",
    jsii_struct_bases=[],
    name_mapping={
        "asset_model_id": "assetModelId",
        "asset_name": "assetName",
        "asset_hierarchies": "assetHierarchies",
        "asset_properties": "assetProperties",
        "tags": "tags",
    },
)
class CfnAssetProps:
    def __init__(
        self,
        *,
        asset_model_id: builtins.str,
        asset_name: builtins.str,
        asset_hierarchies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAsset.AssetHierarchyProperty, _IResolvable_a771d0ef]]]] = None,
        asset_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAsset.AssetPropertyProperty, _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::IoTSiteWise::Asset``.

        :param asset_model_id: ``AWS::IoTSiteWise::Asset.AssetModelId``.
        :param asset_name: ``AWS::IoTSiteWise::Asset.AssetName``.
        :param asset_hierarchies: ``AWS::IoTSiteWise::Asset.AssetHierarchies``.
        :param asset_properties: ``AWS::IoTSiteWise::Asset.AssetProperties``.
        :param tags: ``AWS::IoTSiteWise::Asset.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "asset_model_id": asset_model_id,
            "asset_name": asset_name,
        }
        if asset_hierarchies is not None:
            self._values["asset_hierarchies"] = asset_hierarchies
        if asset_properties is not None:
            self._values["asset_properties"] = asset_properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def asset_model_id(self) -> builtins.str:
        """``AWS::IoTSiteWise::Asset.AssetModelId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetmodelid
        """
        result = self._values.get("asset_model_id")
        assert result is not None, "Required property 'asset_model_id' is missing"
        return result

    @builtins.property
    def asset_name(self) -> builtins.str:
        """``AWS::IoTSiteWise::Asset.AssetName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetname
        """
        result = self._values.get("asset_name")
        assert result is not None, "Required property 'asset_name' is missing"
        return result

    @builtins.property
    def asset_hierarchies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAsset.AssetHierarchyProperty, _IResolvable_a771d0ef]]]]:
        """``AWS::IoTSiteWise::Asset.AssetHierarchies``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assethierarchies
        """
        result = self._values.get("asset_hierarchies")
        return result

    @builtins.property
    def asset_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAsset.AssetPropertyProperty, _IResolvable_a771d0ef]]]]:
        """``AWS::IoTSiteWise::Asset.AssetProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetproperties
        """
        result = self._values.get("asset_properties")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::IoTSiteWise::Asset.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnGateway(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iotsitewise.CfnGateway",
):
    """A CloudFormation ``AWS::IoTSiteWise::Gateway``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html
    :cloudformationResource: AWS::IoTSiteWise::Gateway
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        gateway_name: builtins.str,
        gateway_platform: typing.Union["CfnGateway.GatewayPlatformProperty", _IResolvable_a771d0ef],
        gateway_capability_summaries: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGateway.GatewayCapabilitySummaryProperty", _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::IoTSiteWise::Gateway``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param gateway_name: ``AWS::IoTSiteWise::Gateway.GatewayName``.
        :param gateway_platform: ``AWS::IoTSiteWise::Gateway.GatewayPlatform``.
        :param gateway_capability_summaries: ``AWS::IoTSiteWise::Gateway.GatewayCapabilitySummaries``.
        :param tags: ``AWS::IoTSiteWise::Gateway.Tags``.
        """
        props = CfnGatewayProps(
            gateway_name=gateway_name,
            gateway_platform=gateway_platform,
            gateway_capability_summaries=gateway_capability_summaries,
            tags=tags,
        )

        jsii.create(CfnGateway, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrGatewayId")
    def attr_gateway_id(self) -> builtins.str:
        """
        :cloudformationAttribute: GatewayId
        """
        return jsii.get(self, "attrGatewayId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::IoTSiteWise::Gateway.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gatewayName")
    def gateway_name(self) -> builtins.str:
        """``AWS::IoTSiteWise::Gateway.GatewayName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewayname
        """
        return jsii.get(self, "gatewayName")

    @gateway_name.setter # type: ignore
    def gateway_name(self, value: builtins.str) -> None:
        jsii.set(self, "gatewayName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gatewayPlatform")
    def gateway_platform(
        self,
    ) -> typing.Union["CfnGateway.GatewayPlatformProperty", _IResolvable_a771d0ef]:
        """``AWS::IoTSiteWise::Gateway.GatewayPlatform``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewayplatform
        """
        return jsii.get(self, "gatewayPlatform")

    @gateway_platform.setter # type: ignore
    def gateway_platform(
        self,
        value: typing.Union["CfnGateway.GatewayPlatformProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "gatewayPlatform", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gatewayCapabilitySummaries")
    def gateway_capability_summaries(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGateway.GatewayCapabilitySummaryProperty", _IResolvable_a771d0ef]]]]:
        """``AWS::IoTSiteWise::Gateway.GatewayCapabilitySummaries``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewaycapabilitysummaries
        """
        return jsii.get(self, "gatewayCapabilitySummaries")

    @gateway_capability_summaries.setter # type: ignore
    def gateway_capability_summaries(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGateway.GatewayCapabilitySummaryProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "gatewayCapabilitySummaries", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnGateway.GatewayCapabilitySummaryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capability_namespace": "capabilityNamespace",
            "capability_configuration": "capabilityConfiguration",
        },
    )
    class GatewayCapabilitySummaryProperty:
        def __init__(
            self,
            *,
            capability_namespace: builtins.str,
            capability_configuration: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param capability_namespace: ``CfnGateway.GatewayCapabilitySummaryProperty.CapabilityNamespace``.
            :param capability_configuration: ``CfnGateway.GatewayCapabilitySummaryProperty.CapabilityConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewaycapabilitysummary.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "capability_namespace": capability_namespace,
            }
            if capability_configuration is not None:
                self._values["capability_configuration"] = capability_configuration

        @builtins.property
        def capability_namespace(self) -> builtins.str:
            """``CfnGateway.GatewayCapabilitySummaryProperty.CapabilityNamespace``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewaycapabilitysummary.html#cfn-iotsitewise-gateway-gatewaycapabilitysummary-capabilitynamespace
            """
            result = self._values.get("capability_namespace")
            assert result is not None, "Required property 'capability_namespace' is missing"
            return result

        @builtins.property
        def capability_configuration(self) -> typing.Optional[builtins.str]:
            """``CfnGateway.GatewayCapabilitySummaryProperty.CapabilityConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewaycapabilitysummary.html#cfn-iotsitewise-gateway-gatewaycapabilitysummary-capabilityconfiguration
            """
            result = self._values.get("capability_configuration")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayCapabilitySummaryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnGateway.GatewayPlatformProperty",
        jsii_struct_bases=[],
        name_mapping={"greengrass": "greengrass"},
    )
    class GatewayPlatformProperty:
        def __init__(
            self,
            *,
            greengrass: typing.Union["CfnGateway.GreengrassProperty", _IResolvable_a771d0ef],
        ) -> None:
            """
            :param greengrass: ``CfnGateway.GatewayPlatformProperty.Greengrass``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewayplatform.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "greengrass": greengrass,
            }

        @builtins.property
        def greengrass(
            self,
        ) -> typing.Union["CfnGateway.GreengrassProperty", _IResolvable_a771d0ef]:
            """``CfnGateway.GatewayPlatformProperty.Greengrass``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewayplatform.html#cfn-iotsitewise-gateway-gatewayplatform-greengrass
            """
            result = self._values.get("greengrass")
            assert result is not None, "Required property 'greengrass' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayPlatformProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iotsitewise.CfnGateway.GreengrassProperty",
        jsii_struct_bases=[],
        name_mapping={"group_arn": "groupArn"},
    )
    class GreengrassProperty:
        def __init__(self, *, group_arn: builtins.str) -> None:
            """
            :param group_arn: ``CfnGateway.GreengrassProperty.GroupArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-greengrass.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "group_arn": group_arn,
            }

        @builtins.property
        def group_arn(self) -> builtins.str:
            """``CfnGateway.GreengrassProperty.GroupArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-greengrass.html#cfn-iotsitewise-gateway-greengrass-grouparn
            """
            result = self._values.get("group_arn")
            assert result is not None, "Required property 'group_arn' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GreengrassProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iotsitewise.CfnGatewayProps",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_name": "gatewayName",
        "gateway_platform": "gatewayPlatform",
        "gateway_capability_summaries": "gatewayCapabilitySummaries",
        "tags": "tags",
    },
)
class CfnGatewayProps:
    def __init__(
        self,
        *,
        gateway_name: builtins.str,
        gateway_platform: typing.Union[CfnGateway.GatewayPlatformProperty, _IResolvable_a771d0ef],
        gateway_capability_summaries: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGateway.GatewayCapabilitySummaryProperty, _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::IoTSiteWise::Gateway``.

        :param gateway_name: ``AWS::IoTSiteWise::Gateway.GatewayName``.
        :param gateway_platform: ``AWS::IoTSiteWise::Gateway.GatewayPlatform``.
        :param gateway_capability_summaries: ``AWS::IoTSiteWise::Gateway.GatewayCapabilitySummaries``.
        :param tags: ``AWS::IoTSiteWise::Gateway.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "gateway_name": gateway_name,
            "gateway_platform": gateway_platform,
        }
        if gateway_capability_summaries is not None:
            self._values["gateway_capability_summaries"] = gateway_capability_summaries
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def gateway_name(self) -> builtins.str:
        """``AWS::IoTSiteWise::Gateway.GatewayName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewayname
        """
        result = self._values.get("gateway_name")
        assert result is not None, "Required property 'gateway_name' is missing"
        return result

    @builtins.property
    def gateway_platform(
        self,
    ) -> typing.Union[CfnGateway.GatewayPlatformProperty, _IResolvable_a771d0ef]:
        """``AWS::IoTSiteWise::Gateway.GatewayPlatform``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewayplatform
        """
        result = self._values.get("gateway_platform")
        assert result is not None, "Required property 'gateway_platform' is missing"
        return result

    @builtins.property
    def gateway_capability_summaries(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGateway.GatewayCapabilitySummaryProperty, _IResolvable_a771d0ef]]]]:
        """``AWS::IoTSiteWise::Gateway.GatewayCapabilitySummaries``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewaycapabilitysummaries
        """
        result = self._values.get("gateway_capability_summaries")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::IoTSiteWise::Gateway.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAsset",
    "CfnAssetModel",
    "CfnAssetModelProps",
    "CfnAssetProps",
    "CfnGateway",
    "CfnGatewayProps",
]

publication.publish()
