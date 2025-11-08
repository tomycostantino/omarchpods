#!/bin/bash
# MagicPods Arch Linux installer script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== MagicPods Arch Linux Installer ===${NC}\n"

# Check if running on Arch Linux
if [ ! -f /etc/arch-release ]; then
    echo -e "${RED}Error: This script is designed for Arch Linux${NC}"
    exit 1
fi

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}Error: Do not run this script as root${NC}"
    echo "The script will request sudo privileges when needed."
    exit 1
fi

# Install dependencies
echo -e "${YELLOW}Installing system dependencies...${NC}"
sudo pacman -S --needed --noconfirm base-devel cmake bluez python git

# Build and install the package
echo -e "${YELLOW}Building MagicPods package...${NC}"
# Go to repository root where PKGBUILD is located
cd "$(dirname "$0")/.."
makepkg -si --noconfirm

# Enable and start the service
echo -e "${YELLOW}Setting up MagicPods Core service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable magicpods.service
sudo systemctl start magicpods.service

# Check service status
if systemctl is-active --quiet magicpods.service; then
    echo -e "${GREEN}✓ MagicPods Core service is running${NC}"
else
    echo -e "${RED}✗ MagicPods Core service failed to start${NC}"
    echo "Check logs with: journalctl -u magicpods.service -f"
    exit 1
fi

echo -e "\n${GREEN}=== Installation Complete ===${NC}"
echo -e "Run ${GREEN}magicpods-ui${NC} to launch the user interface"
echo -e "Check service status: ${YELLOW}systemctl status magicpods.service${NC}"
echo -e "View logs: ${YELLOW}journalctl -u magicpods.service -f${NC}"

