from aws_cdk import (
    Stack,
)

from aws_cdk.assertions import Template, Match

from webserver.network import NetworkConstruct

import pytest

@pytest.fixture(scope='session')
def test_stack_template() -> Template:
    stack = Stack()
    NetworkConstruct(stack, 'TestNetwork')
    return Template.from_stack(stack)

def test_vpc_created(test_stack_template: Template):
    test_stack_template.resource_count_is('AWS::EC2::VPC', 1)

def test_vpc_cidr_block(test_stack_template: Template):
    test_stack_template.has_resource_properties("AWS::EC2::VPC", {
        "CidrBlock": "10.0.0.0/16"
    })

def test_subnets_created(test_stack_template: Template):
    test_stack_template.resource_count_is('AWS::EC2::Subnet', 4)

def test_subnets_cidr_blocks(test_stack_template: Template):
    # Public Subnets
    test_stack_template.has_resource_properties("AWS::EC2::Subnet", {
        "CidrBlock": "10.0.1.0/24", "MapPublicIpOnLaunch": True
    })
    test_stack_template.has_resource_properties("AWS::EC2::Subnet", {
        "CidrBlock": "10.0.2.0/24", "MapPublicIpOnLaunch": True
    })

    # Private Subnets
    test_stack_template.has_resource_properties("AWS::EC2::Subnet", {
        "CidrBlock": "10.0.3.0/24", "MapPublicIpOnLaunch": False
    })
    test_stack_template.has_resource_properties("AWS::EC2::Subnet", {
        "CidrBlock": "10.0.4.0/24", "MapPublicIpOnLaunch": False
    })

def test_exactly_two_public_subnets(test_stack_template: Template):
    public_subnets = test_stack_template.find_resources(
        "AWS::EC2::Subnet",
        props={
            "Properties": {
                "MapPublicIpOnLaunch": True,
                "Tags": Match.array_with([
                    {
                        "Key": "aws-cdk:subnet-type", 
                        "Value": "Public"
                    }
                ])
            }
        }
    )

    assert len(public_subnets) == 2, "Should be exactly 2 public subnets"

def test_exactly_two_private_subnets(test_stack_template: Template):
    private_subnets = test_stack_template.find_resources(
        "AWS::EC2::Subnet",
        props={
            "Properties": {
                "MapPublicIpOnLaunch": False,
                "Tags": Match.array_with([
                    {"Key": "aws-cdk:subnet-type", "Value": "Private"}
                ])
            }
        }
    )
    assert len(private_subnets) == 2, "Should be exactly 2 private subnets"

def test_internet_gateway_created(test_stack_template: Template):
    test_stack_template.resource_count_is("AWS::EC2::InternetGateway", 1)

def test_public_subnets_have_route_to_internet_gateway(test_stack_template: Template):
    test_stack_template.has_resource_properties(
        "AWS::EC2::Route", {
            "RouteTableId": Match.any_value(),
            "DestinationCidrBlock": "0.0.0.0/0",
            "GatewayId": {
                "Ref": Match.string_like_regexp("TestNetwork*")
            }
        }
    )