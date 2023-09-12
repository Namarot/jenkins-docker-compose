# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64" # This will set up Ubuntu 20.04. You can change to other versions if desired.
  
  # Private network configuration
  config.vm.network "private_network", type: "static", ip: "192.168.56.11"

  config.vm.provision "shell", inline: <<-SHELL
    # Update and upgrade the system
    sudo apt-get update && sudo apt-get upgrade -y

    # Install some essential tools
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg

    # Add Docker's GPG key
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    # Add the repository to Apt sources:
    echo \
      "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update

    # Install Docker
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io

    # Install Docker Compose
    sudo curl -fsSL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Add vagrant user to docker group
    sudo usermod -aG docker vagrant

    # Create SSH directory for vagrant user if not exists
    sudo -u vagrant mkdir -p /home/vagrant/.ssh

    # Fetch the public key from synced folder
    cat /vagrant/ssh_keys/jenkins_key.pub >> /home/vagrant/.ssh/authorized_keys

    # Ensure correct permissions
    sudo chmod 700 /home/vagrant/.ssh
    sudo chmod 600 /home/vagrant/.ssh/authorized_keys
    sudo chown -R vagrant:vagrant /home/vagrant/.ssh/

    # Disable password authentication for SSH
    sudo sed -i 's/^PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
    sudo service ssh restart
  SHELL
end
