import cv2

# Read the QR code image
img = cv2.imread("site.png")

# Initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

# Detect and decode the QR code
data, bbox, straight_qrcode = detector.detectAndDecode(img)

# If there is a QR code
if bbox is not None:
    print(f"QRCode data: {data}")
    
    # Draw bounding box lines
    n_lines = len(bbox)
    for i in range(n_lines):
        # Convert points to integers
        point1 = tuple(map(int, bbox[i][0]))
        point2 = tuple(map(int, bbox[(i + 1) % n_lines][0]))
        cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)

    # Display the image with the bounding box
    cv2.imshow("QR Code", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No QR code detected.")
