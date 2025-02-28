# Checkmk Plugin: Microsoft Azure AddOn Special Agent

The **Microsoft Azure AddOn** Special Agent is an extension for the monitoring software **Checkmk**.  
It can be integrated into Checkmk 2.3 or newer.

You can download the extension package as an `.mkp` file from the [releases](../../releases) in this repository and upload it directly to your Checkmk site.  
See the Checkmk [documentation](https://docs.checkmk.com/latest/en/mkps.html) for details.

## Plugin Information

This Special Agent implements checks that aren't available in the official **Microsoft Azure** plugin.

The Plugin provides monitoring for the following components:
- Azure Arc State
- Azure Machine Extension (Azure Arc & Azure VM)

See [Check Details](#check-details) for more information.

## Prerequisites

This Special Agent uses the Microsoft Azure Resource Graph REST API to collect the monitoring data.  
To access the API, you need a Microsoft Entra tenant and a Microsoft Entra app registration with a client secret ([Steps to Get It Working](#steps-to-get-it-working)).

You need at least read permission on the required Azure resources.

To implement the check, you need to configure the *Microsoft Azure AddOn* Special Agent in Checkmk.
You will need the Microsoft Entra tenant ID, the App ID and the client secret from the Microsoft Entra app registration.
When you configure the Special Agent, you have the option to select only the services that you want to monitor. You do not have to implement all the checks, but at least one of them.

> [!NOTE]
> This plugin uses HTTPS connections to Microsoft.
>Make sure you have enabled **Trust system-wide configured CAs** or uploaded the CA certificates for the Microsoft domains in Checkmk.
>You can find these options in **Setup** > **Global settings** > **Trusted certificate authorities for SSL** under **Site management**.
>If your system does not trust the certificate you will encounter the error: `certificate verify failed: unable to get local issuer certificate`.
>
>Also do not block the communications to:
>- https://login.microsoftonline.com
>- https://management.azure.com

## Check Details
### Azure Arc State

#### Description

This check monitors the connection state of Azure Arc onboarded machines. 

#### Checkmk Service Example

![grafik](https://github.com/user-attachments/assets/a93c1621-9607-4936-ac9b-e561aa1ded4c)

#### Checkmk Parameters

1. **State connected**: Set the severity level of the state connected. The default severity level is ok.
2. **State disconnected**: Set the severity level of the state disconnected. The default severity level is warning.
3. **State error**: Set the severity level of the state error. The default severity level is critical.
4. **State expired**: Set the severity level of the state expired. The default severity level is unknown.

---

### Azure Machine Extension (Azure Arc & Azure VM)

#### Description

This check monitors the provisioning state of the Azure extensions installed on Azure Arc machines and/or Azure VMs.

#### Checkmk Service Example

![grafik](https://github.com/user-attachments/assets/843577cf-192f-4bf2-865f-75d4585a5d99)

#### Checkmk Parameters

1. **Provisioning state succeeded**: Set the severity level of the provisioning state succeeded. The default severity level is ok.
2. **Provisioning state failed**: Set the severity level of the provisioning state failed. The default severity level is critical.
3. **Provisioning state canceled**: Set the severity level of the provisioning state canceled. The default severity level is warning.
4. **Provisioning state creating**: Set the severity level of the provisioning state creating. The default severity level is ok.
5. **Provisioning state updating**: Set the severity level of the provisioning state updating. The default severity level is ok.
6. **Provisioning state deleting**: Set the severity level of the provisioning state deleting. The default severity level is ok.

## Steps to Get It Working

To use this Checkmk Special Agent, you must configure a Microsoft Entra application to access the Microsoft Azure Resource Graph REST API endpoints.
You must also have a host in Checkmk and configure the Special Agent rule for the host.

### Microsoft Entra Configuration
#### Register an Application

1. Sign in to the Microsoft Entra Admin Center (https://entra.microsoft.com) as a Global Administrator (or at least a Privileged Role Administrator)
2. Browse to **Identity** > **Applications** > **App registrations**
3. Select **New registration**
4. Provide a meaningful name (e.g. "Checkmk Special Agent")
5. Select **Accounts in this organizational directory only**
6. Do not specify a **Redirect URI**
7. Click **Register**

> [!NOTE]
> In the overview of your new application registration, you will find the **Application (client) ID** and the **Directory (tenant) ID**.
> You will need this information later for the configuration of the Checkmk Special Agent.

#### Configure the Application
1. Go to **Certificates & secrets** and click **New client secret**
2. Enter a description (e.g. the Checkmk Site name) and select an expiration period for the secret
3. Grant the application the necessary RBAC roles for your Azure resources

### Checkmk Special Agent Configuration

1. Log in to your Checkmk site

#### Add a New Password

1. Browse to **Setup** > **Passwords**
2. Select **Add password**
3. Specify a **Unique ID** and a **Title**
4. Copy the generated secret from the Microsoft Entra Admin Center to the **Password** field
5. Click **Save**

#### Add Checkmk Host

1. Add a new host in **Setup** > **Hosts**
2. Configure your custom settings and set
    -   **IP address family**: No IP
    -   **Checkmk agent / API integrations**: API integrations if configured, else Checkmk agent
3. Save

#### Add Special Agent Rule

1. Navigate to the Special Agent rule **Setup** > **Microsoft Azure AddOn** (use the search bar)
2. Add a new rule and configure the required settings
    -   **Application (client) ID** and **Directory (tenant) ID** from the Microsoft Entra Application
    -   For **Client Secret** select **From password store** and the password from **Add a New Password**
    -   Select all services that you want to monitor
    -   Add the newly created host in **Explicit hosts**
3. Save and go to your new host and discover your new services
4. Activate the changes
