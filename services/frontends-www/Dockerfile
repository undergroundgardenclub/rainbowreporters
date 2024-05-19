FROM node:20.5.0

# Root
WORKDIR /usr/src/frontends-www

# Install packages with yarn from npm registry (yarn needs .npmrc for auth)
# TODO: rm .npmrc after yarn install
COPY package*.json ./
RUN npm install

# Copy src
COPY . .

# Build
RUN npm run build

# Start
EXPOSE 8000
CMD ["npm", "run", "start"]
