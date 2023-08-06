from aws_cdk import (
    core,
    aws_rds as _rds,
    aws_ec2 as _ec2,
    aws_s3 as _s3,
    aws_secretsmanager as _secretsmanager,
    aws_kms as _kms,
)

engine_to_cdk_engine = {
    "legacy-aurora-mysql": _rds.DatabaseClusterEngine.aurora,
    "aurora-mysql": _rds.DatabaseClusterEngine.aurora_mysql,
    "aurora-postgresql": _rds.DatabaseClusterEngine.aurora_postgres,
    "oracle_s2": _rds.DatabaseInstanceEngine.oracle_se2,
    "oracle_ee": _rds.DatabaseInstanceEngine.oracle_ee,
    "mysql": _rds.DatabaseInstanceEngine.mysql,
    "postgresql": _rds.DatabaseInstanceEngine.postgres
}

engine_to_cluster_parameter_group_family = {
    "legacy-aurora-mysql": "default.aurora5.6",
    "aurora-mysql": "default.aurora-mysql5.7",
    "aurora-postgresql": "default.aurora-postgresql9.6",
    "oracle_s2": "default.oracle-se2-12-2",
    "oracle_ee": "default.oracle-ee-19",
    "mysql": "default.mysql5.7",
    "postgresql" : None
}

engine_to_version_class = {
    "legacy-aurora-mysql": _rds.AuroraEngineVersion,
    "aurora-mysql": _rds.AuroraMysqlEngineVersion,
    "mysql": _rds.MysqlEngineVersion,
    "oracle_s2": _rds.OracleEngineVersion,
    "oracle_ee": _rds.OracleEngineVersion,
    "aurora-postgresql": _rds.AuroraPostgresEngineVersion,
    "postgresql": _rds.PostgresEngineVersion
}


