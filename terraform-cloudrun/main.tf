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
resource "google_cloud_run_service" "chatbot" {
  name     = "sql-agent-api"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/acoustic-env-452102-r3/chatbot-repo/sql-agent-api"
        ports {
          container_port = 5600
        }
        env {
          name  = "OPENAI_API_KEY"
          value = "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"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "null_resource" "set_telegram_webhook" {
  provisioner "local-exec" {
    command = "curl -X POST 'https://api.telegram.org/bot${var.telegram_token}/setWebhook?url=${google_cloud_run_service.sql_agent_api.status[0].url}/webhook'"
  }

  depends_on = [google_cloud_run_service.sql_agent_api]
}


output "cloud_run_url" {
  value = google_cloud_run_service.chatbot.status[0].url
}

