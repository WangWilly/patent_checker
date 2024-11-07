################################################################################
# Base image
FROM node:20.9.0-alpine AS base

################################################################################
# Builder dependencies
FROM base AS builder-deps
WORKDIR /app
RUN apk add --no-cache libc6-compat
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

################################################################################
# Build the source code
FROM base AS builder
WORKDIR /app
COPY --from=builder-deps /app/node_modules ./node_modules/
COPY frontend/ ./
RUN npx expo export -p web

################################################################################
# Runner
FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/dist ./dist

EXPOSE 3000
ENV PORT=3000

CMD npx serve -s dist -l $PORT
