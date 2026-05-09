variable "app_name" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "container_app_environment_id" {
  type = string
}

variable "acr_login_server" {
  type = string
}

variable "acr_username" {
  type = string
}

variable "acr_password" {
  type      = string
  sensitive = true
}

variable "image_name" {
  type = string
}

variable "image_tag" {
  type = string
}

variable "cpu" {
  type = number
}

variable "memory" {
  type = string
}

variable "environment_variables" {
  type = map(string)
  default = {}
}

variable "external_enabled" {
  type    = bool
  default = false
}

variable "target_port" {
  type    = number
  default = 8000
}