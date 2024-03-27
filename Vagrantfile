# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.define "colbert", primary: true do |colbert|
    colbert.vm.box = "ubuntu/focal64"
    colbert.vm.hostname = "colbert"

    colbert.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
    end

    colbert.vm.provision "shell", inline: <<-SHELL
      apt-get update
      DEBIAN_FRONTEND="noninteractive" apt-get install -y build-essential python3-venv \
       python3-dev
    SHELL

    colbert.vm.provision "create-virtualenv-py3", type: :shell, privileged: false, inline: <<-SHELL
      cd ~
      python3 -m venv venv_py3
    SHELL

    colbert.vm.provision "pip3-install", type: :shell, privileged: false, inline: <<-SHELL
      source ~/venv_py3/bin/activate
      pip3 install --upgrade pip
      pip3 install -r /vagrant/requirements.txt
    SHELL

    colbert.vm.provision "bashrc", type: :shell, privileged: false, inline: <<-SHELL
      echo "cd /vagrant" >> ~/.bashrc
      echo "source ~/venv_py3/bin/activate" >> ~/.bashrc
    SHELL
  end
end
