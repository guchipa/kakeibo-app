import os
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, TIMESTAMP, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import time

# .env ファイルから環境変数を読み込む
# (docker-compose.yml で環境変数を渡しているので厳密には不要だが、
# ローカルで直接 main.py を実行する際にも役立つ)
load_dotenv()

# ---------------------------------
# 1. データベース接続設定
# ---------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

# FastAPIがMySQLに接続しにいく
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------------------------------
# 2. テーブルモデル (テーブル設計) の定義
# ---------------------------------
# `transactions` テーブルをPythonのクラスとして定義
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    type = Column(String(10), nullable=False)  # 'expense' or 'income'
    category = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)
    memo = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


# ---------------------------------
# 3. FastAPI アプリケーションの初期化
# ---------------------------------
app = FastAPI()


# ---------------------------------
# 4. データベース接続とテーブル作成
# ---------------------------------
@app.on_event("startup")
def startup_event():
    # アプリ起動時にテーブルが存在しない場合、自動的に作成する
    # DBが起動するまで少し待機する処理（簡易的）
    retries = 5
    while retries > 0:
        try:
            # データベースエンジンに接続を試みる
            with engine.connect() as connection:
                print("Database connection successful!")
                # テーブルを作成
                Base.metadata.create_all(bind=engine)
                print("Tables created successfully (if not exists).")
                break  # 成功したらループを抜ける
        except Exception as e:
            print(f"Database connection failed. Retrying... ({retries} attempts left)")
            print(f"Error: {e}")
            retries -= 1
            time.sleep(5)  # 5秒待って再試行


# ---------------------------------
# 5. 動作確認用のAPIエンドポイント
# ---------------------------------
@app.get("/")
def read_root():
    return {"message": "家計簿アプリのバックエンド (FastAPI) です"}


@app.get("/api/test")
def test_api():
    return {"status": "ok", "message": "APIは正常に動作しています"}
