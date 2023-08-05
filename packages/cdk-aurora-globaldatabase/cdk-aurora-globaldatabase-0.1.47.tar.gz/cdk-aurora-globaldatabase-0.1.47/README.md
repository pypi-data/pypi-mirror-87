[![NPM version](https://badge.fury.io/js/cdk-aurora-globaldatabase.svg)](https://badge.fury.io/js/cdk-aurora-globaldatabase)
[![PyPI version](https://badge.fury.io/py/cdk-aurora-globaldatabase.svg)](https://badge.fury.io/py/cdk-aurora-globaldatabase)
![Release](https://github.com/guan840912/cdk-aurora-globaldatabase/workflows/Release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-aurora-globaldatabase?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-aurora-globaldatabase?label=pypi&color=blue)

# cdk-aurora-globaldatabase

`cdk-aurora-globaldatabase` is an AWS CDK construct library that allows you to create [Amazon Aurora Global Databases](https://aws.amazon.com/rds/aurora/global-database/) with AWS CDK in Typescript or Python.

# Why

**Amazon Aurora Global Databases** is designed for multi-regional Amazon Aurora Database clusters that span across different AWS regions. Due to the lack of native cloudformation support, it has been very challenging to build with cloudformation or AWS CDK with the upstream `aws-rds` construct.

`cdk-aurora-globaldatabase` aims to offload the heavy-lifting and helps you provision and deploy cross-regional **Amazon Aurora Global Databases** simply with just a few CDK statements.

## Now Try It !!!

# Sample for Mysql

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from ..index import GolbalAuroraRDSMaster, InstanceTypeEnum, GolbalAuroraRDSSlaveInfra
from aws_cdk.core import App, Stack, CfnOutput
import aws_cdk.aws_ec2 as ec2
# new app .
mock_app = App()

# setting two region env config .
env_singapro = {"account": process.env.CDK_DEFAULT_ACCOUNT, "region": "ap-southeast-1"}
env_tokyo = {"account": process.env.CDK_DEFAULT_ACCOUNT, "region": "ap-northeast-1"}

# create stack main .
stack_m = Stack(mock_app, "testing-stackM", env=env_tokyo)
vpc_public = ec2.Vpc(stack_m, "defaultVpc",
    nat_gateways=0,
    max_azs=3,
    subnet_configuration=[SubnetConfiguration(
        cidr_mask=26,
        name="masterVPC2",
        subnet_type=ec2.SubnetType.PUBLIC
    )]
)
globaldb_m = GolbalAuroraRDSMaster(stack_m, "golbalAuroraRDSMaster",
    instance_type=InstanceTypeEnum.R5_LARGE,
    vpc=vpc_public,
    rds_password="1qaz2wsx"
)
globaldb_m.rds_cluster.connections.allow_default_port_from(ec2.Peer.ipv4(f"{process.env.MYIP}/32"))

# create stack slave infra or you can give your subnet group.
stack_s = Stack(mock_app, "testing-stackS", env=env_singapro)
vpc_public2 = ec2.Vpc(stack_s, "defaultVpc2",
    nat_gateways=0,
    max_azs=3,
    subnet_configuration=[SubnetConfiguration(
        cidr_mask=26,
        name="secondVPC2",
        subnet_type=ec2.SubnetType.PUBLIC
    )]
)
globaldb_s = GolbalAuroraRDSSlaveInfra(stack_s, "slaveregion", vpc=vpc_public2, subnet_type=ec2.SubnetType.PUBLIC)

# so we need to wait stack slave created first .
stack_m.add_dependency(stack_s)

CfnOutput(stack_m, "password", value=globaldb_m.rds_password)
# add second region cluster
globaldb_m.add_regional_cluster(stack_m, "addregionalrds",
    region="ap-southeast-1",
    db_subnet_group_name=globaldb_s.db_subnet_group.db_subnet_group_name
)
```

![like this ](./image/Mysql-cluster.jpg)

# Sample for Postgres

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from ..index import GolbalAuroraRDSMaster, InstanceTypeEnum, GolbalAuroraRDSSlaveInfra
from aws_cdk.core import App, Stack, CfnOutput
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as _rds

mock_app = App()
env_singapro = {"account": process.env.CDK_DEFAULT_ACCOUNT, "region": "ap-southeast-1"}
env_tokyo = {"account": process.env.CDK_DEFAULT_ACCOUNT, "region": "ap-northeast-1"}

stack_m = Stack(mock_app, "testing-stackM", env=env_tokyo)
vpc_public = ec2.Vpc(stack_m, "defaultVpc",
    nat_gateways=0,
    max_azs=3,
    subnet_configuration=[SubnetConfiguration(
        cidr_mask=26,
        name="masterVPC2",
        subnet_type=ec2.SubnetType.PUBLIC
    )]
)

# Note if you use postgres , need to give the same value in engineVersion and  dbClusterpPG's engine .
globaldb_m = GolbalAuroraRDSMaster(stack_m, "golbalAuroraRDSMaster",
    instance_type=InstanceTypeEnum.R5_LARGE,
    vpc=vpc_public,
    rds_password="1qaz2wsx",
    engine_version=_rds.DatabaseClusterEngine.aurora_postgres(
        version=_rds.AuroraPostgresEngineVersion.VER_11_7
    ),
    db_clusterp_pG=_rds.ParameterGroup(stack_m, "dbClusterparametergroup",
        engine=_rds.DatabaseClusterEngine.aurora_postgres(
            version=_rds.AuroraPostgresEngineVersion.VER_11_7
        ),
        parameters={
            "rds.force_ssl": "1",
            "rds.log_retention_period": "10080",
            "auto_explain.log_min_duration": "5000",
            "auto_explain.log_verbose": "1",
            "timezone": "UTC+8",
            "shared_preload_libraries": "auto_explain,pg_stat_statements,pg_hint_plan,pgaudit",
            "log_connections": "1",
            "log_statement": "ddl",
            "log_disconnections": "1",
            "log_lock_waits": "1",
            "log_min_duration_statement": "5000",
            "log_rotation_age": "1440",
            "log_rotation_size": "102400",
            "random_page_cost": "1",
            "track_activity_query_size": "16384",
            "idle_in_transaction_session_timeout": "7200000"
        }
    )
)
globaldb_m.rds_cluster.connections.allow_default_port_from(ec2.Peer.ipv4(f"{process.env.MYIP}/32"))

stack_s = Stack(mock_app, "testing-stackS", env=env_singapro)
vpc_public2 = ec2.Vpc(stack_s, "defaultVpc2",
    nat_gateways=0,
    max_azs=3,
    subnet_configuration=[SubnetConfiguration(
        cidr_mask=26,
        name="secondVPC2",
        subnet_type=ec2.SubnetType.PUBLIC
    )]
)
globaldb_s = GolbalAuroraRDSSlaveInfra(stack_s, "slaveregion",
    vpc=vpc_public2, subnet_type=ec2.SubnetType.PUBLIC
)

stack_m.add_dependency(stack_s)

CfnOutput(stack_m, "password", value=globaldb_m.rds_password)
# add second region cluster
globaldb_m.add_regional_cluster(stack_m, "addregionalrds",
    region="ap-southeast-1",
    db_subnet_group_name=globaldb_s.db_subnet_group.db_subnet_group_name
)
```

### To deploy

```bash
cdk deploy
```

### To destroy

```bash
cdk destroy
```

## :clap:  Supporters

[![Stargazers repo roster for @guan840912/cdk-aurora-globaldatabase](https://reporoster.com/stars/guan840912/cdk-aurora-globaldatabase)](https://github.com/guan840912/cdk-aurora-globaldatabase/stargazers)
[![Forkers repo roster for @guan840912/cdk-aurora-globaldatabase](https://reporoster.com/forks/guan840912/cdk-aurora-globaldatabase)](https://github.com/guan840912/cdk-aurora-globaldatabase/network/members)
