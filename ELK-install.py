import subprocess
import os
import fileinput
from os import path

#fetch the Elasticsaerch GPG key
if path.exists("/usr/share/keyrings/elasticsearch-keyring.gpg"):
    print("Elastic GPG key already added")
else:
    print("Adding Elastic GPG key")
    subprocess.run("wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg",shell=True)
#add the source list 

if path.exists("/etc/apt/sources.list.d/elastic-8.x.list"):
    print("Source list file already added")
else:
    print("adding elasic source file")
    subprocess.run("echo 'deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main' | sudo tee -a /etc/apt/sources.list.d/elastic-8.x.list", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

#add zeek install here
if path.exists("/etc/apt/trusted.gpg.d/security_zeek.gpg"):
    print("Zeek GPG key already added")
else:
    print("Adding Zeek GPG key")
    subprocess.run("curl -fsSL https://download.opensuse.org/repositories/security:zeek/xUbuntu_20.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #add zeek to path
if path.exists("/etc/apt/sources.list.d/security:zeek.list"):
    print("zeek source list already added")
else: 
    print("adding zeek source file")
    subprocess.run("echo 'deb http://download.opensuse.org/repositories/security:/zeek/xUbuntu_20.04/ /' | sudo tee /etc/apt/sources.list.d/security:zeek.list", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL )

#update repositories    
print("updating repositories")
subprocess.run("sudo apt-get update", shell=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 

# List of packages to be installed

packages = ["apt-transport-https","elasticsearch", "logstash", "kibana", "filebeat","zeek"]

# Check if packages are already installed
installed_packages = [
    package for package in packages
    if subprocess.run(["dpkg-query", "-l", package], capture_output=True, text=True).returncode == 0]

# List of packages to be installed
to_install = [package for package in packages if package not in installed_packages]

# Install the packages
for package in to_install:
    result = subprocess.run(["apt-get", "install", "-y", package])

print("starting services")

output = subprocess.run(["systemctl", "is-active", "elasticsearch", "kibana", "filebeat"], capture_output=True)
if output.stdout.decode().strip() != "active":
    subprocess.run("systemctl start elasticsearch kibana filebeat",shell=True)
else:
    print("services already running")

# add the elasticsearch root CA to trusted certificates on host to allow filebeat to connect to elasticsearch without error /usr/local/share/ca-certificates
if path.exists("/usr/loca/share/ca-certificates/http_ca.crt"):
    print("certificate added")
else:
    print("adding Elastic CA certificate")
    subprocess.run("cp /etc/elasticsearch/certs/http_ca.crt /usr/local/share/ca-certificates/",shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run("update-ca-certificates",shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Packages successfully installed")
print("Enter 1 to display post install info")
print("Enter 2 to uninstall packages:")

final_input = input()
if final_input.strip() == '':
    print("No option selected, Exiting script")
elif final_input.strip() == '1':
    print("elastic user password:")
    subprocess.run("/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic",shell=True)
    print("Kibana enrollment token:")
    subprocess.run("/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana",shell=True)
    print("kibana verification code:")
    subprocess.run("/usr/share/kibana/bin/kibana-verification-code",shell=True)
    print("Make sure to add the Elastic user and password to the filebeat.yml file")
    
elif final_input.strip() == 'uninstall':
    subprocess.run(["apt-get", "remove", "--purge", package, "-y"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["rm", "-rf", "/etc/filebeat/"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["rm", "-rf", "/var/lib/elasticsearch"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["rm", "-rf", "/usr/local/share/ca-certificates/http_ca.crt"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["rm", "-rf", "/etc/ssl/certs/http_ca.pem"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["rm", "-rf", "/opt/zeek/"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("packages uninstalled")
else:
    print("Please select valid option")