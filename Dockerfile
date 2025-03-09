# Usar Python como base
FROM python:3.12-slim

# Establecer el directorio de  trabajo en el contenedor 
WORKDIR /app

# Copiar todo a app
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en Flask
EXPOSE 8080

# Comando para ejecutar Flask
CMD ["python", "api/app.py"]