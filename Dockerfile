FROM python:3.12

WORKDIR /app

# Copy the entire pyftg directory
COPY pyftg /app/pyftg

# Install requirements from examples folder
RUN pip install -r pyftg/examples/requirements.txt

# Set the working dir to examples folder
WORKDIR /app/pyftg/examples

CMD ["python", "Main_SinglePyAI.py", "--host", "host.docker.internal", "--a2", "myAI"]