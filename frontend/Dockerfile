# Use the latest Node.js version
FROM node:alpine as build

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

# Production stage
FROM node:alpine

WORKDIR /app

# Copy build artifacts and necessary files
COPY --from=build /app/build ./build
COPY --from=build /app/package.json ./
COPY --from=build /app/node_modules ./node_modules

# Install only production dependencies
RUN npm ci --only=production

EXPOSE 3000

# Run the app
CMD ["node", "build"]