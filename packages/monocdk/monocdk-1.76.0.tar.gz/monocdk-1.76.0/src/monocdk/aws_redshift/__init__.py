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
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    SecretValue as _SecretValue_c18506ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_ec2 import (
    Connections as _Connections_57ccbda9,
    IConnectable as _IConnectable_c1c0e72c,
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_iam import IRole as _IRole_59af6f50
from ..aws_kms import IKey as _IKey_36930160
from ..aws_s3 import IBucket as _IBucket_73486e29
from ..aws_secretsmanager import (
    ISecret as _ISecret_22fb8757,
    ISecretAttachmentTarget as _ISecretAttachmentTarget_b6932462,
    Secret as _Secret_cb33d4cc,
    SecretAttachmentTargetProps as _SecretAttachmentTargetProps_ab8522eb,
    SecretRotation as _SecretRotation_e64158ad,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnCluster(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_redshift.CfnCluster",
):
    """A CloudFormation ``AWS::Redshift::Cluster``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html
    :cloudformationResource: AWS::Redshift::Cluster
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        cluster_type: builtins.str,
        db_name: builtins.str,
        master_username: builtins.str,
        master_user_password: builtins.str,
        node_type: builtins.str,
        allow_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        automated_snapshot_retention_period: typing.Optional[jsii.Number] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        cluster_identifier: typing.Optional[builtins.str] = None,
        cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        cluster_security_groups: typing.Optional[typing.List[builtins.str]] = None,
        cluster_subnet_group_name: typing.Optional[builtins.str] = None,
        cluster_version: typing.Optional[builtins.str] = None,
        elastic_ip: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        hsm_client_certificate_identifier: typing.Optional[builtins.str] = None,
        hsm_configuration_identifier: typing.Optional[builtins.str] = None,
        iam_roles: typing.Optional[typing.List[builtins.str]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        logging_properties: typing.Optional[typing.Union["CfnCluster.LoggingPropertiesProperty", _IResolvable_a771d0ef]] = None,
        number_of_nodes: typing.Optional[jsii.Number] = None,
        owner_account: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        snapshot_cluster_identifier: typing.Optional[builtins.str] = None,
        snapshot_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Create a new ``AWS::Redshift::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster_type: ``AWS::Redshift::Cluster.ClusterType``.
        :param db_name: ``AWS::Redshift::Cluster.DBName``.
        :param master_username: ``AWS::Redshift::Cluster.MasterUsername``.
        :param master_user_password: ``AWS::Redshift::Cluster.MasterUserPassword``.
        :param node_type: ``AWS::Redshift::Cluster.NodeType``.
        :param allow_version_upgrade: ``AWS::Redshift::Cluster.AllowVersionUpgrade``.
        :param automated_snapshot_retention_period: ``AWS::Redshift::Cluster.AutomatedSnapshotRetentionPeriod``.
        :param availability_zone: ``AWS::Redshift::Cluster.AvailabilityZone``.
        :param cluster_identifier: ``AWS::Redshift::Cluster.ClusterIdentifier``.
        :param cluster_parameter_group_name: ``AWS::Redshift::Cluster.ClusterParameterGroupName``.
        :param cluster_security_groups: ``AWS::Redshift::Cluster.ClusterSecurityGroups``.
        :param cluster_subnet_group_name: ``AWS::Redshift::Cluster.ClusterSubnetGroupName``.
        :param cluster_version: ``AWS::Redshift::Cluster.ClusterVersion``.
        :param elastic_ip: ``AWS::Redshift::Cluster.ElasticIp``.
        :param encrypted: ``AWS::Redshift::Cluster.Encrypted``.
        :param hsm_client_certificate_identifier: ``AWS::Redshift::Cluster.HsmClientCertificateIdentifier``.
        :param hsm_configuration_identifier: ``AWS::Redshift::Cluster.HsmConfigurationIdentifier``.
        :param iam_roles: ``AWS::Redshift::Cluster.IamRoles``.
        :param kms_key_id: ``AWS::Redshift::Cluster.KmsKeyId``.
        :param logging_properties: ``AWS::Redshift::Cluster.LoggingProperties``.
        :param number_of_nodes: ``AWS::Redshift::Cluster.NumberOfNodes``.
        :param owner_account: ``AWS::Redshift::Cluster.OwnerAccount``.
        :param port: ``AWS::Redshift::Cluster.Port``.
        :param preferred_maintenance_window: ``AWS::Redshift::Cluster.PreferredMaintenanceWindow``.
        :param publicly_accessible: ``AWS::Redshift::Cluster.PubliclyAccessible``.
        :param snapshot_cluster_identifier: ``AWS::Redshift::Cluster.SnapshotClusterIdentifier``.
        :param snapshot_identifier: ``AWS::Redshift::Cluster.SnapshotIdentifier``.
        :param tags: ``AWS::Redshift::Cluster.Tags``.
        :param vpc_security_group_ids: ``AWS::Redshift::Cluster.VpcSecurityGroupIds``.
        """
        props = CfnClusterProps(
            cluster_type=cluster_type,
            db_name=db_name,
            master_username=master_username,
            master_user_password=master_user_password,
            node_type=node_type,
            allow_version_upgrade=allow_version_upgrade,
            automated_snapshot_retention_period=automated_snapshot_retention_period,
            availability_zone=availability_zone,
            cluster_identifier=cluster_identifier,
            cluster_parameter_group_name=cluster_parameter_group_name,
            cluster_security_groups=cluster_security_groups,
            cluster_subnet_group_name=cluster_subnet_group_name,
            cluster_version=cluster_version,
            elastic_ip=elastic_ip,
            encrypted=encrypted,
            hsm_client_certificate_identifier=hsm_client_certificate_identifier,
            hsm_configuration_identifier=hsm_configuration_identifier,
            iam_roles=iam_roles,
            kms_key_id=kms_key_id,
            logging_properties=logging_properties,
            number_of_nodes=number_of_nodes,
            owner_account=owner_account,
            port=port,
            preferred_maintenance_window=preferred_maintenance_window,
            publicly_accessible=publicly_accessible,
            snapshot_cluster_identifier=snapshot_cluster_identifier,
            snapshot_identifier=snapshot_identifier,
            tags=tags,
            vpc_security_group_ids=vpc_security_group_ids,
        )

        jsii.create(CfnCluster, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrEndpointAddress")
    def attr_endpoint_address(self) -> builtins.str:
        """
        :cloudformationAttribute: Endpoint.Address
        """
        return jsii.get(self, "attrEndpointAddress")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrEndpointPort")
    def attr_endpoint_port(self) -> builtins.str:
        """
        :cloudformationAttribute: Endpoint.Port
        """
        return jsii.get(self, "attrEndpointPort")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::Redshift::Cluster.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterType")
    def cluster_type(self) -> builtins.str:
        """``AWS::Redshift::Cluster.ClusterType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustertype
        """
        return jsii.get(self, "clusterType")

    @cluster_type.setter # type: ignore
    def cluster_type(self, value: builtins.str) -> None:
        jsii.set(self, "clusterType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dbName")
    def db_name(self) -> builtins.str:
        """``AWS::Redshift::Cluster.DBName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-dbname
        """
        return jsii.get(self, "dbName")

    @db_name.setter # type: ignore
    def db_name(self, value: builtins.str) -> None:
        jsii.set(self, "dbName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="masterUsername")
    def master_username(self) -> builtins.str:
        """``AWS::Redshift::Cluster.MasterUsername``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-masterusername
        """
        return jsii.get(self, "masterUsername")

    @master_username.setter # type: ignore
    def master_username(self, value: builtins.str) -> None:
        jsii.set(self, "masterUsername", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="masterUserPassword")
    def master_user_password(self) -> builtins.str:
        """``AWS::Redshift::Cluster.MasterUserPassword``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-masteruserpassword
        """
        return jsii.get(self, "masterUserPassword")

    @master_user_password.setter # type: ignore
    def master_user_password(self, value: builtins.str) -> None:
        jsii.set(self, "masterUserPassword", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        """``AWS::Redshift::Cluster.NodeType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-nodetype
        """
        return jsii.get(self, "nodeType")

    @node_type.setter # type: ignore
    def node_type(self, value: builtins.str) -> None:
        jsii.set(self, "nodeType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowVersionUpgrade")
    def allow_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::Redshift::Cluster.AllowVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-allowversionupgrade
        """
        return jsii.get(self, "allowVersionUpgrade")

    @allow_version_upgrade.setter # type: ignore
    def allow_version_upgrade(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "allowVersionUpgrade", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="automatedSnapshotRetentionPeriod")
    def automated_snapshot_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.AutomatedSnapshotRetentionPeriod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-automatedsnapshotretentionperiod
        """
        return jsii.get(self, "automatedSnapshotRetentionPeriod")

    @automated_snapshot_retention_period.setter # type: ignore
    def automated_snapshot_retention_period(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "automatedSnapshotRetentionPeriod", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.AvailabilityZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-availabilityzone
        """
        return jsii.get(self, "availabilityZone")

    @availability_zone.setter # type: ignore
    def availability_zone(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "availabilityZone", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.ClusterIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusteridentifier
        """
        return jsii.get(self, "clusterIdentifier")

    @cluster_identifier.setter # type: ignore
    def cluster_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clusterIdentifier", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.ClusterParameterGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusterparametergroupname
        """
        return jsii.get(self, "clusterParameterGroupName")

    @cluster_parameter_group_name.setter # type: ignore
    def cluster_parameter_group_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "clusterParameterGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterSecurityGroups")
    def cluster_security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Redshift::Cluster.ClusterSecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustersecuritygroups
        """
        return jsii.get(self, "clusterSecurityGroups")

    @cluster_security_groups.setter # type: ignore
    def cluster_security_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "clusterSecurityGroups", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterSubnetGroupName")
    def cluster_subnet_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.ClusterSubnetGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustersubnetgroupname
        """
        return jsii.get(self, "clusterSubnetGroupName")

    @cluster_subnet_group_name.setter # type: ignore
    def cluster_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clusterSubnetGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterVersion")
    def cluster_version(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.ClusterVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusterversion
        """
        return jsii.get(self, "clusterVersion")

    @cluster_version.setter # type: ignore
    def cluster_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clusterVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="elasticIp")
    def elastic_ip(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.ElasticIp``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-elasticip
        """
        return jsii.get(self, "elasticIp")

    @elastic_ip.setter # type: ignore
    def elastic_ip(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "elasticIp", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="encrypted")
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::Redshift::Cluster.Encrypted``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-encrypted
        """
        return jsii.get(self, "encrypted")

    @encrypted.setter # type: ignore
    def encrypted(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "encrypted", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="hsmClientCertificateIdentifier")
    def hsm_client_certificate_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.HsmClientCertificateIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-hsmclientcertidentifier
        """
        return jsii.get(self, "hsmClientCertificateIdentifier")

    @hsm_client_certificate_identifier.setter # type: ignore
    def hsm_client_certificate_identifier(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "hsmClientCertificateIdentifier", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="hsmConfigurationIdentifier")
    def hsm_configuration_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.HsmConfigurationIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-HsmConfigurationIdentifier
        """
        return jsii.get(self, "hsmConfigurationIdentifier")

    @hsm_configuration_identifier.setter # type: ignore
    def hsm_configuration_identifier(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "hsmConfigurationIdentifier", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="iamRoles")
    def iam_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Redshift::Cluster.IamRoles``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-iamroles
        """
        return jsii.get(self, "iamRoles")

    @iam_roles.setter # type: ignore
    def iam_roles(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "iamRoles", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter # type: ignore
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loggingProperties")
    def logging_properties(
        self,
    ) -> typing.Optional[typing.Union["CfnCluster.LoggingPropertiesProperty", _IResolvable_a771d0ef]]:
        """``AWS::Redshift::Cluster.LoggingProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-loggingproperties
        """
        return jsii.get(self, "loggingProperties")

    @logging_properties.setter # type: ignore
    def logging_properties(
        self,
        value: typing.Optional[typing.Union["CfnCluster.LoggingPropertiesProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "loggingProperties", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="numberOfNodes")
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.NumberOfNodes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-nodetype
        """
        return jsii.get(self, "numberOfNodes")

    @number_of_nodes.setter # type: ignore
    def number_of_nodes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "numberOfNodes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ownerAccount")
    def owner_account(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.OwnerAccount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-owneraccount
        """
        return jsii.get(self, "ownerAccount")

    @owner_account.setter # type: ignore
    def owner_account(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ownerAccount", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-port
        """
        return jsii.get(self, "port")

    @port.setter # type: ignore
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.PreferredMaintenanceWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter # type: ignore
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="publiclyAccessible")
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::Redshift::Cluster.PubliclyAccessible``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-publiclyaccessible
        """
        return jsii.get(self, "publiclyAccessible")

    @publicly_accessible.setter # type: ignore
    def publicly_accessible(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "publiclyAccessible", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshotClusterIdentifier")
    def snapshot_cluster_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.SnapshotClusterIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotclusteridentifier
        """
        return jsii.get(self, "snapshotClusterIdentifier")

    @snapshot_cluster_identifier.setter # type: ignore
    def snapshot_cluster_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "snapshotClusterIdentifier", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snapshotIdentifier")
    def snapshot_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.SnapshotIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotidentifier
        """
        return jsii.get(self, "snapshotIdentifier")

    @snapshot_identifier.setter # type: ignore
    def snapshot_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "snapshotIdentifier", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Redshift::Cluster.VpcSecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-vpcsecuritygroupids
        """
        return jsii.get(self, "vpcSecurityGroupIds")

    @vpc_security_group_ids.setter # type: ignore
    def vpc_security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "vpcSecurityGroupIds", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_redshift.CfnCluster.LoggingPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "s3_key_prefix": "s3KeyPrefix"},
    )
    class LoggingPropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            s3_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket_name: ``CfnCluster.LoggingPropertiesProperty.BucketName``.
            :param s3_key_prefix: ``CfnCluster.LoggingPropertiesProperty.S3KeyPrefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-loggingproperties.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_name": bucket_name,
            }
            if s3_key_prefix is not None:
                self._values["s3_key_prefix"] = s3_key_prefix

        @builtins.property
        def bucket_name(self) -> builtins.str:
            """``CfnCluster.LoggingPropertiesProperty.BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-loggingproperties.html#cfn-redshift-cluster-loggingproperties-bucketname
            """
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return result

        @builtins.property
        def s3_key_prefix(self) -> typing.Optional[builtins.str]:
            """``CfnCluster.LoggingPropertiesProperty.S3KeyPrefix``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-loggingproperties.html#cfn-redshift-cluster-loggingproperties-s3keyprefix
            """
            result = self._values.get("s3_key_prefix")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnClusterParameterGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_redshift.CfnClusterParameterGroup",
):
    """A CloudFormation ``AWS::Redshift::ClusterParameterGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html
    :cloudformationResource: AWS::Redshift::ClusterParameterGroup
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: builtins.str,
        parameter_group_family: builtins.str,
        parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnClusterParameterGroup.ParameterProperty", _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::Redshift::ClusterParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Redshift::ClusterParameterGroup.Description``.
        :param parameter_group_family: ``AWS::Redshift::ClusterParameterGroup.ParameterGroupFamily``.
        :param parameters: ``AWS::Redshift::ClusterParameterGroup.Parameters``.
        :param tags: ``AWS::Redshift::ClusterParameterGroup.Tags``.
        """
        props = CfnClusterParameterGroupProps(
            description=description,
            parameter_group_family=parameter_group_family,
            parameters=parameters,
            tags=tags,
        )

        jsii.create(CfnClusterParameterGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::Redshift::ClusterParameterGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        """``AWS::Redshift::ClusterParameterGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameterGroupFamily")
    def parameter_group_family(self) -> builtins.str:
        """``AWS::Redshift::ClusterParameterGroup.ParameterGroupFamily``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-parametergroupfamily
        """
        return jsii.get(self, "parameterGroupFamily")

    @parameter_group_family.setter # type: ignore
    def parameter_group_family(self, value: builtins.str) -> None:
        jsii.set(self, "parameterGroupFamily", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnClusterParameterGroup.ParameterProperty", _IResolvable_a771d0ef]]]]:
        """``AWS::Redshift::ClusterParameterGroup.Parameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter # type: ignore
    def parameters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnClusterParameterGroup.ParameterProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "parameters", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_redshift.CfnClusterParameterGroup.ParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class ParameterProperty:
        def __init__(
            self,
            *,
            parameter_name: builtins.str,
            parameter_value: builtins.str,
        ) -> None:
            """
            :param parameter_name: ``CfnClusterParameterGroup.ParameterProperty.ParameterName``.
            :param parameter_value: ``CfnClusterParameterGroup.ParameterProperty.ParameterValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-property-redshift-clusterparametergroup-parameter.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "parameter_name": parameter_name,
                "parameter_value": parameter_value,
            }

        @builtins.property
        def parameter_name(self) -> builtins.str:
            """``CfnClusterParameterGroup.ParameterProperty.ParameterName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-property-redshift-clusterparametergroup-parameter.html#cfn-redshift-clusterparametergroup-parameter-parametername
            """
            result = self._values.get("parameter_name")
            assert result is not None, "Required property 'parameter_name' is missing"
            return result

        @builtins.property
        def parameter_value(self) -> builtins.str:
            """``CfnClusterParameterGroup.ParameterProperty.ParameterValue``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-property-redshift-clusterparametergroup-parameter.html#cfn-redshift-clusterparametergroup-parameter-parametervalue
            """
            result = self._values.get("parameter_value")
            assert result is not None, "Required property 'parameter_value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.CfnClusterParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "parameter_group_family": "parameterGroupFamily",
        "parameters": "parameters",
        "tags": "tags",
    },
)
class CfnClusterParameterGroupProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        parameter_group_family: builtins.str,
        parameters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnClusterParameterGroup.ParameterProperty, _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Redshift::ClusterParameterGroup``.

        :param description: ``AWS::Redshift::ClusterParameterGroup.Description``.
        :param parameter_group_family: ``AWS::Redshift::ClusterParameterGroup.ParameterGroupFamily``.
        :param parameters: ``AWS::Redshift::ClusterParameterGroup.Parameters``.
        :param tags: ``AWS::Redshift::ClusterParameterGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "parameter_group_family": parameter_group_family,
        }
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        """``AWS::Redshift::ClusterParameterGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-description
        """
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return result

    @builtins.property
    def parameter_group_family(self) -> builtins.str:
        """``AWS::Redshift::ClusterParameterGroup.ParameterGroupFamily``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-parametergroupfamily
        """
        result = self._values.get("parameter_group_family")
        assert result is not None, "Required property 'parameter_group_family' is missing"
        return result

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnClusterParameterGroup.ParameterProperty, _IResolvable_a771d0ef]]]]:
        """``AWS::Redshift::ClusterParameterGroup.Parameters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-parameters
        """
        result = self._values.get("parameters")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::Redshift::ClusterParameterGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.CfnClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_type": "clusterType",
        "db_name": "dbName",
        "master_username": "masterUsername",
        "master_user_password": "masterUserPassword",
        "node_type": "nodeType",
        "allow_version_upgrade": "allowVersionUpgrade",
        "automated_snapshot_retention_period": "automatedSnapshotRetentionPeriod",
        "availability_zone": "availabilityZone",
        "cluster_identifier": "clusterIdentifier",
        "cluster_parameter_group_name": "clusterParameterGroupName",
        "cluster_security_groups": "clusterSecurityGroups",
        "cluster_subnet_group_name": "clusterSubnetGroupName",
        "cluster_version": "clusterVersion",
        "elastic_ip": "elasticIp",
        "encrypted": "encrypted",
        "hsm_client_certificate_identifier": "hsmClientCertificateIdentifier",
        "hsm_configuration_identifier": "hsmConfigurationIdentifier",
        "iam_roles": "iamRoles",
        "kms_key_id": "kmsKeyId",
        "logging_properties": "loggingProperties",
        "number_of_nodes": "numberOfNodes",
        "owner_account": "ownerAccount",
        "port": "port",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "publicly_accessible": "publiclyAccessible",
        "snapshot_cluster_identifier": "snapshotClusterIdentifier",
        "snapshot_identifier": "snapshotIdentifier",
        "tags": "tags",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnClusterProps:
    def __init__(
        self,
        *,
        cluster_type: builtins.str,
        db_name: builtins.str,
        master_username: builtins.str,
        master_user_password: builtins.str,
        node_type: builtins.str,
        allow_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        automated_snapshot_retention_period: typing.Optional[jsii.Number] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        cluster_identifier: typing.Optional[builtins.str] = None,
        cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        cluster_security_groups: typing.Optional[typing.List[builtins.str]] = None,
        cluster_subnet_group_name: typing.Optional[builtins.str] = None,
        cluster_version: typing.Optional[builtins.str] = None,
        elastic_ip: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        hsm_client_certificate_identifier: typing.Optional[builtins.str] = None,
        hsm_configuration_identifier: typing.Optional[builtins.str] = None,
        iam_roles: typing.Optional[typing.List[builtins.str]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        logging_properties: typing.Optional[typing.Union[CfnCluster.LoggingPropertiesProperty, _IResolvable_a771d0ef]] = None,
        number_of_nodes: typing.Optional[jsii.Number] = None,
        owner_account: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        snapshot_cluster_identifier: typing.Optional[builtins.str] = None,
        snapshot_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Redshift::Cluster``.

        :param cluster_type: ``AWS::Redshift::Cluster.ClusterType``.
        :param db_name: ``AWS::Redshift::Cluster.DBName``.
        :param master_username: ``AWS::Redshift::Cluster.MasterUsername``.
        :param master_user_password: ``AWS::Redshift::Cluster.MasterUserPassword``.
        :param node_type: ``AWS::Redshift::Cluster.NodeType``.
        :param allow_version_upgrade: ``AWS::Redshift::Cluster.AllowVersionUpgrade``.
        :param automated_snapshot_retention_period: ``AWS::Redshift::Cluster.AutomatedSnapshotRetentionPeriod``.
        :param availability_zone: ``AWS::Redshift::Cluster.AvailabilityZone``.
        :param cluster_identifier: ``AWS::Redshift::Cluster.ClusterIdentifier``.
        :param cluster_parameter_group_name: ``AWS::Redshift::Cluster.ClusterParameterGroupName``.
        :param cluster_security_groups: ``AWS::Redshift::Cluster.ClusterSecurityGroups``.
        :param cluster_subnet_group_name: ``AWS::Redshift::Cluster.ClusterSubnetGroupName``.
        :param cluster_version: ``AWS::Redshift::Cluster.ClusterVersion``.
        :param elastic_ip: ``AWS::Redshift::Cluster.ElasticIp``.
        :param encrypted: ``AWS::Redshift::Cluster.Encrypted``.
        :param hsm_client_certificate_identifier: ``AWS::Redshift::Cluster.HsmClientCertificateIdentifier``.
        :param hsm_configuration_identifier: ``AWS::Redshift::Cluster.HsmConfigurationIdentifier``.
        :param iam_roles: ``AWS::Redshift::Cluster.IamRoles``.
        :param kms_key_id: ``AWS::Redshift::Cluster.KmsKeyId``.
        :param logging_properties: ``AWS::Redshift::Cluster.LoggingProperties``.
        :param number_of_nodes: ``AWS::Redshift::Cluster.NumberOfNodes``.
        :param owner_account: ``AWS::Redshift::Cluster.OwnerAccount``.
        :param port: ``AWS::Redshift::Cluster.Port``.
        :param preferred_maintenance_window: ``AWS::Redshift::Cluster.PreferredMaintenanceWindow``.
        :param publicly_accessible: ``AWS::Redshift::Cluster.PubliclyAccessible``.
        :param snapshot_cluster_identifier: ``AWS::Redshift::Cluster.SnapshotClusterIdentifier``.
        :param snapshot_identifier: ``AWS::Redshift::Cluster.SnapshotIdentifier``.
        :param tags: ``AWS::Redshift::Cluster.Tags``.
        :param vpc_security_group_ids: ``AWS::Redshift::Cluster.VpcSecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_type": cluster_type,
            "db_name": db_name,
            "master_username": master_username,
            "master_user_password": master_user_password,
            "node_type": node_type,
        }
        if allow_version_upgrade is not None:
            self._values["allow_version_upgrade"] = allow_version_upgrade
        if automated_snapshot_retention_period is not None:
            self._values["automated_snapshot_retention_period"] = automated_snapshot_retention_period
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if cluster_identifier is not None:
            self._values["cluster_identifier"] = cluster_identifier
        if cluster_parameter_group_name is not None:
            self._values["cluster_parameter_group_name"] = cluster_parameter_group_name
        if cluster_security_groups is not None:
            self._values["cluster_security_groups"] = cluster_security_groups
        if cluster_subnet_group_name is not None:
            self._values["cluster_subnet_group_name"] = cluster_subnet_group_name
        if cluster_version is not None:
            self._values["cluster_version"] = cluster_version
        if elastic_ip is not None:
            self._values["elastic_ip"] = elastic_ip
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if hsm_client_certificate_identifier is not None:
            self._values["hsm_client_certificate_identifier"] = hsm_client_certificate_identifier
        if hsm_configuration_identifier is not None:
            self._values["hsm_configuration_identifier"] = hsm_configuration_identifier
        if iam_roles is not None:
            self._values["iam_roles"] = iam_roles
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if logging_properties is not None:
            self._values["logging_properties"] = logging_properties
        if number_of_nodes is not None:
            self._values["number_of_nodes"] = number_of_nodes
        if owner_account is not None:
            self._values["owner_account"] = owner_account
        if port is not None:
            self._values["port"] = port
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if snapshot_cluster_identifier is not None:
            self._values["snapshot_cluster_identifier"] = snapshot_cluster_identifier
        if snapshot_identifier is not None:
            self._values["snapshot_identifier"] = snapshot_identifier
        if tags is not None:
            self._values["tags"] = tags
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def cluster_type(self) -> builtins.str:
        """``AWS::Redshift::Cluster.ClusterType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustertype
        """
        result = self._values.get("cluster_type")
        assert result is not None, "Required property 'cluster_type' is missing"
        return result

    @builtins.property
    def db_name(self) -> builtins.str:
        """``AWS::Redshift::Cluster.DBName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-dbname
        """
        result = self._values.get("db_name")
        assert result is not None, "Required property 'db_name' is missing"
        return result

    @builtins.property
    def master_username(self) -> builtins.str:
        """``AWS::Redshift::Cluster.MasterUsername``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-masterusername
        """
        result = self._values.get("master_username")
        assert result is not None, "Required property 'master_username' is missing"
        return result

    @builtins.property
    def master_user_password(self) -> builtins.str:
        """``AWS::Redshift::Cluster.MasterUserPassword``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-masteruserpassword
        """
        result = self._values.get("master_user_password")
        assert result is not None, "Required property 'master_user_password' is missing"
        return result

    @builtins.property
    def node_type(self) -> builtins.str:
        """``AWS::Redshift::Cluster.NodeType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-nodetype
        """
        result = self._values.get("node_type")
        assert result is not None, "Required property 'node_type' is missing"
        return result

    @builtins.property
    def allow_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::Redshift::Cluster.AllowVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-allowversionupgrade
        """
        result = self._values.get("allow_version_upgrade")
        return result

    @builtins.property
    def automated_snapshot_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.AutomatedSnapshotRetentionPeriod``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-automatedsnapshotretentionperiod
        """
        result = self._values.get("automated_snapshot_retention_period")
        return result

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.AvailabilityZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-availabilityzone
        """
        result = self._values.get("availability_zone")
        return result

    @builtins.property
    def cluster_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.ClusterIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusteridentifier
        """
        result = self._values.get("cluster_identifier")
        return result

    @builtins.property
    def cluster_parameter_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.ClusterParameterGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusterparametergroupname
        """
        result = self._values.get("cluster_parameter_group_name")
        return result

    @builtins.property
    def cluster_security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Redshift::Cluster.ClusterSecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustersecuritygroups
        """
        result = self._values.get("cluster_security_groups")
        return result

    @builtins.property
    def cluster_subnet_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.ClusterSubnetGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustersubnetgroupname
        """
        result = self._values.get("cluster_subnet_group_name")
        return result

    @builtins.property
    def cluster_version(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.ClusterVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusterversion
        """
        result = self._values.get("cluster_version")
        return result

    @builtins.property
    def elastic_ip(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.ElasticIp``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-elasticip
        """
        result = self._values.get("elastic_ip")
        return result

    @builtins.property
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::Redshift::Cluster.Encrypted``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-encrypted
        """
        result = self._values.get("encrypted")
        return result

    @builtins.property
    def hsm_client_certificate_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.HsmClientCertificateIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-hsmclientcertidentifier
        """
        result = self._values.get("hsm_client_certificate_identifier")
        return result

    @builtins.property
    def hsm_configuration_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.HsmConfigurationIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-HsmConfigurationIdentifier
        """
        result = self._values.get("hsm_configuration_identifier")
        return result

    @builtins.property
    def iam_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Redshift::Cluster.IamRoles``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-iamroles
        """
        result = self._values.get("iam_roles")
        return result

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-kmskeyid
        """
        result = self._values.get("kms_key_id")
        return result

    @builtins.property
    def logging_properties(
        self,
    ) -> typing.Optional[typing.Union[CfnCluster.LoggingPropertiesProperty, _IResolvable_a771d0ef]]:
        """``AWS::Redshift::Cluster.LoggingProperties``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-loggingproperties
        """
        result = self._values.get("logging_properties")
        return result

    @builtins.property
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.NumberOfNodes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-nodetype
        """
        result = self._values.get("number_of_nodes")
        return result

    @builtins.property
    def owner_account(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.OwnerAccount``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-owneraccount
        """
        result = self._values.get("owner_account")
        return result

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-port
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.PreferredMaintenanceWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-preferredmaintenancewindow
        """
        result = self._values.get("preferred_maintenance_window")
        return result

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        """``AWS::Redshift::Cluster.PubliclyAccessible``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-publiclyaccessible
        """
        result = self._values.get("publicly_accessible")
        return result

    @builtins.property
    def snapshot_cluster_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.SnapshotClusterIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotclusteridentifier
        """
        result = self._values.get("snapshot_cluster_identifier")
        return result

    @builtins.property
    def snapshot_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::Cluster.SnapshotIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotidentifier
        """
        result = self._values.get("snapshot_identifier")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::Redshift::Cluster.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::Redshift::Cluster.VpcSecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-vpcsecuritygroupids
        """
        result = self._values.get("vpc_security_group_ids")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnClusterSecurityGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_redshift.CfnClusterSecurityGroup",
):
    """A CloudFormation ``AWS::Redshift::ClusterSecurityGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html
    :cloudformationResource: AWS::Redshift::ClusterSecurityGroup
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: builtins.str,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::Redshift::ClusterSecurityGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Redshift::ClusterSecurityGroup.Description``.
        :param tags: ``AWS::Redshift::ClusterSecurityGroup.Tags``.
        """
        props = CfnClusterSecurityGroupProps(description=description, tags=tags)

        jsii.create(CfnClusterSecurityGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::Redshift::ClusterSecurityGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html#cfn-redshift-clustersecuritygroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        """``AWS::Redshift::ClusterSecurityGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html#cfn-redshift-clustersecuritygroup-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnClusterSecurityGroupIngress(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_redshift.CfnClusterSecurityGroupIngress",
):
    """A CloudFormation ``AWS::Redshift::ClusterSecurityGroupIngress``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html
    :cloudformationResource: AWS::Redshift::ClusterSecurityGroupIngress
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        cluster_security_group_name: builtins.str,
        cidrip: typing.Optional[builtins.str] = None,
        ec2_security_group_name: typing.Optional[builtins.str] = None,
        ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::Redshift::ClusterSecurityGroupIngress``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster_security_group_name: ``AWS::Redshift::ClusterSecurityGroupIngress.ClusterSecurityGroupName``.
        :param cidrip: ``AWS::Redshift::ClusterSecurityGroupIngress.CIDRIP``.
        :param ec2_security_group_name: ``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupName``.
        :param ec2_security_group_owner_id: ``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupOwnerId``.
        """
        props = CfnClusterSecurityGroupIngressProps(
            cluster_security_group_name=cluster_security_group_name,
            cidrip=cidrip,
            ec2_security_group_name=ec2_security_group_name,
            ec2_security_group_owner_id=ec2_security_group_owner_id,
        )

        jsii.create(CfnClusterSecurityGroupIngress, self, [scope, id, props])

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
    @jsii.member(jsii_name="clusterSecurityGroupName")
    def cluster_security_group_name(self) -> builtins.str:
        """``AWS::Redshift::ClusterSecurityGroupIngress.ClusterSecurityGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-clustersecuritygroupname
        """
        return jsii.get(self, "clusterSecurityGroupName")

    @cluster_security_group_name.setter # type: ignore
    def cluster_security_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "clusterSecurityGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cidrip")
    def cidrip(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.CIDRIP``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-cidrip
        """
        return jsii.get(self, "cidrip")

    @cidrip.setter # type: ignore
    def cidrip(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cidrip", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ec2SecurityGroupName")
    def ec2_security_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-ec2securitygroupname
        """
        return jsii.get(self, "ec2SecurityGroupName")

    @ec2_security_group_name.setter # type: ignore
    def ec2_security_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ec2SecurityGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ec2SecurityGroupOwnerId")
    def ec2_security_group_owner_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupOwnerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-ec2securitygroupownerid
        """
        return jsii.get(self, "ec2SecurityGroupOwnerId")

    @ec2_security_group_owner_id.setter # type: ignore
    def ec2_security_group_owner_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ec2SecurityGroupOwnerId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.CfnClusterSecurityGroupIngressProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_security_group_name": "clusterSecurityGroupName",
        "cidrip": "cidrip",
        "ec2_security_group_name": "ec2SecurityGroupName",
        "ec2_security_group_owner_id": "ec2SecurityGroupOwnerId",
    },
)
class CfnClusterSecurityGroupIngressProps:
    def __init__(
        self,
        *,
        cluster_security_group_name: builtins.str,
        cidrip: typing.Optional[builtins.str] = None,
        ec2_security_group_name: typing.Optional[builtins.str] = None,
        ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::Redshift::ClusterSecurityGroupIngress``.

        :param cluster_security_group_name: ``AWS::Redshift::ClusterSecurityGroupIngress.ClusterSecurityGroupName``.
        :param cidrip: ``AWS::Redshift::ClusterSecurityGroupIngress.CIDRIP``.
        :param ec2_security_group_name: ``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupName``.
        :param ec2_security_group_owner_id: ``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupOwnerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_security_group_name": cluster_security_group_name,
        }
        if cidrip is not None:
            self._values["cidrip"] = cidrip
        if ec2_security_group_name is not None:
            self._values["ec2_security_group_name"] = ec2_security_group_name
        if ec2_security_group_owner_id is not None:
            self._values["ec2_security_group_owner_id"] = ec2_security_group_owner_id

    @builtins.property
    def cluster_security_group_name(self) -> builtins.str:
        """``AWS::Redshift::ClusterSecurityGroupIngress.ClusterSecurityGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-clustersecuritygroupname
        """
        result = self._values.get("cluster_security_group_name")
        assert result is not None, "Required property 'cluster_security_group_name' is missing"
        return result

    @builtins.property
    def cidrip(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.CIDRIP``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-cidrip
        """
        result = self._values.get("cidrip")
        return result

    @builtins.property
    def ec2_security_group_name(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-ec2securitygroupname
        """
        result = self._values.get("ec2_security_group_name")
        return result

    @builtins.property
    def ec2_security_group_owner_id(self) -> typing.Optional[builtins.str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupOwnerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-ec2securitygroupownerid
        """
        result = self._values.get("ec2_security_group_owner_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterSecurityGroupIngressProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.CfnClusterSecurityGroupProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "tags": "tags"},
)
class CfnClusterSecurityGroupProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Redshift::ClusterSecurityGroup``.

        :param description: ``AWS::Redshift::ClusterSecurityGroup.Description``.
        :param tags: ``AWS::Redshift::ClusterSecurityGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        """``AWS::Redshift::ClusterSecurityGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html#cfn-redshift-clustersecuritygroup-description
        """
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::Redshift::ClusterSecurityGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html#cfn-redshift-clustersecuritygroup-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterSecurityGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnClusterSubnetGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_redshift.CfnClusterSubnetGroup",
):
    """A CloudFormation ``AWS::Redshift::ClusterSubnetGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html
    :cloudformationResource: AWS::Redshift::ClusterSubnetGroup
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: builtins.str,
        subnet_ids: typing.List[builtins.str],
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Create a new ``AWS::Redshift::ClusterSubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Redshift::ClusterSubnetGroup.Description``.
        :param subnet_ids: ``AWS::Redshift::ClusterSubnetGroup.SubnetIds``.
        :param tags: ``AWS::Redshift::ClusterSubnetGroup.Tags``.
        """
        props = CfnClusterSubnetGroupProps(
            description=description, subnet_ids=subnet_ids, tags=tags
        )

        jsii.create(CfnClusterSubnetGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        """``AWS::Redshift::ClusterSubnetGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        """``AWS::Redshift::ClusterSubnetGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        """``AWS::Redshift::ClusterSubnetGroup.SubnetIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter # type: ignore
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "subnetIds", value)


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.CfnClusterSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnClusterSubnetGroupProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        subnet_ids: typing.List[builtins.str],
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Redshift::ClusterSubnetGroup``.

        :param description: ``AWS::Redshift::ClusterSubnetGroup.Description``.
        :param subnet_ids: ``AWS::Redshift::ClusterSubnetGroup.SubnetIds``.
        :param tags: ``AWS::Redshift::ClusterSubnetGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "subnet_ids": subnet_ids,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        """``AWS::Redshift::ClusterSubnetGroup.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-description
        """
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return result

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        """``AWS::Redshift::ClusterSubnetGroup.SubnetIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-subnetids
        """
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        """``AWS::Redshift::ClusterSubnetGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.ClusterAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_endpoint_address": "clusterEndpointAddress",
        "cluster_endpoint_port": "clusterEndpointPort",
        "cluster_name": "clusterName",
        "security_groups": "securityGroups",
    },
)
class ClusterAttributes:
    def __init__(
        self,
        *,
        cluster_endpoint_address: builtins.str,
        cluster_endpoint_port: jsii.Number,
        cluster_name: builtins.str,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
    ) -> None:
        """(experimental) Properties that describe an existing cluster instance.

        :param cluster_endpoint_address: (experimental) Cluster endpoint address.
        :param cluster_endpoint_port: (experimental) Cluster endpoint port.
        :param cluster_name: (experimental) Identifier for the cluster.
        :param security_groups: (experimental) The security groups of the redshift cluster. Default: no security groups will be attached to the import

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_endpoint_address": cluster_endpoint_address,
            "cluster_endpoint_port": cluster_endpoint_port,
            "cluster_name": cluster_name,
        }
        if security_groups is not None:
            self._values["security_groups"] = security_groups

    @builtins.property
    def cluster_endpoint_address(self) -> builtins.str:
        """(experimental) Cluster endpoint address.

        :stability: experimental
        """
        result = self._values.get("cluster_endpoint_address")
        assert result is not None, "Required property 'cluster_endpoint_address' is missing"
        return result

    @builtins.property
    def cluster_endpoint_port(self) -> jsii.Number:
        """(experimental) Cluster endpoint port.

        :stability: experimental
        """
        result = self._values.get("cluster_endpoint_port")
        assert result is not None, "Required property 'cluster_endpoint_port' is missing"
        return result

    @builtins.property
    def cluster_name(self) -> builtins.str:
        """(experimental) Identifier for the cluster.

        :stability: experimental
        """
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return result

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        """(experimental) The security groups of the redshift cluster.

        :default: no security groups will be attached to the import

        :stability: experimental
        """
        result = self._values.get("security_groups")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.ClusterParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters", "description": "description"},
)
class ClusterParameterGroupProps:
    def __init__(
        self,
        *,
        parameters: typing.Mapping[builtins.str, builtins.str],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Properties for a parameter group.

        :param parameters: (experimental) The parameters in this parameter group.
        :param description: (experimental) Description for this parameter group. Default: a CDK generated description

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "parameters": parameters,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        """(experimental) The parameters in this parameter group.

        :stability: experimental
        """
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """(experimental) Description for this parameter group.

        :default: a CDK generated description

        :stability: experimental
        """
        result = self._values.get("description")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.ClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "master_user": "masterUser",
        "vpc": "vpc",
        "cluster_name": "clusterName",
        "cluster_type": "clusterType",
        "default_database_name": "defaultDatabaseName",
        "encrypted": "encrypted",
        "encryption_key": "encryptionKey",
        "logging_bucket": "loggingBucket",
        "logging_key_prefix": "loggingKeyPrefix",
        "node_type": "nodeType",
        "number_of_nodes": "numberOfNodes",
        "parameter_group": "parameterGroup",
        "port": "port",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "publicly_accessible": "publiclyAccessible",
        "removal_policy": "removalPolicy",
        "roles": "roles",
        "security_groups": "securityGroups",
        "subnet_group": "subnetGroup",
        "vpc_subnets": "vpcSubnets",
    },
)
class ClusterProps:
    def __init__(
        self,
        *,
        master_user: "Login",
        vpc: _IVpc_6d1f76c4,
        cluster_name: typing.Optional[builtins.str] = None,
        cluster_type: typing.Optional["ClusterType"] = None,
        default_database_name: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        logging_bucket: typing.Optional[_IBucket_73486e29] = None,
        logging_key_prefix: typing.Optional[builtins.str] = None,
        node_type: typing.Optional["NodeType"] = None,
        number_of_nodes: typing.Optional[jsii.Number] = None,
        parameter_group: typing.Optional["IClusterParameterGroup"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        roles: typing.Optional[typing.List[_IRole_59af6f50]] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        subnet_group: typing.Optional["IClusterSubnetGroup"] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        """(experimental) Properties for a new database cluster.

        :param master_user: (experimental) Username and password for the administrative user.
        :param vpc: (experimental) The VPC to place the cluster in.
        :param cluster_name: (experimental) An optional identifier for the cluster. Default: - A name is automatically generated.
        :param cluster_type: (experimental) Settings for the individual instances that are launched. Default: {@link ClusterType.MULTI_NODE}
        :param default_database_name: (experimental) Name of a database which is automatically created inside the cluster. Default: - default_db
        :param encrypted: (experimental) Whether to enable encryption of data at rest in the cluster. Default: true
        :param encryption_key: (experimental) The KMS key to use for encryption of data at rest. Default: - AWS-managed key, if encryption at rest is enabled
        :param logging_bucket: (experimental) Bucket to send logs to. Logging information includes queries and connection attempts, for the specified Amazon Redshift cluster. Default: - No Logs
        :param logging_key_prefix: (experimental) Prefix used for logging. Default: - no prefix
        :param node_type: (experimental) The node type to be provisioned for the cluster. Default: {@link NodeType.DC2_LARGE}
        :param number_of_nodes: (experimental) Number of compute nodes in the cluster. Only specify this property for multi-node clusters. Value must be at least 2 and no more than 100. Default: - 2 if ``clusterType`` is ClusterType.MULTI_NODE, undefined otherwise
        :param parameter_group: (experimental) Additional parameters to pass to the database engine https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html. Default: - No parameter group.
        :param port: (experimental) What port to listen on. Default: - The default for the engine is used.
        :param preferred_maintenance_window: (experimental) A preferred maintenance window day/time range. Should be specified as a range ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). Example: 'Sun:23:45-Mon:00:15' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param publicly_accessible: (experimental) Whether to make cluster publicly accessible. Default: false
        :param removal_policy: (experimental) The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update. Default: RemovalPolicy.RETAIN
        :param roles: (experimental) A list of AWS Identity and Access Management (IAM) role that can be used by the cluster to access other AWS services. Specify a maximum of 10 roles. Default: - No role is attached to the cluster.
        :param security_groups: (experimental) Security group. Default: - a new security group is created.
        :param subnet_group: (experimental) A cluster subnet group to use with this cluster. Default: - a new subnet group will be created.
        :param vpc_subnets: (experimental) Where to place the instances within the VPC. Default: - private subnets

        :stability: experimental
        """
        if isinstance(master_user, dict):
            master_user = Login(**master_user)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "master_user": master_user,
            "vpc": vpc,
        }
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if cluster_type is not None:
            self._values["cluster_type"] = cluster_type
        if default_database_name is not None:
            self._values["default_database_name"] = default_database_name
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if logging_bucket is not None:
            self._values["logging_bucket"] = logging_bucket
        if logging_key_prefix is not None:
            self._values["logging_key_prefix"] = logging_key_prefix
        if node_type is not None:
            self._values["node_type"] = node_type
        if number_of_nodes is not None:
            self._values["number_of_nodes"] = number_of_nodes
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if port is not None:
            self._values["port"] = port
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if roles is not None:
            self._values["roles"] = roles
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_group is not None:
            self._values["subnet_group"] = subnet_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def master_user(self) -> "Login":
        """(experimental) Username and password for the administrative user.

        :stability: experimental
        """
        result = self._values.get("master_user")
        assert result is not None, "Required property 'master_user' is missing"
        return result

    @builtins.property
    def vpc(self) -> _IVpc_6d1f76c4:
        """(experimental) The VPC to place the cluster in.

        :stability: experimental
        """
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        """(experimental) An optional identifier for the cluster.

        :default: - A name is automatically generated.

        :stability: experimental
        """
        result = self._values.get("cluster_name")
        return result

    @builtins.property
    def cluster_type(self) -> typing.Optional["ClusterType"]:
        """(experimental) Settings for the individual instances that are launched.

        :default: {@link ClusterType.MULTI_NODE}

        :stability: experimental
        """
        result = self._values.get("cluster_type")
        return result

    @builtins.property
    def default_database_name(self) -> typing.Optional[builtins.str]:
        """(experimental) Name of a database which is automatically created inside the cluster.

        :default: - default_db

        :stability: experimental
        """
        result = self._values.get("default_database_name")
        return result

    @builtins.property
    def encrypted(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether to enable encryption of data at rest in the cluster.

        :default: true

        :stability: experimental
        """
        result = self._values.get("encrypted")
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        """(experimental) The KMS key to use for encryption of data at rest.

        :default: - AWS-managed key, if encryption at rest is enabled

        :stability: experimental
        """
        result = self._values.get("encryption_key")
        return result

    @builtins.property
    def logging_bucket(self) -> typing.Optional[_IBucket_73486e29]:
        """(experimental) Bucket to send logs to.

        Logging information includes queries and connection attempts, for the specified Amazon Redshift cluster.

        :default: - No Logs

        :stability: experimental
        """
        result = self._values.get("logging_bucket")
        return result

    @builtins.property
    def logging_key_prefix(self) -> typing.Optional[builtins.str]:
        """(experimental) Prefix used for logging.

        :default: - no prefix

        :stability: experimental
        """
        result = self._values.get("logging_key_prefix")
        return result

    @builtins.property
    def node_type(self) -> typing.Optional["NodeType"]:
        """(experimental) The node type to be provisioned for the cluster.

        :default: {@link NodeType.DC2_LARGE}

        :stability: experimental
        """
        result = self._values.get("node_type")
        return result

    @builtins.property
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        """(experimental) Number of compute nodes in the cluster. Only specify this property for multi-node clusters.

        Value must be at least 2 and no more than 100.

        :default: - 2 if ``clusterType`` is ClusterType.MULTI_NODE, undefined otherwise

        :stability: experimental
        """
        result = self._values.get("number_of_nodes")
        return result

    @builtins.property
    def parameter_group(self) -> typing.Optional["IClusterParameterGroup"]:
        """(experimental) Additional parameters to pass to the database engine https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html.

        :default: - No parameter group.

        :stability: experimental
        """
        result = self._values.get("parameter_group")
        return result

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """(experimental) What port to listen on.

        :default: - The default for the engine is used.

        :stability: experimental
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        """(experimental) A preferred maintenance window day/time range. Should be specified as a range ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC).

        Example: 'Sun:23:45-Mon:00:15'

        :default:

        - 30-minute window selected at random from an 8-hour block of time for
        each AWS Region, occurring on a random day of the week.

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :stability: experimental
        """
        result = self._values.get("preferred_maintenance_window")
        return result

    @builtins.property
    def publicly_accessible(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether to make cluster publicly accessible.

        :default: false

        :stability: experimental
        """
        result = self._values.get("publicly_accessible")
        return result

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        """(experimental) The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        """
        result = self._values.get("removal_policy")
        return result

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[_IRole_59af6f50]]:
        """(experimental) A list of AWS Identity and Access Management (IAM) role that can be used by the cluster to access other AWS services.

        Specify a maximum of 10 roles.

        :default: - No role is attached to the cluster.

        :stability: experimental
        """
        result = self._values.get("roles")
        return result

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        """(experimental) Security group.

        :default: - a new security group is created.

        :stability: experimental
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def subnet_group(self) -> typing.Optional["IClusterSubnetGroup"]:
        """(experimental) A cluster subnet group to use with this cluster.

        :default: - a new subnet group will be created.

        :stability: experimental
        """
        result = self._values.get("subnet_group")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        """(experimental) Where to place the instances within the VPC.

        :default: - private subnets

        :stability: experimental
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.ClusterSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "vpc": "vpc",
        "removal_policy": "removalPolicy",
        "vpc_subnets": "vpcSubnets",
    },
)
class ClusterSubnetGroupProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        vpc: _IVpc_6d1f76c4,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        """(experimental) Properties for creating a ClusterSubnetGroup.

        :param description: (experimental) Description of the subnet group.
        :param vpc: (experimental) The VPC to place the subnet group in.
        :param removal_policy: (experimental) The removal policy to apply when the subnet group are removed from the stack or replaced during an update. Default: RemovalPolicy.RETAIN
        :param vpc_subnets: (experimental) Which subnets within the VPC to associate with this group. Default: - private subnets

        :stability: experimental
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "vpc": vpc,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def description(self) -> builtins.str:
        """(experimental) Description of the subnet group.

        :stability: experimental
        """
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return result

    @builtins.property
    def vpc(self) -> _IVpc_6d1f76c4:
        """(experimental) The VPC to place the subnet group in.

        :stability: experimental
        """
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        """(experimental) The removal policy to apply when the subnet group are removed from the stack or replaced during an update.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        """
        result = self._values.get("removal_policy")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        """(experimental) Which subnets within the VPC to associate with this group.

        :default: - private subnets

        :stability: experimental
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_redshift.ClusterType")
class ClusterType(enum.Enum):
    """(experimental) What cluster type to use.

    Used by {@link ClusterProps.clusterType}

    :stability: experimental
    """

    SINGLE_NODE = "SINGLE_NODE"
    """(experimental) single-node cluster, the {@link ClusterProps.numberOfNodes} parameter is not required.

    :stability: experimental
    """
    MULTI_NODE = "MULTI_NODE"
    """(experimental) multi-node cluster, set the amount of nodes using {@link ClusterProps.numberOfNodes} parameter.

    :stability: experimental
    """


