"""
[![awscdk-jsii-template](https://img.shields.io/badge/built%20with-awscdk--jsii--template-blue)](https://github.com/pahud/awscdk-jsii-template)
[![NPM version](https://badge.fury.io/js/cdk-spot-one.svg)](https://badge.fury.io/js/cdk-spot-one)
[![PyPI version](https://badge.fury.io/py/cdk-spot-one.svg)](https://badge.fury.io/py/cdk-spot-one)
![Release](https://github.com/pahud/cdk-spot-one/workflows/Release/badge.svg)

# cdk-spot-one

One spot instance with EIP and defined duration. No interruption.

# Why

Sometimes we need an Amazon EC2 instance with static fixed IP for testing or development purpose for a duration of
time(probably hours). We need to make sure during this time, no interruption will occur and we don't want to pay
for on-demand rate. `cdk-spot-one` helps you reserve one single spot instance with pre-allocated or new
Elastic IP addresses(EIP) with defined `blockDuration`, during which time the spot instance will be secured with no spot interruption.

Behind the scene, `cdk-spot-one` provisions a spot fleet with capacity of single instance for you and it associates the EIP with this instance. The spot fleet is reserved as spot block with `blockDuration` from one hour up to six hours to ensure the high availability for your spot instance.

Multiple spot instances are possible by simply specifying the `targetCapacity` construct property, but we only associate the EIP with the first spot instance at this moment.

Enjoy your highly durable one spot instance with AWS CDK!

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_spot_one import SpotFleet

# create the first fleet for one hour and associate with our existing EIP
fleet = SpotFleet(stack, "SpotFleet")

# configure the expiration after 1 hour
fleet.expire_after(Duration.hours(1))

# create the 2nd fleet with single Gravition 2 instance for 6 hours and associate with new EIP
fleet2 = SpotFleet(stack, "SpotFleet2",
    block_duration=BlockDuration.SIX_HOURS,
    eip_allocation_id="eipalloc-0d1bc6d85895a5410",
    default_instance_type=InstanceType("c6g.large"),
    vpc=fleet.vpc
)
# configure the expiration after 6 hours
fleet2.expire_after(Duration.hours(6))

# print the instanceId from each spot fleet
CfnOutput(stack, "SpotFleetInstanceId", value=fleet.instance_id)
CfnOutput(stack, "SpotFleet2InstanceId", value=fleet2.instance_id)
```

# Create spot instances without duration block

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
fleet = SpotFleet(stack, "SpotFleet",
    block_duration=BlockDuration.NONE
)
```

NOTE: This kind of spot instance will be interrupted by AWS. However the fleet is using type [maintain](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet.html#spot-fleet-allocation-strategy), the fleet can be refulfilled.

# ARM64 and Graviton 2 support

`cdk-spot-one` selects the latest Amazon Linux 2 AMI for your `ARM64` instances. Simply select the instance types with the `defaultInstanceType` property and the `SpotFleet` will auto configure correct AMI for the instance.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
defaultInstanceType: new InstanceType('c6g.large')
```

# SSH connect

By default the `cdk-spot-one` does not bind any SSH public key for you on the instance. You are encouraged to use `ec2-instance-connect` to send your public key from local followed by one-time SSH connect.

For example:

```sh
pubkey="$HOME/.ssh/aws_2020_id_rsa.pub"
echo "sending public key to ${instanceId}"
aws ec2-instance-connect send-ssh-public-key --instance-id ${instanceId} --instance-os-user ec2-user \
--ssh-public-key file://${pubkey} --availability-zone ${az}
```

## npx ec2-connect INSTANCE_ID

To connect to the instance, run `npx ec2-connect` as below:

```sh
$ npx ec2-connect i-01f827ab9de7b93a9
```

or

```sh
$ npx ec2-connect i-01f827ab9de7b93a9 ~/.ssh/other_public_key_path
```

If you are using different SSH public key(default is ~/.ssh/id_rsa.pub)
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.core
import constructs


@jsii.data_type(
    jsii_type="cdk-spot-one.BaseSpotFleetProps",
    jsii_struct_bases=[aws_cdk.core.ResourceProps],
    name_mapping={
        "account": "account",
        "physical_name": "physicalName",
        "region": "region",
        "additional_user_data": "additionalUserData",
        "block_device_mappings": "blockDeviceMappings",
        "block_duration": "blockDuration",
        "custom_ami_id": "customAmiId",
        "default_instance_type": "defaultInstanceType",
        "instance_interruption_behavior": "instanceInterruptionBehavior",
        "instance_role": "instanceRole",
        "key_name": "keyName",
        "security_group": "securityGroup",
        "target_capacity": "targetCapacity",
        "terminate_instances_with_expiration": "terminateInstancesWithExpiration",
        "valid_from": "validFrom",
        "valid_until": "validUntil",
        "vpc": "vpc",
        "vpc_subnet": "vpcSubnet",
    },
)
class BaseSpotFleetProps(aws_cdk.core.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        additional_user_data: typing.Optional[typing.List[builtins.str]] = None,
        block_device_mappings: typing.Optional[typing.List[aws_cdk.aws_ec2.CfnLaunchTemplate.BlockDeviceMappingProperty]] = None,
        block_duration: typing.Optional["BlockDuration"] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        default_instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        instance_interruption_behavior: typing.Optional["InstanceInterruptionBehavior"] = None,
        instance_role: typing.Optional[aws_cdk.aws_iam.Role] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.SecurityGroup] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        terminate_instances_with_expiration: typing.Optional[builtins.bool] = None,
        valid_from: typing.Optional[builtins.str] = None,
        valid_until: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnet: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param additional_user_data: Additional commands for user data. Default: - no additional user data
        :param block_device_mappings: blockDeviceMappings for config instance. Default: - from ami config.
        :param block_duration: reservce the spot instance as spot block with defined duration. Default: - BlockDuration.ONE_HOUR
        :param custom_ami_id: custom AMI ID. Default: - The latest Amaozn Linux 2 AMI ID
        :param default_instance_type: default EC2 instance type. Default: - t3.large
        :param instance_interruption_behavior: The behavior when a Spot Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE
        :param instance_role: IAM role for the spot instance.
        :param key_name: SSH key name. Default: - no ssh key will be assigned
        :param security_group: Security group for the spot fleet. Default: - allows TCP 22 SSH ingress rule
        :param target_capacity: number of the target capacity. Default: - 1
        :param terminate_instances_with_expiration: terminate the instance when the allocation is expired. Default: - true
        :param valid_from: the time when the spot fleet allocation starts. Default: - no expiration
        :param valid_until: the time when the spot fleet allocation expires. Default: - no expiration
        :param vpc: VPC for the spot fleet. Default: - new VPC will be created
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        """
        if isinstance(vpc_subnet, dict):
            vpc_subnet = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnet)
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if additional_user_data is not None:
            self._values["additional_user_data"] = additional_user_data
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings
        if block_duration is not None:
            self._values["block_duration"] = block_duration
        if custom_ami_id is not None:
            self._values["custom_ami_id"] = custom_ami_id
        if default_instance_type is not None:
            self._values["default_instance_type"] = default_instance_type
        if instance_interruption_behavior is not None:
            self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if key_name is not None:
            self._values["key_name"] = key_name
        if security_group is not None:
            self._values["security_group"] = security_group
        if target_capacity is not None:
            self._values["target_capacity"] = target_capacity
        if terminate_instances_with_expiration is not None:
            self._values["terminate_instances_with_expiration"] = terminate_instances_with_expiration
        if valid_from is not None:
            self._values["valid_from"] = valid_from
        if valid_until is not None:
            self._values["valid_until"] = valid_until
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnet is not None:
            self._values["vpc_subnet"] = vpc_subnet

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        """The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        """
        result = self._values.get("account")
        return result

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        """The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        """
        result = self._values.get("physical_name")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def additional_user_data(self) -> typing.Optional[typing.List[builtins.str]]:
        """Additional commands for user data.

        :default: - no additional user data
        """
        result = self._values.get("additional_user_data")
        return result

    @builtins.property
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.CfnLaunchTemplate.BlockDeviceMappingProperty]]:
        """blockDeviceMappings for config instance.

        :default: - from ami config.
        """
        result = self._values.get("block_device_mappings")
        return result

    @builtins.property
    def block_duration(self) -> typing.Optional["BlockDuration"]:
        """reservce the spot instance as spot block with defined duration.

        :default: - BlockDuration.ONE_HOUR
        """
        result = self._values.get("block_duration")
        return result

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[builtins.str]:
        """custom AMI ID.

        :default: - The latest Amaozn Linux 2 AMI ID
        """
        result = self._values.get("custom_ami_id")
        return result

    @builtins.property
    def default_instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """default EC2 instance type.

        :default: - t3.large
        """
        result = self._values.get("default_instance_type")
        return result

    @builtins.property
    def instance_interruption_behavior(
        self,
    ) -> typing.Optional["InstanceInterruptionBehavior"]:
        """The behavior when a Spot Instance is interrupted.

        :default: - InstanceInterruptionBehavior.TERMINATE
        """
        result = self._values.get("instance_interruption_behavior")
        return result

    @builtins.property
    def instance_role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        """IAM role for the spot instance."""
        result = self._values.get("instance_role")
        return result

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        """SSH key name.

        :default: - no ssh key will be assigned
        """
        result = self._values.get("key_name")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.SecurityGroup]:
        """Security group for the spot fleet.

        :default: - allows TCP 22 SSH ingress rule
        """
        result = self._values.get("security_group")
        return result

    @builtins.property
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        """number of the target capacity.

        :default: - 1
        """
        result = self._values.get("target_capacity")
        return result

    @builtins.property
    def terminate_instances_with_expiration(self) -> typing.Optional[builtins.bool]:
        """terminate the instance when the allocation is expired.

        :default: - true
        """
        result = self._values.get("terminate_instances_with_expiration")
        return result

    @builtins.property
    def valid_from(self) -> typing.Optional[builtins.str]:
        """the time when the spot fleet allocation starts.

        :default: - no expiration
        """
        result = self._values.get("valid_from")
        return result

    @builtins.property
    def valid_until(self) -> typing.Optional[builtins.str]:
        """the time when the spot fleet allocation expires.

        :default: - no expiration
        """
        result = self._values.get("valid_until")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC for the spot fleet.

        :default: - new VPC will be created
        """
        result = self._values.get("vpc")
        return result

    @builtins.property
    def vpc_subnet(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """VPC subnet for the spot fleet.

        :default: - public subnet
        """
        result = self._values.get("vpc_subnet")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseSpotFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-spot-one.BlockDuration")
class BlockDuration(enum.Enum):
    ONE_HOUR = "ONE_HOUR"
    TWO_HOURS = "TWO_HOURS"
    THREE_HOURS = "THREE_HOURS"
    FOUR_HOURS = "FOUR_HOURS"
    FIVE_HOURS = "FIVE_HOURS"
    SIX_HOURS = "SIX_HOURS"
    NONE = "NONE"


@jsii.interface(jsii_type="cdk-spot-one.ILaunchtemplate")
class ILaunchtemplate(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILaunchtemplateProxy

    @jsii.member(jsii_name="bind")
    def bind(self, spotfleet: "SpotFleet") -> "SpotFleetLaunchTemplateConfig":
        """
        :param spotfleet: -
        """
        ...


class _ILaunchtemplateProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-spot-one.ILaunchtemplate"

    @jsii.member(jsii_name="bind")
    def bind(self, spotfleet: "SpotFleet") -> "SpotFleetLaunchTemplateConfig":
        """
        :param spotfleet: -
        """
        return jsii.invoke(self, "bind", [spotfleet])


@jsii.enum(jsii_type="cdk-spot-one.InstanceInterruptionBehavior")
class InstanceInterruptionBehavior(enum.Enum):
    HIBERNATE = "HIBERNATE"
    STOP = "STOP"
    TERMINATE = "TERMINATE"


@jsii.implements(ILaunchtemplate)
class LaunchTemplate(metaclass=jsii.JSIIMeta, jsii_type="cdk-spot-one.LaunchTemplate"):
    def __init__(self) -> None:
        jsii.create(LaunchTemplate, self, [])

    @jsii.member(jsii_name="bind")
    def bind(self, spotfleet: "SpotFleet") -> "SpotFleetLaunchTemplateConfig":
        """
        :param spotfleet: -
        """
        return jsii.invoke(self, "bind", [spotfleet])


@jsii.enum(jsii_type="cdk-spot-one.NodeType")
class NodeType(enum.Enum):
    """Whether the worker nodes should support GPU or just standard instances."""

    STANDARD = "STANDARD"
    """Standard instances."""
    GPU = "GPU"
    """GPU instances."""
    INFERENTIA = "INFERENTIA"
    """Inferentia instances."""
    ARM = "ARM"
    """ARM instances."""


class SpotFleet(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-spot-one.SpotFleet",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        eip_allocation_id: typing.Optional[builtins.str] = None,
        launch_template: typing.Optional[ILaunchtemplate] = None,
        additional_user_data: typing.Optional[typing.List[builtins.str]] = None,
        block_device_mappings: typing.Optional[typing.List[aws_cdk.aws_ec2.CfnLaunchTemplate.BlockDeviceMappingProperty]] = None,
        block_duration: typing.Optional[BlockDuration] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        default_instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
        instance_role: typing.Optional[aws_cdk.aws_iam.Role] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.SecurityGroup] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        terminate_instances_with_expiration: typing.Optional[builtins.bool] = None,
        valid_from: typing.Optional[builtins.str] = None,
        valid_until: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnet: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        account: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param eip_allocation_id: Allocation ID for your existing Elastic IP Address.
        :param launch_template: Launch template for the spot fleet.
        :param additional_user_data: Additional commands for user data. Default: - no additional user data
        :param block_device_mappings: blockDeviceMappings for config instance. Default: - from ami config.
        :param block_duration: reservce the spot instance as spot block with defined duration. Default: - BlockDuration.ONE_HOUR
        :param custom_ami_id: custom AMI ID. Default: - The latest Amaozn Linux 2 AMI ID
        :param default_instance_type: default EC2 instance type. Default: - t3.large
        :param instance_interruption_behavior: The behavior when a Spot Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE
        :param instance_role: IAM role for the spot instance.
        :param key_name: SSH key name. Default: - no ssh key will be assigned
        :param security_group: Security group for the spot fleet. Default: - allows TCP 22 SSH ingress rule
        :param target_capacity: number of the target capacity. Default: - 1
        :param terminate_instances_with_expiration: terminate the instance when the allocation is expired. Default: - true
        :param valid_from: the time when the spot fleet allocation starts. Default: - no expiration
        :param valid_until: the time when the spot fleet allocation expires. Default: - no expiration
        :param vpc: VPC for the spot fleet. Default: - new VPC will be created
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        """
        props = SpotFleetProps(
            eip_allocation_id=eip_allocation_id,
            launch_template=launch_template,
            additional_user_data=additional_user_data,
            block_device_mappings=block_device_mappings,
            block_duration=block_duration,
            custom_ami_id=custom_ami_id,
            default_instance_type=default_instance_type,
            instance_interruption_behavior=instance_interruption_behavior,
            instance_role=instance_role,
            key_name=key_name,
            security_group=security_group,
            target_capacity=target_capacity,
            terminate_instances_with_expiration=terminate_instances_with_expiration,
            valid_from=valid_from,
            valid_until=valid_until,
            vpc=vpc,
            vpc_subnet=vpc_subnet,
            account=account,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(SpotFleet, self, [scope, id, props])

    @jsii.member(jsii_name="expireAfter")
    def expire_after(self, duration: aws_cdk.core.Duration) -> None:
        """
        :param duration: -
        """
        return jsii.invoke(self, "expireAfter", [duration])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultInstanceType")
    def default_instance_type(self) -> aws_cdk.aws_ec2.InstanceType:
        return jsii.get(self, "defaultInstanceType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultSecurityGroup")
    def default_security_group(self) -> aws_cdk.aws_ec2.ISecurityGroup:
        """The default security group of the instance, which only allows TCP 22 SSH ingress rule."""
        return jsii.get(self, "defaultSecurityGroup")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        """the first instance id in this fleet."""
        return jsii.get(self, "instanceId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceRole")
    def instance_role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "instanceRole")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        """instance type of the first instance in this fleet."""
        return jsii.get(self, "instanceType")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(self) -> ILaunchtemplate:
        return jsii.get(self, "launchTemplate")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="spotFleetId")
    def spot_fleet_id(self) -> builtins.str:
        return jsii.get(self, "spotFleetId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="spotFleetRequestId")
    def spot_fleet_request_id(self) -> builtins.str:
        """SpotFleetRequestId for this spot fleet."""
        return jsii.get(self, "spotFleetRequestId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return jsii.get(self, "vpc")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetCapacity")
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "targetCapacity")


