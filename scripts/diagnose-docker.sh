#!/bin/bash
# Docker diagnostic script

echo "================================"
echo "Docker Diagnostic Tool"
echo "================================"
echo ""

echo "1. Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "   ✓ Docker is installed"
    docker --version
else
    echo "   ✗ Docker is NOT installed"
    echo ""
    echo "Install with:"
    echo "  sudo apt update"
    echo "  sudo apt install docker.io"
    exit 1
fi
echo ""

echo "2. Checking Docker daemon status..."
if systemctl is-active --quiet docker; then
    echo "   ✓ Docker service is active"
else
    echo "   ✗ Docker service is NOT running"
    echo ""
    echo "Try starting it with:"
    echo "  sudo systemctl start docker"
    echo ""
    systemctl status docker --no-pager
fi
echo ""

echo "3. Checking Docker socket..."
if [ -S /var/run/docker.sock ]; then
    echo "   ✓ Docker socket exists"
    ls -la /var/run/docker.sock
else
    echo "   ✗ Docker socket NOT found"
fi
echo ""

echo "4. Checking user permissions..."
if groups | grep -q docker; then
    echo "   ✓ User is in docker group"
else
    echo "   ✗ User is NOT in docker group"
    echo ""
    echo "Add yourself with:"
    echo "  sudo usermod -aG docker $USER"
    echo "  newgrp docker"
fi
echo ""

echo "5. Testing Docker connection..."
if docker info &> /dev/null; then
    echo "   ✓ Docker is accessible"
else
    echo "   ✗ Cannot connect to Docker daemon"
    echo ""
    echo "Error details:"
    docker info 2>&1 | head -5
fi
echo ""

echo "6. Checking docker-compose..."
if command -v docker-compose &> /dev/null; then
    echo "   ✓ docker-compose is installed"
    docker-compose --version
elif docker compose version &> /dev/null; then
    echo "   ✓ docker compose (plugin) is installed"
    docker compose version
else
    echo "   ✗ docker-compose is NOT installed"
    echo ""
    echo "Install with:"
    echo "  sudo apt install docker-compose-plugin"
fi
echo ""

echo "================================"
echo "Summary"
echo "================================"
if docker info &> /dev/null; then
    echo "✓ Docker is working! You can run ./scripts/docker-start.sh"
else
    echo "✗ Docker needs attention. Follow the suggestions above."
fi
echo ""
