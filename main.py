import time
import socketio
from datetime import datetime
from PIL import Image
import requests

# Create a Socket.IO client
sio = socketio.Client()

# Initialize a blank canvas
width, height = 256, 256
canvas = Image.new('RGB', (width, height), 'white')
pixels = canvas.load()

# Discord webhook URL
WEBHOOK_URL = 'https://canary.discord.com/api/webhooks/1312834422357364827/0CGw5wNRlj4S_cENVBRaoEu0umiD6wqp2aEfr__gulc0AdrPxYz1P50eCcvdzhorCg7S'

def save_canvas_as_image():
    # Get the current date and time
    now = datetime.now()
    filename = f"{now.strftime('%d-%m-%Y-%H-%M-%S')}.png"

    # Save the image
    canvas.save(filename)
    print(f"Saved image as {filename}")

    # Send the image to Discord
    send_image_to_discord(filename)

def send_image_to_discord(filename):
    with open(filename, 'rb') as f:
        payload = {
            'file': (filename, f, 'image/png')
        }
        response = requests.post(WEBHOOK_URL, files=payload)
        if response.status_code == 200:
            print(f"Image {filename} sent to Discord successfully")
        else:
            print(f"Failed to send image to Discord: {response.status_code}, {response.text}")

@sio.event
def connect():
    print('Connected to the server')
    sio.emit('requestCanvas')  # Request the entire canvas data

@sio.event
def disconnect():
    print('Disconnected from the server')

@sio.on('canvas')
def on_canvas(canvasData):
    print('Received canvas data')
    draw_canvas(canvasData)
    save_canvas_as_image()
    sio.disconnect()  # Disconnect after receiving and saving the canvas

def draw_canvas(canvasData):
    try:
        for y, row in enumerate(canvasData):
            for x, pixel in enumerate(row):
                r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                pixels[x, y] = (r, g, b)
        print('Canvas drawn')
    except Exception as e:
        print(f"Error drawing canvas: {e}")

def main():
 while True:
  try:
        # Connect to the Socket.IO server
   sio.connect('http://5.59.97.201:6969')

        # Wait for the connection to be established and data to be received
   sio.wait()

        # Wait for 60 seconds before reconnecting
   time.sleep(60)
  except:
   pass
if __name__ == "__main__":
    main()
