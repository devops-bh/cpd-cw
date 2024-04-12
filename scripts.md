https://askubuntu.com/questions/66492/scp-copy-over-ssh-doesnt-work-permission-denied-error-please

# Copy upload-images to EC2 instance

Make sure you remove the authentication via environment variables when trying to run the script on the ec2 instance (though not sure if you actually need to)

```
scp -r -i "ec2temp.pem" upload-images.py ec2-user@ec2-44-212-18-30.compute-1.amazonaws.com:/home/ec2-user
upload-images.py
```

# Enter into remote instance

ssh -i "ec2temp.pem" ec2-user@ec2-44-212-18-30.compute-1.amazonaws.com

# Copy images

C:\Users\sleep\software-dev-2024\cloud-platform-dev>scp -r -i "ec2temp.pem" images ec2-user@ec2-44-212-18-30.compute-1.amazonaws.com:/home/ec2-user