class DatabaseSecret(
    _Secret_cb33d4cc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_redshift.DatabaseSecret",
):
    """(experimental) A database secret.

    :stability: experimental
    :resource: AWS::SecretsManager::Secret
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        username: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param username: (experimental) The username.
        :param encryption_key: (experimental) The KMS key to use to encrypt the secret. Default: default master key

        :stability: experimental
        """
        props = DatabaseSecretProps(username=username, encryption_key=encryption_key)

        jsii.create(DatabaseSecret, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.DatabaseSecretProps",
    jsii_struct_bases=[],
    name_mapping={"username": "username", "encryption_key": "encryptionKey"},
)
class DatabaseSecretProps:
    def __init__(
        self,
        *,
        username: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
    ) -> None:
        """(experimental) Construction properties for a DatabaseSecret.

        :param username: (experimental) The username.
        :param encryption_key: (experimental) The KMS key to use to encrypt the secret. Default: default master key

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "username": username,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def username(self) -> builtins.str:
        """(experimental) The username.

        :stability: experimental
        """
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        """(experimental) The KMS key to use to encrypt the secret.

        :default: default master key

        :stability: experimental
        """
        result = self._values.get("encryption_key")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Endpoint(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_redshift.Endpoint"):
    """(experimental) Connection endpoint of a redshift cluster.

    Consists of a combination of hostname and port.

    :stability: experimental
    """

    def __init__(self, address: builtins.str, port: jsii.Number) -> None:
        """
        :param address: -
        :param port: -

        :stability: experimental
        """
        jsii.create(Endpoint, self, [address, port])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        """(experimental) The hostname of the endpoint.

        :stability: experimental
        """
        return jsii.get(self, "hostname")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        """(experimental) The port of the endpoint.

        :stability: experimental
        """
        return jsii.get(self, "port")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="socketAddress")
    def socket_address(self) -> builtins.str:
        """(experimental) The combination of "HOSTNAME:PORT" for this endpoint.

        :stability: experimental
        """
        return jsii.get(self, "socketAddress")


@jsii.interface(jsii_type="monocdk.aws_redshift.ICluster")
class ICluster(
    _IResource_8c1dbbbd,
    _IConnectable_c1c0e72c,
    _ISecretAttachmentTarget_b6932462,
    typing_extensions.Protocol,
):
    """(experimental) Create a Redshift Cluster with a given number of nodes.

    Implemented by {@link Cluster} via {@link ClusterBase}.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IClusterProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> Endpoint:
        """(experimental) The endpoint to use for read/write operations.

        :stability: experimental
        :attribute: EndpointAddress,EndpointPort
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        """(experimental) Name of the cluster.

        :stability: experimental
        :attribute: ClusterName
        """
        ...


class _IClusterProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore
    jsii.proxy_for(_IConnectable_c1c0e72c), # type: ignore
    jsii.proxy_for(_ISecretAttachmentTarget_b6932462), # type: ignore
):
    """(experimental) Create a Redshift Cluster with a given number of nodes.

    Implemented by {@link Cluster} via {@link ClusterBase}.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_redshift.ICluster"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> Endpoint:
        """(experimental) The endpoint to use for read/write operations.

        :stability: experimental
        :attribute: EndpointAddress,EndpointPort
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        """(experimental) Name of the cluster.

        :stability: experimental
        :attribute: ClusterName
        """
        return jsii.get(self, "clusterName")


@jsii.interface(jsii_type="monocdk.aws_redshift.IClusterParameterGroup")
class IClusterParameterGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    """(experimental) A parameter group.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IClusterParameterGroupProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> builtins.str:
        """(experimental) The name of this parameter group.

        :stability: experimental
        :attribute: true
        """
        ...


