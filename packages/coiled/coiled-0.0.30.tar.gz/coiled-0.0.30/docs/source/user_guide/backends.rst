Cloud Accounts
==============

Hosted
------

By default your computations run inside Coiled's AWS account.
This makes it easy for you to get started quickly, without needing
to set up any additional infrastructure.

However, you may prefer to run Coiled-managed computations within your own
infrastructure for security or billing purposes.
Coiled can drive infrastructure that you own if you give it permission.

AWS
---

You can have Coiled run computations in your own AWS account.
This allows you to take advantage of any business or security arrangements
(such as startup credits or custom data access controls) you already have.

To do this,
`create an access key ID and secret access key <https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys>`_
and add them to the Team page of your Coiled account.

From now on, clusters you create with Coiled will be launched in your AWS account.

.. note::

    The AWS credentials you supply must be long-lived (not temporary) tokens, and have sufficient permissions
    to allow Coiled to set up management infrastructure and create & launch compute resources from within
    your AWS account.

    Also, note that if you have not used AWS Elastic Container Service in this
    account before, you may need to `create the necessary service-linked IAM role <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using-service-linked-roles.html>`_
    -- we cannot yet create it automatically.

For the full set of required permissions, click the dropdown below.

.. dropdown:: Click to see the full set of required permissions
  :title: bg-white

  * sts:GetCallerIdentity
  * iam:GetRole
  * iam:CreateRole
  * iam:AttachRolePolicy
  * iam:DeleteRole
  * iam:PassRole
  * ecs:RegisterTaskDefinition
  * ecs:RunTask
  * ecs:ListTasks
  * ecs:DescribeTasks
  * ecs:StopTask
  * ecs:ListTaskDefinitions
  * ecs:DescribeTaskDefinition
  * ecs:ListClusters
  * ecs:CreateCluster
  * ecr:DescribeImages
  * ecr:ListImages
  * ecr:DescribeRepositories
  * ecr:CreateRepository
  * ecr:GetAuthorizationToken
  * ecr:InitiateLayerUpload
  * ecr:UploadLayerPart
  * ecr:CompleteLayerUpload
  * ec2:DescribeSubnets
  * ec2:CreateSecurityGroup
  * ec2:AuthorizeSecurityGroupIngress
  * ec2:CreateTags
  * ec2:DescribeSecurityGroups
  * ec2:DeleteSecurityGroup
  * ec2:DescribeVpcs
  * ec2:DescribeRouteTables
  * ec2:CreateVpc
  * ec2:ModifyVpcAttribute
  * ec2:CreateInternetGateway
  * ec2:AttachInternetGateway
  * ec2:CreateVpcPeeringConnection
  * ec2:DescribeVpcPeeringConnections
  * ec2:CreateRouteTable
  * ec2:CreateRoute
  * ec2:DescribeAvailabilityZones
  * ec2:CreateSubnet
  * ec2:AssociateRouteTable
  * ec2:ModifySubnetAttribute
  * ec2:AllocateAddress
  * ec2:CreateNatGateway
  * ec2:DescribeNatGateways
  * ec2:DescribeNetworkInterfaces
  * logs:CreateLogGroup
  * logs:PutRetentionPolicy
  * logs:GetLogEvents

The below JSON template lists all the above permissions and can be used to `create the required IAM policy directly <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html#access_policies_create-json-editor>`_.

.. dropdown:: IAM policy template
  :title: bg-white

  .. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sts:GetCallerIdentity",
                "iam:GetRole",
                "iam:CreateRole",
                "iam:AttachRolePolicy",
                "iam:DeleteRole",
                "iam:PassRole",
                "ecs:RegisterTaskDefinition",
                "ecs:RunTask",
                "ecs:ListTasks",
                "ecs:DescribeTasks",
                "ecs:StopTask",
                "ecs:ListTaskDefinitions",
                "ecs:DescribeTaskDefinition",
                "ecs:ListClusters",
                "ecs:CreateCluster",
                "ecr:DescribeImages",
                "ecr:ListImages",
                "ecr:DescribeRepositories",
                "ecr:CreateRepository",
                "ecr:GetAuthorizationToken",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ec2:DescribeSubnets",
                "ec2:CreateSecurityGroup",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:CreateTags",
                "ec2:DescribeSecurityGroups",
                "ec2:DeleteSecurityGroup",
                "ec2:DescribeVpcs",
                "ec2:DescribeRouteTables",
                "ec2:CreateVpc",
                "ec2:ModifyVpcAttribute",
                "ec2:CreateInternetGateway",
                "ec2:AttachInternetGateway",
                "ec2:CreateVpcPeeringConnection",
                "ec2:DescribeVpcPeeringConnections",
                "ec2:CreateRouteTable",
                "ec2:CreateRoute",
                "ec2:DescribeAvailabilityZones",
                "ec2:CreateSubnet",
                "ec2:AssociateRouteTable",
                "ec2:ModifySubnetAttribute",
                "ec2:AllocateAddress",
                "ec2:CreateNatGateway",
                "ec2:DescribeNatGateways",
                "ec2:DescribeNetworkInterfaces",
                "logs:CreateLogGroup",
                "logs:PutRetentionPolicy",
                "logs:GetLogEvents"
            ],
            "Resource": "*"
            }
        ]
    }

Kubernetes
----------

You can also have Coiled launch computations on a Kubernetes cluster that you control.
This is a good way to run Coiled on other clouds or on-prem infrastructure.
In this situation you provide Coiiled a Kubernetes configuration file that
gives access to a particular namespace.

This feature is available in the general release, but not exposed through the web UI by
default while we iterate with early adopter users.  If you would like to be
part of our early-adopter program then please e-mail us at hello@coiled.io .
