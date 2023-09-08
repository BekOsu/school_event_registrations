# Final image.
FROM python:3.9.12-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential=12.6 \
  git=1:2.20.* \
  curl=* \
  libssl-dev=* \
  libssl1.1 \
  unzip=* \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /event_registration

# Copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt /event_registration/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files
COPY . /event_registration/



