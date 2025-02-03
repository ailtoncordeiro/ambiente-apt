output "endpoint1_ip" {
  description = "Endereço IP da instância endpoint1"
  value       = google_compute_instance.endpoint1.network_interface[0].access_config[0].nat_ip
}

output "domain_controller_ip" {
  description = "Endereço IP da instância do controlador de domínio"
  value       = google_compute_instance.domain_controller.network_interface[0].access_config[0].nat_ip
}

output "attacker_ip" {
  description = "Endereço IP da instância atacante"
  value       = google_compute_instance.attacker.network_interface[0].access_config[0].nat_ip
}
