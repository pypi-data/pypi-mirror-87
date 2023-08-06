"""
## AWS::ApplicationInsights Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_applicationinsights as applicationinsights
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
class CfnApplication(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication",
):
    """A CloudFormation ``AWS::ApplicationInsights::Application``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html
    :cloudformationResource: AWS::ApplicationInsights::Application
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        resource_group_name: builtins.str,
        auto_configuration_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        component_monitoring_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ComponentMonitoringSettingProperty"]]]] = None,
        custom_components: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.CustomComponentProperty"]]]] = None,
        cwe_monitor_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        log_pattern_sets: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.LogPatternSetProperty"]]]] = None,
        ops_center_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ops_item_sns_topic_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Create a new ``AWS::ApplicationInsights::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_group_name: ``AWS::ApplicationInsights::Application.ResourceGroupName``.
        :param auto_configuration_enabled: ``AWS::ApplicationInsights::Application.AutoConfigurationEnabled``.
        :param component_monitoring_settings: ``AWS::ApplicationInsights::Application.ComponentMonitoringSettings``.
        :param custom_components: ``AWS::ApplicationInsights::Application.CustomComponents``.
        :param cwe_monitor_enabled: ``AWS::ApplicationInsights::Application.CWEMonitorEnabled``.
        :param log_pattern_sets: ``AWS::ApplicationInsights::Application.LogPatternSets``.
        :param ops_center_enabled: ``AWS::ApplicationInsights::Application.OpsCenterEnabled``.
        :param ops_item_sns_topic_arn: ``AWS::ApplicationInsights::Application.OpsItemSNSTopicArn``.
        :param tags: ``AWS::ApplicationInsights::Application.Tags``.
        """
        props = CfnApplicationProps(
            resource_group_name=resource_group_name,
            auto_configuration_enabled=auto_configuration_enabled,
            component_monitoring_settings=component_monitoring_settings,
            custom_components=custom_components,
            cwe_monitor_enabled=cwe_monitor_enabled,
            log_pattern_sets=log_pattern_sets,
            ops_center_enabled=ops_center_enabled,
            ops_item_sns_topic_arn=ops_item_sns_topic_arn,
            tags=tags,
        )

        jsii.create(CfnApplication, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrApplicationArn")
    def attr_application_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: ApplicationARN
        """
        return jsii.get(self, "attrApplicationArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ApplicationInsights::Application.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        """``AWS::ApplicationInsights::Application.ResourceGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-resourcegroupname
        """
        return jsii.get(self, "resourceGroupName")

    @resource_group_name.setter # type: ignore
    def resource_group_name(self, value: builtins.str) -> None:
        jsii.set(self, "resourceGroupName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoConfigurationEnabled")
    def auto_configuration_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApplicationInsights::Application.AutoConfigurationEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-autoconfigurationenabled
        """
        return jsii.get(self, "autoConfigurationEnabled")

    @auto_configuration_enabled.setter # type: ignore
    def auto_configuration_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "autoConfigurationEnabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="componentMonitoringSettings")
    def component_monitoring_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ComponentMonitoringSettingProperty"]]]]:
        """``AWS::ApplicationInsights::Application.ComponentMonitoringSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-componentmonitoringsettings
        """
        return jsii.get(self, "componentMonitoringSettings")

    @component_monitoring_settings.setter # type: ignore
    def component_monitoring_settings(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ComponentMonitoringSettingProperty"]]]],
    ) -> None:
        jsii.set(self, "componentMonitoringSettings", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="customComponents")
    def custom_components(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.CustomComponentProperty"]]]]:
        """``AWS::ApplicationInsights::Application.CustomComponents``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-customcomponents
        """
        return jsii.get(self, "customComponents")

    @custom_components.setter # type: ignore
    def custom_components(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.CustomComponentProperty"]]]],
    ) -> None:
        jsii.set(self, "customComponents", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cweMonitorEnabled")
    def cwe_monitor_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApplicationInsights::Application.CWEMonitorEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-cwemonitorenabled
        """
        return jsii.get(self, "cweMonitorEnabled")

    @cwe_monitor_enabled.setter # type: ignore
    def cwe_monitor_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "cweMonitorEnabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="logPatternSets")
    def log_pattern_sets(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.LogPatternSetProperty"]]]]:
        """``AWS::ApplicationInsights::Application.LogPatternSets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-logpatternsets
        """
        return jsii.get(self, "logPatternSets")

    @log_pattern_sets.setter # type: ignore
    def log_pattern_sets(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.LogPatternSetProperty"]]]],
    ) -> None:
        jsii.set(self, "logPatternSets", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="opsCenterEnabled")
    def ops_center_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApplicationInsights::Application.OpsCenterEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-opscenterenabled
        """
        return jsii.get(self, "opsCenterEnabled")

    @ops_center_enabled.setter # type: ignore
    def ops_center_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "opsCenterEnabled", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="opsItemSnsTopicArn")
    def ops_item_sns_topic_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ApplicationInsights::Application.OpsItemSNSTopicArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-opsitemsnstopicarn
        """
        return jsii.get(self, "opsItemSnsTopicArn")

    @ops_item_sns_topic_arn.setter # type: ignore
    def ops_item_sns_topic_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "opsItemSnsTopicArn", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.AlarmMetricProperty",
        jsii_struct_bases=[],
        name_mapping={"alarm_metric_name": "alarmMetricName"},
    )
    class AlarmMetricProperty:
        def __init__(self, *, alarm_metric_name: builtins.str) -> None:
            """
            :param alarm_metric_name: ``CfnApplication.AlarmMetricProperty.AlarmMetricName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-alarmmetric.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "alarm_metric_name": alarm_metric_name,
            }

        @builtins.property
        def alarm_metric_name(self) -> builtins.str:
            """``CfnApplication.AlarmMetricProperty.AlarmMetricName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-alarmmetric.html#cfn-applicationinsights-application-alarmmetric-alarmmetricname
            """
            result = self._values.get("alarm_metric_name")
            assert result is not None, "Required property 'alarm_metric_name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.AlarmProperty",
        jsii_struct_bases=[],
        name_mapping={"alarm_name": "alarmName", "severity": "severity"},
    )
    class AlarmProperty:
        def __init__(
            self,
            *,
            alarm_name: builtins.str,
            severity: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param alarm_name: ``CfnApplication.AlarmProperty.AlarmName``.
            :param severity: ``CfnApplication.AlarmProperty.Severity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-alarm.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "alarm_name": alarm_name,
            }
            if severity is not None:
                self._values["severity"] = severity

        @builtins.property
        def alarm_name(self) -> builtins.str:
            """``CfnApplication.AlarmProperty.AlarmName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-alarm.html#cfn-applicationinsights-application-alarm-alarmname
            """
            result = self._values.get("alarm_name")
            assert result is not None, "Required property 'alarm_name' is missing"
            return result

        @builtins.property
        def severity(self) -> typing.Optional[builtins.str]:
            """``CfnApplication.AlarmProperty.Severity``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-alarm.html#cfn-applicationinsights-application-alarm-severity
            """
            result = self._values.get("severity")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.ComponentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration_details": "configurationDetails",
            "sub_component_type_configurations": "subComponentTypeConfigurations",
        },
    )
    class ComponentConfigurationProperty:
        def __init__(
            self,
            *,
            configuration_details: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ConfigurationDetailsProperty"]] = None,
            sub_component_type_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.SubComponentTypeConfigurationProperty"]]]] = None,
        ) -> None:
            """
            :param configuration_details: ``CfnApplication.ComponentConfigurationProperty.ConfigurationDetails``.
            :param sub_component_type_configurations: ``CfnApplication.ComponentConfigurationProperty.SubComponentTypeConfigurations``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if configuration_details is not None:
                self._values["configuration_details"] = configuration_details
            if sub_component_type_configurations is not None:
                self._values["sub_component_type_configurations"] = sub_component_type_configurations

        @builtins.property
        def configuration_details(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ConfigurationDetailsProperty"]]:
            """``CfnApplication.ComponentConfigurationProperty.ConfigurationDetails``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentconfiguration.html#cfn-applicationinsights-application-componentconfiguration-configurationdetails
            """
            result = self._values.get("configuration_details")
            return result

        @builtins.property
        def sub_component_type_configurations(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.SubComponentTypeConfigurationProperty"]]]]:
            """``CfnApplication.ComponentConfigurationProperty.SubComponentTypeConfigurations``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentconfiguration.html#cfn-applicationinsights-application-componentconfiguration-subcomponenttypeconfigurations
            """
            result = self._values.get("sub_component_type_configurations")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.ComponentMonitoringSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_arn": "componentArn",
            "component_configuration_mode": "componentConfigurationMode",
            "component_name": "componentName",
            "custom_component_configuration": "customComponentConfiguration",
            "default_overwrite_component_configuration": "defaultOverwriteComponentConfiguration",
            "tier": "tier",
        },
    )
    class ComponentMonitoringSettingProperty:
        def __init__(
            self,
            *,
            component_arn: typing.Optional[builtins.str] = None,
            component_configuration_mode: typing.Optional[builtins.str] = None,
            component_name: typing.Optional[builtins.str] = None,
            custom_component_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ComponentConfigurationProperty"]] = None,
            default_overwrite_component_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ComponentConfigurationProperty"]] = None,
            tier: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param component_arn: ``CfnApplication.ComponentMonitoringSettingProperty.ComponentARN``.
            :param component_configuration_mode: ``CfnApplication.ComponentMonitoringSettingProperty.ComponentConfigurationMode``.
            :param component_name: ``CfnApplication.ComponentMonitoringSettingProperty.ComponentName``.
            :param custom_component_configuration: ``CfnApplication.ComponentMonitoringSettingProperty.CustomComponentConfiguration``.
            :param default_overwrite_component_configuration: ``CfnApplication.ComponentMonitoringSettingProperty.DefaultOverwriteComponentConfiguration``.
            :param tier: ``CfnApplication.ComponentMonitoringSettingProperty.Tier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if component_arn is not None:
                self._values["component_arn"] = component_arn
            if component_configuration_mode is not None:
                self._values["component_configuration_mode"] = component_configuration_mode
            if component_name is not None:
                self._values["component_name"] = component_name
            if custom_component_configuration is not None:
                self._values["custom_component_configuration"] = custom_component_configuration
            if default_overwrite_component_configuration is not None:
                self._values["default_overwrite_component_configuration"] = default_overwrite_component_configuration
            if tier is not None:
                self._values["tier"] = tier

        @builtins.property
        def component_arn(self) -> typing.Optional[builtins.str]:
            """``CfnApplication.ComponentMonitoringSettingProperty.ComponentARN``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-componentarn
            """
            result = self._values.get("component_arn")
            return result

        @builtins.property
        def component_configuration_mode(self) -> typing.Optional[builtins.str]:
            """``CfnApplication.ComponentMonitoringSettingProperty.ComponentConfigurationMode``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-componentconfigurationmode
            """
            result = self._values.get("component_configuration_mode")
            return result

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            """``CfnApplication.ComponentMonitoringSettingProperty.ComponentName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-componentname
            """
            result = self._values.get("component_name")
            return result

        @builtins.property
        def custom_component_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ComponentConfigurationProperty"]]:
            """``CfnApplication.ComponentMonitoringSettingProperty.CustomComponentConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-customcomponentconfiguration
            """
            result = self._values.get("custom_component_configuration")
            return result

        @builtins.property
        def default_overwrite_component_configuration(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.ComponentConfigurationProperty"]]:
            """``CfnApplication.ComponentMonitoringSettingProperty.DefaultOverwriteComponentConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-defaultoverwritecomponentconfiguration
            """
            result = self._values.get("default_overwrite_component_configuration")
            return result

        @builtins.property
        def tier(self) -> typing.Optional[builtins.str]:
            """``CfnApplication.ComponentMonitoringSettingProperty.Tier``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-componentmonitoringsetting.html#cfn-applicationinsights-application-componentmonitoringsetting-tier
            """
            result = self._values.get("tier")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentMonitoringSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.ConfigurationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarm_metrics": "alarmMetrics",
            "alarms": "alarms",
            "logs": "logs",
            "windows_events": "windowsEvents",
        },
    )
    class ConfigurationDetailsProperty:
        def __init__(
            self,
            *,
            alarm_metrics: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.AlarmMetricProperty"]]]] = None,
            alarms: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.AlarmProperty"]]]] = None,
            logs: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.LogProperty"]]]] = None,
            windows_events: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.WindowsEventProperty"]]]] = None,
        ) -> None:
            """
            :param alarm_metrics: ``CfnApplication.ConfigurationDetailsProperty.AlarmMetrics``.
            :param alarms: ``CfnApplication.ConfigurationDetailsProperty.Alarms``.
            :param logs: ``CfnApplication.ConfigurationDetailsProperty.Logs``.
            :param windows_events: ``CfnApplication.ConfigurationDetailsProperty.WindowsEvents``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if alarm_metrics is not None:
                self._values["alarm_metrics"] = alarm_metrics
            if alarms is not None:
                self._values["alarms"] = alarms
            if logs is not None:
                self._values["logs"] = logs
            if windows_events is not None:
                self._values["windows_events"] = windows_events

        @builtins.property
        def alarm_metrics(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.AlarmMetricProperty"]]]]:
            """``CfnApplication.ConfigurationDetailsProperty.AlarmMetrics``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-alarmmetrics
            """
            result = self._values.get("alarm_metrics")
            return result

        @builtins.property
        def alarms(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.AlarmProperty"]]]]:
            """``CfnApplication.ConfigurationDetailsProperty.Alarms``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-alarms
            """
            result = self._values.get("alarms")
            return result

        @builtins.property
        def logs(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.LogProperty"]]]]:
            """``CfnApplication.ConfigurationDetailsProperty.Logs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-logs
            """
            result = self._values.get("logs")
            return result

        @builtins.property
        def windows_events(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.WindowsEventProperty"]]]]:
            """``CfnApplication.ConfigurationDetailsProperty.WindowsEvents``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-configurationdetails.html#cfn-applicationinsights-application-configurationdetails-windowsevents
            """
            result = self._values.get("windows_events")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.CustomComponentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_name": "componentName",
            "resource_list": "resourceList",
        },
    )
    class CustomComponentProperty:
        def __init__(
            self,
            *,
            component_name: builtins.str,
            resource_list: typing.List[builtins.str],
        ) -> None:
            """
            :param component_name: ``CfnApplication.CustomComponentProperty.ComponentName``.
            :param resource_list: ``CfnApplication.CustomComponentProperty.ResourceList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-customcomponent.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "component_name": component_name,
                "resource_list": resource_list,
            }

        @builtins.property
        def component_name(self) -> builtins.str:
            """``CfnApplication.CustomComponentProperty.ComponentName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-customcomponent.html#cfn-applicationinsights-application-customcomponent-componentname
            """
            result = self._values.get("component_name")
            assert result is not None, "Required property 'component_name' is missing"
            return result

        @builtins.property
        def resource_list(self) -> typing.List[builtins.str]:
            """``CfnApplication.CustomComponentProperty.ResourceList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-customcomponent.html#cfn-applicationinsights-application-customcomponent-resourcelist
            """
            result = self._values.get("resource_list")
            assert result is not None, "Required property 'resource_list' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomComponentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.LogPatternProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pattern": "pattern",
            "pattern_name": "patternName",
            "rank": "rank",
        },
    )
    class LogPatternProperty:
        def __init__(
            self,
            *,
            pattern: builtins.str,
            pattern_name: builtins.str,
            rank: jsii.Number,
        ) -> None:
            """
            :param pattern: ``CfnApplication.LogPatternProperty.Pattern``.
            :param pattern_name: ``CfnApplication.LogPatternProperty.PatternName``.
            :param rank: ``CfnApplication.LogPatternProperty.Rank``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpattern.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "pattern": pattern,
                "pattern_name": pattern_name,
                "rank": rank,
            }

        @builtins.property
        def pattern(self) -> builtins.str:
            """``CfnApplication.LogPatternProperty.Pattern``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpattern.html#cfn-applicationinsights-application-logpattern-pattern
            """
            result = self._values.get("pattern")
            assert result is not None, "Required property 'pattern' is missing"
            return result

        @builtins.property
        def pattern_name(self) -> builtins.str:
            """``CfnApplication.LogPatternProperty.PatternName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpattern.html#cfn-applicationinsights-application-logpattern-patternname
            """
            result = self._values.get("pattern_name")
            assert result is not None, "Required property 'pattern_name' is missing"
            return result

        @builtins.property
        def rank(self) -> jsii.Number:
            """``CfnApplication.LogPatternProperty.Rank``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpattern.html#cfn-applicationinsights-application-logpattern-rank
            """
            result = self._values.get("rank")
            assert result is not None, "Required property 'rank' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogPatternProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.LogPatternSetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_patterns": "logPatterns",
            "pattern_set_name": "patternSetName",
        },
    )
    class LogPatternSetProperty:
        def __init__(
            self,
            *,
            log_patterns: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.LogPatternProperty"]]],
            pattern_set_name: builtins.str,
        ) -> None:
            """
            :param log_patterns: ``CfnApplication.LogPatternSetProperty.LogPatterns``.
            :param pattern_set_name: ``CfnApplication.LogPatternSetProperty.PatternSetName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpatternset.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "log_patterns": log_patterns,
                "pattern_set_name": pattern_set_name,
            }

        @builtins.property
        def log_patterns(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.LogPatternProperty"]]]:
            """``CfnApplication.LogPatternSetProperty.LogPatterns``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpatternset.html#cfn-applicationinsights-application-logpatternset-logpatterns
            """
            result = self._values.get("log_patterns")
            assert result is not None, "Required property 'log_patterns' is missing"
            return result

        @builtins.property
        def pattern_set_name(self) -> builtins.str:
            """``CfnApplication.LogPatternSetProperty.PatternSetName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-logpatternset.html#cfn-applicationinsights-application-logpatternset-patternsetname
            """
            result = self._values.get("pattern_set_name")
            assert result is not None, "Required property 'pattern_set_name' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogPatternSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.LogProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_type": "logType",
            "encoding": "encoding",
            "log_group_name": "logGroupName",
            "log_path": "logPath",
            "pattern_set": "patternSet",
        },
    )
    class LogProperty:
        def __init__(
            self,
            *,
            log_type: builtins.str,
            encoding: typing.Optional[builtins.str] = None,
            log_group_name: typing.Optional[builtins.str] = None,
            log_path: typing.Optional[builtins.str] = None,
            pattern_set: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param log_type: ``CfnApplication.LogProperty.LogType``.
            :param encoding: ``CfnApplication.LogProperty.Encoding``.
            :param log_group_name: ``CfnApplication.LogProperty.LogGroupName``.
            :param log_path: ``CfnApplication.LogProperty.LogPath``.
            :param pattern_set: ``CfnApplication.LogProperty.PatternSet``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "log_type": log_type,
            }
            if encoding is not None:
                self._values["encoding"] = encoding
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name
            if log_path is not None:
                self._values["log_path"] = log_path
            if pattern_set is not None:
                self._values["pattern_set"] = pattern_set

        @builtins.property
        def log_type(self) -> builtins.str:
            """``CfnApplication.LogProperty.LogType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html#cfn-applicationinsights-application-log-logtype
            """
            result = self._values.get("log_type")
            assert result is not None, "Required property 'log_type' is missing"
            return result

        @builtins.property
        def encoding(self) -> typing.Optional[builtins.str]:
            """``CfnApplication.LogProperty.Encoding``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html#cfn-applicationinsights-application-log-encoding
            """
            result = self._values.get("encoding")
            return result

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            """``CfnApplication.LogProperty.LogGroupName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html#cfn-applicationinsights-application-log-loggroupname
            """
            result = self._values.get("log_group_name")
            return result

        @builtins.property
        def log_path(self) -> typing.Optional[builtins.str]:
            """``CfnApplication.LogProperty.LogPath``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html#cfn-applicationinsights-application-log-logpath
            """
            result = self._values.get("log_path")
            return result

        @builtins.property
        def pattern_set(self) -> typing.Optional[builtins.str]:
            """``CfnApplication.LogProperty.PatternSet``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-log.html#cfn-applicationinsights-application-log-patternset
            """
            result = self._values.get("pattern_set")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.SubComponentConfigurationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarm_metrics": "alarmMetrics",
            "logs": "logs",
            "windows_events": "windowsEvents",
        },
    )
    class SubComponentConfigurationDetailsProperty:
        def __init__(
            self,
            *,
            alarm_metrics: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.AlarmMetricProperty"]]]] = None,
            logs: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.LogProperty"]]]] = None,
            windows_events: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.WindowsEventProperty"]]]] = None,
        ) -> None:
            """
            :param alarm_metrics: ``CfnApplication.SubComponentConfigurationDetailsProperty.AlarmMetrics``.
            :param logs: ``CfnApplication.SubComponentConfigurationDetailsProperty.Logs``.
            :param windows_events: ``CfnApplication.SubComponentConfigurationDetailsProperty.WindowsEvents``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponentconfigurationdetails.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if alarm_metrics is not None:
                self._values["alarm_metrics"] = alarm_metrics
            if logs is not None:
                self._values["logs"] = logs
            if windows_events is not None:
                self._values["windows_events"] = windows_events

        @builtins.property
        def alarm_metrics(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.AlarmMetricProperty"]]]]:
            """``CfnApplication.SubComponentConfigurationDetailsProperty.AlarmMetrics``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponentconfigurationdetails.html#cfn-applicationinsights-application-subcomponentconfigurationdetails-alarmmetrics
            """
            result = self._values.get("alarm_metrics")
            return result

        @builtins.property
        def logs(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.LogProperty"]]]]:
            """``CfnApplication.SubComponentConfigurationDetailsProperty.Logs``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponentconfigurationdetails.html#cfn-applicationinsights-application-subcomponentconfigurationdetails-logs
            """
            result = self._values.get("logs")
            return result

        @builtins.property
        def windows_events(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnApplication.WindowsEventProperty"]]]]:
            """``CfnApplication.SubComponentConfigurationDetailsProperty.WindowsEvents``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponentconfigurationdetails.html#cfn-applicationinsights-application-subcomponentconfigurationdetails-windowsevents
            """
            result = self._values.get("windows_events")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubComponentConfigurationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.SubComponentTypeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "sub_component_configuration_details": "subComponentConfigurationDetails",
            "sub_component_type": "subComponentType",
        },
    )
    class SubComponentTypeConfigurationProperty:
        def __init__(
            self,
            *,
            sub_component_configuration_details: typing.Union[aws_cdk.core.IResolvable, "CfnApplication.SubComponentConfigurationDetailsProperty"],
            sub_component_type: builtins.str,
        ) -> None:
            """
            :param sub_component_configuration_details: ``CfnApplication.SubComponentTypeConfigurationProperty.SubComponentConfigurationDetails``.
            :param sub_component_type: ``CfnApplication.SubComponentTypeConfigurationProperty.SubComponentType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponenttypeconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "sub_component_configuration_details": sub_component_configuration_details,
                "sub_component_type": sub_component_type,
            }

        @builtins.property
        def sub_component_configuration_details(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, "CfnApplication.SubComponentConfigurationDetailsProperty"]:
            """``CfnApplication.SubComponentTypeConfigurationProperty.SubComponentConfigurationDetails``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponenttypeconfiguration.html#cfn-applicationinsights-application-subcomponenttypeconfiguration-subcomponentconfigurationdetails
            """
            result = self._values.get("sub_component_configuration_details")
            assert result is not None, "Required property 'sub_component_configuration_details' is missing"
            return result

        @builtins.property
        def sub_component_type(self) -> builtins.str:
            """``CfnApplication.SubComponentTypeConfigurationProperty.SubComponentType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-subcomponenttypeconfiguration.html#cfn-applicationinsights-application-subcomponenttypeconfiguration-subcomponenttype
            """
            result = self._values.get("sub_component_type")
            assert result is not None, "Required property 'sub_component_type' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubComponentTypeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-applicationinsights.CfnApplication.WindowsEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_levels": "eventLevels",
            "event_name": "eventName",
            "log_group_name": "logGroupName",
            "pattern_set": "patternSet",
        },
    )
    class WindowsEventProperty:
        def __init__(
            self,
            *,
            event_levels: typing.List[builtins.str],
            event_name: builtins.str,
            log_group_name: builtins.str,
            pattern_set: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param event_levels: ``CfnApplication.WindowsEventProperty.EventLevels``.
            :param event_name: ``CfnApplication.WindowsEventProperty.EventName``.
            :param log_group_name: ``CfnApplication.WindowsEventProperty.LogGroupName``.
            :param pattern_set: ``CfnApplication.WindowsEventProperty.PatternSet``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-windowsevent.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "event_levels": event_levels,
                "event_name": event_name,
                "log_group_name": log_group_name,
            }
            if pattern_set is not None:
                self._values["pattern_set"] = pattern_set

        @builtins.property
        def event_levels(self) -> typing.List[builtins.str]:
            """``CfnApplication.WindowsEventProperty.EventLevels``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-windowsevent.html#cfn-applicationinsights-application-windowsevent-eventlevels
            """
            result = self._values.get("event_levels")
            assert result is not None, "Required property 'event_levels' is missing"
            return result

        @builtins.property
        def event_name(self) -> builtins.str:
            """``CfnApplication.WindowsEventProperty.EventName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-windowsevent.html#cfn-applicationinsights-application-windowsevent-eventname
            """
            result = self._values.get("event_name")
            assert result is not None, "Required property 'event_name' is missing"
            return result

        @builtins.property
        def log_group_name(self) -> builtins.str:
            """``CfnApplication.WindowsEventProperty.LogGroupName``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-windowsevent.html#cfn-applicationinsights-application-windowsevent-loggroupname
            """
            result = self._values.get("log_group_name")
            assert result is not None, "Required property 'log_group_name' is missing"
            return result

        @builtins.property
        def pattern_set(self) -> typing.Optional[builtins.str]:
            """``CfnApplication.WindowsEventProperty.PatternSet``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationinsights-application-windowsevent.html#cfn-applicationinsights-application-windowsevent-patternset
            """
            result = self._values.get("pattern_set")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WindowsEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-applicationinsights.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "resource_group_name": "resourceGroupName",
        "auto_configuration_enabled": "autoConfigurationEnabled",
        "component_monitoring_settings": "componentMonitoringSettings",
        "custom_components": "customComponents",
        "cwe_monitor_enabled": "cweMonitorEnabled",
        "log_pattern_sets": "logPatternSets",
        "ops_center_enabled": "opsCenterEnabled",
        "ops_item_sns_topic_arn": "opsItemSnsTopicArn",
        "tags": "tags",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        resource_group_name: builtins.str,
        auto_configuration_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        component_monitoring_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApplication.ComponentMonitoringSettingProperty]]]] = None,
        custom_components: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApplication.CustomComponentProperty]]]] = None,
        cwe_monitor_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        log_pattern_sets: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApplication.LogPatternSetProperty]]]] = None,
        ops_center_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ops_item_sns_topic_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        """Properties for defining a ``AWS::ApplicationInsights::Application``.

        :param resource_group_name: ``AWS::ApplicationInsights::Application.ResourceGroupName``.
        :param auto_configuration_enabled: ``AWS::ApplicationInsights::Application.AutoConfigurationEnabled``.
        :param component_monitoring_settings: ``AWS::ApplicationInsights::Application.ComponentMonitoringSettings``.
        :param custom_components: ``AWS::ApplicationInsights::Application.CustomComponents``.
        :param cwe_monitor_enabled: ``AWS::ApplicationInsights::Application.CWEMonitorEnabled``.
        :param log_pattern_sets: ``AWS::ApplicationInsights::Application.LogPatternSets``.
        :param ops_center_enabled: ``AWS::ApplicationInsights::Application.OpsCenterEnabled``.
        :param ops_item_sns_topic_arn: ``AWS::ApplicationInsights::Application.OpsItemSNSTopicArn``.
        :param tags: ``AWS::ApplicationInsights::Application.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "resource_group_name": resource_group_name,
        }
        if auto_configuration_enabled is not None:
            self._values["auto_configuration_enabled"] = auto_configuration_enabled
        if component_monitoring_settings is not None:
            self._values["component_monitoring_settings"] = component_monitoring_settings
        if custom_components is not None:
            self._values["custom_components"] = custom_components
        if cwe_monitor_enabled is not None:
            self._values["cwe_monitor_enabled"] = cwe_monitor_enabled
        if log_pattern_sets is not None:
            self._values["log_pattern_sets"] = log_pattern_sets
        if ops_center_enabled is not None:
            self._values["ops_center_enabled"] = ops_center_enabled
        if ops_item_sns_topic_arn is not None:
            self._values["ops_item_sns_topic_arn"] = ops_item_sns_topic_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        """``AWS::ApplicationInsights::Application.ResourceGroupName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-resourcegroupname
        """
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return result

    @builtins.property
    def auto_configuration_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApplicationInsights::Application.AutoConfigurationEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-autoconfigurationenabled
        """
        result = self._values.get("auto_configuration_enabled")
        return result

    @builtins.property
    def component_monitoring_settings(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApplication.ComponentMonitoringSettingProperty]]]]:
        """``AWS::ApplicationInsights::Application.ComponentMonitoringSettings``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-componentmonitoringsettings
        """
        result = self._values.get("component_monitoring_settings")
        return result

    @builtins.property
    def custom_components(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApplication.CustomComponentProperty]]]]:
        """``AWS::ApplicationInsights::Application.CustomComponents``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-customcomponents
        """
        result = self._values.get("custom_components")
        return result

    @builtins.property
    def cwe_monitor_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApplicationInsights::Application.CWEMonitorEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-cwemonitorenabled
        """
        result = self._values.get("cwe_monitor_enabled")
        return result

    @builtins.property
    def log_pattern_sets(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnApplication.LogPatternSetProperty]]]]:
        """``AWS::ApplicationInsights::Application.LogPatternSets``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-logpatternsets
        """
        result = self._values.get("log_pattern_sets")
        return result

    @builtins.property
    def ops_center_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApplicationInsights::Application.OpsCenterEnabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-opscenterenabled
        """
        result = self._values.get("ops_center_enabled")
        return result

    @builtins.property
    def ops_item_sns_topic_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::ApplicationInsights::Application.OpsItemSNSTopicArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-opsitemsnstopicarn
        """
        result = self._values.get("ops_item_sns_topic_arn")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::ApplicationInsights::Application.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationinsights-application.html#cfn-applicationinsights-application-tags
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplication",
    "CfnApplicationProps",
]

publication.publish()
