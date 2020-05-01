FROM python:3

RUN addgroup -gid 1000 appuser && \
    adduser -uid 1000 --ingroup appuser appuser &&\
    cd /home/appuser &&\
    git clone https://github.com/oSoc19/best &&\    
    cd best &&\
    pip install --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt &&\
    # Give entire home folder to appuser
    chown -R 1000:1000 /home/appuser &&\
    echo done

# You should always create a separate user for Dockerfiles!
 USER appuser




