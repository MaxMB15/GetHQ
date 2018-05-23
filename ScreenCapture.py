import subprocess
from PIL import Image

#Get the iphone source info
output = subprocess.check_output([
    'osascript',
    '-e',
    'tell app "Quicktime Player" to id of window 1'
])
window_id = int(output.strip())

#Save the image
subprocess.call([
    'screencapture',
    '-t', 'jpg',
    '-x',
    '-r',
    '-o',
    '-l{}'.format(window_id),
    'screenshot.png'
])