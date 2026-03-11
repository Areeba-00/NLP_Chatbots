# ── Frontend Dockerfile ───────────────────────────────────────────
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files first (for caching)
COPY package.json .

# Install dependencies
RUN npm install

# Copy rest of the code
COPY . .

# Expose Vite port
EXPOSE 5173

# Run Vite dev server (accessible outside container)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
