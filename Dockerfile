FROM debian:bookworm

WORKDIR /rtsp-server/

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-gi \
    python3-cairo \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    libgirepository1.0-dev \
    gir1.2-glib-2.0 \
    gir1.2-gst-rtsp-server-1.0 \
    gobject-introspection \
    build-essential \
    cmake \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    ffmpeg \
    wget

COPY . .

CMD ["python3", "main.py"]
