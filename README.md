# Checkmk Plugin: Microsoft Azure AddOn Special Agent

## Plugin Information
The Microsoft Azure AddOn Special Agent can be integrated into Checkmk 2.3 or newer.

You can download the .mkp file from releases in this repository to upload it directly to your Checkmk site.

The Plugin provides monitoring of these components:
- Azure Arc State
- Azure Machine Extension (Azure Arc & Azure VM)

This Special Agent implements checks that aren't available in the official "Microsoft Azure" plugin.

## Prerequisites

This Special Agent uses the Azure Resource Graph REST API to collect the monitoring data.
To access the API, you need a Microsoft Entra Tenant and a Microsoft Entra App Registration with a secret.

You need at least read permission on the required Azure resources.

To implement the check, you need to configure the *Microsoft Azure AddOn* Special Agent in Checkmk.
You will need the Microsoft Entra Tenant ID, the Microsoft Entra App Registration ID and Secret.
When you configure the Special Agent, you have the option to select only the services that you want to monitor. You do not have to implement all the checks, but at least one of them.

## Azure Arc State

### Description

This check monitors the connection state of Azure Arc onboarded machines. 

### Checkmk service example

![grafik](https://github.com/user-attachments/assets/a93c1621-9607-4936-ac9b-e561aa1ded4c)


### Checkmk Parameters

1. **State connected**: Set the severity level of the state connected. The default severity level is ok.
2. **State disconnected**: Set the severity level of the state disconnected. The default severity level is warning.
3. **State error**: Set the severity level of the state error. The default severity level is critical.
4. **State expired**: Set the severity level of the state expired. The default severity level is unknown.

## Azure Machine Extension (Azure Arc & Azure VM)

### Description

This check monitors the provisioning state of the Azure extensions installed on Azure Arc machines and/or Azure VMs.

### Checkmk service example

![grafik](https://github.com/user-attachments/assets/843577cf-192f-4bf2-865f-75d4585a5d99)

### Checkmk Parameters

1. **Provisioning state succeeded**: Set the severity level of the provisioning state succeeded. The default severity level is ok.
2. **Provisioning state failed**: Set the severity level of the provisioning state failed. The default severity level is critical.
3. **Provisioning state canceled**: Set the severity level of the provisioning state canceled. The default severity level is warning.
4. **Provisioning state creating**: Set the severity level of the provisioning state creating. The default severity level is ok.
5. **Provisioning state updating**: Set the severity level of the provisioning state updating. The default severity level is ok.
6. **Provisioning state deleting**: Set the severity level of the provisioning state deleting. The default severity level is ok.

