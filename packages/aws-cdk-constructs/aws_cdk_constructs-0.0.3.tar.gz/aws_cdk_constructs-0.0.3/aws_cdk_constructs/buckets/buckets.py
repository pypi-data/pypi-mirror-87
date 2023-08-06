from aws_cdk import (
    aws_s3 as _s3,
    aws_iam as _iam,
    core,
)
import boto3


def check_if_bucket_exist(s3_bucket_name, profile=None):
    aws_session = boto3.Session(profile_name=profile)
    sdk_s3 = aws_session.client("s3")
    bucket_exist = True

    if not s3_bucket_name:
        return False

    try:
        sdk_s3.get_bucket_location(Bucket=s3_bucket_name)
    except:
        bucket_exist = False

    return bucket_exist

class Buckets(core.Construct):
    """ 

    Args:

        s3_assets_bucket_name (str): The S3 Bucket in which the application assets are stored

        s3_code_bucket_name (str): The S3 Bucket in which the application code-base is stored
        
        s3_assets_bucket_has_cdn (str): Wheather or not the Assets bucket will be serverd by a Cloudflare CDN
        
        s3_assets_bucket_website_index_document (str): Use this parameter to configure the Assets bucket as Web Hosting. This is the S3 key of the index document of your static site (generally is index.html)
        
        s3_assets_bucket_website_error_document (str): Use this parameter to configure the Assets bucket as Web Hosting. This is the S3 key of the error document of your static site (generally is error.html)

    """
    @property
    def get_s3_bucket_assets(self):
        """Returns the Assets S3 bucket

        Returns:
            aws_s3.Bucket: the Assets S3 bucket
        """
        return self.s3_assets_bucket

    @property
    def get_s3_bucket_code(self):
        """Returns the Code S3 bucket

        Returns:
            aws_s3.Bucket: the Code S3 bucket
        """
        return self.s3_code_bucket

    def create_bucket(
        self,
        logic_id,
        bucket_name,
        access_control=None,
        public_read_access=False,
        website_index_document=None,
        website_error_document=None,
        removal_policy=None,
        **kwargs
    ):
        """Create an S3 bucket

        Args:

            logic_id (str): The logical ID of the S3 Bucket
            
            bucket_name (str): The S3 Bucket name
            
            access_control (aws_cdk.aws_s3.BucketAccessControl): The S3 Bucket access control policy. For more info see `access_control` in https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html
            
            website_index_document (str): Use this parameter to configure the S3 bucket as Web Hosting. This is the S3 key of the index document of your static site (generally is index.html)
            
            website_error_document (str): Use this parameter to configure the S3 bucket as Web Hosting. This is the S3 key of the error document of your static site (generally is error.html)
            
            removal_policy (aws_cdk.core.RemovalPolicy): The S3 Bucket removal policy. For more info see `removal_policy` in https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html

        Returns:
            aws_s3.Bucket: the Code S3 bucket
        """
        # Create S3 bucket
        return _s3.Bucket(
            self,
            logic_id,
            bucket_name=bucket_name,
            access_control=access_control,
            public_read_access=public_read_access,
            website_index_document=website_index_document,
            website_error_document=website_error_document,
            removal_policy=removal_policy,
        )

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        s3_code_bucket_name=None,
        s3_assets_bucket_name=None,
        s3_assets_bucket_is_public="False",
        s3_assets_bucket_has_cdn="False",
        s3_assets_bucket_website_index_document=None,
        s3_assets_bucket_website_error_document="index.html",
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # Declare variables
        self.s3_code_bucket = self.s3_assets_bucket = None

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create conditions
        code_bucket_name_was_provided = s3_code_bucket_name.strip()
        assets_bucket_name_was_provided = s3_assets_bucket_name.strip()

        code_bucket_already_exist = check_if_bucket_exist(
            s3_bucket_name=s3_code_bucket_name
        )

        assets_bucket_already_exist = check_if_bucket_exist(
            s3_bucket_name=s3_assets_bucket_name
        )

        # Check if bucket has to be public
        assets_public_read_access = (
            s3_assets_bucket_is_public
            and isinstance(s3_assets_bucket_is_public, str)
            and s3_assets_bucket_is_public.lower() == "true"
        )

        include_cdn = (
            s3_assets_bucket_has_cdn
            and isinstance(s3_assets_bucket_has_cdn, str)
            and s3_assets_bucket_has_cdn.lower() == "true"
        )
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Conditionally create resources

        # S3 Bucket for code
        if code_bucket_name_was_provided and not code_bucket_already_exist:
            self.s3_code_bucket = self.create_bucket(
                logic_id="Code",
                bucket_name=s3_code_bucket_name,
                public_read_access=False,
                access_control=_s3.BucketAccessControl.PRIVATE,
                block_public_access=_s3.BlockPublicAccess.BLOCK_ALL,  # https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html
            )

        # S3 Bucket for assets
        if assets_bucket_name_was_provided and not assets_bucket_already_exist:
            # Default access level: PRIVATE
            self.s3_assets_bucket = self.create_bucket(
                logic_id="Assets",
                bucket_name=s3_assets_bucket_name,
                website_index_document=s3_assets_bucket_website_index_document,
                website_error_document=s3_assets_bucket_website_error_document,
                removal_policy=core.RemovalPolicy.DESTROY
                if assets_public_read_access
                else core.RemovalPolicy.RETAIN,
            )

            if assets_public_read_access:
                # Grant access to anyone
                self.s3_assets_bucket.grant_public_access()

                self.s3_assets_bucket.add_cors_rule(
                    allowed_methods=[
                        _s3.HttpMethods.GET,
                        _s3.HttpMethods.POST,
                        _s3.HttpMethods.PUT,
                        _s3.HttpMethods.DELETE,
                        _s3.HttpMethods.HEAD,
                    ],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                )

            # Limit access to CDN
            if s3_assets_bucket_has_cdn:

                # Cloudflare doc https://support.cloudflare.com/hc/en-us/articles/360037983412-Configuring-an-Amazon-Web-Services-static-site-to-use-Cloudflare
                cloudflare_ips = [
                    "2400:cb00::/32",
                    "2405:8100::/32",
                    "2405:b500::/32",
                    "2606:4700::/32",
                    "2803:f800::/32",
                    "2c0f:f248::/32",
                    "2a06:98c0::/29",
                    "103.21.244.0/22",
                    "103.22.200.0/22",
                    "103.31.4.0/22",
                    "104.16.0.0/12",
                    "108.162.192.0/18",
                    "131.0.72.0/22",
                    "141.101.64.0/18",
                    "162.158.0.0/15",
                    "172.64.0.0/13",
                    "173.245.48.0/20",
                    "188.114.96.0/20",
                    "190.93.240.0/20",
                    "197.234.240.0/22",
                    "198.41.128.0/17",
                ]

                self.s3_assets_bucket.add_to_resource_policy(
                    _iam.PolicyStatement(
                        effect=_iam.Effect.DENY,
                        principals=[_iam.Anyone()],
                        actions=["s3:GetObject"],
                        resources=[
                            "arn:aws:s3:::" + s3_assets_bucket_name,
                            "arn:aws:s3:::" + s3_assets_bucket_name + "/*",
                        ],
                        conditions={"NotIpAddress": {"aws:SourceIp": cloudflare_ips}},
                    )
                )

                self.s3_assets_bucket.add_cors_rule(
                    allowed_methods=[
                        _s3.HttpMethods.GET,
                        _s3.HttpMethods.POST,
                        _s3.HttpMethods.PUT,
                        _s3.HttpMethods.DELETE,
                        _s3.HttpMethods.HEAD,
                    ],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                )
