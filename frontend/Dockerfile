FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./


RUN apk add --no-cache python3 make g++ pkgconfig pixman-dev cairo-dev pango-dev jpeg-dev giflib-dev \
    && npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80