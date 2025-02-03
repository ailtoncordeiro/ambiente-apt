# Define o provedor da Google Cloud
provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Criação da VPC customizada (rede virtual isolada)
resource "google_compute_network" "corp_net" {
  name                    = "corp-network"
  auto_create_subnetworks = false
}

# Criação de uma sub-rede para o ambiente corporativo
resource "google_compute_subnetwork" "corp_subnet" {
  name          = "corp-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.corp_net.name
}

# Regra de firewall para permitir apenas a comunicação interna entre as VMs
resource "google_compute_firewall" "allow_internal" {
  name    = "allow-internal"
  network = google_compute_network.corp_net.name

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "icmp"
  }

  # Apenas IPs internos da sub-rede terão permissão de comunicação
  source_ranges = ["10.0.0.0/24"]
}

# Regra para permitir acesso RDP
resource "google_compute_firewall" "allow_rdp" {
  name    = "allow-rdp"
  network = google_compute_network.corp_net.name

  allow {
    protocol = "tcp"
    ports    = ["3389"]
  }

  # IP Liberado
  source_ranges = ["177.37.150.212/32"]
}

# Regra para pemitir acesso SSH na máquina atacante
resource "google_compute_firewall" "allow_ssh_attacker" {
  name    = "allow-ssh-attacker"
  network = google_compute_network.corp_net.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["177.37.150.212/32"]

  # Aplica essa regra somente à instância com a tag "ssh-attacker"
  target_tags = ["ssh-attacker"]
}

# Instância Windows para Endpoint
resource "google_compute_instance" "endpoint1" {
  name         = "endpoint1"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    auto_delete = true
    device_name = "endpoint1-instance-disk"

    initialize_params {
      image = "projects/windows-cloud/global/images/windows-server-2025-dc-v20250123"
      size = 50
      type = "pd_balance" 
    }

    mode = "READ_WRITE"

  }

  network_interface {
    network    = google_compute_network.corp_net.name
    subnetwork = google_compute_subnetwork.corp_subnet.name
    
    access_config {
      network_tier = "PREMIUM"
    }
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

}

# Instância Windows para Controlador de Domínio
resource "google_compute_instance" "domain_controller" {
  name         = "domain-controller"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    auto_delete = true
    device_name = "domain_controller-instance-disk"

    initialize_params {
      image = "projects/windows-cloud/global/images/windows-server-2025-dc-v20250123"
      size = 50
      type = "pd_balance" 
    }

    mode = "READ_WRITE"

  }

  network_interface {
    network    = google_compute_network.corp_net.name
    subnetwork = google_compute_subnetwork.corp_subnet.name
    
    access_config {
      network_tier = "PREMIUM"
    }
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }
}

# Instância para Máquina Atacante
resource "google_compute_instance" "attacker" {
  name         = "attacker"
  machine_type = "n1-standard-1"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-11-kali-cloud-amd64-v20230420" 
    }
  }

  network_interface {
    network    = google_compute_network.corp_net.name
    subnetwork = google_compute_subnetwork.corp_subnet.name
    access_config {
      network_tier = "PREMIUM"
    }
  }

  tags = ["ssh-attacker"]

}
