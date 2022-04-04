FROM python:3.10.4-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apk add python3-dev py3-setuptools gcc linux-headers libc-dev
RUN apk add tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./main.py"]
