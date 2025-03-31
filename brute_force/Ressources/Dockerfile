# Use Kali Linux as the base image
FROM kalilinux/kali-rolling

# Set non-interactive mode to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install Hydra
RUN apt update && apt install -y hydra && apt clean

COPY 10-million-password-list-top-10000.txt .

CMD ["/bin/bash"]
