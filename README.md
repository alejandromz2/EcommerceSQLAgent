
## Para pruebas locales

Para hacer accesible tu puerto
sh
ngrok http 5600 

Esto te dará un url igual a https://123.ngrok-free.app el cual es accesible gracias a ngrok
Posteriormente tienes que hacer accesible este url por medio de un webhook del api de telegram

sh
curl -X POST "https://api.telegram.org/bot7935980561:AAFeanQu_2e9giVKRqVM5dovFtO5dtaEC_w/setWebhook?url=https://123.ngrok-free.app/webhook"


# Para subir el docker a la nube usando Terraform

1. Primero iniciamos sesión en GCP: 

sh
gcloud auth login

2. Posteriomente seleccionas el proyecto:

sh
gcloud config set project TU_PROYECTO_ID


