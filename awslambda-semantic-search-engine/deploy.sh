# Build the docker image
docker build -t  awslambda-semantic-search-engine .

# Create a ECR repository
aws ecr create-repository --repository-name awslambda-semantic-search-engine --image-scanning-configuration scanOnPush=true --region ap-south-1

# Tag the image to match the repository name
docker tag awslambda-semantic-search-engine:latest 759125962999.dkr.ecr.ap-south-1.amazonaws.com/awslambda-semantic-search-engine:latest

# Register docker to ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 759125962999.dkr.ecr.ap-south-1.amazonaws.com

# Push the image to ECR
docker push 759125962999.dkr.ecr.ap-south-1.amazonaws.com/awslambda-semantic-search-engine:latest