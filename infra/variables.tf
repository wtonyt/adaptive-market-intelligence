variable "location" {
  default = "East US"
}

variable "resource_group_name" {
  default = "market-ml-rg"
}

variable "container_app_name" {
  default = "market-ml-api"
}

variable "acr_name" {
  default = "marketmlacr123" # must be globally unique
}

variable "polygon_api_key" {
  type      = string
  sensitive = true
}
