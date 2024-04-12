# even Pip warns the use of sudo isn't a good idea, but it will suffice for now, 
# I'm doing this as I am not sure if I'd need to chmod ec2-user ec2-instance-workload
# and I am trying to get to the point where I need not manually interact with & within the EC2 instance 
# ideally you'd use Cloudformation or Ansible to do this 
sudo pip3 install boto3 python-dotenv
sudo python3 upload-images.py