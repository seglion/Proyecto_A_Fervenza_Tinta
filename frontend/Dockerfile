# frontend/Dockerfile

# 1. Usar una imagen base de Node.js
FROM node:20-alpine

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar los ficheros de dependencias e instalarlas
# Esto se hace primero para aprovechar la caché de Docker
COPY package*.json ./
RUN npm install

# 4. Copiar el resto del código fuente de la aplicación
COPY . .

# 5. Exponer el puerto del servidor de desarrollo
EXPOSE 5173

# 6. El comando para iniciar la aplicación en modo desarrollo
CMD ["npm", "run", "dev"]