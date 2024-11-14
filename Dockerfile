FROM public.ecr.aws/lambda/python:3.11

# Install Chrome and dependencies
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromium.zip" "https://raw.githubusercontent.com/Sparticuz/chromium/v110.0.1/chromium.zip" && \
    curl -Lo "/tmp/chromedriver.zip" "https://raw.githubusercontent.com/Sparticuz/chromium/v110.0.1/chromedriver.zip" && \
    unzip /tmp/chromium.zip -d /opt/ && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    mv /opt/chromium /opt/chrome && \
    chmod 755 /opt/chrome /opt/chromedriver && \
    rm -rf /tmp/chromium.zip /tmp/chromedriver.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy function code
COPY src/ .

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]

# FROM public.ecr.aws/lambda/python:3.9 as stage

# # Hack to install chromium dependencies
# RUN yum install -y -q sudo unzip

# # Find the version of latest stable build of chromium from below
# # https://omahaproxy.appspot.com/
# # Then follow the instructions here in below URL 
# # to download old builds of Chrome/Chromium that are stable
# # Current stable version of Chromium
# ENV CHROMIUM_VERSION=1002910 


# # Install Chromium
# COPY install-browser.sh /tmp/
# RUN /usr/bin/bash /tmp/install-browser.sh

# FROM public.ecr.aws/lambda/python:3.9 as base

# COPY chrome-deps.txt /tmp/
# RUN yum install -y $(cat /tmp/chrome-deps.txt)

# # Install Python dependencies for function
# COPY requirements.txt /tmp/
# RUN python3 -m pip install --upgrade pip -q
# RUN python3 -m pip install -r /tmp/requirements.txt -q 


# COPY --from=stage /opt/chrome /opt/chrome
# COPY --from=stage /opt/chromedriver /opt/chromedriver
# COPY app.py ${LAMBDA_TASK_ROOT}

# CMD [ "app.handler" ]