@jsii.data_type(
    jsii_type="cdk-spot-one.SpotFleetLaunchTemplateConfig",
    jsii_struct_bases=[],
    name_mapping={"launch_template": "launchTemplate", "spotfleet": "spotfleet"},
)
class SpotFleetLaunchTemplateConfig:
    def __init__(
        self,
        *,
        launch_template: ILaunchtemplate,
        spotfleet: SpotFleet,
    ) -> None:
        """
        :param launch_template: 
        :param spotfleet: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "launch_template": launch_template,
            "spotfleet": spotfleet,
        }

    @builtins.property
    def launch_template(self) -> ILaunchtemplate:
        result = self._values.get("launch_template")
        assert result is not None, "Required property 'launch_template' is missing"
        return result

    @builtins.property
    def spotfleet(self) -> SpotFleet:
        result = self._values.get("spotfleet")
        assert result is not None, "Required property 'spotfleet' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpotFleetLaunchTemplateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-spot-one.SpotFleetProps",
    jsii_struct_bases=[BaseSpotFleetProps],
    name_mapping={
        "account": "account",
        "physical_name": "physicalName",
        "region": "region",
        "additional_user_data": "additionalUserData",
        "block_device_mappings": "blockDeviceMappings",
        "block_duration": "blockDuration",
        "custom_ami_id": "customAmiId",
        "default_instance_type": "defaultInstanceType",
        "instance_interruption_behavior": "instanceInterruptionBehavior",
        "instance_role": "instanceRole",
        "key_name": "keyName",
        "security_group": "securityGroup",
        "target_capacity": "targetCapacity",
        "terminate_instances_with_expiration": "terminateInstancesWithExpiration",
        "valid_from": "validFrom",
        "valid_until": "validUntil",
        "vpc": "vpc",
        "vpc_subnet": "vpcSubnet",
        "eip_allocation_id": "eipAllocationId",
        "launch_template": "launchTemplate",
    },
)
class SpotFleetProps(BaseSpotFleetProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        additional_user_data: typing.Optional[typing.List[builtins.str]] = None,
        block_device_mappings: typing.Optional[typing.List[aws_cdk.aws_ec2.CfnLaunchTemplate.BlockDeviceMappingProperty]] = None,
        block_duration: typing.Optional[BlockDuration] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        default_instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
        instance_role: typing.Optional[aws_cdk.aws_iam.Role] = None,
        key_name: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.SecurityGroup] = None,
        target_capacity: typing.Optional[jsii.Number] = None,
        terminate_instances_with_expiration: typing.Optional[builtins.bool] = None,
        valid_from: typing.Optional[builtins.str] = None,
        valid_until: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnet: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        eip_allocation_id: typing.Optional[builtins.str] = None,
        launch_template: typing.Optional[ILaunchtemplate] = None,
    ) -> None:
        """
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param additional_user_data: Additional commands for user data. Default: - no additional user data
        :param block_device_mappings: blockDeviceMappings for config instance. Default: - from ami config.
        :param block_duration: reservce the spot instance as spot block with defined duration. Default: - BlockDuration.ONE_HOUR
        :param custom_ami_id: custom AMI ID. Default: - The latest Amaozn Linux 2 AMI ID
        :param default_instance_type: default EC2 instance type. Default: - t3.large
        :param instance_interruption_behavior: The behavior when a Spot Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE
        :param instance_role: IAM role for the spot instance.
        :param key_name: SSH key name. Default: - no ssh key will be assigned
        :param security_group: Security group for the spot fleet. Default: - allows TCP 22 SSH ingress rule
        :param target_capacity: number of the target capacity. Default: - 1
        :param terminate_instances_with_expiration: terminate the instance when the allocation is expired. Default: - true
        :param valid_from: the time when the spot fleet allocation starts. Default: - no expiration
        :param valid_until: the time when the spot fleet allocation expires. Default: - no expiration
        :param vpc: VPC for the spot fleet. Default: - new VPC will be created
        :param vpc_subnet: VPC subnet for the spot fleet. Default: - public subnet
        :param eip_allocation_id: Allocation ID for your existing Elastic IP Address.
        :param launch_template: Launch template for the spot fleet.
        """
        if isinstance(vpc_subnet, dict):
            vpc_subnet = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnet)
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if additional_user_data is not None:
            self._values["additional_user_data"] = additional_user_data
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings
        if block_duration is not None:
            self._values["block_duration"] = block_duration
        if custom_ami_id is not None:
            self._values["custom_ami_id"] = custom_ami_id
        if default_instance_type is not None:
            self._values["default_instance_type"] = default_instance_type
        if instance_interruption_behavior is not None:
            self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if key_name is not None:
            self._values["key_name"] = key_name
        if security_group is not None:
            self._values["security_group"] = security_group
        if target_capacity is not None:
            self._values["target_capacity"] = target_capacity
        if terminate_instances_with_expiration is not None:
            self._values["terminate_instances_with_expiration"] = terminate_instances_with_expiration
        if valid_from is not None:
            self._values["valid_from"] = valid_from
        if valid_until is not None:
            self._values["valid_until"] = valid_until
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnet is not None:
            self._values["vpc_subnet"] = vpc_subnet
        if eip_allocation_id is not None:
            self._values["eip_allocation_id"] = eip_allocation_id
        if launch_template is not None:
            self._values["launch_template"] = launch_template

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        """The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        """
        result = self._values.get("account")
        return result

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        """The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        """
        result = self._values.get("physical_name")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def additional_user_data(self) -> typing.Optional[typing.List[builtins.str]]:
        """Additional commands for user data.

        :default: - no additional user data
        """
        result = self._values.get("additional_user_data")
        return result

    @builtins.property
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.CfnLaunchTemplate.BlockDeviceMappingProperty]]:
        """blockDeviceMappings for config instance.

        :default: - from ami config.
        """
        result = self._values.get("block_device_mappings")
        return result

    @builtins.property
    def block_duration(self) -> typing.Optional[BlockDuration]:
        """reservce the spot instance as spot block with defined duration.

        :default: - BlockDuration.ONE_HOUR
        """
        result = self._values.get("block_duration")
        return result

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[builtins.str]:
        """custom AMI ID.

        :default: - The latest Amaozn Linux 2 AMI ID
        """
        result = self._values.get("custom_ami_id")
        return result

    @builtins.property
    def default_instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """default EC2 instance type.

        :default: - t3.large
        """
        result = self._values.get("default_instance_type")
        return result

    @builtins.property
    def instance_interruption_behavior(
        self,
    ) -> typing.Optional[InstanceInterruptionBehavior]:
        """The behavior when a Spot Instance is interrupted.

        :default: - InstanceInterruptionBehavior.TERMINATE
        """
        result = self._values.get("instance_interruption_behavior")
        return result

    @builtins.property
    def instance_role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        """IAM role for the spot instance."""
        result = self._values.get("instance_role")
        return result

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        """SSH key name.

        :default: - no ssh key will be assigned
        """
        result = self._values.get("key_name")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.SecurityGroup]:
        """Security group for the spot fleet.

        :default: - allows TCP 22 SSH ingress rule
        """
        result = self._values.get("security_group")
        return result

    @builtins.property
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        """number of the target capacity.

        :default: - 1
        """
        result = self._values.get("target_capacity")
        return result

    @builtins.property
    def terminate_instances_with_expiration(self) -> typing.Optional[builtins.bool]:
        """terminate the instance when the allocation is expired.

        :default: - true
        """
        result = self._values.get("terminate_instances_with_expiration")
        return result

    @builtins.property
    def valid_from(self) -> typing.Optional[builtins.str]:
        """the time when the spot fleet allocation starts.

        :default: - no expiration
        """
        result = self._values.get("valid_from")
        return result

    @builtins.property
    def valid_until(self) -> typing.Optional[builtins.str]:
        """the time when the spot fleet allocation expires.

        :default: - no expiration
        """
        result = self._values.get("valid_until")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC for the spot fleet.

        :default: - new VPC will be created
        """
        result = self._values.get("vpc")
        return result

    @builtins.property
    def vpc_subnet(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """VPC subnet for the spot fleet.

        :default: - public subnet
        """
        result = self._values.get("vpc_subnet")
        return result

    @builtins.property
    def eip_allocation_id(self) -> typing.Optional[builtins.str]:
        """Allocation ID for your existing Elastic IP Address.

        :defalt: new EIP and its association will be created for the first instance in this spot fleet
        """
        result = self._values.get("eip_allocation_id")
        return result

    @builtins.property
    def launch_template(self) -> typing.Optional[ILaunchtemplate]:
        """Launch template for the spot fleet."""
        result = self._values.get("launch_template")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpotFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcProvider(
    aws_cdk.core.Stack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-spot-one.VpcProvider",
):
    def __init__(
        self,
        scope: typing.Optional[constructs.Construct] = None,
        id: typing.Optional[builtins.str] = None,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.core.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.core.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Creates a new stack.

        :param scope: Parent of this stack, usually an ``App`` or a ``Stage``, but could be any construct.
        :param id: The construct ID of this stack. If ``stackName`` is not explicitly defined, this id (and any parent IDs) will be used to determine the physical ID of the stack.
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        """
        props = aws_cdk.core.StackProps(
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(VpcProvider, self, [scope, id, props])

    @jsii.member(jsii_name="getOrCreate")
    @builtins.classmethod
    def get_or_create(cls, scope: aws_cdk.core.Construct) -> aws_cdk.aws_ec2.IVpc:
        """
        :param scope: -
        """
        return jsii.sinvoke(cls, "getOrCreate", [scope])


__all__ = [
    "BaseSpotFleetProps",
    "BlockDuration",
    "ILaunchtemplate",
    "InstanceInterruptionBehavior",
    "LaunchTemplate",
    "NodeType",
    "SpotFleet",
    "SpotFleetLaunchTemplateConfig",
    "SpotFleetProps",
    "VpcProvider",
]

publication.publish()
