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
class CfnCacheCluster(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnCacheCluster",
):
    """A CloudFormation ``AWS::ElastiCache::CacheCluster``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html
    :cloudformationResource: AWS::ElastiCache::CacheCluster
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        cache_node_type: builtins.str,
        engine: builtins.str,
        num_cache_nodes: jsii.Number,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        az_mode: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        cache_security_group_names: typing.Optional[typing.List[builtins.str]] = None,
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_availability_zone: typing.Optional[builtins.str] = None,
        preferred_availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        snapshot_arns: typing.Optional[typing.List[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Create a new ``AWS::ElastiCache::CacheCluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cache_node_type: ``AWS::ElastiCache::CacheCluster.CacheNodeType``.
        :param engine: ``AWS::ElastiCache::CacheCluster.Engine``.
        :param num_cache_nodes: ``AWS::ElastiCache::CacheCluster.NumCacheNodes``.
        :param auto_minor_version_upgrade: ``AWS::ElastiCache::CacheCluster.AutoMinorVersionUpgrade``.
        :param az_mode: ``AWS::ElastiCache::CacheCluster.AZMode``.
        :param cache_parameter_group_name: ``AWS::ElastiCache::CacheCluster.CacheParameterGroupName``.
        :param cache_security_group_names: ``AWS::ElastiCache::CacheCluster.CacheSecurityGroupNames``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::CacheCluster.CacheSubnetGroupName``.
        :param cluster_name: ``AWS::ElastiCache::CacheCluster.ClusterName``.
        :param engine_version: ``AWS::ElastiCache::CacheCluster.EngineVersion``.
        :param notification_topic_arn: ``AWS::ElastiCache::CacheCluster.NotificationTopicArn``.
        :param port: ``AWS::ElastiCache::CacheCluster.Port``.
        :param preferred_availability_zone: ``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZone``.
        :param preferred_availability_zones: ``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZones``.
        :param preferred_maintenance_window: ``AWS::ElastiCache::CacheCluster.PreferredMaintenanceWindow``.
        :param snapshot_arns: ``AWS::ElastiCache::CacheCluster.SnapshotArns``.
        :param snapshot_name: ``AWS::ElastiCache::CacheCluster.SnapshotName``.
        :param snapshot_retention_limit: ``AWS::ElastiCache::CacheCluster.SnapshotRetentionLimit``.
        :param snapshot_window: ``AWS::ElastiCache::CacheCluster.SnapshotWindow``.
        :param tags: ``AWS::ElastiCache::CacheCluster.Tags``.
        :param vpc_security_group_ids: ``AWS::ElastiCache::CacheCluster.VpcSecurityGroupIds``.
        """
        props = CfnCacheClusterProps(
            cache_node_type=cache_node_type,
            engine=engine,
            num_cache_nodes=num_cache_nodes,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            az_mode=az_mode,
            cache_parameter_group_name=cache_parameter_group_name,
            cache_security_group_names=cache_security_group_names,
            cache_subnet_group_name=cache_subnet_group_name,
            cluster_name=cluster_name,
            engine_version=engine_version,
            notification_topic_arn=notification_topic_arn,
            port=port,
            preferred_availability_zone=preferred_availability_zone,
            preferred_availability_zones=preferred_availability_zones,
            preferred_maintenance_window=preferred_maintenance_window,
            snapshot_arns=snapshot_arns,
            snapshot_name=snapshot_name,
            snapshot_retention_limit=snapshot_retention_limit,
            snapshot_window=snapshot_window,
            tags=tags,
            vpc_security_group_ids=vpc_security_group_ids,
        )

        jsii.create(CfnCacheCluster, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrConfigurationEndpointAddress")
    def attr_configuration_endpoint_address(self) -> builtins.str:
        """
        :cloudformationAttribute: ConfigurationEndpoint.Address
        """
        return jsii.get(self, "attrConfigurationEndpointAddress")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrConfigurationEndpointPort")
    def attr_configuration_endpoint_port(self) -> builtins.str:
        """
        :cloudformationAttribute: ConfigurationEndpoint.Port
        """
        return jsii.get(self, "attrConfigurationEndpointPort")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrRedisEndpointAddress")
    def attr_redis_endpoint_address(self) -> builtins.str:
        """
        :cloudformationAttribute: RedisEndpoint.Address
        """
        return jsii.get(self, "attrRedisEndpointAddress")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrRedisEndpointPort")
    def attr_redis_endpoint_port(self) -> builtins.str:
        """
        :cloudformationAttribute: RedisEndpoint.Port
        """
        return jsii.get(self, "attrRedisEndpointPort")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::ElastiCache::CacheCluster.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cacheNodeType")
    def cache_node_type(self) -> builtins.str:
        """``AWS::ElastiCache::CacheCluster.CacheNodeType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachenodetype
        """
        return jsii.get(self, "cacheNodeType")

    @cache_node_type.setter # type: ignore
    def cache_node_type(self, value: builtins.str) -> None:
        jsii.set(self, "cacheNodeType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        """``AWS::ElastiCache::CacheCluster.Engine``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engine
        """
        return jsii.get(self, "engine")

    @engine.setter # type: ignore
    def engine(self, value: builtins.str) -> None:
        jsii.set(self, "engine", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="numCacheNodes")
    def num_cache_nodes(self) -> jsii.Number:
        """``AWS::ElastiCache::CacheCluster.NumCacheNodes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-numcachenodes
        """
        return jsii.get(self, "numCacheNodes")

    @num_cache_nodes.setter # type: ignore
    def num_cache_nodes(self, value: jsii.Number) -> None:
        jsii.set(self, "numCacheNodes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::CacheCluster.AutoMinorVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-autominorversionupgrade
        """
        return jsii.get(self, "autoMinorVersionUpgrade")

    @auto_minor_version_upgrade.setter # type: ignore
    def auto_minor_version_upgrade(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="azMode")
    def az_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.AZMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-azmode
        """
        return jsii.get(self, "azMode")

    @az_mode.setter # type: ignore
    def az_mode(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "azMode", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cacheParameterGroupName")
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.CacheParameterGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cacheparametergroupname
        """
        return jsii.get(self, "cacheParameterGroupName")

    @cache_parameter_group_name.setter # type: ignore
    def cache_parameter_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cacheParameterGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cacheSecurityGroupNames")
    def cache_security_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::CacheCluster.CacheSecurityGroupNames``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesecuritygroupnames
        """
        return jsii.get(self, "cacheSecurityGroupNames")

    @cache_security_group_names.setter # type: ignore
    def cache_security_group_names(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "cacheSecurityGroupNames", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cacheSubnetGroupName")
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.CacheSubnetGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesubnetgroupname
        """
        return jsii.get(self, "cacheSubnetGroupName")

    @cache_subnet_group_name.setter # type: ignore
    def cache_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cacheSubnetGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.ClusterName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-clustername
        """
        return jsii.get(self, "clusterName")

    @cluster_name.setter # type: ignore
    def cluster_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clusterName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.EngineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engineversion
        """
        return jsii.get(self, "engineVersion")

    @engine_version.setter # type: ignore
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "engineVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="notificationTopicArn")
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.NotificationTopicArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-notificationtopicarn
        """
        return jsii.get(self, "notificationTopicArn")

    @notification_topic_arn.setter # type: ignore
    def notification_topic_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "notificationTopicArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::CacheCluster.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-port
        """
        return jsii.get(self, "port")

    @port.setter # type: ignore
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="preferredAvailabilityZone")
    def preferred_availability_zone(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzone
        """
        return jsii.get(self, "preferredAvailabilityZone")

    @preferred_availability_zone.setter # type: ignore
    def preferred_availability_zone(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "preferredAvailabilityZone", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="preferredAvailabilityZones")
    def preferred_availability_zones(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZones``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzones
        """
        return jsii.get(self, "preferredAvailabilityZones")

    @preferred_availability_zones.setter # type: ignore
    def preferred_availability_zones(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "preferredAvailabilityZones", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.PreferredMaintenanceWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter # type: ignore
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshotArns")
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::CacheCluster.SnapshotArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotarns
        """
        return jsii.get(self, "snapshotArns")

    @snapshot_arns.setter # type: ignore
    def snapshot_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "snapshotArns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshotName")
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.SnapshotName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotname
        """
        return jsii.get(self, "snapshotName")

    @snapshot_name.setter # type: ignore
    def snapshot_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "snapshotName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshotRetentionLimit")
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::CacheCluster.SnapshotRetentionLimit``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotretentionlimit
        """
        return jsii.get(self, "snapshotRetentionLimit")

    @snapshot_retention_limit.setter # type: ignore
    def snapshot_retention_limit(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "snapshotRetentionLimit", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshotWindow")
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.SnapshotWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotwindow
        """
        return jsii.get(self, "snapshotWindow")

    @snapshot_window.setter # type: ignore
    def snapshot_window(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "snapshotWindow", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::CacheCluster.VpcSecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-vpcsecuritygroupids
        """
        return jsii.get(self, "vpcSecurityGroupIds")

    @vpc_security_group_ids.setter # type: ignore
    def vpc_security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "vpcSecurityGroupIds", value)


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnCacheClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_node_type": "cacheNodeType",
        "engine": "engine",
        "num_cache_nodes": "numCacheNodes",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "az_mode": "azMode",
        "cache_parameter_group_name": "cacheParameterGroupName",
        "cache_security_group_names": "cacheSecurityGroupNames",
        "cache_subnet_group_name": "cacheSubnetGroupName",
        "cluster_name": "clusterName",
        "engine_version": "engineVersion",
        "notification_topic_arn": "notificationTopicArn",
        "port": "port",
        "preferred_availability_zone": "preferredAvailabilityZone",
        "preferred_availability_zones": "preferredAvailabilityZones",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "snapshot_arns": "snapshotArns",
        "snapshot_name": "snapshotName",
        "snapshot_retention_limit": "snapshotRetentionLimit",
        "snapshot_window": "snapshotWindow",
        "tags": "tags",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnCacheClusterProps:
    def __init__(
        self,
        *,
        cache_node_type: builtins.str,
        engine: builtins.str,
        num_cache_nodes: jsii.Number,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        az_mode: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        cache_security_group_names: typing.Optional[typing.List[builtins.str]] = None,
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_availability_zone: typing.Optional[builtins.str] = None,
        preferred_availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        snapshot_arns: typing.Optional[typing.List[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElastiCache::CacheCluster``.

        :param cache_node_type: ``AWS::ElastiCache::CacheCluster.CacheNodeType``.
        :param engine: ``AWS::ElastiCache::CacheCluster.Engine``.
        :param num_cache_nodes: ``AWS::ElastiCache::CacheCluster.NumCacheNodes``.
        :param auto_minor_version_upgrade: ``AWS::ElastiCache::CacheCluster.AutoMinorVersionUpgrade``.
        :param az_mode: ``AWS::ElastiCache::CacheCluster.AZMode``.
        :param cache_parameter_group_name: ``AWS::ElastiCache::CacheCluster.CacheParameterGroupName``.
        :param cache_security_group_names: ``AWS::ElastiCache::CacheCluster.CacheSecurityGroupNames``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::CacheCluster.CacheSubnetGroupName``.
        :param cluster_name: ``AWS::ElastiCache::CacheCluster.ClusterName``.
        :param engine_version: ``AWS::ElastiCache::CacheCluster.EngineVersion``.
        :param notification_topic_arn: ``AWS::ElastiCache::CacheCluster.NotificationTopicArn``.
        :param port: ``AWS::ElastiCache::CacheCluster.Port``.
        :param preferred_availability_zone: ``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZone``.
        :param preferred_availability_zones: ``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZones``.
        :param preferred_maintenance_window: ``AWS::ElastiCache::CacheCluster.PreferredMaintenanceWindow``.
        :param snapshot_arns: ``AWS::ElastiCache::CacheCluster.SnapshotArns``.
        :param snapshot_name: ``AWS::ElastiCache::CacheCluster.SnapshotName``.
        :param snapshot_retention_limit: ``AWS::ElastiCache::CacheCluster.SnapshotRetentionLimit``.
        :param snapshot_window: ``AWS::ElastiCache::CacheCluster.SnapshotWindow``.
        :param tags: ``AWS::ElastiCache::CacheCluster.Tags``.
        :param vpc_security_group_ids: ``AWS::ElastiCache::CacheCluster.VpcSecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cache_node_type": cache_node_type,
            "engine": engine,
            "num_cache_nodes": num_cache_nodes,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if az_mode is not None:
            self._values["az_mode"] = az_mode
        if cache_parameter_group_name is not None:
            self._values["cache_parameter_group_name"] = cache_parameter_group_name
        if cache_security_group_names is not None:
            self._values["cache_security_group_names"] = cache_security_group_names
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn
        if port is not None:
            self._values["port"] = port
        if preferred_availability_zone is not None:
            self._values["preferred_availability_zone"] = preferred_availability_zone
        if preferred_availability_zones is not None:
            self._values["preferred_availability_zones"] = preferred_availability_zones
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if snapshot_arns is not None:
            self._values["snapshot_arns"] = snapshot_arns
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if snapshot_retention_limit is not None:
            self._values["snapshot_retention_limit"] = snapshot_retention_limit
        if snapshot_window is not None:
            self._values["snapshot_window"] = snapshot_window
        if tags is not None:
            self._values["tags"] = tags
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def cache_node_type(self) -> builtins.str:
        """``AWS::ElastiCache::CacheCluster.CacheNodeType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachenodetype
        """
        result = self._values.get("cache_node_type")
        assert result is not None, "Required property 'cache_node_type' is missing"
        return result

    @builtins.property
    def engine(self) -> builtins.str:
        """``AWS::ElastiCache::CacheCluster.Engine``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engine
        """
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return result

    @builtins.property
    def num_cache_nodes(self) -> jsii.Number:
        """``AWS::ElastiCache::CacheCluster.NumCacheNodes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-numcachenodes
        """
        result = self._values.get("num_cache_nodes")
        assert result is not None, "Required property 'num_cache_nodes' is missing"
        return result

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::CacheCluster.AutoMinorVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-autominorversionupgrade
        """
        result = self._values.get("auto_minor_version_upgrade")
        return result

    @builtins.property
    def az_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.AZMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-azmode
        """
        result = self._values.get("az_mode")
        return result

    @builtins.property
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.CacheParameterGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cacheparametergroupname
        """
        result = self._values.get("cache_parameter_group_name")
        return result

    @builtins.property
    def cache_security_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::CacheCluster.CacheSecurityGroupNames``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesecuritygroupnames
        """
        result = self._values.get("cache_security_group_names")
        return result

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.CacheSubnetGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesubnetgroupname
        """
        result = self._values.get("cache_subnet_group_name")
        return result

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.ClusterName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-clustername
        """
        result = self._values.get("cluster_name")
        return result

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.EngineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engineversion
        """
        result = self._values.get("engine_version")
        return result

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.NotificationTopicArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-notificationtopicarn
        """
        result = self._values.get("notification_topic_arn")
        return result

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::CacheCluster.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-port
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def preferred_availability_zone(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzone
        """
        result = self._values.get("preferred_availability_zone")
        return result

    @builtins.property
    def preferred_availability_zones(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::CacheCluster.PreferredAvailabilityZones``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzones
        """
        result = self._values.get("preferred_availability_zones")
        return result

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.PreferredMaintenanceWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredmaintenancewindow
        """
        result = self._values.get("preferred_maintenance_window")
        return result

    @builtins.property
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::CacheCluster.SnapshotArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotarns
        """
        result = self._values.get("snapshot_arns")
        return result

    @builtins.property
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.SnapshotName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotname
        """
        result = self._values.get("snapshot_name")
        return result

    @builtins.property
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::CacheCluster.SnapshotRetentionLimit``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotretentionlimit
        """
        result = self._values.get("snapshot_retention_limit")
        return result

    @builtins.property
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::CacheCluster.SnapshotWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotwindow
        """
        result = self._values.get("snapshot_window")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::ElastiCache::CacheCluster.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::CacheCluster.VpcSecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-vpcsecuritygroupids
        """
        result = self._values.get("vpc_security_group_ids")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCacheClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnParameterGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnParameterGroup",
):
    """A CloudFormation ``AWS::ElastiCache::ParameterGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html
    :cloudformationResource: AWS::ElastiCache::ParameterGroup
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        cache_parameter_group_family: builtins.str,
        description: builtins.str,
        properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        """Create a new ``AWS::ElastiCache::ParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cache_parameter_group_family: ``AWS::ElastiCache::ParameterGroup.CacheParameterGroupFamily``.
        :param description: ``AWS::ElastiCache::ParameterGroup.Description``.
        :param properties: ``AWS::ElastiCache::ParameterGroup.Properties``.
        """
        props = CfnParameterGroupProps(
            cache_parameter_group_family=cache_parameter_group_family,
            description=description,
            properties=properties,
        )

        jsii.create(CfnParameterGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="cacheParameterGroupFamily")
    def cache_parameter_group_family(self) -> builtins.str:
        """``AWS::ElastiCache::ParameterGroup.CacheParameterGroupFamily``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-cacheparametergroupfamily
        """
        return jsii.get(self, "cacheParameterGroupFamily")

    @cache_parameter_group_family.setter # type: ignore
    def cache_parameter_group_family(self, value: builtins.str) -> None:
        jsii.set(self, "cacheParameterGroupFamily", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        """``AWS::ElastiCache::ParameterGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::ElastiCache::ParameterGroup.Properties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-properties
        """
        return jsii.get(self, "properties")

    @properties.setter # type: ignore
    def properties(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "properties", value)


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_parameter_group_family": "cacheParameterGroupFamily",
        "description": "description",
        "properties": "properties",
    },
)
class CfnParameterGroupProps:
    def __init__(
        self,
        *,
        cache_parameter_group_family: builtins.str,
        description: builtins.str,
        properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElastiCache::ParameterGroup``.

        :param cache_parameter_group_family: ``AWS::ElastiCache::ParameterGroup.CacheParameterGroupFamily``.
        :param description: ``AWS::ElastiCache::ParameterGroup.Description``.
        :param properties: ``AWS::ElastiCache::ParameterGroup.Properties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cache_parameter_group_family": cache_parameter_group_family,
            "description": description,
        }
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def cache_parameter_group_family(self) -> builtins.str:
        """``AWS::ElastiCache::ParameterGroup.CacheParameterGroupFamily``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-cacheparametergroupfamily
        """
        result = self._values.get("cache_parameter_group_family")
        assert result is not None, "Required property 'cache_parameter_group_family' is missing"
        return result

    @builtins.property
    def description(self) -> builtins.str:
        """``AWS::ElastiCache::ParameterGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-description
        """
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return result

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::ElastiCache::ParameterGroup.Properties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-properties
        """
        result = self._values.get("properties")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnReplicationGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnReplicationGroup",
):
    """A CloudFormation ``AWS::ElastiCache::ReplicationGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html
    :cloudformationResource: AWS::ElastiCache::ReplicationGroup
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        replication_group_description: builtins.str,
        at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        auth_token: typing.Optional[builtins.str] = None,
        automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        cache_node_type: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        cache_security_group_names: typing.Optional[typing.List[builtins.str]] = None,
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        global_replication_group_id: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        multi_az_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        node_group_configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnReplicationGroup.NodeGroupConfigurationProperty", _IResolvable_a771d0ef]]]] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        num_cache_clusters: typing.Optional[jsii.Number] = None,
        num_node_groups: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_cache_cluster_a_zs: typing.Optional[typing.List[builtins.str]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        primary_cluster_id: typing.Optional[builtins.str] = None,
        replicas_per_node_group: typing.Optional[jsii.Number] = None,
        replication_group_id: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
        snapshot_arns: typing.Optional[typing.List[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshotting_cluster_id: typing.Optional[builtins.str] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        """Create a new ``AWS::ElastiCache::ReplicationGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param replication_group_description: ``AWS::ElastiCache::ReplicationGroup.ReplicationGroupDescription``.
        :param at_rest_encryption_enabled: ``AWS::ElastiCache::ReplicationGroup.AtRestEncryptionEnabled``.
        :param auth_token: ``AWS::ElastiCache::ReplicationGroup.AuthToken``.
        :param automatic_failover_enabled: ``AWS::ElastiCache::ReplicationGroup.AutomaticFailoverEnabled``.
        :param auto_minor_version_upgrade: ``AWS::ElastiCache::ReplicationGroup.AutoMinorVersionUpgrade``.
        :param cache_node_type: ``AWS::ElastiCache::ReplicationGroup.CacheNodeType``.
        :param cache_parameter_group_name: ``AWS::ElastiCache::ReplicationGroup.CacheParameterGroupName``.
        :param cache_security_group_names: ``AWS::ElastiCache::ReplicationGroup.CacheSecurityGroupNames``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::ReplicationGroup.CacheSubnetGroupName``.
        :param engine: ``AWS::ElastiCache::ReplicationGroup.Engine``.
        :param engine_version: ``AWS::ElastiCache::ReplicationGroup.EngineVersion``.
        :param global_replication_group_id: ``AWS::ElastiCache::ReplicationGroup.GlobalReplicationGroupId``.
        :param kms_key_id: ``AWS::ElastiCache::ReplicationGroup.KmsKeyId``.
        :param multi_az_enabled: ``AWS::ElastiCache::ReplicationGroup.MultiAZEnabled``.
        :param node_group_configuration: ``AWS::ElastiCache::ReplicationGroup.NodeGroupConfiguration``.
        :param notification_topic_arn: ``AWS::ElastiCache::ReplicationGroup.NotificationTopicArn``.
        :param num_cache_clusters: ``AWS::ElastiCache::ReplicationGroup.NumCacheClusters``.
        :param num_node_groups: ``AWS::ElastiCache::ReplicationGroup.NumNodeGroups``.
        :param port: ``AWS::ElastiCache::ReplicationGroup.Port``.
        :param preferred_cache_cluster_a_zs: ``AWS::ElastiCache::ReplicationGroup.PreferredCacheClusterAZs``.
        :param preferred_maintenance_window: ``AWS::ElastiCache::ReplicationGroup.PreferredMaintenanceWindow``.
        :param primary_cluster_id: ``AWS::ElastiCache::ReplicationGroup.PrimaryClusterId``.
        :param replicas_per_node_group: ``AWS::ElastiCache::ReplicationGroup.ReplicasPerNodeGroup``.
        :param replication_group_id: ``AWS::ElastiCache::ReplicationGroup.ReplicationGroupId``.
        :param security_group_ids: ``AWS::ElastiCache::ReplicationGroup.SecurityGroupIds``.
        :param snapshot_arns: ``AWS::ElastiCache::ReplicationGroup.SnapshotArns``.
        :param snapshot_name: ``AWS::ElastiCache::ReplicationGroup.SnapshotName``.
        :param snapshot_retention_limit: ``AWS::ElastiCache::ReplicationGroup.SnapshotRetentionLimit``.
        :param snapshotting_cluster_id: ``AWS::ElastiCache::ReplicationGroup.SnapshottingClusterId``.
        :param snapshot_window: ``AWS::ElastiCache::ReplicationGroup.SnapshotWindow``.
        :param tags: ``AWS::ElastiCache::ReplicationGroup.Tags``.
        :param transit_encryption_enabled: ``AWS::ElastiCache::ReplicationGroup.TransitEncryptionEnabled``.
        """
        props = CfnReplicationGroupProps(
            replication_group_description=replication_group_description,
            at_rest_encryption_enabled=at_rest_encryption_enabled,
            auth_token=auth_token,
            automatic_failover_enabled=automatic_failover_enabled,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            cache_node_type=cache_node_type,
            cache_parameter_group_name=cache_parameter_group_name,
            cache_security_group_names=cache_security_group_names,
            cache_subnet_group_name=cache_subnet_group_name,
            engine=engine,
            engine_version=engine_version,
            global_replication_group_id=global_replication_group_id,
            kms_key_id=kms_key_id,
            multi_az_enabled=multi_az_enabled,
            node_group_configuration=node_group_configuration,
            notification_topic_arn=notification_topic_arn,
            num_cache_clusters=num_cache_clusters,
            num_node_groups=num_node_groups,
            port=port,
            preferred_cache_cluster_a_zs=preferred_cache_cluster_a_zs,
            preferred_maintenance_window=preferred_maintenance_window,
            primary_cluster_id=primary_cluster_id,
            replicas_per_node_group=replicas_per_node_group,
            replication_group_id=replication_group_id,
            security_group_ids=security_group_ids,
            snapshot_arns=snapshot_arns,
            snapshot_name=snapshot_name,
            snapshot_retention_limit=snapshot_retention_limit,
            snapshotting_cluster_id=snapshotting_cluster_id,
            snapshot_window=snapshot_window,
            tags=tags,
            transit_encryption_enabled=transit_encryption_enabled,
        )

        jsii.create(CfnReplicationGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrConfigurationEndPointAddress")
    def attr_configuration_end_point_address(self) -> builtins.str:
        """
        :cloudformationAttribute: ConfigurationEndPoint.Address
        """
        return jsii.get(self, "attrConfigurationEndPointAddress")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrConfigurationEndPointPort")
    def attr_configuration_end_point_port(self) -> builtins.str:
        """
        :cloudformationAttribute: ConfigurationEndPoint.Port
        """
        return jsii.get(self, "attrConfigurationEndPointPort")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrPrimaryEndPointAddress")
    def attr_primary_end_point_address(self) -> builtins.str:
        """
        :cloudformationAttribute: PrimaryEndPoint.Address
        """
        return jsii.get(self, "attrPrimaryEndPointAddress")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrPrimaryEndPointPort")
    def attr_primary_end_point_port(self) -> builtins.str:
        """
        :cloudformationAttribute: PrimaryEndPoint.Port
        """
        return jsii.get(self, "attrPrimaryEndPointPort")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrReadEndPointAddresses")
    def attr_read_end_point_addresses(self) -> builtins.str:
        """
        :cloudformationAttribute: ReadEndPoint.Addresses
        """
        return jsii.get(self, "attrReadEndPointAddresses")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrReadEndPointAddressesList")
    def attr_read_end_point_addresses_list(self) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: ReadEndPoint.Addresses.List
        """
        return jsii.get(self, "attrReadEndPointAddressesList")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrReadEndPointPorts")
    def attr_read_end_point_ports(self) -> builtins.str:
        """
        :cloudformationAttribute: ReadEndPoint.Ports
        """
        return jsii.get(self, "attrReadEndPointPorts")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrReadEndPointPortsList")
    def attr_read_end_point_ports_list(self) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: ReadEndPoint.Ports.List
        """
        return jsii.get(self, "attrReadEndPointPortsList")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrReaderEndPointAddress")
    def attr_reader_end_point_address(self) -> builtins.str:
        """
        :cloudformationAttribute: ReaderEndPoint.Address
        """
        return jsii.get(self, "attrReaderEndPointAddress")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrReaderEndPointPort")
    def attr_reader_end_point_port(self) -> builtins.str:
        """
        :cloudformationAttribute: ReaderEndPoint.Port
        """
        return jsii.get(self, "attrReaderEndPointPort")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::ElastiCache::ReplicationGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="replicationGroupDescription")
    def replication_group_description(self) -> builtins.str:
        """``AWS::ElastiCache::ReplicationGroup.ReplicationGroupDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupdescription
        """
        return jsii.get(self, "replicationGroupDescription")

    @replication_group_description.setter # type: ignore
    def replication_group_description(self, value: builtins.str) -> None:
        jsii.set(self, "replicationGroupDescription", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="atRestEncryptionEnabled")
    def at_rest_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::ReplicationGroup.AtRestEncryptionEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-atrestencryptionenabled
        """
        return jsii.get(self, "atRestEncryptionEnabled")

    @at_rest_encryption_enabled.setter # type: ignore
    def at_rest_encryption_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "atRestEncryptionEnabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="authToken")
    def auth_token(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.AuthToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-authtoken
        """
        return jsii.get(self, "authToken")

    @auth_token.setter # type: ignore
    def auth_token(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "authToken", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="automaticFailoverEnabled")
    def automatic_failover_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::ReplicationGroup.AutomaticFailoverEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-automaticfailoverenabled
        """
        return jsii.get(self, "automaticFailoverEnabled")

    @automatic_failover_enabled.setter # type: ignore
    def automatic_failover_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "automaticFailoverEnabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::ReplicationGroup.AutoMinorVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-autominorversionupgrade
        """
        return jsii.get(self, "autoMinorVersionUpgrade")

    @auto_minor_version_upgrade.setter # type: ignore
    def auto_minor_version_upgrade(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cacheNodeType")
    def cache_node_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheNodeType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachenodetype
        """
        return jsii.get(self, "cacheNodeType")

    @cache_node_type.setter # type: ignore
    def cache_node_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cacheNodeType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cacheParameterGroupName")
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheParameterGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cacheparametergroupname
        """
        return jsii.get(self, "cacheParameterGroupName")

    @cache_parameter_group_name.setter # type: ignore
    def cache_parameter_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cacheParameterGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cacheSecurityGroupNames")
    def cache_security_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::ReplicationGroup.CacheSecurityGroupNames``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesecuritygroupnames
        """
        return jsii.get(self, "cacheSecurityGroupNames")

    @cache_security_group_names.setter # type: ignore
    def cache_security_group_names(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "cacheSecurityGroupNames", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cacheSubnetGroupName")
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheSubnetGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesubnetgroupname
        """
        return jsii.get(self, "cacheSubnetGroupName")

    @cache_subnet_group_name.setter # type: ignore
    def cache_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cacheSubnetGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engine")
    def engine(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.Engine``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engine
        """
        return jsii.get(self, "engine")

    @engine.setter # type: ignore
    def engine(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "engine", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.EngineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engineversion
        """
        return jsii.get(self, "engineVersion")

    @engine_version.setter # type: ignore
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "engineVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="globalReplicationGroupId")
    def global_replication_group_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.GlobalReplicationGroupId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-globalreplicationgroupid
        """
        return jsii.get(self, "globalReplicationGroupId")

    @global_replication_group_id.setter # type: ignore
    def global_replication_group_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "globalReplicationGroupId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter # type: ignore
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="multiAzEnabled")
    def multi_az_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::ReplicationGroup.MultiAZEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-multiazenabled
        """
        return jsii.get(self, "multiAzEnabled")

    @multi_az_enabled.setter # type: ignore
    def multi_az_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "multiAzEnabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="nodeGroupConfiguration")
    def node_group_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnReplicationGroup.NodeGroupConfigurationProperty", _IResolvable_a771d0ef]]]]:
        """``AWS::ElastiCache::ReplicationGroup.NodeGroupConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-nodegroupconfiguration
        """
        return jsii.get(self, "nodeGroupConfiguration")

    @node_group_configuration.setter # type: ignore
    def node_group_configuration(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnReplicationGroup.NodeGroupConfigurationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "nodeGroupConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="notificationTopicArn")
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.NotificationTopicArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-notificationtopicarn
        """
        return jsii.get(self, "notificationTopicArn")

    @notification_topic_arn.setter # type: ignore
    def notification_topic_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "notificationTopicArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="numCacheClusters")
    def num_cache_clusters(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.NumCacheClusters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numcacheclusters
        """
        return jsii.get(self, "numCacheClusters")

    @num_cache_clusters.setter # type: ignore
    def num_cache_clusters(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "numCacheClusters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="numNodeGroups")
    def num_node_groups(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.NumNodeGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numnodegroups
        """
        return jsii.get(self, "numNodeGroups")

    @num_node_groups.setter # type: ignore
    def num_node_groups(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "numNodeGroups", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-port
        """
        return jsii.get(self, "port")

    @port.setter # type: ignore
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="preferredCacheClusterAZs")
    def preferred_cache_cluster_a_zs(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::ReplicationGroup.PreferredCacheClusterAZs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredcacheclusterazs
        """
        return jsii.get(self, "preferredCacheClusterAZs")

    @preferred_cache_cluster_a_zs.setter # type: ignore
    def preferred_cache_cluster_a_zs(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "preferredCacheClusterAZs", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.PreferredMaintenanceWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter # type: ignore
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="primaryClusterId")
    def primary_cluster_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.PrimaryClusterId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-primaryclusterid
        """
        return jsii.get(self, "primaryClusterId")

    @primary_cluster_id.setter # type: ignore
    def primary_cluster_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "primaryClusterId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="replicasPerNodeGroup")
    def replicas_per_node_group(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.ReplicasPerNodeGroup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicaspernodegroup
        """
        return jsii.get(self, "replicasPerNodeGroup")

    @replicas_per_node_group.setter # type: ignore
    def replicas_per_node_group(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "replicasPerNodeGroup", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="replicationGroupId")
    def replication_group_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.ReplicationGroupId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupid
        """
        return jsii.get(self, "replicationGroupId")

    @replication_group_id.setter # type: ignore
    def replication_group_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "replicationGroupId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::ReplicationGroup.SecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-securitygroupids
        """
        return jsii.get(self, "securityGroupIds")

    @security_group_ids.setter # type: ignore
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "securityGroupIds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshotArns")
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotarns
        """
        return jsii.get(self, "snapshotArns")

    @snapshot_arns.setter # type: ignore
    def snapshot_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "snapshotArns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshotName")
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotname
        """
        return jsii.get(self, "snapshotName")

    @snapshot_name.setter # type: ignore
    def snapshot_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "snapshotName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshotRetentionLimit")
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotRetentionLimit``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotretentionlimit
        """
        return jsii.get(self, "snapshotRetentionLimit")

    @snapshot_retention_limit.setter # type: ignore
    def snapshot_retention_limit(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "snapshotRetentionLimit", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshottingClusterId")
    def snapshotting_cluster_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshottingClusterId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshottingclusterid
        """
        return jsii.get(self, "snapshottingClusterId")

    @snapshotting_cluster_id.setter # type: ignore
    def snapshotting_cluster_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "snapshottingClusterId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshotWindow")
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotwindow
        """
        return jsii.get(self, "snapshotWindow")

    @snapshot_window.setter # type: ignore
    def snapshot_window(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "snapshotWindow", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="transitEncryptionEnabled")
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::ReplicationGroup.TransitEncryptionEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-transitencryptionenabled
        """
        return jsii.get(self, "transitEncryptionEnabled")

    @transit_encryption_enabled.setter # type: ignore
    def transit_encryption_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "transitEncryptionEnabled", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnReplicationGroup.NodeGroupConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "node_group_id": "nodeGroupId",
            "primary_availability_zone": "primaryAvailabilityZone",
            "replica_availability_zones": "replicaAvailabilityZones",
            "replica_count": "replicaCount",
            "slots": "slots",
        },
    )
    class NodeGroupConfigurationProperty:
        def __init__(
            self,
            *,
            node_group_id: typing.Optional[builtins.str] = None,
            primary_availability_zone: typing.Optional[builtins.str] = None,
            replica_availability_zones: typing.Optional[typing.List[builtins.str]] = None,
            replica_count: typing.Optional[jsii.Number] = None,
            slots: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param node_group_id: ``CfnReplicationGroup.NodeGroupConfigurationProperty.NodeGroupId``.
            :param primary_availability_zone: ``CfnReplicationGroup.NodeGroupConfigurationProperty.PrimaryAvailabilityZone``.
            :param replica_availability_zones: ``CfnReplicationGroup.NodeGroupConfigurationProperty.ReplicaAvailabilityZones``.
            :param replica_count: ``CfnReplicationGroup.NodeGroupConfigurationProperty.ReplicaCount``.
            :param slots: ``CfnReplicationGroup.NodeGroupConfigurationProperty.Slots``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if node_group_id is not None:
                self._values["node_group_id"] = node_group_id
            if primary_availability_zone is not None:
                self._values["primary_availability_zone"] = primary_availability_zone
            if replica_availability_zones is not None:
                self._values["replica_availability_zones"] = replica_availability_zones
            if replica_count is not None:
                self._values["replica_count"] = replica_count
            if slots is not None:
                self._values["slots"] = slots

        @builtins.property
        def node_group_id(self) -> typing.Optional[builtins.str]:
            """``CfnReplicationGroup.NodeGroupConfigurationProperty.NodeGroupId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-nodegroupid
            """
            result = self._values.get("node_group_id")
            return result

        @builtins.property
        def primary_availability_zone(self) -> typing.Optional[builtins.str]:
            """``CfnReplicationGroup.NodeGroupConfigurationProperty.PrimaryAvailabilityZone``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-primaryavailabilityzone
            """
            result = self._values.get("primary_availability_zone")
            return result

        @builtins.property
        def replica_availability_zones(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnReplicationGroup.NodeGroupConfigurationProperty.ReplicaAvailabilityZones``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-replicaavailabilityzones
            """
            result = self._values.get("replica_availability_zones")
            return result

        @builtins.property
        def replica_count(self) -> typing.Optional[jsii.Number]:
            """``CfnReplicationGroup.NodeGroupConfigurationProperty.ReplicaCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-replicacount
            """
            result = self._values.get("replica_count")
            return result

        @builtins.property
        def slots(self) -> typing.Optional[builtins.str]:
            """``CfnReplicationGroup.NodeGroupConfigurationProperty.Slots``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-slots
            """
            result = self._values.get("slots")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeGroupConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnReplicationGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "replication_group_description": "replicationGroupDescription",
        "at_rest_encryption_enabled": "atRestEncryptionEnabled",
        "auth_token": "authToken",
        "automatic_failover_enabled": "automaticFailoverEnabled",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "cache_node_type": "cacheNodeType",
        "cache_parameter_group_name": "cacheParameterGroupName",
        "cache_security_group_names": "cacheSecurityGroupNames",
        "cache_subnet_group_name": "cacheSubnetGroupName",
        "engine": "engine",
        "engine_version": "engineVersion",
        "global_replication_group_id": "globalReplicationGroupId",
        "kms_key_id": "kmsKeyId",
        "multi_az_enabled": "multiAzEnabled",
        "node_group_configuration": "nodeGroupConfiguration",
        "notification_topic_arn": "notificationTopicArn",
        "num_cache_clusters": "numCacheClusters",
        "num_node_groups": "numNodeGroups",
        "port": "port",
        "preferred_cache_cluster_a_zs": "preferredCacheClusterAZs",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "primary_cluster_id": "primaryClusterId",
        "replicas_per_node_group": "replicasPerNodeGroup",
        "replication_group_id": "replicationGroupId",
        "security_group_ids": "securityGroupIds",
        "snapshot_arns": "snapshotArns",
        "snapshot_name": "snapshotName",
        "snapshot_retention_limit": "snapshotRetentionLimit",
        "snapshotting_cluster_id": "snapshottingClusterId",
        "snapshot_window": "snapshotWindow",
        "tags": "tags",
        "transit_encryption_enabled": "transitEncryptionEnabled",
    },
)
class CfnReplicationGroupProps:
    def __init__(
        self,
        *,
        replication_group_description: builtins.str,
        at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        auth_token: typing.Optional[builtins.str] = None,
        automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        cache_node_type: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        cache_security_group_names: typing.Optional[typing.List[builtins.str]] = None,
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        global_replication_group_id: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        multi_az_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        node_group_configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnReplicationGroup.NodeGroupConfigurationProperty, _IResolvable_a771d0ef]]]] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        num_cache_clusters: typing.Optional[jsii.Number] = None,
        num_node_groups: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_cache_cluster_a_zs: typing.Optional[typing.List[builtins.str]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        primary_cluster_id: typing.Optional[builtins.str] = None,
        replicas_per_node_group: typing.Optional[jsii.Number] = None,
        replication_group_id: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
        snapshot_arns: typing.Optional[typing.List[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshotting_cluster_id: typing.Optional[builtins.str] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElastiCache::ReplicationGroup``.

        :param replication_group_description: ``AWS::ElastiCache::ReplicationGroup.ReplicationGroupDescription``.
        :param at_rest_encryption_enabled: ``AWS::ElastiCache::ReplicationGroup.AtRestEncryptionEnabled``.
        :param auth_token: ``AWS::ElastiCache::ReplicationGroup.AuthToken``.
        :param automatic_failover_enabled: ``AWS::ElastiCache::ReplicationGroup.AutomaticFailoverEnabled``.
        :param auto_minor_version_upgrade: ``AWS::ElastiCache::ReplicationGroup.AutoMinorVersionUpgrade``.
        :param cache_node_type: ``AWS::ElastiCache::ReplicationGroup.CacheNodeType``.
        :param cache_parameter_group_name: ``AWS::ElastiCache::ReplicationGroup.CacheParameterGroupName``.
        :param cache_security_group_names: ``AWS::ElastiCache::ReplicationGroup.CacheSecurityGroupNames``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::ReplicationGroup.CacheSubnetGroupName``.
        :param engine: ``AWS::ElastiCache::ReplicationGroup.Engine``.
        :param engine_version: ``AWS::ElastiCache::ReplicationGroup.EngineVersion``.
        :param global_replication_group_id: ``AWS::ElastiCache::ReplicationGroup.GlobalReplicationGroupId``.
        :param kms_key_id: ``AWS::ElastiCache::ReplicationGroup.KmsKeyId``.
        :param multi_az_enabled: ``AWS::ElastiCache::ReplicationGroup.MultiAZEnabled``.
        :param node_group_configuration: ``AWS::ElastiCache::ReplicationGroup.NodeGroupConfiguration``.
        :param notification_topic_arn: ``AWS::ElastiCache::ReplicationGroup.NotificationTopicArn``.
        :param num_cache_clusters: ``AWS::ElastiCache::ReplicationGroup.NumCacheClusters``.
        :param num_node_groups: ``AWS::ElastiCache::ReplicationGroup.NumNodeGroups``.
        :param port: ``AWS::ElastiCache::ReplicationGroup.Port``.
        :param preferred_cache_cluster_a_zs: ``AWS::ElastiCache::ReplicationGroup.PreferredCacheClusterAZs``.
        :param preferred_maintenance_window: ``AWS::ElastiCache::ReplicationGroup.PreferredMaintenanceWindow``.
        :param primary_cluster_id: ``AWS::ElastiCache::ReplicationGroup.PrimaryClusterId``.
        :param replicas_per_node_group: ``AWS::ElastiCache::ReplicationGroup.ReplicasPerNodeGroup``.
        :param replication_group_id: ``AWS::ElastiCache::ReplicationGroup.ReplicationGroupId``.
        :param security_group_ids: ``AWS::ElastiCache::ReplicationGroup.SecurityGroupIds``.
        :param snapshot_arns: ``AWS::ElastiCache::ReplicationGroup.SnapshotArns``.
        :param snapshot_name: ``AWS::ElastiCache::ReplicationGroup.SnapshotName``.
        :param snapshot_retention_limit: ``AWS::ElastiCache::ReplicationGroup.SnapshotRetentionLimit``.
        :param snapshotting_cluster_id: ``AWS::ElastiCache::ReplicationGroup.SnapshottingClusterId``.
        :param snapshot_window: ``AWS::ElastiCache::ReplicationGroup.SnapshotWindow``.
        :param tags: ``AWS::ElastiCache::ReplicationGroup.Tags``.
        :param transit_encryption_enabled: ``AWS::ElastiCache::ReplicationGroup.TransitEncryptionEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "replication_group_description": replication_group_description,
        }
        if at_rest_encryption_enabled is not None:
            self._values["at_rest_encryption_enabled"] = at_rest_encryption_enabled
        if auth_token is not None:
            self._values["auth_token"] = auth_token
        if automatic_failover_enabled is not None:
            self._values["automatic_failover_enabled"] = automatic_failover_enabled
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if cache_node_type is not None:
            self._values["cache_node_type"] = cache_node_type
        if cache_parameter_group_name is not None:
            self._values["cache_parameter_group_name"] = cache_parameter_group_name
        if cache_security_group_names is not None:
            self._values["cache_security_group_names"] = cache_security_group_names
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name
        if engine is not None:
            self._values["engine"] = engine
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if global_replication_group_id is not None:
            self._values["global_replication_group_id"] = global_replication_group_id
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if multi_az_enabled is not None:
            self._values["multi_az_enabled"] = multi_az_enabled
        if node_group_configuration is not None:
            self._values["node_group_configuration"] = node_group_configuration
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn
        if num_cache_clusters is not None:
            self._values["num_cache_clusters"] = num_cache_clusters
        if num_node_groups is not None:
            self._values["num_node_groups"] = num_node_groups
        if port is not None:
            self._values["port"] = port
        if preferred_cache_cluster_a_zs is not None:
            self._values["preferred_cache_cluster_a_zs"] = preferred_cache_cluster_a_zs
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if primary_cluster_id is not None:
            self._values["primary_cluster_id"] = primary_cluster_id
        if replicas_per_node_group is not None:
            self._values["replicas_per_node_group"] = replicas_per_node_group
        if replication_group_id is not None:
            self._values["replication_group_id"] = replication_group_id
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if snapshot_arns is not None:
            self._values["snapshot_arns"] = snapshot_arns
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if snapshot_retention_limit is not None:
            self._values["snapshot_retention_limit"] = snapshot_retention_limit
        if snapshotting_cluster_id is not None:
            self._values["snapshotting_cluster_id"] = snapshotting_cluster_id
        if snapshot_window is not None:
            self._values["snapshot_window"] = snapshot_window
        if tags is not None:
            self._values["tags"] = tags
        if transit_encryption_enabled is not None:
            self._values["transit_encryption_enabled"] = transit_encryption_enabled

    @builtins.property
    def replication_group_description(self) -> builtins.str:
        """``AWS::ElastiCache::ReplicationGroup.ReplicationGroupDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupdescription
        """
        result = self._values.get("replication_group_description")
        assert result is not None, "Required property 'replication_group_description' is missing"
        return result

    @builtins.property
    def at_rest_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::ReplicationGroup.AtRestEncryptionEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-atrestencryptionenabled
        """
        result = self._values.get("at_rest_encryption_enabled")
        return result

    @builtins.property
    def auth_token(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.AuthToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-authtoken
        """
        result = self._values.get("auth_token")
        return result

    @builtins.property
    def automatic_failover_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::ReplicationGroup.AutomaticFailoverEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-automaticfailoverenabled
        """
        result = self._values.get("automatic_failover_enabled")
        return result

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::ReplicationGroup.AutoMinorVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-autominorversionupgrade
        """
        result = self._values.get("auto_minor_version_upgrade")
        return result

    @builtins.property
    def cache_node_type(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheNodeType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachenodetype
        """
        result = self._values.get("cache_node_type")
        return result

    @builtins.property
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheParameterGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cacheparametergroupname
        """
        result = self._values.get("cache_parameter_group_name")
        return result

    @builtins.property
    def cache_security_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::ReplicationGroup.CacheSecurityGroupNames``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesecuritygroupnames
        """
        result = self._values.get("cache_security_group_names")
        return result

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.CacheSubnetGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesubnetgroupname
        """
        result = self._values.get("cache_subnet_group_name")
        return result

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.Engine``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engine
        """
        result = self._values.get("engine")
        return result

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.EngineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engineversion
        """
        result = self._values.get("engine_version")
        return result

    @builtins.property
    def global_replication_group_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.GlobalReplicationGroupId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-globalreplicationgroupid
        """
        result = self._values.get("global_replication_group_id")
        return result

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-kmskeyid
        """
        result = self._values.get("kms_key_id")
        return result

    @builtins.property
    def multi_az_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::ReplicationGroup.MultiAZEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-multiazenabled
        """
        result = self._values.get("multi_az_enabled")
        return result

    @builtins.property
    def node_group_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnReplicationGroup.NodeGroupConfigurationProperty, _IResolvable_a771d0ef]]]]:
        """``AWS::ElastiCache::ReplicationGroup.NodeGroupConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-nodegroupconfiguration
        """
        result = self._values.get("node_group_configuration")
        return result

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.NotificationTopicArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-notificationtopicarn
        """
        result = self._values.get("notification_topic_arn")
        return result

    @builtins.property
    def num_cache_clusters(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.NumCacheClusters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numcacheclusters
        """
        result = self._values.get("num_cache_clusters")
        return result

    @builtins.property
    def num_node_groups(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.NumNodeGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numnodegroups
        """
        result = self._values.get("num_node_groups")
        return result

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-port
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def preferred_cache_cluster_a_zs(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::ReplicationGroup.PreferredCacheClusterAZs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredcacheclusterazs
        """
        result = self._values.get("preferred_cache_cluster_a_zs")
        return result

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.PreferredMaintenanceWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredmaintenancewindow
        """
        result = self._values.get("preferred_maintenance_window")
        return result

    @builtins.property
    def primary_cluster_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.PrimaryClusterId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-primaryclusterid
        """
        result = self._values.get("primary_cluster_id")
        return result

    @builtins.property
    def replicas_per_node_group(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.ReplicasPerNodeGroup``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicaspernodegroup
        """
        result = self._values.get("replicas_per_node_group")
        return result

    @builtins.property
    def replication_group_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.ReplicationGroupId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupid
        """
        result = self._values.get("replication_group_id")
        return result

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::ReplicationGroup.SecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-securitygroupids
        """
        result = self._values.get("security_group_ids")
        return result

    @builtins.property
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotarns
        """
        result = self._values.get("snapshot_arns")
        return result

    @builtins.property
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotname
        """
        result = self._values.get("snapshot_name")
        return result

    @builtins.property
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotRetentionLimit``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotretentionlimit
        """
        result = self._values.get("snapshot_retention_limit")
        return result

    @builtins.property
    def snapshotting_cluster_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshottingClusterId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshottingclusterid
        """
        result = self._values.get("snapshotting_cluster_id")
        return result

    @builtins.property
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::ReplicationGroup.SnapshotWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotwindow
        """
        result = self._values.get("snapshot_window")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::ElastiCache::ReplicationGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::ElastiCache::ReplicationGroup.TransitEncryptionEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-transitencryptionenabled
        """
        result = self._values.get("transit_encryption_enabled")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSecurityGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnSecurityGroup",
):
    """A CloudFormation ``AWS::ElastiCache::SecurityGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html
    :cloudformationResource: AWS::ElastiCache::SecurityGroup
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: builtins.str,
    ) -> None:
        """Create a new ``AWS::ElastiCache::SecurityGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::ElastiCache::SecurityGroup.Description``.
        """
        props = CfnSecurityGroupProps(description=description)

        jsii.create(CfnSecurityGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        """``AWS::ElastiCache::SecurityGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html#cfn-elasticache-securitygroup-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnSecurityGroupIngress(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnSecurityGroupIngress",
):
    """A CloudFormation ``AWS::ElastiCache::SecurityGroupIngress``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html
    :cloudformationResource: AWS::ElastiCache::SecurityGroupIngress
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        cache_security_group_name: builtins.str,
        ec2_security_group_name: builtins.str,
        ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ElastiCache::SecurityGroupIngress``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cache_security_group_name: ``AWS::ElastiCache::SecurityGroupIngress.CacheSecurityGroupName``.
        :param ec2_security_group_name: ``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupName``.
        :param ec2_security_group_owner_id: ``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupOwnerId``.
        """
        props = CfnSecurityGroupIngressProps(
            cache_security_group_name=cache_security_group_name,
            ec2_security_group_name=ec2_security_group_name,
            ec2_security_group_owner_id=ec2_security_group_owner_id,
        )

        jsii.create(CfnSecurityGroupIngress, self, [scope, id, props])

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
    @jsii.member(jsii_name="cacheSecurityGroupName")
    def cache_security_group_name(self) -> builtins.str:
        """``AWS::ElastiCache::SecurityGroupIngress.CacheSecurityGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-cachesecuritygroupname
        """
        return jsii.get(self, "cacheSecurityGroupName")

    @cache_security_group_name.setter # type: ignore
    def cache_security_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "cacheSecurityGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ec2SecurityGroupName")
    def ec2_security_group_name(self) -> builtins.str:
        """``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupname
        """
        return jsii.get(self, "ec2SecurityGroupName")

    @ec2_security_group_name.setter # type: ignore
    def ec2_security_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "ec2SecurityGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ec2SecurityGroupOwnerId")
    def ec2_security_group_owner_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupOwnerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupownerid
        """
        return jsii.get(self, "ec2SecurityGroupOwnerId")

    @ec2_security_group_owner_id.setter # type: ignore
    def ec2_security_group_owner_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ec2SecurityGroupOwnerId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnSecurityGroupIngressProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_security_group_name": "cacheSecurityGroupName",
        "ec2_security_group_name": "ec2SecurityGroupName",
        "ec2_security_group_owner_id": "ec2SecurityGroupOwnerId",
    },
)
class CfnSecurityGroupIngressProps:
    def __init__(
        self,
        *,
        cache_security_group_name: builtins.str,
        ec2_security_group_name: builtins.str,
        ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElastiCache::SecurityGroupIngress``.

        :param cache_security_group_name: ``AWS::ElastiCache::SecurityGroupIngress.CacheSecurityGroupName``.
        :param ec2_security_group_name: ``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupName``.
        :param ec2_security_group_owner_id: ``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupOwnerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cache_security_group_name": cache_security_group_name,
            "ec2_security_group_name": ec2_security_group_name,
        }
        if ec2_security_group_owner_id is not None:
            self._values["ec2_security_group_owner_id"] = ec2_security_group_owner_id

    @builtins.property
    def cache_security_group_name(self) -> builtins.str:
        """``AWS::ElastiCache::SecurityGroupIngress.CacheSecurityGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-cachesecuritygroupname
        """
        result = self._values.get("cache_security_group_name")
        assert result is not None, "Required property 'cache_security_group_name' is missing"
        return result

    @builtins.property
    def ec2_security_group_name(self) -> builtins.str:
        """``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupname
        """
        result = self._values.get("ec2_security_group_name")
        assert result is not None, "Required property 'ec2_security_group_name' is missing"
        return result

    @builtins.property
    def ec2_security_group_owner_id(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::SecurityGroupIngress.EC2SecurityGroupOwnerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupownerid
        """
        result = self._values.get("ec2_security_group_owner_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityGroupIngressProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnSecurityGroupProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description"},
)
class CfnSecurityGroupProps:
    def __init__(self, *, description: builtins.str) -> None:
        """Properties for defining a ``AWS::ElastiCache::SecurityGroup``.

        :param description: ``AWS::ElastiCache::SecurityGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
        }

    @builtins.property
    def description(self) -> builtins.str:
        """``AWS::ElastiCache::SecurityGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html#cfn-elasticache-securitygroup-description
        """
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSubnetGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnSubnetGroup",
):
    """A CloudFormation ``AWS::ElastiCache::SubnetGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html
    :cloudformationResource: AWS::ElastiCache::SubnetGroup
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: builtins.str,
        subnet_ids: typing.List[builtins.str],
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ElastiCache::SubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::ElastiCache::SubnetGroup.Description``.
        :param subnet_ids: ``AWS::ElastiCache::SubnetGroup.SubnetIds``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::SubnetGroup.CacheSubnetGroupName``.
        """
        props = CfnSubnetGroupProps(
            description=description,
            subnet_ids=subnet_ids,
            cache_subnet_group_name=cache_subnet_group_name,
        )

        jsii.create(CfnSubnetGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        """``AWS::ElastiCache::SubnetGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        """``AWS::ElastiCache::SubnetGroup.SubnetIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter # type: ignore
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "subnetIds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cacheSubnetGroupName")
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::SubnetGroup.CacheSubnetGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-cachesubnetgroupname
        """
        return jsii.get(self, "cacheSubnetGroupName")

    @cache_subnet_group_name.setter # type: ignore
    def cache_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cacheSubnetGroupName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "subnet_ids": "subnetIds",
        "cache_subnet_group_name": "cacheSubnetGroupName",
    },
)
class CfnSubnetGroupProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        subnet_ids: typing.List[builtins.str],
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ElastiCache::SubnetGroup``.

        :param description: ``AWS::ElastiCache::SubnetGroup.Description``.
        :param subnet_ids: ``AWS::ElastiCache::SubnetGroup.SubnetIds``.
        :param cache_subnet_group_name: ``AWS::ElastiCache::SubnetGroup.CacheSubnetGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "subnet_ids": subnet_ids,
        }
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name

    @builtins.property
    def description(self) -> builtins.str:
        """``AWS::ElastiCache::SubnetGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-description
        """
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return result

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        """``AWS::ElastiCache::SubnetGroup.SubnetIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-subnetids
        """
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return result

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::ElastiCache::SubnetGroup.CacheSubnetGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-cachesubnetgroupname
        """
        result = self._values.get("cache_subnet_group_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCacheCluster",
    "CfnCacheClusterProps",
    "CfnParameterGroup",
    "CfnParameterGroupProps",
    "CfnReplicationGroup",
    "CfnReplicationGroupProps",
    "CfnSecurityGroup",
    "CfnSecurityGroupIngress",
    "CfnSecurityGroupIngressProps",
    "CfnSecurityGroupProps",
    "CfnSubnetGroup",
    "CfnSubnetGroupProps",
]

publication.publish()
