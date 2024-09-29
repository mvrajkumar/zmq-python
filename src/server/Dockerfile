FROM python:latest

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir nibabel pydicom matplotlib pillow med2image
    # Note: we had to merge the two "pip install" package lists here, otherwise
    # the last "pip install" command in the OP may break dependency resolution
    
RUN pip install pyzmq

RUN pip install Flask

ADD pub_server.py /tmp/publisher.py

# Flask Port
EXPOSE 5000

# Zmq Sub Server
EXPOSE 5570

CMD ["python","/tmp/publisher.py"]
