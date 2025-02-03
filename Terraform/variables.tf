variable "project_id" {
  description = "ID do projeto na Google Cloud"
  type        = string
}

variable "region" {
  description = "Região onde as instâncias serão criadas"
  type        = string
  default     = "us-central1"  # ou a região de sua preferência
}

variable "zone" {
  description = "Zona onde as instâncias serão criadas"
  type        = string
  default     = "us-central1-c"
}
