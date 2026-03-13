targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment (e.g., dev, prod)')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Name of the Azure OpenAI model deployment')
param openAiModelName string = 'gpt-5.3-chat'

@description('Version of the OpenAI model')
param openAiModelVersion string = '2026-03-03'

@description('The initial steering.md content to upload')
param steeringContent string = ''

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: tags
}

// User-assigned Managed Identity
module identity './modules/identity.bicep' = {
  name: 'identity'
  scope: rg
  params: {
    name: '${abbrs.managedIdentity}${resourceToken}'
    location: location
    tags: tags
  }
}

// Storage account for agent workspace
module storage './modules/storage.bicep' = {
  name: 'storage'
  scope: rg
  params: {
    name: '${abbrs.storageAccount}${resourceToken}'
    location: location
    tags: tags
    containerName: 'agent-workspace'
    identityPrincipalId: identity.outputs.principalId
  }
}

// Azure OpenAI
module openai './modules/openai.bicep' = {
  name: 'openai'
  scope: rg
  params: {
    name: '${abbrs.openAi}${resourceToken}'
    location: location
    tags: tags
    modelName: openAiModelName
    modelVersion: openAiModelVersion
    identityPrincipalId: identity.outputs.principalId
  }
}

// Container Apps Environment + Agent App
module aca './modules/aca.bicep' = {
  name: 'aca'
  scope: rg
  params: {
    name: '${abbrs.containerApp}${resourceToken}'
    location: location
    tags: tags
    identityId: identity.outputs.id
    identityClientId: identity.outputs.clientId
    openAiEndpoint: openai.outputs.endpoint
    openAiDeployment: openAiModelName
    storageAccountName: storage.outputs.name
  }
}

// Outputs for azd
output AZURE_OPENAI_ENDPOINT string = openai.outputs.endpoint
output AZURE_OPENAI_DEPLOYMENT string = openAiModelName
output AZURE_STORAGE_ACCOUNT_NAME string = storage.outputs.name
output AZURE_CONTAINER_APP_NAME string = aca.outputs.appName
output AZURE_RESOURCE_GROUP string = rg.name
output AZURE_MANAGED_IDENTITY_CLIENT_ID string = identity.outputs.clientId
