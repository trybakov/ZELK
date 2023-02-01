import subprocess
import os
import fileinput
from os import path

#fetch the Elasticsaerch GPG key
if path.exists("/usr/share/keyrings/elasticsearch-keyring.gpg"):
    print("GPG key already added")
else:
    p1 = subprocess.Popen(["wget", "-qO", "-", "https://artifacts.elastic.co/GPG-KEY-elasticsearch"], stdout=subprocess.PIPE)
    subprocess.run(["sudo", "gpg", "--dearmor", "-o", "/usr/share/keyrings/elasticsearch-keyring.gpg"], stdin=p1.stdout)
#add the source list 
if path.exists("/etc/apt/sources.list.d/elastic-8.x.list"):
    #subprocess.run(["sudo", "apt-get", "update"])
    print("Source list file already added")
else:
    subprocess.run("echo 'deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main' | sudo tee -a /etc/apt/sources.list.d/elastic-8.x.list", shell=True)
    subprocess.run(["apt-get", "install", "apt-transport-https"],capture_output=True, text=True)

#update repositories    
subprocess.run(["sudo", "apt-get", "update"],capture_output=True, text=True) 
print("Updating repositories")

#install the stack
# Check if Elasticsearch is already installed
result = subprocess.run(["dpkg-query", "-l", "elasticsearch"], capture_output=True, text=True)
if result.returncode == 0:
    print("Elasticsearch is already installed, skipping installation")
else:
    subprocess.run(["apt-get", "install", "-y", "elasticsearch"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Installing Elasticsearch")
# Check if Logstash is already installed
result = subprocess.run(["dpkg-query", "-l", "logstash"], capture_output=True, text=True)
if result.returncode == 0:
    print("Logstash is already installed, skipping installation")
else:
    subprocess.run(["apt-get", "install", "-y", "logstash"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Installing Logstash")
# Check if Kibana is already installed
result = subprocess.run(["dpkg-query", "-l", "kibana"], capture_output=True, text=True)
if result.returncode == 0:
    print("Kibana is already installed, skipping installation")
else:
    subprocess.run(["apt-get", "install", "-y", "kibana"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Installing Kibana")
#Check if Filebeat is already installed
result = subprocess.run(["dpkg-query", "-l", "filebeat"], capture_output=True, text=True)
if result.returncode == 0:
    print("Filebeat is already installed, skipping installation")
else:
    subprocess.run(["apt-get", "install", "-y", "filebeat"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("installing Filebeat")

print("starting services")

output = subprocess.run(["systemctl", "is-active", "elasticsearch", "kibana", "filebeat"], capture_output=True)
if output.stdout.decode().strip() != "active":
    subprocess.run(["systemctl", "start", "elasticsearch"])
    subprocess.run(["systemctl", "start", "kibana"])
    subprocess.run(["systemctl", "start", "filebeat"])
else:
    print("services already running")

# add the elasticsearch root CA to trusted certificates on host to allow filebeat to connect to elasticsearch without error /usr/local/share/ca-certificates
subprocess.run("cp /etc/elasticsearch/certs/http_ca.crt /usr/local/share/ca-certificates/",shell=True)
subprocess.run("update-ca-certificates",shell=True)

print("Packages successfully installed")
print("Enter 1 to display necessarry security information")
print("If you wish to uninstall the packages please type 'uninstall':")
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
    subprocess.run(["apt-get", "remove", "--purge", "elasticsearch", "logstash", "kibana", "filebeat", "-y"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["rm", "-rf", "/etc/filebeat/"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["rm", "-rf", "/var/lib/elasticsearch"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["rm", "-rf", "/usr/local/share/ca-certificates/http_ca.crt"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["rm", "-rf", "/etc/ssl/certs/http_ca.pem"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("packages uninstalled")
else:
    print("Please select valid option")