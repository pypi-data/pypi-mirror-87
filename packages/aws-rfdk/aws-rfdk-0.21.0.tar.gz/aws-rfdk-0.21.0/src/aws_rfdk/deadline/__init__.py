import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import aws_cdk.aws_autoscaling
import aws_cdk.aws_certificatemanager
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_docdb
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr_assets
import aws_cdk.aws_ecs
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_logs
import aws_cdk.aws_route53
import aws_cdk.aws_s3
import aws_cdk.aws_secretsmanager
import aws_cdk.core
from .. import (
    ConnectableApplicationEndpoint as _ConnectableApplicationEndpoint_075040da,
    HealthCheckConfig as _HealthCheckConfig_ebe26fb6,
    IHealthMonitor as _IHealthMonitor_ab248fa9,
    IMongoDb as _IMongoDb_dbee748a,
    IMonitorableFleet as _IMonitorableFleet_71f4eb88,
    IMountableLinuxFilesystem as _IMountableLinuxFilesystem_5182ce0b,
    IScriptHost as _IScriptHost_ad38c9ad,
    IX509CertificatePem as _IX509CertificatePem_da3ef30f,
    IX509CertificatePkcs12 as _IX509CertificatePkcs12_63b2574c,
    LogGroupFactoryProps as _LogGroupFactoryProps_b817ed21,
)


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.BuildArgs",
    jsii_struct_bases=[],
    name_mapping={},
)
class BuildArgs:
    def __init__(self) -> None:
        """Build arguments to supply to a Docker image build."""
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildArgs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseConnection(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aws-rfdk.deadline.DatabaseConnection",
):
    """Helper class for connecting Thinkbox's Deadline to a specific Database."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _DatabaseConnectionProxy

    def __init__(self) -> None:
        jsii.create(DatabaseConnection, self, [])

    @jsii.member(jsii_name="forDocDB")
    @builtins.classmethod
    def for_doc_db(
        cls,
        *,
        database: aws_cdk.aws_docdb.IDatabaseCluster,
        login: aws_cdk.aws_secretsmanager.ISecret,
    ) -> "DatabaseConnection":
        """Creates a DatabaseConnection which allows Deadline to connect to Amazon DocumentDB.

        Note: Deadline officially supports only databases that are compatible with MongoDB 3.6.


        Resources Deployed

        This construct does not deploy any resources

        :param database: The Document DB Cluster this connection is for. Note: Deadline officially supports only databases that are compatible with MongoDB 3.6.
        :param login: A Secret that contains the login information for the database. This must be a secret containing a JSON document as follows: { "username": "", "password": "" }
        """
        options = DocDBConnectionOptions(database=database, login=login)

        return jsii.sinvoke(cls, "forDocDB", [options])

    @jsii.member(jsii_name="forMongoDbInstance")
    @builtins.classmethod
    def for_mongo_db_instance(
        cls,
        *,
        client_certificate: _IX509CertificatePkcs12_63b2574c,
        database: _IMongoDb_dbee748a,
    ) -> "DatabaseConnection":
        """Creates a DatabaseConnection which allows Deadline to connect to MongoDB.

        Note: Deadline officially supports only databases that are compatible with MongoDB 3.6.


        Resources Deployed

        This construct does not deploy any resources

        :param client_certificate: The client certificate to register in the database during install of the Deadline Repository, and for the Deadline Client to use to connect to the database. This **MUST** be signed by the same signing certificate as the MongoDB server's certificate. Note: A limitation of Deadline **requires** that this certificate be signed directly by your root certificate authority (CA). Deadline will be unable to connect to MongoDB if it has been signed by an intermediate CA.
        :param database: The MongoDB database to connect to. Note: Deadline officially supports only databases that are compatible with MongoDB 3.6.
        """
        options = MongoDbInstanceConnectionOptions(
            client_certificate=client_certificate, database=database
        )

        return jsii.sinvoke(cls, "forMongoDbInstance", [options])

    @jsii.member(jsii_name="addChildDependency")
    @abc.abstractmethod
    def add_child_dependency(self, child: aws_cdk.core.IConstruct) -> None:
        """Add an ordering dependency to another Construct.

        All constructs in the child's scope will be deployed after the database has been deployed.

        This can be used to ensure that the database is fully up and serving data before an instance attempts to connect to it.

        :param child: The child to make dependent upon this database.
        """
        ...

    @jsii.member(jsii_name="addConnectionDBArgs")
    @abc.abstractmethod
    def add_connection_db_args(self, host: "IHost") -> None:
        """Adds commands to an Instance or Autoscaling groups User Data to configure the Deadline client so it can access the DB  Implementation must add commands to the instance userData that exports a function called configure_deadline_database() that accepts no arguments, and does what ever deadline-specific setup is required to allow Deadline to connect to the database.

        This implementation avoids secrets being leaked to the cloud-init logs.

        :param host: -
        """
        ...

    @jsii.member(jsii_name="addInstallerDBArgs")
    @abc.abstractmethod
    def add_installer_db_args(self, host: "IHost") -> None:
        """Adds commands to a UserData to build the argument list needed to install the Deadline Repository.

        The implementation must export a shell function called configure_database_installation_args(),
        that takes no arguments. This function must define an array environment variable called
        INSTALLER_DB_ARGS where each element of the array is a key-value pair of Deadline installer
        option to option value. (ex: ["--dbuser"]=someusername).

        This implementation avoids secrets being leaked to the cloud-init logs.

        :param host: -
        """
        ...

    @jsii.member(jsii_name="allowConnectionsFrom")
    @abc.abstractmethod
    def allow_connections_from(self, other: aws_cdk.aws_ec2.IConnectable) -> None:
        """Allow connections to the Database from the given connection peer.

        :param other: -
        """
        ...

    @jsii.member(jsii_name="grantRead")
    @abc.abstractmethod
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> None:
        """Grants permissions to the principal that allow it to use the Database as a typical Deadline user.

        :param grantee: -
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="containerEnvironment")
    @abc.abstractmethod
    def container_environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        """Returns the environment variables for configuring containers to connect to the database."""
        ...


class _DatabaseConnectionProxy(DatabaseConnection):
    @jsii.member(jsii_name="addChildDependency")
    def add_child_dependency(self, child: aws_cdk.core.IConstruct) -> None:
        """Add an ordering dependency to another Construct.

        All constructs in the child's scope will be deployed after the database has been deployed.

        This can be used to ensure that the database is fully up and serving data before an instance attempts to connect to it.

        :param child: The child to make dependent upon this database.
        """
        return jsii.invoke(self, "addChildDependency", [child])

    @jsii.member(jsii_name="addConnectionDBArgs")
    def add_connection_db_args(self, host: "IHost") -> None:
        """Adds commands to an Instance or Autoscaling groups User Data to configure the Deadline client so it can access the DB  Implementation must add commands to the instance userData that exports a function called configure_deadline_database() that accepts no arguments, and does what ever deadline-specific setup is required to allow Deadline to connect to the database.

        This implementation avoids secrets being leaked to the cloud-init logs.

        :param host: -
        """
        return jsii.invoke(self, "addConnectionDBArgs", [host])

    @jsii.member(jsii_name="addInstallerDBArgs")
    def add_installer_db_args(self, host: "IHost") -> None:
        """Adds commands to a UserData to build the argument list needed to install the Deadline Repository.

        The implementation must export a shell function called configure_database_installation_args(),
        that takes no arguments. This function must define an array environment variable called
        INSTALLER_DB_ARGS where each element of the array is a key-value pair of Deadline installer
        option to option value. (ex: ["--dbuser"]=someusername).

        This implementation avoids secrets being leaked to the cloud-init logs.

        :param host: -
        """
        return jsii.invoke(self, "addInstallerDBArgs", [host])

    @jsii.member(jsii_name="allowConnectionsFrom")
    def allow_connections_from(self, other: aws_cdk.aws_ec2.IConnectable) -> None:
        """Allow connections to the Database from the given connection peer.

        :param other: -
        """
        return jsii.invoke(self, "allowConnectionsFrom", [other])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> None:
        """Grants permissions to the principal that allow it to use the Database as a typical Deadline user.

        :param grantee: -
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="containerEnvironment")
    def container_environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        """Returns the environment variables for configuring containers to connect to the database."""
        return jsii.get(self, "containerEnvironment")


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.DeadlineDockerRecipes",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeadlineDockerRecipes:
    def __init__(self) -> None:
        """A collection of Deadline Docker recipes."""
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeadlineDockerRecipes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.DocDBConnectionOptions",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "login": "login"},
)
class DocDBConnectionOptions:
    def __init__(
        self,
        *,
        database: aws_cdk.aws_docdb.IDatabaseCluster,
        login: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        """Options when constructing UserData for Linux.

        :param database: The Document DB Cluster this connection is for. Note: Deadline officially supports only databases that are compatible with MongoDB 3.6.
        :param login: A Secret that contains the login information for the database. This must be a secret containing a JSON document as follows: { "username": "", "password": "" }
        """
        self._values: typing.Dict[str, typing.Any] = {
            "database": database,
            "login": login,
        }

    @builtins.property
    def database(self) -> aws_cdk.aws_docdb.IDatabaseCluster:
        """The Document DB Cluster this connection is for.

        Note: Deadline officially supports only databases that are compatible with MongoDB 3.6.
        """
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return result

    @builtins.property
    def login(self) -> aws_cdk.aws_secretsmanager.ISecret:
        """A Secret that contains the login information for the database.

        This must be a secret containing a JSON document as follows:
        {
        "username": "",
        "password": ""
        }
        """
        result = self._values.get("login")
        assert result is not None, "Required property 'login' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocDBConnectionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ECSConnectOptions",
    jsii_struct_bases=[],
    name_mapping={"grantee": "grantee", "hosts": "hosts"},
)
class ECSConnectOptions:
    def __init__(
        self,
        *,
        grantee: aws_cdk.aws_iam.IGrantable,
        hosts: typing.List["IHost"],
    ) -> None:
        """Properties that need to be provided in order to connect an ECS service to a Render Queue.

        :param grantee: The task definitions Role that needs permissions.
        :param hosts: The set of hosts that will be hosting the containers. This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "grantee": grantee,
            "hosts": hosts,
        }

    @builtins.property
    def grantee(self) -> aws_cdk.aws_iam.IGrantable:
        """The task definitions Role that needs permissions."""
        result = self._values.get("grantee")
        assert result is not None, "Required property 'grantee' is missing"
        return result

    @builtins.property
    def hosts(self) -> typing.List["IHost"]:
        """The set of hosts that will be hosting the containers.

        This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.
        """
        result = self._values.get("hosts")
        assert result is not None, "Required property 'hosts' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ECSConnectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ECSContainerInstanceProps",
    jsii_struct_bases=[],
    name_mapping={"hosts": "hosts", "filesystem_mount_point": "filesystemMountPoint"},
)
class ECSContainerInstanceProps:
    def __init__(
        self,
        *,
        hosts: typing.List["IHost"],
        filesystem_mount_point: typing.Optional[builtins.str] = None,
    ) -> None:
        """Configuration interface for specifying ECS container instances to permit connecting hosted ECS tasks to the repository.

        :param hosts: The set of hosts that will be hosting the containers. This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.
        :param filesystem_mount_point: The path where the repository file-system is mounted on the container hosts. Default: "/mnt/repo"
        """
        self._values: typing.Dict[str, typing.Any] = {
            "hosts": hosts,
        }
        if filesystem_mount_point is not None:
            self._values["filesystem_mount_point"] = filesystem_mount_point

    @builtins.property
    def hosts(self) -> typing.List["IHost"]:
        """The set of hosts that will be hosting the containers.

        This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.
        """
        result = self._values.get("hosts")
        assert result is not None, "Required property 'hosts' is missing"
        return result

    @builtins.property
    def filesystem_mount_point(self) -> typing.Optional[builtins.str]:
        """The path where the repository file-system is mounted on the container hosts.

        :default: "/mnt/repo"
        """
        result = self._values.get("filesystem_mount_point")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ECSContainerInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ECSDirectConnectProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_instances": "containerInstances",
        "containers": "containers",
    },
)
class ECSDirectConnectProps:
    def __init__(
        self,
        *,
        container_instances: ECSContainerInstanceProps,
        containers: "ECSTaskProps",
    ) -> None:
        """The properties used to configure Deadline running in an Amazon EC2 ECS task to directly connect to the repository.

        :param container_instances: Configuration of ECS host instances to permit connecting hosted ECS tasks to the repository.
        :param containers: Configuration to directly connect an ECS task to the repository.
        """
        if isinstance(container_instances, dict):
            container_instances = ECSContainerInstanceProps(**container_instances)
        if isinstance(containers, dict):
            containers = ECSTaskProps(**containers)
        self._values: typing.Dict[str, typing.Any] = {
            "container_instances": container_instances,
            "containers": containers,
        }

    @builtins.property
    def container_instances(self) -> ECSContainerInstanceProps:
        """Configuration of ECS host instances to permit connecting hosted ECS tasks to the repository."""
        result = self._values.get("container_instances")
        assert result is not None, "Required property 'container_instances' is missing"
        return result

    @builtins.property
    def containers(self) -> "ECSTaskProps":
        """Configuration to directly connect an ECS task to the repository."""
        result = self._values.get("containers")
        assert result is not None, "Required property 'containers' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ECSDirectConnectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ECSTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "task_definition": "taskDefinition",
        "filesystem_mount_point": "filesystemMountPoint",
    },
)
class ECSTaskProps:
    def __init__(
        self,
        *,
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        filesystem_mount_point: typing.Optional[builtins.str] = None,
    ) -> None:
        """Configuration interface to directly connect an ECS task to the repository.

        :param task_definition: The task definition to connect to the repository. [disable-awslint:ref-via-interface]
        :param filesystem_mount_point: The path where the repository file-system is mounted within the container. Default: "/opt/Thinkbox/DeadlineRepository{MAJOR_VER}"
        """
        self._values: typing.Dict[str, typing.Any] = {
            "task_definition": task_definition,
        }
        if filesystem_mount_point is not None:
            self._values["filesystem_mount_point"] = filesystem_mount_point

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """The task definition to connect to the repository.

        [disable-awslint:ref-via-interface]
        """
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return result

    @builtins.property
    def filesystem_mount_point(self) -> typing.Optional[builtins.str]:
        """The path where the repository file-system is mounted within the container.

        :default: "/opt/Thinkbox/DeadlineRepository{MAJOR_VER}"
        """
        result = self._values.get("filesystem_mount_point")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ECSTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-rfdk.deadline.IContainerDirectRepositoryConnection")
class IContainerDirectRepositoryConnection(typing_extensions.Protocol):
    """Interface that can be used to configure a {@link @aws-cdk/aws-ecs#ContainerDefinition} definition to directly connect to the repository."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IContainerDirectRepositoryConnectionProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="containerEnvironment")
    def container_environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        """Environment variables that configure a direct connection to the repository."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="readOnlyMountPoint")
    def read_only_mount_point(self) -> aws_cdk.aws_ecs.MountPoint:
        """A {@link MountPoint} that can be used to create a read/write mount the repository file-system from the task's container instance into a container.

        This can be used with the ``addMountPoint`` method of the
        {@link @aws-cdk/aws-ecs#ContainerDefinition} instance.
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="readWriteMountPoint")
    def read_write_mount_point(self) -> aws_cdk.aws_ecs.MountPoint:
        """A {@link MountPoint} that can be used to create a read/write mount the repository file-system from the task's container instance into a container.

        This can be used with the ``addMountPoint`` method of the
        {@link @aws-cdk/aws-ecs#ContainerDefinition} instance.
        """
        ...


class _IContainerDirectRepositoryConnectionProxy:
    """Interface that can be used to configure a {@link @aws-cdk/aws-ecs#ContainerDefinition} definition to directly connect to the repository."""

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IContainerDirectRepositoryConnection"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="containerEnvironment")
    def container_environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        """Environment variables that configure a direct connection to the repository."""
        return jsii.get(self, "containerEnvironment")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="readOnlyMountPoint")
    def read_only_mount_point(self) -> aws_cdk.aws_ecs.MountPoint:
        """A {@link MountPoint} that can be used to create a read/write mount the repository file-system from the task's container instance into a container.

        This can be used with the ``addMountPoint`` method of the
        {@link @aws-cdk/aws-ecs#ContainerDefinition} instance.
        """
        return jsii.get(self, "readOnlyMountPoint")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="readWriteMountPoint")
    def read_write_mount_point(self) -> aws_cdk.aws_ecs.MountPoint:
        """A {@link MountPoint} that can be used to create a read/write mount the repository file-system from the task's container instance into a container.

        This can be used with the ``addMountPoint`` method of the
        {@link @aws-cdk/aws-ecs#ContainerDefinition} instance.
        """
        return jsii.get(self, "readWriteMountPoint")


