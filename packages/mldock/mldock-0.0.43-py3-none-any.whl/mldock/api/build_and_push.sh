#!/usr/bin/env bash

# This script shows how to build the Docker image and push it to ECR to be ready for use
# by SageMaker.

# The argument to this script is the image name. This will be used as the image on the local
# machine and combined with the account and region to form the repository name for ECR.
IMAGE_NAME=$1
BASE_PATH=$2
ASSERTS_DIR=$3
MODULE_PATH=$4
TARGET_DIR_NAME=$5
REQUIREMENTS_FILE_PATH=$6

if [ "$IMAGE_NAME" == "" ]
then
    echo "Usage: $0 <image-name>"
    exit 1
fi

# Get the account number associated with the current IAM credentials
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
echo "account=$ACCOUNT"
if [ $? -ne 0 ]
then
    exit 255
fi


# Get the region defined in the current configuration (default to us-west-2 if none defined)
REGION=$(aws configure get region)
REGION=${REGION:-us-west-1}
echo "region=$REGION"

ECR_REPOSITORY="${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com"
ECR_IMAGE="${ECR_REPOSITORY}/${IMAGE_NAME}:latest"

echo "ECR name = $ECR_IMAGE"
# If the repository doesn't exist in ECR, create it.

aws ecr describe-repositories --repository-names "${IMAGE_NAME}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${IMAGE_NAME}" > /dev/null
fi

# Get the login command from ECR and execute it directly
$(aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_REPOSITORY})

# Build the docker image locally with the image name and then push it to ECR
# with the full name.

docker build \
-f ${ASSETS_DIR}/Dockerfile \
-t ${IMAGE_NAME} \
${BASE_PATH} \
--build-arg module_path=${MODULE_PATH} \
--build-arg target_dir_name=${TARGET_DIR_NAME} \
--build-arg requirements_file_path=${REQUIREMENTS_FILE_PATH}

docker tag ${IMAGE_NAME} ${ECR_IMAGE}
docker push ${ECR_IMAGE}
