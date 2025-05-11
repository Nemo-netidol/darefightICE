FROM python:3.12

WORKDIR /app

COPY . .

RUN cd pyftg/examples && pip install -r requirements.txt

RUN pip install typer

CMD ["python", "Main_SinglePyAI.py", "--a2", "myAI"]  


