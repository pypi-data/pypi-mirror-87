FROM taktile/base-serving-api-arrow:latest
ENV APPDIR /app

# Install requirements
COPY ./requirements.txt ${APPDIR}/user_requirements.txt
RUN pip install -r ${APPDIR}/user_requirements.txt

# Copy code and assets for running the application
COPY ./src ${APPDIR}/src
COPY ./assets ${APPDIR}/assets
COPY ./tests ${APPDIR}/user_tests

ARG TKTL_ADMIN_TOKEN
ENV TKTL_ADMIN_TOKEN=$TKTL_ADMIN_TOKEN

RUN git clone https://$TKTL_ADMIN_TOKEN@github.com/taktile-org/taktile-cli.git cli-edge && \
    cd cli-edge && \
    git fetch && \
    pip install -e .

# Run model profile
RUN python ${APPDIR}/profile_endpoints.py
