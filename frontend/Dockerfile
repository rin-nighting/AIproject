FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./

RUN apk add --no-cache python3 make g++ pkgconfig pixman-dev cairo-dev pango-dev jpeg-dev giflib-dev \
    && npm install \
    && chmod -R +x node_modules/.bin

COPY . .

# 再次修正 .bin 权限
RUN chmod -R +x node_modules/.bin

RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80