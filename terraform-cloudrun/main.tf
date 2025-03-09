terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.6.0"
}

provider "google" {
  project = "acoustic-env-452102-r3"
  region  = "us-central1"
}

# Servicio 1: API Flask en Cloud Run
resource "google_cloud_run_service" "sql-agent-api" {
  name     = "sql-agent-api"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/acoustic-env-452102-r3/chatbot-repo/sql-agent-api"
        
        ports {
          container_port = 8080
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

output "cloud_run_url" {
  value = google_cloud_run_service.sql-agent-api.status[0].url
}

