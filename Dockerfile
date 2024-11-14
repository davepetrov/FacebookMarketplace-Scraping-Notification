FROM amazon/aws-lambda-python:3.12

# Install dependencies
RUN yum install -y unzip curl jq

# Copy and make the installer script executable
COPY ./chrome-installer.sh ./chrome-installer.sh
RUN chmod +x ./chrome-installer.sh
RUN ./chrome-installer.sh
RUN rm ./chrome-installer.sh

# Install Chrome dependencies
RUN yum install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY src/ ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]
