# 1. ベースとなるPythonイメージを指定
FROM python:3.10-slim

# 2. 作業ディレクトリを設定
WORKDIR /app

# 3. 高速インストーラ「uv」をインストール
# uv自身はpipでインストールする
RUN pip install uv

# 4. 必要なライブラリをインストール
COPY requirements.txt .

# --system : venv を作らず、コンテナのグローバル環境にインストール
# --no-cache : Dockerビルドキャッシュを効率化
RUN uv pip install --system --no-cache -r requirements.txt

# 5. PCのコードをコンテナにコピー
COPY . .

# 6. コンテナ起動時に実行するコマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]