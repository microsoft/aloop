@description('Base name for container app resources')
param name string

@description('Location for the resource')
param location string

@description('Tags for the resource')
param tags object = {}

@description('User-assigned managed identity resource ID')
param identityId string

@description('Client ID of the managed identity')
param identityClientId string

@description('Azure OpenAI endpoint URL')
param openAiEndpoint string

@description('Azure OpenAI deployment name')
param openAiDeployment string

@description('Storage account name')
param storageAccountName string

var envName = 'cae-${name}'
var appName = name
var logName = 'log-${name}'
var crName = replace('cr${name}', '-', '')

// Log Analytics workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// Container Registry
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {
  name: crName
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}

// Container Apps Environment
resource acaEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: envName
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

// AcrPull role for the managed identity on the container registry
resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(containerRegistry.id, identityId, '7f951dda-4ed3-4680-a7ca-43fe172d538d')
  scope: containerRegistry
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: reference(identityId, '2023-01-31').principalId
    principalType: 'ServicePrincipal'
  }
}

// Container App — the agent
resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: appName
  location: location
  tags: union(tags, { 'azd-service-name': 'agent' })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identityId}': {}
    }
  }
  properties: {
    managedEnvironmentId: acaEnv.id
    configuration: {
      activeRevisionsMode: 'Single'
      registries: [
        {
          server: containerRegistry.properties.loginServer
          identity: identityId
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'loop-agent'
          image: '${containerRegistry.properties.loginServer}/loop-agent:latest'
          resources: {
            cpu: json('1.0')
            memory: '2Gi'
          }
          env: [
            { name: 'AZURE_OPENAI_ENDPOINT', value: openAiEndpoint }
            { name: 'AZURE_OPENAI_DEPLOYMENT', value: openAiDeployment }
            { name: 'AZURE_OPENAI_API_VERSION', value: '2025-03-01-preview' }
            { name: 'AZURE_STORAGE_ACCOUNT_NAME', value: storageAccountName }
            { name: 'AZURE_STORAGE_CONTAINER', value: 'agent-workspace' }
            { name: 'AZURE_CLIENT_ID', value: identityClientId }
            { name: 'AGENT_NAME', value: 'aloop' }
            { name: 'LOOP_INTERVAL_MINUTES', value: '10' }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
  dependsOn: [acrPullRole]
}

output appName string = app.name
output envName string = acaEnv.name
output registryName string = containerRegistry.name
output registryServer string = containerRegistry.properties.loginServer
