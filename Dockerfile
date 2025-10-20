# Stage 1: Build the frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/hotel-predict-sparkle-main
COPY hotel-predict-sparkle-main/package.json hotel-predict-sparkle-main/package-lock.json ./
# what does the above line do and how?
# It copies the package.json and package-lock.json files from the hotel-predict-sparkle-main directory on the host machine to the current working directory in the Docker image (/app/hotel-predict-sparkle-main).
# explain its sytax
# The syntax is: COPY <source> <destination>
# The source can be a file or directory on the host machine, and the destination is the path in the Docker image where the files will be copied to.
# The . at the end represents
RUN npm ci
COPY hotel-predict-sparkle-main/ ./
RUN npm run build

# Stage 2: Build and run the Python backend
FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
#what does the above two lines do?
# PYTHONDONTWRITEBYTECODE=1 prevents Python from writing .pyc files to disk
# PYTHONUNBUFFERED=1 ensures that Python output is sent straight to the terminal without being buffered


     
# Install OS dependencies for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# No -e flag for production builds
# why?
# The -e flag is used for installing packages in "editable" mode, which is useful during development when you want to make changes to the package and have those changes reflected immediately without needing to reinstall the package.
# The --no-cache-dir option tells pip not to store the downloaded packages in a cache.

# Copy Python application files
COPY . .
# after COPY . .
#RUN python pipeline/training_pipeline.py
RUN python -m pipeline.training_pipeline

#Copy the built frontend artifacts from the frontend-builder stage
#COPY --from=frontend-builder /app/hotel-predict-sparkle-main/dist /app/application/dist
COPY --from=frontend-builder /app/hotel-predict-sparkle-main/dist /app/hotel-predict-sparkle-main/dist
# what is the above line doing?
# It copies the dist folder from the frontend-builder stage to the backend stage
# The dist folder contains the built frontend files (HTML, CSS, JS)
# The backend (Flask app) serves these files to the client
# will the dist folder be auto created if it does not exist in the backend?
# If not, we can create it using RUN mkdir -p /app/hotel-predict-sparkle-main/dist
# but it should be there since we are copying from the frontend-builder stage

# Expose the application port
EXPOSE 5000

# Run the Python application
CMD ["python", "application.py"]

#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "application:app", "--workers", "2", "--threads", "2"]
#-----------------------------------------------------------------------------------------------------------------------
# ---------- Stage 1: Build frontend ----------
#FROM node:18-alpine AS frontend-builder
#WORKDIR /app/hotel-predict-sparkle-main

# copy lock/package first for caching
#COPY hotel-predict-sparkle-main/package.json hotel-predict-sparkle-main/package-lock.json ./
#RUN npm ci --silent

# copy source & build
#COPY hotel-predict-sparkle-main/ ./
#RUN npm run build

# ---------- Stage 2: Runtime (Python) ----------
#FROM python:3.11-slim

# keep python from writing .pyc and make logs unbuffered
#ENV PYTHONDONTWRITEBYTECODE=1 \
#    PYTHONUNBUFFERED=1

#WORKDIR /app

# install system deps needed for some python packages (and building wheels)
#RUN apt-get update \
#    && apt-get install -y --no-install-recommends \
#       build-essential \
#       libgomp1 \
#       curl \
#    && rm -rf /var/lib/apt/lists/*

    #what does the above lines do?
    # It removes the cached package lists to reduce the image size.
    # build-essential is needed to compile some Python packages from source
    # libgomp1 is needed for packages that use OpenMP (like some ML libraries)
    # curl is useful for downloading files (if needed in your app)
    # --no-install-recommends avoids installing unnecessary packages

# copy and install python deps (cache-friendly)
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

# copy only the backend files you need
# (we copy the whole repo for simplicity; later you can be more selective)
#COPY . .

# copy built frontend into the path your Flask app expects
#COPY --from=frontend-builder /app/hotel-predict-sparkle-main/dist /app/hotel-predict-sparkle-main/dist

# run training during build so the trained model is baked into the image
#RUN python pipeline/training_pipeline.py

# expose the port your app listens on (ensure application.py uses the same port)
#EXPOSE 5000

# production-ready server; change to ["python","application.py"] for dev-only
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "application:app", "--workers", "2", "--threads", "2"]
#how does the above line work?
