param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroup,

    [Parameter(Mandatory=$true)]
    [string]$Location,

    [Parameter(Mandatory=$true)]
    [string]$AppName,

    [Parameter(Mandatory=$true)]
    [string]$PlanName,

    [Parameter(Mandatory=$true)]
    [string]$SmtpUser,

    [Parameter(Mandatory=$true)]
    [string]$SmtpPassword,

    [Parameter(Mandatory=$true)]
    [string]$MailFrom
)

$ErrorActionPreference = "Stop"

Write-Host "Creating resource group..."
az group create --name $ResourceGroup --location $Location | Out-Null

Write-Host "Creating Linux App Service plan..."
az appservice plan create --name $PlanName --resource-group $ResourceGroup --location $Location --is-linux --sku B1 | Out-Null

Write-Host "Creating web app..."
az webapp create --name $AppName --resource-group $ResourceGroup --plan $PlanName --runtime "PYTHON|3.12" | Out-Null

Write-Host "Configuring startup command..."
az webapp config set --resource-group $ResourceGroup --name $AppName --startup-file "bash startup.sh" | Out-Null

$publicUrl = "https://$AppName.azurewebsites.net"

Write-Host "Setting app settings..."
$settings = @(
    "SCM_DO_BUILD_DURING_DEPLOYMENT=true",
    "ENABLE_ORYX_BUILD=true",
    "SMTP_HOST=smtp.office365.com",
    "SMTP_PORT=587",
    "SMTP_USE_TLS=true",
    "SMTP_USER=$SmtpUser",
    "SMTP_PASSWORD=$SmtpPassword",
    "MAIL_FROM=$MailFrom",
    "MAIL_TO=6077cro@walmart.com",
    "PUBLIC_URL=$publicUrl"
)

az webapp config appsettings set --resource-group $ResourceGroup --name $AppName --settings $settings | Out-Null

Write-Host "Done. Deploy code with:"
Write-Host "  az webapp deployment source config-local-git --name $AppName --resource-group $ResourceGroup"
Write-Host "Then push this repo to the returned Azure Git remote, or use GitHub Deployment Center in portal."
Write-Host "App URL: $publicUrl"
Write-Host "QR URL: $publicUrl/qr"
