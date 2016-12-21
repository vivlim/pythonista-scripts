import appex
import paramiko
from datetime import datetime
import clipboard
import photos
from PIL import Image

max_image_size = 1024

def main():
  if not appex.is_running_extension():
    print('Running standalone, grabbing last picture created')
    img = photos.get_recently_added_album().assets[-1].get_image()
  else:
    img = appex.get_image()
  if img:
    print("You passed in an image of size {}x{}".format(img.width, img.height))
    if img.width > max_image_size or img.height > max_image_size:
        print("Scaling down image since it's big")
        img.thumbnail((max_image_size, max_image_size), Image.ANTIALIAS)
        print("New size is {}x{}".format(img.width, img.height))
        
    img.show()
    print('Starting upload... wait for another line to be printed')

    # open file on server
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('vvn.space', username='vivlim')
    sftp = ssh.open_sftp()
    
    now = datetime.now()
    filename = "upload-{}-{}-{}_{}-{}-{}.jpg".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    file = sftp.file("public_html/" + filename, mode="w")
    
    img.save(file, "JPEG", quality=100)
    file.flush()
    sftp.close()
    ssh.close()
    
    clipboard.set("http://vvn.space/~vivlim/" + filename)
    print("done, url copied")
  else:
    print('No input image found')

if __name__ == '__main__':
  main()
