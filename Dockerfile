FROM amazon/aws-lambda-python:3.12

# Install dependencies
RUN apt-get update && \
    apt-get install -y unzip curl jq

# Copy and make the installer script executable
COPY ./chrome-installer.sh ./chrome-installer.sh
RUN chmod +x ./chrome-installer.sh
RUN ./chrome-installer.sh
RUN rm ./chrome-installer.sh

# Install Chrome dependencies
RUN apt-get install -y \
    atk \
    cups-libs \
    gtk3 \
    libxcomposite1 \
    alsa-lib \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxi6 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    pango1.0-0 \
    at-spi2-core \
    libxt6 \
    xvfb \
    dbus-glib-1 \
    libnss3

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY src/ ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]