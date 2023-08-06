"""
# AWS OpsWorks Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApp(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opsworks.CfnApp",
):
    """A CloudFormation ``AWS::OpsWorks::App``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html
    :cloudformationResource: AWS::OpsWorks::App
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        stack_id: builtins.str,
        type: builtins.str,
        app_source: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApp.SourceProperty"]] = None,
        attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        data_sources: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApp.DataSourceProperty"]]]] = None,
        description: typing.Optional[builtins.str] = None,
        domains: typing.Optional[typing.List[builtins.str]] = None,
        enable_ssl: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        environment: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApp.EnvironmentVariableProperty"]]]] = None,
        shortname: typing.Optional[builtins.str] = None,
        ssl_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApp.SslConfigurationProperty"]] = None,
    ) -> None:
        """Create a new ``AWS::OpsWorks::App``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::OpsWorks::App.Name``.
        :param stack_id: ``AWS::OpsWorks::App.StackId``.
        :param type: ``AWS::OpsWorks::App.Type``.
        :param app_source: ``AWS::OpsWorks::App.AppSource``.
        :param attributes: ``AWS::OpsWorks::App.Attributes``.
        :param data_sources: ``AWS::OpsWorks::App.DataSources``.
        :param description: ``AWS::OpsWorks::App.Description``.
        :param domains: ``AWS::OpsWorks::App.Domains``.
        :param enable_ssl: ``AWS::OpsWorks::App.EnableSsl``.
        :param environment: ``AWS::OpsWorks::App.Environment``.
        :param shortname: ``AWS::OpsWorks::App.Shortname``.
        :param ssl_configuration: ``AWS::OpsWorks::App.SslConfiguration``.
        """
        props = CfnAppProps(
            name=name,
            stack_id=stack_id,
            type=type,
            app_source=app_source,
            attributes=attributes,
            data_sources=data_sources,
            description=description,
            domains=domains,
            enable_ssl=enable_ssl,
            environment=environment,
            shortname=shortname,
            ssl_configuration=ssl_configuration,
        )

        jsii.create(CfnApp, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::OpsWorks::App.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> builtins.str:
        """``AWS::OpsWorks::App.StackId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-stackid
        """
        return jsii.get(self, "stackId")

    @stack_id.setter # type: ignore
    def stack_id(self, value: builtins.str) -> None:
        jsii.set(self, "stackId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """``AWS::OpsWorks::App.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="appSource")
    def app_source(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApp.SourceProperty"]]:
        """``AWS::OpsWorks::App.AppSource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-appsource
        """
        return jsii.get(self, "appSource")

    @app_source.setter # type: ignore
    def app_source(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApp.SourceProperty"]],
    ) -> None:
        jsii.set(self, "appSource", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::OpsWorks::App.Attributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-attributes
        """
        return jsii.get(self, "attributes")

    @attributes.setter # type: ignore
    def attributes(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "attributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dataSources")
    def data_sources(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApp.DataSourceProperty"]]]]:
        """``AWS::OpsWorks::App.DataSources``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-datasources
        """
        return jsii.get(self, "dataSources")

    @data_sources.setter # type: ignore
    def data_sources(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApp.DataSourceProperty"]]]],
    ) -> None:
        jsii.set(self, "dataSources", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::App.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::App.Domains``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-domains
        """
        return jsii.get(self, "domains")

    @domains.setter # type: ignore
    def domains(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "domains", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enableSsl")
    def enable_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::App.EnableSsl``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-enablessl
        """
        return jsii.get(self, "enableSsl")

    @enable_ssl.setter # type: ignore
    def enable_ssl(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "enableSsl", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApp.EnvironmentVariableProperty"]]]]:
        """``AWS::OpsWorks::App.Environment``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-environment
        """
        return jsii.get(self, "environment")

    @environment.setter # type: ignore
    def environment(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApp.EnvironmentVariableProperty"]]]],
    ) -> None:
        jsii.set(self, "environment", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="shortname")
    def shortname(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::App.Shortname``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-shortname
        """
        return jsii.get(self, "shortname")

    @shortname.setter # type: ignore
    def shortname(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "shortname", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sslConfiguration")
    def ssl_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApp.SslConfigurationProperty"]]:
        """``AWS::OpsWorks::App.SslConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-sslconfiguration
        """
        return jsii.get(self, "sslConfiguration")

    @ssl_configuration.setter # type: ignore
    def ssl_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApp.SslConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "sslConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnApp.DataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "database_name": "databaseName", "type": "type"},
    )
    class DataSourceProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param arn: ``CfnApp.DataSourceProperty.Arn``.
            :param database_name: ``CfnApp.DataSourceProperty.DatabaseName``.
            :param type: ``CfnApp.DataSourceProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if database_name is not None:
                self._values["database_name"] = database_name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            """``CfnApp.DataSourceProperty.Arn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-arn
            """
            result = self._values.get("arn")
            return result

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            """``CfnApp.DataSourceProperty.DatabaseName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-databasename
            """
            result = self._values.get("database_name")
            return result

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            """``CfnApp.DataSourceProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-datasource.html#cfn-opsworks-app-datasource-type
            """
            result = self._values.get("type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnApp.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value", "secure": "secure"},
    )
    class EnvironmentVariableProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            value: builtins.str,
            secure: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param key: ``CfnApp.EnvironmentVariableProperty.Key``.
            :param value: ``CfnApp.EnvironmentVariableProperty.Value``.
            :param secure: ``CfnApp.EnvironmentVariableProperty.Secure``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "value": value,
            }
            if secure is not None:
                self._values["secure"] = secure

        @builtins.property
        def key(self) -> builtins.str:
            """``CfnApp.EnvironmentVariableProperty.Key``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html#cfn-opsworks-app-environment-key
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnApp.EnvironmentVariableProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html#value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        @builtins.property
        def secure(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnApp.EnvironmentVariableProperty.Secure``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-environment.html#cfn-opsworks-app-environment-secure
            """
            result = self._values.get("secure")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnApp.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password": "password",
            "revision": "revision",
            "ssh_key": "sshKey",
            "type": "type",
            "url": "url",
            "username": "username",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            revision: typing.Optional[builtins.str] = None,
            ssh_key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param password: ``CfnApp.SourceProperty.Password``.
            :param revision: ``CfnApp.SourceProperty.Revision``.
            :param ssh_key: ``CfnApp.SourceProperty.SshKey``.
            :param type: ``CfnApp.SourceProperty.Type``.
            :param url: ``CfnApp.SourceProperty.Url``.
            :param username: ``CfnApp.SourceProperty.Username``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if revision is not None:
                self._values["revision"] = revision
            if ssh_key is not None:
                self._values["ssh_key"] = ssh_key
            if type is not None:
                self._values["type"] = type
            if url is not None:
                self._values["url"] = url
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            """``CfnApp.SourceProperty.Password``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-pw
            """
            result = self._values.get("password")
            return result

        @builtins.property
        def revision(self) -> typing.Optional[builtins.str]:
            """``CfnApp.SourceProperty.Revision``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-revision
            """
            result = self._values.get("revision")
            return result

        @builtins.property
        def ssh_key(self) -> typing.Optional[builtins.str]:
            """``CfnApp.SourceProperty.SshKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-sshkey
            """
            result = self._values.get("ssh_key")
            return result

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            """``CfnApp.SourceProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-type
            """
            result = self._values.get("type")
            return result

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            """``CfnApp.SourceProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-url
            """
            result = self._values.get("url")
            return result

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            """``CfnApp.SourceProperty.Username``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-username
            """
            result = self._values.get("username")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnApp.SslConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate": "certificate",
            "chain": "chain",
            "private_key": "privateKey",
        },
    )
    class SslConfigurationProperty:
        def __init__(
            self,
            *,
            certificate: typing.Optional[builtins.str] = None,
            chain: typing.Optional[builtins.str] = None,
            private_key: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param certificate: ``CfnApp.SslConfigurationProperty.Certificate``.
            :param chain: ``CfnApp.SslConfigurationProperty.Chain``.
            :param private_key: ``CfnApp.SslConfigurationProperty.PrivateKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if certificate is not None:
                self._values["certificate"] = certificate
            if chain is not None:
                self._values["chain"] = chain
            if private_key is not None:
                self._values["private_key"] = private_key

        @builtins.property
        def certificate(self) -> typing.Optional[builtins.str]:
            """``CfnApp.SslConfigurationProperty.Certificate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfig-certificate
            """
            result = self._values.get("certificate")
            return result

        @builtins.property
        def chain(self) -> typing.Optional[builtins.str]:
            """``CfnApp.SslConfigurationProperty.Chain``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfig-chain
            """
            result = self._values.get("chain")
            return result

        @builtins.property
        def private_key(self) -> typing.Optional[builtins.str]:
            """``CfnApp.SslConfigurationProperty.PrivateKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-app-sslconfiguration.html#cfn-opsworks-app-sslconfig-privatekey
            """
            result = self._values.get("private_key")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SslConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opsworks.CfnAppProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "stack_id": "stackId",
        "type": "type",
        "app_source": "appSource",
        "attributes": "attributes",
        "data_sources": "dataSources",
        "description": "description",
        "domains": "domains",
        "enable_ssl": "enableSsl",
        "environment": "environment",
        "shortname": "shortname",
        "ssl_configuration": "sslConfiguration",
    },
)
class CfnAppProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        stack_id: builtins.str,
        type: builtins.str,
        app_source: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApp.SourceProperty]] = None,
        attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        data_sources: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApp.DataSourceProperty]]]] = None,
        description: typing.Optional[builtins.str] = None,
        domains: typing.Optional[typing.List[builtins.str]] = None,
        enable_ssl: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        environment: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApp.EnvironmentVariableProperty]]]] = None,
        shortname: typing.Optional[builtins.str] = None,
        ssl_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApp.SslConfigurationProperty]] = None,
    ) -> None:
        """Properties for defining a ``AWS::OpsWorks::App``.

        :param name: ``AWS::OpsWorks::App.Name``.
        :param stack_id: ``AWS::OpsWorks::App.StackId``.
        :param type: ``AWS::OpsWorks::App.Type``.
        :param app_source: ``AWS::OpsWorks::App.AppSource``.
        :param attributes: ``AWS::OpsWorks::App.Attributes``.
        :param data_sources: ``AWS::OpsWorks::App.DataSources``.
        :param description: ``AWS::OpsWorks::App.Description``.
        :param domains: ``AWS::OpsWorks::App.Domains``.
        :param enable_ssl: ``AWS::OpsWorks::App.EnableSsl``.
        :param environment: ``AWS::OpsWorks::App.Environment``.
        :param shortname: ``AWS::OpsWorks::App.Shortname``.
        :param ssl_configuration: ``AWS::OpsWorks::App.SslConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "stack_id": stack_id,
            "type": type,
        }
        if app_source is not None:
            self._values["app_source"] = app_source
        if attributes is not None:
            self._values["attributes"] = attributes
        if data_sources is not None:
            self._values["data_sources"] = data_sources
        if description is not None:
            self._values["description"] = description
        if domains is not None:
            self._values["domains"] = domains
        if enable_ssl is not None:
            self._values["enable_ssl"] = enable_ssl
        if environment is not None:
            self._values["environment"] = environment
        if shortname is not None:
            self._values["shortname"] = shortname
        if ssl_configuration is not None:
            self._values["ssl_configuration"] = ssl_configuration

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::OpsWorks::App.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def stack_id(self) -> builtins.str:
        """``AWS::OpsWorks::App.StackId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-stackid
        """
        result = self._values.get("stack_id")
        assert result is not None, "Required property 'stack_id' is missing"
        return result

    @builtins.property
    def type(self) -> builtins.str:
        """``AWS::OpsWorks::App.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-type
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def app_source(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApp.SourceProperty]]:
        """``AWS::OpsWorks::App.AppSource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-appsource
        """
        result = self._values.get("app_source")
        return result

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::OpsWorks::App.Attributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-attributes
        """
        result = self._values.get("attributes")
        return result

    @builtins.property
    def data_sources(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApp.DataSourceProperty]]]]:
        """``AWS::OpsWorks::App.DataSources``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-datasources
        """
        result = self._values.get("data_sources")
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::App.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::App.Domains``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-domains
        """
        result = self._values.get("domains")
        return result

    @builtins.property
    def enable_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::App.EnableSsl``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-enablessl
        """
        result = self._values.get("enable_ssl")
        return result

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApp.EnvironmentVariableProperty]]]]:
        """``AWS::OpsWorks::App.Environment``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-environment
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def shortname(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::App.Shortname``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-shortname
        """
        result = self._values.get("shortname")
        return result

    @builtins.property
    def ssl_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnApp.SslConfigurationProperty]]:
        """``AWS::OpsWorks::App.SslConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-app.html#cfn-opsworks-app-sslconfiguration
        """
        result = self._values.get("ssl_configuration")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnElasticLoadBalancerAttachment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opsworks.CfnElasticLoadBalancerAttachment",
):
    """A CloudFormation ``AWS::OpsWorks::ElasticLoadBalancerAttachment``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html
    :cloudformationResource: AWS::OpsWorks::ElasticLoadBalancerAttachment
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        elastic_load_balancer_name: builtins.str,
        layer_id: builtins.str,
    ) -> None:
        """Create a new ``AWS::OpsWorks::ElasticLoadBalancerAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param elastic_load_balancer_name: ``AWS::OpsWorks::ElasticLoadBalancerAttachment.ElasticLoadBalancerName``.
        :param layer_id: ``AWS::OpsWorks::ElasticLoadBalancerAttachment.LayerId``.
        """
        props = CfnElasticLoadBalancerAttachmentProps(
            elastic_load_balancer_name=elastic_load_balancer_name, layer_id=layer_id
        )

        jsii.create(CfnElasticLoadBalancerAttachment, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="elasticLoadBalancerName")
    def elastic_load_balancer_name(self) -> builtins.str:
        """``AWS::OpsWorks::ElasticLoadBalancerAttachment.ElasticLoadBalancerName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html#cfn-opsworks-elbattachment-elbname
        """
        return jsii.get(self, "elasticLoadBalancerName")

    @elastic_load_balancer_name.setter # type: ignore
    def elastic_load_balancer_name(self, value: builtins.str) -> None:
        jsii.set(self, "elasticLoadBalancerName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="layerId")
    def layer_id(self) -> builtins.str:
        """``AWS::OpsWorks::ElasticLoadBalancerAttachment.LayerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html#cfn-opsworks-elbattachment-layerid
        """
        return jsii.get(self, "layerId")

    @layer_id.setter # type: ignore
    def layer_id(self, value: builtins.str) -> None:
        jsii.set(self, "layerId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opsworks.CfnElasticLoadBalancerAttachmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "elastic_load_balancer_name": "elasticLoadBalancerName",
        "layer_id": "layerId",
    },
)
class CfnElasticLoadBalancerAttachmentProps:
    def __init__(
        self,
        *,
        elastic_load_balancer_name: builtins.str,
        layer_id: builtins.str,
    ) -> None:
        """Properties for defining a ``AWS::OpsWorks::ElasticLoadBalancerAttachment``.

        :param elastic_load_balancer_name: ``AWS::OpsWorks::ElasticLoadBalancerAttachment.ElasticLoadBalancerName``.
        :param layer_id: ``AWS::OpsWorks::ElasticLoadBalancerAttachment.LayerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "elastic_load_balancer_name": elastic_load_balancer_name,
            "layer_id": layer_id,
        }

    @builtins.property
    def elastic_load_balancer_name(self) -> builtins.str:
        """``AWS::OpsWorks::ElasticLoadBalancerAttachment.ElasticLoadBalancerName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html#cfn-opsworks-elbattachment-elbname
        """
        result = self._values.get("elastic_load_balancer_name")
        assert result is not None, "Required property 'elastic_load_balancer_name' is missing"
        return result

    @builtins.property
    def layer_id(self) -> builtins.str:
        """``AWS::OpsWorks::ElasticLoadBalancerAttachment.LayerId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-elbattachment.html#cfn-opsworks-elbattachment-layerid
        """
        result = self._values.get("layer_id")
        assert result is not None, "Required property 'layer_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnElasticLoadBalancerAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnInstance(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opsworks.CfnInstance",
):
    """A CloudFormation ``AWS::OpsWorks::Instance``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html
    :cloudformationResource: AWS::OpsWorks::Instance
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        instance_type: builtins.str,
        layer_ids: typing.List[builtins.str],
        stack_id: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        ami_id: typing.Optional[builtins.str] = None,
        architecture: typing.Optional[builtins.str] = None,
        auto_scaling_type: typing.Optional[builtins.str] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        block_device_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnInstance.BlockDeviceMappingProperty"]]]] = None,
        ebs_optimized: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        elastic_ips: typing.Optional[typing.List[builtins.str]] = None,
        hostname: typing.Optional[builtins.str] = None,
        install_updates_on_boot: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        os: typing.Optional[builtins.str] = None,
        root_device_type: typing.Optional[builtins.str] = None,
        ssh_key_name: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tenancy: typing.Optional[builtins.str] = None,
        time_based_auto_scaling: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnInstance.TimeBasedAutoScalingProperty"]] = None,
        virtualization_type: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Create a new ``AWS::OpsWorks::Instance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_type: ``AWS::OpsWorks::Instance.InstanceType``.
        :param layer_ids: ``AWS::OpsWorks::Instance.LayerIds``.
        :param stack_id: ``AWS::OpsWorks::Instance.StackId``.
        :param agent_version: ``AWS::OpsWorks::Instance.AgentVersion``.
        :param ami_id: ``AWS::OpsWorks::Instance.AmiId``.
        :param architecture: ``AWS::OpsWorks::Instance.Architecture``.
        :param auto_scaling_type: ``AWS::OpsWorks::Instance.AutoScalingType``.
        :param availability_zone: ``AWS::OpsWorks::Instance.AvailabilityZone``.
        :param block_device_mappings: ``AWS::OpsWorks::Instance.BlockDeviceMappings``.
        :param ebs_optimized: ``AWS::OpsWorks::Instance.EbsOptimized``.
        :param elastic_ips: ``AWS::OpsWorks::Instance.ElasticIps``.
        :param hostname: ``AWS::OpsWorks::Instance.Hostname``.
        :param install_updates_on_boot: ``AWS::OpsWorks::Instance.InstallUpdatesOnBoot``.
        :param os: ``AWS::OpsWorks::Instance.Os``.
        :param root_device_type: ``AWS::OpsWorks::Instance.RootDeviceType``.
        :param ssh_key_name: ``AWS::OpsWorks::Instance.SshKeyName``.
        :param subnet_id: ``AWS::OpsWorks::Instance.SubnetId``.
        :param tenancy: ``AWS::OpsWorks::Instance.Tenancy``.
        :param time_based_auto_scaling: ``AWS::OpsWorks::Instance.TimeBasedAutoScaling``.
        :param virtualization_type: ``AWS::OpsWorks::Instance.VirtualizationType``.
        :param volumes: ``AWS::OpsWorks::Instance.Volumes``.
        """
        props = CfnInstanceProps(
            instance_type=instance_type,
            layer_ids=layer_ids,
            stack_id=stack_id,
            agent_version=agent_version,
            ami_id=ami_id,
            architecture=architecture,
            auto_scaling_type=auto_scaling_type,
            availability_zone=availability_zone,
            block_device_mappings=block_device_mappings,
            ebs_optimized=ebs_optimized,
            elastic_ips=elastic_ips,
            hostname=hostname,
            install_updates_on_boot=install_updates_on_boot,
            os=os,
            root_device_type=root_device_type,
            ssh_key_name=ssh_key_name,
            subnet_id=subnet_id,
            tenancy=tenancy,
            time_based_auto_scaling=time_based_auto_scaling,
            virtualization_type=virtualization_type,
            volumes=volumes,
        )

        jsii.create(CfnInstance, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrAvailabilityZone")
    def attr_availability_zone(self) -> builtins.str:
        """
        :cloudformationAttribute: AvailabilityZone
        """
        return jsii.get(self, "attrAvailabilityZone")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrPrivateDnsName")
    def attr_private_dns_name(self) -> builtins.str:
        """
        :cloudformationAttribute: PrivateDnsName
        """
        return jsii.get(self, "attrPrivateDnsName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrPrivateIp")
    def attr_private_ip(self) -> builtins.str:
        """
        :cloudformationAttribute: PrivateIp
        """
        return jsii.get(self, "attrPrivateIp")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrPublicDnsName")
    def attr_public_dns_name(self) -> builtins.str:
        """
        :cloudformationAttribute: PublicDnsName
        """
        return jsii.get(self, "attrPublicDnsName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrPublicIp")
    def attr_public_ip(self) -> builtins.str:
        """
        :cloudformationAttribute: PublicIp
        """
        return jsii.get(self, "attrPublicIp")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        """``AWS::OpsWorks::Instance.InstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-instancetype
        """
        return jsii.get(self, "instanceType")

    @instance_type.setter # type: ignore
    def instance_type(self, value: builtins.str) -> None:
        jsii.set(self, "instanceType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="layerIds")
    def layer_ids(self) -> typing.List[builtins.str]:
        """``AWS::OpsWorks::Instance.LayerIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-layerids
        """
        return jsii.get(self, "layerIds")

    @layer_ids.setter # type: ignore
    def layer_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "layerIds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> builtins.str:
        """``AWS::OpsWorks::Instance.StackId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-stackid
        """
        return jsii.get(self, "stackId")

    @stack_id.setter # type: ignore
    def stack_id(self, value: builtins.str) -> None:
        jsii.set(self, "stackId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="agentVersion")
    def agent_version(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.AgentVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-agentversion
        """
        return jsii.get(self, "agentVersion")

    @agent_version.setter # type: ignore
    def agent_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "agentVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="amiId")
    def ami_id(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.AmiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-amiid
        """
        return jsii.get(self, "amiId")

    @ami_id.setter # type: ignore
    def ami_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "amiId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.Architecture``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-architecture
        """
        return jsii.get(self, "architecture")

    @architecture.setter # type: ignore
    def architecture(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "architecture", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoScalingType")
    def auto_scaling_type(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.AutoScalingType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-autoscalingtype
        """
        return jsii.get(self, "autoScalingType")

    @auto_scaling_type.setter # type: ignore
    def auto_scaling_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "autoScalingType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.AvailabilityZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-availabilityzone
        """
        return jsii.get(self, "availabilityZone")

    @availability_zone.setter # type: ignore
    def availability_zone(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "availabilityZone", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="blockDeviceMappings")
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnInstance.BlockDeviceMappingProperty"]]]]:
        """``AWS::OpsWorks::Instance.BlockDeviceMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-blockdevicemappings
        """
        return jsii.get(self, "blockDeviceMappings")

    @block_device_mappings.setter # type: ignore
    def block_device_mappings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnInstance.BlockDeviceMappingProperty"]]]],
    ) -> None:
        jsii.set(self, "blockDeviceMappings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ebsOptimized")
    def ebs_optimized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Instance.EbsOptimized``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-ebsoptimized
        """
        return jsii.get(self, "ebsOptimized")

    @ebs_optimized.setter # type: ignore
    def ebs_optimized(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "ebsOptimized", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="elasticIps")
    def elastic_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::Instance.ElasticIps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-elasticips
        """
        return jsii.get(self, "elasticIps")

    @elastic_ips.setter # type: ignore
    def elastic_ips(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "elasticIps", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.Hostname``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-hostname
        """
        return jsii.get(self, "hostname")

    @hostname.setter # type: ignore
    def hostname(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "hostname", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="installUpdatesOnBoot")
    def install_updates_on_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Instance.InstallUpdatesOnBoot``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-installupdatesonboot
        """
        return jsii.get(self, "installUpdatesOnBoot")

    @install_updates_on_boot.setter # type: ignore
    def install_updates_on_boot(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "installUpdatesOnBoot", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="os")
    def os(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.Os``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-os
        """
        return jsii.get(self, "os")

    @os.setter # type: ignore
    def os(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "os", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rootDeviceType")
    def root_device_type(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.RootDeviceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-rootdevicetype
        """
        return jsii.get(self, "rootDeviceType")

    @root_device_type.setter # type: ignore
    def root_device_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "rootDeviceType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sshKeyName")
    def ssh_key_name(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.SshKeyName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-sshkeyname
        """
        return jsii.get(self, "sshKeyName")

    @ssh_key_name.setter # type: ignore
    def ssh_key_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sshKeyName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.SubnetId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-subnetid
        """
        return jsii.get(self, "subnetId")

    @subnet_id.setter # type: ignore
    def subnet_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "subnetId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tenancy")
    def tenancy(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.Tenancy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-tenancy
        """
        return jsii.get(self, "tenancy")

    @tenancy.setter # type: ignore
    def tenancy(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "tenancy", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="timeBasedAutoScaling")
    def time_based_auto_scaling(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnInstance.TimeBasedAutoScalingProperty"]]:
        """``AWS::OpsWorks::Instance.TimeBasedAutoScaling``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-timebasedautoscaling
        """
        return jsii.get(self, "timeBasedAutoScaling")

    @time_based_auto_scaling.setter # type: ignore
    def time_based_auto_scaling(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnInstance.TimeBasedAutoScalingProperty"]],
    ) -> None:
        jsii.set(self, "timeBasedAutoScaling", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="virtualizationType")
    def virtualization_type(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.VirtualizationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-virtualizationtype
        """
        return jsii.get(self, "virtualizationType")

    @virtualization_type.setter # type: ignore
    def virtualization_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "virtualizationType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::Instance.Volumes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-volumes
        """
        return jsii.get(self, "volumes")

    @volumes.setter # type: ignore
    def volumes(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "volumes", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnInstance.BlockDeviceMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "device_name": "deviceName",
            "ebs": "ebs",
            "no_device": "noDevice",
            "virtual_name": "virtualName",
        },
    )
    class BlockDeviceMappingProperty:
        def __init__(
            self,
            *,
            device_name: typing.Optional[builtins.str] = None,
            ebs: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnInstance.EbsBlockDeviceProperty"]] = None,
            no_device: typing.Optional[builtins.str] = None,
            virtual_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param device_name: ``CfnInstance.BlockDeviceMappingProperty.DeviceName``.
            :param ebs: ``CfnInstance.BlockDeviceMappingProperty.Ebs``.
            :param no_device: ``CfnInstance.BlockDeviceMappingProperty.NoDevice``.
            :param virtual_name: ``CfnInstance.BlockDeviceMappingProperty.VirtualName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if device_name is not None:
                self._values["device_name"] = device_name
            if ebs is not None:
                self._values["ebs"] = ebs
            if no_device is not None:
                self._values["no_device"] = no_device
            if virtual_name is not None:
                self._values["virtual_name"] = virtual_name

        @builtins.property
        def device_name(self) -> typing.Optional[builtins.str]:
            """``CfnInstance.BlockDeviceMappingProperty.DeviceName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-devicename
            """
            result = self._values.get("device_name")
            return result

        @builtins.property
        def ebs(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnInstance.EbsBlockDeviceProperty"]]:
            """``CfnInstance.BlockDeviceMappingProperty.Ebs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-ebs
            """
            result = self._values.get("ebs")
            return result

        @builtins.property
        def no_device(self) -> typing.Optional[builtins.str]:
            """``CfnInstance.BlockDeviceMappingProperty.NoDevice``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-nodevice
            """
            result = self._values.get("no_device")
            return result

        @builtins.property
        def virtual_name(self) -> typing.Optional[builtins.str]:
            """``CfnInstance.BlockDeviceMappingProperty.VirtualName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-blockdevicemapping.html#cfn-opsworks-instance-blockdevicemapping-virtualname
            """
            result = self._values.get("virtual_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlockDeviceMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnInstance.EbsBlockDeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_on_termination": "deleteOnTermination",
            "iops": "iops",
            "snapshot_id": "snapshotId",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class EbsBlockDeviceProperty:
        def __init__(
            self,
            *,
            delete_on_termination: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            iops: typing.Optional[jsii.Number] = None,
            snapshot_id: typing.Optional[builtins.str] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param delete_on_termination: ``CfnInstance.EbsBlockDeviceProperty.DeleteOnTermination``.
            :param iops: ``CfnInstance.EbsBlockDeviceProperty.Iops``.
            :param snapshot_id: ``CfnInstance.EbsBlockDeviceProperty.SnapshotId``.
            :param volume_size: ``CfnInstance.EbsBlockDeviceProperty.VolumeSize``.
            :param volume_type: ``CfnInstance.EbsBlockDeviceProperty.VolumeType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if delete_on_termination is not None:
                self._values["delete_on_termination"] = delete_on_termination
            if iops is not None:
                self._values["iops"] = iops
            if snapshot_id is not None:
                self._values["snapshot_id"] = snapshot_id
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def delete_on_termination(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnInstance.EbsBlockDeviceProperty.DeleteOnTermination``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-deleteontermination
            """
            result = self._values.get("delete_on_termination")
            return result

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            """``CfnInstance.EbsBlockDeviceProperty.Iops``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-iops
            """
            result = self._values.get("iops")
            return result

        @builtins.property
        def snapshot_id(self) -> typing.Optional[builtins.str]:
            """``CfnInstance.EbsBlockDeviceProperty.SnapshotId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-snapshotid
            """
            result = self._values.get("snapshot_id")
            return result

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            """``CfnInstance.EbsBlockDeviceProperty.VolumeSize``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-volumesize
            """
            result = self._values.get("volume_size")
            return result

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            """``CfnInstance.EbsBlockDeviceProperty.VolumeType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-ebsblockdevice.html#cfn-opsworks-instance-ebsblockdevice-volumetype
            """
            result = self._values.get("volume_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsBlockDeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnInstance.TimeBasedAutoScalingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "friday": "friday",
            "monday": "monday",
            "saturday": "saturday",
            "sunday": "sunday",
            "thursday": "thursday",
            "tuesday": "tuesday",
            "wednesday": "wednesday",
        },
    )
    class TimeBasedAutoScalingProperty:
        def __init__(
            self,
            *,
            friday: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            monday: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            saturday: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            sunday: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            thursday: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            tuesday: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            wednesday: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            """
            :param friday: ``CfnInstance.TimeBasedAutoScalingProperty.Friday``.
            :param monday: ``CfnInstance.TimeBasedAutoScalingProperty.Monday``.
            :param saturday: ``CfnInstance.TimeBasedAutoScalingProperty.Saturday``.
            :param sunday: ``CfnInstance.TimeBasedAutoScalingProperty.Sunday``.
            :param thursday: ``CfnInstance.TimeBasedAutoScalingProperty.Thursday``.
            :param tuesday: ``CfnInstance.TimeBasedAutoScalingProperty.Tuesday``.
            :param wednesday: ``CfnInstance.TimeBasedAutoScalingProperty.Wednesday``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if friday is not None:
                self._values["friday"] = friday
            if monday is not None:
                self._values["monday"] = monday
            if saturday is not None:
                self._values["saturday"] = saturday
            if sunday is not None:
                self._values["sunday"] = sunday
            if thursday is not None:
                self._values["thursday"] = thursday
            if tuesday is not None:
                self._values["tuesday"] = tuesday
            if wednesday is not None:
                self._values["wednesday"] = wednesday

        @builtins.property
        def friday(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnInstance.TimeBasedAutoScalingProperty.Friday``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-friday
            """
            result = self._values.get("friday")
            return result

        @builtins.property
        def monday(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnInstance.TimeBasedAutoScalingProperty.Monday``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-monday
            """
            result = self._values.get("monday")
            return result

        @builtins.property
        def saturday(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnInstance.TimeBasedAutoScalingProperty.Saturday``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-saturday
            """
            result = self._values.get("saturday")
            return result

        @builtins.property
        def sunday(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnInstance.TimeBasedAutoScalingProperty.Sunday``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-sunday
            """
            result = self._values.get("sunday")
            return result

        @builtins.property
        def thursday(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnInstance.TimeBasedAutoScalingProperty.Thursday``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-thursday
            """
            result = self._values.get("thursday")
            return result

        @builtins.property
        def tuesday(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnInstance.TimeBasedAutoScalingProperty.Tuesday``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-tuesday
            """
            result = self._values.get("tuesday")
            return result

        @builtins.property
        def wednesday(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            """``CfnInstance.TimeBasedAutoScalingProperty.Wednesday``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-instance-timebasedautoscaling.html#cfn-opsworks-instance-timebasedautoscaling-wednesday
            """
            result = self._values.get("wednesday")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeBasedAutoScalingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opsworks.CfnInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "layer_ids": "layerIds",
        "stack_id": "stackId",
        "agent_version": "agentVersion",
        "ami_id": "amiId",
        "architecture": "architecture",
        "auto_scaling_type": "autoScalingType",
        "availability_zone": "availabilityZone",
        "block_device_mappings": "blockDeviceMappings",
        "ebs_optimized": "ebsOptimized",
        "elastic_ips": "elasticIps",
        "hostname": "hostname",
        "install_updates_on_boot": "installUpdatesOnBoot",
        "os": "os",
        "root_device_type": "rootDeviceType",
        "ssh_key_name": "sshKeyName",
        "subnet_id": "subnetId",
        "tenancy": "tenancy",
        "time_based_auto_scaling": "timeBasedAutoScaling",
        "virtualization_type": "virtualizationType",
        "volumes": "volumes",
    },
)
class CfnInstanceProps:
    def __init__(
        self,
        *,
        instance_type: builtins.str,
        layer_ids: typing.List[builtins.str],
        stack_id: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        ami_id: typing.Optional[builtins.str] = None,
        architecture: typing.Optional[builtins.str] = None,
        auto_scaling_type: typing.Optional[builtins.str] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        block_device_mappings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnInstance.BlockDeviceMappingProperty]]]] = None,
        ebs_optimized: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        elastic_ips: typing.Optional[typing.List[builtins.str]] = None,
        hostname: typing.Optional[builtins.str] = None,
        install_updates_on_boot: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        os: typing.Optional[builtins.str] = None,
        root_device_type: typing.Optional[builtins.str] = None,
        ssh_key_name: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tenancy: typing.Optional[builtins.str] = None,
        time_based_auto_scaling: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnInstance.TimeBasedAutoScalingProperty]] = None,
        virtualization_type: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::OpsWorks::Instance``.

        :param instance_type: ``AWS::OpsWorks::Instance.InstanceType``.
        :param layer_ids: ``AWS::OpsWorks::Instance.LayerIds``.
        :param stack_id: ``AWS::OpsWorks::Instance.StackId``.
        :param agent_version: ``AWS::OpsWorks::Instance.AgentVersion``.
        :param ami_id: ``AWS::OpsWorks::Instance.AmiId``.
        :param architecture: ``AWS::OpsWorks::Instance.Architecture``.
        :param auto_scaling_type: ``AWS::OpsWorks::Instance.AutoScalingType``.
        :param availability_zone: ``AWS::OpsWorks::Instance.AvailabilityZone``.
        :param block_device_mappings: ``AWS::OpsWorks::Instance.BlockDeviceMappings``.
        :param ebs_optimized: ``AWS::OpsWorks::Instance.EbsOptimized``.
        :param elastic_ips: ``AWS::OpsWorks::Instance.ElasticIps``.
        :param hostname: ``AWS::OpsWorks::Instance.Hostname``.
        :param install_updates_on_boot: ``AWS::OpsWorks::Instance.InstallUpdatesOnBoot``.
        :param os: ``AWS::OpsWorks::Instance.Os``.
        :param root_device_type: ``AWS::OpsWorks::Instance.RootDeviceType``.
        :param ssh_key_name: ``AWS::OpsWorks::Instance.SshKeyName``.
        :param subnet_id: ``AWS::OpsWorks::Instance.SubnetId``.
        :param tenancy: ``AWS::OpsWorks::Instance.Tenancy``.
        :param time_based_auto_scaling: ``AWS::OpsWorks::Instance.TimeBasedAutoScaling``.
        :param virtualization_type: ``AWS::OpsWorks::Instance.VirtualizationType``.
        :param volumes: ``AWS::OpsWorks::Instance.Volumes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "instance_type": instance_type,
            "layer_ids": layer_ids,
            "stack_id": stack_id,
        }
        if agent_version is not None:
            self._values["agent_version"] = agent_version
        if ami_id is not None:
            self._values["ami_id"] = ami_id
        if architecture is not None:
            self._values["architecture"] = architecture
        if auto_scaling_type is not None:
            self._values["auto_scaling_type"] = auto_scaling_type
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if block_device_mappings is not None:
            self._values["block_device_mappings"] = block_device_mappings
        if ebs_optimized is not None:
            self._values["ebs_optimized"] = ebs_optimized
        if elastic_ips is not None:
            self._values["elastic_ips"] = elastic_ips
        if hostname is not None:
            self._values["hostname"] = hostname
        if install_updates_on_boot is not None:
            self._values["install_updates_on_boot"] = install_updates_on_boot
        if os is not None:
            self._values["os"] = os
        if root_device_type is not None:
            self._values["root_device_type"] = root_device_type
        if ssh_key_name is not None:
            self._values["ssh_key_name"] = ssh_key_name
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tenancy is not None:
            self._values["tenancy"] = tenancy
        if time_based_auto_scaling is not None:
            self._values["time_based_auto_scaling"] = time_based_auto_scaling
        if virtualization_type is not None:
            self._values["virtualization_type"] = virtualization_type
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def instance_type(self) -> builtins.str:
        """``AWS::OpsWorks::Instance.InstanceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-instancetype
        """
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return result

    @builtins.property
    def layer_ids(self) -> typing.List[builtins.str]:
        """``AWS::OpsWorks::Instance.LayerIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-layerids
        """
        result = self._values.get("layer_ids")
        assert result is not None, "Required property 'layer_ids' is missing"
        return result

    @builtins.property
    def stack_id(self) -> builtins.str:
        """``AWS::OpsWorks::Instance.StackId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-stackid
        """
        result = self._values.get("stack_id")
        assert result is not None, "Required property 'stack_id' is missing"
        return result

    @builtins.property
    def agent_version(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.AgentVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-agentversion
        """
        result = self._values.get("agent_version")
        return result

    @builtins.property
    def ami_id(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.AmiId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-amiid
        """
        result = self._values.get("ami_id")
        return result

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.Architecture``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-architecture
        """
        result = self._values.get("architecture")
        return result

    @builtins.property
    def auto_scaling_type(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.AutoScalingType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-autoscalingtype
        """
        result = self._values.get("auto_scaling_type")
        return result

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.AvailabilityZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-availabilityzone
        """
        result = self._values.get("availability_zone")
        return result

    @builtins.property
    def block_device_mappings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnInstance.BlockDeviceMappingProperty]]]]:
        """``AWS::OpsWorks::Instance.BlockDeviceMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-blockdevicemappings
        """
        result = self._values.get("block_device_mappings")
        return result

    @builtins.property
    def ebs_optimized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Instance.EbsOptimized``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-ebsoptimized
        """
        result = self._values.get("ebs_optimized")
        return result

    @builtins.property
    def elastic_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::Instance.ElasticIps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-elasticips
        """
        result = self._values.get("elastic_ips")
        return result

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.Hostname``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-hostname
        """
        result = self._values.get("hostname")
        return result

    @builtins.property
    def install_updates_on_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Instance.InstallUpdatesOnBoot``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-installupdatesonboot
        """
        result = self._values.get("install_updates_on_boot")
        return result

    @builtins.property
    def os(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.Os``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-os
        """
        result = self._values.get("os")
        return result

    @builtins.property
    def root_device_type(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.RootDeviceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-rootdevicetype
        """
        result = self._values.get("root_device_type")
        return result

    @builtins.property
    def ssh_key_name(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.SshKeyName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-sshkeyname
        """
        result = self._values.get("ssh_key_name")
        return result

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.SubnetId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-subnetid
        """
        result = self._values.get("subnet_id")
        return result

    @builtins.property
    def tenancy(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.Tenancy``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-tenancy
        """
        result = self._values.get("tenancy")
        return result

    @builtins.property
    def time_based_auto_scaling(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnInstance.TimeBasedAutoScalingProperty]]:
        """``AWS::OpsWorks::Instance.TimeBasedAutoScaling``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-timebasedautoscaling
        """
        result = self._values.get("time_based_auto_scaling")
        return result

    @builtins.property
    def virtualization_type(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Instance.VirtualizationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-virtualizationtype
        """
        result = self._values.get("virtualization_type")
        return result

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::Instance.Volumes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-instance.html#cfn-opsworks-instance-volumes
        """
        result = self._values.get("volumes")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnLayer(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opsworks.CfnLayer",
):
    """A CloudFormation ``AWS::OpsWorks::Layer``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html
    :cloudformationResource: AWS::OpsWorks::Layer
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        auto_assign_elastic_ips: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        auto_assign_public_ips: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        enable_auto_healing: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        name: builtins.str,
        shortname: builtins.str,
        stack_id: builtins.str,
        type: builtins.str,
        attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        custom_instance_profile_arn: typing.Optional[builtins.str] = None,
        custom_json: typing.Any = None,
        custom_recipes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.RecipesProperty"]] = None,
        custom_security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
        install_updates_on_boot: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        lifecycle_event_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.LifecycleEventConfigurationProperty"]] = None,
        load_based_auto_scaling: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.LoadBasedAutoScalingProperty"]] = None,
        packages: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        use_ebs_optimized_instances: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        volume_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.VolumeConfigurationProperty"]]]] = None,
    ) -> None:
        """Create a new ``AWS::OpsWorks::Layer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auto_assign_elastic_ips: ``AWS::OpsWorks::Layer.AutoAssignElasticIps``.
        :param auto_assign_public_ips: ``AWS::OpsWorks::Layer.AutoAssignPublicIps``.
        :param enable_auto_healing: ``AWS::OpsWorks::Layer.EnableAutoHealing``.
        :param name: ``AWS::OpsWorks::Layer.Name``.
        :param shortname: ``AWS::OpsWorks::Layer.Shortname``.
        :param stack_id: ``AWS::OpsWorks::Layer.StackId``.
        :param type: ``AWS::OpsWorks::Layer.Type``.
        :param attributes: ``AWS::OpsWorks::Layer.Attributes``.
        :param custom_instance_profile_arn: ``AWS::OpsWorks::Layer.CustomInstanceProfileArn``.
        :param custom_json: ``AWS::OpsWorks::Layer.CustomJson``.
        :param custom_recipes: ``AWS::OpsWorks::Layer.CustomRecipes``.
        :param custom_security_group_ids: ``AWS::OpsWorks::Layer.CustomSecurityGroupIds``.
        :param install_updates_on_boot: ``AWS::OpsWorks::Layer.InstallUpdatesOnBoot``.
        :param lifecycle_event_configuration: ``AWS::OpsWorks::Layer.LifecycleEventConfiguration``.
        :param load_based_auto_scaling: ``AWS::OpsWorks::Layer.LoadBasedAutoScaling``.
        :param packages: ``AWS::OpsWorks::Layer.Packages``.
        :param tags: ``AWS::OpsWorks::Layer.Tags``.
        :param use_ebs_optimized_instances: ``AWS::OpsWorks::Layer.UseEbsOptimizedInstances``.
        :param volume_configurations: ``AWS::OpsWorks::Layer.VolumeConfigurations``.
        """
        props = CfnLayerProps(
            auto_assign_elastic_ips=auto_assign_elastic_ips,
            auto_assign_public_ips=auto_assign_public_ips,
            enable_auto_healing=enable_auto_healing,
            name=name,
            shortname=shortname,
            stack_id=stack_id,
            type=type,
            attributes=attributes,
            custom_instance_profile_arn=custom_instance_profile_arn,
            custom_json=custom_json,
            custom_recipes=custom_recipes,
            custom_security_group_ids=custom_security_group_ids,
            install_updates_on_boot=install_updates_on_boot,
            lifecycle_event_configuration=lifecycle_event_configuration,
            load_based_auto_scaling=load_based_auto_scaling,
            packages=packages,
            tags=tags,
            use_ebs_optimized_instances=use_ebs_optimized_instances,
            volume_configurations=volume_configurations,
        )

        jsii.create(CfnLayer, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::OpsWorks::Layer.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoAssignElasticIps")
    def auto_assign_elastic_ips(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::OpsWorks::Layer.AutoAssignElasticIps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignelasticips
        """
        return jsii.get(self, "autoAssignElasticIps")

    @auto_assign_elastic_ips.setter # type: ignore
    def auto_assign_elastic_ips(
        self,
        value: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "autoAssignElasticIps", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoAssignPublicIps")
    def auto_assign_public_ips(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::OpsWorks::Layer.AutoAssignPublicIps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignpublicips
        """
        return jsii.get(self, "autoAssignPublicIps")

    @auto_assign_public_ips.setter # type: ignore
    def auto_assign_public_ips(
        self,
        value: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "autoAssignPublicIps", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="customJson")
    def custom_json(self) -> typing.Any:
        """``AWS::OpsWorks::Layer.CustomJson``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customjson
        """
        return jsii.get(self, "customJson")

    @custom_json.setter # type: ignore
    def custom_json(self, value: typing.Any) -> None:
        jsii.set(self, "customJson", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enableAutoHealing")
    def enable_auto_healing(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::OpsWorks::Layer.EnableAutoHealing``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-enableautohealing
        """
        return jsii.get(self, "enableAutoHealing")

    @enable_auto_healing.setter # type: ignore
    def enable_auto_healing(
        self,
        value: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "enableAutoHealing", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::OpsWorks::Layer.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="shortname")
    def shortname(self) -> builtins.str:
        """``AWS::OpsWorks::Layer.Shortname``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-shortname
        """
        return jsii.get(self, "shortname")

    @shortname.setter # type: ignore
    def shortname(self, value: builtins.str) -> None:
        jsii.set(self, "shortname", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> builtins.str:
        """``AWS::OpsWorks::Layer.StackId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-stackid
        """
        return jsii.get(self, "stackId")

    @stack_id.setter # type: ignore
    def stack_id(self, value: builtins.str) -> None:
        jsii.set(self, "stackId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """``AWS::OpsWorks::Layer.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::OpsWorks::Layer.Attributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-attributes
        """
        return jsii.get(self, "attributes")

    @attributes.setter # type: ignore
    def attributes(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "attributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="customInstanceProfileArn")
    def custom_instance_profile_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Layer.CustomInstanceProfileArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-custominstanceprofilearn
        """
        return jsii.get(self, "customInstanceProfileArn")

    @custom_instance_profile_arn.setter # type: ignore
    def custom_instance_profile_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "customInstanceProfileArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="customRecipes")
    def custom_recipes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.RecipesProperty"]]:
        """``AWS::OpsWorks::Layer.CustomRecipes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customrecipes
        """
        return jsii.get(self, "customRecipes")

    @custom_recipes.setter # type: ignore
    def custom_recipes(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.RecipesProperty"]],
    ) -> None:
        jsii.set(self, "customRecipes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="customSecurityGroupIds")
    def custom_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::Layer.CustomSecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customsecuritygroupids
        """
        return jsii.get(self, "customSecurityGroupIds")

    @custom_security_group_ids.setter # type: ignore
    def custom_security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "customSecurityGroupIds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="installUpdatesOnBoot")
    def install_updates_on_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Layer.InstallUpdatesOnBoot``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-installupdatesonboot
        """
        return jsii.get(self, "installUpdatesOnBoot")

    @install_updates_on_boot.setter # type: ignore
    def install_updates_on_boot(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "installUpdatesOnBoot", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lifecycleEventConfiguration")
    def lifecycle_event_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.LifecycleEventConfigurationProperty"]]:
        """``AWS::OpsWorks::Layer.LifecycleEventConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-lifecycleeventconfiguration
        """
        return jsii.get(self, "lifecycleEventConfiguration")

    @lifecycle_event_configuration.setter # type: ignore
    def lifecycle_event_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.LifecycleEventConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "lifecycleEventConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="loadBasedAutoScaling")
    def load_based_auto_scaling(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.LoadBasedAutoScalingProperty"]]:
        """``AWS::OpsWorks::Layer.LoadBasedAutoScaling``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-loadbasedautoscaling
        """
        return jsii.get(self, "loadBasedAutoScaling")

    @load_based_auto_scaling.setter # type: ignore
    def load_based_auto_scaling(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.LoadBasedAutoScalingProperty"]],
    ) -> None:
        jsii.set(self, "loadBasedAutoScaling", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="packages")
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::Layer.Packages``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-packages
        """
        return jsii.get(self, "packages")

    @packages.setter # type: ignore
    def packages(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "packages", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="useEbsOptimizedInstances")
    def use_ebs_optimized_instances(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Layer.UseEbsOptimizedInstances``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-useebsoptimizedinstances
        """
        return jsii.get(self, "useEbsOptimizedInstances")

    @use_ebs_optimized_instances.setter # type: ignore
    def use_ebs_optimized_instances(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "useEbsOptimizedInstances", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="volumeConfigurations")
    def volume_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.VolumeConfigurationProperty"]]]]:
        """``AWS::OpsWorks::Layer.VolumeConfigurations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-volumeconfigurations
        """
        return jsii.get(self, "volumeConfigurations")

    @volume_configurations.setter # type: ignore
    def volume_configurations(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.VolumeConfigurationProperty"]]]],
    ) -> None:
        jsii.set(self, "volumeConfigurations", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnLayer.AutoScalingThresholdsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cpu_threshold": "cpuThreshold",
            "ignore_metrics_time": "ignoreMetricsTime",
            "instance_count": "instanceCount",
            "load_threshold": "loadThreshold",
            "memory_threshold": "memoryThreshold",
            "thresholds_wait_time": "thresholdsWaitTime",
        },
    )
    class AutoScalingThresholdsProperty:
        def __init__(
            self,
            *,
            cpu_threshold: typing.Optional[jsii.Number] = None,
            ignore_metrics_time: typing.Optional[jsii.Number] = None,
            instance_count: typing.Optional[jsii.Number] = None,
            load_threshold: typing.Optional[jsii.Number] = None,
            memory_threshold: typing.Optional[jsii.Number] = None,
            thresholds_wait_time: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param cpu_threshold: ``CfnLayer.AutoScalingThresholdsProperty.CpuThreshold``.
            :param ignore_metrics_time: ``CfnLayer.AutoScalingThresholdsProperty.IgnoreMetricsTime``.
            :param instance_count: ``CfnLayer.AutoScalingThresholdsProperty.InstanceCount``.
            :param load_threshold: ``CfnLayer.AutoScalingThresholdsProperty.LoadThreshold``.
            :param memory_threshold: ``CfnLayer.AutoScalingThresholdsProperty.MemoryThreshold``.
            :param thresholds_wait_time: ``CfnLayer.AutoScalingThresholdsProperty.ThresholdsWaitTime``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if cpu_threshold is not None:
                self._values["cpu_threshold"] = cpu_threshold
            if ignore_metrics_time is not None:
                self._values["ignore_metrics_time"] = ignore_metrics_time
            if instance_count is not None:
                self._values["instance_count"] = instance_count
            if load_threshold is not None:
                self._values["load_threshold"] = load_threshold
            if memory_threshold is not None:
                self._values["memory_threshold"] = memory_threshold
            if thresholds_wait_time is not None:
                self._values["thresholds_wait_time"] = thresholds_wait_time

        @builtins.property
        def cpu_threshold(self) -> typing.Optional[jsii.Number]:
            """``CfnLayer.AutoScalingThresholdsProperty.CpuThreshold``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-cputhreshold
            """
            result = self._values.get("cpu_threshold")
            return result

        @builtins.property
        def ignore_metrics_time(self) -> typing.Optional[jsii.Number]:
            """``CfnLayer.AutoScalingThresholdsProperty.IgnoreMetricsTime``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-ignoremetricstime
            """
            result = self._values.get("ignore_metrics_time")
            return result

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            """``CfnLayer.AutoScalingThresholdsProperty.InstanceCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-instancecount
            """
            result = self._values.get("instance_count")
            return result

        @builtins.property
        def load_threshold(self) -> typing.Optional[jsii.Number]:
            """``CfnLayer.AutoScalingThresholdsProperty.LoadThreshold``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-loadthreshold
            """
            result = self._values.get("load_threshold")
            return result

        @builtins.property
        def memory_threshold(self) -> typing.Optional[jsii.Number]:
            """``CfnLayer.AutoScalingThresholdsProperty.MemoryThreshold``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-memorythreshold
            """
            result = self._values.get("memory_threshold")
            return result

        @builtins.property
        def thresholds_wait_time(self) -> typing.Optional[jsii.Number]:
            """``CfnLayer.AutoScalingThresholdsProperty.ThresholdsWaitTime``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling-autoscalingthresholds.html#cfn-opsworks-layer-loadbasedautoscaling-autoscalingthresholds-thresholdwaittime
            """
            result = self._values.get("thresholds_wait_time")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingThresholdsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnLayer.LifecycleEventConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"shutdown_event_configuration": "shutdownEventConfiguration"},
    )
    class LifecycleEventConfigurationProperty:
        def __init__(
            self,
            *,
            shutdown_event_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.ShutdownEventConfigurationProperty"]] = None,
        ) -> None:
            """
            :param shutdown_event_configuration: ``CfnLayer.LifecycleEventConfigurationProperty.ShutdownEventConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if shutdown_event_configuration is not None:
                self._values["shutdown_event_configuration"] = shutdown_event_configuration

        @builtins.property
        def shutdown_event_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.ShutdownEventConfigurationProperty"]]:
            """``CfnLayer.LifecycleEventConfigurationProperty.ShutdownEventConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration.html#cfn-opsworks-layer-lifecycleconfiguration-shutdowneventconfiguration
            """
            result = self._values.get("shutdown_event_configuration")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleEventConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnLayer.LoadBasedAutoScalingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "down_scaling": "downScaling",
            "enable": "enable",
            "up_scaling": "upScaling",
        },
    )
    class LoadBasedAutoScalingProperty:
        def __init__(
            self,
            *,
            down_scaling: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.AutoScalingThresholdsProperty"]] = None,
            enable: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            up_scaling: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.AutoScalingThresholdsProperty"]] = None,
        ) -> None:
            """
            :param down_scaling: ``CfnLayer.LoadBasedAutoScalingProperty.DownScaling``.
            :param enable: ``CfnLayer.LoadBasedAutoScalingProperty.Enable``.
            :param up_scaling: ``CfnLayer.LoadBasedAutoScalingProperty.UpScaling``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if down_scaling is not None:
                self._values["down_scaling"] = down_scaling
            if enable is not None:
                self._values["enable"] = enable
            if up_scaling is not None:
                self._values["up_scaling"] = up_scaling

        @builtins.property
        def down_scaling(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.AutoScalingThresholdsProperty"]]:
            """``CfnLayer.LoadBasedAutoScalingProperty.DownScaling``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-downscaling
            """
            result = self._values.get("down_scaling")
            return result

        @builtins.property
        def enable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnLayer.LoadBasedAutoScalingProperty.Enable``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-enable
            """
            result = self._values.get("enable")
            return result

        @builtins.property
        def up_scaling(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnLayer.AutoScalingThresholdsProperty"]]:
            """``CfnLayer.LoadBasedAutoScalingProperty.UpScaling``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-loadbasedautoscaling.html#cfn-opsworks-layer-loadbasedautoscaling-upscaling
            """
            result = self._values.get("up_scaling")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoadBasedAutoScalingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnLayer.RecipesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configure": "configure",
            "deploy": "deploy",
            "setup": "setup",
            "shutdown": "shutdown",
            "undeploy": "undeploy",
        },
    )
    class RecipesProperty:
        def __init__(
            self,
            *,
            configure: typing.Optional[typing.List[builtins.str]] = None,
            deploy: typing.Optional[typing.List[builtins.str]] = None,
            setup: typing.Optional[typing.List[builtins.str]] = None,
            shutdown: typing.Optional[typing.List[builtins.str]] = None,
            undeploy: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param configure: ``CfnLayer.RecipesProperty.Configure``.
            :param deploy: ``CfnLayer.RecipesProperty.Deploy``.
            :param setup: ``CfnLayer.RecipesProperty.Setup``.
            :param shutdown: ``CfnLayer.RecipesProperty.Shutdown``.
            :param undeploy: ``CfnLayer.RecipesProperty.Undeploy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if configure is not None:
                self._values["configure"] = configure
            if deploy is not None:
                self._values["deploy"] = deploy
            if setup is not None:
                self._values["setup"] = setup
            if shutdown is not None:
                self._values["shutdown"] = shutdown
            if undeploy is not None:
                self._values["undeploy"] = undeploy

        @builtins.property
        def configure(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnLayer.RecipesProperty.Configure``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-configure
            """
            result = self._values.get("configure")
            return result

        @builtins.property
        def deploy(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnLayer.RecipesProperty.Deploy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-deploy
            """
            result = self._values.get("deploy")
            return result

        @builtins.property
        def setup(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnLayer.RecipesProperty.Setup``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-setup
            """
            result = self._values.get("setup")
            return result

        @builtins.property
        def shutdown(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnLayer.RecipesProperty.Shutdown``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-shutdown
            """
            result = self._values.get("shutdown")
            return result

        @builtins.property
        def undeploy(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnLayer.RecipesProperty.Undeploy``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-recipes.html#cfn-opsworks-layer-customrecipes-undeploy
            """
            result = self._values.get("undeploy")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecipesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnLayer.ShutdownEventConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delay_until_elb_connections_drained": "delayUntilElbConnectionsDrained",
            "execution_timeout": "executionTimeout",
        },
    )
    class ShutdownEventConfigurationProperty:
        def __init__(
            self,
            *,
            delay_until_elb_connections_drained: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            execution_timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param delay_until_elb_connections_drained: ``CfnLayer.ShutdownEventConfigurationProperty.DelayUntilElbConnectionsDrained``.
            :param execution_timeout: ``CfnLayer.ShutdownEventConfigurationProperty.ExecutionTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration-shutdowneventconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if delay_until_elb_connections_drained is not None:
                self._values["delay_until_elb_connections_drained"] = delay_until_elb_connections_drained
            if execution_timeout is not None:
                self._values["execution_timeout"] = execution_timeout

        @builtins.property
        def delay_until_elb_connections_drained(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnLayer.ShutdownEventConfigurationProperty.DelayUntilElbConnectionsDrained``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration-shutdowneventconfiguration.html#cfn-opsworks-layer-lifecycleconfiguration-shutdowneventconfiguration-delayuntilelbconnectionsdrained
            """
            result = self._values.get("delay_until_elb_connections_drained")
            return result

        @builtins.property
        def execution_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnLayer.ShutdownEventConfigurationProperty.ExecutionTimeout``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-lifecycleeventconfiguration-shutdowneventconfiguration.html#cfn-opsworks-layer-lifecycleconfiguration-shutdowneventconfiguration-executiontimeout
            """
            result = self._values.get("execution_timeout")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ShutdownEventConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnLayer.VolumeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encrypted": "encrypted",
            "iops": "iops",
            "mount_point": "mountPoint",
            "number_of_disks": "numberOfDisks",
            "raid_level": "raidLevel",
            "size": "size",
            "volume_type": "volumeType",
        },
    )
    class VolumeConfigurationProperty:
        def __init__(
            self,
            *,
            encrypted: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            iops: typing.Optional[jsii.Number] = None,
            mount_point: typing.Optional[builtins.str] = None,
            number_of_disks: typing.Optional[jsii.Number] = None,
            raid_level: typing.Optional[jsii.Number] = None,
            size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param encrypted: ``CfnLayer.VolumeConfigurationProperty.Encrypted``.
            :param iops: ``CfnLayer.VolumeConfigurationProperty.Iops``.
            :param mount_point: ``CfnLayer.VolumeConfigurationProperty.MountPoint``.
            :param number_of_disks: ``CfnLayer.VolumeConfigurationProperty.NumberOfDisks``.
            :param raid_level: ``CfnLayer.VolumeConfigurationProperty.RaidLevel``.
            :param size: ``CfnLayer.VolumeConfigurationProperty.Size``.
            :param volume_type: ``CfnLayer.VolumeConfigurationProperty.VolumeType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if encrypted is not None:
                self._values["encrypted"] = encrypted
            if iops is not None:
                self._values["iops"] = iops
            if mount_point is not None:
                self._values["mount_point"] = mount_point
            if number_of_disks is not None:
                self._values["number_of_disks"] = number_of_disks
            if raid_level is not None:
                self._values["raid_level"] = raid_level
            if size is not None:
                self._values["size"] = size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def encrypted(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnLayer.VolumeConfigurationProperty.Encrypted``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volumeconfiguration-encrypted
            """
            result = self._values.get("encrypted")
            return result

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            """``CfnLayer.VolumeConfigurationProperty.Iops``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-iops
            """
            result = self._values.get("iops")
            return result

        @builtins.property
        def mount_point(self) -> typing.Optional[builtins.str]:
            """``CfnLayer.VolumeConfigurationProperty.MountPoint``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-mountpoint
            """
            result = self._values.get("mount_point")
            return result

        @builtins.property
        def number_of_disks(self) -> typing.Optional[jsii.Number]:
            """``CfnLayer.VolumeConfigurationProperty.NumberOfDisks``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-numberofdisks
            """
            result = self._values.get("number_of_disks")
            return result

        @builtins.property
        def raid_level(self) -> typing.Optional[jsii.Number]:
            """``CfnLayer.VolumeConfigurationProperty.RaidLevel``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-raidlevel
            """
            result = self._values.get("raid_level")
            return result

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            """``CfnLayer.VolumeConfigurationProperty.Size``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-size
            """
            result = self._values.get("size")
            return result

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            """``CfnLayer.VolumeConfigurationProperty.VolumeType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-layer-volumeconfiguration.html#cfn-opsworks-layer-volconfig-volumetype
            """
            result = self._values.get("volume_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opsworks.CfnLayerProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_assign_elastic_ips": "autoAssignElasticIps",
        "auto_assign_public_ips": "autoAssignPublicIps",
        "enable_auto_healing": "enableAutoHealing",
        "name": "name",
        "shortname": "shortname",
        "stack_id": "stackId",
        "type": "type",
        "attributes": "attributes",
        "custom_instance_profile_arn": "customInstanceProfileArn",
        "custom_json": "customJson",
        "custom_recipes": "customRecipes",
        "custom_security_group_ids": "customSecurityGroupIds",
        "install_updates_on_boot": "installUpdatesOnBoot",
        "lifecycle_event_configuration": "lifecycleEventConfiguration",
        "load_based_auto_scaling": "loadBasedAutoScaling",
        "packages": "packages",
        "tags": "tags",
        "use_ebs_optimized_instances": "useEbsOptimizedInstances",
        "volume_configurations": "volumeConfigurations",
    },
)
class CfnLayerProps:
    def __init__(
        self,
        *,
        auto_assign_elastic_ips: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        auto_assign_public_ips: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        enable_auto_healing: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
        name: builtins.str,
        shortname: builtins.str,
        stack_id: builtins.str,
        type: builtins.str,
        attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        custom_instance_profile_arn: typing.Optional[builtins.str] = None,
        custom_json: typing.Any = None,
        custom_recipes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLayer.RecipesProperty]] = None,
        custom_security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
        install_updates_on_boot: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        lifecycle_event_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLayer.LifecycleEventConfigurationProperty]] = None,
        load_based_auto_scaling: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLayer.LoadBasedAutoScalingProperty]] = None,
        packages: typing.Optional[typing.List[builtins.str]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        use_ebs_optimized_instances: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        volume_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLayer.VolumeConfigurationProperty]]]] = None,
    ) -> None:
        """Properties for defining a ``AWS::OpsWorks::Layer``.

        :param auto_assign_elastic_ips: ``AWS::OpsWorks::Layer.AutoAssignElasticIps``.
        :param auto_assign_public_ips: ``AWS::OpsWorks::Layer.AutoAssignPublicIps``.
        :param enable_auto_healing: ``AWS::OpsWorks::Layer.EnableAutoHealing``.
        :param name: ``AWS::OpsWorks::Layer.Name``.
        :param shortname: ``AWS::OpsWorks::Layer.Shortname``.
        :param stack_id: ``AWS::OpsWorks::Layer.StackId``.
        :param type: ``AWS::OpsWorks::Layer.Type``.
        :param attributes: ``AWS::OpsWorks::Layer.Attributes``.
        :param custom_instance_profile_arn: ``AWS::OpsWorks::Layer.CustomInstanceProfileArn``.
        :param custom_json: ``AWS::OpsWorks::Layer.CustomJson``.
        :param custom_recipes: ``AWS::OpsWorks::Layer.CustomRecipes``.
        :param custom_security_group_ids: ``AWS::OpsWorks::Layer.CustomSecurityGroupIds``.
        :param install_updates_on_boot: ``AWS::OpsWorks::Layer.InstallUpdatesOnBoot``.
        :param lifecycle_event_configuration: ``AWS::OpsWorks::Layer.LifecycleEventConfiguration``.
        :param load_based_auto_scaling: ``AWS::OpsWorks::Layer.LoadBasedAutoScaling``.
        :param packages: ``AWS::OpsWorks::Layer.Packages``.
        :param tags: ``AWS::OpsWorks::Layer.Tags``.
        :param use_ebs_optimized_instances: ``AWS::OpsWorks::Layer.UseEbsOptimizedInstances``.
        :param volume_configurations: ``AWS::OpsWorks::Layer.VolumeConfigurations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "auto_assign_elastic_ips": auto_assign_elastic_ips,
            "auto_assign_public_ips": auto_assign_public_ips,
            "enable_auto_healing": enable_auto_healing,
            "name": name,
            "shortname": shortname,
            "stack_id": stack_id,
            "type": type,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if custom_instance_profile_arn is not None:
            self._values["custom_instance_profile_arn"] = custom_instance_profile_arn
        if custom_json is not None:
            self._values["custom_json"] = custom_json
        if custom_recipes is not None:
            self._values["custom_recipes"] = custom_recipes
        if custom_security_group_ids is not None:
            self._values["custom_security_group_ids"] = custom_security_group_ids
        if install_updates_on_boot is not None:
            self._values["install_updates_on_boot"] = install_updates_on_boot
        if lifecycle_event_configuration is not None:
            self._values["lifecycle_event_configuration"] = lifecycle_event_configuration
        if load_based_auto_scaling is not None:
            self._values["load_based_auto_scaling"] = load_based_auto_scaling
        if packages is not None:
            self._values["packages"] = packages
        if tags is not None:
            self._values["tags"] = tags
        if use_ebs_optimized_instances is not None:
            self._values["use_ebs_optimized_instances"] = use_ebs_optimized_instances
        if volume_configurations is not None:
            self._values["volume_configurations"] = volume_configurations

    @builtins.property
    def auto_assign_elastic_ips(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::OpsWorks::Layer.AutoAssignElasticIps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignelasticips
        """
        result = self._values.get("auto_assign_elastic_ips")
        assert result is not None, "Required property 'auto_assign_elastic_ips' is missing"
        return result

    @builtins.property
    def auto_assign_public_ips(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::OpsWorks::Layer.AutoAssignPublicIps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-autoassignpublicips
        """
        result = self._values.get("auto_assign_public_ips")
        assert result is not None, "Required property 'auto_assign_public_ips' is missing"
        return result

    @builtins.property
    def enable_auto_healing(
        self,
    ) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::OpsWorks::Layer.EnableAutoHealing``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-enableautohealing
        """
        result = self._values.get("enable_auto_healing")
        assert result is not None, "Required property 'enable_auto_healing' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::OpsWorks::Layer.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def shortname(self) -> builtins.str:
        """``AWS::OpsWorks::Layer.Shortname``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-shortname
        """
        result = self._values.get("shortname")
        assert result is not None, "Required property 'shortname' is missing"
        return result

    @builtins.property
    def stack_id(self) -> builtins.str:
        """``AWS::OpsWorks::Layer.StackId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-stackid
        """
        result = self._values.get("stack_id")
        assert result is not None, "Required property 'stack_id' is missing"
        return result

    @builtins.property
    def type(self) -> builtins.str:
        """``AWS::OpsWorks::Layer.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-type
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::OpsWorks::Layer.Attributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-attributes
        """
        result = self._values.get("attributes")
        return result

    @builtins.property
    def custom_instance_profile_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Layer.CustomInstanceProfileArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-custominstanceprofilearn
        """
        result = self._values.get("custom_instance_profile_arn")
        return result

    @builtins.property
    def custom_json(self) -> typing.Any:
        """``AWS::OpsWorks::Layer.CustomJson``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customjson
        """
        result = self._values.get("custom_json")
        return result

    @builtins.property
    def custom_recipes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLayer.RecipesProperty]]:
        """``AWS::OpsWorks::Layer.CustomRecipes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customrecipes
        """
        result = self._values.get("custom_recipes")
        return result

    @builtins.property
    def custom_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::Layer.CustomSecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-customsecuritygroupids
        """
        result = self._values.get("custom_security_group_ids")
        return result

    @builtins.property
    def install_updates_on_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Layer.InstallUpdatesOnBoot``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-installupdatesonboot
        """
        result = self._values.get("install_updates_on_boot")
        return result

    @builtins.property
    def lifecycle_event_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLayer.LifecycleEventConfigurationProperty]]:
        """``AWS::OpsWorks::Layer.LifecycleEventConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-lifecycleeventconfiguration
        """
        result = self._values.get("lifecycle_event_configuration")
        return result

    @builtins.property
    def load_based_auto_scaling(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnLayer.LoadBasedAutoScalingProperty]]:
        """``AWS::OpsWorks::Layer.LoadBasedAutoScaling``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-loadbasedautoscaling
        """
        result = self._values.get("load_based_auto_scaling")
        return result

    @builtins.property
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::Layer.Packages``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-packages
        """
        result = self._values.get("packages")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::OpsWorks::Layer.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def use_ebs_optimized_instances(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Layer.UseEbsOptimizedInstances``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-useebsoptimizedinstances
        """
        result = self._values.get("use_ebs_optimized_instances")
        return result

    @builtins.property
    def volume_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnLayer.VolumeConfigurationProperty]]]]:
        """``AWS::OpsWorks::Layer.VolumeConfigurations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-layer.html#cfn-opsworks-layer-volumeconfigurations
        """
        result = self._values.get("volume_configurations")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLayerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStack(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opsworks.CfnStack",
):
    """A CloudFormation ``AWS::OpsWorks::Stack``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html
    :cloudformationResource: AWS::OpsWorks::Stack
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        default_instance_profile_arn: builtins.str,
        name: builtins.str,
        service_role_arn: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        chef_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.ChefConfigurationProperty"]] = None,
        clone_app_ids: typing.Optional[typing.List[builtins.str]] = None,
        clone_permissions: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        configuration_manager: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.StackConfigurationManagerProperty"]] = None,
        custom_cookbooks_source: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.SourceProperty"]] = None,
        custom_json: typing.Any = None,
        default_availability_zone: typing.Optional[builtins.str] = None,
        default_os: typing.Optional[builtins.str] = None,
        default_root_device_type: typing.Optional[builtins.str] = None,
        default_ssh_key_name: typing.Optional[builtins.str] = None,
        default_subnet_id: typing.Optional[builtins.str] = None,
        ecs_cluster_arn: typing.Optional[builtins.str] = None,
        elastic_ips: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.ElasticIpProperty"]]]] = None,
        hostname_theme: typing.Optional[builtins.str] = None,
        rds_db_instances: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.RdsDbInstanceProperty"]]]] = None,
        source_stack_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        use_custom_cookbooks: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        use_opsworks_security_groups: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::OpsWorks::Stack``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_instance_profile_arn: ``AWS::OpsWorks::Stack.DefaultInstanceProfileArn``.
        :param name: ``AWS::OpsWorks::Stack.Name``.
        :param service_role_arn: ``AWS::OpsWorks::Stack.ServiceRoleArn``.
        :param agent_version: ``AWS::OpsWorks::Stack.AgentVersion``.
        :param attributes: ``AWS::OpsWorks::Stack.Attributes``.
        :param chef_configuration: ``AWS::OpsWorks::Stack.ChefConfiguration``.
        :param clone_app_ids: ``AWS::OpsWorks::Stack.CloneAppIds``.
        :param clone_permissions: ``AWS::OpsWorks::Stack.ClonePermissions``.
        :param configuration_manager: ``AWS::OpsWorks::Stack.ConfigurationManager``.
        :param custom_cookbooks_source: ``AWS::OpsWorks::Stack.CustomCookbooksSource``.
        :param custom_json: ``AWS::OpsWorks::Stack.CustomJson``.
        :param default_availability_zone: ``AWS::OpsWorks::Stack.DefaultAvailabilityZone``.
        :param default_os: ``AWS::OpsWorks::Stack.DefaultOs``.
        :param default_root_device_type: ``AWS::OpsWorks::Stack.DefaultRootDeviceType``.
        :param default_ssh_key_name: ``AWS::OpsWorks::Stack.DefaultSshKeyName``.
        :param default_subnet_id: ``AWS::OpsWorks::Stack.DefaultSubnetId``.
        :param ecs_cluster_arn: ``AWS::OpsWorks::Stack.EcsClusterArn``.
        :param elastic_ips: ``AWS::OpsWorks::Stack.ElasticIps``.
        :param hostname_theme: ``AWS::OpsWorks::Stack.HostnameTheme``.
        :param rds_db_instances: ``AWS::OpsWorks::Stack.RdsDbInstances``.
        :param source_stack_id: ``AWS::OpsWorks::Stack.SourceStackId``.
        :param tags: ``AWS::OpsWorks::Stack.Tags``.
        :param use_custom_cookbooks: ``AWS::OpsWorks::Stack.UseCustomCookbooks``.
        :param use_opsworks_security_groups: ``AWS::OpsWorks::Stack.UseOpsworksSecurityGroups``.
        :param vpc_id: ``AWS::OpsWorks::Stack.VpcId``.
        """
        props = CfnStackProps(
            default_instance_profile_arn=default_instance_profile_arn,
            name=name,
            service_role_arn=service_role_arn,
            agent_version=agent_version,
            attributes=attributes,
            chef_configuration=chef_configuration,
            clone_app_ids=clone_app_ids,
            clone_permissions=clone_permissions,
            configuration_manager=configuration_manager,
            custom_cookbooks_source=custom_cookbooks_source,
            custom_json=custom_json,
            default_availability_zone=default_availability_zone,
            default_os=default_os,
            default_root_device_type=default_root_device_type,
            default_ssh_key_name=default_ssh_key_name,
            default_subnet_id=default_subnet_id,
            ecs_cluster_arn=ecs_cluster_arn,
            elastic_ips=elastic_ips,
            hostname_theme=hostname_theme,
            rds_db_instances=rds_db_instances,
            source_stack_id=source_stack_id,
            tags=tags,
            use_custom_cookbooks=use_custom_cookbooks,
            use_opsworks_security_groups=use_opsworks_security_groups,
            vpc_id=vpc_id,
        )

        jsii.create(CfnStack, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::OpsWorks::Stack.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="customJson")
    def custom_json(self) -> typing.Any:
        """``AWS::OpsWorks::Stack.CustomJson``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-custjson
        """
        return jsii.get(self, "customJson")

    @custom_json.setter # type: ignore
    def custom_json(self, value: typing.Any) -> None:
        jsii.set(self, "customJson", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultInstanceProfileArn")
    def default_instance_profile_arn(self) -> builtins.str:
        """``AWS::OpsWorks::Stack.DefaultInstanceProfileArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultinstanceprof
        """
        return jsii.get(self, "defaultInstanceProfileArn")

    @default_instance_profile_arn.setter # type: ignore
    def default_instance_profile_arn(self, value: builtins.str) -> None:
        jsii.set(self, "defaultInstanceProfileArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::OpsWorks::Stack.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> builtins.str:
        """``AWS::OpsWorks::Stack.ServiceRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-servicerolearn
        """
        return jsii.get(self, "serviceRoleArn")

    @service_role_arn.setter # type: ignore
    def service_role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "serviceRoleArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="agentVersion")
    def agent_version(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.AgentVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-agentversion
        """
        return jsii.get(self, "agentVersion")

    @agent_version.setter # type: ignore
    def agent_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "agentVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::OpsWorks::Stack.Attributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-attributes
        """
        return jsii.get(self, "attributes")

    @attributes.setter # type: ignore
    def attributes(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "attributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="chefConfiguration")
    def chef_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.ChefConfigurationProperty"]]:
        """``AWS::OpsWorks::Stack.ChefConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-chefconfiguration
        """
        return jsii.get(self, "chefConfiguration")

    @chef_configuration.setter # type: ignore
    def chef_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.ChefConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "chefConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cloneAppIds")
    def clone_app_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::Stack.CloneAppIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-cloneappids
        """
        return jsii.get(self, "cloneAppIds")

    @clone_app_ids.setter # type: ignore
    def clone_app_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "cloneAppIds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clonePermissions")
    def clone_permissions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Stack.ClonePermissions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-clonepermissions
        """
        return jsii.get(self, "clonePermissions")

    @clone_permissions.setter # type: ignore
    def clone_permissions(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "clonePermissions", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="configurationManager")
    def configuration_manager(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.StackConfigurationManagerProperty"]]:
        """``AWS::OpsWorks::Stack.ConfigurationManager``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-configmanager
        """
        return jsii.get(self, "configurationManager")

    @configuration_manager.setter # type: ignore
    def configuration_manager(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.StackConfigurationManagerProperty"]],
    ) -> None:
        jsii.set(self, "configurationManager", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="customCookbooksSource")
    def custom_cookbooks_source(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.SourceProperty"]]:
        """``AWS::OpsWorks::Stack.CustomCookbooksSource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-custcookbooksource
        """
        return jsii.get(self, "customCookbooksSource")

    @custom_cookbooks_source.setter # type: ignore
    def custom_cookbooks_source(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStack.SourceProperty"]],
    ) -> None:
        jsii.set(self, "customCookbooksSource", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultAvailabilityZone")
    def default_availability_zone(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.DefaultAvailabilityZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultaz
        """
        return jsii.get(self, "defaultAvailabilityZone")

    @default_availability_zone.setter # type: ignore
    def default_availability_zone(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "defaultAvailabilityZone", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultOs")
    def default_os(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.DefaultOs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultos
        """
        return jsii.get(self, "defaultOs")

    @default_os.setter # type: ignore
    def default_os(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "defaultOs", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultRootDeviceType")
    def default_root_device_type(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.DefaultRootDeviceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultrootdevicetype
        """
        return jsii.get(self, "defaultRootDeviceType")

    @default_root_device_type.setter # type: ignore
    def default_root_device_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "defaultRootDeviceType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultSshKeyName")
    def default_ssh_key_name(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.DefaultSshKeyName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultsshkeyname
        """
        return jsii.get(self, "defaultSshKeyName")

    @default_ssh_key_name.setter # type: ignore
    def default_ssh_key_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "defaultSshKeyName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="defaultSubnetId")
    def default_subnet_id(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.DefaultSubnetId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#defaultsubnet
        """
        return jsii.get(self, "defaultSubnetId")

    @default_subnet_id.setter # type: ignore
    def default_subnet_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "defaultSubnetId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ecsClusterArn")
    def ecs_cluster_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.EcsClusterArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-ecsclusterarn
        """
        return jsii.get(self, "ecsClusterArn")

    @ecs_cluster_arn.setter # type: ignore
    def ecs_cluster_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ecsClusterArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="elasticIps")
    def elastic_ips(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.ElasticIpProperty"]]]]:
        """``AWS::OpsWorks::Stack.ElasticIps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-elasticips
        """
        return jsii.get(self, "elasticIps")

    @elastic_ips.setter # type: ignore
    def elastic_ips(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.ElasticIpProperty"]]]],
    ) -> None:
        jsii.set(self, "elasticIps", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="hostnameTheme")
    def hostname_theme(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.HostnameTheme``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-hostnametheme
        """
        return jsii.get(self, "hostnameTheme")

    @hostname_theme.setter # type: ignore
    def hostname_theme(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "hostnameTheme", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="rdsDbInstances")
    def rds_db_instances(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.RdsDbInstanceProperty"]]]]:
        """``AWS::OpsWorks::Stack.RdsDbInstances``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-rdsdbinstances
        """
        return jsii.get(self, "rdsDbInstances")

    @rds_db_instances.setter # type: ignore
    def rds_db_instances(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnStack.RdsDbInstanceProperty"]]]],
    ) -> None:
        jsii.set(self, "rdsDbInstances", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceStackId")
    def source_stack_id(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.SourceStackId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-sourcestackid
        """
        return jsii.get(self, "sourceStackId")

    @source_stack_id.setter # type: ignore
    def source_stack_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sourceStackId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="useCustomCookbooks")
    def use_custom_cookbooks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Stack.UseCustomCookbooks``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#usecustcookbooks
        """
        return jsii.get(self, "useCustomCookbooks")

    @use_custom_cookbooks.setter # type: ignore
    def use_custom_cookbooks(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "useCustomCookbooks", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="useOpsworksSecurityGroups")
    def use_opsworks_security_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Stack.UseOpsworksSecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-useopsworkssecuritygroups
        """
        return jsii.get(self, "useOpsworksSecurityGroups")

    @use_opsworks_security_groups.setter # type: ignore
    def use_opsworks_security_groups(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "useOpsworksSecurityGroups", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.VpcId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-vpcid
        """
        return jsii.get(self, "vpcId")

    @vpc_id.setter # type: ignore
    def vpc_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "vpcId", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnStack.ChefConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "berkshelf_version": "berkshelfVersion",
            "manage_berkshelf": "manageBerkshelf",
        },
    )
    class ChefConfigurationProperty:
        def __init__(
            self,
            *,
            berkshelf_version: typing.Optional[builtins.str] = None,
            manage_berkshelf: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            """
            :param berkshelf_version: ``CfnStack.ChefConfigurationProperty.BerkshelfVersion``.
            :param manage_berkshelf: ``CfnStack.ChefConfigurationProperty.ManageBerkshelf``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if berkshelf_version is not None:
                self._values["berkshelf_version"] = berkshelf_version
            if manage_berkshelf is not None:
                self._values["manage_berkshelf"] = manage_berkshelf

        @builtins.property
        def berkshelf_version(self) -> typing.Optional[builtins.str]:
            """``CfnStack.ChefConfigurationProperty.BerkshelfVersion``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html#cfn-opsworks-chefconfiguration-berkshelfversion
            """
            result = self._values.get("berkshelf_version")
            return result

        @builtins.property
        def manage_berkshelf(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnStack.ChefConfigurationProperty.ManageBerkshelf``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-chefconfiguration.html#cfn-opsworks-chefconfiguration-berkshelfversion
            """
            result = self._values.get("manage_berkshelf")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChefConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnStack.ElasticIpProperty",
        jsii_struct_bases=[],
        name_mapping={"ip": "ip", "name": "name"},
    )
    class ElasticIpProperty:
        def __init__(
            self,
            *,
            ip: builtins.str,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param ip: ``CfnStack.ElasticIpProperty.Ip``.
            :param name: ``CfnStack.ElasticIpProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "ip": ip,
            }
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def ip(self) -> builtins.str:
            """``CfnStack.ElasticIpProperty.Ip``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html#cfn-opsworks-stack-elasticip-ip
            """
            result = self._values.get("ip")
            assert result is not None, "Required property 'ip' is missing"
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnStack.ElasticIpProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-elasticip.html#cfn-opsworks-stack-elasticip-name
            """
            result = self._values.get("name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticIpProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnStack.RdsDbInstanceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "db_password": "dbPassword",
            "db_user": "dbUser",
            "rds_db_instance_arn": "rdsDbInstanceArn",
        },
    )
    class RdsDbInstanceProperty:
        def __init__(
            self,
            *,
            db_password: builtins.str,
            db_user: builtins.str,
            rds_db_instance_arn: builtins.str,
        ) -> None:
            """
            :param db_password: ``CfnStack.RdsDbInstanceProperty.DbPassword``.
            :param db_user: ``CfnStack.RdsDbInstanceProperty.DbUser``.
            :param rds_db_instance_arn: ``CfnStack.RdsDbInstanceProperty.RdsDbInstanceArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "db_password": db_password,
                "db_user": db_user,
                "rds_db_instance_arn": rds_db_instance_arn,
            }

        @builtins.property
        def db_password(self) -> builtins.str:
            """``CfnStack.RdsDbInstanceProperty.DbPassword``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-dbpassword
            """
            result = self._values.get("db_password")
            assert result is not None, "Required property 'db_password' is missing"
            return result

        @builtins.property
        def db_user(self) -> builtins.str:
            """``CfnStack.RdsDbInstanceProperty.DbUser``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-dbuser
            """
            result = self._values.get("db_user")
            assert result is not None, "Required property 'db_user' is missing"
            return result

        @builtins.property
        def rds_db_instance_arn(self) -> builtins.str:
            """``CfnStack.RdsDbInstanceProperty.RdsDbInstanceArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-rdsdbinstance.html#cfn-opsworks-stack-rdsdbinstance-rdsdbinstancearn
            """
            result = self._values.get("rds_db_instance_arn")
            assert result is not None, "Required property 'rds_db_instance_arn' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RdsDbInstanceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnStack.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password": "password",
            "revision": "revision",
            "ssh_key": "sshKey",
            "type": "type",
            "url": "url",
            "username": "username",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            revision: typing.Optional[builtins.str] = None,
            ssh_key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param password: ``CfnStack.SourceProperty.Password``.
            :param revision: ``CfnStack.SourceProperty.Revision``.
            :param ssh_key: ``CfnStack.SourceProperty.SshKey``.
            :param type: ``CfnStack.SourceProperty.Type``.
            :param url: ``CfnStack.SourceProperty.Url``.
            :param username: ``CfnStack.SourceProperty.Username``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if revision is not None:
                self._values["revision"] = revision
            if ssh_key is not None:
                self._values["ssh_key"] = ssh_key
            if type is not None:
                self._values["type"] = type
            if url is not None:
                self._values["url"] = url
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            """``CfnStack.SourceProperty.Password``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-password
            """
            result = self._values.get("password")
            return result

        @builtins.property
        def revision(self) -> typing.Optional[builtins.str]:
            """``CfnStack.SourceProperty.Revision``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-revision
            """
            result = self._values.get("revision")
            return result

        @builtins.property
        def ssh_key(self) -> typing.Optional[builtins.str]:
            """``CfnStack.SourceProperty.SshKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-sshkey
            """
            result = self._values.get("ssh_key")
            return result

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            """``CfnStack.SourceProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-type
            """
            result = self._values.get("type")
            return result

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            """``CfnStack.SourceProperty.Url``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-url
            """
            result = self._values.get("url")
            return result

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            """``CfnStack.SourceProperty.Username``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-source.html#cfn-opsworks-custcookbooksource-username
            """
            result = self._values.get("username")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opsworks.CfnStack.StackConfigurationManagerProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class StackConfigurationManagerProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param name: ``CfnStack.StackConfigurationManagerProperty.Name``.
            :param version: ``CfnStack.StackConfigurationManagerProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigmanager.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """``CfnStack.StackConfigurationManagerProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigmanager.html#cfn-opsworks-configmanager-name
            """
            result = self._values.get("name")
            return result

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            """``CfnStack.StackConfigurationManagerProperty.Version``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opsworks-stack-stackconfigmanager.html#cfn-opsworks-configmanager-version
            """
            result = self._values.get("version")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StackConfigurationManagerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opsworks.CfnStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_instance_profile_arn": "defaultInstanceProfileArn",
        "name": "name",
        "service_role_arn": "serviceRoleArn",
        "agent_version": "agentVersion",
        "attributes": "attributes",
        "chef_configuration": "chefConfiguration",
        "clone_app_ids": "cloneAppIds",
        "clone_permissions": "clonePermissions",
        "configuration_manager": "configurationManager",
        "custom_cookbooks_source": "customCookbooksSource",
        "custom_json": "customJson",
        "default_availability_zone": "defaultAvailabilityZone",
        "default_os": "defaultOs",
        "default_root_device_type": "defaultRootDeviceType",
        "default_ssh_key_name": "defaultSshKeyName",
        "default_subnet_id": "defaultSubnetId",
        "ecs_cluster_arn": "ecsClusterArn",
        "elastic_ips": "elasticIps",
        "hostname_theme": "hostnameTheme",
        "rds_db_instances": "rdsDbInstances",
        "source_stack_id": "sourceStackId",
        "tags": "tags",
        "use_custom_cookbooks": "useCustomCookbooks",
        "use_opsworks_security_groups": "useOpsworksSecurityGroups",
        "vpc_id": "vpcId",
    },
)
class CfnStackProps:
    def __init__(
        self,
        *,
        default_instance_profile_arn: builtins.str,
        name: builtins.str,
        service_role_arn: builtins.str,
        agent_version: typing.Optional[builtins.str] = None,
        attributes: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        chef_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStack.ChefConfigurationProperty]] = None,
        clone_app_ids: typing.Optional[typing.List[builtins.str]] = None,
        clone_permissions: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        configuration_manager: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStack.StackConfigurationManagerProperty]] = None,
        custom_cookbooks_source: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStack.SourceProperty]] = None,
        custom_json: typing.Any = None,
        default_availability_zone: typing.Optional[builtins.str] = None,
        default_os: typing.Optional[builtins.str] = None,
        default_root_device_type: typing.Optional[builtins.str] = None,
        default_ssh_key_name: typing.Optional[builtins.str] = None,
        default_subnet_id: typing.Optional[builtins.str] = None,
        ecs_cluster_arn: typing.Optional[builtins.str] = None,
        elastic_ips: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStack.ElasticIpProperty]]]] = None,
        hostname_theme: typing.Optional[builtins.str] = None,
        rds_db_instances: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStack.RdsDbInstanceProperty]]]] = None,
        source_stack_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        use_custom_cookbooks: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        use_opsworks_security_groups: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::OpsWorks::Stack``.

        :param default_instance_profile_arn: ``AWS::OpsWorks::Stack.DefaultInstanceProfileArn``.
        :param name: ``AWS::OpsWorks::Stack.Name``.
        :param service_role_arn: ``AWS::OpsWorks::Stack.ServiceRoleArn``.
        :param agent_version: ``AWS::OpsWorks::Stack.AgentVersion``.
        :param attributes: ``AWS::OpsWorks::Stack.Attributes``.
        :param chef_configuration: ``AWS::OpsWorks::Stack.ChefConfiguration``.
        :param clone_app_ids: ``AWS::OpsWorks::Stack.CloneAppIds``.
        :param clone_permissions: ``AWS::OpsWorks::Stack.ClonePermissions``.
        :param configuration_manager: ``AWS::OpsWorks::Stack.ConfigurationManager``.
        :param custom_cookbooks_source: ``AWS::OpsWorks::Stack.CustomCookbooksSource``.
        :param custom_json: ``AWS::OpsWorks::Stack.CustomJson``.
        :param default_availability_zone: ``AWS::OpsWorks::Stack.DefaultAvailabilityZone``.
        :param default_os: ``AWS::OpsWorks::Stack.DefaultOs``.
        :param default_root_device_type: ``AWS::OpsWorks::Stack.DefaultRootDeviceType``.
        :param default_ssh_key_name: ``AWS::OpsWorks::Stack.DefaultSshKeyName``.
        :param default_subnet_id: ``AWS::OpsWorks::Stack.DefaultSubnetId``.
        :param ecs_cluster_arn: ``AWS::OpsWorks::Stack.EcsClusterArn``.
        :param elastic_ips: ``AWS::OpsWorks::Stack.ElasticIps``.
        :param hostname_theme: ``AWS::OpsWorks::Stack.HostnameTheme``.
        :param rds_db_instances: ``AWS::OpsWorks::Stack.RdsDbInstances``.
        :param source_stack_id: ``AWS::OpsWorks::Stack.SourceStackId``.
        :param tags: ``AWS::OpsWorks::Stack.Tags``.
        :param use_custom_cookbooks: ``AWS::OpsWorks::Stack.UseCustomCookbooks``.
        :param use_opsworks_security_groups: ``AWS::OpsWorks::Stack.UseOpsworksSecurityGroups``.
        :param vpc_id: ``AWS::OpsWorks::Stack.VpcId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "default_instance_profile_arn": default_instance_profile_arn,
            "name": name,
            "service_role_arn": service_role_arn,
        }
        if agent_version is not None:
            self._values["agent_version"] = agent_version
        if attributes is not None:
            self._values["attributes"] = attributes
        if chef_configuration is not None:
            self._values["chef_configuration"] = chef_configuration
        if clone_app_ids is not None:
            self._values["clone_app_ids"] = clone_app_ids
        if clone_permissions is not None:
            self._values["clone_permissions"] = clone_permissions
        if configuration_manager is not None:
            self._values["configuration_manager"] = configuration_manager
        if custom_cookbooks_source is not None:
            self._values["custom_cookbooks_source"] = custom_cookbooks_source
        if custom_json is not None:
            self._values["custom_json"] = custom_json
        if default_availability_zone is not None:
            self._values["default_availability_zone"] = default_availability_zone
        if default_os is not None:
            self._values["default_os"] = default_os
        if default_root_device_type is not None:
            self._values["default_root_device_type"] = default_root_device_type
        if default_ssh_key_name is not None:
            self._values["default_ssh_key_name"] = default_ssh_key_name
        if default_subnet_id is not None:
            self._values["default_subnet_id"] = default_subnet_id
        if ecs_cluster_arn is not None:
            self._values["ecs_cluster_arn"] = ecs_cluster_arn
        if elastic_ips is not None:
            self._values["elastic_ips"] = elastic_ips
        if hostname_theme is not None:
            self._values["hostname_theme"] = hostname_theme
        if rds_db_instances is not None:
            self._values["rds_db_instances"] = rds_db_instances
        if source_stack_id is not None:
            self._values["source_stack_id"] = source_stack_id
        if tags is not None:
            self._values["tags"] = tags
        if use_custom_cookbooks is not None:
            self._values["use_custom_cookbooks"] = use_custom_cookbooks
        if use_opsworks_security_groups is not None:
            self._values["use_opsworks_security_groups"] = use_opsworks_security_groups
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def default_instance_profile_arn(self) -> builtins.str:
        """``AWS::OpsWorks::Stack.DefaultInstanceProfileArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultinstanceprof
        """
        result = self._values.get("default_instance_profile_arn")
        assert result is not None, "Required property 'default_instance_profile_arn' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::OpsWorks::Stack.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def service_role_arn(self) -> builtins.str:
        """``AWS::OpsWorks::Stack.ServiceRoleArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-servicerolearn
        """
        result = self._values.get("service_role_arn")
        assert result is not None, "Required property 'service_role_arn' is missing"
        return result

    @builtins.property
    def agent_version(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.AgentVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-agentversion
        """
        result = self._values.get("agent_version")
        return result

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
        """``AWS::OpsWorks::Stack.Attributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-attributes
        """
        result = self._values.get("attributes")
        return result

    @builtins.property
    def chef_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStack.ChefConfigurationProperty]]:
        """``AWS::OpsWorks::Stack.ChefConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-chefconfiguration
        """
        result = self._values.get("chef_configuration")
        return result

    @builtins.property
    def clone_app_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::OpsWorks::Stack.CloneAppIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-cloneappids
        """
        result = self._values.get("clone_app_ids")
        return result

    @builtins.property
    def clone_permissions(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Stack.ClonePermissions``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-clonepermissions
        """
        result = self._values.get("clone_permissions")
        return result

    @builtins.property
    def configuration_manager(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStack.StackConfigurationManagerProperty]]:
        """``AWS::OpsWorks::Stack.ConfigurationManager``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-configmanager
        """
        result = self._values.get("configuration_manager")
        return result

    @builtins.property
    def custom_cookbooks_source(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnStack.SourceProperty]]:
        """``AWS::OpsWorks::Stack.CustomCookbooksSource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-custcookbooksource
        """
        result = self._values.get("custom_cookbooks_source")
        return result

    @builtins.property
    def custom_json(self) -> typing.Any:
        """``AWS::OpsWorks::Stack.CustomJson``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-custjson
        """
        result = self._values.get("custom_json")
        return result

    @builtins.property
    def default_availability_zone(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.DefaultAvailabilityZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultaz
        """
        result = self._values.get("default_availability_zone")
        return result

    @builtins.property
    def default_os(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.DefaultOs``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultos
        """
        result = self._values.get("default_os")
        return result

    @builtins.property
    def default_root_device_type(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.DefaultRootDeviceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultrootdevicetype
        """
        result = self._values.get("default_root_device_type")
        return result

    @builtins.property
    def default_ssh_key_name(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.DefaultSshKeyName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-defaultsshkeyname
        """
        result = self._values.get("default_ssh_key_name")
        return result

    @builtins.property
    def default_subnet_id(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.DefaultSubnetId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#defaultsubnet
        """
        result = self._values.get("default_subnet_id")
        return result

    @builtins.property
    def ecs_cluster_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.EcsClusterArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-ecsclusterarn
        """
        result = self._values.get("ecs_cluster_arn")
        return result

    @builtins.property
    def elastic_ips(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStack.ElasticIpProperty]]]]:
        """``AWS::OpsWorks::Stack.ElasticIps``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-elasticips
        """
        result = self._values.get("elastic_ips")
        return result

    @builtins.property
    def hostname_theme(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.HostnameTheme``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-hostnametheme
        """
        result = self._values.get("hostname_theme")
        return result

    @builtins.property
    def rds_db_instances(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnStack.RdsDbInstanceProperty]]]]:
        """``AWS::OpsWorks::Stack.RdsDbInstances``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-rdsdbinstances
        """
        result = self._values.get("rds_db_instances")
        return result

    @builtins.property
    def source_stack_id(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.SourceStackId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-sourcestackid
        """
        result = self._values.get("source_stack_id")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::OpsWorks::Stack.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def use_custom_cookbooks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Stack.UseCustomCookbooks``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#usecustcookbooks
        """
        result = self._values.get("use_custom_cookbooks")
        return result

    @builtins.property
    def use_opsworks_security_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::Stack.UseOpsworksSecurityGroups``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-useopsworkssecuritygroups
        """
        result = self._values.get("use_opsworks_security_groups")
        return result

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Stack.VpcId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-stack.html#cfn-opsworks-stack-vpcid
        """
        result = self._values.get("vpc_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnUserProfile(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opsworks.CfnUserProfile",
):
    """A CloudFormation ``AWS::OpsWorks::UserProfile``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html
    :cloudformationResource: AWS::OpsWorks::UserProfile
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        iam_user_arn: builtins.str,
        allow_self_management: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ssh_public_key: typing.Optional[builtins.str] = None,
        ssh_username: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::OpsWorks::UserProfile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param iam_user_arn: ``AWS::OpsWorks::UserProfile.IamUserArn``.
        :param allow_self_management: ``AWS::OpsWorks::UserProfile.AllowSelfManagement``.
        :param ssh_public_key: ``AWS::OpsWorks::UserProfile.SshPublicKey``.
        :param ssh_username: ``AWS::OpsWorks::UserProfile.SshUsername``.
        """
        props = CfnUserProfileProps(
            iam_user_arn=iam_user_arn,
            allow_self_management=allow_self_management,
            ssh_public_key=ssh_public_key,
            ssh_username=ssh_username,
        )

        jsii.create(CfnUserProfile, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrSshUsername")
    def attr_ssh_username(self) -> builtins.str:
        """
        :cloudformationAttribute: SshUsername
        """
        return jsii.get(self, "attrSshUsername")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="iamUserArn")
    def iam_user_arn(self) -> builtins.str:
        """``AWS::OpsWorks::UserProfile.IamUserArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-iamuserarn
        """
        return jsii.get(self, "iamUserArn")

    @iam_user_arn.setter # type: ignore
    def iam_user_arn(self, value: builtins.str) -> None:
        jsii.set(self, "iamUserArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowSelfManagement")
    def allow_self_management(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::UserProfile.AllowSelfManagement``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-allowselfmanagement
        """
        return jsii.get(self, "allowSelfManagement")

    @allow_self_management.setter # type: ignore
    def allow_self_management(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "allowSelfManagement", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sshPublicKey")
    def ssh_public_key(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::UserProfile.SshPublicKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshpublickey
        """
        return jsii.get(self, "sshPublicKey")

    @ssh_public_key.setter # type: ignore
    def ssh_public_key(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sshPublicKey", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sshUsername")
    def ssh_username(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::UserProfile.SshUsername``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshusername
        """
        return jsii.get(self, "sshUsername")

    @ssh_username.setter # type: ignore
    def ssh_username(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sshUsername", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opsworks.CfnUserProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "iam_user_arn": "iamUserArn",
        "allow_self_management": "allowSelfManagement",
        "ssh_public_key": "sshPublicKey",
        "ssh_username": "sshUsername",
    },
)
class CfnUserProfileProps:
    def __init__(
        self,
        *,
        iam_user_arn: builtins.str,
        allow_self_management: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ssh_public_key: typing.Optional[builtins.str] = None,
        ssh_username: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::OpsWorks::UserProfile``.

        :param iam_user_arn: ``AWS::OpsWorks::UserProfile.IamUserArn``.
        :param allow_self_management: ``AWS::OpsWorks::UserProfile.AllowSelfManagement``.
        :param ssh_public_key: ``AWS::OpsWorks::UserProfile.SshPublicKey``.
        :param ssh_username: ``AWS::OpsWorks::UserProfile.SshUsername``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "iam_user_arn": iam_user_arn,
        }
        if allow_self_management is not None:
            self._values["allow_self_management"] = allow_self_management
        if ssh_public_key is not None:
            self._values["ssh_public_key"] = ssh_public_key
        if ssh_username is not None:
            self._values["ssh_username"] = ssh_username

    @builtins.property
    def iam_user_arn(self) -> builtins.str:
        """``AWS::OpsWorks::UserProfile.IamUserArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-iamuserarn
        """
        result = self._values.get("iam_user_arn")
        assert result is not None, "Required property 'iam_user_arn' is missing"
        return result

    @builtins.property
    def allow_self_management(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::OpsWorks::UserProfile.AllowSelfManagement``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-allowselfmanagement
        """
        result = self._values.get("allow_self_management")
        return result

    @builtins.property
    def ssh_public_key(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::UserProfile.SshPublicKey``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshpublickey
        """
        result = self._values.get("ssh_public_key")
        return result

    @builtins.property
    def ssh_username(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::UserProfile.SshUsername``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-userprofile.html#cfn-opsworks-userprofile-sshusername
        """
        result = self._values.get("ssh_username")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnVolume(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opsworks.CfnVolume",
):
    """A CloudFormation ``AWS::OpsWorks::Volume``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html
    :cloudformationResource: AWS::OpsWorks::Volume
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        ec2_volume_id: builtins.str,
        stack_id: builtins.str,
        mount_point: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::OpsWorks::Volume``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param ec2_volume_id: ``AWS::OpsWorks::Volume.Ec2VolumeId``.
        :param stack_id: ``AWS::OpsWorks::Volume.StackId``.
        :param mount_point: ``AWS::OpsWorks::Volume.MountPoint``.
        :param name: ``AWS::OpsWorks::Volume.Name``.
        """
        props = CfnVolumeProps(
            ec2_volume_id=ec2_volume_id,
            stack_id=stack_id,
            mount_point=mount_point,
            name=name,
        )

        jsii.create(CfnVolume, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="ec2VolumeId")
    def ec2_volume_id(self) -> builtins.str:
        """``AWS::OpsWorks::Volume.Ec2VolumeId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-ec2volumeid
        """
        return jsii.get(self, "ec2VolumeId")

    @ec2_volume_id.setter # type: ignore
    def ec2_volume_id(self, value: builtins.str) -> None:
        jsii.set(self, "ec2VolumeId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> builtins.str:
        """``AWS::OpsWorks::Volume.StackId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-stackid
        """
        return jsii.get(self, "stackId")

    @stack_id.setter # type: ignore
    def stack_id(self, value: builtins.str) -> None:
        jsii.set(self, "stackId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="mountPoint")
    def mount_point(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Volume.MountPoint``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-mountpoint
        """
        return jsii.get(self, "mountPoint")

    @mount_point.setter # type: ignore
    def mount_point(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "mountPoint", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Volume.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opsworks.CfnVolumeProps",
    jsii_struct_bases=[],
    name_mapping={
        "ec2_volume_id": "ec2VolumeId",
        "stack_id": "stackId",
        "mount_point": "mountPoint",
        "name": "name",
    },
)
class CfnVolumeProps:
    def __init__(
        self,
        *,
        ec2_volume_id: builtins.str,
        stack_id: builtins.str,
        mount_point: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::OpsWorks::Volume``.

        :param ec2_volume_id: ``AWS::OpsWorks::Volume.Ec2VolumeId``.
        :param stack_id: ``AWS::OpsWorks::Volume.StackId``.
        :param mount_point: ``AWS::OpsWorks::Volume.MountPoint``.
        :param name: ``AWS::OpsWorks::Volume.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "ec2_volume_id": ec2_volume_id,
            "stack_id": stack_id,
        }
        if mount_point is not None:
            self._values["mount_point"] = mount_point
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def ec2_volume_id(self) -> builtins.str:
        """``AWS::OpsWorks::Volume.Ec2VolumeId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-ec2volumeid
        """
        result = self._values.get("ec2_volume_id")
        assert result is not None, "Required property 'ec2_volume_id' is missing"
        return result

    @builtins.property
    def stack_id(self) -> builtins.str:
        """``AWS::OpsWorks::Volume.StackId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-stackid
        """
        result = self._values.get("stack_id")
        assert result is not None, "Required property 'stack_id' is missing"
        return result

    @builtins.property
    def mount_point(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Volume.MountPoint``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-mountpoint
        """
        result = self._values.get("mount_point")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """``AWS::OpsWorks::Volume.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opsworks-volume.html#cfn-opsworks-volume-name
        """
        result = self._values.get("name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVolumeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApp",
    "CfnAppProps",
    "CfnElasticLoadBalancerAttachment",
    "CfnElasticLoadBalancerAttachmentProps",
    "CfnInstance",
    "CfnInstanceProps",
    "CfnLayer",
    "CfnLayerProps",
    "CfnStack",
    "CfnStackProps",
    "CfnUserProfile",
    "CfnUserProfileProps",
    "CfnVolume",
    "CfnVolumeProps",
]

publication.publish()
