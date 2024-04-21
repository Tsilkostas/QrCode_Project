import qrcode
from io import BytesIO
import base64

def generate_qr_code_image(data):
    """
    Generate a QR code image based on the provided data.

    Parameters:
        data (str): The data to be encoded in the QR code.

    Returns:
        bytes: The bytes of the generated QR code image.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_bytes = BytesIO()
    img.save(img_bytes) 
    img_bytes.seek(0)

    encoded_img = base64.b64encode(img_bytes.read()).decode('utf-8')
    
    return encoded_img
