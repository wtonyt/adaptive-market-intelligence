provider "azurerm" {
  features {}
}

# -----------------------------------
# Resource Group
# -----------------------------------
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# -----------------------------------
# Azure Container Registry
# -----------------------------------
resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  sku                 = "Basic"
  admin_enabled       = true
}

# -----------------------------------
# Container Apps Environment
# -----------------------------------
resource "azurerm_container_app_environment" "env" {
  name                = "market-ml-dev-env"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
}

module "service_bus" {
  source = "../../modules/service-bus"

  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location

  namespace_name = "marketmldevbus"
  queue_name     = "signals"
}
# -----------------------------------
# API Service
# -----------------------------------
module "api_service" {
  source = "../../modules/container-app"

  app_name                     = "market-ml-api-dev"
  resource_group_name          = azurerm_resource_group.rg.name
  container_app_environment_id = azurerm_container_app_environment.env.id

  acr_login_server = azurerm_container_registry.acr.login_server
  acr_username     = azurerm_container_registry.acr.admin_username
  acr_password     = azurerm_container_registry.acr.admin_password

  image_name = "market-ml-api"
  image_tag  = "latest"

  cpu    = 0.5
  memory = "1Gi"

  external_enabled = true
  target_port      = 8000

  environment_variables = {
    AZURE_TENANT_ID = "8c9420b7-f093-41c2-a377-93488616df67"
    AZURE_AUDIENCE  = "api://b3322710-f6dd-4ead-aa02-d2e9770d6d62"
  }
}

# -----------------------------------
# Poller Service
# -----------------------------------
module "poller_service" {
  source = "../../modules/container-app"

  app_name                     = "poller-service-dev"
  resource_group_name          = azurerm_resource_group.rg.name
  container_app_environment_id = azurerm_container_app_environment.env.id

  acr_login_server = azurerm_container_registry.acr.login_server
  acr_username     = azurerm_container_registry.acr.admin_username
  acr_password     = azurerm_container_registry.acr.admin_password

  image_name = "poller-service"
  image_tag  = "latest"

  cpu    = 0.25
  memory = "0.5Gi"

  external_enabled = false

  environment_variables = {
    SIGNAL_API      = "https://api.polygon.io/v2/aggs/ticker/AAPL/prev"
    POLYGON_API_KEY = var.polygon_api_key
  }
}