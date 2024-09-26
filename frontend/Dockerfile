# Use Node.js LTS version
FROM node:lts-alpine as build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy project files
COPY . .

# Build the app
RUN npm run build

# Serve the app
FROM node:lts-alpine

WORKDIR /app

COPY --from=build /app/build build/
COPY --from=build /app/package.json .
COPY --from=build /app/node_modules node_modules/

EXPOSE 3000

CMD ["node", "build"]