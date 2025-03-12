# 使用 Python 3.9 作為基底映像
FROM python:3.9

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install -r requirements.txt

# 複製專案程式碼
COPY . .

# 啟動 Flask API
CMD ["python", "app.py"]
