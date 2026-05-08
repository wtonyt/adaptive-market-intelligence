output "api_url" {
  value = module.api_service.fqdn
}

output "poller_container_app_id" {
  value = module.poller_service.container_app_id
}