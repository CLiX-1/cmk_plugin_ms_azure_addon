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

## Check Details
### Azure Arc State

#### Description

This check monitors the connection state of Azure Arc onboarded machines. 

#### Checkmk service example

![grafik](https://github.com/user-attachments/assets/a93c1621-9607-4936-ac9b-e561aa1ded4c)


#### Checkmk Parameters

1. **State connected**: Set the severity level of the state connected. The default severity level is ok.
2. **State disconnected**: Set the severity level of the state disconnected. The default severity level is warning.
3. **State error**: Set the severity level of the state error. The default severity level is critical.
4. **State expired**: Set the severity level of the state expired. The default severity level is unknown.

### Azure Machine Extension (Azure Arc & Azure VM)

#### Description

This check monitors the provisioning state of the Azure extensions installed on Azure Arc machines and/or Azure VMs.

#### Checkmk service example

![grafik](https://github.com/user-attachments/assets/843577cf-192f-4bf2-865f-75d4585a5d99)

#### Checkmk Parameters

1. **Provisioning state succeeded**: Set the severity level of the provisioning state succeeded. The default severity level is ok.
2. **Provisioning state failed**: Set the severity level of the provisioning state failed. The default severity level is critical.
3. **Provisioning state canceled**: Set the severity level of the provisioning state canceled. The default severity level is warning.
4. **Provisioning state creating**: Set the severity level of the provisioning state creating. The default severity level is ok.
5. **Provisioning state updating**: Set the severity level of the provisioning state updating. The default severity level is ok.
6. **Provisioning state deleting**: Set the severity level of the provisioning state deleting. The default severity level is ok.

## Steps to get it working

To use this Checkmk Special Agent, you must configure a Microsoft Entra Application to access the Microsoft Graph API endpoints.
You must also have a host in Checkmk and configure the Special Agent rule for the host.

### Microsoft Entra Configuration
#### Register an Application

1. Sign in to the Microsoft Entra Admin Center (https://entra.microsoft.com) as a Global Administrator (at least a Privileged Role Administrator)
2. Browse to **Identity** > **Applications** > **App registrations**
3. Select **New registration**
4. Provide a meaningful name (e.g. "Checkmk Special Agent")
5. Select **Accounts in this organizational directory only**
6. Do not specify a **Redirect URI**
7. Click **Register**

> [!NOTE]
> In the overview of your new application registration you will find the **Application (client) ID** and the **Directory (tenant) ID**.
> You will need this information later for the configuration of the Checkmk Special Agent.

#### Configure the Application
1. Go to **API permissions**
2. Click **Add a permission** > **Microsoft Graph** > **Application permissions**
3. Add all API permissions for all services that you want to monitor (see sections above)
4. Select **Grant admin consent** > **Yes**
5. Go to **Certificates & secrets** and click on **New client secret**
6. Insert a description (e.g. the Checkmk Site name) and select an expiration period for the secret

### Checkmk Special Agent Configuration

1. Log in to your Checkmk Site
   
#### Add a New Password

1. Browse to **Setup** > **Passwords**
2. Select **Add password**
3. Specify a **Unique ID** and a **Ttile**
4. Copy the generated secret from the Microsoft Entra Admin Center to the **Password** field
5. Click **Save**

#### Add Checkmk Host

1. Add a new host in **Setup** > **Hosts**
2. Configure your custom settings and set
 - **IP address family**: No IP
 - **Checkmk agent / API integrations**: API integrations if configured, else Checkmk agent
3. Save

#### Add Special Agent Rule

1. Navigate to the Special Agent rule **Setup** > **Microsoft 365** (use the search bar)
2. Add a new rule and configure the required settings
- **Application (client) ID** and **Directory (tenant) ID** from the Microsoft Entra Application
- For **Client secret** select **From password store** and the password from **Add a New Password**
- Select all services that you want to monitor
- Add the newly created host in **Explicit hosts**
3. Save and go to your new host and discover your new services
4. Activate the changes
