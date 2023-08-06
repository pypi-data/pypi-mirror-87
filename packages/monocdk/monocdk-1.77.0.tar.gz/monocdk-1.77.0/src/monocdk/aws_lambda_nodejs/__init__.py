import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import (
    BundlingDockerImage as _BundlingDockerImage_86dee600,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
)
from ..aws_codeguruprofiler import IProfilingGroup as _IProfilingGroup_418eb20c
from ..aws_ec2 import (
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_iam import (
    IRole as _IRole_59af6f50, PolicyStatement as _PolicyStatement_296fe8a3
)
from ..aws_lambda import (
    FileSystem as _FileSystem_17be1f4c,
    Function as _Function_40b20aa5,
    FunctionOptions as _FunctionOptions_dc75a392,
    IDestination as _IDestination_7f253ff1,
    IEventSource as _IEventSource_7914870e,
    ILayerVersion as _ILayerVersion_b2b86380,
    LogRetentionRetryOptions as _LogRetentionRetryOptions_7acc40ab,
    Runtime as _Runtime_932d369a,
    Tracing as _Tracing_b7f4a8b6,
    VersionOptions as _VersionOptions_085bb455,
)
from ..aws_logs import RetentionDays as _RetentionDays_6c560d31
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_nodejs.BundlingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "build_args": "buildArgs",
        "command_hooks": "commandHooks",
        "docker_image": "dockerImage",
        "environment": "environment",
        "esbuild_version": "esbuildVersion",
        "external_modules": "externalModules",
        "force_docker_bundling": "forceDockerBundling",
        "loader": "loader",
        "minify": "minify",
        "node_modules": "nodeModules",
        "source_map": "sourceMap",
        "target": "target",
    },
)
class BundlingOptions:
    def __init__(
        self,
        *,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        command_hooks: typing.Optional["ICommandHooks"] = None,
        docker_image: typing.Optional[_BundlingDockerImage_86dee600] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        esbuild_version: typing.Optional[builtins.str] = None,
        external_modules: typing.Optional[typing.List[builtins.str]] = None,
        force_docker_bundling: typing.Optional[builtins.bool] = None,
        loader: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        minify: typing.Optional[builtins.bool] = None,
        node_modules: typing.Optional[typing.List[builtins.str]] = None,
        source_map: typing.Optional[builtins.bool] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Bundling options.

        :param build_args: (experimental) Build arguments to pass when building the bundling image. Default: - no build arguments are passed
        :param command_hooks: (experimental) Command hooks. Default: - do not run additional commands
        :param docker_image: (experimental) A custom bundling Docker image. This image should have esbuild installed globally. If you plan to use ``nodeModules`` it should also have ``npm`` or ``yarn`` depending on the lock file you're using. See https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-lambda-nodejs/lib/Dockerfile for the default image provided by @aws-cdk/aws-lambda-nodejs. Default: - use the Docker image provided by
        :param environment: (experimental) Environment variables defined when bundling runs. Default: - no environment variables are defined.
        :param esbuild_version: (experimental) The version of esbuild to use when running in a Docker container. Default: - latest v0
        :param external_modules: (experimental) A list of modules that should be considered as externals (already available in the runtime). Default: ['aws-sdk']
        :param force_docker_bundling: (experimental) Force bundling in a Docker container even if local bundling is possible. This is useful if your function relies on node modules that should be installed (``nodeModules``) in a Lambda compatible environment. Default: false
        :param loader: (experimental) Use loaders to change how a given input file is interpreted. Configuring a loader for a given file type lets you load that file type with an ``import`` statement or a ``require`` call. Default: - use esbuild default loaders
        :param minify: (experimental) Whether to minify files when bundling. Default: false
        :param node_modules: (experimental) A list of modules that should be installed instead of bundled. Modules are installed in a Lambda compatible environnment only when bundling runs in Docker. Default: - all modules are bundled
        :param source_map: (experimental) Whether to include source maps when bundling. Default: false
        :param target: (experimental) Target environment for the generated JavaScript code. Default: - the node version of the runtime

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if build_args is not None:
            self._values["build_args"] = build_args
        if command_hooks is not None:
            self._values["command_hooks"] = command_hooks
        if docker_image is not None:
            self._values["docker_image"] = docker_image
        if environment is not None:
            self._values["environment"] = environment
        if esbuild_version is not None:
            self._values["esbuild_version"] = esbuild_version
        if external_modules is not None:
            self._values["external_modules"] = external_modules
        if force_docker_bundling is not None:
            self._values["force_docker_bundling"] = force_docker_bundling
        if loader is not None:
            self._values["loader"] = loader
        if minify is not None:
            self._values["minify"] = minify
        if node_modules is not None:
            self._values["node_modules"] = node_modules
        if source_map is not None:
            self._values["source_map"] = source_map
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Build arguments to pass when building the bundling image.

        :default: - no build arguments are passed

        :stability: experimental
        """
        result = self._values.get("build_args")
        return result

    @builtins.property
    def command_hooks(self) -> typing.Optional["ICommandHooks"]:
        """(experimental) Command hooks.

        :default: - do not run additional commands

        :stability: experimental
        """
        result = self._values.get("command_hooks")
        return result

    @builtins.property
    def docker_image(self) -> typing.Optional[_BundlingDockerImage_86dee600]:
        """(experimental) A custom bundling Docker image.

        This image should have esbuild installed globally. If you plan to use ``nodeModules``
        it should also have ``npm`` or ``yarn`` depending on the lock file you're using.

        See https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-lambda-nodejs/lib/Dockerfile
        for the default image provided by @aws-cdk/aws-lambda-nodejs.

        :default: - use the Docker image provided by

        :stability: experimental
        :aws-cdk: /aws-lambda-nodejs
        """
        result = self._values.get("docker_image")
        return result

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Environment variables defined when bundling runs.

        :default: - no environment variables are defined.

        :stability: experimental
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def esbuild_version(self) -> typing.Optional[builtins.str]:
        """(experimental) The version of esbuild to use when running in a Docker container.

        :default: - latest v0

        :stability: experimental
        """
        result = self._values.get("esbuild_version")
        return result

    @builtins.property
    def external_modules(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) A list of modules that should be considered as externals (already available in the runtime).

        :default: ['aws-sdk']

        :stability: experimental
        """
        result = self._values.get("external_modules")
        return result

    @builtins.property
    def force_docker_bundling(self) -> typing.Optional[builtins.bool]:
        """(experimental) Force bundling in a Docker container even if local bundling is possible.

        This is useful if your function relies on node modules
        that should be installed (``nodeModules``) in a Lambda compatible
        environment.

        :default: false

        :stability: experimental
        """
        result = self._values.get("force_docker_bundling")
        return result

    @builtins.property
    def loader(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Use loaders to change how a given input file is interpreted.

        Configuring a loader for a given file type lets you load that file type with
        an ``import`` statement or a ``require`` call.

        :default: - use esbuild default loaders

        :see: https://esbuild.github.io/api/#loader
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            ".png""dataurl"
        """
        result = self._values.get("loader")
        return result

    @builtins.property
    def minify(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether to minify files when bundling.

        :default: false

        :stability: experimental
        """
        result = self._values.get("minify")
        return result

    @builtins.property
    def node_modules(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) A list of modules that should be installed instead of bundled.

        Modules are
        installed in a Lambda compatible environnment only when bundling runs in
        Docker.

        :default: - all modules are bundled

        :stability: experimental
        """
        result = self._values.get("node_modules")
        return result

    @builtins.property
    def source_map(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether to include source maps when bundling.

        :default: false

        :stability: experimental
        """
        result = self._values.get("source_map")
        return result

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        """(experimental) Target environment for the generated JavaScript code.

        :default: - the node version of the runtime

        :see: https://esbuild.github.io/api/#target
        :stability: experimental
        """
        result = self._values.get("target")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BundlingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_lambda_nodejs.ICommandHooks")
class ICommandHooks(typing_extensions.Protocol):
    """(experimental) Command hooks.

    These commands will run in the environment in which bundling occurs: inside
    the container for Docker bundling or on the host OS for local bundling.

    Commands are chained with ``&&``.

    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            # Copy a file from the input directory to the output directory
            # to include it in the bundled asset
            after_bundling(input_dir, string, output_dir, string)string[]return [f"cp {inputDir}/my-binary.node {outputDir}"]
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ICommandHooksProxy

    @jsii.member(jsii_name="afterBundling")
    def after_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        """(experimental) Returns commands to run after bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="beforeBundling")
    def before_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        """(experimental) Returns commands to run before bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="beforeInstall")
    def before_install(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        """(experimental) Returns commands to run before installing node modules.

        This hook only runs when node modules are installed.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        """
        ...


class _ICommandHooksProxy:
    """(experimental) Command hooks.

    These commands will run in the environment in which bundling occurs: inside
    the container for Docker bundling or on the host OS for local bundling.

    Commands are chained with ``&&``.

    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            # Copy a file from the input directory to the output directory
            # to include it in the bundled asset
            after_bundling(input_dir, string, output_dir, string)string[]return [f"cp {inputDir}/my-binary.node {outputDir}"]
    """

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_lambda_nodejs.ICommandHooks"

    @jsii.member(jsii_name="afterBundling")
    def after_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        """(experimental) Returns commands to run after bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        """
        return jsii.invoke(self, "afterBundling", [input_dir, output_dir])

    @jsii.member(jsii_name="beforeBundling")
    def before_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        """(experimental) Returns commands to run before bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        """
        return jsii.invoke(self, "beforeBundling", [input_dir, output_dir])

    @jsii.member(jsii_name="beforeInstall")
    def before_install(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        """(experimental) Returns commands to run before installing node modules.

        This hook only runs when node modules are installed.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        """
        return jsii.invoke(self, "beforeInstall", [input_dir, output_dir])


class NodejsFunction(
    _Function_40b20aa5,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_nodejs.NodejsFunction",
):
    """(experimental) A Node.js Lambda function bundled using esbuild.

    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        aws_sdk_connection_reuse: typing.Optional[builtins.bool] = None,
        bundling: typing.Optional[BundlingOptions] = None,
        deps_lock_file_path: typing.Optional[builtins.str] = None,
        entry: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[_Runtime_932d369a] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        current_version_options: typing.Optional[_VersionOptions_085bb455] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        events: typing.Optional[typing.List[_IEventSource_7914870e]] = None,
        filesystem: typing.Optional[_FileSystem_17be1f4c] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        layers: typing.Optional[typing.List[_ILayerVersion_b2b86380]] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        log_retention_retry_options: typing.Optional[_LogRetentionRetryOptions_7acc40ab] = None,
        log_retention_role: typing.Optional[_IRole_59af6f50] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_IProfilingGroup_418eb20c] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        tracing: typing.Optional[_Tracing_b7f4a8b6] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
        max_event_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IDestination_7f253ff1] = None,
        on_success: typing.Optional[_IDestination_7f253ff1] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param aws_sdk_connection_reuse: (experimental) Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript. This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable to ``1``. Default: true
        :param bundling: (experimental) Bundling options. Default: - use default bundling options: no minify, no sourcemap, all modules are bundled.
        :param deps_lock_file_path: (experimental) The path to the dependencies lock file (``yarn.lock`` or ``package-lock.json``). This will be used as the source for the volume mounted in the Docker container. Modules specified in ``nodeModules`` will be installed using the right installer (``npm`` or ``yarn``) along with this lock file. Default: - the path is found by walking up parent directories searching for a ``yarn.lock`` or ``package-lock.json`` file
        :param entry: (experimental) Path to the entry file (JavaScript or TypeScript). Default: - Derived from the name of the defining file and the construct's id. If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts`` and ``stack.my-handler.js``.
        :param handler: (experimental) The name of the exported handler in the entry file. Default: handler
        :param runtime: (experimental) The runtime environment. Only runtimes of the Node.js family are supported. Default: - ``NODEJS_12_X`` if ``process.versions.node`` >= '12.0.0', ``NODEJS_10_X`` otherwise.
        :param allow_all_outbound: (experimental) Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: (experimental) Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param current_version_options: (experimental) Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: (experimental) The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: (experimental) Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: (experimental) A description of the function. Default: - No description.
        :param environment: (experimental) Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: (experimental) Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: (experimental) The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: (experimental) A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: (experimental) Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: (experimental) A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: (experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: (experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: (experimental) The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: (experimental) Enable profiling. Default: - No profiling.
        :param profiling_group: (experimental) Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: (experimental) The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: (experimental) Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: (deprecated) What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: (experimental) The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: (experimental) The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: (experimental) Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: (experimental) VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: (experimental) Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: (experimental) The destination for failed invocations. Default: - no destination
        :param on_success: (experimental) The destination for successful invocations. Default: - no destination
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        :stability: experimental
        """
        props = NodejsFunctionProps(
            aws_sdk_connection_reuse=aws_sdk_connection_reuse,
            bundling=bundling,
            deps_lock_file_path=deps_lock_file_path,
            entry=entry,
            handler=handler,
            runtime=runtime,
            allow_all_outbound=allow_all_outbound,
            allow_public_subnet=allow_public_subnet,
            current_version_options=current_version_options,
            dead_letter_queue=dead_letter_queue,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            description=description,
            environment=environment,
            events=events,
            filesystem=filesystem,
            function_name=function_name,
            initial_policy=initial_policy,
            layers=layers,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            memory_size=memory_size,
            profiling=profiling,
            profiling_group=profiling_group,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            security_group=security_group,
            security_groups=security_groups,
            timeout=timeout,
            tracing=tracing,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        jsii.create(NodejsFunction, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_nodejs.NodejsFunctionProps",
    jsii_struct_bases=[_FunctionOptions_dc75a392],
    name_mapping={
        "max_event_age": "maxEventAge",
        "on_failure": "onFailure",
        "on_success": "onSuccess",
        "retry_attempts": "retryAttempts",
        "allow_all_outbound": "allowAllOutbound",
        "allow_public_subnet": "allowPublicSubnet",
        "current_version_options": "currentVersionOptions",
        "dead_letter_queue": "deadLetterQueue",
        "dead_letter_queue_enabled": "deadLetterQueueEnabled",
        "description": "description",
        "environment": "environment",
        "events": "events",
        "filesystem": "filesystem",
        "function_name": "functionName",
        "initial_policy": "initialPolicy",
        "layers": "layers",
        "log_retention": "logRetention",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "log_retention_role": "logRetentionRole",
        "memory_size": "memorySize",
        "profiling": "profiling",
        "profiling_group": "profilingGroup",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "timeout": "timeout",
        "tracing": "tracing",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "aws_sdk_connection_reuse": "awsSdkConnectionReuse",
        "bundling": "bundling",
        "deps_lock_file_path": "depsLockFilePath",
        "entry": "entry",
        "handler": "handler",
        "runtime": "runtime",
    },
)
class NodejsFunctionProps(_FunctionOptions_dc75a392):
    def __init__(
        self,
        *,
        max_event_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IDestination_7f253ff1] = None,
        on_success: typing.Optional[_IDestination_7f253ff1] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        current_version_options: typing.Optional[_VersionOptions_085bb455] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        events: typing.Optional[typing.List[_IEventSource_7914870e]] = None,
        filesystem: typing.Optional[_FileSystem_17be1f4c] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        layers: typing.Optional[typing.List[_ILayerVersion_b2b86380]] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        log_retention_retry_options: typing.Optional[_LogRetentionRetryOptions_7acc40ab] = None,
        log_retention_role: typing.Optional[_IRole_59af6f50] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_IProfilingGroup_418eb20c] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        tracing: typing.Optional[_Tracing_b7f4a8b6] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
        aws_sdk_connection_reuse: typing.Optional[builtins.bool] = None,
        bundling: typing.Optional[BundlingOptions] = None,
        deps_lock_file_path: typing.Optional[builtins.str] = None,
        entry: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[_Runtime_932d369a] = None,
    ) -> None:
        """(experimental) Properties for a NodejsFunction.

        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: (experimental) The destination for failed invocations. Default: - no destination
        :param on_success: (experimental) The destination for successful invocations. Default: - no destination
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param allow_all_outbound: (experimental) Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: (experimental) Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param current_version_options: (experimental) Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: (experimental) The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: (experimental) Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: (experimental) A description of the function. Default: - No description.
        :param environment: (experimental) Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: (experimental) Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: (experimental) The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: (experimental) A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: (experimental) Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: (experimental) A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: (experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: (experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: (experimental) The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: (experimental) Enable profiling. Default: - No profiling.
        :param profiling_group: (experimental) Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: (experimental) The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: (experimental) Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: (deprecated) What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: (experimental) The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: (experimental) The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: (experimental) Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: (experimental) VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: (experimental) Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param aws_sdk_connection_reuse: (experimental) Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript. This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable to ``1``. Default: true
        :param bundling: (experimental) Bundling options. Default: - use default bundling options: no minify, no sourcemap, all modules are bundled.
        :param deps_lock_file_path: (experimental) The path to the dependencies lock file (``yarn.lock`` or ``package-lock.json``). This will be used as the source for the volume mounted in the Docker container. Modules specified in ``nodeModules`` will be installed using the right installer (``npm`` or ``yarn``) along with this lock file. Default: - the path is found by walking up parent directories searching for a ``yarn.lock`` or ``package-lock.json`` file
        :param entry: (experimental) Path to the entry file (JavaScript or TypeScript). Default: - Derived from the name of the defining file and the construct's id. If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts`` and ``stack.my-handler.js``.
        :param handler: (experimental) The name of the exported handler in the entry file. Default: handler
        :param runtime: (experimental) The runtime environment. Only runtimes of the Node.js family are supported. Default: - ``NODEJS_12_X`` if ``process.versions.node`` >= '12.0.0', ``NODEJS_10_X`` otherwise.

        :stability: experimental
        """
        if isinstance(current_version_options, dict):
            current_version_options = _VersionOptions_085bb455(**current_version_options)
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = _LogRetentionRetryOptions_7acc40ab(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        if isinstance(bundling, dict):
            bundling = BundlingOptions(**bundling)
        self._values: typing.Dict[str, typing.Any] = {}
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if on_success is not None:
            self._values["on_success"] = on_success
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if allow_public_subnet is not None:
            self._values["allow_public_subnet"] = allow_public_subnet
        if current_version_options is not None:
            self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None:
            self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if events is not None:
            self._values["events"] = events
        if filesystem is not None:
            self._values["filesystem"] = filesystem
        if function_name is not None:
            self._values["function_name"] = function_name
        if initial_policy is not None:
            self._values["initial_policy"] = initial_policy
        if layers is not None:
            self._values["layers"] = layers
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None:
            self._values["log_retention_role"] = log_retention_role
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if profiling is not None:
            self._values["profiling"] = profiling
        if profiling_group is not None:
            self._values["profiling_group"] = profiling_group
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if aws_sdk_connection_reuse is not None:
            self._values["aws_sdk_connection_reuse"] = aws_sdk_connection_reuse
        if bundling is not None:
            self._values["bundling"] = bundling
        if deps_lock_file_path is not None:
            self._values["deps_lock_file_path"] = deps_lock_file_path
        if entry is not None:
            self._values["entry"] = entry
        if handler is not None:
            self._values["handler"] = handler
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_070aa057]:
        """(experimental) The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        :default: Duration.hours(6)

        :stability: experimental
        """
        result = self._values.get("max_event_age")
        return result

    @builtins.property
    def on_failure(self) -> typing.Optional[_IDestination_7f253ff1]:
        """(experimental) The destination for failed invocations.

        :default: - no destination

        :stability: experimental
        """
        result = self._values.get("on_failure")
        return result

    @builtins.property
    def on_success(self) -> typing.Optional[_IDestination_7f253ff1]:
        """(experimental) The destination for successful invocations.

        :default: - no destination

        :stability: experimental
        """
        result = self._values.get("on_success")
        return result

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """(experimental) The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        :default: 2

        :stability: experimental
        """
        result = self._values.get("retry_attempts")
        return result

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether to allow the Lambda to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        :default: true

        :stability: experimental
        """
        result = self._values.get("allow_all_outbound")
        return result

    @builtins.property
    def allow_public_subnet(self) -> typing.Optional[builtins.bool]:
        """(experimental) Lambda Functions in a public subnet can NOT access the internet.

        Use this property to acknowledge this limitation and still place the function in a public subnet.

        :default: false

        :see: https://stackoverflow.com/questions/52992085/why-cant-an-aws-lambda-function-inside-a-public-subnet-in-a-vpc-connect-to-the/52994841#52994841
        :stability: experimental
        """
        result = self._values.get("allow_public_subnet")
        return result

    @builtins.property
    def current_version_options(self) -> typing.Optional[_VersionOptions_085bb455]:
        """(experimental) Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        :default: - default options as described in ``VersionOptions``

        :stability: experimental
        """
        result = self._values.get("current_version_options")
        return result

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        """(experimental) The SQS queue to use if DLQ is enabled.

        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``

        :stability: experimental
        """
        result = self._values.get("dead_letter_queue")
        return result

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[builtins.bool]:
        """(experimental) Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.

        :stability: experimental
        """
        result = self._values.get("dead_letter_queue_enabled")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """(experimental) A description of the function.

        :default: - No description.

        :stability: experimental
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        :default: - No environment variables.

        :stability: experimental
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def events(self) -> typing.Optional[typing.List[_IEventSource_7914870e]]:
        """(experimental) Event sources for this function.

        You can also add event sources using ``addEventSource``.

        :default: - No event sources.

        :stability: experimental
        """
        result = self._values.get("events")
        return result

    @builtins.property
    def filesystem(self) -> typing.Optional[_FileSystem_17be1f4c]:
        """(experimental) The filesystem configuration for the lambda function.

        :default: - will not mount any filesystem

        :stability: experimental
        """
        result = self._values.get("filesystem")
        return result

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        """(experimental) A name for the function.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
        ID for the function's name. For more information, see Name Type.

        :stability: experimental
        """
        result = self._values.get("function_name")
        return result

    @builtins.property
    def initial_policy(self) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        """(experimental) Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        :default: - No policy statements are added to the created Lambda role.

        :stability: experimental
        """
        result = self._values.get("initial_policy")
        return result

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[_ILayerVersion_b2b86380]]:
        """(experimental) A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by mulitple functions.

        :default: - No layers.

        :stability: experimental
        """
        result = self._values.get("layers")
        return result

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_6c560d31]:
        """(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.INFINITE

        :stability: experimental
        """
        result = self._values.get("log_retention")
        return result

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional[_LogRetentionRetryOptions_7acc40ab]:
        """(experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        :default: - Default AWS SDK retry options.

        :stability: experimental
        """
        result = self._values.get("log_retention_retry_options")
        return result

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_IRole_59af6f50]:
        """(experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        :default: - A new role is created.

        :stability: experimental
        """
        result = self._values.get("log_retention_role")
        return result

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        """(experimental) The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        :default: 128

        :stability: experimental
        """
        result = self._values.get("memory_size")
        return result

    @builtins.property
    def profiling(self) -> typing.Optional[builtins.bool]:
        """(experimental) Enable profiling.

        :default: - No profiling.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        :stability: experimental
        """
        result = self._values.get("profiling")
        return result

    @builtins.property
    def profiling_group(self) -> typing.Optional[_IProfilingGroup_418eb20c]:
        """(experimental) Profiling Group.

        :default: - A new profiling group will be created if ``profiling`` is set.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        :stability: experimental
        """
        result = self._values.get("profiling_group")
        return result

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """(experimental) The maximum of concurrent executions you want to reserve for the function.

        :default: - No specific limit - account limit.

        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        :stability: experimental
        """
        result = self._values.get("reserved_concurrent_executions")
        return result

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        """(experimental) Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        :default:

        - A unique role will be generated for this lambda function.
        Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.

        :stability: experimental
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_cdbba9d3]:
        """(deprecated) What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead.

        Only used if 'vpc' is supplied.

        Use securityGroups property instead.
        Function constructor will throw an error if both are specified.

        :default:

        - If the function is placed within a VPC and a security group is
        not specified, either by this or securityGroups prop, a dedicated security
        group will be created for this function.

        :deprecated: - This property is deprecated, use securityGroups instead

        :stability: deprecated
        """
        result = self._values.get("security_group")
        return result

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        """(experimental) The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        :default:

        - If the function is placed within a VPC and a security group is
        not specified, either by this or securityGroup prop, a dedicated security
        group will be created for this function.

        :stability: experimental
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        """(experimental) The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        :default: Duration.seconds(3)

        :stability: experimental
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def tracing(self) -> typing.Optional[_Tracing_b7f4a8b6]:
        """(experimental) Enable AWS X-Ray Tracing for Lambda Function.

        :default: Tracing.Disabled

        :stability: experimental
        """
        result = self._values.get("tracing")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        """(experimental) VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.

        :default: - Function is not placed within a VPC.

        :stability: experimental
        """
        result = self._values.get("vpc")
        return result

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        """(experimental) Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied. Note: internet access for Lambdas
        requires a NAT gateway, so picking Public subnets is not allowed.

        :default: - the Vpc default strategy if not specified

        :stability: experimental
        """
        result = self._values.get("vpc_subnets")
        return result

    @builtins.property
    def aws_sdk_connection_reuse(self) -> typing.Optional[builtins.bool]:
        """(experimental) Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript.

        This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable
        to ``1``.

        :default: true

        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/node-reusing-connections.html
        :stability: experimental
        """
        result = self._values.get("aws_sdk_connection_reuse")
        return result

    @builtins.property
    def bundling(self) -> typing.Optional[BundlingOptions]:
        """(experimental) Bundling options.

        :default:

        - use default bundling options: no minify, no sourcemap, all
        modules are bundled.

        :stability: experimental
        """
        result = self._values.get("bundling")
        return result

    @builtins.property
    def deps_lock_file_path(self) -> typing.Optional[builtins.str]:
        """(experimental) The path to the dependencies lock file (``yarn.lock`` or ``package-lock.json``).

        This will be used as the source for the volume mounted in the Docker
        container.

        Modules specified in ``nodeModules`` will be installed using the right
        installer (``npm`` or ``yarn``) along with this lock file.

        :default:

        - the path is found by walking up parent directories searching for
        a ``yarn.lock`` or ``package-lock.json`` file

        :stability: experimental
        """
        result = self._values.get("deps_lock_file_path")
        return result

    @builtins.property
    def entry(self) -> typing.Optional[builtins.str]:
        """(experimental) Path to the entry file (JavaScript or TypeScript).

        :default:

        - Derived from the name of the defining file and the construct's id.
        If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id
        (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts``
        and ``stack.my-handler.js``.

        :stability: experimental
        """
        result = self._values.get("entry")
        return result

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        """(experimental) The name of the exported handler in the entry file.

        :default: handler

        :stability: experimental
        """
        result = self._values.get("handler")
        return result

    @builtins.property
    def runtime(self) -> typing.Optional[_Runtime_932d369a]:
        """(experimental) The runtime environment.

        Only runtimes of the Node.js family are
        supported.

        :default:

        - ``NODEJS_12_X`` if ``process.versions.node`` >= '12.0.0',
        ``NODEJS_10_X`` otherwise.

        :stability: experimental
        """
        result = self._values.get("runtime")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodejsFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BundlingOptions",
    "ICommandHooks",
    "NodejsFunction",
    "NodejsFunctionProps",
]

publication.publish()
