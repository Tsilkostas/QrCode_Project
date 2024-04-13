import qrcode
from io import BytesIO

def generate_qr_code_image(data):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the image to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    
    return img_bytes.getvalue()
