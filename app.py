from flask import Flask, render_template, request, send_file, jsonify
import os
import numpy as np
import cv2 as cv
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Use directory of this script as base path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the model once at startup
numpy_file = np.load(os.path.join(BASE_DIR, 'pts_in_hull.npy'))
Caffe_net = cv.dnn.readNetFromCaffe(
    os.path.join(BASE_DIR, "models", "colorization_deploy_v2.prototxt"),
    os.path.join(BASE_DIR, "models", "colorization_release_v2.caffemodel")
)
numpy_file = numpy_file.transpose().reshape(2, 313, 1, 1)
Caffe_net.getLayer(Caffe_net.getLayerId('class8_ab')).blobs = [numpy_file.astype(np.float32)]
Caffe_net.getLayer(Caffe_net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]

def colorize_image(image_bytes):
    """Colorize a black and white image"""
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv.imdecode(nparr, cv.IMREAD_COLOR)
    
    if frame is None:
        raise ValueError("Invalid image")
    
    # Process the image
    input_width = 224
    input_height = 224
    rgb_img = (frame[:,:,[2, 1, 0]] * 1.0 / 255).astype(np.float32)
    lab_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2Lab)
    l_channel = lab_img[:,:,0]
    l_channel_resize = cv.resize(l_channel, (input_width, input_height))
    l_channel_resize -= 50
    
    Caffe_net.setInput(cv.dnn.blobFromImage(l_channel_resize))
    ab_channel = Caffe_net.forward()[0,:,:,:].transpose((1,2,0))
    
    (original_height, original_width) = rgb_img.shape[:2]
    ab_channel_us = cv.resize(ab_channel, (original_width, original_height))
    lab_output = np.concatenate((l_channel[:,:,np.newaxis], ab_channel_us), axis=2)
    bgr_output = np.clip(cv.cvtColor(lab_output, cv.COLOR_Lab2BGR), 0, 1)
    
    # Convert to bytes
    result_img = (bgr_output * 255).astype(np.uint8)
    _, buffer = cv.imencode('.png', result_img)
    return buffer.tobytes()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy", "service": "Mono2Color"}), 200

@app.route('/colorize', methods=['POST'])
def colorize():
    if 'image' not in request.files:
        return 'No image uploaded', 400
    
    file = request.files['image']
    if file.filename == '':
        return 'No image selected', 400
    
    if file:
        try:
            # Read the image
            image_bytes = file.read()
            
            # Colorize the image
            colorized_bytes = colorize_image(image_bytes)
            
            # Return the colorized image
            return send_file(
                io.BytesIO(colorized_bytes),
                mimetype='image/png',
                as_attachment=False,
                download_name='colorized.png'
            )
        except Exception as e:
            return f'Error processing image: {str(e)}', 500

if __name__ == '__main__':
    # Use PORT environment variable for Render deployment
    port = int(os.environ.get('PORT', 5000))
    # Use gunicorn in production, fallback to Flask dev server locally
    app.run(host='0.0.0.0', port=port)
