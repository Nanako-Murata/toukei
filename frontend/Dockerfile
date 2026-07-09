# ==== ステージ1：Reactビルド ====
FROM node:22-slim AS build

WORKDIR /build

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# ==== ステージ2：Nginxで配信 ====
FROM nginx:alpine

RUN apk add --no-cache wget

# Vite は dist フォルダに出力される
COPY --from=build /build/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]