class _IClusterParameterGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore
):
    """(experimental) A parameter group.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_redshift.IClusterParameterGroup"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> builtins.str:
        """(experimental) The name of this parameter group.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "clusterParameterGroupName")


@jsii.interface(jsii_type="monocdk.aws_redshift.IClusterSubnetGroup")
class IClusterSubnetGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    """(experimental) Interface for a cluster subnet group.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IClusterSubnetGroupProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterSubnetGroupName")
    def cluster_subnet_group_name(self) -> builtins.str:
        """(experimental) The name of the cluster subnet group.

        :stability: experimental
        :attribute: true
        """
        ...


class _IClusterSubnetGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore
):
    """(experimental) Interface for a cluster subnet group.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_redshift.IClusterSubnetGroup"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterSubnetGroupName")
    def cluster_subnet_group_name(self) -> builtins.str:
        """(experimental) The name of the cluster subnet group.

        :stability: experimental
        :attribute: true
        """
        return jsii.get(self, "clusterSubnetGroupName")


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.Login",
    jsii_struct_bases=[],
    name_mapping={
        "master_username": "masterUsername",
        "encryption_key": "encryptionKey",
        "master_password": "masterPassword",
    },
)
class Login:
    def __init__(
        self,
        *,
        master_username: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        master_password: typing.Optional[_SecretValue_c18506ef] = None,
    ) -> None:
        """(experimental) Username and password combination.

        :param master_username: (experimental) Username.
        :param encryption_key: (experimental) KMS encryption key to encrypt the generated secret. Default: default master key
        :param master_password: (experimental) Password. Do not put passwords in your CDK code directly. Default: a Secrets Manager generated password

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "master_username": master_username,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if master_password is not None:
            self._values["master_password"] = master_password

    @builtins.property
    def master_username(self) -> builtins.str:
        """(experimental) Username.

        :stability: experimental
        """
        result = self._values.get("master_username")
        assert result is not None, "Required property 'master_username' is missing"
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        """(experimental) KMS encryption key to encrypt the generated secret.

        :default: default master key

        :stability: experimental
        """
        result = self._values.get("encryption_key")
        return result

    @builtins.property
    def master_password(self) -> typing.Optional[_SecretValue_c18506ef]:
        """(experimental) Password.

        Do not put passwords in your CDK code directly.

        :default: a Secrets Manager generated password

        :stability: experimental
        """
        result = self._values.get("master_password")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Login(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_redshift.NodeType")
class NodeType(enum.Enum):
    """(experimental) Possible Node Types to use in the cluster used for defining {@link ClusterProps.nodeType}.

    :stability: experimental
    """

    DS2_XLARGE = "DS2_XLARGE"
    """(experimental) ds2.xlarge.

    :stability: experimental
    """
    DS2_8XLARGE = "DS2_8XLARGE"
    """(experimental) ds2.8xlarge.

    :stability: experimental
    """
    DC1_LARGE = "DC1_LARGE"
    """(experimental) dc1.large.

    :stability: experimental
    """
    DC1_8XLARGE = "DC1_8XLARGE"
    """(experimental) dc1.8xlarge.

    :stability: experimental
    """
    DC2_LARGE = "DC2_LARGE"
    """(experimental) dc2.large.

    :stability: experimental
    """
    DC2_8XLARGE = "DC2_8XLARGE"
    """(experimental) dc2.8xlarge.

    :stability: experimental
    """
    RA3_16XLARGE = "RA3_16XLARGE"
    """(experimental) ra3.16xlarge.

    :stability: experimental
    """


@jsii.data_type(
    jsii_type="monocdk.aws_redshift.RotationMultiUserOptions",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "automatically_after": "automaticallyAfter"},
)
class RotationMultiUserOptions:
    def __init__(
        self,
        *,
        secret: _ISecret_22fb8757,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        """(experimental) Options to add the multi user rotation.

        :param secret: (experimental) The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> }
        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "secret": secret,
        }
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after

    @builtins.property
    def secret(self) -> _ISecret_22fb8757:
        """(experimental) The secret to rotate.

        It must be a JSON string with the following format::

           {
              "engine": <required: database engine>,
              "host": <required: instance host name>,
              "username": <required: username>,
              "password": <required: password>,
              "dbname": <optional: database name>,
              "port": <optional: if not specified, default port will be used>,
              "masterarn": <required: the arn of the master secret which will be used to create users/change passwords>
           }

        :stability: experimental
        """
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return result

    @builtins.property
    def automatically_after(self) -> typing.Optional[_Duration_070aa057]:
        """(experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        :default: Duration.days(30)

        :stability: experimental
        """
        result = self._values.get("automatically_after")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RotationMultiUserOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ICluster)
