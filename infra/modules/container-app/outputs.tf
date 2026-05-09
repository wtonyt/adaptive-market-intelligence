output "container_app_id" {
  value = azurerm_container_app.app.id
}

output "fqdn" {
  value = azurerm_container_app.app.latest_revision_fqdn
}