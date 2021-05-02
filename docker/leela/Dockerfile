FROM nvidia/cuda:10.0-cudnn7-devel

RUN apt-get update && apt-get dist-upgrade -y && apt clean all
RUN apt-get update && apt-get install -y curl wget supervisor git clang-6.0 ninja-build protobuf-compiler libprotobuf-dev python3-pip && apt-get clean all
RUN pip3 install --upgrade pip
RUN pip3 install meson
RUN pip3 install python-chess==0.28.0

RUN mkdir src
WORKDIR src/
COPY . .
RUN pip3 install jupyter
WORKDIR /src/notebooks
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
RUN pip3 install psycopg2-binary
RUN pip3 install redis==3.5.2
RUN pip3 install rq==1.5.2
RUN pip3 install rq-dashboard
#RUN pip3 install numpy
#RUN pip3 install pillow
#RUN pip3 install matplotlib
#RUN pip3 install scipy
#RUN pip3 install tensorflow

ENTRYPOINT ["/usr/bin/tini", "--"]


RUN mkdir /lczero && \
    cd ~ && \
    git clone -b release/0.21 --recurse-submodules https://github.com/LeelaChessZero/lc0.git && \
    cd lc0 &&\
    ./build.sh

#RUN mkdir /lczero && \
#    cd ~ && \
#    git clone -b release/0.26 --recurse-submodules https://github.com/LeelaChessZero/lc0.git && \
#    cd lc0 &&\
#    ./build.sh

RUN cp /root/lc0/build/release/lc0 /lczero && \
    # cp ../LS15-20x256SE-jj-9-75000000.pb /lczero/ && \ (still having trouble with larger nets)
    file /lczero/lc0 && \
    chmod +x /lczero/lc0

RUN cd /lczero && \
    wget https://github.com/LeelaChessZero/lczero-client/releases/download/v29/lc0-training-client-linux && \
    chmod +x lc0-training-client-linux && \
    wget http://storage.lczero.org/files/networks-contrib/J20-460
    # wget http://storage.lczero.org/files/networks-contrib/J94-130 (I had some trouble getting the larger nets working)

RUN mkdir /Stockfish && \
    cd ~ && \
    git clone https://github.com/official-stockfish/Stockfish.git &&\
    cd Stockfish &&\
    cd src &&\
    make help &&\
    make net &&\
    make build ARCH=x86-64-modern

COPY supervisord.conf /etc/supervisor/conf.d/
COPY settings.json /lczero/settings.json
RUN service supervisor start

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]


