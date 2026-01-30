#!/bin/bash

echo "╔═══════════════════════════════════╗"
echo "║     NET TOOL SETUP WIZARD         ║"
echo "╚═══════════════════════════════════╝"
echo ""
echo "[*] Making script executable..."
chmod +x net_tool.py

echo "[*] Creating shortcut 'nettool'..."
echo "alias nettool='python $PWD/net_tool.py'" >> ~/.bashrc
echo "alias connect='python $PWD/net_tool.py'" >> ~/.bashrc

echo ""
echo "------------------------------------------------"
echo "[+] SUCCESS!"
echo "------------------------------------------------"
echo "1. Please restart Termux app completely."
echo "2. After restart, you can just type 'nettool' or 'connect' to start!"
echo "------------------------------------------------"