@jsii.interface(jsii_type="aws-rfdk.deadline.IHost")
class IHost(
    aws_cdk.aws_ec2.IConnectable,
    aws_cdk.core.IConstruct,
    _IScriptHost_ad38c9ad,
    typing_extensions.Protocol,
):
    """Interface for any constructs that are Capable of connecting to Deadline."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IHostProxy


class _IHostProxy(
    jsii.proxy_for(aws_cdk.aws_ec2.IConnectable), # type: ignore
    jsii.proxy_for(aws_cdk.core.IConstruct), # type: ignore
    jsii.proxy_for(_IScriptHost_ad38c9ad), # type: ignore
):
    """Interface for any constructs that are Capable of connecting to Deadline."""

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IHost"
    pass


@jsii.interface(jsii_type="aws-rfdk.deadline.IInstanceUserDataProvider")
class IInstanceUserDataProvider(typing_extensions.Protocol):
    """Provider for adding user data scripts Methods of this interface will be invoked in WorkerInstanceConfiguration on different stages of worker configuration."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IInstanceUserDataProviderProxy

    @jsii.member(jsii_name="postWorkerLaunch")
    def post_worker_launch(self, host: IHost) -> None:
        """Method that is invoked after all configuration is done and worker started.

        :param host: -
        """
        ...

    @jsii.member(jsii_name="preCloudWatchAgent")
    def pre_cloud_watch_agent(self, host: IHost) -> None:
        """Method that is invoked before configuring the Cloud Watch Agent.

        :param host: -
        """
        ...

    @jsii.member(jsii_name="preRenderQueueConfiguration")
    def pre_render_queue_configuration(self, host: IHost) -> None:
        """Method that is invoked before the render queue configuration.

        :param host: -
        """
        ...

    @jsii.member(jsii_name="preWorkerConfiguration")
    def pre_worker_configuration(self, host: IHost) -> None:
        """Method that is invoked after configuring the connection to the render queue and before configuring the Deadline Worker.

        :param host: -
        """
        ...


class _IInstanceUserDataProviderProxy:
    """Provider for adding user data scripts Methods of this interface will be invoked in WorkerInstanceConfiguration on different stages of worker configuration."""

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IInstanceUserDataProvider"

    @jsii.member(jsii_name="postWorkerLaunch")
    def post_worker_launch(self, host: IHost) -> None:
        """Method that is invoked after all configuration is done and worker started.

        :param host: -
        """
        return jsii.invoke(self, "postWorkerLaunch", [host])

    @jsii.member(jsii_name="preCloudWatchAgent")
    def pre_cloud_watch_agent(self, host: IHost) -> None:
        """Method that is invoked before configuring the Cloud Watch Agent.

        :param host: -
        """
        return jsii.invoke(self, "preCloudWatchAgent", [host])

    @jsii.member(jsii_name="preRenderQueueConfiguration")
    def pre_render_queue_configuration(self, host: IHost) -> None:
        """Method that is invoked before the render queue configuration.

        :param host: -
        """
        return jsii.invoke(self, "preRenderQueueConfiguration", [host])

    @jsii.member(jsii_name="preWorkerConfiguration")
    def pre_worker_configuration(self, host: IHost) -> None:
        """Method that is invoked after configuring the connection to the render queue and before configuring the Deadline Worker.

        :param host: -
        """
        return jsii.invoke(self, "preWorkerConfiguration", [host])


@jsii.interface(jsii_type="aws-rfdk.deadline.IReleaseVersion")
class IReleaseVersion(typing_extensions.Protocol):
    """Represents a release of Deadline up to and including the third (release) component of the version.

    E.g. 10.1.9
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IReleaseVersionProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="majorVersion")
    def major_version(self) -> jsii.Number:
        """The major version number."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="minorVersion")
    def minor_version(self) -> jsii.Number:
        """The minor version number."""
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> jsii.Number:
        """The release version number."""
        ...


class _IReleaseVersionProxy:
    """Represents a release of Deadline up to and including the third (release) component of the version.

    E.g. 10.1.9
    """

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IReleaseVersion"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="majorVersion")
    def major_version(self) -> jsii.Number:
        """The major version number."""
        return jsii.get(self, "majorVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="minorVersion")
    def minor_version(self) -> jsii.Number:
        """The minor version number."""
        return jsii.get(self, "minorVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> jsii.Number:
        """The release version number."""
        return jsii.get(self, "releaseVersion")


@jsii.interface(jsii_type="aws-rfdk.deadline.IRenderQueue")
class IRenderQueue(
    aws_cdk.core.IConstruct,
    aws_cdk.aws_ec2.IConnectable,
    typing_extensions.Protocol,
):
    """Interface for Deadline Render Queue."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRenderQueueProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> _ConnectableApplicationEndpoint_075040da:
        """The endpoint used to connect to the Render Queue."""
        ...

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        grantee: aws_cdk.aws_iam.IGrantable,
        hosts: typing.List[IHost],
    ) -> typing.Mapping[builtins.str, builtins.str]:
        """Configures an ECS cluster to be able to connect to a RenderQueue.

        :param grantee: The task definitions Role that needs permissions.
        :param hosts: The set of hosts that will be hosting the containers. This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.

        :return: An environment mapping that is used to configure the Docker Images
        """
        ...

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(self, *, host: IHost) -> None:
        """Configure an Instance/Autoscaling group to connect to a RenderQueue.

        :param host: The Instance/UserData which will directly connect to the Repository.
        """
        ...


class _IRenderQueueProxy(
    jsii.proxy_for(aws_cdk.core.IConstruct), # type: ignore
    jsii.proxy_for(aws_cdk.aws_ec2.IConnectable), # type: ignore
):
    """Interface for Deadline Render Queue."""

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IRenderQueue"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> _ConnectableApplicationEndpoint_075040da:
        """The endpoint used to connect to the Render Queue."""
        return jsii.get(self, "endpoint")

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        grantee: aws_cdk.aws_iam.IGrantable,
        hosts: typing.List[IHost],
    ) -> typing.Mapping[builtins.str, builtins.str]:
        """Configures an ECS cluster to be able to connect to a RenderQueue.

        :param grantee: The task definitions Role that needs permissions.
        :param hosts: The set of hosts that will be hosting the containers. This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.

        :return: An environment mapping that is used to configure the Docker Images
        """
        params = ECSConnectOptions(grantee=grantee, hosts=hosts)

        return jsii.invoke(self, "configureClientECS", [params])

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(self, *, host: IHost) -> None:
        """Configure an Instance/Autoscaling group to connect to a RenderQueue.

        :param host: The Instance/UserData which will directly connect to the Repository.
        """
        params = InstanceConnectOptions(host=host)

        return jsii.invoke(self, "configureClientInstance", [params])


@jsii.interface(jsii_type="aws-rfdk.deadline.IRepository")
class IRepository(aws_cdk.core.IConstruct, typing_extensions.Protocol):
    """Interface for Deadline Repository."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRepositoryProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rootPrefix")
    def root_prefix(self) -> builtins.str:
        """The path to the Deadline Repository directory.

        This is expressed as a relative path from the root of the Deadline Repository file-system.
        """
        ...

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> "IVersion":
        """The version of Deadline for Linux that is installed on this Repository."""
        ...

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        container_instances: ECSContainerInstanceProps,
        containers: ECSTaskProps,
    ) -> IContainerDirectRepositoryConnection:
        """Configures an ECS Container Instance and Task Definition for deploying a Deadline Client that directly connects to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData

        :param container_instances: Configuration of ECS host instances to permit connecting hosted ECS tasks to the repository.
        :param containers: Configuration to directly connect an ECS task to the repository.

        :return: A mapping of environment variable names and their values to set in the container
        """
        ...

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(
        self,
        *,
        host: IHost,
        mount_point: builtins.str,
    ) -> None:
        """Configure a Deadline Client, that is running in an Amazon EC2 instance, for direct connection to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData
        - Configures Deadline to direct-connect to the Repository.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param mount_point: The location where the Repositories file system will be mounted on the instance.
        """
        ...


class _IRepositoryProxy(
    jsii.proxy_for(aws_cdk.core.IConstruct) # type: ignore
):
    """Interface for Deadline Repository."""

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IRepository"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rootPrefix")
    def root_prefix(self) -> builtins.str:
        """The path to the Deadline Repository directory.

        This is expressed as a relative path from the root of the Deadline Repository file-system.
        """
        return jsii.get(self, "rootPrefix")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> "IVersion":
        """The version of Deadline for Linux that is installed on this Repository."""
        return jsii.get(self, "version")

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        container_instances: ECSContainerInstanceProps,
        containers: ECSTaskProps,
    ) -> IContainerDirectRepositoryConnection:
        """Configures an ECS Container Instance and Task Definition for deploying a Deadline Client that directly connects to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData

        :param container_instances: Configuration of ECS host instances to permit connecting hosted ECS tasks to the repository.
        :param containers: Configuration to directly connect an ECS task to the repository.

        :return: A mapping of environment variable names and their values to set in the container
        """
        props = ECSDirectConnectProps(
            container_instances=container_instances, containers=containers
        )

        return jsii.invoke(self, "configureClientECS", [props])

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(
        self,
        *,
        host: IHost,
        mount_point: builtins.str,
    ) -> None:
        """Configure a Deadline Client, that is running in an Amazon EC2 instance, for direct connection to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData
        - Configures Deadline to direct-connect to the Repository.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param mount_point: The location where the Repositories file system will be mounted on the instance.
        """
        props = InstanceDirectConnectProps(host=host, mount_point=mount_point)

        return jsii.invoke(self, "configureClientInstance", [props])


@jsii.interface(jsii_type="aws-rfdk.deadline.IVersion")
class IVersion(IReleaseVersion, typing_extensions.Protocol):
    """This interface represents a deadline version.

    It contains the
    major, minor, and release numbers essential to identify
    a version. It also includes the S3 path of the installers.

    The Deadline version tag consists of four numbers:
    Major.Minor.Release.Patch
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IVersionProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="linuxInstallers")
    def linux_installers(self) -> "PlatformInstallers":
        """The Linux installers for this version.

        :default: No installers for Linux are provided.
        """
        ...

    @jsii.member(jsii_name="linuxFullVersionString")
    def linux_full_version_string(self) -> builtins.str:
        """Construct the full version string for the linux patch release referenced in this version object.

        This is constructed by joining the major, minor,
        release, and patch versions by dots.
        """
        ...


class _IVersionProxy(
    jsii.proxy_for(IReleaseVersion) # type: ignore
):
    """This interface represents a deadline version.

    It contains the
    major, minor, and release numbers essential to identify
    a version. It also includes the S3 path of the installers.

    The Deadline version tag consists of four numbers:
    Major.Minor.Release.Patch
    """

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IVersion"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="linuxInstallers")
    def linux_installers(self) -> "PlatformInstallers":
        """The Linux installers for this version.

        :default: No installers for Linux are provided.
        """
        return jsii.get(self, "linuxInstallers")

    @jsii.member(jsii_name="linuxFullVersionString")
    def linux_full_version_string(self) -> builtins.str:
        """Construct the full version string for the linux patch release referenced in this version object.

        This is constructed by joining the major, minor,
        release, and patch versions by dots.
        """
        return jsii.invoke(self, "linuxFullVersionString", [])


@jsii.interface(jsii_type="aws-rfdk.deadline.IWorkerFleet")
class IWorkerFleet(
    aws_cdk.core.IResource,
    aws_cdk.aws_ec2.IConnectable,
    aws_cdk.aws_iam.IGrantable,
    typing_extensions.Protocol,
):
    """Interface for Deadline Worker Fleet."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IWorkerFleetProxy


class _IWorkerFleetProxy(
    jsii.proxy_for(aws_cdk.core.IResource), # type: ignore
    jsii.proxy_for(aws_cdk.aws_ec2.IConnectable), # type: ignore
    jsii.proxy_for(aws_cdk.aws_iam.IGrantable), # type: ignore
):
    """Interface for Deadline Worker Fleet."""

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IWorkerFleet"
    pass


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.Installer",
    jsii_struct_bases=[],
    name_mapping={"object_key": "objectKey", "s3_bucket": "s3Bucket"},
)
class Installer:
    def __init__(
        self,
        *,
        object_key: builtins.str,
        s3_bucket: aws_cdk.aws_s3.IBucket,
    ) -> None:
        """This interface represents a deadline installer object stored on an S3 bucket.

        :param object_key: The object key where the installer file is located.
        :param s3_bucket: The S3 Bucket interface where the installer is located.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "object_key": object_key,
            "s3_bucket": s3_bucket,
        }

    @builtins.property
    def object_key(self) -> builtins.str:
        """The object key where the installer file is located."""
        result = self._values.get("object_key")
        assert result is not None, "Required property 'object_key' is missing"
        return result

    @builtins.property
    def s3_bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The S3 Bucket interface where the installer is located."""
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Installer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.InstanceConnectOptions",
    jsii_struct_bases=[],
    name_mapping={"host": "host"},
)
class InstanceConnectOptions:
    def __init__(self, *, host: IHost) -> None:
        """Properties that need to be provided in order to connect instances to a Render Queue.

        :param host: The Instance/UserData which will directly connect to the Repository.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "host": host,
        }

    @builtins.property
    def host(self) -> IHost:
        """The Instance/UserData which will directly connect to the Repository."""
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceConnectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.InstanceDirectConnectProps",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "mount_point": "mountPoint"},
)
class InstanceDirectConnectProps:
    def __init__(self, *, host: IHost, mount_point: builtins.str) -> None:
        """The Properties used to configure Deadline, that is running in an Amazon EC2 instance, a direct connection with a repository.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param mount_point: The location where the Repositories file system will be mounted on the instance.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "host": host,
            "mount_point": mount_point,
        }

    @builtins.property
    def host(self) -> IHost:
        """The Instance/UserData which will directly connect to the Repository."""
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return result

    @builtins.property
    def mount_point(self) -> builtins.str:
        """The location where the Repositories file system will be mounted on the instance."""
        result = self._values.get("mount_point")
        assert result is not None, "Required property 'mount_point' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceDirectConnectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IInstanceUserDataProvider)
