provider "azurerm" {
  features {}
}

# -----------------------------
# Resource Group
# -----------------------------
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# -----------------------------
# Azure Container Registry
# -----------------------------
resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  sku                 = "Basic"
  admin_enabled       = true
}

# -----------------------------
# Container Apps Environment
# -----------------------------
resource "azurerm_container_app_environment" "env" {
  name                = "market-ml-env"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
}

# -----------------------------
# API Service (FastAPI)
# -----------------------------
resource "azurerm_container_app" "api" {
  name                         = var.container_app_name
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  depends_on = [azurerm_container_registry.acr]

  registry {
    server   = azurerm_container_registry.acr.login_server
    username = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  template {
    container {
      name   = "api"
      image  = "${azurerm_container_registry.acr.login_server}/market-ml-api:latest"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "AZURE_TENANT_ID"
        value = "8c9420b7-f093-41c2-a377-93488616df67"
      }

      env {
        name  = "AZURE_AUDIENCE"
        value = "api://b3322710-f6dd-4ead-aa02-d2e9770d6d62"
      }
    }

  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }
}

# -----------------------------
# Poller Service (Signal Ingestion)
# -----------------------------
resource "azurerm_container_app" "poller" {
  name                         = "poller-service"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  depends_on = [azurerm_container_registry.acr]

  registry {
    server   = azurerm_container_registry.acr.login_server
    username = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  template {
    container {
      name   = "poller"
      image  = "${azurerm_container_registry.acr.login_server}/poller-service:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "SIGNAL_API"
        value = "https://api.polygon.io/v2/aggs/ticker/AAPL/prev"
      }

      env {
        name  = "POLYGON_API_KEY"
        value = var.polygon_api_key
      }
    }

  }
}