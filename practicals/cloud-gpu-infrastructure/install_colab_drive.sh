#!/usr/bin/env bash

set -euo pipefail

REMOTE_NAME="gdrive"
MOUNT_POINT="$HOME/gdrive"
COLAB_PATH="/content/drive/MyDrive"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

success() {
    echo -e "${GREEN}✓${NC} $1"
}

info() {
    echo -e "${BLUE}==>${NC} $1"
}

warn() {
    echo -e "${YELLOW}!${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

echo
echo "==============================================="
echo " Google Colab Local Runtime Drive Installer"
echo "==============================================="
echo

##########################################
# Check Ubuntu
##########################################

if ! command -v apt >/dev/null 2>&1; then
    error "This installer currently supports Ubuntu/Debian only."
    exit 1
fi

##########################################
# Install rclone
##########################################

info "Checking rclone..."

if ! command -v rclone >/dev/null 2>&1; then

    warn "rclone is not installed."

    read -rp "Install it now? [Y/n]: " ans
    ans=${ans:-Y}

    if [[ "$ans" =~ ^[Yy]$ ]]; then
        sudo apt update
        sudo apt install -y rclone
        success "rclone installed."
    else
        error "Cannot continue without rclone."
        exit 1
    fi

else
    success "rclone already installed."
fi

##########################################
# Configure Google Drive
##########################################

info "Checking Google Drive remote..."

if ! rclone listremotes | grep -qx "${REMOTE_NAME}:"; then

    warn "Google Drive remote '${REMOTE_NAME}' not found."

    cat <<EOF

The rclone configuration wizard will open.

Choose:

  n                     New remote
  Name                  gdrive
  Storage               drive
  Client ID             <Press Enter>
  Client Secret         <Press Enter>
  Scope                 1 (Full Access)
  Service Account       <Press Enter>
  Advanced Config       n
  Auto Config           y
  Shared Drive          n (unless you use one)
  Save                  y

A browser will open for Google authentication.

EOF

    read -rp "Press Enter to launch rclone config..."

    rclone config

else
    success "Google Drive already configured."
fi

##########################################
# Create mount point
##########################################

info "Preparing mount directory..."

mkdir -p "$MOUNT_POINT"

success "$MOUNT_POINT ready."

##########################################
# Mount Drive
##########################################

info "Checking Drive mount..."

if mountpoint -q "$MOUNT_POINT"; then

    success "Google Drive already mounted."

else

    info "Mounting Google Drive..."

    rclone mount "${REMOTE_NAME}:" "$MOUNT_POINT" \
        --daemon \
        --vfs-cache-mode writes

    sleep 3

    if mountpoint -q "$MOUNT_POINT"; then
        success "Drive mounted."
    else
        error "Mount failed."
        exit 1
    fi

fi

##########################################
# Create Colab directory
##########################################

info "Preparing Colab directory..."

sudo mkdir -p /content/drive
sudo mkdir -p "$COLAB_PATH"

##########################################
# Bind mount
##########################################

info "Checking bind mount..."

if mountpoint -q "$COLAB_PATH"; then

    success "Bind mount already exists."

else

    sudo mount --bind "$MOUNT_POINT" "$COLAB_PATH"

    success "Bind mount created."

fi

##########################################
# Verification
##########################################

info "Verifying installation..."

echo

echo "Google Drive:"
ls "$MOUNT_POINT" | head

echo

echo "Colab Path:"
ls "$COLAB_PATH" | head

echo

success "Installation completed successfully."

cat <<EOF

Your notebooks can now use:

    /content/drive/MyDrive

exactly as they do on hosted Google Colab.

No code changes are required.

EOF