class InstanceUserDataProvider(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.InstanceUserDataProvider",
):
    """Implementation of {@link IInstanceUserDataProvider}.

    Can be used as sub-class with override the desired methods
    to add custom user data commands for WorkerInstanceFleet or WorkerInstanceConfiguration.
    """

    def __init__(self, scope: aws_cdk.core.Construct, id: builtins.str) -> None:
        """
        :param scope: -
        :param id: -
        """
        jsii.create(InstanceUserDataProvider, self, [scope, id])

    @jsii.member(jsii_name="postWorkerLaunch")
    def post_worker_launch(self, _host: IHost) -> None:
        """Method that is invoked after all configuration is done and worker started.

        :param _host: -

        :inheritdoc: true
        """
        return jsii.invoke(self, "postWorkerLaunch", [_host])

    @jsii.member(jsii_name="preCloudWatchAgent")
    def pre_cloud_watch_agent(self, _host: IHost) -> None:
        """Method that is invoked before configuring the Cloud Watch Agent.

        :param _host: -

        :inheritdoc: true
        """
        return jsii.invoke(self, "preCloudWatchAgent", [_host])

    @jsii.member(jsii_name="preRenderQueueConfiguration")
    def pre_render_queue_configuration(self, _host: IHost) -> None:
        """Method that is invoked before the render queue configuration.

        :param _host: -

        :inheritdoc: true
        """
        return jsii.invoke(self, "preRenderQueueConfiguration", [_host])

    @jsii.member(jsii_name="preWorkerConfiguration")
    def pre_worker_configuration(self, _host: IHost) -> None:
        """Method that is invoked after configuring the connection to the render queue and before configuring the Deadline Worker.

        :param _host: -

        :inheritdoc: true
        """
        return jsii.invoke(self, "preWorkerConfiguration", [_host])


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.Manifest",
    jsii_struct_bases=[],
    name_mapping={"recipes": "recipes", "schema": "schema", "version": "version"},
)
class Manifest:
    def __init__(
        self,
        *,
        recipes: DeadlineDockerRecipes,
        schema: jsii.Number,
        version: builtins.str,
    ) -> None:
        """The manifest included with Deadline Docker image recipes.

        :param recipes: The recipes.
        :param schema: The manifest schema version number.
        :param version: The version of Deadline that the staging directory contains.
        """
        if isinstance(recipes, dict):
            recipes = DeadlineDockerRecipes(**recipes)
        self._values: typing.Dict[str, typing.Any] = {
            "recipes": recipes,
            "schema": schema,
            "version": version,
        }

    @builtins.property
    def recipes(self) -> DeadlineDockerRecipes:
        """The recipes."""
        result = self._values.get("recipes")
        assert result is not None, "Required property 'recipes' is missing"
        return result

    @builtins.property
    def schema(self) -> jsii.Number:
        """The manifest schema version number."""
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return result

    @builtins.property
    def version(self) -> builtins.str:
        """The version of Deadline that the staging directory contains."""
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Manifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.MongoDbInstanceConnectionOptions",
    jsii_struct_bases=[],
    name_mapping={"client_certificate": "clientCertificate", "database": "database"},
)
class MongoDbInstanceConnectionOptions:
    def __init__(
        self,
        *,
        client_certificate: _IX509CertificatePkcs12_63b2574c,
        database: _IMongoDb_dbee748a,
    ) -> None:
        """
        :param client_certificate: The client certificate to register in the database during install of the Deadline Repository, and for the Deadline Client to use to connect to the database. This **MUST** be signed by the same signing certificate as the MongoDB server's certificate. Note: A limitation of Deadline **requires** that this certificate be signed directly by your root certificate authority (CA). Deadline will be unable to connect to MongoDB if it has been signed by an intermediate CA.
        :param database: The MongoDB database to connect to. Note: Deadline officially supports only databases that are compatible with MongoDB 3.6.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "client_certificate": client_certificate,
            "database": database,
        }

    @builtins.property
    def client_certificate(self) -> _IX509CertificatePkcs12_63b2574c:
        """The client certificate to register in the database during install of the Deadline Repository, and for the Deadline Client to use to connect to the database.

        This **MUST** be signed by the same signing certificate as the MongoDB server's certificate.

        Note: A limitation of Deadline **requires** that this certificate be signed directly by your root certificate authority (CA).
        Deadline will be unable to connect to MongoDB if it has been signed by an intermediate CA.
        """
        result = self._values.get("client_certificate")
        assert result is not None, "Required property 'client_certificate' is missing"
        return result

    @builtins.property
    def database(self) -> _IMongoDb_dbee748a:
        """The MongoDB database to connect to.

        Note: Deadline officially supports only databases that are compatible with MongoDB 3.6.
        """
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MongoDbInstanceConnectionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.PlatformInstallers",
    jsii_struct_bases=[],
    name_mapping={"patch_version": "patchVersion", "repository": "repository"},
)
class PlatformInstallers:
    def __init__(self, *, patch_version: jsii.Number, repository: Installer) -> None:
        """This interface represents a collection of Deadline installer files for a specific Deadline version stored in S3.

        :param patch_version: The patch version for these Deadline installers. ex: If the installer is for version 10.1.8.5, then this will be 5.
        :param repository: The Deadline Repository installer for this platform, as extracted from the bundle on the Thinkbox download site. For example:. - DeadlineRepository-10.1.8.5-linux-x64-installer.run - DeadlineRepository-10.1.8.5-windows-installer.exe
        """
        if isinstance(repository, dict):
            repository = Installer(**repository)
        self._values: typing.Dict[str, typing.Any] = {
            "patch_version": patch_version,
            "repository": repository,
        }

    @builtins.property
    def patch_version(self) -> jsii.Number:
        """The patch version for these Deadline installers.

        ex: If the installer is for version 10.1.8.5, then this will be 5.
        """
        result = self._values.get("patch_version")
        assert result is not None, "Required property 'patch_version' is missing"
        return result

    @builtins.property
    def repository(self) -> Installer:
        """The Deadline Repository installer for this platform, as extracted from the bundle on the Thinkbox download site. For example:.

        - DeadlineRepository-10.1.8.5-linux-x64-installer.run
        - DeadlineRepository-10.1.8.5-windows-installer.exe
        """
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlatformInstallers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.Recipe",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "title": "title",
        "build_args": "buildArgs",
        "target": "target",
    },
)
class Recipe:
    def __init__(
        self,
        *,
        description: builtins.str,
        title: builtins.str,
        build_args: typing.Optional[BuildArgs] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        """Docker container image recipe.

        :param description: Description of the recipe.
        :param title: Title of the recipe.
        :param build_args: The Docker build arguments for the recipe. Default: No build arguments are supplied
        :param target: Optional target for a Docker multi-stage build. Default: The last stage in the Dockerfile is used
        """
        if isinstance(build_args, dict):
            build_args = BuildArgs(**build_args)
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "title": title,
        }
        if build_args is not None:
            self._values["build_args"] = build_args
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def description(self) -> builtins.str:
        """Description of the recipe."""
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return result

    @builtins.property
    def title(self) -> builtins.str:
        """Title of the recipe."""
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return result

    @builtins.property
    def build_args(self) -> typing.Optional[BuildArgs]:
        """The Docker build arguments for the recipe.

        :default: No build arguments are supplied
        """
        result = self._values.get("build_args")
        return result

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        """Optional target for a Docker multi-stage build.

        :default: The last stage in the Dockerfile is used
        """
        result = self._values.get("target")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Recipe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_iam.IGrantable, IRenderQueue)
class RenderQueue(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.RenderQueue",
):
    """The RenderQueue construct deploys an Elastic Container Service (ECS) service that serves Deadline's REST HTTP API to Deadline Clients.

    Most Deadline clients will connect to a Deadline render farm via the the RenderQueue. The API provides Deadline
    clients access to Deadline's database and repository file-system in a way that is secure, performant, and scalable.


    Resources Deployed

    - An Amazon Elastic Container Service (ECS) cluster.
    - An AWS EC2 auto-scaling group that provides the instances that host the ECS service.
    - An ECS service with a task definition that deploys the Deadline Remote Connetion Server (RCS) in a container.
    - A Amazon CloudWatch log group for streaming logs from the Deadline RCS.
    - An application load balancer, listener and target group that balance incoming traffic among the RCS containers.



    Security Considerations

    - The instances deployed by this construct download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - Care must be taken to secure what can connect to the RenderQueue. The RenderQueue does not authenticate API
      requests made against it. You must limit access to the RenderQueue endpoint to only trusted hosts. Those hosts
      should be governed carefully, as malicious software could use the API to remotely execute code across the entire render farm.
    - The RenderQueue can be deployed with network encryption through Transport Layer Security (TLS) or without it. Unencrypted
      network communications can be eavesdropped upon or modified in transit. We strongly recommend deploying the RenderQueue
      with TLS enabled in production environments.
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        images: "RenderQueueImages",
        repository: IRepository,
        version: IVersion,
        vpc: aws_cdk.aws_ec2.IVpc,
        access_logs: typing.Optional["RenderQueueAccessLogProps"] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        health_check_config: typing.Optional["RenderQueueHealthCheckConfiguration"] = None,
        hostname: typing.Optional["RenderQueueHostNameProps"] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        log_group_props: typing.Optional[_LogGroupFactoryProps_b817ed21] = None,
        render_queue_size: typing.Optional["RenderQueueSizeConstraints"] = None,
        traffic_encryption: typing.Optional["RenderQueueTrafficEncryptionProps"] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param images: A collection of Docker container images used to run the RenderQueue.
        :param repository: The Deadline Repository which the RCS instances will create a direct connection to.
        :param version: The Deadline Client version that will be running within this RenderQueue.
        :param vpc: VPC to launch the Render Queue in.
        :param access_logs: Properties for configuring access logging for the load balancer used by the Render Queue. This is disabled by default, but it is highly recommended to enable it to allow engineers to identify and root cause incidents such as unauthorized access. Default: - Access logging is disabled
        :param deletion_protection: Indicates whether deletion protection is enabled for the LoadBalancer. Default: true Note: This value is true by default which means that the deletion protection is enabled for the load balancer. Hence, user needs to disable it using AWS Console or CLI before deleting the stack.
        :param health_check_config: Configuration for the health checks performed by the RenderQueue upon the Deadline RCS. Default: The values outlined in {@link RenderQueueHealthCheckConfiguration}
        :param hostname: Hostname to use to connect to the RenderQueue. Default: A hostname is generated by the Application Load Balancer that fronts the RenderQueue.
        :param instance_type: The type of instance on which each Deadline RCS will run. Default: c5.Large instances will be launched.
        :param log_group_props: Properties for setting up the Render Queue's LogGroup. Default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        :param render_queue_size: Constraints on the number of Deadline RCS processes that can be run as part of this RenderQueue. Default: Allow no more and no less than one Deadline RCS to be running.
        :param traffic_encryption: Whether or not network traffic to the RenderQueue should be encrypted. Enabling this requires that all Deadline clients connect with TLS. Default: traffic is encrypted between Clients and the Render Queue and between its components
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        """
        props = RenderQueueProps(
            images=images,
            repository=repository,
            version=version,
            vpc=vpc,
            access_logs=access_logs,
            deletion_protection=deletion_protection,
            health_check_config=health_check_config,
            hostname=hostname,
            instance_type=instance_type,
            log_group_props=log_group_props,
            render_queue_size=render_queue_size,
            traffic_encryption=traffic_encryption,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(RenderQueue, self, [scope, id, props])

    @jsii.member(jsii_name="addChildDependency")
    def add_child_dependency(self, child: aws_cdk.core.IConstruct) -> None:
        """Add an ordering dependency to another Construct.

        All constructs in the child's scope will be deployed after the RenderQueue has been deployed and is ready to recieve traffic.

        This can be used to ensure that the RenderQueue is fully up and serving queries before a client attempts to connect to it.

        :param child: The child to make dependent upon this RenderQueue.
        """
        return jsii.invoke(self, "addChildDependency", [child])

    @jsii.member(jsii_name="addSEPPolicies")
    def add_sep_policies(
        self,
        include_resource_tracker: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Adds AWS Managed Policies to the Render Queue so it is able to control Deadlines Spot Event Plugin.

        See: https://docs.thinkboxsoftware.com/products/deadline/10.1/1_User%20Manual/manual/event-spot.html for additonal information.

        :param include_resource_tracker: Whether or not the Resource tracker admin policy should also be addd (Default: True).
        """
        return jsii.invoke(self, "addSEPPolicies", [include_resource_tracker])

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        grantee: aws_cdk.aws_iam.IGrantable,
        hosts: typing.List[IHost],
    ) -> typing.Mapping[builtins.str, builtins.str]:
        """Configures an ECS cluster to be able to connect to a RenderQueue.

        :param grantee: The task definitions Role that needs permissions.
        :param hosts: The set of hosts that will be hosting the containers. This can be AutoScalingGroups that make up the capacity of an Amazon ECS cluster, or individual instances.

        :inheritdoc: true
        """
        param = ECSConnectOptions(grantee=grantee, hosts=hosts)

        return jsii.invoke(self, "configureClientECS", [param])

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(self, *, host: IHost) -> None:
        """Configure an Instance/Autoscaling group to connect to a RenderQueue.

        :param host: The Instance/UserData which will directly connect to the Repository.

        :inheritdoc: true
        """
        param = InstanceConnectOptions(host=host)

        return jsii.invoke(self, "configureClientInstance", [param])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="asg")
    def asg(self) -> aws_cdk.aws_autoscaling.AutoScalingGroup:
        """The Amazon EC2 Auto Scaling Group within the {@link RenderQueue.cluster} that contains the Deadline RCS's instances."""
        return jsii.get(self, "asg")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.Cluster:
        """The Amazon ECS cluster that is hosting the fleet of Deadline RCS applications."""
        return jsii.get(self, "cluster")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Allows specifying security group connections for the Render Queue.

        :inheritdoc: true
        """
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> _ConnectableApplicationEndpoint_075040da:
        """The endpoint that Deadline clients can use to connect to the Render Queue.

        :inheritdoc: true
        """
        return jsii.get(self, "endpoint")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer:
        """The application load balancer that serves the traffic."""
        return jsii.get(self, "loadBalancer")


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueAccessLogProps",
    jsii_struct_bases=[],
    name_mapping={"destination_bucket": "destinationBucket", "prefix": "prefix"},
)
class RenderQueueAccessLogProps:
    def __init__(
        self,
        *,
        destination_bucket: aws_cdk.aws_s3.IBucket,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for enabling access logs for the Render Queue's load balancer.

        See
        https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html
        for more information on what gets logged and how to access them.

        :param destination_bucket: The S3 Bucket that the access logs should be stored in. It is recommended to set a lifecycle rule on this Bucket to avoid having it grow indefinitely. Costs will be incurred for requests made to put logs in the Bucket as well as storage.
        :param prefix: The prefix to be used for the access logs when they are stored in S3. Default: None
        """
        self._values: typing.Dict[str, typing.Any] = {
            "destination_bucket": destination_bucket,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def destination_bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The S3 Bucket that the access logs should be stored in.

        It is recommended to set a lifecycle rule on
        this Bucket to avoid having it grow indefinitely. Costs will be incurred for
        requests made to put logs in the Bucket as well as storage.
        """
        result = self._values.get("destination_bucket")
        assert result is not None, "Required property 'destination_bucket' is missing"
        return result

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        """The prefix to be used for the access logs when they are stored in S3.

        :default: None
        """
        result = self._values.get("prefix")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueAccessLogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueExternalTLSProps",
    jsii_struct_bases=[],
    name_mapping={
        "acm_certificate": "acmCertificate",
        "acm_certificate_chain": "acmCertificateChain",
        "rfdk_certificate": "rfdkCertificate",
    },
)
class RenderQueueExternalTLSProps:
    def __init__(
        self,
        *,
        acm_certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
        acm_certificate_chain: typing.Optional[aws_cdk.aws_secretsmanager.ISecret] = None,
        rfdk_certificate: typing.Optional[_IX509CertificatePem_da3ef30f] = None,
    ) -> None:
        """Properties for configuring external TLS connections between the Render Queue and Deadline clients.

        You must provide one of the following combinations of properties:

        - acmCertificate ({@link @aws-cdk/aws-certificatemanager#ICertificate}) representing a certificate in ACM and
          acmCertificateChain ({@link @aws-cdk/aws-secretsmanager#ISecret}) containing the Certificate chain of the acmCertificate.
        - rfdkCertificate ({@link IX509CertificatePem}) Representing all of the properties of the certificate.

        In both cases the certificate chain **must** include only the CA certificates PEM file due to a known limitation in Deadline.

        :param acm_certificate: The ACM certificate that will be used for establishing incoming external TLS connections to the RenderQueue. Default: If not provided then the rfdkCertificate must be provided.
        :param acm_certificate_chain: The secret containing the cert chain of the provided acmCert. This certifiate chain **must** include only the CA Certificates PEM file. Default: If an acmCertificate was provided then this must be provided, otherwise this is ignored.
        :param rfdk_certificate: The parameters for an X509 Certificate that will be imported into ACM then used by the RenderQueue. Default: If not provided then an acmCertificate and acmCertificateChain must be provided.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if acm_certificate is not None:
            self._values["acm_certificate"] = acm_certificate
        if acm_certificate_chain is not None:
            self._values["acm_certificate_chain"] = acm_certificate_chain
        if rfdk_certificate is not None:
            self._values["rfdk_certificate"] = rfdk_certificate

    @builtins.property
    def acm_certificate(
        self,
    ) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """The ACM certificate that will be used for establishing incoming external TLS connections to the RenderQueue.

        :default: If  not provided then the rfdkCertificate must be provided.
        """
        result = self._values.get("acm_certificate")
        return result

    @builtins.property
    def acm_certificate_chain(
        self,
    ) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secret containing the cert chain of the provided acmCert.

        This certifiate chain **must** include only the CA Certificates PEM file.

        :default: If an acmCertificate was provided then this must be provided, otherwise this is ignored.
        """
        result = self._values.get("acm_certificate_chain")
        return result

    @builtins.property
    def rfdk_certificate(self) -> typing.Optional[_IX509CertificatePem_da3ef30f]:
        """The parameters for an X509 Certificate that will be imported into ACM then used by the RenderQueue.

        :default: If not provided then an acmCertificate and acmCertificateChain must be provided.
        """
        result = self._values.get("rfdk_certificate")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueExternalTLSProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueHealthCheckConfiguration",
    jsii_struct_bases=[],
    name_mapping={"check_interval": "checkInterval", "grace_period": "gracePeriod"},
)
class RenderQueueHealthCheckConfiguration:
    def __init__(
        self,
        *,
        check_interval: typing.Optional[aws_cdk.core.Duration] = None,
        grace_period: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Configuration for the health checks performed by the RenderQueue upon the Deadline RCS.

        These health checks periodically query the Deadline RCS to ensure that it is still operating
        nominally. If a Deadline RCS is found to not be operating nominally, then it will be terminated
        and automatically replaced.

        Please see {@link https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html}
        for additional information on this style of health check.

        :param check_interval: The approximate amount of time between health checks for an individual RCS instance. The value provided must be between 5 and 300 seconds. Default: 1 Minute
        :param grace_period: The startup duration where we will not perform health checks on newly created RCS instances. This should be at least a little longer than the time it takes for the Deadline RCS to start up. Default: 5 Minutes
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if check_interval is not None:
            self._values["check_interval"] = check_interval
        if grace_period is not None:
            self._values["grace_period"] = grace_period

    @builtins.property
    def check_interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The approximate amount of time between health checks for an individual RCS instance.

        The value provided must be between 5 and 300 seconds.

        :default: 1 Minute
        """
        result = self._values.get("check_interval")
        return result

    @builtins.property
    def grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The startup duration where we will not perform health checks on newly created RCS instances.

        This should be at least a little longer than the time it takes for the Deadline RCS to start up.

        :default: 5 Minutes
        """
        result = self._values.get("grace_period")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueHealthCheckConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueHostNameProps",
    jsii_struct_bases=[],
    name_mapping={"zone": "zone", "hostname": "hostname"},
)
class RenderQueueHostNameProps:
    def __init__(
        self,
        *,
        zone: aws_cdk.aws_route53.IPrivateHostedZone,
        hostname: typing.Optional[builtins.str] = None,
    ) -> None:
        """Parameters for the generation of a VPC-internal hostname for the RenderQueue.

        :param zone: The private zone to which the DNS A record for the render queue will be added.
        :param hostname: The hostname to assign to the RenderQueue. A valid hostname is 1 to 63 characters long and may only contain: - letters from A-Z - digits from 0 to 9 - the hyphen (-) It must start with a letter and end with a letter or digit. Default: "renderqueue"
        """
        self._values: typing.Dict[str, typing.Any] = {
            "zone": zone,
        }
        if hostname is not None:
            self._values["hostname"] = hostname

    @builtins.property
    def zone(self) -> aws_cdk.aws_route53.IPrivateHostedZone:
        """The private zone to which the DNS A record for the render queue will be added."""
        result = self._values.get("zone")
        assert result is not None, "Required property 'zone' is missing"
        return result

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        """The hostname to assign to the RenderQueue.

        A valid hostname is 1 to 63 characters long and may only contain:

        - letters from A-Z
        - digits from 0 to 9
        - the hyphen (-)
          It must start with a letter and end with a letter or digit.

        :default: "renderqueue"
        """
        result = self._values.get("hostname")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueHostNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueImages",
    jsii_struct_bases=[],
    name_mapping={"remote_connection_server": "remoteConnectionServer"},
)
class RenderQueueImages:
    def __init__(
        self,
        *,
        remote_connection_server: aws_cdk.aws_ecs.ContainerImage,
    ) -> None:
        """Collection of {@link ContainerImage}s required to deploy the RenderQueue.

        :param remote_connection_server: The AWS ECS container image from which the Deadline RCS will be run. This container **must** implement the same environment variable interface as defined in the official container images provided by AWS-Thinkbox. Note: A future change to the RenderQueue will make this property optional.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "remote_connection_server": remote_connection_server,
        }

    @builtins.property
    def remote_connection_server(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The AWS ECS container image from which the Deadline RCS will be run.

        This container
        **must** implement the same environment variable interface as defined in the official
        container images provided by AWS-Thinkbox.

        Note: A future change to the RenderQueue will make this property optional.
        """
        result = self._values.get("remote_connection_server")
        assert result is not None, "Required property 'remote_connection_server' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueImages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "images": "images",
        "repository": "repository",
        "version": "version",
        "vpc": "vpc",
        "access_logs": "accessLogs",
        "deletion_protection": "deletionProtection",
        "health_check_config": "healthCheckConfig",
        "hostname": "hostname",
        "instance_type": "instanceType",
        "log_group_props": "logGroupProps",
        "render_queue_size": "renderQueueSize",
        "traffic_encryption": "trafficEncryption",
        "vpc_subnets": "vpcSubnets",
    },
)
class RenderQueueProps:
    def __init__(
        self,
        *,
        images: RenderQueueImages,
        repository: IRepository,
        version: IVersion,
        vpc: aws_cdk.aws_ec2.IVpc,
        access_logs: typing.Optional[RenderQueueAccessLogProps] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        health_check_config: typing.Optional[RenderQueueHealthCheckConfiguration] = None,
        hostname: typing.Optional[RenderQueueHostNameProps] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        log_group_props: typing.Optional[_LogGroupFactoryProps_b817ed21] = None,
        render_queue_size: typing.Optional["RenderQueueSizeConstraints"] = None,
        traffic_encryption: typing.Optional["RenderQueueTrafficEncryptionProps"] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Properties for the Render Queue.

        :param images: A collection of Docker container images used to run the RenderQueue.
        :param repository: The Deadline Repository which the RCS instances will create a direct connection to.
        :param version: The Deadline Client version that will be running within this RenderQueue.
        :param vpc: VPC to launch the Render Queue in.
        :param access_logs: Properties for configuring access logging for the load balancer used by the Render Queue. This is disabled by default, but it is highly recommended to enable it to allow engineers to identify and root cause incidents such as unauthorized access. Default: - Access logging is disabled
        :param deletion_protection: Indicates whether deletion protection is enabled for the LoadBalancer. Default: true Note: This value is true by default which means that the deletion protection is enabled for the load balancer. Hence, user needs to disable it using AWS Console or CLI before deleting the stack.
        :param health_check_config: Configuration for the health checks performed by the RenderQueue upon the Deadline RCS. Default: The values outlined in {@link RenderQueueHealthCheckConfiguration}
        :param hostname: Hostname to use to connect to the RenderQueue. Default: A hostname is generated by the Application Load Balancer that fronts the RenderQueue.
        :param instance_type: The type of instance on which each Deadline RCS will run. Default: c5.Large instances will be launched.
        :param log_group_props: Properties for setting up the Render Queue's LogGroup. Default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        :param render_queue_size: Constraints on the number of Deadline RCS processes that can be run as part of this RenderQueue. Default: Allow no more and no less than one Deadline RCS to be running.
        :param traffic_encryption: Whether or not network traffic to the RenderQueue should be encrypted. Enabling this requires that all Deadline clients connect with TLS. Default: traffic is encrypted between Clients and the Render Queue and between its components
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        """
        if isinstance(images, dict):
            images = RenderQueueImages(**images)
        if isinstance(access_logs, dict):
            access_logs = RenderQueueAccessLogProps(**access_logs)
        if isinstance(health_check_config, dict):
            health_check_config = RenderQueueHealthCheckConfiguration(**health_check_config)
        if isinstance(hostname, dict):
            hostname = RenderQueueHostNameProps(**hostname)
        if isinstance(log_group_props, dict):
            log_group_props = _LogGroupFactoryProps_b817ed21(**log_group_props)
        if isinstance(render_queue_size, dict):
            render_queue_size = RenderQueueSizeConstraints(**render_queue_size)
        if isinstance(traffic_encryption, dict):
            traffic_encryption = RenderQueueTrafficEncryptionProps(**traffic_encryption)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "images": images,
            "repository": repository,
            "version": version,
            "vpc": vpc,
        }
        if access_logs is not None:
            self._values["access_logs"] = access_logs
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if health_check_config is not None:
            self._values["health_check_config"] = health_check_config
        if hostname is not None:
            self._values["hostname"] = hostname
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if render_queue_size is not None:
            self._values["render_queue_size"] = render_queue_size
        if traffic_encryption is not None:
            self._values["traffic_encryption"] = traffic_encryption
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def images(self) -> RenderQueueImages:
        """A collection of Docker container images used to run the RenderQueue."""
        result = self._values.get("images")
        assert result is not None, "Required property 'images' is missing"
        return result

    @builtins.property
    def repository(self) -> IRepository:
        """The Deadline Repository which the RCS instances will create a direct connection to."""
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return result

    @builtins.property
    def version(self) -> IVersion:
        """The Deadline Client version that will be running within this RenderQueue."""
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return result

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC to launch the Render Queue in."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def access_logs(self) -> typing.Optional[RenderQueueAccessLogProps]:
        """Properties for configuring access logging for the load balancer used by the Render Queue.

        This is disabled by default, but it is highly recommended to enable it to
        allow engineers to identify and root cause incidents such as unauthorized access.

        :default: - Access logging is disabled
        """
        result = self._values.get("access_logs")
        return result

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        """Indicates whether deletion protection is enabled for the LoadBalancer.

        :default:

        true

        Note: This value is true by default which means that the deletion protection is enabled for the
        load balancer. Hence, user needs to disable it using AWS Console or CLI before deleting the stack.

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#deletion-protection
        """
        result = self._values.get("deletion_protection")
        return result

    @builtins.property
    def health_check_config(
        self,
    ) -> typing.Optional[RenderQueueHealthCheckConfiguration]:
        """Configuration for the health checks performed by the RenderQueue upon the Deadline RCS.

        :default: The values outlined in {@link RenderQueueHealthCheckConfiguration}
        """
        result = self._values.get("health_check_config")
        return result

    @builtins.property
    def hostname(self) -> typing.Optional[RenderQueueHostNameProps]:
        """Hostname to use to connect to the RenderQueue.

        :default: A hostname is generated by the Application Load Balancer that fronts the RenderQueue.
        """
        result = self._values.get("hostname")
        return result

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """The type of instance on which each Deadline RCS will run.

        :default: c5.Large instances will be launched.
        """
        result = self._values.get("instance_type")
        return result

    @builtins.property
    def log_group_props(self) -> typing.Optional[_LogGroupFactoryProps_b817ed21]:
        """Properties for setting up the Render Queue's LogGroup.

        :default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        """
        result = self._values.get("log_group_props")
        return result

    @builtins.property
    def render_queue_size(self) -> typing.Optional["RenderQueueSizeConstraints"]:
        """Constraints on the number of Deadline RCS processes that can be run as part of this RenderQueue.

        :default: Allow no more and no less than one Deadline RCS to be running.
        """
        result = self._values.get("render_queue_size")
        return result

    @builtins.property
    def traffic_encryption(
        self,
    ) -> typing.Optional["RenderQueueTrafficEncryptionProps"]:
        """Whether or not network traffic to the RenderQueue should be encrypted.

        Enabling this requires that all Deadline clients connect with TLS.

        :default: traffic is encrypted between Clients and the Render Queue and between its components
        """
        result = self._values.get("traffic_encryption")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place instances within the VPC.

        :default: - All Private subnets.
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueSizeConstraints",
    jsii_struct_bases=[],
    name_mapping={"desired": "desired", "min": "min"},
)
class RenderQueueSizeConstraints:
    def __init__(
        self,
        *,
        desired: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Constraints on the number of Deadline RCS processes that will be created as part of this RenderQueue.

        The number of processes created will be equal to the desired capacity. Setting the minimum and
        maximum capacity provides constraints for modifying the number of processes dynamically via,
        say, the AWS Console.

        :param desired: The number of Deadline RCS processes that you want to create as part of this RenderQueue. If this is set to a number, every deployment will reset the number of RCS processes to this number. It is recommended to leave this value undefined. Currently, the Deadline RCS does not properly support being horizontally scaled behind a load-balancer. For this reason, the desired number of processes can only be set to 1 currently. Default: The min size.
        :param min: Minimum number of Deadline RCS processes that will serve RenderQueue requests. Currently, the Deadline RCS does not properly support being horizontally scaled behind a load-balancer. For this reason, the minimum can be at most one, otherwise an error is thrown. The minimum that this can value be set to is 1. Default: 1
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if desired is not None:
            self._values["desired"] = desired
        if min is not None:
            self._values["min"] = min

    @builtins.property
    def desired(self) -> typing.Optional[jsii.Number]:
        """The number of Deadline RCS processes that you want to create as part of this RenderQueue.

        If this is set to a number, every deployment will reset the number of RCS processes
        to this number. It is recommended to leave this value undefined.

        Currently, the Deadline RCS does not properly support being horizontally scaled behind a load-balancer. For this
        reason, the desired number of processes can only be set to 1 currently.

        :default: The min size.
        """
        result = self._values.get("desired")
        return result

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        """Minimum number of Deadline RCS processes that will serve RenderQueue requests.

        Currently, the Deadline RCS does not properly support being horizontally scaled behind a load-balancer. For this
        reason, the minimum can be at most one, otherwise an error is thrown.

        The minimum that this can value be set to is 1.

        :default: 1
        """
        result = self._values.get("min")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueSizeConstraints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RenderQueueTrafficEncryptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "external_tls": "externalTLS",
        "internal_protocol": "internalProtocol",
    },
)
class RenderQueueTrafficEncryptionProps:
    def __init__(
        self,
        *,
        external_tls: typing.Optional[RenderQueueExternalTLSProps] = None,
        internal_protocol: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol] = None,
    ) -> None:
        """Interface to specify the protocols used (HTTP vs HTTPS) for communication between the Render Queue and clients and internally between the components of the RenderQueue.

        :param external_tls: Properties for configuring external TLS connections between the Render Queue and Deadline clients. Default: Plain HTTP communication is used
        :param internal_protocol: Whether to encrypt traffic between the Application Load Balancer and its backing services. Default: HTTPS
        """
        if isinstance(external_tls, dict):
            external_tls = RenderQueueExternalTLSProps(**external_tls)
        self._values: typing.Dict[str, typing.Any] = {}
        if external_tls is not None:
            self._values["external_tls"] = external_tls
        if internal_protocol is not None:
            self._values["internal_protocol"] = internal_protocol

    @builtins.property
    def external_tls(self) -> typing.Optional[RenderQueueExternalTLSProps]:
        """Properties for configuring external TLS connections between the Render Queue and Deadline clients.

        :default: Plain HTTP communication is used
        """
        result = self._values.get("external_tls")
        return result

    @builtins.property
    def internal_protocol(
        self,
    ) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]:
        """Whether to encrypt traffic between the Application Load Balancer and its backing services.

        :default: HTTPS
        """
        result = self._values.get("internal_protocol")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RenderQueueTrafficEncryptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRepository)
