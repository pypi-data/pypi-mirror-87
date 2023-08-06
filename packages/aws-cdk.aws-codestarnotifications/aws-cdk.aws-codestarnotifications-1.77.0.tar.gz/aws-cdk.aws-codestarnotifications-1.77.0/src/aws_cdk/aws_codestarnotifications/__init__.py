"""
# AWS::CodeStarNotifications Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codestarnotifications as codestarnotifications
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
class CfnNotificationRule(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codestarnotifications.CfnNotificationRule",
):
    """A CloudFormation ``AWS::CodeStarNotifications::NotificationRule``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html
    :cloudformationResource: AWS::CodeStarNotifications::NotificationRule
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        detail_type: builtins.str,
        event_type_ids: typing.List[builtins.str],
        name: builtins.str,
        resource: builtins.str,
        targets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnNotificationRule.TargetProperty", aws_cdk.core.IResolvable]]],
        status: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        """Create a new ``AWS::CodeStarNotifications::NotificationRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param detail_type: ``AWS::CodeStarNotifications::NotificationRule.DetailType``.
        :param event_type_ids: ``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.
        :param name: ``AWS::CodeStarNotifications::NotificationRule.Name``.
        :param resource: ``AWS::CodeStarNotifications::NotificationRule.Resource``.
        :param targets: ``AWS::CodeStarNotifications::NotificationRule.Targets``.
        :param status: ``AWS::CodeStarNotifications::NotificationRule.Status``.
        :param tags: ``AWS::CodeStarNotifications::NotificationRule.Tags``.
        """
        props = CfnNotificationRuleProps(
            detail_type=detail_type,
            event_type_ids=event_type_ids,
            name=name,
            resource=resource,
            targets=targets,
            status=status,
            tags=tags,
        )

        jsii.create(CfnNotificationRule, self, [scope, id, props])

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
        """``AWS::CodeStarNotifications::NotificationRule.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="detailType")
    def detail_type(self) -> builtins.str:
        """``AWS::CodeStarNotifications::NotificationRule.DetailType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-detailtype
        """
        return jsii.get(self, "detailType")

    @detail_type.setter # type: ignore
    def detail_type(self, value: builtins.str) -> None:
        jsii.set(self, "detailType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="eventTypeIds")
    def event_type_ids(self) -> typing.List[builtins.str]:
        """``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-eventtypeids
        """
        return jsii.get(self, "eventTypeIds")

    @event_type_ids.setter # type: ignore
    def event_type_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "eventTypeIds", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """``AWS::CodeStarNotifications::NotificationRule.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-name
        """
        return jsii.get(self, "name")

    @name.setter # type: ignore
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        """``AWS::CodeStarNotifications::NotificationRule.Resource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-resource
        """
        return jsii.get(self, "resource")

    @resource.setter # type: ignore
    def resource(self, value: builtins.str) -> None:
        jsii.set(self, "resource", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnNotificationRule.TargetProperty", aws_cdk.core.IResolvable]]]:
        """``AWS::CodeStarNotifications::NotificationRule.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-targets
        """
        return jsii.get(self, "targets")

    @targets.setter # type: ignore
    def targets(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnNotificationRule.TargetProperty", aws_cdk.core.IResolvable]]],
    ) -> None:
        jsii.set(self, "targets", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeStarNotifications::NotificationRule.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-status
        """
        return jsii.get(self, "status")

    @status.setter # type: ignore
    def status(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codestarnotifications.CfnNotificationRule.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={"target_address": "targetAddress", "target_type": "targetType"},
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            target_address: typing.Optional[builtins.str] = None,
            target_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param target_address: ``CfnNotificationRule.TargetProperty.TargetAddress``.
            :param target_type: ``CfnNotificationRule.TargetProperty.TargetType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if target_address is not None:
                self._values["target_address"] = target_address
            if target_type is not None:
                self._values["target_type"] = target_type

        @builtins.property
        def target_address(self) -> typing.Optional[builtins.str]:
            """``CfnNotificationRule.TargetProperty.TargetAddress``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html#cfn-codestarnotifications-notificationrule-target-targetaddress
            """
            result = self._values.get("target_address")
            return result

        @builtins.property
        def target_type(self) -> typing.Optional[builtins.str]:
            """``CfnNotificationRule.TargetProperty.TargetType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html#cfn-codestarnotifications-notificationrule-target-targettype
            """
            result = self._values.get("target_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codestarnotifications.CfnNotificationRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "detail_type": "detailType",
        "event_type_ids": "eventTypeIds",
        "name": "name",
        "resource": "resource",
        "targets": "targets",
        "status": "status",
        "tags": "tags",
    },
)
class CfnNotificationRuleProps:
    def __init__(
        self,
        *,
        detail_type: builtins.str,
        event_type_ids: typing.List[builtins.str],
        name: builtins.str,
        resource: builtins.str,
        targets: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[CfnNotificationRule.TargetProperty, aws_cdk.core.IResolvable]]],
        status: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        """Properties for defining a ``AWS::CodeStarNotifications::NotificationRule``.

        :param detail_type: ``AWS::CodeStarNotifications::NotificationRule.DetailType``.
        :param event_type_ids: ``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.
        :param name: ``AWS::CodeStarNotifications::NotificationRule.Name``.
        :param resource: ``AWS::CodeStarNotifications::NotificationRule.Resource``.
        :param targets: ``AWS::CodeStarNotifications::NotificationRule.Targets``.
        :param status: ``AWS::CodeStarNotifications::NotificationRule.Status``.
        :param tags: ``AWS::CodeStarNotifications::NotificationRule.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "detail_type": detail_type,
            "event_type_ids": event_type_ids,
            "name": name,
            "resource": resource,
            "targets": targets,
        }
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def detail_type(self) -> builtins.str:
        """``AWS::CodeStarNotifications::NotificationRule.DetailType``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-detailtype
        """
        result = self._values.get("detail_type")
        assert result is not None, "Required property 'detail_type' is missing"
        return result

    @builtins.property
    def event_type_ids(self) -> typing.List[builtins.str]:
        """``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-eventtypeids
        """
        result = self._values.get("event_type_ids")
        assert result is not None, "Required property 'event_type_ids' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """``AWS::CodeStarNotifications::NotificationRule.Name``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-name
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def resource(self) -> builtins.str:
        """``AWS::CodeStarNotifications::NotificationRule.Resource``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-resource
        """
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return result

    @builtins.property
    def targets(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[CfnNotificationRule.TargetProperty, aws_cdk.core.IResolvable]]]:
        """``AWS::CodeStarNotifications::NotificationRule.Targets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-targets
        """
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return result

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::CodeStarNotifications::NotificationRule.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-status
        """
        result = self._values.get("status")
        return result

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::CodeStarNotifications::NotificationRule.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNotificationRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnNotificationRule",
    "CfnNotificationRuleProps",
]

publication.publish()
