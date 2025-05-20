# Use official Node.js image
FROM node:20

# Create app directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy app source
COPY . .

# Build the app for production
RUN npm run build

# Serve with a lightweight HTTP server
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "4173"]

EXPOSE 4173