class Database(core.Construct):
    """
    A CDK construct to create a "computational tier" for your system.
    The construct will make easy to develop a fully compliant macro infrastructure component that includes EC2 instances, served by an Application Load Balancer.

    """
    @property
    def security_group(self):
        return self._rds_security_group

    @property
    def cluster(self):
        return self._cluster

    @property
    def instance(self):
        return self._instance

    @staticmethod
    def get_engine(database_engine, database_engine_version):
        # For MySQL engine: extract db major version
        major_version = database_engine_version.split(".")
        major_version = major_version[:-1]
        major_version = ".".join(major_version)

        return engine_to_cdk_engine[database_engine](
            # version=database_engine_version if database_engine_version else None
            version=engine_to_version_class[database_engine].of(
                database_engine_version, major_version
            )
        )

    def __init__(
        self,
        scope: core.Construct,
        id:str,
        environments_parameters=None,
        environment=None,
        app_name=None,
        database_instance_type=None,
        database_name=None,
        database_master_username="faoadmin",
        database_snapshot_id=None,
        database_engine=None,
        database_engine_version=None,
        database_cluster_parameters_group_name=None,
        parameter_group=None,
        database_allocated_storage=None,
        database_will_send_email=False,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create conditions

        environment = environment.lower()
        aws_account = environments_parameters["accounts"][environment]
        account_id = aws_account["id"]
        vpc = _ec2.Vpc.from_lookup(self, "VPC", vpc_id=aws_account["vpc"])

        is_production = environment == "Production"
        is_not_production = not is_production

        is_ha = is_production

        use_snapshot = database_snapshot_id
        not_use_snapshot = not use_snapshot

        is_cluster_compatible = "aurora" in database_engine
        is_not_cluster_compatible = not is_cluster_compatible

        is_oracle = "oracle" in database_engine

        has_no_parameter_group = parameter_group is None and database_cluster_parameters_group_name is None

        has_no_defult_parameter_group = has_no_parameter_group and engine_to_cluster_parameter_group_family[database_engine] is None

        sends_emails = (
            database_will_send_email
            and isinstance(database_will_send_email, str)
            and database_will_send_email.lower() == "true"
        )
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Validate input params

        # TODO

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Retrieve info from already existing AWS resources
        # Important: you need an internet connection!

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create AWS resources

        # ~~~~~~~~~~~~~~~~
        # Security group
        # ~~~~~~~~~~~~~~~~
        self._rds_security_group = _ec2.SecurityGroup(
            self,
            "rds_sg",
            vpc=vpc,
            security_group_name=app_name + "rds_sg",
            allow_all_outbound=True,
        )

        bastion_host_production_control_security_group = (
            _ec2.SecurityGroup.from_security_group_id(
                self,
                "bastion_host_production_control_security_group",
                aws_account["bastion_host_production_control_security_group"],
                mutable=False,
            )
        )

        security_groups=[
                self._rds_security_group,
                bastion_host_production_control_security_group,
            ]

        # Security group to send email
        if sends_emails:
            smtp_access_security_group = _ec2.SecurityGroup.from_security_group_id(
                self,
                "smtp_relay_security_group",
                aws_account["smtp_relay_security_group"],
                mutable=False,
            )
            security_groups.append(smtp_access_security_group)
            
        # ~~~~~~~~~~~~~~~~
        # RDS Instance type
        # ~~~~~~~~~~~~~~~~
        instance_type = _ec2.InstanceType(database_instance_type)
        instance_props = _rds.InstanceProps(
            instance_type=instance_type,
            vpc=vpc,
            security_groups=security_groups,
        )

        # ~~~~~~~~~~~~~~~~
        # AWS Secret Manager
        # ~~~~~~~~~~~~~~~~
        credentials = _rds.Credentials.from_username(database_master_username)
        identifier_prefix = (app_name + "-" + environment + "-").replace("_", "-")

        # ~~~~~~~~~~~~~~~~
        # KMS Encryption key
        # ~~~~~~~~~~~~~~~~
        key_arn = account_id
        key_arn = (
            "arn:aws:kms:eu-west-1:" + account_id + ":key/" + aws_account["kms_rds_key"]
        )
        encryption_key = _kms.Key.from_key_arn(self, "encryption_key", key_arn)

        # ~~~~~~~~~~~~~~~~
        # RDS Parameter group
        # ~~~~~~~~~~~~~~~~
        my_parameter_group = None
        if has_no_defult_parameter_group is False:
            my_parameter_group = (
                parameter_group
                or _rds.ParameterGroup.from_parameter_group_name(
                    self,
                    "parameter_group",
                    parameter_group_name=database_cluster_parameters_group_name
                    if database_cluster_parameters_group_name
                    else engine_to_cluster_parameter_group_family[database_engine],
                )
            )

        # ~~~~~~~~~~~~~~~~
        # RDS Database engine
        # ~~~~~~~~~~~~~~~~
        self._engine = self.get_engine(database_engine, database_engine_version)

        # ~~~~~~~~~~~~~~~~
        # RDS Cluster
        # ~~~~~~~~~~~~~~~~
        if is_cluster_compatible:
            self._cluster = _rds.DatabaseCluster(
                self,
                "cluster",
                engine=self._engine,
                instance_props=instance_props,
                credentials=credentials,
                cluster_identifier=identifier_prefix + database_engine,
                instance_identifier_base=identifier_prefix,
                # No need to create instance resource, only specify the amount
                instances=2 if is_ha else 1,
                backup=_rds.BackupProps(
                    retention=core.Duration.days(30), preferred_window="01:00-02:00"
                ),
                default_database_name="fao_default_schema",
                preferred_maintenance_window="mon:03:00-mon:04:00",
                parameter_group=my_parameter_group,
                storage_encryption_key=encryption_key,
            )

            # Conditionally create a cluster from a snapshot
            if use_snapshot:
                self._cluster.node.find_child("Resource").add_property_override(
                    "SnapshotIdentifier", database_snapshot_id
                )
                # While creating an RDS from a snapshot, MasterUsername cannot be specified
                self._cluster.node.find_child("Resource").add_property_override(
                    "MasterUsername", None
                )

        # ~~~~~~~~~~~~~~~~
        # RDS Instance
        # ~~~~~~~~~~~~~~~~
        if is_not_cluster_compatible:
            self._instance = _rds.DatabaseInstance(
                self,
                "instance",
                engine=self._engine,
                allocated_storage=database_allocated_storage and int(database_allocated_storage),
                allow_major_version_upgrade=False,
                database_name=database_name if database_name else None,
                license_model=_rds.LicenseModel.BRING_YOUR_OWN_LICENSE if is_oracle else None,
                credentials=credentials,
                # parameter_group=my_parameter_group,
                instance_type=instance_type,
                vpc=vpc,
                auto_minor_version_upgrade=True,
                backup_retention=core.Duration.days(30),
                copy_tags_to_snapshot=True,
                deletion_protection=is_production,
                instance_identifier=identifier_prefix + "db",
                # max_allocated_storage=None,
                multi_az=is_production,
                # option_group=None,
                preferred_maintenance_window="mon:03:00-mon:04:00",
                processor_features=None,
                security_groups=security_groups,
                storage_encryption_key=encryption_key,
            )

            self._instance.add_rotation_single_user(
                automatically_after=core.Duration.days(30)
            )
