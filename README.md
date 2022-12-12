# audiolizr

Audiolizr (*a contraction of **audio** and **analyzer***) is a BentoML service that transcribes Youtube videos and extracts the following metadata from them: 
- keywords and topics using the Yake algorithm
- a generated summary using the T5 algorithm
- named entities (people's name, locations, products, organizations, etc.) using spaCy

This service is deployed on AWS EC2 on a GPU-powered [g4dn.xlarge](https://aws.amazon.com/fr/ec2/instance-types/g4/) instance.

<img src="./images/audiolizr.png">

### Dependencies

- [pytube](https://github.com/pytube/pytube) 
- [whisper](https://github.com/openai/whisper)
- [Yake](https://github.com/LIAAD/yake) 
- [spaCy](https://github.com/explosion/spaCy)
- [transformers](https://github.com/huggingface/transformers)


### Run locally

If you don't have the dependencies installed on your computer and want to create a fresh clean environment, run the following commands

```
cd audiolizr/
pipenv install 
pipenv shell
```

Serve in development mode

```
cd src/
bentoml serve service:svc --reload
```

Serve in production mode

```
cd src/
bentoml serve service:svc --production --api-workers 2
```

To prepare the deployment, build the bento

```
cd src/
bentoml build
```

```
[nltk_data] Downloading package punkt to
[nltk_data]     /Users/ahmedbesbes/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
Building BentoML service "speech_to_text_pipeline:m57a6etzlg4imhqa" from build context "/Users/ahmedbesbes/Documents/perso/whisper/src".

██████╗░███████╗███╗░░██╗████████╗░█████╗░███╗░░░███╗██╗░░░░░
██╔══██╗██╔════╝████╗░██║╚══██╔══╝██╔══██╗████╗░████║██║░░░░░
██████╦╝█████╗░░██╔██╗██║░░░██║░░░██║░░██║██╔████╔██║██║░░░░░
██╔══██╗██╔══╝░░██║╚████║░░░██║░░░██║░░██║██║╚██╔╝██║██║░░░░░
██████╦╝███████╗██║░╚███║░░░██║░░░╚█████╔╝██║░╚═╝░██║███████╗
╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░░╚════╝░╚═╝░░░░░╚═╝╚══════╝

Successfully built Bento(tag="speech_to_text_pipeline:m57a6etzlg4imhqa").
```

Containerize the bento to build a docker image

```shell
bentoml containerize speech_to_text_pipeline
```

```shell
Building OCI-compliant image for speech_to_text_pipeline:m57a6etzlg4imhqa with docker

[+] Building 30.7s (20/20) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                         0.0s
 => => transferring dockerfile: 2.52kB                                                                                                                                       0.0s
 => [internal] load .dockerignore                                                                                                                                            0.0s
 => => transferring context: 2B                                                                                                                                              0.0s
 => [internal] load metadata for docker.io/nvidia/cuda:11.6.2-cudnn8-runtime-ubuntu20.04                                                                                     1.1s
 => [base-container  1/15] FROM docker.io/nvidia/cuda:11.6.2-cudnn8-runtime-ubuntu20.04@sha256:812fe80b7123467f5d6c746bd5d7cbd3b96f385c3c6a57a532b21617ad433858              0.0s
 => [internal] load build context                                                                                                                                            0.0s
 => => transferring context: 24.82kB                                                                                                                                         0.0s
 => CACHED [base-container  2/15] RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache     0.0s
 => CACHED [base-container  3/15] RUN --mount=type=cache,target=/var/lib/apt --mount=type=cache,target=/var/cache/apt set -eux &&     apt-get update -y &&     apt-get inst  0.0s
 => CACHED [base-container  4/15] RUN --mount=type=cache,target=/var/lib/apt --mount=type=cache,target=/var/cache/apt     set -eux &&     apt-get install -y --no-install-r  0.0s
 => CACHED [base-container  5/15] RUN ln -sf /usr/bin/python3.9 /usr/bin/python3 &&     ln -sf /usr/bin/pip3.9 /usr/bin/pip3                                                 0.0s
 => CACHED [base-container  6/15] RUN curl -O https://bootstrap.pypa.io/get-pip.py &&     python3 get-pip.py &&     rm -rf get-pip.py                                        0.0s
 => CACHED [base-container  7/15] RUN groupadd -g 1034 -o bentoml && useradd -m -u 1034 -g 1034 -o -r bentoml                                                                0.0s
 => CACHED [base-container  8/15] RUN mkdir /home/bentoml/bento && chown bentoml:bentoml /home/bentoml/bento -R                                                              0.0s
 => CACHED [base-container  9/15] WORKDIR /home/bentoml/bento                                                                                                                0.0s
 => [base-container 10/15] COPY --chown=bentoml:bentoml . ./                                                                                                                 0.0s
 => [base-container 11/15] RUN --mount=type=cache,target=/root/.cache/pip bash -euxo pipefail /home/bentoml/bento/env/python/install.sh                                     20.6s
 => [base-container 12/15] RUN chmod +x /home/bentoml/bento/env/docker/setup_script                                                                                          0.2s
 => [base-container 13/15] RUN /home/bentoml/bento/env/docker/setup_script                                                                                                   6.1s
 => [base-container 14/15] RUN rm -rf /var/lib/{apt,cache,log}                                                                                                               0.2s
 => [base-container 15/15] RUN chmod +x /home/bentoml/bento/env/docker/entrypoint.sh                                                                                         0.2s
 => exporting to image                                                                                                                                                       2.2s
 => => exporting layers                                                                                                                                                      2.2s
 => => writing image sha256:a08cdb9a3818379359500fe78c0af72a38516cde471e8f6ca1c26e177a7f99c1                                                                                 0.0s
 => => naming to docker.io/library/speech_to_text_pipeline:m57a6etzlg4imhqa                                                                                                  0.0s
Successfully built Bento container for "speech_to_text_pipeline" with tag(s) "speech_to_text_pipeline:m57a6etzlg4imhqa"
To run your newly built Bento container, use 'speech_to_text_pipeline:m57a6etzlg4imhqa' as a tag and pass it to 'docker run'. For example:
    docker run -it --rm -p 3000:3000 speech_to_text_pipeline:m57a6etzlg4imhqa serve --production
```

Run the service from the build docker image

```
docker run -it --rm -p 3000:3000 speech_to_text_pipeline:m57a6etzlg4imhqa serve --production --api-workers 2
```

### Deploy to EC2