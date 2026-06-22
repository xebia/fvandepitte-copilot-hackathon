import qrcode

# Create QR code for the repository URL
url = "https://github.com/xebia/copilot-proximus-hackathon"
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Create image with white background and black QR code
img = qr.make_image(fill_color="black", back_color="white")
img.save("repo-qr-code.png")
