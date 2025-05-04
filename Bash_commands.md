- sudo: execute an action as a superuser (sudo = superuser do)
- In "nano" terminal, M-A = Alt + A, ^J = Ctrl + J

- Transfer a file from windows file to WSL: mkdir -p ~/Downloads
cp /mnt/c/Users/<YourUsername>/Downloads/LM_Studio-0.3.2.AppImage ~/Downloads

- Install and run LM-studio on Linux:
1. sudo apt install -y chromium-sandbox
2. cd ~/Downloado, chmod u+x <lmstudio_file>
3. ./<lmstudio_file> --appimage-extract
4. cd squashfs-root
5. sudo chown root:root chrome-sandbox
6. sudo chmod 4755 chrome-sandbox
7. ./lm-studio : run lmstudio