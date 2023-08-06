from aws_cdk import core, aws_iam as _iam


class CdkServiceUser(core.Construct):
    @property
    def service_user(self):
        return self._service_user

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        app_name,
        aws_cdk_parameters,
        environment,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create conditions

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Validate input params

        aws_account = aws_cdk_parameters["accounts"][environment.lower()]

        account_id = aws_account["id"]

        kms_ssm_key = aws_account["kms_ssm_key"]
        kms_rds_key = aws_account["kms_rds_key"]
        kms_ebs_key = aws_account["kms_ebs_key"]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Retrieve info from already existing AWS resources
        # Important: you need an internet connection!

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create AWS resources

        managed_policy = _iam.ManagedPolicy(
            self,
            "managed_policy",
            description=app_name + " managed policy for CDK",
            statements=[
                # Resource ALL
                _iam.PolicyStatement(
                    actions=[
                        "cloudformation:Describe*",
                        "cloudformation:ValidateTemplate",
                        "cloudformation:CreateChangeSet",
                        "cloudformation:ExecuteChangeSe",
                        "ec2:CreateSecurityGroup",
                        "ec2:*SecurityGroup*",
                        "ec2:Describe*",
                        "ec2:createTags*",
                        "serverlessrepo:SearchApplications",
                        "serverlessrepo:GetApplication",
                        "serverlessrepo:*CloudFormationTemplate",
                        "serverlessrepo:*CloudFormationChangeSet",
                        "serverlessrepo:List*",
                        "serverlessrepo:Get*",
                        "secretsmanager:GetRandomPassword",
                        "elasticloadbalancingv2:Describe*",
                        "elasticloadbalancing:Describe*",
                        "elasticloadbalancing:Delete*",
                        "elasticloadbalancingv2:*",
                        "elasticloadbalancing:*",
                        "elasticloadbalancing:ModifyLoadBalancerAttributes*",
                        "autoscaling:Describe*",
                        "iam:PutRolePolicy",
                        "iam:getRolePolicy",
                        "iam:GetUser",
                        "iam:DeleteRolePolicy",
                        "iam:DetachUserPolicy",
                        "iam:ListAccessKeys",
                        "iam:DeleteUser",
                        "iam:AttachUserPolicy",
                        "iam:PassRole",
                        "iam:DeleteAccessKey",
                        "rds:DescribeEngineDefaultParameters",
                        "elasticfilesystem:DeleteMountTarget",
                        "elasticfilesystem:DescribeFileSystems",
                    ],
                    resources=["*"],
                ),
                # Filter by ARN pattern
                _iam.PolicyStatement(
                    actions=[
                        "cloudformation:*",
                    ],
                    resources=[
                        "arn:aws:cloudformation:eu-west-1:*:stack/" + app_name + "*"
                    ],
                ),
                _iam.PolicyStatement(
                    actions=[
                        "s3:*",
                    ],
                    resources=[
                        "arn:aws:s3:::" + app_name + "*",
                        "arn:aws:s3:::awsserverlessrepo-changesets-*",
                    ],
                ),
                _iam.PolicyStatement(
                    actions=[
                        "ec2:*",
                    ],
                    resources=["arn:aws:ec2:eu-west-1:*:*/" + app_name + "*"],
                ),
                _iam.PolicyStatement(
                    actions=[
                        "elasticloadbalancingv2:*",
                        "elasticloadbalancing:*",
                    ],
                    resources=[
                        "arn:aws:elasticloadbalancing:eu-west-1:*:*/" + app_name + "*"
                    ],
                ),
                _iam.PolicyStatement(
                    actions=[
                        "rds:*",
                    ],
                    resources=["arn:aws:rds:eu-west-1:*:*:" + app_name + "*"],
                ),
                _iam.PolicyStatement(
                    actions=[
                        "secretsmanager:*",
                    ],
                    resources=[
                        "arn:aws:secretsmanager:eu-west-1:*:*:" + app_name + "*"
                    ],
                ),
                _iam.PolicyStatement(
                    actions=[
                        "lambda:*",
                    ],
                    resources=["arn:aws:lambda:eu-west-1:*:*:" + app_name + "*"],
                ),
                _iam.PolicyStatement(
                    actions=[
                        "autoscaling:*",
                    ],
                    resources=[
                        "arn:aws:autoscaling:eu-west-1:*:*:*:*" + app_name + "*",
                    ],
                ),
                _iam.PolicyStatement(
                    actions=[
                        "elasticfilesystem:*",
                    ],
                    resources=[
                        "arn:aws:elasticfilesystem:eu-west-1:*:*:*:*" + app_name + "*",
                    ],
                ),
                _iam.PolicyStatement(
                    actions=[
                        "iam:*",
                    ],
                    resources=[
                        "arn:aws:iam::*:user/" + app_name + "*",
                        # "arn:aws:iam::*:federated-user/" + app_name + "*",
                        "arn:aws:iam::*:role/" + app_name + "*",
                        "arn:aws:iam::*:group/" + app_name + "*",
                        "arn:aws:iam::*:instance-profile/" + app_name + "*",
                        # "arn:aws:iam::*:mfa/" + app_name + "*",
                        # "arn:aws:iam::*:server-certificate/" + app_name + "*",
                        "arn:aws:iam::*:policy/" + app_name + "*",
                        # "arn:aws:iam::*:sms-mfa/" + app_name + "*",
                        # "arn:aws:iam::*:saml-provider/" + app_name + "*",
                        # "arn:aws:iam::*:oidc-provider/" + app_name + "*",
                        # "arn:aws:iam::*:report/" + app_name + "*",
                        # "arn:aws:iam::*:access-report/" + app_name + "*",
                    ],
                ),
                # Filter by TAG
                _iam.PolicyStatement(
                    actions=[
                        "cloudformation:*",
                        "s3:*",
                        "ec2:*",
                        "elasticloadbalancingv2:*",
                        "elasticloadbalancing:*",
                        "rds:*",
                        "secretsmanager:*",
                        "autoscaling:*",
                        "lambda:*",
                        "logs:*",
                        "iam:*",
                        "elasticfilesystem:*",
                    ],
                    resources=["*"],
                    conditions={
                        "ForAnyValue:StringLikeIfExists": {
                            "aws:RequestTag/ApplicationName": app_name
                        }
                    },
                ),
                # Filter by SPECIFIC RESOURCE
                _iam.PolicyStatement(
                    actions=[
                        "kms:Decrypt",
                        "kms:Encrypt",
                        "kms:ReEncrypt*",
                        "kms:GenerateDataKey*",
                        "kms:Describe*",
                        "kms:CreateGrant",
                        "kms:DescribeKey",
                    ],
                    resources=[
                        "arn:aws:kms:eu-west-1:" + account_id + ":key/" + kms_ebs_key,
                        "arn:aws:kms:eu-west-1:" + account_id + ":key/" + kms_rds_key,
                        "arn:aws:kms:eu-west-1:" + account_id + ":key/" + kms_ssm_key,
                    ],
                ),
                _iam.PolicyStatement(
                    actions=[
                        "ssm:Describe*",
                        "ssm:Get*",
                        "ssm:List*",
                    ],
                    resources=[
                        "arn:aws:ssm:eu-west-1:"
                        + account_id
                        + ":parameter/"
                        + app_name
                        + "*"
                    ],
                ),
            ],
        )

        self._service_user = _iam.User(
            self,
            "service_user",
            managed_policies=[managed_policy],
            user_name="SRVUSR-" + app_name + "_" + environment + "_cdk",
        )
