FROM python:3.12.0b2-slim-buster
WORKDIR /Users/shailendrasingh/Desktop/Git_Desktop/MLOps/docker_demo
COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python3", "-m", "flask", "--app", "loan_app.py", "run", "--host=0.0.0.0" ]