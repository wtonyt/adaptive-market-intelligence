output "api_url" {
  value = module.api_service.fqdn
}

output "poller_container_app_id" {
  value = module.poller_service.container_app_id
}

output "service_bus_connection_string" {
  value     = module.service_bus.primary_connection_string
  sensitive = true
}

output "service_bus_queue_name" {
  value = module.service_bus.queue_name
}