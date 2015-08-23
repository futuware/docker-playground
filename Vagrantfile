# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.require_version ">= 1.4.0"

require_dnsmasq = RUBY_PLATFORM !~ /cygwin|mswin|mingw|bccwin|wince|emx/
$machines = ["deploy", "app1"]

Vagrant.configure("2") do |config|

    unless require_dnsmasq and Vagrant.has_plugin?("vagrant-dnsmasq")
          puts 'vagrant-dnsmasq is not installed! run: vagrant plugin install vagrant-dnsmasq'
          exit!
    end

#    unless Vagrant.has_plugin?("vagrant-vbguest")
#          puts 'vagrant-vbguest is not installed! run: vagrant plugin install vagrant-vbguest'
#    end

    config.vm.box = "ubuntu1204"
    config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/precise/current/precise-server-cloudimg-amd64-vagrant-disk1.box"

    config.ssh.forward_agent = true

    memory = "512"

    config.vm.provider :vmware_fusion do |fusion|
        fusion.vmx["memsize"] = memory
        fusion.vmx["numvcpus"] = "1"
    end

    config.vm.provider :virtualbox do |vbox|
        vbox.customize [
            "modifyvm", :id,
            "--memory", memory,
            "--natdnshostresolver1", "on",
            "--groups", "/kapellmeister",
        ]
    end

    # Machines configuration
    $machines.each_with_index do |name, i|
        config.vm.define "#{name}" do |m|
            m.vm.hostname = "#{name}.vm"
            domain_name = "#{name}.foo"
            last_octet = 30 + i + 1
            ip = "192.168.130.#{last_octet}"
            m.vm.network :private_network, ip:ip

            config.vm.provider :virtualbox do |vbox|
                vbox.name = "#{name}"
            end

            m.vm.provision "shell", inline: provision_script_body

            if require_dnsmasq
                config.dnsmasq.domain = domain_name
                config.dnsmasq.ip = ip
            end
        end
    end

    if require_dnsmasq
        config.dnsmasq.dnsmasqconf = '/usr/local/etc/dnsmasq.conf'
        if RUBY_PLATFORM =~ /darwin/
            dnsmasq_service = "homebrew.mxcl.dnsmasq"
            config.dnsmasq.reload_command = "sudo launchctl stop #{dnsmasq_service}; sudo launchctl start #{dnsmasq_service}"
        end
    end
end


def provision_script_body()
    ssh_pub_key = File.readlines("vagrant_rsa.pub").first.strip
    ssh_priv_key = File.read("vagrant_rsa")
    script = <<SCRIPT
echo "#{ssh_pub_key}" >> /home/vagrant/.ssh/authorized_keys
echo "#{ssh_pub_key}" > /home/vagrant/.ssh/vagrant_rsa.pub
echo "#{ssh_priv_key}" > /home/vagrant/.ssh/vagrant_rsa
echo "#{ssh_config_contents}" > /home/vagrant/.ssh/config
SCRIPT
    return script
end


def ssh_config_contents()
    config = ""
    $machines.each do |name|
        config += <<CONFIG
Host #{name}.foo
IdentityFile /home/vagrant/.ssh/vagrant_rsa
CONFIG
    end
    return config
end
