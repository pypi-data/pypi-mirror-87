"""
## AWS Database Migration Service Construct Library

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
class CfnCertificate(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-dms.CfnCertificate",
):
    """A CloudFormation ``AWS::DMS::Certificate``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html
    :cloudformationResource: AWS::DMS::Certificate
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        certificate_identifier: typing.Optional[builtins.str] = None,
        certificate_pem: typing.Optional[builtins.str] = None,
        certificate_wallet: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::DMS::Certificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate_identifier: ``AWS::DMS::Certificate.CertificateIdentifier``.
        :param certificate_pem: ``AWS::DMS::Certificate.CertificatePem``.
        :param certificate_wallet: ``AWS::DMS::Certificate.CertificateWallet``.
        """
        props = CfnCertificateProps(
            certificate_identifier=certificate_identifier,
            certificate_pem=certificate_pem,
            certificate_wallet=certificate_wallet,
        )

        jsii.create(CfnCertificate, self, [scope, id, props])

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
    @jsii.member(jsii_name="certificateIdentifier")
    def certificate_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Certificate.CertificateIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html#cfn-dms-certificate-certificateidentifier
        """
        return jsii.get(self, "certificateIdentifier")

    @certificate_identifier.setter # type: ignore
    def certificate_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "certificateIdentifier", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificatePem")
    def certificate_pem(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Certificate.CertificatePem``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html#cfn-dms-certificate-certificatepem
        """
        return jsii.get(self, "certificatePem")

    @certificate_pem.setter # type: ignore
    def certificate_pem(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "certificatePem", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateWallet")
    def certificate_wallet(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Certificate.CertificateWallet``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html#cfn-dms-certificate-certificatewallet
        """
        return jsii.get(self, "certificateWallet")

    @certificate_wallet.setter # type: ignore
    def certificate_wallet(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "certificateWallet", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dms.CfnCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_identifier": "certificateIdentifier",
        "certificate_pem": "certificatePem",
        "certificate_wallet": "certificateWallet",
    },
)
class CfnCertificateProps:
    def __init__(
        self,
        *,
        certificate_identifier: typing.Optional[builtins.str] = None,
        certificate_pem: typing.Optional[builtins.str] = None,
        certificate_wallet: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::DMS::Certificate``.

        :param certificate_identifier: ``AWS::DMS::Certificate.CertificateIdentifier``.
        :param certificate_pem: ``AWS::DMS::Certificate.CertificatePem``.
        :param certificate_wallet: ``AWS::DMS::Certificate.CertificateWallet``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if certificate_identifier is not None:
            self._values["certificate_identifier"] = certificate_identifier
        if certificate_pem is not None:
            self._values["certificate_pem"] = certificate_pem
        if certificate_wallet is not None:
            self._values["certificate_wallet"] = certificate_wallet

    @builtins.property
    def certificate_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Certificate.CertificateIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html#cfn-dms-certificate-certificateidentifier
        """
        result = self._values.get("certificate_identifier")
        return result

    @builtins.property
    def certificate_pem(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Certificate.CertificatePem``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html#cfn-dms-certificate-certificatepem
        """
        result = self._values.get("certificate_pem")
        return result

    @builtins.property
    def certificate_wallet(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Certificate.CertificateWallet``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-certificate.html#cfn-dms-certificate-certificatewallet
        """
        result = self._values.get("certificate_wallet")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEndpoint(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-dms.CfnEndpoint",
):
    """A CloudFormation ``AWS::DMS::Endpoint``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html
    :cloudformationResource: AWS::DMS::Endpoint
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        endpoint_type: builtins.str,
        engine_name: builtins.str,
        certificate_arn: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        dynamo_db_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.DynamoDbSettingsProperty"]] = None,
        elasticsearch_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.ElasticsearchSettingsProperty"]] = None,
        endpoint_identifier: typing.Optional[builtins.str] = None,
        extra_connection_attributes: typing.Optional[builtins.str] = None,
        kafka_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.KafkaSettingsProperty"]] = None,
        kinesis_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.KinesisSettingsProperty"]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        mongo_db_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.MongoDbSettingsProperty"]] = None,
        neptune_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.NeptuneSettingsProperty"]] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        s3_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.S3SettingsProperty"]] = None,
        server_name: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::DMS::Endpoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param endpoint_type: ``AWS::DMS::Endpoint.EndpointType``.
        :param engine_name: ``AWS::DMS::Endpoint.EngineName``.
        :param certificate_arn: ``AWS::DMS::Endpoint.CertificateArn``.
        :param database_name: ``AWS::DMS::Endpoint.DatabaseName``.
        :param dynamo_db_settings: ``AWS::DMS::Endpoint.DynamoDbSettings``.
        :param elasticsearch_settings: ``AWS::DMS::Endpoint.ElasticsearchSettings``.
        :param endpoint_identifier: ``AWS::DMS::Endpoint.EndpointIdentifier``.
        :param extra_connection_attributes: ``AWS::DMS::Endpoint.ExtraConnectionAttributes``.
        :param kafka_settings: ``AWS::DMS::Endpoint.KafkaSettings``.
        :param kinesis_settings: ``AWS::DMS::Endpoint.KinesisSettings``.
        :param kms_key_id: ``AWS::DMS::Endpoint.KmsKeyId``.
        :param mongo_db_settings: ``AWS::DMS::Endpoint.MongoDbSettings``.
        :param neptune_settings: ``AWS::DMS::Endpoint.NeptuneSettings``.
        :param password: ``AWS::DMS::Endpoint.Password``.
        :param port: ``AWS::DMS::Endpoint.Port``.
        :param s3_settings: ``AWS::DMS::Endpoint.S3Settings``.
        :param server_name: ``AWS::DMS::Endpoint.ServerName``.
        :param ssl_mode: ``AWS::DMS::Endpoint.SslMode``.
        :param tags: ``AWS::DMS::Endpoint.Tags``.
        :param username: ``AWS::DMS::Endpoint.Username``.
        """
        props = CfnEndpointProps(
            endpoint_type=endpoint_type,
            engine_name=engine_name,
            certificate_arn=certificate_arn,
            database_name=database_name,
            dynamo_db_settings=dynamo_db_settings,
            elasticsearch_settings=elasticsearch_settings,
            endpoint_identifier=endpoint_identifier,
            extra_connection_attributes=extra_connection_attributes,
            kafka_settings=kafka_settings,
            kinesis_settings=kinesis_settings,
            kms_key_id=kms_key_id,
            mongo_db_settings=mongo_db_settings,
            neptune_settings=neptune_settings,
            password=password,
            port=port,
            s3_settings=s3_settings,
            server_name=server_name,
            ssl_mode=ssl_mode,
            tags=tags,
            username=username,
        )

        jsii.create(CfnEndpoint, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrExternalId")
    def attr_external_id(self) -> builtins.str:
        """
        :cloudformationAttribute: ExternalId
        """
        return jsii.get(self, "attrExternalId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::DMS::Endpoint.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> builtins.str:
        """``AWS::DMS::Endpoint.EndpointType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-endpointtype
        """
        return jsii.get(self, "endpointType")

    @endpoint_type.setter # type: ignore
    def endpoint_type(self, value: builtins.str) -> None:
        jsii.set(self, "endpointType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engineName")
    def engine_name(self) -> builtins.str:
        """``AWS::DMS::Endpoint.EngineName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-enginename
        """
        return jsii.get(self, "engineName")

    @engine_name.setter # type: ignore
    def engine_name(self, value: builtins.str) -> None:
        jsii.set(self, "engineName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.CertificateArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-certificatearn
        """
        return jsii.get(self, "certificateArn")

    @certificate_arn.setter # type: ignore
    def certificate_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "certificateArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.DatabaseName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-databasename
        """
        return jsii.get(self, "databaseName")

    @database_name.setter # type: ignore
    def database_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "databaseName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dynamoDbSettings")
    def dynamo_db_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.DynamoDbSettingsProperty"]]:
        """``AWS::DMS::Endpoint.DynamoDbSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-dynamodbsettings
        """
        return jsii.get(self, "dynamoDbSettings")

    @dynamo_db_settings.setter # type: ignore
    def dynamo_db_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.DynamoDbSettingsProperty"]],
    ) -> None:
        jsii.set(self, "dynamoDbSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="elasticsearchSettings")
    def elasticsearch_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.ElasticsearchSettingsProperty"]]:
        """``AWS::DMS::Endpoint.ElasticsearchSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-elasticsearchsettings
        """
        return jsii.get(self, "elasticsearchSettings")

    @elasticsearch_settings.setter # type: ignore
    def elasticsearch_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.ElasticsearchSettingsProperty"]],
    ) -> None:
        jsii.set(self, "elasticsearchSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpointIdentifier")
    def endpoint_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.EndpointIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-endpointidentifier
        """
        return jsii.get(self, "endpointIdentifier")

    @endpoint_identifier.setter # type: ignore
    def endpoint_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "endpointIdentifier", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="extraConnectionAttributes")
    def extra_connection_attributes(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.ExtraConnectionAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-extraconnectionattributes
        """
        return jsii.get(self, "extraConnectionAttributes")

    @extra_connection_attributes.setter # type: ignore
    def extra_connection_attributes(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "extraConnectionAttributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kafkaSettings")
    def kafka_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.KafkaSettingsProperty"]]:
        """``AWS::DMS::Endpoint.KafkaSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-kafkasettings
        """
        return jsii.get(self, "kafkaSettings")

    @kafka_settings.setter # type: ignore
    def kafka_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.KafkaSettingsProperty"]],
    ) -> None:
        jsii.set(self, "kafkaSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kinesisSettings")
    def kinesis_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.KinesisSettingsProperty"]]:
        """``AWS::DMS::Endpoint.KinesisSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-kinesissettings
        """
        return jsii.get(self, "kinesisSettings")

    @kinesis_settings.setter # type: ignore
    def kinesis_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.KinesisSettingsProperty"]],
    ) -> None:
        jsii.set(self, "kinesisSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter # type: ignore
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="mongoDbSettings")
    def mongo_db_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.MongoDbSettingsProperty"]]:
        """``AWS::DMS::Endpoint.MongoDbSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-mongodbsettings
        """
        return jsii.get(self, "mongoDbSettings")

    @mongo_db_settings.setter # type: ignore
    def mongo_db_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.MongoDbSettingsProperty"]],
    ) -> None:
        jsii.set(self, "mongoDbSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="neptuneSettings")
    def neptune_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.NeptuneSettingsProperty"]]:
        """``AWS::DMS::Endpoint.NeptuneSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-neptunesettings
        """
        return jsii.get(self, "neptuneSettings")

    @neptune_settings.setter # type: ignore
    def neptune_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.NeptuneSettingsProperty"]],
    ) -> None:
        jsii.set(self, "neptuneSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.Password``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-password
        """
        return jsii.get(self, "password")

    @password.setter # type: ignore
    def password(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "password", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::DMS::Endpoint.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-port
        """
        return jsii.get(self, "port")

    @port.setter # type: ignore
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="s3Settings")
    def s3_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.S3SettingsProperty"]]:
        """``AWS::DMS::Endpoint.S3Settings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-s3settings
        """
        return jsii.get(self, "s3Settings")

    @s3_settings.setter # type: ignore
    def s3_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnEndpoint.S3SettingsProperty"]],
    ) -> None:
        jsii.set(self, "s3Settings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serverName")
    def server_name(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.ServerName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-servername
        """
        return jsii.get(self, "serverName")

    @server_name.setter # type: ignore
    def server_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "serverName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sslMode")
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.SslMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-sslmode
        """
        return jsii.get(self, "sslMode")

    @ssl_mode.setter # type: ignore
    def ssl_mode(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sslMode", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="username")
    def username(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.Username``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-username
        """
        return jsii.get(self, "username")

    @username.setter # type: ignore
    def username(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "username", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dms.CfnEndpoint.DynamoDbSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"service_access_role_arn": "serviceAccessRoleArn"},
    )
    class DynamoDbSettingsProperty:
        def __init__(
            self,
            *,
            service_access_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param service_access_role_arn: ``CfnEndpoint.DynamoDbSettingsProperty.ServiceAccessRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-dynamodbsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if service_access_role_arn is not None:
                self._values["service_access_role_arn"] = service_access_role_arn

        @builtins.property
        def service_access_role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.DynamoDbSettingsProperty.ServiceAccessRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-dynamodbsettings.html#cfn-dms-endpoint-dynamodbsettings-serviceaccessrolearn
            """
            result = self._values.get("service_access_role_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDbSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dms.CfnEndpoint.ElasticsearchSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint_uri": "endpointUri",
            "error_retry_duration": "errorRetryDuration",
            "full_load_error_percentage": "fullLoadErrorPercentage",
            "service_access_role_arn": "serviceAccessRoleArn",
        },
    )
    class ElasticsearchSettingsProperty:
        def __init__(
            self,
            *,
            endpoint_uri: typing.Optional[builtins.str] = None,
            error_retry_duration: typing.Optional[jsii.Number] = None,
            full_load_error_percentage: typing.Optional[jsii.Number] = None,
            service_access_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param endpoint_uri: ``CfnEndpoint.ElasticsearchSettingsProperty.EndpointUri``.
            :param error_retry_duration: ``CfnEndpoint.ElasticsearchSettingsProperty.ErrorRetryDuration``.
            :param full_load_error_percentage: ``CfnEndpoint.ElasticsearchSettingsProperty.FullLoadErrorPercentage``.
            :param service_access_role_arn: ``CfnEndpoint.ElasticsearchSettingsProperty.ServiceAccessRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-elasticsearchsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if endpoint_uri is not None:
                self._values["endpoint_uri"] = endpoint_uri
            if error_retry_duration is not None:
                self._values["error_retry_duration"] = error_retry_duration
            if full_load_error_percentage is not None:
                self._values["full_load_error_percentage"] = full_load_error_percentage
            if service_access_role_arn is not None:
                self._values["service_access_role_arn"] = service_access_role_arn

        @builtins.property
        def endpoint_uri(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.ElasticsearchSettingsProperty.EndpointUri``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-elasticsearchsettings.html#cfn-dms-endpoint-elasticsearchsettings-endpointuri
            """
            result = self._values.get("endpoint_uri")
            return result

        @builtins.property
        def error_retry_duration(self) -> typing.Optional[jsii.Number]:
            """``CfnEndpoint.ElasticsearchSettingsProperty.ErrorRetryDuration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-elasticsearchsettings.html#cfn-dms-endpoint-elasticsearchsettings-errorretryduration
            """
            result = self._values.get("error_retry_duration")
            return result

        @builtins.property
        def full_load_error_percentage(self) -> typing.Optional[jsii.Number]:
            """``CfnEndpoint.ElasticsearchSettingsProperty.FullLoadErrorPercentage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-elasticsearchsettings.html#cfn-dms-endpoint-elasticsearchsettings-fullloaderrorpercentage
            """
            result = self._values.get("full_load_error_percentage")
            return result

        @builtins.property
        def service_access_role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.ElasticsearchSettingsProperty.ServiceAccessRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-elasticsearchsettings.html#cfn-dms-endpoint-elasticsearchsettings-serviceaccessrolearn
            """
            result = self._values.get("service_access_role_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dms.CfnEndpoint.KafkaSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"broker": "broker", "topic": "topic"},
    )
    class KafkaSettingsProperty:
        def __init__(
            self,
            *,
            broker: typing.Optional[builtins.str] = None,
            topic: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param broker: ``CfnEndpoint.KafkaSettingsProperty.Broker``.
            :param topic: ``CfnEndpoint.KafkaSettingsProperty.Topic``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if broker is not None:
                self._values["broker"] = broker
            if topic is not None:
                self._values["topic"] = topic

        @builtins.property
        def broker(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.KafkaSettingsProperty.Broker``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-broker
            """
            result = self._values.get("broker")
            return result

        @builtins.property
        def topic(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.KafkaSettingsProperty.Topic``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kafkasettings.html#cfn-dms-endpoint-kafkasettings-topic
            """
            result = self._values.get("topic")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dms.CfnEndpoint.KinesisSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "message_format": "messageFormat",
            "service_access_role_arn": "serviceAccessRoleArn",
            "stream_arn": "streamArn",
        },
    )
    class KinesisSettingsProperty:
        def __init__(
            self,
            *,
            message_format: typing.Optional[builtins.str] = None,
            service_access_role_arn: typing.Optional[builtins.str] = None,
            stream_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param message_format: ``CfnEndpoint.KinesisSettingsProperty.MessageFormat``.
            :param service_access_role_arn: ``CfnEndpoint.KinesisSettingsProperty.ServiceAccessRoleArn``.
            :param stream_arn: ``CfnEndpoint.KinesisSettingsProperty.StreamArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if message_format is not None:
                self._values["message_format"] = message_format
            if service_access_role_arn is not None:
                self._values["service_access_role_arn"] = service_access_role_arn
            if stream_arn is not None:
                self._values["stream_arn"] = stream_arn

        @builtins.property
        def message_format(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.KinesisSettingsProperty.MessageFormat``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-messageformat
            """
            result = self._values.get("message_format")
            return result

        @builtins.property
        def service_access_role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.KinesisSettingsProperty.ServiceAccessRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-serviceaccessrolearn
            """
            result = self._values.get("service_access_role_arn")
            return result

        @builtins.property
        def stream_arn(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.KinesisSettingsProperty.StreamArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-kinesissettings.html#cfn-dms-endpoint-kinesissettings-streamarn
            """
            result = self._values.get("stream_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dms.CfnEndpoint.MongoDbSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_mechanism": "authMechanism",
            "auth_source": "authSource",
            "auth_type": "authType",
            "database_name": "databaseName",
            "docs_to_investigate": "docsToInvestigate",
            "extract_doc_id": "extractDocId",
            "nesting_level": "nestingLevel",
            "password": "password",
            "port": "port",
            "server_name": "serverName",
            "username": "username",
        },
    )
    class MongoDbSettingsProperty:
        def __init__(
            self,
            *,
            auth_mechanism: typing.Optional[builtins.str] = None,
            auth_source: typing.Optional[builtins.str] = None,
            auth_type: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            docs_to_investigate: typing.Optional[builtins.str] = None,
            extract_doc_id: typing.Optional[builtins.str] = None,
            nesting_level: typing.Optional[builtins.str] = None,
            password: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            server_name: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param auth_mechanism: ``CfnEndpoint.MongoDbSettingsProperty.AuthMechanism``.
            :param auth_source: ``CfnEndpoint.MongoDbSettingsProperty.AuthSource``.
            :param auth_type: ``CfnEndpoint.MongoDbSettingsProperty.AuthType``.
            :param database_name: ``CfnEndpoint.MongoDbSettingsProperty.DatabaseName``.
            :param docs_to_investigate: ``CfnEndpoint.MongoDbSettingsProperty.DocsToInvestigate``.
            :param extract_doc_id: ``CfnEndpoint.MongoDbSettingsProperty.ExtractDocId``.
            :param nesting_level: ``CfnEndpoint.MongoDbSettingsProperty.NestingLevel``.
            :param password: ``CfnEndpoint.MongoDbSettingsProperty.Password``.
            :param port: ``CfnEndpoint.MongoDbSettingsProperty.Port``.
            :param server_name: ``CfnEndpoint.MongoDbSettingsProperty.ServerName``.
            :param username: ``CfnEndpoint.MongoDbSettingsProperty.Username``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if auth_mechanism is not None:
                self._values["auth_mechanism"] = auth_mechanism
            if auth_source is not None:
                self._values["auth_source"] = auth_source
            if auth_type is not None:
                self._values["auth_type"] = auth_type
            if database_name is not None:
                self._values["database_name"] = database_name
            if docs_to_investigate is not None:
                self._values["docs_to_investigate"] = docs_to_investigate
            if extract_doc_id is not None:
                self._values["extract_doc_id"] = extract_doc_id
            if nesting_level is not None:
                self._values["nesting_level"] = nesting_level
            if password is not None:
                self._values["password"] = password
            if port is not None:
                self._values["port"] = port
            if server_name is not None:
                self._values["server_name"] = server_name
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def auth_mechanism(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.MongoDbSettingsProperty.AuthMechanism``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-authmechanism
            """
            result = self._values.get("auth_mechanism")
            return result

        @builtins.property
        def auth_source(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.MongoDbSettingsProperty.AuthSource``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-authsource
            """
            result = self._values.get("auth_source")
            return result

        @builtins.property
        def auth_type(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.MongoDbSettingsProperty.AuthType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-authtype
            """
            result = self._values.get("auth_type")
            return result

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.MongoDbSettingsProperty.DatabaseName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-databasename
            """
            result = self._values.get("database_name")
            return result

        @builtins.property
        def docs_to_investigate(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.MongoDbSettingsProperty.DocsToInvestigate``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-docstoinvestigate
            """
            result = self._values.get("docs_to_investigate")
            return result

        @builtins.property
        def extract_doc_id(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.MongoDbSettingsProperty.ExtractDocId``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-extractdocid
            """
            result = self._values.get("extract_doc_id")
            return result

        @builtins.property
        def nesting_level(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.MongoDbSettingsProperty.NestingLevel``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-nestinglevel
            """
            result = self._values.get("nesting_level")
            return result

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.MongoDbSettingsProperty.Password``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-password
            """
            result = self._values.get("password")
            return result

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            """``CfnEndpoint.MongoDbSettingsProperty.Port``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-port
            """
            result = self._values.get("port")
            return result

        @builtins.property
        def server_name(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.MongoDbSettingsProperty.ServerName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-servername
            """
            result = self._values.get("server_name")
            return result

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.MongoDbSettingsProperty.Username``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-mongodbsettings.html#cfn-dms-endpoint-mongodbsettings-username
            """
            result = self._values.get("username")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MongoDbSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dms.CfnEndpoint.NeptuneSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "error_retry_duration": "errorRetryDuration",
            "iam_auth_enabled": "iamAuthEnabled",
            "max_file_size": "maxFileSize",
            "max_retry_count": "maxRetryCount",
            "s3_bucket_folder": "s3BucketFolder",
            "s3_bucket_name": "s3BucketName",
            "service_access_role_arn": "serviceAccessRoleArn",
        },
    )
    class NeptuneSettingsProperty:
        def __init__(
            self,
            *,
            error_retry_duration: typing.Optional[jsii.Number] = None,
            iam_auth_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            max_file_size: typing.Optional[jsii.Number] = None,
            max_retry_count: typing.Optional[jsii.Number] = None,
            s3_bucket_folder: typing.Optional[builtins.str] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
            service_access_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param error_retry_duration: ``CfnEndpoint.NeptuneSettingsProperty.ErrorRetryDuration``.
            :param iam_auth_enabled: ``CfnEndpoint.NeptuneSettingsProperty.IamAuthEnabled``.
            :param max_file_size: ``CfnEndpoint.NeptuneSettingsProperty.MaxFileSize``.
            :param max_retry_count: ``CfnEndpoint.NeptuneSettingsProperty.MaxRetryCount``.
            :param s3_bucket_folder: ``CfnEndpoint.NeptuneSettingsProperty.S3BucketFolder``.
            :param s3_bucket_name: ``CfnEndpoint.NeptuneSettingsProperty.S3BucketName``.
            :param service_access_role_arn: ``CfnEndpoint.NeptuneSettingsProperty.ServiceAccessRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if error_retry_duration is not None:
                self._values["error_retry_duration"] = error_retry_duration
            if iam_auth_enabled is not None:
                self._values["iam_auth_enabled"] = iam_auth_enabled
            if max_file_size is not None:
                self._values["max_file_size"] = max_file_size
            if max_retry_count is not None:
                self._values["max_retry_count"] = max_retry_count
            if s3_bucket_folder is not None:
                self._values["s3_bucket_folder"] = s3_bucket_folder
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name
            if service_access_role_arn is not None:
                self._values["service_access_role_arn"] = service_access_role_arn

        @builtins.property
        def error_retry_duration(self) -> typing.Optional[jsii.Number]:
            """``CfnEndpoint.NeptuneSettingsProperty.ErrorRetryDuration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-errorretryduration
            """
            result = self._values.get("error_retry_duration")
            return result

        @builtins.property
        def iam_auth_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnEndpoint.NeptuneSettingsProperty.IamAuthEnabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-iamauthenabled
            """
            result = self._values.get("iam_auth_enabled")
            return result

        @builtins.property
        def max_file_size(self) -> typing.Optional[jsii.Number]:
            """``CfnEndpoint.NeptuneSettingsProperty.MaxFileSize``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-maxfilesize
            """
            result = self._values.get("max_file_size")
            return result

        @builtins.property
        def max_retry_count(self) -> typing.Optional[jsii.Number]:
            """``CfnEndpoint.NeptuneSettingsProperty.MaxRetryCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-maxretrycount
            """
            result = self._values.get("max_retry_count")
            return result

        @builtins.property
        def s3_bucket_folder(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.NeptuneSettingsProperty.S3BucketFolder``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-s3bucketfolder
            """
            result = self._values.get("s3_bucket_folder")
            return result

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.NeptuneSettingsProperty.S3BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-s3bucketname
            """
            result = self._values.get("s3_bucket_name")
            return result

        @builtins.property
        def service_access_role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.NeptuneSettingsProperty.ServiceAccessRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-neptunesettings.html#cfn-dms-endpoint-neptunesettings-serviceaccessrolearn
            """
            result = self._values.get("service_access_role_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NeptuneSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-dms.CfnEndpoint.S3SettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_folder": "bucketFolder",
            "bucket_name": "bucketName",
            "compression_type": "compressionType",
            "csv_delimiter": "csvDelimiter",
            "csv_row_delimiter": "csvRowDelimiter",
            "external_table_definition": "externalTableDefinition",
            "service_access_role_arn": "serviceAccessRoleArn",
        },
    )
    class S3SettingsProperty:
        def __init__(
            self,
            *,
            bucket_folder: typing.Optional[builtins.str] = None,
            bucket_name: typing.Optional[builtins.str] = None,
            compression_type: typing.Optional[builtins.str] = None,
            csv_delimiter: typing.Optional[builtins.str] = None,
            csv_row_delimiter: typing.Optional[builtins.str] = None,
            external_table_definition: typing.Optional[builtins.str] = None,
            service_access_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param bucket_folder: ``CfnEndpoint.S3SettingsProperty.BucketFolder``.
            :param bucket_name: ``CfnEndpoint.S3SettingsProperty.BucketName``.
            :param compression_type: ``CfnEndpoint.S3SettingsProperty.CompressionType``.
            :param csv_delimiter: ``CfnEndpoint.S3SettingsProperty.CsvDelimiter``.
            :param csv_row_delimiter: ``CfnEndpoint.S3SettingsProperty.CsvRowDelimiter``.
            :param external_table_definition: ``CfnEndpoint.S3SettingsProperty.ExternalTableDefinition``.
            :param service_access_role_arn: ``CfnEndpoint.S3SettingsProperty.ServiceAccessRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if bucket_folder is not None:
                self._values["bucket_folder"] = bucket_folder
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if compression_type is not None:
                self._values["compression_type"] = compression_type
            if csv_delimiter is not None:
                self._values["csv_delimiter"] = csv_delimiter
            if csv_row_delimiter is not None:
                self._values["csv_row_delimiter"] = csv_row_delimiter
            if external_table_definition is not None:
                self._values["external_table_definition"] = external_table_definition
            if service_access_role_arn is not None:
                self._values["service_access_role_arn"] = service_access_role_arn

        @builtins.property
        def bucket_folder(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.S3SettingsProperty.BucketFolder``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-bucketfolder
            """
            result = self._values.get("bucket_folder")
            return result

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.S3SettingsProperty.BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-bucketname
            """
            result = self._values.get("bucket_name")
            return result

        @builtins.property
        def compression_type(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.S3SettingsProperty.CompressionType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-compressiontype
            """
            result = self._values.get("compression_type")
            return result

        @builtins.property
        def csv_delimiter(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.S3SettingsProperty.CsvDelimiter``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvdelimiter
            """
            result = self._values.get("csv_delimiter")
            return result

        @builtins.property
        def csv_row_delimiter(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.S3SettingsProperty.CsvRowDelimiter``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-csvrowdelimiter
            """
            result = self._values.get("csv_row_delimiter")
            return result

        @builtins.property
        def external_table_definition(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.S3SettingsProperty.ExternalTableDefinition``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-externaltabledefinition
            """
            result = self._values.get("external_table_definition")
            return result

        @builtins.property
        def service_access_role_arn(self) -> typing.Optional[builtins.str]:
            """``CfnEndpoint.S3SettingsProperty.ServiceAccessRoleArn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dms-endpoint-s3settings.html#cfn-dms-endpoint-s3settings-serviceaccessrolearn
            """
            result = self._values.get("service_access_role_arn")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3SettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dms.CfnEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_type": "endpointType",
        "engine_name": "engineName",
        "certificate_arn": "certificateArn",
        "database_name": "databaseName",
        "dynamo_db_settings": "dynamoDbSettings",
        "elasticsearch_settings": "elasticsearchSettings",
        "endpoint_identifier": "endpointIdentifier",
        "extra_connection_attributes": "extraConnectionAttributes",
        "kafka_settings": "kafkaSettings",
        "kinesis_settings": "kinesisSettings",
        "kms_key_id": "kmsKeyId",
        "mongo_db_settings": "mongoDbSettings",
        "neptune_settings": "neptuneSettings",
        "password": "password",
        "port": "port",
        "s3_settings": "s3Settings",
        "server_name": "serverName",
        "ssl_mode": "sslMode",
        "tags": "tags",
        "username": "username",
    },
)
class CfnEndpointProps:
    def __init__(
        self,
        *,
        endpoint_type: builtins.str,
        engine_name: builtins.str,
        certificate_arn: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
        dynamo_db_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.DynamoDbSettingsProperty]] = None,
        elasticsearch_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.ElasticsearchSettingsProperty]] = None,
        endpoint_identifier: typing.Optional[builtins.str] = None,
        extra_connection_attributes: typing.Optional[builtins.str] = None,
        kafka_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.KafkaSettingsProperty]] = None,
        kinesis_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.KinesisSettingsProperty]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        mongo_db_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.MongoDbSettingsProperty]] = None,
        neptune_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.NeptuneSettingsProperty]] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        s3_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.S3SettingsProperty]] = None,
        server_name: typing.Optional[builtins.str] = None,
        ssl_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::DMS::Endpoint``.

        :param endpoint_type: ``AWS::DMS::Endpoint.EndpointType``.
        :param engine_name: ``AWS::DMS::Endpoint.EngineName``.
        :param certificate_arn: ``AWS::DMS::Endpoint.CertificateArn``.
        :param database_name: ``AWS::DMS::Endpoint.DatabaseName``.
        :param dynamo_db_settings: ``AWS::DMS::Endpoint.DynamoDbSettings``.
        :param elasticsearch_settings: ``AWS::DMS::Endpoint.ElasticsearchSettings``.
        :param endpoint_identifier: ``AWS::DMS::Endpoint.EndpointIdentifier``.
        :param extra_connection_attributes: ``AWS::DMS::Endpoint.ExtraConnectionAttributes``.
        :param kafka_settings: ``AWS::DMS::Endpoint.KafkaSettings``.
        :param kinesis_settings: ``AWS::DMS::Endpoint.KinesisSettings``.
        :param kms_key_id: ``AWS::DMS::Endpoint.KmsKeyId``.
        :param mongo_db_settings: ``AWS::DMS::Endpoint.MongoDbSettings``.
        :param neptune_settings: ``AWS::DMS::Endpoint.NeptuneSettings``.
        :param password: ``AWS::DMS::Endpoint.Password``.
        :param port: ``AWS::DMS::Endpoint.Port``.
        :param s3_settings: ``AWS::DMS::Endpoint.S3Settings``.
        :param server_name: ``AWS::DMS::Endpoint.ServerName``.
        :param ssl_mode: ``AWS::DMS::Endpoint.SslMode``.
        :param tags: ``AWS::DMS::Endpoint.Tags``.
        :param username: ``AWS::DMS::Endpoint.Username``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_type": endpoint_type,
            "engine_name": engine_name,
        }
        if certificate_arn is not None:
            self._values["certificate_arn"] = certificate_arn
        if database_name is not None:
            self._values["database_name"] = database_name
        if dynamo_db_settings is not None:
            self._values["dynamo_db_settings"] = dynamo_db_settings
        if elasticsearch_settings is not None:
            self._values["elasticsearch_settings"] = elasticsearch_settings
        if endpoint_identifier is not None:
            self._values["endpoint_identifier"] = endpoint_identifier
        if extra_connection_attributes is not None:
            self._values["extra_connection_attributes"] = extra_connection_attributes
        if kafka_settings is not None:
            self._values["kafka_settings"] = kafka_settings
        if kinesis_settings is not None:
            self._values["kinesis_settings"] = kinesis_settings
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if mongo_db_settings is not None:
            self._values["mongo_db_settings"] = mongo_db_settings
        if neptune_settings is not None:
            self._values["neptune_settings"] = neptune_settings
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if s3_settings is not None:
            self._values["s3_settings"] = s3_settings
        if server_name is not None:
            self._values["server_name"] = server_name
        if ssl_mode is not None:
            self._values["ssl_mode"] = ssl_mode
        if tags is not None:
            self._values["tags"] = tags
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def endpoint_type(self) -> builtins.str:
        """``AWS::DMS::Endpoint.EndpointType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-endpointtype
        """
        result = self._values.get("endpoint_type")
        assert result is not None, "Required property 'endpoint_type' is missing"
        return result

    @builtins.property
    def engine_name(self) -> builtins.str:
        """``AWS::DMS::Endpoint.EngineName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-enginename
        """
        result = self._values.get("engine_name")
        assert result is not None, "Required property 'engine_name' is missing"
        return result

    @builtins.property
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.CertificateArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-certificatearn
        """
        result = self._values.get("certificate_arn")
        return result

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.DatabaseName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-databasename
        """
        result = self._values.get("database_name")
        return result

    @builtins.property
    def dynamo_db_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.DynamoDbSettingsProperty]]:
        """``AWS::DMS::Endpoint.DynamoDbSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-dynamodbsettings
        """
        result = self._values.get("dynamo_db_settings")
        return result

    @builtins.property
    def elasticsearch_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.ElasticsearchSettingsProperty]]:
        """``AWS::DMS::Endpoint.ElasticsearchSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-elasticsearchsettings
        """
        result = self._values.get("elasticsearch_settings")
        return result

    @builtins.property
    def endpoint_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.EndpointIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-endpointidentifier
        """
        result = self._values.get("endpoint_identifier")
        return result

    @builtins.property
    def extra_connection_attributes(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.ExtraConnectionAttributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-extraconnectionattributes
        """
        result = self._values.get("extra_connection_attributes")
        return result

    @builtins.property
    def kafka_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.KafkaSettingsProperty]]:
        """``AWS::DMS::Endpoint.KafkaSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-kafkasettings
        """
        result = self._values.get("kafka_settings")
        return result

    @builtins.property
    def kinesis_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.KinesisSettingsProperty]]:
        """``AWS::DMS::Endpoint.KinesisSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-kinesissettings
        """
        result = self._values.get("kinesis_settings")
        return result

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-kmskeyid
        """
        result = self._values.get("kms_key_id")
        return result

    @builtins.property
    def mongo_db_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.MongoDbSettingsProperty]]:
        """``AWS::DMS::Endpoint.MongoDbSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-mongodbsettings
        """
        result = self._values.get("mongo_db_settings")
        return result

    @builtins.property
    def neptune_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.NeptuneSettingsProperty]]:
        """``AWS::DMS::Endpoint.NeptuneSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-neptunesettings
        """
        result = self._values.get("neptune_settings")
        return result

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.Password``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-password
        """
        result = self._values.get("password")
        return result

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::DMS::Endpoint.Port``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-port
        """
        result = self._values.get("port")
        return result

    @builtins.property
    def s3_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnEndpoint.S3SettingsProperty]]:
        """``AWS::DMS::Endpoint.S3Settings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-s3settings
        """
        result = self._values.get("s3_settings")
        return result

    @builtins.property
    def server_name(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.ServerName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-servername
        """
        result = self._values.get("server_name")
        return result

    @builtins.property
    def ssl_mode(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.SslMode``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-sslmode
        """
        result = self._values.get("ssl_mode")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::DMS::Endpoint.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::Endpoint.Username``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-endpoint.html#cfn-dms-endpoint-username
        """
        result = self._values.get("username")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEventSubscription(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-dms.CfnEventSubscription",
):
    """A CloudFormation ``AWS::DMS::EventSubscription``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html
    :cloudformationResource: AWS::DMS::EventSubscription
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        sns_topic_arn: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        event_categories: typing.Optional[typing.List[builtins.str]] = None,
        source_ids: typing.Optional[typing.List[builtins.str]] = None,
        source_type: typing.Optional[builtins.str] = None,
        subscription_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::DMS::EventSubscription``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param sns_topic_arn: ``AWS::DMS::EventSubscription.SnsTopicArn``.
        :param enabled: ``AWS::DMS::EventSubscription.Enabled``.
        :param event_categories: ``AWS::DMS::EventSubscription.EventCategories``.
        :param source_ids: ``AWS::DMS::EventSubscription.SourceIds``.
        :param source_type: ``AWS::DMS::EventSubscription.SourceType``.
        :param subscription_name: ``AWS::DMS::EventSubscription.SubscriptionName``.
        :param tags: ``AWS::DMS::EventSubscription.Tags``.
        """
        props = CfnEventSubscriptionProps(
            sns_topic_arn=sns_topic_arn,
            enabled=enabled,
            event_categories=event_categories,
            source_ids=source_ids,
            source_type=source_type,
            subscription_name=subscription_name,
            tags=tags,
        )

        jsii.create(CfnEventSubscription, self, [scope, id, props])

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
        """``AWS::DMS::EventSubscription.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="snsTopicArn")
    def sns_topic_arn(self) -> builtins.str:
        """``AWS::DMS::EventSubscription.SnsTopicArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-snstopicarn
        """
        return jsii.get(self, "snsTopicArn")

    @sns_topic_arn.setter # type: ignore
    def sns_topic_arn(self, value: builtins.str) -> None:
        jsii.set(self, "snsTopicArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::DMS::EventSubscription.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventCategories")
    def event_categories(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::DMS::EventSubscription.EventCategories``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-eventcategories
        """
        return jsii.get(self, "eventCategories")

    @event_categories.setter # type: ignore
    def event_categories(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "eventCategories", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceIds")
    def source_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::DMS::EventSubscription.SourceIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-sourceids
        """
        return jsii.get(self, "sourceIds")

    @source_ids.setter # type: ignore
    def source_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "sourceIds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::EventSubscription.SourceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-sourcetype
        """
        return jsii.get(self, "sourceType")

    @source_type.setter # type: ignore
    def source_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sourceType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subscriptionName")
    def subscription_name(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::EventSubscription.SubscriptionName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-subscriptionname
        """
        return jsii.get(self, "subscriptionName")

    @subscription_name.setter # type: ignore
    def subscription_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "subscriptionName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dms.CfnEventSubscriptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "sns_topic_arn": "snsTopicArn",
        "enabled": "enabled",
        "event_categories": "eventCategories",
        "source_ids": "sourceIds",
        "source_type": "sourceType",
        "subscription_name": "subscriptionName",
        "tags": "tags",
    },
)
class CfnEventSubscriptionProps:
    def __init__(
        self,
        *,
        sns_topic_arn: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        event_categories: typing.Optional[typing.List[builtins.str]] = None,
        source_ids: typing.Optional[typing.List[builtins.str]] = None,
        source_type: typing.Optional[builtins.str] = None,
        subscription_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::DMS::EventSubscription``.

        :param sns_topic_arn: ``AWS::DMS::EventSubscription.SnsTopicArn``.
        :param enabled: ``AWS::DMS::EventSubscription.Enabled``.
        :param event_categories: ``AWS::DMS::EventSubscription.EventCategories``.
        :param source_ids: ``AWS::DMS::EventSubscription.SourceIds``.
        :param source_type: ``AWS::DMS::EventSubscription.SourceType``.
        :param subscription_name: ``AWS::DMS::EventSubscription.SubscriptionName``.
        :param tags: ``AWS::DMS::EventSubscription.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "sns_topic_arn": sns_topic_arn,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_categories is not None:
            self._values["event_categories"] = event_categories
        if source_ids is not None:
            self._values["source_ids"] = source_ids
        if source_type is not None:
            self._values["source_type"] = source_type
        if subscription_name is not None:
            self._values["subscription_name"] = subscription_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def sns_topic_arn(self) -> builtins.str:
        """``AWS::DMS::EventSubscription.SnsTopicArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-snstopicarn
        """
        result = self._values.get("sns_topic_arn")
        assert result is not None, "Required property 'sns_topic_arn' is missing"
        return result

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::DMS::EventSubscription.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-enabled
        """
        result = self._values.get("enabled")
        return result

    @builtins.property
    def event_categories(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::DMS::EventSubscription.EventCategories``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-eventcategories
        """
        result = self._values.get("event_categories")
        return result

    @builtins.property
    def source_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::DMS::EventSubscription.SourceIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-sourceids
        """
        result = self._values.get("source_ids")
        return result

    @builtins.property
    def source_type(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::EventSubscription.SourceType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-sourcetype
        """
        result = self._values.get("source_type")
        return result

    @builtins.property
    def subscription_name(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::EventSubscription.SubscriptionName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-subscriptionname
        """
        result = self._values.get("subscription_name")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::DMS::EventSubscription.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-eventsubscription.html#cfn-dms-eventsubscription-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnReplicationInstance(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-dms.CfnReplicationInstance",
):
    """A CloudFormation ``AWS::DMS::ReplicationInstance``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html
    :cloudformationResource: AWS::DMS::ReplicationInstance
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        replication_instance_class: builtins.str,
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        multi_az: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        replication_instance_identifier: typing.Optional[builtins.str] = None,
        replication_subnet_group_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Create a new ``AWS::DMS::ReplicationInstance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param replication_instance_class: ``AWS::DMS::ReplicationInstance.ReplicationInstanceClass``.
        :param allocated_storage: ``AWS::DMS::ReplicationInstance.AllocatedStorage``.
        :param allow_major_version_upgrade: ``AWS::DMS::ReplicationInstance.AllowMajorVersionUpgrade``.
        :param auto_minor_version_upgrade: ``AWS::DMS::ReplicationInstance.AutoMinorVersionUpgrade``.
        :param availability_zone: ``AWS::DMS::ReplicationInstance.AvailabilityZone``.
        :param engine_version: ``AWS::DMS::ReplicationInstance.EngineVersion``.
        :param kms_key_id: ``AWS::DMS::ReplicationInstance.KmsKeyId``.
        :param multi_az: ``AWS::DMS::ReplicationInstance.MultiAZ``.
        :param preferred_maintenance_window: ``AWS::DMS::ReplicationInstance.PreferredMaintenanceWindow``.
        :param publicly_accessible: ``AWS::DMS::ReplicationInstance.PubliclyAccessible``.
        :param replication_instance_identifier: ``AWS::DMS::ReplicationInstance.ReplicationInstanceIdentifier``.
        :param replication_subnet_group_identifier: ``AWS::DMS::ReplicationInstance.ReplicationSubnetGroupIdentifier``.
        :param tags: ``AWS::DMS::ReplicationInstance.Tags``.
        :param vpc_security_group_ids: ``AWS::DMS::ReplicationInstance.VpcSecurityGroupIds``.
        """
        props = CfnReplicationInstanceProps(
            replication_instance_class=replication_instance_class,
            allocated_storage=allocated_storage,
            allow_major_version_upgrade=allow_major_version_upgrade,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            engine_version=engine_version,
            kms_key_id=kms_key_id,
            multi_az=multi_az,
            preferred_maintenance_window=preferred_maintenance_window,
            publicly_accessible=publicly_accessible,
            replication_instance_identifier=replication_instance_identifier,
            replication_subnet_group_identifier=replication_subnet_group_identifier,
            tags=tags,
            vpc_security_group_ids=vpc_security_group_ids,
        )

        jsii.create(CfnReplicationInstance, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrReplicationInstancePrivateIpAddresses")
    def attr_replication_instance_private_ip_addresses(
        self,
    ) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: ReplicationInstancePrivateIpAddresses
        """
        return jsii.get(self, "attrReplicationInstancePrivateIpAddresses")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrReplicationInstancePublicIpAddresses")
    def attr_replication_instance_public_ip_addresses(
        self,
    ) -> typing.List[builtins.str]:
        """
        :cloudformationAttribute: ReplicationInstancePublicIpAddresses
        """
        return jsii.get(self, "attrReplicationInstancePublicIpAddresses")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::DMS::ReplicationInstance.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="replicationInstanceClass")
    def replication_instance_class(self) -> builtins.str:
        """``AWS::DMS::ReplicationInstance.ReplicationInstanceClass``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-replicationinstanceclass
        """
        return jsii.get(self, "replicationInstanceClass")

    @replication_instance_class.setter # type: ignore
    def replication_instance_class(self, value: builtins.str) -> None:
        jsii.set(self, "replicationInstanceClass", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allocatedStorage")
    def allocated_storage(self) -> typing.Optional[jsii.Number]:
        """``AWS::DMS::ReplicationInstance.AllocatedStorage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-allocatedstorage
        """
        return jsii.get(self, "allocatedStorage")

    @allocated_storage.setter # type: ignore
    def allocated_storage(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "allocatedStorage", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowMajorVersionUpgrade")
    def allow_major_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::DMS::ReplicationInstance.AllowMajorVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-allowmajorversionupgrade
        """
        return jsii.get(self, "allowMajorVersionUpgrade")

    @allow_major_version_upgrade.setter # type: ignore
    def allow_major_version_upgrade(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "allowMajorVersionUpgrade", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::DMS::ReplicationInstance.AutoMinorVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-autominorversionupgrade
        """
        return jsii.get(self, "autoMinorVersionUpgrade")

    @auto_minor_version_upgrade.setter # type: ignore
    def auto_minor_version_upgrade(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.AvailabilityZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-availabilityzone
        """
        return jsii.get(self, "availabilityZone")

    @availability_zone.setter # type: ignore
    def availability_zone(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "availabilityZone", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.EngineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-engineversion
        """
        return jsii.get(self, "engineVersion")

    @engine_version.setter # type: ignore
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "engineVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter # type: ignore
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="multiAz")
    def multi_az(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::DMS::ReplicationInstance.MultiAZ``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-multiaz
        """
        return jsii.get(self, "multiAz")

    @multi_az.setter # type: ignore
    def multi_az(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "multiAz", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.PreferredMaintenanceWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter # type: ignore
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="publiclyAccessible")
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::DMS::ReplicationInstance.PubliclyAccessible``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-publiclyaccessible
        """
        return jsii.get(self, "publiclyAccessible")

    @publicly_accessible.setter # type: ignore
    def publicly_accessible(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "publiclyAccessible", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="replicationInstanceIdentifier")
    def replication_instance_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.ReplicationInstanceIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-replicationinstanceidentifier
        """
        return jsii.get(self, "replicationInstanceIdentifier")

    @replication_instance_identifier.setter # type: ignore
    def replication_instance_identifier(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "replicationInstanceIdentifier", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="replicationSubnetGroupIdentifier")
    def replication_subnet_group_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.ReplicationSubnetGroupIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-replicationsubnetgroupidentifier
        """
        return jsii.get(self, "replicationSubnetGroupIdentifier")

    @replication_subnet_group_identifier.setter # type: ignore
    def replication_subnet_group_identifier(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "replicationSubnetGroupIdentifier", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::DMS::ReplicationInstance.VpcSecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-vpcsecuritygroupids
        """
        return jsii.get(self, "vpcSecurityGroupIds")

    @vpc_security_group_ids.setter # type: ignore
    def vpc_security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "vpcSecurityGroupIds", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dms.CfnReplicationInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "replication_instance_class": "replicationInstanceClass",
        "allocated_storage": "allocatedStorage",
        "allow_major_version_upgrade": "allowMajorVersionUpgrade",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "engine_version": "engineVersion",
        "kms_key_id": "kmsKeyId",
        "multi_az": "multiAz",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "publicly_accessible": "publiclyAccessible",
        "replication_instance_identifier": "replicationInstanceIdentifier",
        "replication_subnet_group_identifier": "replicationSubnetGroupIdentifier",
        "tags": "tags",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnReplicationInstanceProps:
    def __init__(
        self,
        *,
        replication_instance_class: builtins.str,
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        multi_az: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        replication_instance_identifier: typing.Optional[builtins.str] = None,
        replication_subnet_group_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::DMS::ReplicationInstance``.

        :param replication_instance_class: ``AWS::DMS::ReplicationInstance.ReplicationInstanceClass``.
        :param allocated_storage: ``AWS::DMS::ReplicationInstance.AllocatedStorage``.
        :param allow_major_version_upgrade: ``AWS::DMS::ReplicationInstance.AllowMajorVersionUpgrade``.
        :param auto_minor_version_upgrade: ``AWS::DMS::ReplicationInstance.AutoMinorVersionUpgrade``.
        :param availability_zone: ``AWS::DMS::ReplicationInstance.AvailabilityZone``.
        :param engine_version: ``AWS::DMS::ReplicationInstance.EngineVersion``.
        :param kms_key_id: ``AWS::DMS::ReplicationInstance.KmsKeyId``.
        :param multi_az: ``AWS::DMS::ReplicationInstance.MultiAZ``.
        :param preferred_maintenance_window: ``AWS::DMS::ReplicationInstance.PreferredMaintenanceWindow``.
        :param publicly_accessible: ``AWS::DMS::ReplicationInstance.PubliclyAccessible``.
        :param replication_instance_identifier: ``AWS::DMS::ReplicationInstance.ReplicationInstanceIdentifier``.
        :param replication_subnet_group_identifier: ``AWS::DMS::ReplicationInstance.ReplicationSubnetGroupIdentifier``.
        :param tags: ``AWS::DMS::ReplicationInstance.Tags``.
        :param vpc_security_group_ids: ``AWS::DMS::ReplicationInstance.VpcSecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "replication_instance_class": replication_instance_class,
        }
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if allow_major_version_upgrade is not None:
            self._values["allow_major_version_upgrade"] = allow_major_version_upgrade
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if replication_instance_identifier is not None:
            self._values["replication_instance_identifier"] = replication_instance_identifier
        if replication_subnet_group_identifier is not None:
            self._values["replication_subnet_group_identifier"] = replication_subnet_group_identifier
        if tags is not None:
            self._values["tags"] = tags
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def replication_instance_class(self) -> builtins.str:
        """``AWS::DMS::ReplicationInstance.ReplicationInstanceClass``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-replicationinstanceclass
        """
        result = self._values.get("replication_instance_class")
        assert result is not None, "Required property 'replication_instance_class' is missing"
        return result

    @builtins.property
    def allocated_storage(self) -> typing.Optional[jsii.Number]:
        """``AWS::DMS::ReplicationInstance.AllocatedStorage``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-allocatedstorage
        """
        result = self._values.get("allocated_storage")
        return result

    @builtins.property
    def allow_major_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::DMS::ReplicationInstance.AllowMajorVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-allowmajorversionupgrade
        """
        result = self._values.get("allow_major_version_upgrade")
        return result

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::DMS::ReplicationInstance.AutoMinorVersionUpgrade``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-autominorversionupgrade
        """
        result = self._values.get("auto_minor_version_upgrade")
        return result

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.AvailabilityZone``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-availabilityzone
        """
        result = self._values.get("availability_zone")
        return result

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.EngineVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-engineversion
        """
        result = self._values.get("engine_version")
        return result

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.KmsKeyId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-kmskeyid
        """
        result = self._values.get("kms_key_id")
        return result

    @builtins.property
    def multi_az(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::DMS::ReplicationInstance.MultiAZ``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-multiaz
        """
        result = self._values.get("multi_az")
        return result

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.PreferredMaintenanceWindow``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-preferredmaintenancewindow
        """
        result = self._values.get("preferred_maintenance_window")
        return result

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::DMS::ReplicationInstance.PubliclyAccessible``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-publiclyaccessible
        """
        result = self._values.get("publicly_accessible")
        return result

    @builtins.property
    def replication_instance_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.ReplicationInstanceIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-replicationinstanceidentifier
        """
        result = self._values.get("replication_instance_identifier")
        return result

    @builtins.property
    def replication_subnet_group_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationInstance.ReplicationSubnetGroupIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-replicationsubnetgroupidentifier
        """
        result = self._values.get("replication_subnet_group_identifier")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::DMS::ReplicationInstance.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::DMS::ReplicationInstance.VpcSecurityGroupIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationinstance.html#cfn-dms-replicationinstance-vpcsecuritygroupids
        """
        result = self._values.get("vpc_security_group_ids")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnReplicationSubnetGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-dms.CfnReplicationSubnetGroup",
):
    """A CloudFormation ``AWS::DMS::ReplicationSubnetGroup``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html
    :cloudformationResource: AWS::DMS::ReplicationSubnetGroup
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        replication_subnet_group_description: builtins.str,
        subnet_ids: typing.List[builtins.str],
        replication_subnet_group_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::DMS::ReplicationSubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param replication_subnet_group_description: ``AWS::DMS::ReplicationSubnetGroup.ReplicationSubnetGroupDescription``.
        :param subnet_ids: ``AWS::DMS::ReplicationSubnetGroup.SubnetIds``.
        :param replication_subnet_group_identifier: ``AWS::DMS::ReplicationSubnetGroup.ReplicationSubnetGroupIdentifier``.
        :param tags: ``AWS::DMS::ReplicationSubnetGroup.Tags``.
        """
        props = CfnReplicationSubnetGroupProps(
            replication_subnet_group_description=replication_subnet_group_description,
            subnet_ids=subnet_ids,
            replication_subnet_group_identifier=replication_subnet_group_identifier,
            tags=tags,
        )

        jsii.create(CfnReplicationSubnetGroup, self, [scope, id, props])

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
        """``AWS::DMS::ReplicationSubnetGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="replicationSubnetGroupDescription")
    def replication_subnet_group_description(self) -> builtins.str:
        """``AWS::DMS::ReplicationSubnetGroup.ReplicationSubnetGroupDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-replicationsubnetgroupdescription
        """
        return jsii.get(self, "replicationSubnetGroupDescription")

    @replication_subnet_group_description.setter # type: ignore
    def replication_subnet_group_description(self, value: builtins.str) -> None:
        jsii.set(self, "replicationSubnetGroupDescription", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        """``AWS::DMS::ReplicationSubnetGroup.SubnetIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter # type: ignore
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "subnetIds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="replicationSubnetGroupIdentifier")
    def replication_subnet_group_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationSubnetGroup.ReplicationSubnetGroupIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-replicationsubnetgroupidentifier
        """
        return jsii.get(self, "replicationSubnetGroupIdentifier")

    @replication_subnet_group_identifier.setter # type: ignore
    def replication_subnet_group_identifier(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "replicationSubnetGroupIdentifier", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dms.CfnReplicationSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "replication_subnet_group_description": "replicationSubnetGroupDescription",
        "subnet_ids": "subnetIds",
        "replication_subnet_group_identifier": "replicationSubnetGroupIdentifier",
        "tags": "tags",
    },
)
class CfnReplicationSubnetGroupProps:
    def __init__(
        self,
        *,
        replication_subnet_group_description: builtins.str,
        subnet_ids: typing.List[builtins.str],
        replication_subnet_group_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::DMS::ReplicationSubnetGroup``.

        :param replication_subnet_group_description: ``AWS::DMS::ReplicationSubnetGroup.ReplicationSubnetGroupDescription``.
        :param subnet_ids: ``AWS::DMS::ReplicationSubnetGroup.SubnetIds``.
        :param replication_subnet_group_identifier: ``AWS::DMS::ReplicationSubnetGroup.ReplicationSubnetGroupIdentifier``.
        :param tags: ``AWS::DMS::ReplicationSubnetGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "replication_subnet_group_description": replication_subnet_group_description,
            "subnet_ids": subnet_ids,
        }
        if replication_subnet_group_identifier is not None:
            self._values["replication_subnet_group_identifier"] = replication_subnet_group_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def replication_subnet_group_description(self) -> builtins.str:
        """``AWS::DMS::ReplicationSubnetGroup.ReplicationSubnetGroupDescription``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-replicationsubnetgroupdescription
        """
        result = self._values.get("replication_subnet_group_description")
        assert result is not None, "Required property 'replication_subnet_group_description' is missing"
        return result

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        """``AWS::DMS::ReplicationSubnetGroup.SubnetIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-subnetids
        """
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return result

    @builtins.property
    def replication_subnet_group_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationSubnetGroup.ReplicationSubnetGroupIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-replicationsubnetgroupidentifier
        """
        result = self._values.get("replication_subnet_group_identifier")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::DMS::ReplicationSubnetGroup.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationsubnetgroup.html#cfn-dms-replicationsubnetgroup-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnReplicationTask(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-dms.CfnReplicationTask",
):
    """A CloudFormation ``AWS::DMS::ReplicationTask``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html
    :cloudformationResource: AWS::DMS::ReplicationTask
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        migration_type: builtins.str,
        replication_instance_arn: builtins.str,
        source_endpoint_arn: builtins.str,
        table_mappings: builtins.str,
        target_endpoint_arn: builtins.str,
        cdc_start_position: typing.Optional[builtins.str] = None,
        cdc_start_time: typing.Optional[jsii.Number] = None,
        cdc_stop_position: typing.Optional[builtins.str] = None,
        replication_task_identifier: typing.Optional[builtins.str] = None,
        replication_task_settings: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        task_data: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::DMS::ReplicationTask``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param migration_type: ``AWS::DMS::ReplicationTask.MigrationType``.
        :param replication_instance_arn: ``AWS::DMS::ReplicationTask.ReplicationInstanceArn``.
        :param source_endpoint_arn: ``AWS::DMS::ReplicationTask.SourceEndpointArn``.
        :param table_mappings: ``AWS::DMS::ReplicationTask.TableMappings``.
        :param target_endpoint_arn: ``AWS::DMS::ReplicationTask.TargetEndpointArn``.
        :param cdc_start_position: ``AWS::DMS::ReplicationTask.CdcStartPosition``.
        :param cdc_start_time: ``AWS::DMS::ReplicationTask.CdcStartTime``.
        :param cdc_stop_position: ``AWS::DMS::ReplicationTask.CdcStopPosition``.
        :param replication_task_identifier: ``AWS::DMS::ReplicationTask.ReplicationTaskIdentifier``.
        :param replication_task_settings: ``AWS::DMS::ReplicationTask.ReplicationTaskSettings``.
        :param tags: ``AWS::DMS::ReplicationTask.Tags``.
        :param task_data: ``AWS::DMS::ReplicationTask.TaskData``.
        """
        props = CfnReplicationTaskProps(
            migration_type=migration_type,
            replication_instance_arn=replication_instance_arn,
            source_endpoint_arn=source_endpoint_arn,
            table_mappings=table_mappings,
            target_endpoint_arn=target_endpoint_arn,
            cdc_start_position=cdc_start_position,
            cdc_start_time=cdc_start_time,
            cdc_stop_position=cdc_stop_position,
            replication_task_identifier=replication_task_identifier,
            replication_task_settings=replication_task_settings,
            tags=tags,
            task_data=task_data,
        )

        jsii.create(CfnReplicationTask, self, [scope, id, props])

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
        """``AWS::DMS::ReplicationTask.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="migrationType")
    def migration_type(self) -> builtins.str:
        """``AWS::DMS::ReplicationTask.MigrationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-migrationtype
        """
        return jsii.get(self, "migrationType")

    @migration_type.setter # type: ignore
    def migration_type(self, value: builtins.str) -> None:
        jsii.set(self, "migrationType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="replicationInstanceArn")
    def replication_instance_arn(self) -> builtins.str:
        """``AWS::DMS::ReplicationTask.ReplicationInstanceArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-replicationinstancearn
        """
        return jsii.get(self, "replicationInstanceArn")

    @replication_instance_arn.setter # type: ignore
    def replication_instance_arn(self, value: builtins.str) -> None:
        jsii.set(self, "replicationInstanceArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceEndpointArn")
    def source_endpoint_arn(self) -> builtins.str:
        """``AWS::DMS::ReplicationTask.SourceEndpointArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-sourceendpointarn
        """
        return jsii.get(self, "sourceEndpointArn")

    @source_endpoint_arn.setter # type: ignore
    def source_endpoint_arn(self, value: builtins.str) -> None:
        jsii.set(self, "sourceEndpointArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tableMappings")
    def table_mappings(self) -> builtins.str:
        """``AWS::DMS::ReplicationTask.TableMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-tablemappings
        """
        return jsii.get(self, "tableMappings")

    @table_mappings.setter # type: ignore
    def table_mappings(self, value: builtins.str) -> None:
        jsii.set(self, "tableMappings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targetEndpointArn")
    def target_endpoint_arn(self) -> builtins.str:
        """``AWS::DMS::ReplicationTask.TargetEndpointArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-targetendpointarn
        """
        return jsii.get(self, "targetEndpointArn")

    @target_endpoint_arn.setter # type: ignore
    def target_endpoint_arn(self, value: builtins.str) -> None:
        jsii.set(self, "targetEndpointArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cdcStartPosition")
    def cdc_start_position(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationTask.CdcStartPosition``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-cdcstartposition
        """
        return jsii.get(self, "cdcStartPosition")

    @cdc_start_position.setter # type: ignore
    def cdc_start_position(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cdcStartPosition", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cdcStartTime")
    def cdc_start_time(self) -> typing.Optional[jsii.Number]:
        """``AWS::DMS::ReplicationTask.CdcStartTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-cdcstarttime
        """
        return jsii.get(self, "cdcStartTime")

    @cdc_start_time.setter # type: ignore
    def cdc_start_time(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "cdcStartTime", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cdcStopPosition")
    def cdc_stop_position(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationTask.CdcStopPosition``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-cdcstopposition
        """
        return jsii.get(self, "cdcStopPosition")

    @cdc_stop_position.setter # type: ignore
    def cdc_stop_position(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "cdcStopPosition", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="replicationTaskIdentifier")
    def replication_task_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationTask.ReplicationTaskIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-replicationtaskidentifier
        """
        return jsii.get(self, "replicationTaskIdentifier")

    @replication_task_identifier.setter # type: ignore
    def replication_task_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "replicationTaskIdentifier", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="replicationTaskSettings")
    def replication_task_settings(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationTask.ReplicationTaskSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-replicationtasksettings
        """
        return jsii.get(self, "replicationTaskSettings")

    @replication_task_settings.setter # type: ignore
    def replication_task_settings(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "replicationTaskSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskData")
    def task_data(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationTask.TaskData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-taskdata
        """
        return jsii.get(self, "taskData")

    @task_data.setter # type: ignore
    def task_data(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "taskData", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-dms.CfnReplicationTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "migration_type": "migrationType",
        "replication_instance_arn": "replicationInstanceArn",
        "source_endpoint_arn": "sourceEndpointArn",
        "table_mappings": "tableMappings",
        "target_endpoint_arn": "targetEndpointArn",
        "cdc_start_position": "cdcStartPosition",
        "cdc_start_time": "cdcStartTime",
        "cdc_stop_position": "cdcStopPosition",
        "replication_task_identifier": "replicationTaskIdentifier",
        "replication_task_settings": "replicationTaskSettings",
        "tags": "tags",
        "task_data": "taskData",
    },
)
class CfnReplicationTaskProps:
    def __init__(
        self,
        *,
        migration_type: builtins.str,
        replication_instance_arn: builtins.str,
        source_endpoint_arn: builtins.str,
        table_mappings: builtins.str,
        target_endpoint_arn: builtins.str,
        cdc_start_position: typing.Optional[builtins.str] = None,
        cdc_start_time: typing.Optional[jsii.Number] = None,
        cdc_stop_position: typing.Optional[builtins.str] = None,
        replication_task_identifier: typing.Optional[builtins.str] = None,
        replication_task_settings: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
        task_data: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::DMS::ReplicationTask``.

        :param migration_type: ``AWS::DMS::ReplicationTask.MigrationType``.
        :param replication_instance_arn: ``AWS::DMS::ReplicationTask.ReplicationInstanceArn``.
        :param source_endpoint_arn: ``AWS::DMS::ReplicationTask.SourceEndpointArn``.
        :param table_mappings: ``AWS::DMS::ReplicationTask.TableMappings``.
        :param target_endpoint_arn: ``AWS::DMS::ReplicationTask.TargetEndpointArn``.
        :param cdc_start_position: ``AWS::DMS::ReplicationTask.CdcStartPosition``.
        :param cdc_start_time: ``AWS::DMS::ReplicationTask.CdcStartTime``.
        :param cdc_stop_position: ``AWS::DMS::ReplicationTask.CdcStopPosition``.
        :param replication_task_identifier: ``AWS::DMS::ReplicationTask.ReplicationTaskIdentifier``.
        :param replication_task_settings: ``AWS::DMS::ReplicationTask.ReplicationTaskSettings``.
        :param tags: ``AWS::DMS::ReplicationTask.Tags``.
        :param task_data: ``AWS::DMS::ReplicationTask.TaskData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "migration_type": migration_type,
            "replication_instance_arn": replication_instance_arn,
            "source_endpoint_arn": source_endpoint_arn,
            "table_mappings": table_mappings,
            "target_endpoint_arn": target_endpoint_arn,
        }
        if cdc_start_position is not None:
            self._values["cdc_start_position"] = cdc_start_position
        if cdc_start_time is not None:
            self._values["cdc_start_time"] = cdc_start_time
        if cdc_stop_position is not None:
            self._values["cdc_stop_position"] = cdc_stop_position
        if replication_task_identifier is not None:
            self._values["replication_task_identifier"] = replication_task_identifier
        if replication_task_settings is not None:
            self._values["replication_task_settings"] = replication_task_settings
        if tags is not None:
            self._values["tags"] = tags
        if task_data is not None:
            self._values["task_data"] = task_data

    @builtins.property
    def migration_type(self) -> builtins.str:
        """``AWS::DMS::ReplicationTask.MigrationType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-migrationtype
        """
        result = self._values.get("migration_type")
        assert result is not None, "Required property 'migration_type' is missing"
        return result

    @builtins.property
    def replication_instance_arn(self) -> builtins.str:
        """``AWS::DMS::ReplicationTask.ReplicationInstanceArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-replicationinstancearn
        """
        result = self._values.get("replication_instance_arn")
        assert result is not None, "Required property 'replication_instance_arn' is missing"
        return result

    @builtins.property
    def source_endpoint_arn(self) -> builtins.str:
        """``AWS::DMS::ReplicationTask.SourceEndpointArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-sourceendpointarn
        """
        result = self._values.get("source_endpoint_arn")
        assert result is not None, "Required property 'source_endpoint_arn' is missing"
        return result

    @builtins.property
    def table_mappings(self) -> builtins.str:
        """``AWS::DMS::ReplicationTask.TableMappings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-tablemappings
        """
        result = self._values.get("table_mappings")
        assert result is not None, "Required property 'table_mappings' is missing"
        return result

    @builtins.property
    def target_endpoint_arn(self) -> builtins.str:
        """``AWS::DMS::ReplicationTask.TargetEndpointArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-targetendpointarn
        """
        result = self._values.get("target_endpoint_arn")
        assert result is not None, "Required property 'target_endpoint_arn' is missing"
        return result

    @builtins.property
    def cdc_start_position(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationTask.CdcStartPosition``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-cdcstartposition
        """
        result = self._values.get("cdc_start_position")
        return result

    @builtins.property
    def cdc_start_time(self) -> typing.Optional[jsii.Number]:
        """``AWS::DMS::ReplicationTask.CdcStartTime``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-cdcstarttime
        """
        result = self._values.get("cdc_start_time")
        return result

    @builtins.property
    def cdc_stop_position(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationTask.CdcStopPosition``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-cdcstopposition
        """
        result = self._values.get("cdc_stop_position")
        return result

    @builtins.property
    def replication_task_identifier(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationTask.ReplicationTaskIdentifier``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-replicationtaskidentifier
        """
        result = self._values.get("replication_task_identifier")
        return result

    @builtins.property
    def replication_task_settings(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationTask.ReplicationTaskSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-replicationtasksettings
        """
        result = self._values.get("replication_task_settings")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::DMS::ReplicationTask.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def task_data(self) -> typing.Optional[builtins.str]:
        """``AWS::DMS::ReplicationTask.TaskData``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dms-replicationtask.html#cfn-dms-replicationtask-taskdata
        """
        result = self._values.get("task_data")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCertificate",
    "CfnCertificateProps",
    "CfnEndpoint",
    "CfnEndpointProps",
    "CfnEventSubscription",
    "CfnEventSubscriptionProps",
    "CfnReplicationInstance",
    "CfnReplicationInstanceProps",
    "CfnReplicationSubnetGroup",
    "CfnReplicationSubnetGroupProps",
    "CfnReplicationTask",
    "CfnReplicationTaskProps",
]

publication.publish()