class Cluster(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_redshift.Cluster",
):
    """(experimental) Create a Redshift cluster a given number of nodes.

    :stability: experimental
    :resource: AWS::Redshift::Cluster
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        master_user: Login,
        vpc: _IVpc_6d1f76c4,
        cluster_name: typing.Optional[builtins.str] = None,
        cluster_type: typing.Optional[ClusterType] = None,
        default_database_name: typing.Optional[builtins.str] = None,
        encrypted: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        logging_bucket: typing.Optional[_IBucket_73486e29] = None,
        logging_key_prefix: typing.Optional[builtins.str] = None,
        node_type: typing.Optional[NodeType] = None,
        number_of_nodes: typing.Optional[jsii.Number] = None,
        parameter_group: typing.Optional[IClusterParameterGroup] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        roles: typing.Optional[typing.List[_IRole_59af6f50]] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        subnet_group: typing.Optional[IClusterSubnetGroup] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param master_user: (experimental) Username and password for the administrative user.
        :param vpc: (experimental) The VPC to place the cluster in.
        :param cluster_name: (experimental) An optional identifier for the cluster. Default: - A name is automatically generated.
        :param cluster_type: (experimental) Settings for the individual instances that are launched. Default: {@link ClusterType.MULTI_NODE}
        :param default_database_name: (experimental) Name of a database which is automatically created inside the cluster. Default: - default_db
        :param encrypted: (experimental) Whether to enable encryption of data at rest in the cluster. Default: true
        :param encryption_key: (experimental) The KMS key to use for encryption of data at rest. Default: - AWS-managed key, if encryption at rest is enabled
        :param logging_bucket: (experimental) Bucket to send logs to. Logging information includes queries and connection attempts, for the specified Amazon Redshift cluster. Default: - No Logs
        :param logging_key_prefix: (experimental) Prefix used for logging. Default: - no prefix
        :param node_type: (experimental) The node type to be provisioned for the cluster. Default: {@link NodeType.DC2_LARGE}
        :param number_of_nodes: (experimental) Number of compute nodes in the cluster. Only specify this property for multi-node clusters. Value must be at least 2 and no more than 100. Default: - 2 if ``clusterType`` is ClusterType.MULTI_NODE, undefined otherwise
        :param parameter_group: (experimental) Additional parameters to pass to the database engine https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html. Default: - No parameter group.
        :param port: (experimental) What port to listen on. Default: - The default for the engine is used.
        :param preferred_maintenance_window: (experimental) A preferred maintenance window day/time range. Should be specified as a range ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). Example: 'Sun:23:45-Mon:00:15' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param publicly_accessible: (experimental) Whether to make cluster publicly accessible. Default: false
        :param removal_policy: (experimental) The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update. Default: RemovalPolicy.RETAIN
        :param roles: (experimental) A list of AWS Identity and Access Management (IAM) role that can be used by the cluster to access other AWS services. Specify a maximum of 10 roles. Default: - No role is attached to the cluster.
        :param security_groups: (experimental) Security group. Default: - a new security group is created.
        :param subnet_group: (experimental) A cluster subnet group to use with this cluster. Default: - a new subnet group will be created.
        :param vpc_subnets: (experimental) Where to place the instances within the VPC. Default: - private subnets

        :stability: experimental
        """
        props = ClusterProps(
            master_user=master_user,
            vpc=vpc,
            cluster_name=cluster_name,
            cluster_type=cluster_type,
            default_database_name=default_database_name,
            encrypted=encrypted,
            encryption_key=encryption_key,
            logging_bucket=logging_bucket,
            logging_key_prefix=logging_key_prefix,
            node_type=node_type,
            number_of_nodes=number_of_nodes,
            parameter_group=parameter_group,
            port=port,
            preferred_maintenance_window=preferred_maintenance_window,
            publicly_accessible=publicly_accessible,
            removal_policy=removal_policy,
            roles=roles,
            security_groups=security_groups,
            subnet_group=subnet_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(Cluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterAttributes")
    @builtins.classmethod
    def from_cluster_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_endpoint_address: builtins.str,
        cluster_endpoint_port: jsii.Number,
        cluster_name: builtins.str,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
    ) -> ICluster:
        """(experimental) Import an existing DatabaseCluster from properties.

        :param scope: -
        :param id: -
        :param cluster_endpoint_address: (experimental) Cluster endpoint address.
        :param cluster_endpoint_port: (experimental) Cluster endpoint port.
        :param cluster_name: (experimental) Identifier for the cluster.
        :param security_groups: (experimental) The security groups of the redshift cluster. Default: no security groups will be attached to the import

        :stability: experimental
        """
        attrs = ClusterAttributes(
            cluster_endpoint_address=cluster_endpoint_address,
            cluster_endpoint_port=cluster_endpoint_port,
            cluster_name=cluster_name,
            security_groups=security_groups,
        )

        return jsii.sinvoke(cls, "fromClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addRotationMultiUser")
    def add_rotation_multi_user(
        self,
        id: builtins.str,
        *,
        secret: _ISecret_22fb8757,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
    ) -> _SecretRotation_e64158ad:
        """(experimental) Adds the multi user rotation to this cluster.

        :param id: -
        :param secret: (experimental) The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> }
        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        :stability: experimental
        """
        options = RotationMultiUserOptions(
            secret=secret, automatically_after=automatically_after
        )

        return jsii.invoke(self, "addRotationMultiUser", [id, options])

    @jsii.member(jsii_name="addRotationSingleUser")
    def add_rotation_single_user(
        self,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
    ) -> _SecretRotation_e64158ad:
        """(experimental) Adds the single user rotation of the master password to this cluster.

        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        :stability: experimental
        """
        return jsii.invoke(self, "addRotationSingleUser", [automatically_after])

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> _SecretAttachmentTargetProps_ab8522eb:
        """(experimental) Renders the secret attachment target specifications.

        :stability: experimental
        """
        return jsii.invoke(self, "asSecretAttachmentTarget", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> Endpoint:
        """(experimental) The endpoint to use for read/write operations.

        :stability: experimental
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        """(experimental) Identifier of the cluster.

        :stability: experimental
        """
        return jsii.get(self, "clusterName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_57ccbda9:
        """(experimental) Access to the network connections.

        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[_ISecret_22fb8757]:
        """(experimental) The secret attached to this cluster.

        :stability: experimental
        """
        return jsii.get(self, "secret")


@jsii.implements(IClusterParameterGroup)
class ClusterParameterGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_redshift.ClusterParameterGroup",
):
    """(experimental) A cluster parameter group.

    :stability: experimental
    :resource: AWS::Redshift::ClusterParameterGroup
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        parameters: typing.Mapping[builtins.str, builtins.str],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param parameters: (experimental) The parameters in this parameter group.
        :param description: (experimental) Description for this parameter group. Default: a CDK generated description

        :stability: experimental
        """
        props = ClusterParameterGroupProps(
            parameters=parameters, description=description
        )

        jsii.create(ClusterParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterParameterGroupName")
    @builtins.classmethod
    def from_cluster_parameter_group_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        cluster_parameter_group_name: builtins.str,
    ) -> IClusterParameterGroup:
        """(experimental) Imports a parameter group.

        :param scope: -
        :param id: -
        :param cluster_parameter_group_name: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromClusterParameterGroupName", [scope, id, cluster_parameter_group_name])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> builtins.str:
        """(experimental) The name of the parameter group.

        :stability: experimental
        """
        return jsii.get(self, "clusterParameterGroupName")


@jsii.implements(IClusterSubnetGroup)
class ClusterSubnetGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_redshift.ClusterSubnetGroup",
):
    """(experimental) Class for creating a Redshift cluster subnet group.

    :stability: experimental
    :resource: AWS::Redshift::ClusterSubnetGroup
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        description: builtins.str,
        vpc: _IVpc_6d1f76c4,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param description: (experimental) Description of the subnet group.
        :param vpc: (experimental) The VPC to place the subnet group in.
        :param removal_policy: (experimental) The removal policy to apply when the subnet group are removed from the stack or replaced during an update. Default: RemovalPolicy.RETAIN
        :param vpc_subnets: (experimental) Which subnets within the VPC to associate with this group. Default: - private subnets

        :stability: experimental
        """
        props = ClusterSubnetGroupProps(
            description=description,
            vpc=vpc,
            removal_policy=removal_policy,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(ClusterSubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterSubnetGroupName")
    @builtins.classmethod
    def from_cluster_subnet_group_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        cluster_subnet_group_name: builtins.str,
    ) -> IClusterSubnetGroup:
        """(experimental) Imports an existing subnet group by name.

        :param scope: -
        :param id: -
        :param cluster_subnet_group_name: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromClusterSubnetGroupName", [scope, id, cluster_subnet_group_name])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterSubnetGroupName")
    def cluster_subnet_group_name(self) -> builtins.str:
        """(experimental) The name of the cluster subnet group.

        :stability: experimental
        """
        return jsii.get(self, "clusterSubnetGroupName")


__all__ = [
    "CfnCluster",
    "CfnClusterParameterGroup",
    "CfnClusterParameterGroupProps",
    "CfnClusterProps",
    "CfnClusterSecurityGroup",
    "CfnClusterSecurityGroupIngress",
    "CfnClusterSecurityGroupIngressProps",
    "CfnClusterSecurityGroupProps",
    "CfnClusterSubnetGroup",
    "CfnClusterSubnetGroupProps",
    "Cluster",
    "ClusterAttributes",
    "ClusterParameterGroup",
    "ClusterParameterGroupProps",
    "ClusterProps",
    "ClusterSubnetGroup",
    "ClusterSubnetGroupProps",
    "ClusterType",
    "DatabaseSecret",
    "DatabaseSecretProps",
    "Endpoint",
    "ICluster",
    "IClusterParameterGroup",
    "IClusterSubnetGroup",
    "Login",
    "NodeType",
    "RotationMultiUserOptions",
]

publication.publish()
