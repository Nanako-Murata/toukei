# ==== ステージ1：ビルド専用の箱(Reactのコードを静的ファイルに変換) ====
FROM node:22-slim AS build

WORKDIR /build

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# ==== ステージ2：配信専用の箱(Nginxという軽量Webサーバーで配信) ====
FROM nginx:alpine

# ★ Azure のヘルスチェックが wget を使うので必須
RUN apk add --no-cache wget

COPY --from=build /build/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
