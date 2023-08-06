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
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnLifecyclePolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy",
):
    """A CloudFormation ``AWS::DLM::LifecyclePolicy``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html
    :cloudformationResource: AWS::DLM::LifecyclePolicy
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        policy_details: typing.Optional[typing.Union["CfnLifecyclePolicy.PolicyDetailsProperty", _IResolvable_a771d0ef]] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::DLM::LifecyclePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::DLM::LifecyclePolicy.Description``.
        :param execution_role_arn: ``AWS::DLM::LifecyclePolicy.ExecutionRoleArn``.
        :param policy_details: ``AWS::DLM::LifecyclePolicy.PolicyDetails``.
        :param state: ``AWS::DLM::LifecyclePolicy.State``.
        """
        props = CfnLifecyclePolicyProps(
            description=description,
            execution_role_arn=execution_role_arn,
            policy_details=policy_details,
            state=state,
        )

        jsii.create(CfnLifecyclePolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::DLM::LifecyclePolicy.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::DLM::LifecyclePolicy.ExecutionRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-executionrolearn
        """
        return jsii.get(self, "executionRoleArn")

    @execution_role_arn.setter # type: ignore
    def execution_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "executionRoleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="policyDetails")
    def policy_details(
        self,
    ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.PolicyDetailsProperty", _IResolvable_a771d0ef]]:
        """``AWS::DLM::LifecyclePolicy.PolicyDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-policydetails
        """
        return jsii.get(self, "policyDetails")

    @policy_details.setter # type: ignore
    def policy_details(
        self,
        value: typing.Optional[typing.Union["CfnLifecyclePolicy.PolicyDetailsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "policyDetails", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        """``AWS::DLM::LifecyclePolicy.State``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-state
        """
        return jsii.get(self, "state")

    @state.setter # type: ignore
    def state(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "state", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.CreateRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cron_expression": "cronExpression",
            "interval": "interval",
            "interval_unit": "intervalUnit",
            "times": "times",
        },
    )
    class CreateRuleProperty:
        def __init__(
            self,
            *,
            cron_expression: typing.Optional[builtins.str] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
            times: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param cron_expression: ``CfnLifecyclePolicy.CreateRuleProperty.CronExpression``.
            :param interval: ``CfnLifecyclePolicy.CreateRuleProperty.Interval``.
            :param interval_unit: ``CfnLifecyclePolicy.CreateRuleProperty.IntervalUnit``.
            :param times: ``CfnLifecyclePolicy.CreateRuleProperty.Times``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if cron_expression is not None:
                self._values["cron_expression"] = cron_expression
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit
            if times is not None:
                self._values["times"] = times

        @builtins.property
        def cron_expression(self) -> typing.Optional[builtins.str]:
            """``CfnLifecyclePolicy.CreateRuleProperty.CronExpression``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-cronexpression
            """
            result = self._values.get("cron_expression")
            return result

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            """``CfnLifecyclePolicy.CreateRuleProperty.Interval``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-interval
            """
            result = self._values.get("interval")
            return result

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            """``CfnLifecyclePolicy.CreateRuleProperty.IntervalUnit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-intervalunit
            """
            result = self._values.get("interval_unit")
            return result

        @builtins.property
        def times(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnLifecyclePolicy.CreateRuleProperty.Times``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-times
            """
            result = self._values.get("times")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"interval": "interval", "interval_unit": "intervalUnit"},
    )
    class CrossRegionCopyRetainRuleProperty:
        def __init__(
            self,
            *,
            interval: jsii.Number,
            interval_unit: builtins.str,
        ) -> None:
            """
            :param interval: ``CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty.Interval``.
            :param interval_unit: ``CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty.IntervalUnit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "interval": interval,
                "interval_unit": interval_unit,
            }

        @builtins.property
        def interval(self) -> jsii.Number:
            """``CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty.Interval``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyretainrule-interval
            """
            result = self._values.get("interval")
            assert result is not None, "Required property 'interval' is missing"
            return result

        @builtins.property
        def interval_unit(self) -> builtins.str:
            """``CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty.IntervalUnit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyretainrule-intervalunit
            """
            result = self._values.get("interval_unit")
            assert result is not None, "Required property 'interval_unit' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossRegionCopyRetainRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.CrossRegionCopyRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encrypted": "encrypted",
            "target_region": "targetRegion",
            "cmk_arn": "cmkArn",
            "copy_tags": "copyTags",
            "retain_rule": "retainRule",
        },
    )
    class CrossRegionCopyRuleProperty:
        def __init__(
            self,
            *,
            encrypted: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            target_region: builtins.str,
            cmk_arn: typing.Optional[builtins.str] = None,
            copy_tags: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            retain_rule: typing.Optional[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param encrypted: ``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.Encrypted``.
            :param target_region: ``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.TargetRegion``.
            :param cmk_arn: ``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.CmkArn``.
            :param copy_tags: ``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.CopyTags``.
            :param retain_rule: ``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.RetainRule``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "encrypted": encrypted,
                "target_region": target_region,
            }
            if cmk_arn is not None:
                self._values["cmk_arn"] = cmk_arn
            if copy_tags is not None:
                self._values["copy_tags"] = copy_tags
            if retain_rule is not None:
                self._values["retain_rule"] = retain_rule

        @builtins.property
        def encrypted(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            """``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.Encrypted``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-encrypted
            """
            result = self._values.get("encrypted")
            assert result is not None, "Required property 'encrypted' is missing"
            return result

        @builtins.property
        def target_region(self) -> builtins.str:
            """``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.TargetRegion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-targetregion
            """
            result = self._values.get("target_region")
            assert result is not None, "Required property 'target_region' is missing"
            return result

        @builtins.property
        def cmk_arn(self) -> typing.Optional[builtins.str]:
            """``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.CmkArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-cmkarn
            """
            result = self._values.get("cmk_arn")
            return result

        @builtins.property
        def copy_tags(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            """``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.CopyTags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-copytags
            """
            result = self._values.get("copy_tags")
            return result

        @builtins.property
        def retain_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty", _IResolvable_a771d0ef]]:
            """``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.RetainRule``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-retainrule
            """
            result = self._values.get("retain_rule")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossRegionCopyRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.FastRestoreRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zones": "availabilityZones",
            "count": "count",
            "interval": "interval",
            "interval_unit": "intervalUnit",
        },
    )
    class FastRestoreRuleProperty:
        def __init__(
            self,
            *,
            availability_zones: typing.Optional[typing.List[builtins.str]] = None,
            count: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param availability_zones: ``CfnLifecyclePolicy.FastRestoreRuleProperty.AvailabilityZones``.
            :param count: ``CfnLifecyclePolicy.FastRestoreRuleProperty.Count``.
            :param interval: ``CfnLifecyclePolicy.FastRestoreRuleProperty.Interval``.
            :param interval_unit: ``CfnLifecyclePolicy.FastRestoreRuleProperty.IntervalUnit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if availability_zones is not None:
                self._values["availability_zones"] = availability_zones
            if count is not None:
                self._values["count"] = count
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnLifecyclePolicy.FastRestoreRuleProperty.AvailabilityZones``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-availabilityzones
            """
            result = self._values.get("availability_zones")
            return result

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            """``CfnLifecyclePolicy.FastRestoreRuleProperty.Count``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-count
            """
            result = self._values.get("count")
            return result

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            """``CfnLifecyclePolicy.FastRestoreRuleProperty.Interval``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-interval
            """
            result = self._values.get("interval")
            return result

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            """``CfnLifecyclePolicy.FastRestoreRuleProperty.IntervalUnit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-intervalunit
            """
            result = self._values.get("interval_unit")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FastRestoreRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.ParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exclude_boot_volume": "excludeBootVolume",
            "no_reboot": "noReboot",
        },
    )
    class ParametersProperty:
        def __init__(
            self,
            *,
            exclude_boot_volume: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            no_reboot: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            """
            :param exclude_boot_volume: ``CfnLifecyclePolicy.ParametersProperty.ExcludeBootVolume``.
            :param no_reboot: ``CfnLifecyclePolicy.ParametersProperty.NoReboot``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if exclude_boot_volume is not None:
                self._values["exclude_boot_volume"] = exclude_boot_volume
            if no_reboot is not None:
                self._values["no_reboot"] = no_reboot

        @builtins.property
        def exclude_boot_volume(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            """``CfnLifecyclePolicy.ParametersProperty.ExcludeBootVolume``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html#cfn-dlm-lifecyclepolicy-parameters-excludebootvolume
            """
            result = self._values.get("exclude_boot_volume")
            return result

        @builtins.property
        def no_reboot(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            """``CfnLifecyclePolicy.ParametersProperty.NoReboot``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html#cfn-dlm-lifecyclepolicy-parameters-noreboot
            """
            result = self._values.get("no_reboot")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.PolicyDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_types": "resourceTypes",
            "schedules": "schedules",
            "target_tags": "targetTags",
            "parameters": "parameters",
            "policy_type": "policyType",
        },
    )
    class PolicyDetailsProperty:
        def __init__(
            self,
            *,
            resource_types: typing.List[builtins.str],
            schedules: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.ScheduleProperty", _IResolvable_a771d0ef]]],
            target_tags: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]],
            parameters: typing.Optional[typing.Union["CfnLifecyclePolicy.ParametersProperty", _IResolvable_a771d0ef]] = None,
            policy_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param resource_types: ``CfnLifecyclePolicy.PolicyDetailsProperty.ResourceTypes``.
            :param schedules: ``CfnLifecyclePolicy.PolicyDetailsProperty.Schedules``.
            :param target_tags: ``CfnLifecyclePolicy.PolicyDetailsProperty.TargetTags``.
            :param parameters: ``CfnLifecyclePolicy.PolicyDetailsProperty.Parameters``.
            :param policy_type: ``CfnLifecyclePolicy.PolicyDetailsProperty.PolicyType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "resource_types": resource_types,
                "schedules": schedules,
                "target_tags": target_tags,
            }
            if parameters is not None:
                self._values["parameters"] = parameters
            if policy_type is not None:
                self._values["policy_type"] = policy_type

        @builtins.property
        def resource_types(self) -> typing.List[builtins.str]:
            """``CfnLifecyclePolicy.PolicyDetailsProperty.ResourceTypes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-resourcetypes
            """
            result = self._values.get("resource_types")
            assert result is not None, "Required property 'resource_types' is missing"
            return result

        @builtins.property
        def schedules(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.ScheduleProperty", _IResolvable_a771d0ef]]]:
            """``CfnLifecyclePolicy.PolicyDetailsProperty.Schedules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-schedules
            """
            result = self._values.get("schedules")
            assert result is not None, "Required property 'schedules' is missing"
            return result

        @builtins.property
        def target_tags(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]:
            """``CfnLifecyclePolicy.PolicyDetailsProperty.TargetTags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-targettags
            """
            result = self._values.get("target_tags")
            assert result is not None, "Required property 'target_tags' is missing"
            return result

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.ParametersProperty", _IResolvable_a771d0ef]]:
            """``CfnLifecyclePolicy.PolicyDetailsProperty.Parameters``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-parameters
            """
            result = self._values.get("parameters")
            return result

        @builtins.property
        def policy_type(self) -> typing.Optional[builtins.str]:
            """``CfnLifecyclePolicy.PolicyDetailsProperty.PolicyType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-policytype
            """
            result = self._values.get("policy_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.RetainRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "count": "count",
            "interval": "interval",
            "interval_unit": "intervalUnit",
        },
    )
    class RetainRuleProperty:
        def __init__(
            self,
            *,
            count: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[jsii.Number] = None,
            interval_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param count: ``CfnLifecyclePolicy.RetainRuleProperty.Count``.
            :param interval: ``CfnLifecyclePolicy.RetainRuleProperty.Interval``.
            :param interval_unit: ``CfnLifecyclePolicy.RetainRuleProperty.IntervalUnit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count
            if interval is not None:
                self._values["interval"] = interval
            if interval_unit is not None:
                self._values["interval_unit"] = interval_unit

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            """``CfnLifecyclePolicy.RetainRuleProperty.Count``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-count
            """
            result = self._values.get("count")
            return result

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            """``CfnLifecyclePolicy.RetainRuleProperty.Interval``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-interval
            """
            result = self._values.get("interval")
            return result

        @builtins.property
        def interval_unit(self) -> typing.Optional[builtins.str]:
            """``CfnLifecyclePolicy.RetainRuleProperty.IntervalUnit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-intervalunit
            """
            result = self._values.get("interval_unit")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetainRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_dlm.CfnLifecyclePolicy.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "copy_tags": "copyTags",
            "create_rule": "createRule",
            "cross_region_copy_rules": "crossRegionCopyRules",
            "fast_restore_rule": "fastRestoreRule",
            "name": "name",
            "retain_rule": "retainRule",
            "tags_to_add": "tagsToAdd",
            "variable_tags": "variableTags",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            copy_tags: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            create_rule: typing.Optional[typing.Union["CfnLifecyclePolicy.CreateRuleProperty", _IResolvable_a771d0ef]] = None,
            cross_region_copy_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRuleProperty", _IResolvable_a771d0ef]]]] = None,
            fast_restore_rule: typing.Optional[typing.Union["CfnLifecyclePolicy.FastRestoreRuleProperty", _IResolvable_a771d0ef]] = None,
            name: typing.Optional[builtins.str] = None,
            retain_rule: typing.Optional[typing.Union["CfnLifecyclePolicy.RetainRuleProperty", _IResolvable_a771d0ef]] = None,
            tags_to_add: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]] = None,
            variable_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]] = None,
        ) -> None:
            """
            :param copy_tags: ``CfnLifecyclePolicy.ScheduleProperty.CopyTags``.
            :param create_rule: ``CfnLifecyclePolicy.ScheduleProperty.CreateRule``.
            :param cross_region_copy_rules: ``CfnLifecyclePolicy.ScheduleProperty.CrossRegionCopyRules``.
            :param fast_restore_rule: ``CfnLifecyclePolicy.ScheduleProperty.FastRestoreRule``.
            :param name: ``CfnLifecyclePolicy.ScheduleProperty.Name``.
            :param retain_rule: ``CfnLifecyclePolicy.ScheduleProperty.RetainRule``.
            :param tags_to_add: ``CfnLifecyclePolicy.ScheduleProperty.TagsToAdd``.
            :param variable_tags: ``CfnLifecyclePolicy.ScheduleProperty.VariableTags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if copy_tags is not None:
                self._values["copy_tags"] = copy_tags
            if create_rule is not None:
                self._values["create_rule"] = create_rule
            if cross_region_copy_rules is not None:
                self._values["cross_region_copy_rules"] = cross_region_copy_rules
            if fast_restore_rule is not None:
                self._values["fast_restore_rule"] = fast_restore_rule
            if name is not None:
                self._values["name"] = name
            if retain_rule is not None:
                self._values["retain_rule"] = retain_rule
            if tags_to_add is not None:
                self._values["tags_to_add"] = tags_to_add
            if variable_tags is not None:
                self._values["variable_tags"] = variable_tags

        @builtins.property
        def copy_tags(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            """``CfnLifecyclePolicy.ScheduleProperty.CopyTags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-copytags
            """
            result = self._values.get("copy_tags")
            return result

        @builtins.property
        def create_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.CreateRuleProperty", _IResolvable_a771d0ef]]:
            """``CfnLifecyclePolicy.ScheduleProperty.CreateRule``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-createrule
            """
            result = self._values.get("create_rule")
            return result

        @builtins.property
        def cross_region_copy_rules(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRuleProperty", _IResolvable_a771d0ef]]]]:
            """``CfnLifecyclePolicy.ScheduleProperty.CrossRegionCopyRules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-crossregioncopyrules
            """
            result = self._values.get("cross_region_copy_rules")
            return result

        @builtins.property
        def fast_restore_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.FastRestoreRuleProperty", _IResolvable_a771d0ef]]:
            """``CfnLifecyclePolicy.ScheduleProperty.FastRestoreRule``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-fastrestorerule
            """
            result = self._values.get("fast_restore_rule")
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnLifecyclePolicy.ScheduleProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-name
            """
            result = self._values.get("name")
            return result

        @builtins.property
        def retain_rule(
            self,
        ) -> typing.Optional[typing.Union["CfnLifecyclePolicy.RetainRuleProperty", _IResolvable_a771d0ef]]:
            """``CfnLifecyclePolicy.ScheduleProperty.RetainRule``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-retainrule
            """
            result = self._values.get("retain_rule")
            return result

        @builtins.property
        def tags_to_add(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
            """``CfnLifecyclePolicy.ScheduleProperty.TagsToAdd``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-tagstoadd
            """
            result = self._values.get("tags_to_add")
            return result

        @builtins.property
        def variable_tags(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
            """``CfnLifecyclePolicy.ScheduleProperty.VariableTags``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-variabletags
            """
            result = self._values.get("variable_tags")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_dlm.CfnLifecyclePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "execution_role_arn": "executionRoleArn",
        "policy_details": "policyDetails",
        "state": "state",
    },
)
class CfnLifecyclePolicyProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        policy_details: typing.Optional[typing.Union[CfnLifecyclePolicy.PolicyDetailsProperty, _IResolvable_a771d0ef]] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::DLM::LifecyclePolicy``.

        :param description: ``AWS::DLM::LifecyclePolicy.Description``.
        :param execution_role_arn: ``AWS::DLM::LifecyclePolicy.ExecutionRoleArn``.
        :param policy_details: ``AWS::DLM::LifecyclePolicy.PolicyDetails``.
        :param state: ``AWS::DLM::LifecyclePolicy.State``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if policy_details is not None:
            self._values["policy_details"] = policy_details
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::DLM::LifecyclePolicy.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::DLM::LifecyclePolicy.ExecutionRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-executionrolearn
        """
        result = self._values.get("execution_role_arn")
        return result

    @builtins.property
    def policy_details(
        self,
    ) -> typing.Optional[typing.Union[CfnLifecyclePolicy.PolicyDetailsProperty, _IResolvable_a771d0ef]]:
        """``AWS::DLM::LifecyclePolicy.PolicyDetails``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-policydetails
        """
        result = self._values.get("policy_details")
        return result

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        """``AWS::DLM::LifecyclePolicy.State``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-state
        """
        result = self._values.get("state")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLifecyclePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnLifecyclePolicy",
    "CfnLifecyclePolicyProps",
]

publication.publish()
