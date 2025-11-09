# 1. ベースとなるNode.jsイメージを指定
FROM node:18-alpine

# 2. 作業ディレクトリを設定
WORKDIR /app

# 3. 依存関係をインストール
COPY package.json package-lock.json ./
RUN npm install

# 4. PCのコードをコンテナにコピー
COPY . .

# 5. 3000番ポートを開放
EXPOSE 3000

# 6. 開発サーバーを起動
CMD ["npm", "run", "dev"]