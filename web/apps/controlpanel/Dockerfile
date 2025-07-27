FROM node:20-alpine
WORKDIR /app
# Copy the entire monorepo structure
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml ./
COPY packages ./packages
COPY generated ./generated
COPY apps/controlpanel ./apps/controlpanel
# Install dependencies
RUN corepack enable && corepack prepare pnpm@latest --activate
RUN pnpm install
# Set working directory to the controlpanel app
WORKDIR /app/apps/controlpanel
# Start the development server
CMD ["pnpm", "dev"]
