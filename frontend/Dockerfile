FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./

# 安装构建 canvas 依赖所需的包
RUN apk add --no-cache python3 make g++ \
    && npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80