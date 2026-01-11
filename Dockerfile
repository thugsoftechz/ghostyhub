FROM archlinux:base-devel

# Update mirrorlist and system
RUN pacman -Sy --noconfirm archlinux-keyring && \
    pacman -Syu --noconfirm

# Install dependencies
RUN pacman -S --noconfirm \
    archiso \
    git \
    python \
    python-pip \
    dosfstools \
    e2fsprogs \
    squashfs-tools \
    libisoburn \
    mtools

WORKDIR /app

# The user will mount the repo here
CMD ["python3", "build.py", "--build"]
