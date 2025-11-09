#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Omarchpods Installer ===${NC}\n"

if [ ! -f /etc/arch-release ]; then
    echo -e "${RED}Error: This script is designed for Arch Linux${NC}"
    exit 1
fi

if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}Error: Do not run this script as root${NC}"
    echo "The script will request sudo privileges when needed."
    exit 1
fi

echo -e "${YELLOW}Installing system dependencies...${NC}"
sudo pacman -S --needed --noconfirm base-devel cmake bluez python git

echo -e "${YELLOW}Building Omarchpods package...${NC}"
makepkg -si --noconfirm

echo -e "${YELLOW}Setting up Omarchpods Core service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable omarchpods.service
sudo systemctl start omarchpods.service

if systemctl is-active --quiet omarchpods.service; then
    echo -e "${GREEN}✓ Omarchpods Core service is running${NC}"
else
    echo -e "${RED}✗ Omarchpods Core service failed to start${NC}"
    echo "Check logs with: journalctl -u magicpods.service -f"
    exit 1
fi

echo -e "\n${GREEN}=== Installation Complete ===${NC}"
echo -e "Check service status: ${YELLOW}systemctl status omarchpods.service${NC}"
echo -e "Launch UI with: ${YELLOW}omarchy-launch-omarchpods${NC}"

