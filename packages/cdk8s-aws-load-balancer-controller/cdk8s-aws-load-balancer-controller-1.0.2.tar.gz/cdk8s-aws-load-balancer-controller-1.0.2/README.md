[![NPM version](https://badge.fury.io/js/cdk8s-aws-load-balancer-controller.svg)](https://badge.fury.io/js/cdk8s-aws-load-balancer-controller)
[![PyPI version](https://badge.fury.io/py/cdk8s-aws-load-balancer-controller.svg)](https://badge.fury.io/py/cdk8s-aws-load-balancer-controller)
![Release](https://github.com/guan840912/cdk8s-aws-load-balancer-controller/workflows/Release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk8s-aws-load-balancer-controller?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk8s-aws-load-balancer-controller?label=pypi&color=blue)

# cdk8s-aws-load-balancer-controller

> [cdk8s aws load balancer controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller) constructs for cdk8s

This project was formerly known as "CDK AWS ALB Ingress Controller", I just rename it to be "CDK AWS Load Balancer Controller".

Basic implementation of a [aws load balancer controller](https://github.com/kubernetes-sigs/aws-load-balancer-controller) construct for cdk8s. Contributions are welcome!

## Usage

### AWS Load Balance Controller V1

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk8s import App, Chart
from constructs import Construct
from cdk8s_aws_load_balancer_controller import AlbIngressController

class MyChart(Chart):
    def __init__(self, scope, name):
        super().__init__(scope, name)
        AlbIngressController(self, "albingresscntroller",
            cluster_name="EKScluster"
        )
app = App()
MyChart(app, "testcdk8s")
app.synth()
```

### AWS Load Balance Controller V2

#### only support install in default namespace now!!!

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk8s import App, Chart
from cdk8s_aws_load_balancer_controller import AwsLoadBalancerController
import constructs as constructs

class MyChart(Chart):
    def __init__(self, scope, name, *, clusterName):
        super().__init__(scope, name)
        alb = AwsLoadBalancerController(self, "alb",
            cluster_name=cluster_name,
            create_service_account=False
        )
        self.deployment_name = alb.deployment_name
        self.deployment_name_space = alb.namespace
app = App()
MyChart(app, "testcdk8s")
app.synth()
```

# Featrue For Add IAM Policy.

* For IRSA add IAM Policy version 1.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# CDK APP like eks_cluster.ts
from cdk8s_aws_load_balancer_controller import AwsLoadBalancePolicy, VersionsLists
import aws_cdk.aws_eks as eks
cluster = eks.Cluster(self, "MyK8SCluster",
    default_capacity=0,
    masters_role=cluster_admin,
    version=eks.KubernetesVersion.V1_18
)

alb_service_account = cluster.add_service_account("alb-ingress-controller",
    name="alb-ingress-controller",
    namespace="kube-system"
)
# will help you add policy to IAM Role .
AwsLoadBalancePolicy.add_policy(VersionsLists.AWS_LOAD_BALANCER_CONTROLLER_POLICY_V1, alb_service_account)
```

* For IRSA add IAM Policy version 2.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# CDK APP like eks_cluster.ts
from cdk8s_aws_load_balancer_controller import AwsLoadBalancePolicy, VersionsLists
import aws_cdk.aws_eks as eks
cluster = eks.Cluster(self, "MyK8SCluster",
    default_capacity=0,
    masters_role=cluster_admin,
    version=eks.KubernetesVersion.V1_18
)

sa = eks.ServiceAccount(self, "albserviceaccount",
    cluster=cluster,
    name="aws-load-balancer-controller"
)
AwsLoadBalancePolicy.add_policy(VersionsLists.AWS_LOAD_BALANCER_CONTROLLER_POLICY_V2, sa)
```

Also can see [example repo](https://github.com/guan840912/cdk8s-cdk-example)

## License

Distributed under the [Apache 2.0](./LICENSE) license.
