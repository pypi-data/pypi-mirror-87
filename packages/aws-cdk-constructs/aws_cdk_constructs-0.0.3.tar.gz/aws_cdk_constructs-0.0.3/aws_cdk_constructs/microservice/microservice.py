from aws_cdk import (
    core,
    aws_elasticloadbalancingv2 as _alb,
    aws_ec2 as _ec2,
    aws_s3 as _s3,
    aws_certificatemanager as _certificate,
    aws_autoscaling as _asg,
    aws_autoscaling_hooktargets as _asg_hooktargets,
    aws_sns as _sns,
    aws_iam as _iam,
    aws_efs as _efs,
    aws_kms as _kms,
)
import json
import os
import re

alphanumericPattern = pattern = re.compile("\W")


class Microservice(core.Construct):
    """A CDK construct to create a "computational tier" for your system.
    The construct will make easy to develop a fully compliant macro infrastructure component that includes EC2 instances, served by an Application Load Balancer.

    Internally the construct includes:

    - Application Load Balancer, configurable to be 'internal' or 'interet-facing' or to integrate with Cognito

    - Load Balancer listeners, configurable to be HTTPS or HTTP
    
    - Auto Scaling 

    - Target group

    - Launch configuration


    Args:
        access_log_bucket_name (str): To enable Load Balancer acces logs to be stored in the specified S3 bucket
        
        additional_variables (str): You can specify additional parameters that will be available as environment variables for the EC2 user-data script
        
        app_name (str): The application name. This will be used to generate the 'ApplicationName' tag for CSI compliancy. The ID of the application. This must be unique for each system, as it will be used to calculate the AWS costs of the systen

        authorization_endpoint (str): Used with 'authorization_endpoint', 'client_id', 'client_secret', 'issuer', 'token_endpoint', 'user_info_endpoint'. Used to perform the OIDC Cognito integration with the Application Load balancer. More information https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html

        client_id (str): Used with 'authorization_endpoint', 'client_id', 'client_secret', 'issuer', 'token_endpoint', 'user_info_endpoint'. Used to perform the OIDC Cognito integration with the Application Load balancer. More information https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html

        client_secret (str): Used with 'authorization_endpoint', 'client_id', 'client_secret', 'issuer', 'token_endpoint', 'user_info_endpoint'. Used to perform the OIDC Cognito integration with the Application Load balancer. More information https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html

        downstream_port: Used with 'downstream_port', 'downstream_security_group'. In case the EC2 server should integrate with another AWS resource, specify the integration port. This is generally used to specify a database port, whenever an EC2 fetches data from a database.
        In case the EC2 should send traffic to other AWS resources (a.k.a. downstream), specify the port to which send traffic to (e.g. if the EC2 uses a MySQL database, specify the MySQL database port 3306)

        downstream_security_group (str): Used with 'downstream_port', 'downstream_security_group'. In case the EC2 server should integrate with a target AWS resource, specify the target resource security group. This is generally used to specify a database security group, whenever an EC2 fetches data from a database. In case the EC2 should send traffic to other AWS resources (a.k.a. downstream), specify the security group Id of those resources (e.g. if the EC2 uses a database, specify the database cluster security group)

        ebs_snapshot_id (str): In case you want to create a secondary EBS volume from an EBS snapshot for your EC2 instance, this parameter is used to specify the snaphost id. Only use this parameter when your system cannot horizontally scale!

        ebs_volume_size (str): In case you want to create a secondary EBS volume for your EC2 instance, this parameter is used to specify the volume size. The parameter specify the desired GB. Only use this parameter when your system cannot horizontally scale!

        ec2_ami_id (str): Specify the EC2 AMI id to use to create the EC2 instance.

        ec2_health_check_path (str):  Specify the Target Group health check path to use to monitor the state of the EC2 instances. EC2 instances will be constantly monitored, performing requests to this path. The request must receive a successful response code to consider the EC2 healthy. Otherwise the EC2 will be terminated and regenerated. It must start with a slash "/"

        ec2_instance_type (str): Specify the instance type of your EC2 instance. EC2 instance types https://aws.amazon.com/ec2/instance-types

        ec2_traffic_port (str): Specify the port the EC2 instance will listen to. This is used also as the Target Group Health check configuration port. For example (str)if you EC2 is equipped with an Apache Tomcat, listening on port 8080, use this parameter to specify 8080. It's important to note that this is not port the final user will use to connect to the system, as the Load Balancer will be in-front of the EC2.This is the port that the load balancer will use to forward traffic to the EC2 (e.g. Tomacat uses port 8080, Node.js uses port 3000).

        environment (str): Specify the environment in which you want to deploy you system. Allowed values: Development, QA, Production, SharedServices 

        environments_parameters (dict): The dictionary containing the references to CSI AWS environments. This will simplify the environment promotions and enable a parametric development of the infrastructures.

        issuer (str): Used with 'authorization_endpoint', 'client_id', 'client_secret', 'issuer', 'token_endpoint', 'user_info_endpoint'. Used to perform the OIDC Cognito integration with the Application Load balancer. More information https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html

        main_component_name (str): This is just a metadata. Textually specify the component the EC2 instance will host (e.g. tomcat, drupal, ...)

        s3_assets_bucket_name (str): S3 bucket name used to store the assets of the application

        s3_code_bucket_name (str): S3 bucket name used to store the code of the application

        ssl_certificate_arn (str): In case you want to enable HTTPS for your stack, specify the SSL certificate ARN to use. This configuration will force the creation of 2 load balancer Listeners (str)one on port 443 that proxies to the Target Group, a second one on port 80 to redirect the traffic to port 443 and enforce HTTPS. In case the application implements HTTPS, specify the ARN of the SSL Certificate to use. You can find it in AWS Certificate Manager

        toggle_to_trigger_rolling_update (str): Utility paremeter to manually trigger a complete replacement of the EC2 instances fleet. This is used to implement continuous deployment.

        token_endpoint (str): Used with 'authorization_endpoint', 'client_id', 'client_secret', 'issuer', 'token_endpoint', 'user_info_endpoint'. Used to perform the OIDC Cognito integration with the Application Load balancer. More information https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html

        traffic_port (str): Specify the port the Application Load Balancer will listen to. This is the port the final users will contact to browse the system. If HTTPS is enabled, this parameter will be forced to be 443. This is the port that the application will use to accpet traffic (e.g. if the application uses HTTPS, specify 443; if the application uses HTTP, specify 80; etc.)

        upstream_security_group (str): In case the application is published as part of a parent app, please specify the security group of the resource will sent traffic to the app (e.g. if the app is part of fao.org website, given that the app will be receive traffic from the fao.org reverse proxies, specify the fao.org reverse proxy security group ID)

        user_data_s3_key (str): Installation of tools, libs and any other requirements will be performed programmatically via user-data script. Please specify the S3 key of the user-data script to use. This file must be stored within the S3 configuration bucket of the specific environment, following the pattern ${ConfBucket}/${ApplicationName}/${Environment}/${UserDataS3Key} (e.g. dev-fao-aws-configuration-files/myApp1/Development/user-data.sh, prod-fao-aws-configuration-files/myApp2/Production/user-data.sh,)

        user_info_endpoint (str): Used with 'authorization_endpoint', 'client_id', 'client_secret', 'issuer', 'token_endpoint', 'user_info_endpoint'. Used to perform the OIDC Cognito integration with the Application Load balancer. More information https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-listenerrule-authenticateoidcconfig.html

        will_be_ha (str): Only applicatble if the EC2 is stateless! True/False depending to the fact your system can be configure to be highly available.

        will_be_public (str): Whether of not the application should be publicly accessible

        will_send_email (str): Whether of not the application should send email. Real email messages will be sent only from the Production environment. For the other evinronment the system will be configured to use the CSI dev SMTP server

        will_use_efs (str): Wether or not should create a EFS

    """

    @property
    def vpc(self):
        """
        Returns the VPC in which the stack is deployed on
        """
        return self._vpc

    @property
    def alb_logs_bucket(self):
        """
        Returns S3 bucket that the Application Load Balancer is using for storing the logs
        """
        return self._alb_logs_bucket

    @property
    def tcp_connection_ec2_traffic_port(self):
        """
        Returns the EC2 traffic port as TCP connection
        """
        return self._tcp_connection_ec2_traffic_port

    @property
    def tcp_connection_traffic_port(self):
        """
        Returns the Load Balancer port as TCP connection
        """
        return self._tcp_connection_traffic_port

    @property
    def target_group(self):
        """Returns the security group in use by the EC2

        Returns:
            aws_alb.ApplicationTargetGroup: the Application Target gruop
        """
        return self._tg

    @property
    def auto_scaling_group(self):
        """
        Returns the Auto Scaling Group object
        """
        return self._asg

    @property
    def load_balancer(self):
        """
        Returns the Application Load Balancer object
        """
        return self.alb

    @property
    def load_balancer_security_group(self):
        """
        Returns the security group in use by the application load balancer
        """ 
        return self.alb_security_group

    @property
    def ec2_instance_security_group(self):
        """
        Return the security group in use by the EC2 instance
        """ 
        return self.ec2_security_group

    @property
    def user_data(self):
        """
        Return the user-data used by the EC2 instance on boot
        """ 
        return self.base_user_data

    def enable_fao_private_access(self, security_group):
        """
        Apply the correct ingress rules to the provided security group to enable access from the FAO internal networks
        """ 
        security_group.add_ingress_rule(
            peer=self.pulse_cidr_as_peer(self._environments_parameters),
            connection=self.tcp_connection_traffic_port,
            description="Pulse Secure",
        )

        security_group.add_ingress_rule(
            peer=self.fao_hq_clients_as_peer(self._environments_parameters),
            connection=self.tcp_connection_traffic_port,
            description="FAO HQ Clients",
        )

    def create_target_group(
        self,
        id,
        app_name,
        ec2_traffic_port,
        ec2_health_check_path,
        protocol=_alb.ApplicationProtocol.HTTP,
    ):
        """
        Create a fully compliant Target Group object
        """ 
        tg = _alb.ApplicationTargetGroup(
            self,
            id,
            port=int(ec2_traffic_port),  # Must be a int
            protocol=protocol,
            vpc=self._vpc,
            target_type=_alb.TargetType.INSTANCE,
            target_group_name=(app_name + id + "-tg").replace("_", "-"),
        )
        tg.configure_health_check(
            enabled=True,
            healthy_http_codes="200-399",
            healthy_threshold_count=2,
            interval=core.Duration.seconds(6),
            path=ec2_health_check_path,
            port=ec2_traffic_port,
            protocol=protocol,
            timeout=core.Duration.seconds(5),
            unhealthy_threshold_count=2,
        )

        return tg

    def create_load_balancer(self, scope, id, security_group, internet_facing=False, load_balancer_name=None):
        """
        Create a fully compliant Application Load Balancer object
        """ 
        if load_balancer_name is None:
            load_balancer_name = id

        alb = _alb.ApplicationLoadBalancer(
            scope,
            id,
            load_balancer_name=load_balancer_name,
            vpc=self.vpc,
            internet_facing=internet_facing,
            idle_timeout=core.Duration.seconds(50),
            security_group=security_group,
        )
        # Enable logging
        alb.log_access_logs(self._alb_logs_bucket, prefix=self._app_name)
        return alb

    def create_security_group(
        self, scope, id, security_group_name, allow_all_outbound=True
    ):
        """
        Create a fully compliant Security Group
        """ 
        sg = _ec2.SecurityGroup(
            scope,
            id,
            vpc=self._vpc,
            security_group_name=security_group_name,
            allow_all_outbound=allow_all_outbound,
        )
        return sg

    # to update the userData definition after the first initialization
    def set_user_data_additional_variables(self, variables: dict):
        """
        Add the provided variables as environment variables for the user-data script
        """ 
        ADDITIONAL_VARIABLES_PLACEHOLDER = "#ADDITIONAL_VARIABLES_HERE"
        for vkey in variables:
            new_variable_string = (
                'echo "export _KEY_=_VALUE_" >> $MY_VARS_FILE\n'
                + ADDITIONAL_VARIABLES_PLACEHOLDER
            )
            new_variable_string = new_variable_string.replace("_KEY_", vkey)
            new_variable_string = new_variable_string.replace(
                "_VALUE_", variables[vkey]
            )
            self.base_user_data = self.base_user_data.replace(
                ADDITIONAL_VARIABLES_PLACEHOLDER, new_variable_string
            )

        return self.base_user_data

    # to update the userData definition after the first initialization
    def update_user_data(self, user_data: str):
        """
        Replaces the auto generated user-data with the provided one
        """ 
        self.node.find_child(self.asg_name()).node.find_child(
            "LaunchConfig"
        ).user_data = user_data

    @staticmethod
    def pulse_cidr_as_peer(environments_parameters):
        """
        Returns the Pulse secure network as Peer 
        """ 
        fao_networks = environments_parameters["networking"]
        return _ec2.Peer.ipv4(fao_networks["pulse"])

    @staticmethod
    def fao_hq_clients_as_peer(environments_parameters):
        """
        Returns the HQ client subnet as Peer
        """ 
        fao_networks = environments_parameters["networking"]
        return _ec2.Peer.ipv4(fao_networks["fao_hq_clients"])

    def asg_name(self):
        """Prints what the animals name is and what sound it makes.

        If the argument `sound` isn't passed in, the default Animal
        sound is used.

        Parameters
        ----------
        sound : str, optional
            The sound the animal makes (default is None)

        Raises
        ------
        NotImplementedError
            If no sound is set for the animal or passed in as a
            parameter.
        """
        return "asg"

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        main_component_name=None,
        will_be_public=False,
        will_send_email=False,
        ec2_ami_id=None,
        ec2_instance_type=None,
        autoscaling_group_max_size=None,
        s3_code_bucket_name=None,
        s3_assets_bucket_name=None,
        traffic_port=None,
        ec2_traffic_port=None,
        upstream_security_group=None,
        ec2_health_check_path=None,
        user_data_s3_key=None,
        downstream_security_group=None,
        downstream_port=None,
        ssl_certificate_arn=None,
        toggle_to_trigger_rolling_update=None,
        will_be_ha=False,
        ebs_volume_size=None,
        ebs_snapshot_id=None,
        will_use_efs=False,
        environment=None,
        environments_parameters=None,
        access_log_bucket_name="fao-elb-logs",
        app_name=None,
        authorization_endpoint=None,
        token_endpoint=None,
        issuer=None,
        client_id=None,
        client_secret=None,
        user_info_endpoint=None,
        additional_variables: dict = None,
        **kwargs
    ):
        """
        
        """

        super().__init__(scope, id, **kwargs)

        self.id = id

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create conditions
        is_https = not not ssl_certificate_arn
        is_not_https = not is_https

        sends_emails = (
            will_send_email
            and isinstance(will_send_email, str)
            and will_send_email.lower() == "true"
        )

        is_public = (
            will_be_public
            and isinstance(will_be_public, str)
            and will_be_public.lower() == "true"
        )
        is_private = not is_public

        is_production = environment == "Production"
        is_not_procution = not is_production

        has_upstream = not not upstream_security_group
        has_not_upstream = not has_upstream

        is_public_and_no_upstream = is_public and has_not_upstream
        is_public_and_has_upstream = is_public and has_upstream

        has_downstream = not not downstream_security_group
        has_not_downstream = not has_downstream

        is_ha = (
            will_be_ha and isinstance(will_be_ha, str) and will_be_ha.lower() == "true"
        )
        is_not_ha = not is_ha

        use_ebs = not not ebs_volume_size
        create_ebs = use_ebs and is_not_ha

        create_efs = (
            will_use_efs
            and isinstance(will_use_efs, str)
            and will_use_efs.lower() == "true"
        )

        is_private_and_is_https = is_private and is_https

        is_public_has_no_upstream_and_is_https = (
            has_not_upstream and is_public and is_https
        )
        is_public_has_upstream_and_is_https = has_upstream and is_public and is_https

        self._environments_parameters = environments_parameters
        aws_account = self._environments_parameters["accounts"][environment.lower()]

        az_in_use = aws_account["az"]

        account_id = aws_account["id"]

        self._app_name = app_name

        has_oidc = (
            authorization_endpoint
            and token_endpoint
            and issuer
            and client_id
            and client_secret
            and user_info_endpoint
        )
        has_not_oidc = not has_oidc

        has_at_least_one_oidc = (
            authorization_endpoint
            or token_endpoint
            or issuer
            or client_id
            or client_secret
            or user_info_endpoint
        )

        has_additional_variables = additional_variables

        ROOT_VOLUME_SIZE = 50
        AUTOSCALING_GROUP_LOGICAL_ID = re.sub(
            alphanumericPattern, "", "".join([main_component_name, "AutoScalingGroup"])
        )

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Validate input params

        if has_additional_variables and type(additional_variables) is not dict:
            raise Exception(
                "additional_variables should be passed as a python dictionary"
            )

        if has_at_least_one_oidc and not has_oidc:
            raise Exception(
                "OIDC configuration is not valid! If you aimed to configure OIDC listener please provide each of the parmas: authorization_endpoint, token_endpoint, issuer, client_id, client_secret, user_info_endpoint"
            )

        # MUST EXIST environments_parameters, enviroment
        # How to raise an exception in python
        #  raise Exception(
        #     "Impossible to find the mandatory env variable APPLICATION_NAME"
        # )

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Retrieve info from already existing AWS resources
        # Important: you need an internet connection!

        # VPC
        self._vpc = _ec2.Vpc.from_lookup(self, "VPC", vpc_id=aws_account["vpc"])

        # ALB logs bucket
        self._alb_logs_bucket = _s3.Bucket.from_bucket_name(
            self, "alb_logs_bucket", access_log_bucket_name
        )

        # SNS ASG notifications topic
        asg_notifications_topic = _sns.Topic.from_topic_arn(
            self, "asg_notifications_topic", aws_account["asg_sns_topic"]
        )

        # Shared CIDRs and peers for security groups
        self._tcp_connection_traffic_port = _ec2.Port.tcp(int(traffic_port))
        self._tcp_connection_ec2_traffic_port = _ec2.Port.tcp(int(ec2_traffic_port))
        self._pulse_cidr_as_peer = self.pulse_cidr_as_peer(self._environments_parameters)
        self._fao_hq_clients_as_peer = self.fao_hq_clients_as_peer(
            self._environments_parameters
        )
        upstream_security_group_as_peer = _ec2.SecurityGroup.from_security_group_id(
            self, "upstream_security_group", upstream_security_group, mutable=True
        )

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create AWS resources

        # ~~~~~~~~~~~~~~~~
        # EBS
        # ~~~~~~~~~~~~~~~~
        if create_ebs:
            ebs = _ec2.CfnVolume(
                self,
                "ebs",
                availability_zone=az_in_use,
                encrypted=True,
                kms_key_id=aws_account["kms_ebs_key"],
                size=int(ebs_volume_size),
                snapshot_id=ebs_snapshot_id,
            )

        # ~~~~~~~~~~~~~~~~
        # Target group
        # ~~~~~~~~~~~~~~~~
        self._tg = self.create_target_group(
            main_component_name, app_name, ec2_traffic_port, ec2_health_check_path
        )

        # ~~~~~~~~~~~~~~~~
        # Elastic Load Balancer Security Group
        # ~~~~~~~~~~~~~~~~
        self.alb_security_group = self.create_security_group(
            self, "alb_sg", app_name + '_' + main_component_name + "_alb_sg"
        )

        if is_private:
            self.enable_fao_private_access(self.alb_security_group)

        if is_public_and_no_upstream:
            self.alb_security_group.add_ingress_rule(
                peer=_ec2.Peer.any_ipv4(),
                connection=self._tcp_connection_traffic_port,
                description="Everyone",
            )

        if is_public_and_has_upstream:
            self.alb_security_group.add_ingress_rule(
                peer=upstream_security_group_as_peer,
                connection=self._tcp_connection_traffic_port,
                description="From upstream",
            )

        # Used when HTTPS is forced. These rules enable the redirect from HTTP -> HTTPS
        if is_private_and_is_https:
            self.alb_security_group.add_ingress_rule(
                peer=self._pulse_cidr_as_peer,
                connection=_ec2.Port.tcp(80),
                description="Pulse Secure",
            )
            self.alb_security_group.add_ingress_rule(
                peer=self._fao_hq_clients_as_peer,
                connection=_ec2.Port.tcp(80),
                description="FAO HQ Clients",
            )
        # Used when HTTPS is forced. These rules enable the redirect from HTTP -> HTTPS
        if is_public_has_no_upstream_and_is_https:
            self.alb_security_group.add_ingress_rule(
                peer=_ec2.Peer.any_ipv4(),
                connection=_ec2.Port.tcp(80),
                description="Everyone to HTTPS",
            )
        # Used when HTTPS is forced. These rules enable the redirect from HTTP -> HTTPS
        if is_public_has_upstream_and_is_https:
            self.alb_security_group.add_ingress_rule(
                peer=upstream_security_group_as_peer,
                connection=_ec2.Port.tcp(80),
                description="Upstream to HTTPS",
            )

        # ~~~~~~~~~~~~~~~~
        # Elastic Load Balancer v2
        # ~~~~~~~~~~~~~~~~
        self.alb = self.create_load_balancer(
            self, "alb", self.alb_security_group, internet_facing=is_public, load_balancer_name='-'.join([app_name, main_component_name, 'alb'])
        )

        # Listeners
        if is_not_https:
            self.alb.add_listener(
                "is_not_https",
                port=int(traffic_port),
                protocol=_alb.ApplicationProtocol.HTTP,
                default_target_groups=[self._tg],
            )

        if is_https:
            # HTTP listener forces HTTPS
            self.alb.add_listener(
                "redirect_to_https",
                port=80,
                protocol=_alb.ApplicationProtocol.HTTP,
                default_action=_alb.ListenerAction.redirect(
                    host="#{host}",
                    path="/#{path}",
                    port="443",
                    protocol="HTTPS",
                    query="#{query}",
                    permanent=True,
                ),
            )

            # HTTPS certificate
            certificate = _certificate.Certificate.from_certificate_arn(
                self, "https_certificate", certificate_arn=ssl_certificate_arn
            )

            if has_not_oidc:
                self.alb.add_listener(
                    "is_https",
                    port=int(traffic_port),
                    protocol=_alb.ApplicationProtocol.HTTPS,
                    certificates=[certificate],
                    default_target_groups=[self._tg],
                )

            if has_oidc:
                # Default action: forward to TG
                listener_default_action = _alb.ListenerAction.forward(
                    target_groups=[self._tg]
                )

                # OIDC action: authenticate with Cognito and concatenate the forward
                oidc_listener_action = _alb.ListenerAction.authenticate_oidc(
                    authorization_endpoint=authorization_endpoint,
                    token_endpoint=token_endpoint,
                    issuer=issuer,
                    client_id=client_id,
                    client_secret=core.SecretValue(value=client_secret),
                    user_info_endpoint=user_info_endpoint,
                    next=listener_default_action,
                )

                # Create listener
                self.alb.add_listener(
                    "is_https",
                    port=int(traffic_port),
                    protocol=_alb.ApplicationProtocol.HTTPS,
                    certificates=[certificate],
                    default_action=oidc_listener_action,
                )

        # ~~~~~~~~~~~~~~~~
        # Instance profile
        # ~~~~~~~~~~~~~~~~

        role = _iam.Role(
            self,
            "asg_role",
            description=app_name + "_" + main_component_name + "_ec2_role",
            assumed_by=_iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                # AWS managed policy to allow sending logs and custom metrics to CloudWatch
                _iam.ManagedPolicy.from_aws_managed_policy_name(
                    "CloudWatchAgentServerPolicy"
                ),
                # AWS managed policy to allow Session Manager console connections to the EC2 instance
                _iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                ),
            ],
            role_name=app_name + "_" + main_component_name + "_ec2_role",
        )

        # Inline policies
        role.attach_inline_policy(
            _iam.Policy(
                self,
                "ec2_policies",
                statements=[
                    # Policy for EBS
                    _iam.PolicyStatement(
                        actions=["ec2:AttachVolume", "ec2:DescribeVolumeStatus"],
                        resources=["*"],
                    ),
                    # S3 access to get from the config bucket configuration files, code packages and libraries
                    _iam.PolicyStatement(
                        actions=["s3:List*"],
                        resources=[
                            "arn:aws:s3:::" + aws_account["s3_config_bucket"],
                            "arn:aws:s3:::"
                            + aws_account["s3_config_bucket"]
                            + "/"
                            + self._app_name
                            + "/*",
                        ],
                    ),
                    _iam.PolicyStatement(
                        actions=["s3:*"],
                        resources=[
                            "arn:aws:s3:::"
                            + aws_account["s3_config_bucket"]
                            + "/"
                            + self._app_name
                            + "/"
                            + environment,
                            "arn:aws:s3:::"
                            + aws_account["s3_config_bucket"]
                            + "/"
                            + self._app_name
                            + "/"
                            + environment
                            + "/*",
                        ],
                    ),
                    # S3 access to get SentinelOne
                    _iam.PolicyStatement(
                        actions=["s3:List*", "s3:Get*"],
                        resources=[
                            "arn:aws:s3:::"
                            + aws_account["s3_config_bucket"]
                            + "/sentinelone/linux/*",
                        ],
                    ),
                    # KMS LimitedAccess just to use the keys
                    _iam.PolicyStatement(
                        actions=[
                            "kms:Decrypt",
                            "kms:Encrypt",
                            "kms:ReEncrypt*",
                            "kms:GenerateDataKey*",
                            "kms:Describe*",
                        ],
                        resources=[
                            "arn:aws:kms:eu-west-1:"
                            + core.Stack.of(
                                self
                            ).account  # Reference for 'AWS::AccountId'
                            + ":key/"
                            + aws_account["kms_ssm_key"],
                            "arn:aws:kms:eu-west-1:"
                            + core.Stack.of(
                                self
                            ).account  # Reference for 'AWS::AccountId'
                            + ":key/"
                            + aws_account["kms_ebs_key"],
                        ],
                    ),
                    _iam.PolicyStatement(
                        actions=[
                            "kms:CreateGrant",
                            "kms:ListGrants",
                            "kms:RevokeGrant",
                        ],
                        resources=[
                            "arn:aws:kms:eu-west-1:"
                            + core.Stack.of(
                                self
                            ).account  # Reference for 'AWS::AccountId'
                            + ":key/"
                            + aws_account["kms_ebs_key"],
                        ],
                    ),
                    # SSM Parameter store access
                    _iam.PolicyStatement(
                        actions=[
                            "ssm:Describe*",
                            "ssm:Get*",
                            "ssm:List*",
                        ],
                        resources=[
                            "arn:aws:kms:eu-west-1:"
                            + core.Stack.of(
                                self
                            ).account  # Reference for 'AWS::AccountId'
                            + ":parameter/"
                            + self._app_name
                            + "/*"
                        ],
                    ),
                ],
            )
        )

        # Assets bucket policies
        if s3_assets_bucket_name:
            role.attach_inline_policy(
                _iam.Policy(
                    self,
                    "ec2_s3_assets_bucket_policies",
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
        # Code bucket policies
        if s3_code_bucket_name:
            role.attach_inline_policy(
                _iam.Policy(
                    self,
                    "service_user_policies",
                    statements=[
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

        # ~~~~~~~~~~~~~~~~
        # EFS
        # ~~~~~~~~~~~~~~~~
        if create_efs:
            # efs_key = _kms.Key.from_key_arn(self, "efs_key", aws_account["kms_ebs_key"])
            efs = _efs.FileSystem(self, main_component_name+"efs", vpc=self._vpc, encrypted=False)
            # you will find an additional EFS instruction after ASG

        # ~~~~~~~~~~~~~~~~
        # User data
        # ~~~~~~~~~~~~~~~~

        # Look to the path of your current working directory
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "base_user_data.sh")

        # Read the base user data from file
        with open(file_path) as self.base_user_data_content:
            self.base_user_data = self.base_user_data_content.read()
        self.base_user_data_content.close()

        # Inject parameter within the user data script template.
        # To add an environemnt variable to the user data:
        # 1. Add a line to the self.base_user_data.sh
        # 2. Replace the placeholder with a proper value as done below
        self.base_user_data = self.base_user_data.replace(
            "_S3Bucket_", aws_account["s3_config_bucket"]
        )
        self.base_user_data = self.base_user_data.replace(
            "_DataVolumeId_", ebs.ref if create_ebs else ""
        )
        self.base_user_data = self.base_user_data.replace(
            "_SMTPServer_", aws_account["smtp_server_endpoint"]
        )
        self.base_user_data = self.base_user_data.replace(
            "_SMTPPort_", aws_account["smtp_server_port"]
        )
        self.base_user_data = self.base_user_data.replace(
            "_ApplicationName_", self._app_name
        )
        self.base_user_data = self.base_user_data.replace("_Environment_", environment)
        self.base_user_data = self.base_user_data.replace(
            "_S3CodeBucket_", s3_code_bucket_name
        )
        self.base_user_data = self.base_user_data.replace(
            "_S3AssetsBucket_", s3_assets_bucket_name
        )
        self.base_user_data = self.base_user_data.replace(
            "_IsAppPublic_", str(is_public)
        )
        self.base_user_data = self.base_user_data.replace("_AzInUse_", az_in_use)
        self.base_user_data = self.base_user_data.replace(
            "_UserDataS3Key_", user_data_s3_key
        )
        self.base_user_data = self.base_user_data.replace(
            "_ToggleToTriggerRollingUpdate_", toggle_to_trigger_rolling_update
        )
        self.base_user_data = self.base_user_data.replace(
            "_EC2_TRAFFIC_PORT_", ec2_traffic_port
        )
        if create_efs:
            self.base_user_data = self.base_user_data.replace(
                "_EFS_", efs.file_system_id
            )

        if has_additional_variables:
            self.set_user_data_additional_variables(additional_variables)

        user_data = _ec2.UserData.custom(self.base_user_data)

        # ~~~~~~~~~~~~~~~~
        # Auto Scaling Group
        # ~~~~~~~~~~~~~~~~
        instance_type = _ec2.InstanceType(ec2_instance_type)
        machine_image = _ec2.GenericLinuxImage({"eu-west-1": ec2_ami_id})
        vpc_subnets = _ec2.SubnetSelection(availability_zones=[az_in_use])

        # ~~~~~~~~~~~~~~~~
        # Block device mapping
        # ~~~~~~~~~~~~~~~~
        volume = _asg.BlockDeviceVolume()
        volume.ebs(
            ROOT_VOLUME_SIZE,
        )
        block_devices = _asg.BlockDevice(device_name="/dev/xvda", volume=volume)

        self._asg = _asg.AutoScalingGroup(
            self,
            self.asg_name(),
            instance_type=instance_type,
            machine_image=machine_image,
            vpc=self._vpc,
            vpc_subnets=vpc_subnets if create_ebs else None,
            cooldown=core.Duration.seconds(120),
            max_capacity=int(autoscaling_group_max_size),
            allow_all_outbound=True,
            health_check=_asg.HealthCheck.elb(grace=core.Duration.minutes(10)),
            ignore_unmodified_size_properties=True,
            notifications_topic=asg_notifications_topic,
            user_data=user_data,
            instance_monitoring=_asg.Monitoring.DETAILED,
            role=role,
            resource_signal_timeout=core.Duration.minutes(30),
            # block_devices=[block_devices],
            update_type=_asg.UpdateType.ROLLING_UPDATE,
            rolling_update_configuration=_asg.RollingUpdateConfiguration(
                max_batch_size=1,
                min_instances_in_service=2 if is_ha else 1,
                # min_successful_instances_percent=None,
                # pause_time=None,
                # ASG best practice https://aws.amazon.com/premiumsupport/knowledge-center/auto-scaling-group-rolling-updates/
                suspend_processes=[
                    _asg.ScalingProcess.HEALTH_CHECK,
                    _asg.ScalingProcess.REPLACE_UNHEALTHY,
                    _asg.ScalingProcess.AZ_REBALANCE,
                    _asg.ScalingProcess.ALARM_NOTIFICATION,
                    _asg.ScalingProcess.SCHEDULED_ACTIONS,
                ],
                wait_on_resource_signals=True,
            ),
        )

        ags_config = self._asg.node.find_child("LaunchConfig")
        ags_config.add_property_override(
            property_path="BlockDeviceMappings",
            value=[
                {
                    "DeviceName": "/dev/xvda",
                    "Ebs": {"VolumeSize": ROOT_VOLUME_SIZE, "Encrypted": True},
                }
            ],
        )

        # Configure the CFT signal to user data. To overcome the issue that the
        # ASG Logical Id cannot is hard to retrieve, let override it (easier withe the current CDK version)
        # and pass the fixed ASG logical Id as param of the CFN signal
        self._asg.node.default_child.override_logical_id(AUTOSCALING_GROUP_LOGICAL_ID)
        self._asg.add_user_data(
            "/opt/aws/bin/cfn-signal -e $? --stack {} --resource {} --region eu-west-1".format(
                core.Stack.of(self).stack_name, AUTOSCALING_GROUP_LOGICAL_ID
            )
        )

        # Attach Target group
        self._asg.attach_to_application_target_group(self._tg)

        # ~~~~~~~~~~~~~~~~
        # EFS: enble access from ASG
        # ~~~~~~~~~~~~~~~~
        if create_efs:
            # EFS is created above
            efs.connections.allow_default_port_from(self._asg)

        # Add EC2 security group
        self.ec2_security_group = _ec2.SecurityGroup(
            self,
            "ec2_sg",
            vpc=self._vpc,
            security_group_name=app_name + "_" + main_component_name + "_ec2_sg",
            allow_all_outbound=True,
        )
        self.ec2_security_group.add_ingress_rule(
            peer=self.alb_security_group,
            connection=self._tcp_connection_ec2_traffic_port,
            description="From Load Balancer",
        )
        self._asg.add_security_group(self.ec2_security_group)

        # Add mandatory FAO security groups
        # Bastion host access
        bastion_host_security_group = _ec2.SecurityGroup.from_security_group_id(
            self,
            "bastion_host_security_group",
            aws_account["bastion_host_security_group"],
            mutable=False,
        )
        self._asg.add_security_group(bastion_host_security_group)

        # Scan engin access
        scan_target_security_group = _ec2.SecurityGroup.from_security_group_id(
            self,
            "scan_target_security_group",
            aws_account["scan_target_security_group"],
            mutable=False,
        )
        self._asg.add_security_group(scan_target_security_group)

        # Security group to send email
        if sends_emails:
            smtp_access_security_group = _ec2.SecurityGroup.from_security_group_id(
                self,
                "smtp_relay_security_group",
                aws_account["smtp_relay_security_group"],
                mutable=False,
            )
            self._asg.add_security_group(smtp_access_security_group)
            

        # Scaling policies
        self._asg.scale_on_cpu_utilization(
            "asg_cpu_scaling",
            target_utilization_percent=80,
            cooldown=core.Duration.minutes(10),
        )

        # Lifecycle hooks
        asg_notifications_lifecycle_hook_role = _iam.Role.from_role_arn(
            self,
            "asg_notifications_lifecycle_hook_role",
            role_arn=aws_account["asg_cw_alerts_lc_hooks_role"],
            mutable=True,
        )
        notification_metadata = json.dumps(
            {"label": self._app_name + "-" + main_component_name}
        )

        asg_notifications_lifecycle_hook_launch_topic = _sns.Topic.from_topic_arn(
            self,
            "asg_notifications_lifecycle_hook_launch_topic",
            aws_account["asg_cw_alerts_lc_hooks_launch_sns"],
        )
        launch_notification_target = _asg_hooktargets.TopicHook(
            asg_notifications_lifecycle_hook_launch_topic
        )
        self._asg.add_lifecycle_hook(
            "asg_lifecycle_hooks_launch",
            lifecycle_transition=_asg.LifecycleTransition.INSTANCE_LAUNCHING,
            notification_target=launch_notification_target,
            default_result=_asg.DefaultResult.CONTINUE,
            heartbeat_timeout=core.Duration.seconds(60),
            notification_metadata=notification_metadata,
            role=asg_notifications_lifecycle_hook_role,
        )

        asg_notifications_lifecycle_hook_terminate_topic = _sns.Topic.from_topic_arn(
            self,
            "asg_notifications_lifecycle_hook_terminate_topic",
            aws_account["asg_cw_alerts_lc_hooks_terminate_sns"],
        )
        terminate_notification_target = _asg_hooktargets.TopicHook(
            asg_notifications_lifecycle_hook_terminate_topic
        )
        self._asg.add_lifecycle_hook(
            "asg_lifecycle_hooks_terminate",
            lifecycle_transition=_asg.LifecycleTransition.INSTANCE_TERMINATING,
            notification_target=terminate_notification_target,
            default_result=_asg.DefaultResult.CONTINUE,
            heartbeat_timeout=core.Duration.seconds(60),
            notification_metadata=notification_metadata,
            role=asg_notifications_lifecycle_hook_role,
        )

        # Downsteam
        if has_downstream:
            downstream_security_group = _ec2.SecurityGroup.from_security_group_id(
                self,
                "downstream_security_group",
                downstream_security_group,
                mutable=True,
            )
            tcp_connection_downstream_port = _ec2.Port.tcp(int(downstream_port))
            downstream_security_group.add_ingress_rule(
                peer=self.ec2_security_group,
                connection=tcp_connection_downstream_port,
                description="EC2 to downstream",
            )