class Repository(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.Repository",
):
    """This construct represents the main Deadline Repository which contains the central database and file system that Deadline requires.

    When deployed this construct will start up a single instance which will run the Deadline Repository installer to
    initialize the file system and database, the logs of which will be forwarded to Cloudwatch via a CloudWatchAgent.
    After the installation is complete the instance will be shutdown.

    Whenever the stack is updated if a change is detected in the installer a new instance will be started, which will perform
    a check on the existing Deadline Repository. If they are compatible with the new installer an update will be performed
    and the deployment will continue, otherwise the the deployment will be cancelled.
    In either case the instance will be cleaned up.


    Resources Deployed

    - Encrypted Amazon Elastic File System (EFS) - If no file system is provided.
    - An Amazon DocumentDB - If no database connection is provided.
    - Auto Scaling Group (ASG) with min & max capacity of 1 instance.
    - Instance Role and corresponding IAM Policy.
    - An Amazon CloudWatch log group that contains the Deadline Repository installation logs.



    Security Considerations

    - The instances deployed by this construct download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The file system that is created by, or provided to, this construct contains the data for Deadline's Repository file
      system. This file system contains information about your submitted jobs, and the plugin scripts that are run by the
      Deadline applications in your render farm. An actor that can modify the contents of this file system can cause your
      Deadline applications to run code of their choosing. You should restrict access to this file system to only those who
      require it.
    - The database that is created by, or provided to, this construct is used by Deadline to store data about its configuration,
      submitted jobs, machine information and status, and so on. An actor with access to this database can read any information
      that is entered into Deadline, and modify the bevavior of your render farm. You should restrict access to this database
      to only those who require it.
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        version: IVersion,
        vpc: aws_cdk.aws_ec2.IVpc,
        backup_options: typing.Optional["RepositoryBackupOptions"] = None,
        database: typing.Optional[DatabaseConnection] = None,
        database_audit_logging: typing.Optional[builtins.bool] = None,
        document_db_instance_count: typing.Optional[jsii.Number] = None,
        file_system: typing.Optional[_IMountableLinuxFilesystem_5182ce0b] = None,
        log_group_props: typing.Optional[_LogGroupFactoryProps_b817ed21] = None,
        removal_policy: typing.Optional["RepositoryRemovalPolicies"] = None,
        repository_installation_prefix: typing.Optional[builtins.str] = None,
        repository_installation_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param version: Version property to specify the version of deadline repository to be installed. This, in future, would be an optional property. If not passed, it should fetch the latest version of deadline. The current implementation of Version construct only supports importing it with static values, hence keeping it mandatory for now.
        :param vpc: VPC to launch the Repository In.
        :param backup_options: Define the backup options for the resources that this Repository creates. Default: Duration.days(15) for the database
        :param database: Specify the database where the deadline schema needs to be initialized. Note that Deadline supports only databases that are compatible with MongoDB 3.6. Default: A Document DB Cluster will be created with a single db.r5.large instance.
        :param database_audit_logging: If this Repository is creating its own DocumentDB database, then this specifies if audit logging will be enabled. Audit logs are a security best-practice. They record connection, data definition language (DDL), user management, and authorization events within the database, and are useful for post-incident auditing. That is, they can help you figure out what an unauthorized user, who gained access to your database, has done with that access. Default: true
        :param document_db_instance_count: If this Repository is creating its own Amazon DocumentDB database, then this specifies the number of compute instances to be created. Default: 1
        :param file_system: Specify the file system where the deadline repository needs to be initialized. Default: An Encrypted EFS File System will be created
        :param log_group_props: Properties for setting up the Deadline Repository's LogGroup in CloudWatch. Default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        :param removal_policy: Define the removal policies for the resources that this Repository creates. These define what happens to the resoureces when the stack that defines them is destroyed. Default: RemovalPolicy.RETAIN for all resources
        :param repository_installation_prefix: The prefix for the deadline repository installation path on the given file system. Default: : "/DeadlineRepository/"
        :param repository_installation_timeout: The length of time to wait for the repository installation before considering it as failure. The maximum value is 43200 (12 hours). Default: Duration.minutes(15)
        :param vpc_subnets: All resources that are created by this Repository will be deployed to these Subnets. This includes the Auto Scaling Group that is created for running the Repository Installer. If this Repository is creating an Amazon DocumentDB database and/or Amazon Elastic File System (EFS), then this specifies the subnets to which they are deployed. Default: : Private subnets in the VPC
        """
        props = RepositoryProps(
            version=version,
            vpc=vpc,
            backup_options=backup_options,
            database=database,
            database_audit_logging=database_audit_logging,
            document_db_instance_count=document_db_instance_count,
            file_system=file_system,
            log_group_props=log_group_props,
            removal_policy=removal_policy,
            repository_installation_prefix=repository_installation_prefix,
            repository_installation_timeout=repository_installation_timeout,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(Repository, self, [scope, id, props])

    @jsii.member(jsii_name="configureClientECS")
    def configure_client_ecs(
        self,
        *,
        container_instances: ECSContainerInstanceProps,
        containers: ECSTaskProps,
    ) -> IContainerDirectRepositoryConnection:
        """Configures an ECS Container Instance and Task Definition for deploying a Deadline Client that directly connects to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData

        :param container_instances: Configuration of ECS host instances to permit connecting hosted ECS tasks to the repository.
        :param containers: Configuration to directly connect an ECS task to the repository.

        :inheritdoc: true
        """
        props = ECSDirectConnectProps(
            container_instances=container_instances, containers=containers
        )

        return jsii.invoke(self, "configureClientECS", [props])

    @jsii.member(jsii_name="configureClientInstance")
    def configure_client_instance(
        self,
        *,
        host: IHost,
        mount_point: builtins.str,
    ) -> None:
        """Configure a Deadline Client, that is running in an Amazon EC2 instance, for direct connection to this repository.

        This includes:

        - Ingress to database & filesystem Security Groups, as required.
        - IAM Permissions for database & filesystem, as required.
        - Mounts the Repository File System via UserData
        - Configures Deadline to direct-connect to the Repository.

        :param host: The Instance/UserData which will directly connect to the Repository.
        :param mount_point: The location where the Repositories file system will be mounted on the instance.

        :inheritdoc: true
        """
        props = InstanceDirectConnectProps(host=host, mount_point=mount_point)

        return jsii.invoke(self, "configureClientInstance", [props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="databaseConnection")
    def database_connection(self) -> DatabaseConnection:
        """Connection object for the database for this repository."""
        return jsii.get(self, "databaseConnection")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> _IMountableLinuxFilesystem_5182ce0b:
        """The Linux-mountable filesystem that will store the Deadline repository filesystem contents."""
        return jsii.get(self, "fileSystem")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rootPrefix")
    def root_prefix(self) -> builtins.str:
        """The path to the Deadline Repository directory.

        This is expressed as a relative path from the root of the Deadline Repository file-system.

        :inheritdoc: true
        """
        return jsii.get(self, "rootPrefix")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> IVersion:
        """The version of Deadline for Linux that is installed on this Repository.

        :inheritdoc: true
        """
        return jsii.get(self, "version")


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RepositoryBackupOptions",
    jsii_struct_bases=[],
    name_mapping={"database_retention": "databaseRetention"},
)
class RepositoryBackupOptions:
    def __init__(
        self,
        *,
        database_retention: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Properties for backups of resources that are created by the Repository.

        :param database_retention: If this Repository is creating its own Amazon DocumentDB database, then this specifies the retention period to use on the database. If the Repository is not creating a DocumentDB database, because one was given, then this property is ignored. Please visit https://aws.amazon.com/documentdb/pricing/ to learn more about DocumentDB backup storage pricing. Default: Duration.days(15)
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if database_retention is not None:
            self._values["database_retention"] = database_retention

    @builtins.property
    def database_retention(self) -> typing.Optional[aws_cdk.core.Duration]:
        """If this Repository is creating its own Amazon DocumentDB database, then this specifies the retention period to use on the database.

        If the Repository is not creating a DocumentDB database, because one was given,
        then this property is ignored.
        Please visit https://aws.amazon.com/documentdb/pricing/ to learn more about DocumentDB backup storage pricing.

        :default: Duration.days(15)
        """
        result = self._values.get("database_retention")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryBackupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "vpc": "vpc",
        "backup_options": "backupOptions",
        "database": "database",
        "database_audit_logging": "databaseAuditLogging",
        "document_db_instance_count": "documentDbInstanceCount",
        "file_system": "fileSystem",
        "log_group_props": "logGroupProps",
        "removal_policy": "removalPolicy",
        "repository_installation_prefix": "repositoryInstallationPrefix",
        "repository_installation_timeout": "repositoryInstallationTimeout",
        "vpc_subnets": "vpcSubnets",
    },
)
class RepositoryProps:
    def __init__(
        self,
        *,
        version: IVersion,
        vpc: aws_cdk.aws_ec2.IVpc,
        backup_options: typing.Optional[RepositoryBackupOptions] = None,
        database: typing.Optional[DatabaseConnection] = None,
        database_audit_logging: typing.Optional[builtins.bool] = None,
        document_db_instance_count: typing.Optional[jsii.Number] = None,
        file_system: typing.Optional[_IMountableLinuxFilesystem_5182ce0b] = None,
        log_group_props: typing.Optional[_LogGroupFactoryProps_b817ed21] = None,
        removal_policy: typing.Optional["RepositoryRemovalPolicies"] = None,
        repository_installation_prefix: typing.Optional[builtins.str] = None,
        repository_installation_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Properties for the Deadline repository.

        :param version: Version property to specify the version of deadline repository to be installed. This, in future, would be an optional property. If not passed, it should fetch the latest version of deadline. The current implementation of Version construct only supports importing it with static values, hence keeping it mandatory for now.
        :param vpc: VPC to launch the Repository In.
        :param backup_options: Define the backup options for the resources that this Repository creates. Default: Duration.days(15) for the database
        :param database: Specify the database where the deadline schema needs to be initialized. Note that Deadline supports only databases that are compatible with MongoDB 3.6. Default: A Document DB Cluster will be created with a single db.r5.large instance.
        :param database_audit_logging: If this Repository is creating its own DocumentDB database, then this specifies if audit logging will be enabled. Audit logs are a security best-practice. They record connection, data definition language (DDL), user management, and authorization events within the database, and are useful for post-incident auditing. That is, they can help you figure out what an unauthorized user, who gained access to your database, has done with that access. Default: true
        :param document_db_instance_count: If this Repository is creating its own Amazon DocumentDB database, then this specifies the number of compute instances to be created. Default: 1
        :param file_system: Specify the file system where the deadline repository needs to be initialized. Default: An Encrypted EFS File System will be created
        :param log_group_props: Properties for setting up the Deadline Repository's LogGroup in CloudWatch. Default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        :param removal_policy: Define the removal policies for the resources that this Repository creates. These define what happens to the resoureces when the stack that defines them is destroyed. Default: RemovalPolicy.RETAIN for all resources
        :param repository_installation_prefix: The prefix for the deadline repository installation path on the given file system. Default: : "/DeadlineRepository/"
        :param repository_installation_timeout: The length of time to wait for the repository installation before considering it as failure. The maximum value is 43200 (12 hours). Default: Duration.minutes(15)
        :param vpc_subnets: All resources that are created by this Repository will be deployed to these Subnets. This includes the Auto Scaling Group that is created for running the Repository Installer. If this Repository is creating an Amazon DocumentDB database and/or Amazon Elastic File System (EFS), then this specifies the subnets to which they are deployed. Default: : Private subnets in the VPC
        """
        if isinstance(backup_options, dict):
            backup_options = RepositoryBackupOptions(**backup_options)
        if isinstance(log_group_props, dict):
            log_group_props = _LogGroupFactoryProps_b817ed21(**log_group_props)
        if isinstance(removal_policy, dict):
            removal_policy = RepositoryRemovalPolicies(**removal_policy)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "version": version,
            "vpc": vpc,
        }
        if backup_options is not None:
            self._values["backup_options"] = backup_options
        if database is not None:
            self._values["database"] = database
        if database_audit_logging is not None:
            self._values["database_audit_logging"] = database_audit_logging
        if document_db_instance_count is not None:
            self._values["document_db_instance_count"] = document_db_instance_count
        if file_system is not None:
            self._values["file_system"] = file_system
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if repository_installation_prefix is not None:
            self._values["repository_installation_prefix"] = repository_installation_prefix
        if repository_installation_timeout is not None:
            self._values["repository_installation_timeout"] = repository_installation_timeout
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def version(self) -> IVersion:
        """Version property to specify the version of deadline repository to be installed.

        This, in future, would be an optional property. If not passed, it should fetch
        the latest version of deadline. The current implementation of Version construct
        only supports importing it with static values, hence keeping it mandatory for now.
        """
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return result

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC to launch the Repository In."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def backup_options(self) -> typing.Optional[RepositoryBackupOptions]:
        """Define the backup options for the resources that this Repository creates.

        :default: Duration.days(15) for the database
        """
        result = self._values.get("backup_options")
        return result

    @builtins.property
    def database(self) -> typing.Optional[DatabaseConnection]:
        """Specify the database where the deadline schema needs to be initialized.

        Note that Deadline supports only databases that are compatible with MongoDB 3.6.

        :default: A Document DB Cluster will be created with a single db.r5.large instance.
        """
        result = self._values.get("database")
        return result

    @builtins.property
    def database_audit_logging(self) -> typing.Optional[builtins.bool]:
        """If this Repository is creating its own DocumentDB database, then this specifies if audit logging will be enabled.

        Audit logs are a security best-practice. They record connection, data definition language (DDL), user management,
        and authorization events within the database, and are useful for post-incident auditing. That is, they can help you
        figure out what an unauthorized user, who gained access to your database, has done with that access.

        :default: true
        """
        result = self._values.get("database_audit_logging")
        return result

    @builtins.property
    def document_db_instance_count(self) -> typing.Optional[jsii.Number]:
        """If this Repository is creating its own Amazon DocumentDB database, then this specifies the number of compute instances to be created.

        :default: 1
        """
        result = self._values.get("document_db_instance_count")
        return result

    @builtins.property
    def file_system(self) -> typing.Optional[_IMountableLinuxFilesystem_5182ce0b]:
        """Specify the file system where the deadline repository needs to be initialized.

        :default: An Encrypted EFS File System will be created
        """
        result = self._values.get("file_system")
        return result

    @builtins.property
    def log_group_props(self) -> typing.Optional[_LogGroupFactoryProps_b817ed21]:
        """Properties for setting up the Deadline Repository's LogGroup in CloudWatch.

        :default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        """
        result = self._values.get("log_group_props")
        return result

    @builtins.property
    def removal_policy(self) -> typing.Optional["RepositoryRemovalPolicies"]:
        """Define the removal policies for the resources that this Repository creates.

        These define what happens
        to the resoureces when the stack that defines them is destroyed.

        :default: RemovalPolicy.RETAIN for all resources
        """
        result = self._values.get("removal_policy")
        return result

    @builtins.property
    def repository_installation_prefix(self) -> typing.Optional[builtins.str]:
        """The prefix for the deadline repository installation path on the given file system.

        :default: : "/DeadlineRepository/"
        """
        result = self._values.get("repository_installation_prefix")
        return result

    @builtins.property
    def repository_installation_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The length of time to wait for the repository installation before considering it as failure.

        The maximum value is 43200 (12 hours).

        :default: Duration.minutes(15)
        """
        result = self._values.get("repository_installation_timeout")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """All resources that are created by this Repository will be deployed to these Subnets.

        This includes the
        Auto Scaling Group that is created for running the Repository Installer. If this Repository is creating
        an Amazon DocumentDB database and/or Amazon Elastic File System (EFS), then this specifies the subnets
        to which they are deployed.

        :default: : Private subnets in the VPC
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.RepositoryRemovalPolicies",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "filesystem": "filesystem"},
)
class RepositoryRemovalPolicies:
    def __init__(
        self,
        *,
        database: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        filesystem: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
    ) -> None:
        """
        :param database: If this Repository is creating its own Amazon DocumentDB database, then this specifies the retention policy to use on the database. If the Repository is not creating a DocumentDB database, because one was given, then this property is ignored. Default: RemovalPolicy.RETAIN
        :param filesystem: If this Repository is creating its own Amazon Elastic File System (EFS), then this specifies the retention policy to use on the filesystem. If the Repository is not creating an EFS, because one was given, then this property is ignored. Default: RemovalPolicy.RETAIN
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if database is not None:
            self._values["database"] = database
        if filesystem is not None:
            self._values["filesystem"] = filesystem

    @builtins.property
    def database(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """If this Repository is creating its own Amazon DocumentDB database, then this specifies the retention policy to use on the database.

        If the Repository is not creating a DocumentDB database, because one was given,
        then this property is ignored.

        :default: RemovalPolicy.RETAIN
        """
        result = self._values.get("database")
        return result

    @builtins.property
    def filesystem(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """If this Repository is creating its own Amazon Elastic File System (EFS), then this specifies the retention policy to use on the filesystem.

        If the Repository is not creating an EFS, because one was given, then this property is ignored.

        :default: RemovalPolicy.RETAIN
        """
        result = self._values.get("filesystem")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryRemovalPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Stage(metaclass=jsii.JSIIMeta, jsii_type="aws-rfdk.deadline.Stage"):
    """Class for interacting with the Deadline stage directory.

    The stage is a directory that conforms to a conventional structure that RFDK
    requires to deploy Deadline. It should contain a manifest file, the Deadline
    installers, and any supporting files required for building the Deadline
    container.

    Note: Current version of RFDK supports Deadline v10.1.9.2 and later.
    """

    def __init__(self, *, manifest: Manifest, path: builtins.str) -> None:
        """Constructs a Stage instance.

        :param manifest: The parsed manifest that describes the contents of the stage directory.
        :param path: The path to the directory where Deadline is staged.
        """
        props = StageProps(manifest=manifest, path=path)

        jsii.create(Stage, self, [props])

    @jsii.member(jsii_name="fromDirectory")
    @builtins.classmethod
    def from_directory(cls, stage_path: builtins.str) -> "Stage":
        """Returns a {@link Stage} loaded using the specified directory as the Docker build context and loads and uses the manifest named ``manifest.json`` in the directory.

        :param stage_path: The path to the Deadline stage directory.
        """
        return jsii.sinvoke(cls, "fromDirectory", [stage_path])

    @jsii.member(jsii_name="loadManifest")
    @builtins.classmethod
    def load_manifest(cls, manifest_path: builtins.str) -> Manifest:
        """Loads and parses the manifest file from a given path.

        :param manifest_path: The path to the manifest JSON file.
        """
        return jsii.sinvoke(cls, "loadManifest", [manifest_path])

    @jsii.member(jsii_name="getVersion")
    def get_version(self, scope: aws_cdk.core.Construct, id: builtins.str) -> IVersion:
        """Creates a {@link Version} based on the manifest version.

        :param scope: The parent scope.
        :param id: The construct ID.
        """
        return jsii.invoke(self, "getVersion", [scope, id])

    @jsii.member(jsii_name="imageFromRecipe")
    def image_from_recipe(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        recipe_name: builtins.str,
    ) -> aws_cdk.aws_ecr_assets.DockerImageAsset:
        """Construct a {@link DockerImageAsset} instance from a recipe in the Stage.

        :param scope: The scope for the {@link DockerImageAsset}.
        :param id: The construct ID of the {@link DockerImageAsset}.
        :param recipe_name: The name of the recipe.
        """
        return jsii.invoke(self, "imageFromRecipe", [scope, id, recipe_name])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dirPath")
    def dir_path(self) -> builtins.str:
        """The path to the stage directory."""
        return jsii.get(self, "dirPath")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="manifest")
    def manifest(self) -> Manifest:
        """The parsed manifest within the stage directory."""
        return jsii.get(self, "manifest")


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.StageProps",
    jsii_struct_bases=[],
    name_mapping={"manifest": "manifest", "path": "path"},
)
class StageProps:
    def __init__(self, *, manifest: Manifest, path: builtins.str) -> None:
        """Constructor properties of the {@link Stage} class.

        :param manifest: The parsed manifest that describes the contents of the stage directory.
        :param path: The path to the directory where Deadline is staged.
        """
        if isinstance(manifest, dict):
            manifest = Manifest(**manifest)
        self._values: typing.Dict[str, typing.Any] = {
            "manifest": manifest,
            "path": path,
        }

    @builtins.property
    def manifest(self) -> Manifest:
        """The parsed manifest that describes the contents of the stage directory."""
        result = self._values.get("manifest")
        assert result is not None, "Required property 'manifest' is missing"
        return result

    @builtins.property
    def path(self) -> builtins.str:
        """The path to the directory where Deadline is staged."""
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ThinkboxDockerRecipes(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.ThinkboxDockerRecipes",
):
    """An API for interacting with staged Deadline Docker recipes provided by AWS Thinkbox.

    This provides container images as required by RFDK's Deadline constructs such as

    - {@link @aws-rfdk/deadline#RenderQueue}
    - {@link @aws-rfdk/deadline#UsageBasedLicensing}

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        ConstructaRenderQueue
        
        from aws_rfdk.core import App, Stack, Vpc
        from aws_rfdk.deadline import RenderQueue, Repository, ThinkboxDockerRecipes
        app = App()
        stack = Stack(app, "Stack")
        vpc = Vpc(app, stack)
        recipes = ThinkboxDockerRecipes(stack, "Recipes",
            path="/path/to/staged/recipes"
        )
        repository = Repository(stack, "Repository",
            vpc=vpc,
            version=recipes.version
        )
        
        render_queue = RenderQueue(stack, "RenderQueue",
            images=recipes.render_queue_images
        )
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        stage: Stage,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param stage: The place where Deadline is staged.
        """
        props = ThinkboxDockerRecipesProps(stage=stage)

        jsii.create(ThinkboxDockerRecipes, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="licenseForwarder")
    def license_forwarder(self) -> aws_cdk.aws_ecr_assets.DockerImageAsset:
        """A {@link DockerImageAsset} that can be used to build Thinkbox's Deadline License Forwarder Docker Recipe into a container image that can be deployed in CDK."""
        return jsii.get(self, "licenseForwarder")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="remoteConnectionServer")
    def remote_connection_server(self) -> aws_cdk.aws_ecr_assets.DockerImageAsset:
        """A {@link DockerImageAsset} that can be used to build Thinkbox's Deadline RCS Docker Recipe into a container image that can be deployed in CDK."""
        return jsii.get(self, "remoteConnectionServer")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="renderQueueImages")
    def render_queue_images(self) -> RenderQueueImages:
        """Docker images staged locally for use with the {@link RenderQueue} construct."""
        return jsii.get(self, "renderQueueImages")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ublImages")
    def ubl_images(self) -> "UsageBasedLicensingImages":
        """Docker images staged locally for use with the {@link UsageBasedLicensing} construct."""
        return jsii.get(self, "ublImages")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> IVersion:
        """The version of Deadline in the stage directory."""
        return jsii.get(self, "version")


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.ThinkboxDockerRecipesProps",
    jsii_struct_bases=[],
    name_mapping={"stage": "stage"},
)
class ThinkboxDockerRecipesProps:
    def __init__(self, *, stage: Stage) -> None:
        """Interface to specify the properties when instantiating a {@link ThinkboxDockerRecipes} instnace.

        :param stage: The place where Deadline is staged.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "stage": stage,
        }

    @builtins.property
    def stage(self) -> Stage:
        """The place where Deadline is staged."""
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ThinkboxDockerRecipesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-rfdk.deadline.ThinkboxManagedDeadlineDockerRecipes")
class ThinkboxManagedDeadlineDockerRecipes(enum.Enum):
    """An enum that is associated with AWS Thinkbox managed recipes that are available in the stage manifest."""

    REMOTE_CONNECTION_SERVER = "REMOTE_CONNECTION_SERVER"
    """The Docker Image Asset for the Remote Connection Server."""
    LICENSE_FORWARDER = "LICENSE_FORWARDER"
    """The Docker Image Asset for the License Forwarder."""


class UsageBasedLicense(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.UsageBasedLicense",
):
    """Instances of this class represent a usage-based license for a particular product.

    It encapsulates all of the information specific to a product that the UsageBasedLicensing
    construct requires to interoperate with that product.
    """

    def __init__(
        self,
        *,
        license_name: builtins.str,
        ports: typing.List[aws_cdk.aws_ec2.Port],
        limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param license_name: The name of the product that the usage-based license applies to.
        :param ports: The set of ports that are used for licensing traffic.
        :param limit: The maximum number of usage-based licenses that can be used concurrently.
        """
        props = UsageBasedLicenseProps(
            license_name=license_name, ports=ports, limit=limit
        )

        jsii.create(UsageBasedLicense, self, [props])

    @jsii.member(jsii_name="for3dsMax")
    @builtins.classmethod
    def for3ds_max(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for 3dsMax license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited

        :remark:

        3ds-Max usage-based licenses are not available with the UsageBasedLicensing
        construct that deploys Deadline 10.1.9.
        """
        return jsii.sinvoke(cls, "for3dsMax", [limit])

    @jsii.member(jsii_name="forArnold")
    @builtins.classmethod
    def for_arnold(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for Arnold license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited

        :remark:

        3ds-Max usage-based licenses are not available with the UsageBasedLicensing
        construct that deploys Deadline 10.1.9.
        """
        return jsii.sinvoke(cls, "forArnold", [limit])

    @jsii.member(jsii_name="forCinema4D")
    @builtins.classmethod
    def for_cinema4_d(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for Cinema 4D license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forCinema4D", [limit])

    @jsii.member(jsii_name="forClarisse")
    @builtins.classmethod
    def for_clarisse(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for Clarisse license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forClarisse", [limit])

    @jsii.member(jsii_name="forHoudini")
    @builtins.classmethod
    def for_houdini(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for Houdini license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forHoudini", [limit])

    @jsii.member(jsii_name="forKatana")
    @builtins.classmethod
    def for_katana(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for Katana license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forKatana", [limit])

    @jsii.member(jsii_name="forKeyShot")
    @builtins.classmethod
    def for_key_shot(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for KeyShot license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forKeyShot", [limit])

    @jsii.member(jsii_name="forKrakatoa")
    @builtins.classmethod
    def for_krakatoa(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for krakatoa license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forKrakatoa", [limit])

    @jsii.member(jsii_name="forMantra")
    @builtins.classmethod
    def for_mantra(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for Mantra license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forMantra", [limit])

    @jsii.member(jsii_name="forMaxwell")
    @builtins.classmethod
    def for_maxwell(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for maxwell license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forMaxwell", [limit])

    @jsii.member(jsii_name="forMaya")
    @builtins.classmethod
    def for_maya(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for Maya license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited

        :remark:

        3ds-Max usage-based licenses are not available with the UsageBasedLicensing
        construct that deploys Deadline 10.1.9.
        """
        return jsii.sinvoke(cls, "forMaya", [limit])

    @jsii.member(jsii_name="forNuke")
    @builtins.classmethod
    def for_nuke(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for Nuke license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forNuke", [limit])

    @jsii.member(jsii_name="forRealFlow")
    @builtins.classmethod
    def for_real_flow(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for RealFlow license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forRealFlow", [limit])

    @jsii.member(jsii_name="forRedShift")
    @builtins.classmethod
    def for_red_shift(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for RedShift license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forRedShift", [limit])

    @jsii.member(jsii_name="forVray")
    @builtins.classmethod
    def for_vray(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for V-Ray license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forVray", [limit])

    @jsii.member(jsii_name="forYeti")
    @builtins.classmethod
    def for_yeti(
        cls,
        limit: typing.Optional[jsii.Number] = None,
    ) -> "UsageBasedLicense":
        """Method for Yeti license limit.

        :param limit: - The maximum number of rendering tasks that can have this UBL license checked out at the same time.

        :default: - limit will be set to unlimited
        """
        return jsii.sinvoke(cls, "forYeti", [limit])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="UNLIMITED")
    def UNLIMITED(cls) -> jsii.Number:
        """Constant used to signify unlimited overage."""
        return jsii.sget(cls, "UNLIMITED")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="licenseName")
    def license_name(self) -> builtins.str:
        """The name of license limit."""
        return jsii.get(self, "licenseName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[aws_cdk.aws_ec2.Port]:
        """Ports that will be used for this license."""
        return jsii.get(self, "ports")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="limit")
    def limit(self) -> typing.Optional[jsii.Number]:
        """Maximum count of licenses that will be used."""
        return jsii.get(self, "limit")


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.UsageBasedLicenseProps",
    jsii_struct_bases=[],
    name_mapping={"license_name": "licenseName", "ports": "ports", "limit": "limit"},
)
class UsageBasedLicenseProps:
    def __init__(
        self,
        *,
        license_name: builtins.str,
        ports: typing.List[aws_cdk.aws_ec2.Port],
        limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Properties for constructing a {@link UsageBasedLicense} instance.

        :param license_name: The name of the product that the usage-based license applies to.
        :param ports: The set of ports that are used for licensing traffic.
        :param limit: The maximum number of usage-based licenses that can be used concurrently.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "license_name": license_name,
            "ports": ports,
        }
        if limit is not None:
            self._values["limit"] = limit

    @builtins.property
    def license_name(self) -> builtins.str:
        """The name of the product that the usage-based license applies to."""
        result = self._values.get("license_name")
        assert result is not None, "Required property 'license_name' is missing"
        return result

    @builtins.property
    def ports(self) -> typing.List[aws_cdk.aws_ec2.Port]:
        """The set of ports that are used for licensing traffic."""
        result = self._values.get("ports")
        assert result is not None, "Required property 'ports' is missing"
        return result

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        """The maximum number of usage-based licenses that can be used concurrently."""
        result = self._values.get("limit")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UsageBasedLicenseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_iam.IGrantable)
class UsageBasedLicensing(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.UsageBasedLicensing",
):
    """This construct is an implementation of the Deadline component that is required for Usage-based Licensing (UBL) (see: https://docs.thinkboxsoftware.com/products/deadline/10.1/1_User%20Manual/manual/licensing-usage-based.html ) in a render farm.

    Internally this is implemented as one or more instances of the Deadline License Forwarder application set up
    to communicate to the render queue and Thinkbox’s licensing system, and to allow ingress connections
    from the worker nodes so that they can acquire licenses as needed.

    The Deadline License Forwarder is set up to run within an AWS ECS task.

    Access to the running License Forwarder is gated by a security group that, by default, allows no ingress;
    when a Deadline Worker requires access to licensing, then the RFDK constructs will grant that worker’s security group
    ingress on TCP port 17004 as well as other ports as required by the specific licenses being used.

    Note: This construct does not currently implement the Deadline License Forwarder's Web Forwarding functionality.
    This construct is not usable in any China region.


    Resources Deployed

    - The Auto Scaling Group (ASG) added to the Amazon Elastic Container Service cluster that is hosting the Deadline
      License Forwarder for UBL. This creates one C5 Large instance by default.
    - Amazon Elastic Block Store (EBS) device(s) associated with the EC2 instance(s) in the ASG. The default volume size is 30 GiB.
    - An Amazon CloudWatch log group that contains the logs from the Deadline License Forwarder application.



    Security Considerations

    - The instances deployed by this construct download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The Deadline License Forwarder is designed to be secured by restricting network access to it. For security, only the Deadline
      Workers that require access to Usage-based Licenses should be granted network access to the instances deployed by this construct.
      Futhermore, you should restrict that access to only the product(s) that those workers require when deploying this construct.
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        certificate_secret: aws_cdk.aws_secretsmanager.ISecret,
        images: "UsageBasedLicensingImages",
        licenses: typing.List[UsageBasedLicense],
        render_queue: IRenderQueue,
        vpc: aws_cdk.aws_ec2.IVpc,
        desired_count: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        log_group_props: typing.Optional[_LogGroupFactoryProps_b817ed21] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param certificate_secret: A secret with with 3rd Party Licensing Certificates. If you want to use 3rd Party Licensing Certificates you need to purchase render time on Thinkbox Marketplace and download file with certificates. File with certificates should be put in in a secret.
        :param images: Docker Image for License Forwarder.
        :param licenses: License limits that will be set in repository configuration.
        :param render_queue: The Deadline Render Queue, to which the License Forwarder needs to be connected.
        :param vpc: VPC to launch the License Forwarder In.
        :param desired_count: The desired number of Deadline License Forwarders that this construct keeps running. Default: 1
        :param instance_type: Type of instance that will be added to an AutoScalingGroup. Default: - Will be used C5 Large instance
        :param log_group_props: Properties for setting up the Deadline License Forwarder's LogGroup in CloudWatch. Default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        :param vpc_subnets: Subnets within the VPC in which to host the UBLLicesing servers. Default: All private subnets in the VPC.
        """
        props = UsageBasedLicensingProps(
            certificate_secret=certificate_secret,
            images=images,
            licenses=licenses,
            render_queue=render_queue,
            vpc=vpc,
            desired_count=desired_count,
            instance_type=instance_type,
            log_group_props=log_group_props,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(UsageBasedLicensing, self, [scope, id, props])

    @jsii.member(jsii_name="grantPortAccess")
    def grant_port_access(
        self,
        worker_fleet: IWorkerFleet,
        licenses: typing.List[UsageBasedLicense],
    ) -> None:
        """This method grant access of worker fleet to ports that required.

        :param worker_fleet: - worker fleet.
        :param licenses: - UBL licenses.
        """
        return jsii.invoke(self, "grantPortAccess", [worker_fleet, licenses])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="asg")
    def asg(self) -> aws_cdk.aws_autoscaling.AutoScalingGroup:
        """Autoscaling group for license forwarder instances."""
        return jsii.get(self, "asg")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.Cluster:
        """The Amazon ECS cluster that is hosting the Deadline License Forwarder for UBL."""
        return jsii.get(self, "cluster")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """The connections object that allows you to control network egress/ingress to the License Forwarder."""
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.Ec2Service:
        """The ECS service that serves usage based licensing."""
        return jsii.get(self, "service")


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.UsageBasedLicensingImages",
    jsii_struct_bases=[],
    name_mapping={"license_forwarder": "licenseForwarder"},
)
class UsageBasedLicensingImages:
    def __init__(self, *, license_forwarder: aws_cdk.aws_ecs.ContainerImage) -> None:
        """Set of container images used to serve the {@link UsageBasedLicensing} construct.

        :param license_forwarder: The container image for the Deadline License Forwarder.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "license_forwarder": license_forwarder,
        }

    @builtins.property
    def license_forwarder(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The container image for the Deadline License Forwarder."""
        result = self._values.get("license_forwarder")
        assert result is not None, "Required property 'license_forwarder' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UsageBasedLicensingImages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.UsageBasedLicensingProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_secret": "certificateSecret",
        "images": "images",
        "licenses": "licenses",
        "render_queue": "renderQueue",
        "vpc": "vpc",
        "desired_count": "desiredCount",
        "instance_type": "instanceType",
        "log_group_props": "logGroupProps",
        "vpc_subnets": "vpcSubnets",
    },
)
class UsageBasedLicensingProps:
    def __init__(
        self,
        *,
        certificate_secret: aws_cdk.aws_secretsmanager.ISecret,
        images: UsageBasedLicensingImages,
        licenses: typing.List[UsageBasedLicense],
        render_queue: IRenderQueue,
        vpc: aws_cdk.aws_ec2.IVpc,
        desired_count: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        log_group_props: typing.Optional[_LogGroupFactoryProps_b817ed21] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Properties for the UsageBasedLicensing construct.

        :param certificate_secret: A secret with with 3rd Party Licensing Certificates. If you want to use 3rd Party Licensing Certificates you need to purchase render time on Thinkbox Marketplace and download file with certificates. File with certificates should be put in in a secret.
        :param images: Docker Image for License Forwarder.
        :param licenses: License limits that will be set in repository configuration.
        :param render_queue: The Deadline Render Queue, to which the License Forwarder needs to be connected.
        :param vpc: VPC to launch the License Forwarder In.
        :param desired_count: The desired number of Deadline License Forwarders that this construct keeps running. Default: 1
        :param instance_type: Type of instance that will be added to an AutoScalingGroup. Default: - Will be used C5 Large instance
        :param log_group_props: Properties for setting up the Deadline License Forwarder's LogGroup in CloudWatch. Default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        :param vpc_subnets: Subnets within the VPC in which to host the UBLLicesing servers. Default: All private subnets in the VPC.
        """
        if isinstance(images, dict):
            images = UsageBasedLicensingImages(**images)
        if isinstance(log_group_props, dict):
            log_group_props = _LogGroupFactoryProps_b817ed21(**log_group_props)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "certificate_secret": certificate_secret,
            "images": images,
            "licenses": licenses,
            "render_queue": render_queue,
            "vpc": vpc,
        }
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def certificate_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        """A secret with with 3rd Party Licensing Certificates.

        If you want to use 3rd Party Licensing Certificates you need to purchase render time on Thinkbox Marketplace
        and download file with certificates.
        File with certificates should be put in in a secret.
        """
        result = self._values.get("certificate_secret")
        assert result is not None, "Required property 'certificate_secret' is missing"
        return result

    @builtins.property
    def images(self) -> UsageBasedLicensingImages:
        """Docker Image for License Forwarder."""
        result = self._values.get("images")
        assert result is not None, "Required property 'images' is missing"
        return result

    @builtins.property
    def licenses(self) -> typing.List[UsageBasedLicense]:
        """License limits that will be set in repository configuration."""
        result = self._values.get("licenses")
        assert result is not None, "Required property 'licenses' is missing"
        return result

    @builtins.property
    def render_queue(self) -> IRenderQueue:
        """The Deadline Render Queue, to which the License Forwarder needs to be connected."""
        result = self._values.get("render_queue")
        assert result is not None, "Required property 'render_queue' is missing"
        return result

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC to launch the License Forwarder In."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of Deadline License Forwarders that this construct keeps running.

        :default: 1
        """
        result = self._values.get("desired_count")
        return result

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """Type of instance that will be added to an AutoScalingGroup.

        :default: - Will be used C5 Large instance
        """
        result = self._values.get("instance_type")
        return result

    @builtins.property
    def log_group_props(self) -> typing.Optional[_LogGroupFactoryProps_b817ed21]:
        """Properties for setting up the Deadline License Forwarder's LogGroup in CloudWatch.

        :default: - LogGroup will be created with all properties' default values to the LogGroup: /renderfarm/
        """
        result = self._values.get("log_group_props")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Subnets within the VPC in which to host the UBLLicesing servers.

        :default: All private subnets in the VPC.
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UsageBasedLicensingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IVersion)
class VersionQuery(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.VersionQuery",
):
    """This class encapsulates information about a particular version of Thinkbox's Deadline software.

    Information such as the version number, and where to get installers for that version from Amazon S3.

    The version of an official release of Deadline is always four numeric version components separated by dots.
    ex: 10.1.8.5. We refer to the components in this version, in order from left-to-right, as the
    major, minor, release, and patch versions. For example, Deadline version 10.1.8.5 is majorVersion 10, minorVersion 1,
    releaseVersion 8, and patchVersion 5.

    All of the installers provided by an instance of this class must be for the same Deadline release (ex: 10.1.8),
    but the patch versions may differ between operating systems depending on the particulars of that release of Deadline.
    This class provides a simple way to query a version of Deadline prior to or during deployment of a
    CDK app.

    You pass an instance of this class to various Deadline constructs in this library to tell those
    constructs which version of Deadline you want them to use, and be configured for.
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param version: String containing the complete or partial deadline version. Default: - the latest available version of deadline installer.
        """
        props = VersionQueryProps(version=version)

        jsii.create(VersionQuery, self, [scope, id, props])

    @jsii.member(jsii_name="linuxFullVersionString")
    def linux_full_version_string(self) -> builtins.str:
        """Construct the full version string for the linux patch release referenced in this version object.

        This is constructed by joining the major, minor,
        release, and patch versions by dots.
        """
        return jsii.invoke(self, "linuxFullVersionString", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="linuxInstallers")
    def linux_installers(self) -> PlatformInstallers:
        """The Linux installers for this version.

        :inheritdoc: true
        """
        return jsii.get(self, "linuxInstallers")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="majorVersion")
    def major_version(self) -> jsii.Number:
        """The major version number.

        :inheritdoc: true
        """
        return jsii.get(self, "majorVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="minorVersion")
    def minor_version(self) -> jsii.Number:
        """The minor version number.

        :inheritdoc: true
        """
        return jsii.get(self, "minorVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> jsii.Number:
        """The release version number.

        :inheritdoc: true
        """
        return jsii.get(self, "releaseVersion")


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.VersionQueryProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class VersionQueryProps:
    def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
        """Properties for the Deadline Version.

        :param version: String containing the complete or partial deadline version. Default: - the latest available version of deadline installer.
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        """String containing the complete or partial deadline version.

        :default: - the latest available version of deadline installer.
        """
        result = self._values.get("version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VersionQueryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkerInstanceConfiguration(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.WorkerInstanceConfiguration",
):
    """This construct can be used to configure Deadline Workers on an instance to connect to a RenderQueue, stream their log files to CloudWatch, and configure various settings of the Deadline Worker.

    The configuration happens on instance start-up using user data scripting.

    This configuration performs the following steps in order:

    1. Configure Cloud Watch Agent
    2. Configure Deadline Worker RenderQueue connection
    3. Configure Deadline Worker settings

    A ``userDataProvider`` can be specified that defines callback functions.
    These callbacks can be used to inject user data commands at different points during the Worker instance configuration.


    Security Considerations

    - The instances configured by this construct will download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        worker: IHost,
        cloudwatch_log_settings: typing.Optional[_LogGroupFactoryProps_b817ed21] = None,
        render_queue: typing.Optional[IRenderQueue] = None,
        user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
        worker_settings: typing.Optional["WorkerSettings"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param worker: The Deadline Worker that should be configured.
        :param cloudwatch_log_settings: The configuration for streaming the Deadline Worker logs to AWS CloudWatch. Default: The Worker logs will not be streamed to CloudWatch.
        :param render_queue: The RenderQueue that the worker should be configured to connect to. Default: The Worker is not configured to connect to a RenderQueue
        :param user_data_provider: An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle. You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        :param worker_settings: The settings to apply to the Deadline Worker. Default: The Worker is assigned the default settings as outlined in the WorkerSettings interface.
        """
        props = WorkerInstanceConfigurationProps(
            worker=worker,
            cloudwatch_log_settings=cloudwatch_log_settings,
            render_queue=render_queue,
            user_data_provider=user_data_provider,
            worker_settings=worker_settings,
        )

        jsii.create(WorkerInstanceConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="configureCloudWatchLogStream")
    def _configure_cloud_watch_log_stream(
        self,
        worker: IHost,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        log_group_prefix: typing.Optional[builtins.str] = None,
        retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
    ) -> None:
        """This method can be used to configure a Deadline Worker instance to stream its logs to the AWS CloudWatch service.

        The logs that this configures to stream are:

        - EC2 Instance UserData execution; this is the startup scripting that is run when the instance launches
          for the first time.
        - Deadline Worker logs.
        - Deadline Launcher logs.

        :param worker: The worker to configure. This can be an instance, auto scaling group, launch template, etc.
        :param id: Identifier to disambiguate the resources that are created.
        :param bucket_name: The S3 bucket's name to export logs to. Setting this will enable exporting logs from CloudWatch to S3. Default: - No export to S3 will be performed.
        :param log_group_prefix: Prefix assigned to the name of any LogGroups that get created. Default: - No prefix will be applied.
        :param retention: The number of days log events are kept in CloudWatch Logs. Exportation to S3 will happen the day before they expire. Default: - 3 days.
        """
        log_group_props = _LogGroupFactoryProps_b817ed21(
            bucket_name=bucket_name,
            log_group_prefix=log_group_prefix,
            retention=retention,
        )

        return jsii.invoke(self, "configureCloudWatchLogStream", [worker, id, log_group_props])

    @jsii.member(jsii_name="configureWorkerSettings")
    def _configure_worker_settings(
        self,
        worker: IHost,
        id: builtins.str,
        *,
        groups: typing.Optional[typing.List[builtins.str]] = None,
        pools: typing.Optional[typing.List[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """This method can be used to set up the Deadline Worker application on an EC2 instance.

        From a practical
        perspective, this is executing the script found in aws-rfdk/lib/deadline/scripts/[bash,powershell]/configureWorker.[sh,ps1]
        to configure the Deadline Worker application.

        :param worker: The worker to configure. This can be an instance, auto scaling group, launch template, etc.
        :param id: Identifier to disambiguate the resources that are created.
        :param groups: Deadline groups these workers needs to be assigned to. The group is created if it does not already exist. Default: - Worker is not assigned to any group
        :param pools: Deadline pools these workers needs to be assigned to. The pool is created if it does not already exist. Default: - Worker is not assigned to any pool.
        :param region: Deadline region these workers needs to be assigned to. Default: - Worker is not assigned to any region
        """
        settings = WorkerSettings(groups=groups, pools=pools, region=region)

        return jsii.invoke(self, "configureWorkerSettings", [worker, id, settings])


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.WorkerInstanceConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "worker": "worker",
        "cloudwatch_log_settings": "cloudwatchLogSettings",
        "render_queue": "renderQueue",
        "user_data_provider": "userDataProvider",
        "worker_settings": "workerSettings",
    },
)
class WorkerInstanceConfigurationProps:
    def __init__(
        self,
        *,
        worker: IHost,
        cloudwatch_log_settings: typing.Optional[_LogGroupFactoryProps_b817ed21] = None,
        render_queue: typing.Optional[IRenderQueue] = None,
        user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
        worker_settings: typing.Optional["WorkerSettings"] = None,
    ) -> None:
        """Properties for a WorkerInstanceConfiguration.

        :param worker: The Deadline Worker that should be configured.
        :param cloudwatch_log_settings: The configuration for streaming the Deadline Worker logs to AWS CloudWatch. Default: The Worker logs will not be streamed to CloudWatch.
        :param render_queue: The RenderQueue that the worker should be configured to connect to. Default: The Worker is not configured to connect to a RenderQueue
        :param user_data_provider: An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle. You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        :param worker_settings: The settings to apply to the Deadline Worker. Default: The Worker is assigned the default settings as outlined in the WorkerSettings interface.
        """
        if isinstance(cloudwatch_log_settings, dict):
            cloudwatch_log_settings = _LogGroupFactoryProps_b817ed21(**cloudwatch_log_settings)
        if isinstance(worker_settings, dict):
            worker_settings = WorkerSettings(**worker_settings)
        self._values: typing.Dict[str, typing.Any] = {
            "worker": worker,
        }
        if cloudwatch_log_settings is not None:
            self._values["cloudwatch_log_settings"] = cloudwatch_log_settings
        if render_queue is not None:
            self._values["render_queue"] = render_queue
        if user_data_provider is not None:
            self._values["user_data_provider"] = user_data_provider
        if worker_settings is not None:
            self._values["worker_settings"] = worker_settings

    @builtins.property
    def worker(self) -> IHost:
        """The Deadline Worker that should be configured."""
        result = self._values.get("worker")
        assert result is not None, "Required property 'worker' is missing"
        return result

    @builtins.property
    def cloudwatch_log_settings(
        self,
    ) -> typing.Optional[_LogGroupFactoryProps_b817ed21]:
        """The configuration for streaming the Deadline Worker logs to AWS CloudWatch.

        :default: The Worker logs will not be streamed to CloudWatch.
        """
        result = self._values.get("cloudwatch_log_settings")
        return result

    @builtins.property
    def render_queue(self) -> typing.Optional[IRenderQueue]:
        """The RenderQueue that the worker should be configured to connect to.

        :default: The Worker is not configured to connect to a RenderQueue
        """
        result = self._values.get("render_queue")
        return result

    @builtins.property
    def user_data_provider(self) -> typing.Optional[IInstanceUserDataProvider]:
        """An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle.

        You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        """
        result = self._values.get("user_data_provider")
        return result

    @builtins.property
    def worker_settings(self) -> typing.Optional["WorkerSettings"]:
        """The settings to apply to the Deadline Worker.

        :default: The Worker is assigned the default settings as outlined in the WorkerSettings interface.
        """
        result = self._values.get("worker_settings")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkerInstanceConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IWorkerFleet, _IMonitorableFleet_71f4eb88)
class WorkerInstanceFleet(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-rfdk.deadline.WorkerInstanceFleet",
):
    """This construct reperesents a fleet of Deadline Workers.

    The construct consists of an Auto Scaling Group (ASG) of instances using a provided AMI which has Deadline and any number
    of render applications installed.  Whenever an instance in the ASG start it will connect Deadline to the desired render queue.

    When the worker fleet is deployed if it has been provided a HealthMonitor the Worker fleet will register itself against the Monitor
    to ensure that the fleet remains healthy.


    Resources Deployed

    - An EC2 Auto Scaling Group to maintain the number of instances.
    - An Instance Role and corresponding IAM Policy.
    - An Amazon CloudWatch log group that contains the Deadline Worker, Deadline Launcher, and instance-startup logs for the instances
      in the fleet.



    Security Considerations

    - The instances deployed by this construct download and run scripts from your CDK bootstrap bucket when that instance
      is launched. You must limit write access to your CDK bootstrap bucket to prevent an attacker from modifying the actions
      performed by these scripts. We strongly recommend that you either enable Amazon S3 server access logging on your CDK
      bootstrap bucket, or enable AWS CloudTrail on your account to assist in post-incident analysis of compromised production
      environments.
    - The data that is stored on your Worker's local EBS volume can include temporary working files from the applications
      that are rendering your jobs and tasks. That data can be sensitive or privileged, so we recommend that you encrypt
      the data volumes of these instances using either the provided option or by using an encrypted AMI as your source.
    - The software on the AMI that is being used by this construct may pose a security risk. We recommend that you adopt a
      patching strategy to keep this software current with the latest security patches. Please see
      https://docs.aws.amazon.com/rfdk/latest/guide/patching-software.html for more information.
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        render_queue: IRenderQueue,
        vpc: aws_cdk.aws_ec2.IVpc,
        worker_machine_image: aws_cdk.aws_ec2.IMachineImage,
        block_devices: typing.Optional[typing.List[aws_cdk.aws_autoscaling.BlockDevice]] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        health_check_config: typing.Optional[_HealthCheckConfig_ebe26fb6] = None,
        health_monitor: typing.Optional[_IHealthMonitor_ab248fa9] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        key_name: typing.Optional[builtins.str] = None,
        log_group_props: typing.Optional[_LogGroupFactoryProps_b817ed21] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        spot_price: typing.Optional[jsii.Number] = None,
        user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        groups: typing.Optional[typing.List[builtins.str]] = None,
        pools: typing.Optional[typing.List[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param render_queue: Endpoint for the RenderQueue, to which the worker fleet needs to be connected.
        :param vpc: VPC to launch the worker fleet in.
        :param worker_machine_image: AMI of the deadline worker to launch.
        :param block_devices: 
        :param desired_capacity: Initial amount of workers in the fleet. If this is set to a number, every deployment will reset the amount of workers to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param health_check_config: Properties for configuring a health check. Note: The health-check feature is supported with Deadline Client v10.1.9 and later. Default: properties of HealthCheckConfig applies
        :param health_monitor: Health Monitor component to monitor the health of instances. Note: The health-check feature is supported with Deadline Client v10.1.9 and later. Default: - Health Monitoring is turned-off
        :param instance_type: Type of instance to launch for executing repository installer. Default: - a T2-Large type will be used.
        :param key_name: Name of SSH keypair to grant access to instance. Default: - No SSH access will be possible.
        :param log_group_props: Properties for setting up the Deadline Worker's LogGroup. Default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity, or minCapacity if desiredCapacity is not set
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param role: An IAM role to associate with the instance profile assigned to its resources. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: - A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security Group to assign to this fleet. Default: - create new security group
        :param spot_price: The maximum hourly price($) to be paid for each Spot instance. min - 0.001; max - 255 Default: - launches on-demand EC2 instances.
        :param user_data_provider: An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle. You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        :param groups: Deadline groups these workers needs to be assigned to. The group is created if it does not already exist. Default: - Worker is not assigned to any group
        :param pools: Deadline pools these workers needs to be assigned to. The pool is created if it does not already exist. Default: - Worker is not assigned to any pool.
        :param region: Deadline region these workers needs to be assigned to. Default: - Worker is not assigned to any region
        """
        props = WorkerInstanceFleetProps(
            render_queue=render_queue,
            vpc=vpc,
            worker_machine_image=worker_machine_image,
            block_devices=block_devices,
            desired_capacity=desired_capacity,
            health_check_config=health_check_config,
            health_monitor=health_monitor,
            instance_type=instance_type,
            key_name=key_name,
            log_group_props=log_group_props,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            role=role,
            security_group=security_group,
            spot_price=spot_price,
            user_data_provider=user_data_provider,
            vpc_subnets=vpc_subnets,
            groups=groups,
            pools=pools,
            region=region,
        )

        jsii.create(WorkerInstanceFleet, self, [scope, id, props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(
        self,
        security_group: aws_cdk.aws_ec2.ISecurityGroup,
    ) -> None:
        """Add the security group to all workers.

        :param security_group: : The security group to add.
        """
        return jsii.invoke(self, "addSecurityGroup", [security_group])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="SPOT_PRICE_MAX_LIMIT")
    def SPOT_PRICE_MAX_LIMIT(cls) -> jsii.Number:
        """The max limit for spot price."""
        return jsii.sget(cls, "SPOT_PRICE_MAX_LIMIT")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="SPOT_PRICE_MIN_LIMIT")
    def SPOT_PRICE_MIN_LIMIT(cls) -> jsii.Number:
        """The min limit for spot price."""
        return jsii.sget(cls, "SPOT_PRICE_MIN_LIMIT")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """The security groups/rules used to allow network connections to the file system."""
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="env")
    def env(self) -> aws_cdk.core.ResourceEnvironment:
        """The environment this resource belongs to."""
        return jsii.get(self, "env")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="fleet")
    def fleet(self) -> aws_cdk.aws_autoscaling.AutoScalingGroup:
        """The ASG object created by the construct."""
        return jsii.get(self, "fleet")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """The principal to grant permissions to."""
        return jsii.get(self, "grantPrincipal")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stack")
    def stack(self) -> aws_cdk.core.Stack:
        """The stack in which this worker fleet is defined."""
        return jsii.get(self, "stack")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetCapacity")
    def target_capacity(self) -> jsii.Number:
        """This field implements the maximum instance count this fleet can have."""
        return jsii.get(self, "targetCapacity")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetCapacityMetric")
    def target_capacity_metric(self) -> aws_cdk.aws_cloudwatch.IMetric:
        """This field implements the base capacity metric of the fleet against which, the healthy percent will be calculated.

        eg.: GroupDesiredCapacity for an ASG
        """
        return jsii.get(self, "targetCapacityMetric")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetScope")
    def target_scope(self) -> aws_cdk.core.Construct:
        """This field implements the scope in which to create the monitoring resource like TargetGroups, Listener etc."""
        return jsii.get(self, "targetScope")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetToMonitor")
    def target_to_monitor(
        self,
    ) -> aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget:
        """This field implements the component of type INetworkLoadBalancerTarget which can be attached to Network Load Balancer for monitoring.

        eg. An AutoScalingGroup
        """
        return jsii.get(self, "targetToMonitor")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetUpdatePolicy")
    def target_update_policy(self) -> aws_cdk.aws_iam.IPolicy:
        """This field implements a policy which can be attached to the lambda execution role so that it is capable of suspending the fleet.

        eg.: autoscaling:UpdateAutoScalingGroup permission for an ASG
        """
        return jsii.get(self, "targetUpdatePolicy")


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.WorkerSettings",
    jsii_struct_bases=[],
    name_mapping={"groups": "groups", "pools": "pools", "region": "region"},
)
class WorkerSettings:
    def __init__(
        self,
        *,
        groups: typing.Optional[typing.List[builtins.str]] = None,
        pools: typing.Optional[typing.List[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """Configuration settings for Deadline Workers.

        :param groups: Deadline groups these workers needs to be assigned to. The group is created if it does not already exist. Default: - Worker is not assigned to any group
        :param pools: Deadline pools these workers needs to be assigned to. The pool is created if it does not already exist. Default: - Worker is not assigned to any pool.
        :param region: Deadline region these workers needs to be assigned to. Default: - Worker is not assigned to any region
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if groups is not None:
            self._values["groups"] = groups
        if pools is not None:
            self._values["pools"] = pools
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """Deadline groups these workers needs to be assigned to.

        The group is
        created if it does not already exist.

        :default: - Worker is not assigned to any group
        """
        result = self._values.get("groups")
        return result

    @builtins.property
    def pools(self) -> typing.Optional[typing.List[builtins.str]]:
        """Deadline pools these workers needs to be assigned to.

        The pool is created
        if it does not already exist.

        :default: - Worker is not assigned to any pool.
        """
        result = self._values.get("pools")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """Deadline region these workers needs to be assigned to.

        :default: - Worker is not assigned to any region
        """
        result = self._values.get("region")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkerSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-rfdk.deadline.IPatchVersion")
class IPatchVersion(IReleaseVersion, typing_extensions.Protocol):
    """Represents a fully-qualified release version number.

    E.g. 10.1.9.2
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IPatchVersionProxy

    @builtins.property # type: ignore
    @jsii.member(jsii_name="patchVersion")
    def patch_version(self) -> jsii.Number:
        """The patch version number."""
        ...


class _IPatchVersionProxy(
    jsii.proxy_for(IReleaseVersion) # type: ignore
):
    """Represents a fully-qualified release version number.

    E.g. 10.1.9.2
    """

    __jsii_type__: typing.ClassVar[str] = "aws-rfdk.deadline.IPatchVersion"

    @builtins.property # type: ignore
    @jsii.member(jsii_name="patchVersion")
    def patch_version(self) -> jsii.Number:
        """The patch version number."""
        return jsii.get(self, "patchVersion")


@jsii.implements(IPatchVersion)
class Version(metaclass=jsii.JSIIMeta, jsii_type="aws-rfdk.deadline.Version"):
    """This class is reposonsible to do basic operations on version format."""

    def __init__(self, components: typing.List[jsii.Number]) -> None:
        """
        :param components: -
        """
        jsii.create(Version, self, [components])

    @jsii.member(jsii_name="parse")
    @builtins.classmethod
    def parse(cls, version: builtins.str) -> "Version":
        """This method parses the input string and returns the version object.

        :param version: version string to parse.
        """
        return jsii.sinvoke(cls, "parse", [version])

    @jsii.member(jsii_name="isEqual")
    def is_equal(self, version: "Version") -> builtins.bool:
        """This method compares two version strings.

        :param version: -

        :return:

        true if this version is equal to the provided version;
        false otherwise.
        """
        return jsii.invoke(self, "isEqual", [version])

    @jsii.member(jsii_name="isGreaterThan")
    def is_greater_than(self, version: "Version") -> builtins.bool:
        """This method compares two version strings.

        :param version: -

        :return:

        true if this version is greater than the provided version;
        false if this version is less than or equal to the provided verison.
        """
        return jsii.invoke(self, "isGreaterThan", [version])

    @jsii.member(jsii_name="isLessThan")
    def is_less_than(self, version: "Version") -> builtins.bool:
        """This method compares two version strings.

        :param version: -

        :return:

        true if this version is less than the provided version;
        false if this version is greater than or equal to the provided verison.
        """
        return jsii.invoke(self, "isLessThan", [version])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        """The method returns the version components in dot separated string format."""
        return jsii.invoke(self, "toString", [])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="MINIMUM_SUPPORTED_DEADLINE_VERSION")
    def MINIMUM_SUPPORTED_DEADLINE_VERSION(cls) -> "Version":
        """This variable holds the value for minimum supported deadline version."""
        return jsii.sget(cls, "MINIMUM_SUPPORTED_DEADLINE_VERSION")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="majorVersion")
    def major_version(self) -> jsii.Number:
        """The major version number.

        :inheritdoc: true
        """
        return jsii.get(self, "majorVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="minorVersion")
    def minor_version(self) -> jsii.Number:
        """The minor version number.

        :inheritdoc: true
        """
        return jsii.get(self, "minorVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="patchVersion")
    def patch_version(self) -> jsii.Number:
        """The patch version number.

        :inheritdoc: true
        """
        return jsii.get(self, "patchVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> jsii.Number:
        """The release version number.

        :inheritdoc: true
        """
        return jsii.get(self, "releaseVersion")


@jsii.data_type(
    jsii_type="aws-rfdk.deadline.WorkerInstanceFleetProps",
    jsii_struct_bases=[WorkerSettings],
    name_mapping={
        "groups": "groups",
        "pools": "pools",
        "region": "region",
        "render_queue": "renderQueue",
        "vpc": "vpc",
        "worker_machine_image": "workerMachineImage",
        "block_devices": "blockDevices",
        "desired_capacity": "desiredCapacity",
        "health_check_config": "healthCheckConfig",
        "health_monitor": "healthMonitor",
        "instance_type": "instanceType",
        "key_name": "keyName",
        "log_group_props": "logGroupProps",
        "max_capacity": "maxCapacity",
        "min_capacity": "minCapacity",
        "role": "role",
        "security_group": "securityGroup",
        "spot_price": "spotPrice",
        "user_data_provider": "userDataProvider",
        "vpc_subnets": "vpcSubnets",
    },
)
class WorkerInstanceFleetProps(WorkerSettings):
    def __init__(
        self,
        *,
        groups: typing.Optional[typing.List[builtins.str]] = None,
        pools: typing.Optional[typing.List[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        render_queue: IRenderQueue,
        vpc: aws_cdk.aws_ec2.IVpc,
        worker_machine_image: aws_cdk.aws_ec2.IMachineImage,
        block_devices: typing.Optional[typing.List[aws_cdk.aws_autoscaling.BlockDevice]] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        health_check_config: typing.Optional[_HealthCheckConfig_ebe26fb6] = None,
        health_monitor: typing.Optional[_IHealthMonitor_ab248fa9] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        key_name: typing.Optional[builtins.str] = None,
        log_group_props: typing.Optional[_LogGroupFactoryProps_b817ed21] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        spot_price: typing.Optional[jsii.Number] = None,
        user_data_provider: typing.Optional[IInstanceUserDataProvider] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Properties for the Deadline Worker Fleet.

        :param groups: Deadline groups these workers needs to be assigned to. The group is created if it does not already exist. Default: - Worker is not assigned to any group
        :param pools: Deadline pools these workers needs to be assigned to. The pool is created if it does not already exist. Default: - Worker is not assigned to any pool.
        :param region: Deadline region these workers needs to be assigned to. Default: - Worker is not assigned to any region
        :param render_queue: Endpoint for the RenderQueue, to which the worker fleet needs to be connected.
        :param vpc: VPC to launch the worker fleet in.
        :param worker_machine_image: AMI of the deadline worker to launch.
        :param block_devices: 
        :param desired_capacity: Initial amount of workers in the fleet. If this is set to a number, every deployment will reset the amount of workers to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param health_check_config: Properties for configuring a health check. Note: The health-check feature is supported with Deadline Client v10.1.9 and later. Default: properties of HealthCheckConfig applies
        :param health_monitor: Health Monitor component to monitor the health of instances. Note: The health-check feature is supported with Deadline Client v10.1.9 and later. Default: - Health Monitoring is turned-off
        :param instance_type: Type of instance to launch for executing repository installer. Default: - a T2-Large type will be used.
        :param key_name: Name of SSH keypair to grant access to instance. Default: - No SSH access will be possible.
        :param log_group_props: Properties for setting up the Deadline Worker's LogGroup. Default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity, or minCapacity if desiredCapacity is not set
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param role: An IAM role to associate with the instance profile assigned to its resources. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: - A role will automatically be created, it can be accessed via the ``role`` property
        :param security_group: Security Group to assign to this fleet. Default: - create new security group
        :param spot_price: The maximum hourly price($) to be paid for each Spot instance. min - 0.001; max - 255 Default: - launches on-demand EC2 instances.
        :param user_data_provider: An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle. You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        :param vpc_subnets: Where to place the instance within the VPC. Default: - Private subnets.
        """
        if isinstance(health_check_config, dict):
            health_check_config = _HealthCheckConfig_ebe26fb6(**health_check_config)
        if isinstance(log_group_props, dict):
            log_group_props = _LogGroupFactoryProps_b817ed21(**log_group_props)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "render_queue": render_queue,
            "vpc": vpc,
            "worker_machine_image": worker_machine_image,
        }
        if groups is not None:
            self._values["groups"] = groups
        if pools is not None:
            self._values["pools"] = pools
        if region is not None:
            self._values["region"] = region
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if health_check_config is not None:
            self._values["health_check_config"] = health_check_config
        if health_monitor is not None:
            self._values["health_monitor"] = health_monitor
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if key_name is not None:
            self._values["key_name"] = key_name
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if spot_price is not None:
            self._values["spot_price"] = spot_price
        if user_data_provider is not None:
            self._values["user_data_provider"] = user_data_provider
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        """Deadline groups these workers needs to be assigned to.

        The group is
        created if it does not already exist.

        :default: - Worker is not assigned to any group
        """
        result = self._values.get("groups")
        return result

    @builtins.property
    def pools(self) -> typing.Optional[typing.List[builtins.str]]:
        """Deadline pools these workers needs to be assigned to.

        The pool is created
        if it does not already exist.

        :default: - Worker is not assigned to any pool.
        """
        result = self._values.get("pools")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """Deadline region these workers needs to be assigned to.

        :default: - Worker is not assigned to any region
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def render_queue(self) -> IRenderQueue:
        """Endpoint for the RenderQueue, to which the worker fleet needs to be connected."""
        result = self._values.get("render_queue")
        assert result is not None, "Required property 'render_queue' is missing"
        return result

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """VPC to launch the worker fleet in."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def worker_machine_image(self) -> aws_cdk.aws_ec2.IMachineImage:
        """AMI of the deadline worker to launch."""
        result = self._values.get("worker_machine_image")
        assert result is not None, "Required property 'worker_machine_image' is missing"
        return result

    @builtins.property
    def block_devices(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.BlockDevice]]:
        result = self._values.get("block_devices")
        return result

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """Initial amount of workers in the fleet.

        If this is set to a number, every deployment will reset the amount of
        workers to this number. It is recommended to leave this value blank.

        :default: minCapacity, and leave unchanged during deployment
        """
        result = self._values.get("desired_capacity")
        return result

    @builtins.property
    def health_check_config(self) -> typing.Optional[_HealthCheckConfig_ebe26fb6]:
        """Properties for configuring a health check.

        Note: The health-check feature is supported with Deadline Client v10.1.9 and later.

        :default: properties of HealthCheckConfig applies
        """
        result = self._values.get("health_check_config")
        return result

    @builtins.property
    def health_monitor(self) -> typing.Optional[_IHealthMonitor_ab248fa9]:
        """Health Monitor component to monitor the health of instances.

        Note: The health-check feature is supported with Deadline Client v10.1.9 and later.

        :default: - Health Monitoring is turned-off
        """
        result = self._values.get("health_monitor")
        return result

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """Type of instance to launch for executing repository installer.

        :default: - a T2-Large type will be used.
        """
        result = self._values.get("instance_type")
        return result

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        """Name of SSH keypair to grant access to instance.

        :default: - No SSH access will be possible.
        """
        result = self._values.get("key_name")
        return result

    @builtins.property
    def log_group_props(self) -> typing.Optional[_LogGroupFactoryProps_b817ed21]:
        """Properties for setting up the Deadline Worker's LogGroup.

        :default: - LogGroup will be created with all properties' default values and a prefix of "/renderfarm/".
        """
        result = self._values.get("log_group_props")
        return result

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum number of instances in the fleet.

        :default: desiredCapacity, or minCapacity if desiredCapacity is not set
        """
        result = self._values.get("max_capacity")
        return result

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum number of instances in the fleet.

        :default: 1
        """
        result = self._values.get("min_capacity")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """An IAM role to associate with the instance profile assigned to its resources.

        The role must be assumable by the service principal ``ec2.amazonaws.com``:

        :default: - A role will automatically be created, it can be accessed via the ``role`` property

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            role = iam.Role(self, "MyRole",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
            )
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Security Group to assign to this fleet.

        :default: - create new security group
        """
        result = self._values.get("security_group")
        return result

    @builtins.property
    def spot_price(self) -> typing.Optional[jsii.Number]:
        """The maximum hourly price($) to be paid for each Spot instance.

        min - 0.001; max - 255

        :default: - launches on-demand EC2 instances.
        """
        result = self._values.get("spot_price")
        return result

    @builtins.property
    def user_data_provider(self) -> typing.Optional[IInstanceUserDataProvider]:
        """An optional provider of user data commands to be injected at various points during the Worker configuration lifecycle.

        You can provide a subclass of InstanceUserDataProvider with the methods overridden as desired.
        """
        result = self._values.get("user_data_provider")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the instance within the VPC.

        :default: - Private subnets.
        """
        result = self._values.get("vpc_subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkerInstanceFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BuildArgs",
    "DatabaseConnection",
    "DeadlineDockerRecipes",
    "DocDBConnectionOptions",
    "ECSConnectOptions",
    "ECSContainerInstanceProps",
    "ECSDirectConnectProps",
    "ECSTaskProps",
    "IContainerDirectRepositoryConnection",
    "IHost",
    "IInstanceUserDataProvider",
    "IPatchVersion",
    "IReleaseVersion",
    "IRenderQueue",
    "IRepository",
    "IVersion",
    "IWorkerFleet",
    "Installer",
    "InstanceConnectOptions",
    "InstanceDirectConnectProps",
    "InstanceUserDataProvider",
    "Manifest",
    "MongoDbInstanceConnectionOptions",
    "PlatformInstallers",
    "Recipe",
    "RenderQueue",
    "RenderQueueAccessLogProps",
    "RenderQueueExternalTLSProps",
    "RenderQueueHealthCheckConfiguration",
    "RenderQueueHostNameProps",
    "RenderQueueImages",
    "RenderQueueProps",
    "RenderQueueSizeConstraints",
    "RenderQueueTrafficEncryptionProps",
    "Repository",
    "RepositoryBackupOptions",
    "RepositoryProps",
    "RepositoryRemovalPolicies",
    "Stage",
    "StageProps",
    "ThinkboxDockerRecipes",
    "ThinkboxDockerRecipesProps",
    "ThinkboxManagedDeadlineDockerRecipes",
    "UsageBasedLicense",
    "UsageBasedLicenseProps",
    "UsageBasedLicensing",
    "UsageBasedLicensingImages",
    "UsageBasedLicensingProps",
    "Version",
    "VersionQuery",
    "VersionQueryProps",
    "WorkerInstanceConfiguration",
    "WorkerInstanceConfigurationProps",
    "WorkerInstanceFleet",
    "WorkerInstanceFleetProps",
    "WorkerSettings",
]

publication.publish()
