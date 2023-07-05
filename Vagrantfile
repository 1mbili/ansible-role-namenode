# encoding: utf-8
# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

Vagrant.require_version ">= 2.3.7"
ENV["LC_ALL"] = "en_US.UTF-8"
public_key_path = "temp/kluczyki.pub"

config_data = YAML.load_file("vars/main.yml")


Vagrant.configure("2") do |config|
  (1..config_data['datanode_count']).each do |i|
    config.vm.define "dn#{i}" do |datanode|
      datanode.vm.box = 'gusztavvargadr/ubuntu-server'
      datanode.vm.hostname = "dn#{i}"
      datanode.ssh.forward_agent = true
      datanode.vm.provision "file", source: public_key_path, destination: "~/.ssh/kluczyki.pub"
      datanode.vm.provision "shell", inline: <<-SHELL
      cat /home/vagrant/.ssh/kluczyki.pub >> /home/vagrant/.ssh/authorized_keys
      SHELL
      datanode.vm.provider "virtualbox" do |v|
        v.name = "dn#{i}" 
        v.customize ["modifyvm", :id, "--memory", config_data['box_mem']]
        v.customize ["modifyvm", :id, "--ioapic", "on"]
        v.customize ["modifyvm", :id, "--cpus", config_data['cpus']]
      end
      datanode.vm.network "private_network", ip: config_data['network_range'] + "#{i + 2}"
    end
  end
  
  config.vm.define "nn1" do |namenode|
    namenode.vm.box = 'gusztavvargadr/ubuntu-server'
    namenode.vm.hostname = "nn1"
    namenode.ssh.forward_agent = true
    namenode.vm.provision "file", source: public_key_path, destination: "~/.ssh/kluczyki.pub"
    namenode.vm.provision "shell", inline: <<-SHELL
    cat /home/vagrant/.ssh/kluczyki.pub >> /home/vagrant/.ssh/authorized_keys
    SHELL
    namenode.vm.network "private_network", ip: config_data['network_range'] + "2"
    namenode.vm.provider "virtualbox" do |v|
      v.name = "nn1" 
      v.customize ["modifyvm", :id, "--memory", config_data['box_mem']]
      v.customize ["modifyvm", :id, "--ioapic", "on"]
      v.customize ["modifyvm", :id, "--cpus", config_data['cpus']]
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    end
  end
end