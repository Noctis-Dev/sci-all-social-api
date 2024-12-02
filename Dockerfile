FROM ubuntu:latest
WORKDIR /app

# Install wine
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y wine64 wine32

# Copy the .exe file into the container
COPY dist/main.exe /app/

# Run the .exe file using wine
CMD ["wine", "main.exe"]