output "queue_name" {
  value = azurerm_servicebus_queue.queue.name
}

output "namespace_name" {
  value = azurerm_servicebus_namespace.sb.name
}

output "primary_connection_string" {
  value     = azurerm_servicebus_namespace.sb.default_primary_connection_string
  sensitive = true
}