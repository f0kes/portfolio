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
# Note: We're copying the entire app directory as SvelteKit's output location can vary
COPY --from=build /app ./

# Install only production dependencies
RUN npm ci --only=production

EXPOSE 3000

# Run the app
CMD ["npm", "run", "start"]
