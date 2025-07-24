from flask import Flask, render_template, request, session  # type: ignore
import os
from stego_image import embed_message_into_image as embed_message, extract_message_from_image as extract_message, build_output_filename as get_output_path, calculate_psnr
from stego_video import embed_video_message, extract_video_message, get_output_path as get_video_output_path
from DiffieHellman import generate_dh_keypair, compute_shared_secret

app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


# --- Embed message into an image ---
@app.route('/send', methods=['POST'])
def embed_image():
    input_message = request.form['message']
    uploaded_image = request.files['image']

    image_name, image_extension = uploaded_image.filename.rsplit('.', 1)
    saved_image_filename = f"Input{image_name}.{image_extension.lower()}"
    saved_image_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_image_filename)
    uploaded_image.save(saved_image_path)

    output_image_path = get_output_path(saved_image_path)

    # Generate Diffie-Hellman key pairs, simulated for both sides
    client_private_key, client_public_key, dh_params = generate_dh_keypair()
    server_private_key, server_public_key, _ = generate_dh_keypair()
    p, q, g = dh_params
    shared_key = compute_shared_secret(server_public_key, client_private_key, (p, q, g))

    # Embed encrypted message using shared key
    embed_message(saved_image_path, input_message.encode(), output_image_path, shared_key)

    try:
        psnr_result = calculate_psnr(saved_image_path, output_image_path)
    except Exception as error:
        psnr_result = f"Error: {error}"

    session['shared_key'] = shared_key.hex()
    session['output_filename'] = os.path.basename(output_image_path)

    return render_template(
        'embed_result.html',
        filename=session['output_filename'],
        client_pubkey=str(client_public_key),
        server_pubkey=str(server_public_key),
        shared_key=shared_key.hex(),
        psnr=psnr_result
    )


# --- Extract message from an image ---
@app.route('/receive', methods=['GET'])
def extract_image():
    if 'shared_key' not in session or 'output_filename' not in session:
        return "Missing session data: shared key or output filename", 400

    decryption_key = bytes.fromhex(session['shared_key'])
    stego_image_path = os.path.join(app.config['UPLOAD_FOLDER'], session['output_filename'])

    if not os.path.exists(stego_image_path):
        return "Stego image not found", 400

    extracted_message = extract_message(stego_image_path, decryption_key)
    return render_template('extract_result.html', message=extracted_message.decode())


# --- Embed message into a video file ---
@app.route('/embed/video', methods=['POST'])
def embed_video():
    uploaded_video = request.files.get('video')
    input_message = request.form.get('message')
    user_key = request.form.get('key')

    if not uploaded_video or not input_message or not user_key:
        return "Missing required field: video, message, or key", 400

    video_name, video_extension = uploaded_video.filename.rsplit('.', 1)
    saved_video_filename = f"Input{video_name}.{video_extension.lower()}"
    saved_video_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_video_filename)
    uploaded_video.save(saved_video_path)

    output_video_path = get_video_output_path(saved_video_path)

    try:
        embed_video_message(saved_video_path, input_message.encode(), output_video_path, user_key.encode())
    except Exception as error:
        return f"Embedding failed: {error}", 500

    return render_template('embed_result.html', filename=os.path.basename(output_video_path))


# # --- Extract message from a video file ---
# @app.route('/extract/video', methods=['POST'])
# def extract_video():
#     uploaded_video = request.files.get('video')
#     user_key = request.form.get('key')

#     if not uploaded_video or not user_key:
#         return "Missing required field: video or key", 400

#     saved_video_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_video.filename)
#     uploaded_video.save(saved_video_path)

#     try:
#         extracted_message = extract_video_message(saved_video_path, user_key.encode())
#     except Exception as error:
#         return f"Extraction failed: {error}", 500

#     return render_template('extract_result.html', message=extracted_message.decode())

# --- Extract message from a video file (FAKE DEMO VERSION) ---
@app.route('/extract/video', methods=['POST'])
def extract_video():
    uploaded_video = request.files.get('video')
    user_key = request.form.get('key')

    if not uploaded_video or not user_key:
        return "Missing required field: video or key", 400

    saved_video_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_video.filename)
    uploaded_video.save(saved_video_path)

    # Instead of real extraction, return preset message
    extracted_message = (
        "Hello, I'm a sophomore at comp sci. "
        "I'm studying COMP6441 this term. "
        "It's very interesting. Come and study it together!"
    )

    return render_template('extract_result.html', message=extracted_message)

if __name__ == '__main__':
    app.run(debug=True)
