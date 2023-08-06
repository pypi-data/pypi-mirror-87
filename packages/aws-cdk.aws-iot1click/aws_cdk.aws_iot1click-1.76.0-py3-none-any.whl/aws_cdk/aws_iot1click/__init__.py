"""
## AWS IoT 1-Click Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iot1click as iot1click
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
class CfnDevice(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot1click.CfnDevice",
):
    """A CloudFormation ``AWS::IoT1Click::Device``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html
    :cloudformationResource: AWS::IoT1Click::Device
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        device_id: builtins.str,
        enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
    ) -> None:
        """Create a new ``AWS::IoT1Click::Device``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param device_id: ``AWS::IoT1Click::Device.DeviceId``.
        :param enabled: ``AWS::IoT1Click::Device.Enabled``.
        """
        props = CfnDeviceProps(device_id=device_id, enabled=enabled)

        jsii.create(CfnDevice, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrDeviceId")
    def attr_device_id(self) -> builtins.str:
        """
        :cloudformationAttribute: DeviceId
        """
        return jsii.get(self, "attrDeviceId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrEnabled")
    def attr_enabled(self) -> aws_cdk.core.IResolvable:
        """
        :cloudformationAttribute: Enabled
        """
        return jsii.get(self, "attrEnabled")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> builtins.str:
        """``AWS::IoT1Click::Device.DeviceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html#cfn-iot1click-device-deviceid
        """
        return jsii.get(self, "deviceId")

    @device_id.setter # type: ignore
    def device_id(self, value: builtins.str) -> None:
        jsii.set(self, "deviceId", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::IoT1Click::Device.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html#cfn-iot1click-device-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter # type: ignore
    def enabled(
        self,
        value: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "enabled", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot1click.CfnDeviceProps",
    jsii_struct_bases=[],
    name_mapping={"device_id": "deviceId", "enabled": "enabled"},
)
class CfnDeviceProps:
    def __init__(
        self,
        *,
        device_id: builtins.str,
        enabled: typing.Union[builtins.bool, aws_cdk.core.IResolvable],
    ) -> None:
        """Properties for defining a ``AWS::IoT1Click::Device``.

        :param device_id: ``AWS::IoT1Click::Device.DeviceId``.
        :param enabled: ``AWS::IoT1Click::Device.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "device_id": device_id,
            "enabled": enabled,
        }

    @builtins.property
    def device_id(self) -> builtins.str:
        """``AWS::IoT1Click::Device.DeviceId``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html#cfn-iot1click-device-deviceid
        """
        result = self._values.get("device_id")
        assert result is not None, "Required property 'device_id' is missing"
        return result

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, aws_cdk.core.IResolvable]:
        """``AWS::IoT1Click::Device.Enabled``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-device.html#cfn-iot1click-device-enabled
        """
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeviceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPlacement(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot1click.CfnPlacement",
):
    """A CloudFormation ``AWS::IoT1Click::Placement``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html
    :cloudformationResource: AWS::IoT1Click::Placement
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        project_name: builtins.str,
        associated_devices: typing.Any = None,
        attributes: typing.Any = None,
        placement_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::IoT1Click::Placement``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param project_name: ``AWS::IoT1Click::Placement.ProjectName``.
        :param associated_devices: ``AWS::IoT1Click::Placement.AssociatedDevices``.
        :param attributes: ``AWS::IoT1Click::Placement.Attributes``.
        :param placement_name: ``AWS::IoT1Click::Placement.PlacementName``.
        """
        props = CfnPlacementProps(
            project_name=project_name,
            associated_devices=associated_devices,
            attributes=attributes,
            placement_name=placement_name,
        )

        jsii.create(CfnPlacement, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrPlacementName")
    def attr_placement_name(self) -> builtins.str:
        """
        :cloudformationAttribute: PlacementName
        """
        return jsii.get(self, "attrPlacementName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrProjectName")
    def attr_project_name(self) -> builtins.str:
        """
        :cloudformationAttribute: ProjectName
        """
        return jsii.get(self, "attrProjectName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="associatedDevices")
    def associated_devices(self) -> typing.Any:
        """``AWS::IoT1Click::Placement.AssociatedDevices``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-associateddevices
        """
        return jsii.get(self, "associatedDevices")

    @associated_devices.setter # type: ignore
    def associated_devices(self, value: typing.Any) -> None:
        jsii.set(self, "associatedDevices", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attributes")
    def attributes(self) -> typing.Any:
        """``AWS::IoT1Click::Placement.Attributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-attributes
        """
        return jsii.get(self, "attributes")

    @attributes.setter # type: ignore
    def attributes(self, value: typing.Any) -> None:
        jsii.set(self, "attributes", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> builtins.str:
        """``AWS::IoT1Click::Placement.ProjectName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-projectname
        """
        return jsii.get(self, "projectName")

    @project_name.setter # type: ignore
    def project_name(self, value: builtins.str) -> None:
        jsii.set(self, "projectName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="placementName")
    def placement_name(self) -> typing.Optional[builtins.str]:
        """``AWS::IoT1Click::Placement.PlacementName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-placementname
        """
        return jsii.get(self, "placementName")

    @placement_name.setter # type: ignore
    def placement_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "placementName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot1click.CfnPlacementProps",
    jsii_struct_bases=[],
    name_mapping={
        "project_name": "projectName",
        "associated_devices": "associatedDevices",
        "attributes": "attributes",
        "placement_name": "placementName",
    },
)
class CfnPlacementProps:
    def __init__(
        self,
        *,
        project_name: builtins.str,
        associated_devices: typing.Any = None,
        attributes: typing.Any = None,
        placement_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::IoT1Click::Placement``.

        :param project_name: ``AWS::IoT1Click::Placement.ProjectName``.
        :param associated_devices: ``AWS::IoT1Click::Placement.AssociatedDevices``.
        :param attributes: ``AWS::IoT1Click::Placement.Attributes``.
        :param placement_name: ``AWS::IoT1Click::Placement.PlacementName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "project_name": project_name,
        }
        if associated_devices is not None:
            self._values["associated_devices"] = associated_devices
        if attributes is not None:
            self._values["attributes"] = attributes
        if placement_name is not None:
            self._values["placement_name"] = placement_name

    @builtins.property
    def project_name(self) -> builtins.str:
        """``AWS::IoT1Click::Placement.ProjectName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-projectname
        """
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return result

    @builtins.property
    def associated_devices(self) -> typing.Any:
        """``AWS::IoT1Click::Placement.AssociatedDevices``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-associateddevices
        """
        result = self._values.get("associated_devices")
        return result

    @builtins.property
    def attributes(self) -> typing.Any:
        """``AWS::IoT1Click::Placement.Attributes``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-attributes
        """
        result = self._values.get("attributes")
        return result

    @builtins.property
    def placement_name(self) -> typing.Optional[builtins.str]:
        """``AWS::IoT1Click::Placement.PlacementName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-placement.html#cfn-iot1click-placement-placementname
        """
        result = self._values.get("placement_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlacementProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnProject(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot1click.CfnProject",
):
    """A CloudFormation ``AWS::IoT1Click::Project``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html
    :cloudformationResource: AWS::IoT1Click::Project
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        placement_template: typing.Union["CfnProject.PlacementTemplateProperty", aws_cdk.core.IResolvable],
        description: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::IoT1Click::Project``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param placement_template: ``AWS::IoT1Click::Project.PlacementTemplate``.
        :param description: ``AWS::IoT1Click::Project.Description``.
        :param project_name: ``AWS::IoT1Click::Project.ProjectName``.
        """
        props = CfnProjectProps(
            placement_template=placement_template,
            description=description,
            project_name=project_name,
        )

        jsii.create(CfnProject, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrProjectName")
    def attr_project_name(self) -> builtins.str:
        """
        :cloudformationAttribute: ProjectName
        """
        return jsii.get(self, "attrProjectName")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="placementTemplate")
    def placement_template(
        self,
    ) -> typing.Union["CfnProject.PlacementTemplateProperty", aws_cdk.core.IResolvable]:
        """``AWS::IoT1Click::Project.PlacementTemplate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-placementtemplate
        """
        return jsii.get(self, "placementTemplate")

    @placement_template.setter # type: ignore
    def placement_template(
        self,
        value: typing.Union["CfnProject.PlacementTemplateProperty", aws_cdk.core.IResolvable],
    ) -> None:
        jsii.set(self, "placementTemplate", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::IoT1Click::Project.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-description
        """
        return jsii.get(self, "description")

    @description.setter # type: ignore
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> typing.Optional[builtins.str]:
        """``AWS::IoT1Click::Project.ProjectName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-projectname
        """
        return jsii.get(self, "projectName")

    @project_name.setter # type: ignore
    def project_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "projectName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iot1click.CfnProject.DeviceTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "callback_overrides": "callbackOverrides",
            "device_type": "deviceType",
        },
    )
    class DeviceTemplateProperty:
        def __init__(
            self,
            *,
            callback_overrides: typing.Any = None,
            device_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param callback_overrides: ``CfnProject.DeviceTemplateProperty.CallbackOverrides``.
            :param device_type: ``CfnProject.DeviceTemplateProperty.DeviceType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-devicetemplate.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if callback_overrides is not None:
                self._values["callback_overrides"] = callback_overrides
            if device_type is not None:
                self._values["device_type"] = device_type

        @builtins.property
        def callback_overrides(self) -> typing.Any:
            """``CfnProject.DeviceTemplateProperty.CallbackOverrides``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-devicetemplate.html#cfn-iot1click-project-devicetemplate-callbackoverrides
            """
            result = self._values.get("callback_overrides")
            return result

        @builtins.property
        def device_type(self) -> typing.Optional[builtins.str]:
            """``CfnProject.DeviceTemplateProperty.DeviceType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-devicetemplate.html#cfn-iot1click-project-devicetemplate-devicetype
            """
            result = self._values.get("device_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iot1click.CfnProject.PlacementTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_attributes": "defaultAttributes",
            "device_templates": "deviceTemplates",
        },
    )
    class PlacementTemplateProperty:
        def __init__(
            self,
            *,
            default_attributes: typing.Any = None,
            device_templates: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnProject.DeviceTemplateProperty"]]]] = None,
        ) -> None:
            """
            :param default_attributes: ``CfnProject.PlacementTemplateProperty.DefaultAttributes``.
            :param device_templates: ``CfnProject.PlacementTemplateProperty.DeviceTemplates``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-placementtemplate.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if default_attributes is not None:
                self._values["default_attributes"] = default_attributes
            if device_templates is not None:
                self._values["device_templates"] = device_templates

        @builtins.property
        def default_attributes(self) -> typing.Any:
            """``CfnProject.PlacementTemplateProperty.DefaultAttributes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-placementtemplate.html#cfn-iot1click-project-placementtemplate-defaultattributes
            """
            result = self._values.get("default_attributes")
            return result

        @builtins.property
        def device_templates(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Mapping[builtins.str, typing.Union[aws_cdk.core.IResolvable, "CfnProject.DeviceTemplateProperty"]]]]:
            """``CfnProject.PlacementTemplateProperty.DeviceTemplates``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot1click-project-placementtemplate.html#cfn-iot1click-project-placementtemplate-devicetemplates
            """
            result = self._values.get("device_templates")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot1click.CfnProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "placement_template": "placementTemplate",
        "description": "description",
        "project_name": "projectName",
    },
)
class CfnProjectProps:
    def __init__(
        self,
        *,
        placement_template: typing.Union[CfnProject.PlacementTemplateProperty, aws_cdk.core.IResolvable],
        description: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::IoT1Click::Project``.

        :param placement_template: ``AWS::IoT1Click::Project.PlacementTemplate``.
        :param description: ``AWS::IoT1Click::Project.Description``.
        :param project_name: ``AWS::IoT1Click::Project.ProjectName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "placement_template": placement_template,
        }
        if description is not None:
            self._values["description"] = description
        if project_name is not None:
            self._values["project_name"] = project_name

    @builtins.property
    def placement_template(
        self,
    ) -> typing.Union[CfnProject.PlacementTemplateProperty, aws_cdk.core.IResolvable]:
        """``AWS::IoT1Click::Project.PlacementTemplate``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-placementtemplate
        """
        result = self._values.get("placement_template")
        assert result is not None, "Required property 'placement_template' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """``AWS::IoT1Click::Project.Description``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-description
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        """``AWS::IoT1Click::Project.ProjectName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot1click-project.html#cfn-iot1click-project-projectname
        """
        result = self._values.get("project_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDevice",
    "CfnDeviceProps",
    "CfnPlacement",
    "CfnPlacementProps",
    "CfnProject",
    "CfnProjectProps",
]

publication.publish()
