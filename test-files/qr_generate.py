#First Method
# import qrcode
# # example data
# data = "https://www.thepythoncode.com"
# # output file name
# filename = "site.png"
# # generate qr code
# img = qrcode.make(data)
# # save img to a file
# img.save(filename)

import qrcode
import numpy as np
# data to encode
data = "https://www.thepythoncode.com" #will feed data of user in this part

# instantiate QRCode object
qr = qrcode.QRCode(version=1, box_size=10, border=2)
# add data to the QR code
qr.add_data(data)
# compile the data into a QR code array
qr.make()
# print the image shape
print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
# transfer the array into an actual image
img = qr.make_image(fill_color="white", back_color="black")
# save it to a file
img.save("site_inversed.png")