from aws_cdk import core, aws_iam as _iam


class ServiceUserForStaticAssets(core.Construct):
    """Construct to create the Service User to deploy the project static files from a CD/CI pipeline

    Args:
        app_name (str): The application name. This will be used to generate the 'ApplicationName' tag for CSI compliancy. The ID of the application. This must be unique for each system, as it will be used to calculate the AWS costs of the systen

        environment (str): Specify the environment in which you want to deploy you system. Allowed values: Development, QA, Production, SharedServices 

        environments_parameters (dict): The dictionary containing the references to CSI AWS environments. This will simplify the environment promotions and enable a parametric development of the infrastructures.

        s3_assets_bucket_name (str): The S3 Bucket in which the application assets are stored

        s3_code_bucket_name (str): The S3 Bucket in which the application code-base is stored

    """
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        app_name=None,
        environment=None,
        s3_code_bucket_name=None,
        s3_assets_bucket_name=None,
        environments_parameters=None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create conditions

        aws_account = environments_parameters["accounts"][environment.lower()]
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Validate input params

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Retrieve info from already existing AWS resources
        # Important: you need an internet connection!

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create AWS resources

        service_user = _iam.User(
            self,
            "service_user",
            managed_policies=None,
            user_name="SRVUSR-" + app_name + "_" + environment + "_conf",
        )

        service_user.add_managed_policy(
            _iam.ManagedPolicy(
                self,
                "service_user_policies",
                statements=[
                    # S3 Configuration bucket permissions
                    _iam.PolicyStatement(
                        actions=["s3:*"],
                        resources=[
                            "arn:aws:s3:::"
                            + aws_account["s3_config_bucket"]
                            + "/"
                            + app_name
                            + "/"
                            + environment
                            + "/",
                            "arn:aws:s3:::"
                            + aws_account["s3_config_bucket"]
                            + "/"
                            + app_name
                            + "/"
                            + environment
                            + "/*",
                        ],
                    ),
                    _iam.PolicyStatement(
                        actions=["s3:ListBucket*"],
                        resources=["arn:aws:s3:::" + aws_account["s3_config_bucket"]],
                    ),
                ],
            )
        )

        # S3 Code bucket permissions
        if s3_code_bucket_name:
            service_user.add_managed_policy(
                _iam.ManagedPolicy(
                    self,
                    "service_user_s3_code_bucket_policies",
                    statements=[
                        # S3 Assets bucket permissions
                        _iam.PolicyStatement(
                            actions=["s3:*"],
                            resources=[
                                "arn:aws:s3:::" + s3_code_bucket_name,
                                "arn:aws:s3:::" + s3_code_bucket_name + "/*",
                            ],
                        ),
                    ],
                )
            )

            # S3 Assets bucket permissions
        if s3_assets_bucket_name:
            service_user.add_managed_policy(
                _iam.ManagedPolicy(
                    self,
                    "service_user_s3_assets_bucket_policies",
                    statements=[
                        _iam.PolicyStatement(
                            actions=["s3:*"],
                            resources=[
                                "arn:aws:s3:::" + s3_assets_bucket_name,
                                "arn:aws:s3:::" + s3_assets_bucket_name + "/*",
                            ],
                        ),
                    ],
                )
            )
