# docker build -t deep-rock-bot .
# docker stop deep-rock-bot
# docker rm deep-rock-bot
# docker run -d --restart always --name deep-rock-bot -e TZ=America/Denver deep-rock-bot:latest

FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run bot.py when the container launches
CMD ["python", "bot.py"]