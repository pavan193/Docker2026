FROM python

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app/
EXPOSE 5000
CMD ["streamlit", "run", "app.py"]