# Pull the base image with python 3.8 as a runtime for your Lambda
FROM public.ecr.aws/lambda/python:3.8

# Copy the earlier created requirements.txt file to the container
COPY requirements.txt ./

# Install the python requirements from requirements.txt
RUN python3.8 -m pip install -r requirements.txt

# Copy the earlier created app.py file to the container
COPY app.py ./

# Download Universal Encoder Model and store it in a directory
RUN mkdir model
RUN curl -L https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed -o ./model/use4.tar.gz
RUN tar -xf model/use4.tar.gz -C model/
RUN rm -r model/use4.tar.gz

# Set the CMD to your handler
CMD ["app.lambda_handler"]