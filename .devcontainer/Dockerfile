# Use official Python runtime as base image
FROM python:3.11-bullseye

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Create a non-root user to use
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install Python development tools
RUN pip install --upgrade pip \
    && pip install pylint autopep8 black yapf bandit flake8 mypy pycodestyle pydocstyle pytest

# Create directory for Python utilities
RUN mkdir -p /usr/local/py-utils/bin \
    && ln -s /usr/local/bin/autopep8 /usr/local/py-utils/bin/autopep8 \
    && ln -s /usr/local/bin/black /usr/local/py-utils/bin/black \
    && ln -s /usr/local/bin/yapf /usr/local/py-utils/bin/yapf \
    && ln -s /usr/local/bin/bandit /usr/local/py-utils/bin/bandit \
    && ln -s /usr/local/bin/flake8 /usr/local/py-utils/bin/flake8 \
    && ln -s /usr/local/bin/mypy /usr/local/py-utils/bin/mypy \
    && ln -s /usr/local/bin/pycodestyle /usr/local/py-utils/bin/pycodestyle \
    && ln -s /usr/local/bin/pydocstyle /usr/local/py-utils/bin/pydocstyle \
    && ln -s /usr/local/bin/pylint /usr/local/py-utils/bin/pylint \
    && ln -s /usr/local/bin/pytest /usr/local/py-utils/bin/pytest

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

# Set the default user
USER $USERNAME

