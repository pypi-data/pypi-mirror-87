"""
## AWS::ACMPCA Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_acmpca as acmpca
```
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
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificate",
):
    """A CloudFormation ``AWS::ACMPCA::Certificate``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html
    :cloudformationResource: AWS::ACMPCA::Certificate
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        certificate_authority_arn: builtins.str,
        certificate_signing_request: builtins.str,
        signing_algorithm: builtins.str,
        validity: typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ValidityProperty"],
        template_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ACMPCA::Certificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate_authority_arn: ``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.
        :param certificate_signing_request: ``AWS::ACMPCA::Certificate.CertificateSigningRequest``.
        :param signing_algorithm: ``AWS::ACMPCA::Certificate.SigningAlgorithm``.
        :param validity: ``AWS::ACMPCA::Certificate.Validity``.
        :param template_arn: ``AWS::ACMPCA::Certificate.TemplateArn``.
        """
        props = CfnCertificateProps(
            certificate_authority_arn=certificate_authority_arn,
            certificate_signing_request=certificate_signing_request,
            signing_algorithm=signing_algorithm,
            validity=validity,
            template_arn=template_arn,
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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrCertificate")
    def attr_certificate(self) -> builtins.str:
        """
        :cloudformationAttribute: Certificate
        """
        return jsii.get(self, "attrCertificate")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificateauthorityarn
        """
        return jsii.get(self, "certificateAuthorityArn")

    @certificate_authority_arn.setter # type: ignore
    def certificate_authority_arn(self, value: builtins.str) -> None:
        jsii.set(self, "certificateAuthorityArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateSigningRequest")
    def certificate_signing_request(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.CertificateSigningRequest``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificatesigningrequest
        """
        return jsii.get(self, "certificateSigningRequest")

    @certificate_signing_request.setter # type: ignore
    def certificate_signing_request(self, value: builtins.str) -> None:
        jsii.set(self, "certificateSigningRequest", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="signingAlgorithm")
    def signing_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.SigningAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-signingalgorithm
        """
        return jsii.get(self, "signingAlgorithm")

    @signing_algorithm.setter # type: ignore
    def signing_algorithm(self, value: builtins.str) -> None:
        jsii.set(self, "signingAlgorithm", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="validity")
    def validity(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ValidityProperty"]:
        """``AWS::ACMPCA::Certificate.Validity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validity
        """
        return jsii.get(self, "validity")

    @validity.setter # type: ignore
    def validity(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnCertificate.ValidityProperty"],
    ) -> None:
        jsii.set(self, "validity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="templateArn")
    def template_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::Certificate.TemplateArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-templatearn
        """
        return jsii.get(self, "templateArn")

    @template_arn.setter # type: ignore
    def template_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "templateArn", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificate.ValidityProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class ValidityProperty:
        def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
            """
            :param type: ``CfnCertificate.ValidityProperty.Type``.
            :param value: ``CfnCertificate.ValidityProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
                "value": value,
            }

        @builtins.property
        def type(self) -> builtins.str:
            """``CfnCertificate.ValidityProperty.Type``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html#cfn-acmpca-certificate-validity-type
            """
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return result

        @builtins.property
        def value(self) -> jsii.Number:
            """``CfnCertificate.ValidityProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html#cfn-acmpca-certificate-validity-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCertificateAuthority(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority",
):
    """A CloudFormation ``AWS::ACMPCA::CertificateAuthority``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html
    :cloudformationResource: AWS::ACMPCA::CertificateAuthority
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        key_algorithm: builtins.str,
        signing_algorithm: builtins.str,
        subject: typing.Union["CfnCertificateAuthority.SubjectProperty", aws_cdk.core.IResolvable],
        type: builtins.str,
        revocation_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.RevocationConfigurationProperty"]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::ACMPCA::CertificateAuthority``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param key_algorithm: ``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.
        :param signing_algorithm: ``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.
        :param subject: ``AWS::ACMPCA::CertificateAuthority.Subject``.
        :param type: ``AWS::ACMPCA::CertificateAuthority.Type``.
        :param revocation_configuration: ``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.
        :param tags: ``AWS::ACMPCA::CertificateAuthority.Tags``.
        """
        props = CfnCertificateAuthorityProps(
            key_algorithm=key_algorithm,
            signing_algorithm=signing_algorithm,
            subject=subject,
            type=type,
            revocation_configuration=revocation_configuration,
            tags=tags,
        )

        jsii.create(CfnCertificateAuthority, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrCertificateSigningRequest")
    def attr_certificate_signing_request(self) -> builtins.str:
        """
        :cloudformationAttribute: CertificateSigningRequest
        """
        return jsii.get(self, "attrCertificateSigningRequest")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ACMPCA::CertificateAuthority.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="keyAlgorithm")
    def key_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keyalgorithm
        """
        return jsii.get(self, "keyAlgorithm")

    @key_algorithm.setter # type: ignore
    def key_algorithm(self, value: builtins.str) -> None:
        jsii.set(self, "keyAlgorithm", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="signingAlgorithm")
    def signing_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-signingalgorithm
        """
        return jsii.get(self, "signingAlgorithm")

    @signing_algorithm.setter # type: ignore
    def signing_algorithm(self, value: builtins.str) -> None:
        jsii.set(self, "signingAlgorithm", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="subject")
    def subject(
        self,
    ) -> typing.Union["CfnCertificateAuthority.SubjectProperty", aws_cdk.core.IResolvable]:
        """``AWS::ACMPCA::CertificateAuthority.Subject``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-subject
        """
        return jsii.get(self, "subject")

    @subject.setter # type: ignore
    def subject(
        self,
        value: typing.Union["CfnCertificateAuthority.SubjectProperty", aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "subject", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-type
        """
        return jsii.get(self, "type")

    @type.setter # type: ignore
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="revocationConfiguration")
    def revocation_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.RevocationConfigurationProperty"]]:
        """``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-revocationconfiguration
        """
        return jsii.get(self, "revocationConfiguration")

    @revocation_configuration.setter # type: ignore
    def revocation_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.RevocationConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "revocationConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.CrlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_cname": "customCname",
            "enabled": "enabled",
            "expiration_in_days": "expirationInDays",
            "s3_bucket_name": "s3BucketName",
        },
    )
    class CrlConfigurationProperty:
        def __init__(
            self,
            *,
            custom_cname: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            expiration_in_days: typing.Optional[jsii.Number] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param custom_cname: ``CfnCertificateAuthority.CrlConfigurationProperty.CustomCname``.
            :param enabled: ``CfnCertificateAuthority.CrlConfigurationProperty.Enabled``.
            :param expiration_in_days: ``CfnCertificateAuthority.CrlConfigurationProperty.ExpirationInDays``.
            :param s3_bucket_name: ``CfnCertificateAuthority.CrlConfigurationProperty.S3BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if custom_cname is not None:
                self._values["custom_cname"] = custom_cname
            if enabled is not None:
                self._values["enabled"] = enabled
            if expiration_in_days is not None:
                self._values["expiration_in_days"] = expiration_in_days
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name

        @builtins.property
        def custom_cname(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.CustomCname``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-customcname
            """
            result = self._values.get("custom_cname")
            return result

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.Enabled``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-enabled
            """
            result = self._values.get("enabled")
            return result

        @builtins.property
        def expiration_in_days(self) -> typing.Optional[jsii.Number]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.ExpirationInDays``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-expirationindays
            """
            result = self._values.get("expiration_in_days")
            return result

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.CrlConfigurationProperty.S3BucketName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-s3bucketname
            """
            result = self._values.get("s3_bucket_name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.RevocationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"crl_configuration": "crlConfiguration"},
    )
    class RevocationConfigurationProperty:
        def __init__(
            self,
            *,
            crl_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.CrlConfigurationProperty"]] = None,
        ) -> None:
            """
            :param crl_configuration: ``CfnCertificateAuthority.RevocationConfigurationProperty.CrlConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if crl_configuration is not None:
                self._values["crl_configuration"] = crl_configuration

        @builtins.property
        def crl_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCertificateAuthority.CrlConfigurationProperty"]]:
            """``CfnCertificateAuthority.RevocationConfigurationProperty.CrlConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html#cfn-acmpca-certificateauthority-revocationconfiguration-crlconfiguration
            """
            result = self._values.get("crl_configuration")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RevocationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthority.SubjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "common_name": "commonName",
            "country": "country",
            "distinguished_name_qualifier": "distinguishedNameQualifier",
            "generation_qualifier": "generationQualifier",
            "given_name": "givenName",
            "initials": "initials",
            "locality": "locality",
            "organization": "organization",
            "organizational_unit": "organizationalUnit",
            "pseudonym": "pseudonym",
            "serial_number": "serialNumber",
            "state": "state",
            "surname": "surname",
            "title": "title",
        },
    )
    class SubjectProperty:
        def __init__(
            self,
            *,
            common_name: typing.Optional[builtins.str] = None,
            country: typing.Optional[builtins.str] = None,
            distinguished_name_qualifier: typing.Optional[builtins.str] = None,
            generation_qualifier: typing.Optional[builtins.str] = None,
            given_name: typing.Optional[builtins.str] = None,
            initials: typing.Optional[builtins.str] = None,
            locality: typing.Optional[builtins.str] = None,
            organization: typing.Optional[builtins.str] = None,
            organizational_unit: typing.Optional[builtins.str] = None,
            pseudonym: typing.Optional[builtins.str] = None,
            serial_number: typing.Optional[builtins.str] = None,
            state: typing.Optional[builtins.str] = None,
            surname: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param common_name: ``CfnCertificateAuthority.SubjectProperty.CommonName``.
            :param country: ``CfnCertificateAuthority.SubjectProperty.Country``.
            :param distinguished_name_qualifier: ``CfnCertificateAuthority.SubjectProperty.DistinguishedNameQualifier``.
            :param generation_qualifier: ``CfnCertificateAuthority.SubjectProperty.GenerationQualifier``.
            :param given_name: ``CfnCertificateAuthority.SubjectProperty.GivenName``.
            :param initials: ``CfnCertificateAuthority.SubjectProperty.Initials``.
            :param locality: ``CfnCertificateAuthority.SubjectProperty.Locality``.
            :param organization: ``CfnCertificateAuthority.SubjectProperty.Organization``.
            :param organizational_unit: ``CfnCertificateAuthority.SubjectProperty.OrganizationalUnit``.
            :param pseudonym: ``CfnCertificateAuthority.SubjectProperty.Pseudonym``.
            :param serial_number: ``CfnCertificateAuthority.SubjectProperty.SerialNumber``.
            :param state: ``CfnCertificateAuthority.SubjectProperty.State``.
            :param surname: ``CfnCertificateAuthority.SubjectProperty.Surname``.
            :param title: ``CfnCertificateAuthority.SubjectProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if common_name is not None:
                self._values["common_name"] = common_name
            if country is not None:
                self._values["country"] = country
            if distinguished_name_qualifier is not None:
                self._values["distinguished_name_qualifier"] = distinguished_name_qualifier
            if generation_qualifier is not None:
                self._values["generation_qualifier"] = generation_qualifier
            if given_name is not None:
                self._values["given_name"] = given_name
            if initials is not None:
                self._values["initials"] = initials
            if locality is not None:
                self._values["locality"] = locality
            if organization is not None:
                self._values["organization"] = organization
            if organizational_unit is not None:
                self._values["organizational_unit"] = organizational_unit
            if pseudonym is not None:
                self._values["pseudonym"] = pseudonym
            if serial_number is not None:
                self._values["serial_number"] = serial_number
            if state is not None:
                self._values["state"] = state
            if surname is not None:
                self._values["surname"] = surname
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def common_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.CommonName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-commonname
            """
            result = self._values.get("common_name")
            return result

        @builtins.property
        def country(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Country``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-country
            """
            result = self._values.get("country")
            return result

        @builtins.property
        def distinguished_name_qualifier(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.DistinguishedNameQualifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-distinguishednamequalifier
            """
            result = self._values.get("distinguished_name_qualifier")
            return result

        @builtins.property
        def generation_qualifier(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.GenerationQualifier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-generationqualifier
            """
            result = self._values.get("generation_qualifier")
            return result

        @builtins.property
        def given_name(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.GivenName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-givenname
            """
            result = self._values.get("given_name")
            return result

        @builtins.property
        def initials(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Initials``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-initials
            """
            result = self._values.get("initials")
            return result

        @builtins.property
        def locality(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Locality``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-locality
            """
            result = self._values.get("locality")
            return result

        @builtins.property
        def organization(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Organization``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-organization
            """
            result = self._values.get("organization")
            return result

        @builtins.property
        def organizational_unit(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.OrganizationalUnit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-organizationalunit
            """
            result = self._values.get("organizational_unit")
            return result

        @builtins.property
        def pseudonym(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Pseudonym``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-pseudonym
            """
            result = self._values.get("pseudonym")
            return result

        @builtins.property
        def serial_number(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.SerialNumber``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-serialnumber
            """
            result = self._values.get("serial_number")
            return result

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.State``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-state
            """
            result = self._values.get("state")
            return result

        @builtins.property
        def surname(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Surname``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-surname
            """
            result = self._values.get("surname")
            return result

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            """``CfnCertificateAuthority.SubjectProperty.Title``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-title
            """
            result = self._values.get("title")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCertificateAuthorityActivation(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthorityActivation",
):
    """A CloudFormation ``AWS::ACMPCA::CertificateAuthorityActivation``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html
    :cloudformationResource: AWS::ACMPCA::CertificateAuthorityActivation
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        certificate: builtins.str,
        certificate_authority_arn: builtins.str,
        certificate_chain: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::ACMPCA::CertificateAuthorityActivation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate: ``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.
        :param certificate_authority_arn: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.
        :param certificate_chain: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.
        :param status: ``AWS::ACMPCA::CertificateAuthorityActivation.Status``.
        """
        props = CfnCertificateAuthorityActivationProps(
            certificate=certificate,
            certificate_authority_arn=certificate_authority_arn,
            certificate_chain=certificate_chain,
            status=status,
        )

        jsii.create(CfnCertificateAuthorityActivation, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrCompleteCertificateChain")
    def attr_complete_certificate_chain(self) -> builtins.str:
        """
        :cloudformationAttribute: CompleteCertificateChain
        """
        return jsii.get(self, "attrCompleteCertificateChain")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificate
        """
        return jsii.get(self, "certificate")

    @certificate.setter # type: ignore
    def certificate(self, value: builtins.str) -> None:
        jsii.set(self, "certificate", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificateauthorityarn
        """
        return jsii.get(self, "certificateAuthorityArn")

    @certificate_authority_arn.setter # type: ignore
    def certificate_authority_arn(self, value: builtins.str) -> None:
        jsii.set(self, "certificateAuthorityArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificatechain
        """
        return jsii.get(self, "certificateChain")

    @certificate_chain.setter # type: ignore
    def certificate_chain(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "certificateChain", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-status
        """
        return jsii.get(self, "status")

    @status.setter # type: ignore
    def status(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthorityActivationProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "certificate_authority_arn": "certificateAuthorityArn",
        "certificate_chain": "certificateChain",
        "status": "status",
    },
)
class CfnCertificateAuthorityActivationProps:
    def __init__(
        self,
        *,
        certificate: builtins.str,
        certificate_authority_arn: builtins.str,
        certificate_chain: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ACMPCA::CertificateAuthorityActivation``.

        :param certificate: ``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.
        :param certificate_authority_arn: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.
        :param certificate_chain: ``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.
        :param status: ``AWS::ACMPCA::CertificateAuthorityActivation.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "certificate": certificate,
            "certificate_authority_arn": certificate_authority_arn,
        }
        if certificate_chain is not None:
            self._values["certificate_chain"] = certificate_chain
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def certificate(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Certificate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificate
        """
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return result

    @builtins.property
    def certificate_authority_arn(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateAuthorityArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificateauthorityarn
        """
        result = self._values.get("certificate_authority_arn")
        assert result is not None, "Required property 'certificate_authority_arn' is missing"
        return result

    @builtins.property
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.CertificateChain``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificatechain
        """
        result = self._values.get("certificate_chain")
        return result

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::CertificateAuthorityActivation.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-status
        """
        result = self._values.get("status")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateAuthorityActivationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateAuthorityProps",
    jsii_struct_bases=[],
    name_mapping={
        "key_algorithm": "keyAlgorithm",
        "signing_algorithm": "signingAlgorithm",
        "subject": "subject",
        "type": "type",
        "revocation_configuration": "revocationConfiguration",
        "tags": "tags",
    },
)
class CfnCertificateAuthorityProps:
    def __init__(
        self,
        *,
        key_algorithm: builtins.str,
        signing_algorithm: builtins.str,
        subject: typing.Union[CfnCertificateAuthority.SubjectProperty, aws_cdk.core.IResolvable],
        type: builtins.str,
        revocation_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCertificateAuthority.RevocationConfigurationProperty]] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ACMPCA::CertificateAuthority``.

        :param key_algorithm: ``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.
        :param signing_algorithm: ``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.
        :param subject: ``AWS::ACMPCA::CertificateAuthority.Subject``.
        :param type: ``AWS::ACMPCA::CertificateAuthority.Type``.
        :param revocation_configuration: ``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.
        :param tags: ``AWS::ACMPCA::CertificateAuthority.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "key_algorithm": key_algorithm,
            "signing_algorithm": signing_algorithm,
            "subject": subject,
            "type": type,
        }
        if revocation_configuration is not None:
            self._values["revocation_configuration"] = revocation_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def key_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.KeyAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keyalgorithm
        """
        result = self._values.get("key_algorithm")
        assert result is not None, "Required property 'key_algorithm' is missing"
        return result

    @builtins.property
    def signing_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.SigningAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-signingalgorithm
        """
        result = self._values.get("signing_algorithm")
        assert result is not None, "Required property 'signing_algorithm' is missing"
        return result

    @builtins.property
    def subject(
        self,
    ) -> typing.Union[CfnCertificateAuthority.SubjectProperty, aws_cdk.core.IResolvable]:
        """``AWS::ACMPCA::CertificateAuthority.Subject``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-subject
        """
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return result

    @builtins.property
    def type(self) -> builtins.str:
        """``AWS::ACMPCA::CertificateAuthority.Type``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-type
        """
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def revocation_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnCertificateAuthority.RevocationConfigurationProperty]]:
        """``AWS::ACMPCA::CertificateAuthority.RevocationConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-revocationconfiguration
        """
        result = self._values.get("revocation_configuration")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ACMPCA::CertificateAuthority.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateAuthorityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-acmpca.CfnCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_authority_arn": "certificateAuthorityArn",
        "certificate_signing_request": "certificateSigningRequest",
        "signing_algorithm": "signingAlgorithm",
        "validity": "validity",
        "template_arn": "templateArn",
    },
)
class CfnCertificateProps:
    def __init__(
        self,
        *,
        certificate_authority_arn: builtins.str,
        certificate_signing_request: builtins.str,
        signing_algorithm: builtins.str,
        validity: typing.Union[aws_cdk.core.IResolvable, CfnCertificate.ValidityProperty],
        template_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::ACMPCA::Certificate``.

        :param certificate_authority_arn: ``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.
        :param certificate_signing_request: ``AWS::ACMPCA::Certificate.CertificateSigningRequest``.
        :param signing_algorithm: ``AWS::ACMPCA::Certificate.SigningAlgorithm``.
        :param validity: ``AWS::ACMPCA::Certificate.Validity``.
        :param template_arn: ``AWS::ACMPCA::Certificate.TemplateArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "certificate_authority_arn": certificate_authority_arn,
            "certificate_signing_request": certificate_signing_request,
            "signing_algorithm": signing_algorithm,
            "validity": validity,
        }
        if template_arn is not None:
            self._values["template_arn"] = template_arn

    @builtins.property
    def certificate_authority_arn(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.CertificateAuthorityArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificateauthorityarn
        """
        result = self._values.get("certificate_authority_arn")
        assert result is not None, "Required property 'certificate_authority_arn' is missing"
        return result

    @builtins.property
    def certificate_signing_request(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.CertificateSigningRequest``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificatesigningrequest
        """
        result = self._values.get("certificate_signing_request")
        assert result is not None, "Required property 'certificate_signing_request' is missing"
        return result

    @builtins.property
    def signing_algorithm(self) -> builtins.str:
        """``AWS::ACMPCA::Certificate.SigningAlgorithm``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-signingalgorithm
        """
        result = self._values.get("signing_algorithm")
        assert result is not None, "Required property 'signing_algorithm' is missing"
        return result

    @builtins.property
    def validity(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnCertificate.ValidityProperty]:
        """``AWS::ACMPCA::Certificate.Validity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validity
        """
        result = self._values.get("validity")
        assert result is not None, "Required property 'validity' is missing"
        return result

    @builtins.property
    def template_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ACMPCA::Certificate.TemplateArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-templatearn
        """
        result = self._values.get("template_arn")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCertificate",
    "CfnCertificateAuthority",
    "CfnCertificateAuthorityActivation",
    "CfnCertificateAuthorityActivationProps",
    "CfnCertificateAuthorityProps",
    "CfnCertificateProps",
]

publication.publish()
