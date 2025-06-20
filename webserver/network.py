from constructs import Construct

from aws_cdk import (
    aws_ec2 as ec2,
)

class NetworkConstruct(Construct):
    @property
    def vpc(self) -> ec2.Vpc:
        return self._vpc

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Public Subnets
        public_subnet = ec2.SubnetConfiguration(
            name="PublicSubnet",
            subnet_type=ec2.SubnetType.PUBLIC,
            cidr_mask=24
        )

        # Private Subnets
        private_subnet = ec2.SubnetConfiguration(
            name="PrivateSubnet",
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
            cidr_mask=24
        )
        
        self._vpc = ec2.Vpc(
            self, "WebServerVPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            subnet_configuration=[
                public_subnet,
                private_subnet
            ],
            max_azs=2,
            nat_gateways=0
            )