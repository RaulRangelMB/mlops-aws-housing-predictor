# Use the official AWS Lambda base image for Python 3.12
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements-backend.txt dependency list into the Lambda environment
COPY requirements-backend.txt ${LAMBDA_TASK_ROOT}/requirements.txt

# Install Python dependencies directly into the container task root
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copy the modularized source modules from src/ into the container
# This unpacks app.py and predictor.py as flat files inside ${LAMBDA_TASK_ROOT}
COPY src/ ${LAMBDA_TASK_ROOT}/

# Add the trained model file into the container.
COPY models/model.joblib ${LAMBDA_TASK_ROOT}/

# Point AWS Lambda to entrypoint handler function
CMD [ "app.lambda_handler" ]