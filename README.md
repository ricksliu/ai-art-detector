# ai-art-detector

Website that detects if artwork is AI-generated. Built using Angular, Django, PyTorch and PostgreSQL.

Deployed using Nginx, Docker and AWS (RDS, EC2, ECR, S3, CloudFront).

# About

AI Art Detector is a web app that lets users upload images and determines if they are AI-generated using machine learning.

The frontend single-page application is built using Angular. The backend is built using Django and is powered by a CNN binary image classifier built using PyTorch.

![Image of the frontend's home page.](docs/frontend-home-page.png)

![Image of the frontend's result page.](docs/frontend-result-page.png)

## Data

The model was trained on ~20k images from a combination of datasets:

- [laion2B-en](https://huggingface.co/datasets/laion/laion2B-en): Subset of LAION-5B, the dataset used to train the original version of the text-to-image model Stable Diffusion.

- [civitai-stable-diffusion-337k](https://huggingface.co/datasets/thefcraft/civitai-stable-diffusion-337k): Dataset of images generated by Stable Diffusion.

- [midjourney-v5-202304-clean](https://huggingface.co/datasets/wanng/midjourney-v5-202304-clean): Dataset of images generated by Midjourney.

## Results

The model performed reasonably well on the test data with a precision of 0.88 and a recall of 0.94.

![Plot of the model's confusion matrix during testing.](docs/model-confusion-matrix.png)

However, the model struggled to generalize  during training and suffered from overfitting, most likely due to the lack of tuning and data.

![Plot of the model's loss vs epoch during training.](docs/model-loss-plot.png)

Detecting AI-generated artwork using AI is probably feasible to do, but this proof-of-concept does not yet have the accuracy required to make it a real service worth using. Creating such a service would require much more technical ML knowledge and a much larger dataset.

# Architecture

## Frontend

- Frontend: Angular
- CDN: CloudFront
- Static Hosting: S3

## Backend

- API: Django (DRF) + PyTorch
- Database: PostgreSQL
- Reverse Proxy: Nginx
- Backend Server: AWS (RDS + EC2 + ECR) + Docker + Gunicorn

# Setup

## Prerequisites

- Node.js
- Python
- Docker
- AWS CLI

## Local Frontend Setup

Install the Angular CLI npm package globally:
```
npm install -g @angular/cli
```

Navigate to the directory:
```
cd src/frontend
```

Install the required npm packages:
```
npm install
```

To start the frontend:
```
ng serve
```

The frontend should now be live at http://localhost:4200.

## Local Backend Setup

Navigate to the directory:
```
cd src/backend/app
```

It is recommended to set up a virtual Python environment.
The following sets up and activates a virtual environment using `venv`:
```
python -m venv venv
venv/scripts/activate
```

Install the required Python packages:
```
pip install -r requirements.txt
```

Set up SQLite:
```
python manage.py makemigrations
python manage.py migrate
```

To start the backend:
```
python manage.py runserver
```

The backend should now be live at http://localhost:8000.

## ML Model Training

Navigate to the directory:
```
cd src/backend/app
```

To download the dataset:
```
python -m data.scripts.get
```
The `-fmetadata` option forces a redownload of the metadata.
The `-fdata` option forces a redownload of the data.

To preprocess the dataset:
```
python -m data.scripts.preprocess
```
The `-multiplecrop` option creates multiple crops of each image.
The `-mirror` option creates a mirror of each image.

To train a new model (this may take a while):
```
python -m data.scripts.train
```

To use the new model with the backend, update the `MODEL_VER` setting in `src/backend/app/settings.py` with the name of the new model.

# Deployment

Frontend deployment is now handled by Jenkins. Backend deployment is still handled manually for now.

## Manual Frontend Deployment (Deprecated)

Navigate to the directory:
```
cd src/frontend
```

Create a production build in `dist/frontend`:
```
ng build --configuration production
```

Deploy the build to S3:
```
aws s3 sync dist/frontend s3://ai-art-detector.ricksliu.dev
```

## Manual Backend Deployment

Navigate to the directory:
```
cd src/backend
```

Build the Docker images:
```
docker-compose -f compose.prod.yaml build
```

Login to the ECR repository if necessary:
```
aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin 310294657566.dkr.ecr.ca-central-1.amazonaws.com
```

Push the Docker images to the ECR repository:
```
docker-compose -f compose.prod.yaml push
```

Copy the secrets over to the EC2 instance:
```
scp -r -i <path-to-pem-cert> env ec2-user@15.156.44.97:ai-art-detector/src/backend/
```

SSH into the EC2 instance:
```
ssh -i <path-to-pem-cert> ec2-user@15.156.44.97
```

Navigate to the project directory and pull the code from GitHub:
```
cd ai-art-detector
git pull
```

Login to the ECR repository if necessary:
```
aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin 310294657566.dkr.ecr.ca-central-1.amazonaws.com
```

Pull the Docker images from the ECR repository:
```
docker pull 310294657566.dkr.ecr.ca-central-1.amazonaws.com/ai-art-detector:app
docker pull 310294657566.dkr.ecr.ca-central-1.amazonaws.com/ai-art-detector:nginx-proxy
```

Navigate to the directory:
```
cd src/backend
```

Stop the containers:
```
docker-compose -f compose.prod.yaml down -v
```

Start the containers:
```
docker-compose -f compose.prod.yaml up -d
```
