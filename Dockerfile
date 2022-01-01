FROM public.ecr.aws/lambda/python:3.8 as build
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/96.0.4664.45/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F929511%2Fchrome-linux.zip?alt=media" && \
    curl -Lo "/tmp/Noto_Sans_JP.zip" "https://fonts.google.com/download?family=Noto%20Sans%20JP" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/Noto*.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/

FROM public.ecr.aws/lambda/python:3.8
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y
COPY sls/requirements.txt ./
RUN pip install -r requirements.txt

COPY sls/server.py ./
COPY chromeless/picklelib.py ./
COPY sls/fonts.conf /opt/fonts/
COPY sls/versions/ ./versions/
COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt/
COPY --from=build /opt/NotoSansJP-Regular.otf /opt/fonts/
CMD ["server.handler"]
