provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

# --- Factory Foundation (Azure) ---

resource "azurerm_resource_group" "factory" {
  name     = "rg-${var.project_name}-foundation-${var.environment}"
  location = var.location
}

# --- Factory Control Plane (AKS) ---

resource "azurerm_kubernetes_cluster" "factory_k8s" {
  name                = "aks-${var.project_name}-control-plane-${var.environment}"
  location            = azurerm_resource_group.factory.location
  resource_group_name = azurerm_resource_group.factory.name
  dns_prefix          = "factory-k8s"

  default_node_pool {
    name       = "factorypool"
    node_count = 3
    vm_size    = "Standard_D4s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Institutional Template Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "factory" {
  name                   = "psql-${var.project_name}-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.factory.name
  location               = azurerm_resource_group.factory.location
  version                = "13"
  administrator_login    = "factoryadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Global Blueprint Hub (AWS S3) ---

resource "aws_s3_bucket" "blueprint_hub" {
  bucket = "db-enterprise-blueprint-hub-${var.environment}"
}

# --- Factory Secrets & Certificates ---

resource "azurerm_key_vault" "factory" {
  name                        = "kv-factory-${var.environment}"
  location                    = azurerm_resource_group.factory.location
  resource_group_name         = azurerm_resource_group.factory.name
  enabled_for_disk_encryption = true
  tenant_id                   = var.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"
}
