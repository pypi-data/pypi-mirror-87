FROM taktile/base-serving-api-arrow:0.3.4

ENV APPDIR /app

WORKDIR $APPDIR

ARG REPOSITORY_ID
ENV REPOSITORY_ID=$REPOSITORY_ID

ENV TAKTILE_API_URL="https://taktile-api.stg.taktile.com"

# Copy code and assets for running the application
COPY ./samples ${APPDIR}/src


