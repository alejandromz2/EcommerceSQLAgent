
# 
## Para pruebas locales

Para hacer accesible tu puerto
```sh
ngrok http 5600 
```

Esto te dará un url igual a https://123.ngrok-free.app el cual es accesible gracias a ngrok
Posteriormente tienes que hacer accesible este url por medio de un webhook del api de telegram

```sh
curl -X POST "https://api.telegram.org/bot7935980561:AAFeanQu_2e9giVKRqVM5dovFtO5dtaEC_w/setWebhook?url=https://123.ngrok-free.app/webhook"
```

## Para subir el docker a la nube usando Terraform

### 1. Primero iniciamos sesión en GCP: 

```sh
gcloud auth login
```
### 2. Posteriomente seleccionas el proyecto:

```sh
gcloud config set project TU_PROYECTO_ID
```
### 3. Habilitamos los servicios necesarios:

```sh
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable iam.googleapis.com
```

### 4. Creas un repositorio de imagenes en Artifact Registry 

```sh
gcloud artifacts repositories create chatbot-repo \
  --repository-format=docker \
  --location=us-central1
```

### 5. Construir y subir la imagen Docker

#### Autentificarse en Artifact Registry
```sh
gcloud auth configure-docker us-central1-docker.pkg.dev
```

#### Construir la imagen Docker
```sh
docker build -t us-central1-docker.pkg.dev/TU_PROYECTO_ID/chatbot-repo/sql-agent-api .
```

#### Subir la imagen a Artifact Registry
```sh
docker push us-central1-docker.pkg.dev/TU_PROYECTO_ID/chatbot-repo/sql-agent-api
```


### 6. Inicializar y Aplicar Terraform

#### Posicionarte en la carpeta d terraform-cloudrun
```sh
cd terraform-cloudrun
```
#### Iniciar Terraform
```sh
terraform init
```
#### Realiza esta autentifacion
```sh
gcloud auth application-default login
```
#### Plan te permite ver que cambios se van a aplicar
```sh
terraform apply -var="telegram_token=TU_TELEGRAM_BOT_TOKEN" -var="openai_api_key=TU_OPENAI_API_KEY" -auto-approve
```
#### Aplicas los cambios en terraform
```sh
terraform apply -var="openai_api_key=TU_OPENAI_API_KEY" -auto-approve
```

#### Posteriormente hacemos que el servicio que hemos creado sea publico
```sh
gcloud run services add-iam-policy-binding sql-agent-api \
    --member="allUsers" \
    --role="roles/run.invoker" \
    --region=us-central1
```

#### Realizamos este comando para ver el url del servicio
```sh
  terraform output cloud_run_url
```
#### La respuesta tiene que ser esta:
```ini
cloud_run_url = "https://sql-agent-api-xxxxx-uc.a.run.app"
```

#### Posteriormente tienes que realizar el webhook para que el api de telegram detecte el bot
```sh
curl -X POST "https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=<CLOUD_RUN_URL>/webhook"
```

