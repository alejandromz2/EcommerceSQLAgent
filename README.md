# Ecommerce SQL Agent Deployment Guide

Este proyecto implementa un **Agente de Ecommerce** que realiza consultas SQL mediante un API Flask y se conecta a un bot de Telegram. La aplicación está diseñada para ser desplegada en Google Cloud Run utilizando Terraform.

---

## ✨ Requisitos Previos

1. Tener una cuenta en Google Cloud Platform (GCP).  
2. Instalar las siguientes herramientas:
   - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
   - [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
   - [Docker](https://docs.docker.com/get-docker/)
   - [ngrok](https://ngrok.com/) para pruebas locales

3. Asegúrate de incluir este archivo en tu `.gitignore` para evitar exponer tus claves API.

---

## 🕹️ Pruebas Locales

Para probar localmente con Ngrok:

1. Inicia tu servidor localmente en el puerto `5600`.

2. Ejecuta Ngrok para exponer tu API local:
```bash
ngrok http 5600
```

Esto te proporcionará una URL pública, como `https://123.ngrok-free.app`.

3. Configura el webhook de Telegram con la URL pública generada:

```bash
curl -X POST "https://api.telegram.org/bot<TU_TELEGRAM_TOKEN>/setWebhook?url=https://123.ngrok-free.app/webhook"
```

4. Verifica el webhook con:

```bash
curl -X GET "https://api.telegram.org/bot<TU_TELEGRAM_TOKEN>/getWebhookInfo"
```

---

## ☁️ Despliegue en Google Cloud Run

### 1. Iniciar Sesión en GCP
```bash
gcloud auth login
```

### 2. Seleccionar el Proyecto
```bash
gcloud config set project <TU_PROYECTO_ID>
```

### 3. Habilitar los Servicios Necesarios
```bash
gcloud services enable run.googleapis.com

gcloud services enable artifactregistry.googleapis.com

gcloud services enable iam.googleapis.com
```

### 4. Crear el Repositorio en Artifact Registry
```bash
gcloud artifacts repositories create <NOMBRE_DEL_REPOSITORIO> \
  --repository-format=docker \
  --location=<REGION>
```

### 5. Construir y Subir la Imagen Docker

#### Autenticarse en Artifact Registry
```bash
gcloud auth configure-docker <REGION>-docker.pkg.dev
```

#### Construir la Imagen Docker
```bash
docker build -t <REGION>-docker.pkg.dev/<TU_PROYECTO_ID>/<NOMBRE_DEL_REPOSITORIO>/sql-agent-api .
```

#### Subir la Imagen
```bash
docker push <REGION>-docker.pkg.dev/<TU_PROYECTO_ID>/<NOMBRE_DEL_REPOSITORIO>/sql-agent-api
```

---

## 📂 Despliegue con Terraform

### 1. Crea un Directorio en Terraform
```bash
mkdir terraform-cloudrun
```

### 2. Posicionarte en el Directorio de Terraform
```bash
cd terraform-cloudrun
```

### 3. Inicializar Terraform
```bash
terraform init
```

### 4. Autenticarse para la Ejecución
```bash
gcloud auth application-default login
```

### 5. Planificar Cambios
```bash
terraform plan
```

### 6. Aplicar Cambios
```bash
terraform apply -auto-approve
```

### 7. Hacer el Servicio Público
```bash
gcloud run services add-iam-policy-binding <NOMBRE_DEL_SERVICIO> \
    --member="allUsers" \
    --role="roles/run.invoker" \
    --region=<REGION>
```

### 8. Obtener la URL del Servicio
```bash
terraform output cloud_run_url
```

La salida debería ser algo similar a:
```ini
cloud_run_url = "https://<NOMBRE_DEL_SERVICIO>-xxxxx-<REGION>.a.run.app"
```

---

## 📡 Configurar el Webhook en Producción

Una vez que tengas tu URL de Cloud Run, configura el webhook de Telegram:

```bash
curl -X POST "https://api.telegram.org/bot<TU_TELEGRAM_TOKEN>/setWebhook?url=https://<NOMBRE_DEL_SERVICIO>-xxxxx-<REGION>.a.run.app/webhook"
```

Verifica el estado del webhook:
```bash
curl -X GET "https://api.telegram.org/bot<TU_TELEGRAM_TOKEN>/getWebhookInfo"
```
---

## ✨ Resultado Final
- El bot de Telegram responderá a consultas SQL enviadas por los usuarios.  
- El API está desplegado en Google Cloud Run y es accesible públicamente.  
- Todo el proceso de despliegue está automatizado con Terraform.

---

## 🔗 Recursos de Interés
- [Documentación de Cloud Run](https://cloud.google.com/run/docs)  
- [API de Telegram](https://core.telegram.org/bots/api)  
- [Terraform Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)  


✨ **Listo! Ahora tu Agente de Ecommerce SQL está en producción y conectado a Telegram!**
