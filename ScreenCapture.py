# -*- coding: utf-8 -*-

import subprocess
from PIL import Image

#Get the iphone source info
'''output = subprocess.check_output([
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
])'''

#Get the iphone source info
window_id = subprocess.check_output([
    './GetWindowID',
    'Reflector 3',
    'Max Boksem’s iPhone'
    ])

print(window_id)

#Save the image
subprocess.call([
    'screencapture',
    '-x',
    '-r',
    '-o',
    '-l{}'.format(window_id),
    'screenshot.png'
])
