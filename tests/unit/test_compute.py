from aws_cdk import (
    Stack
)
from aws_cdk.assertions import Template

from webserver.compute import ComputeConstruct

import pytest

@pytest.fixture(scope='session')
def test_compute_fixture():
    stack = Stack()
    ComputeConstruct(stack, 'TestCompute')
    return Template.from_stack(stack)