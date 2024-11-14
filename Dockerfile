FROM umihico/aws-lambda-selenium-python:latest

# Set AWS Region
ENV AWS_REGION=us-east-1

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the source code
COPY src/ .

# Set the handler
CMD [ "lambda_function.lambda_handler" ]
