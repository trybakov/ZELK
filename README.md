<h1>ZELK</h1>

This project was created to have an automated process of analyzing a PCAP capture using Zeek and the ELK stack.

<h2>Usage</h2>

> **Note**
> scripts require elevated privileges.

<h3>Istalling ELK and Zeek</h3>
Clone this repository on to your local system and run:

```
sudo python3 ELK-install.py
```
<h3>Configure Zeek</h3>
Add Zeek to path

```
echo "export PATH=$PATH:/opt/zeek/bin" >> ~/.bashrc
```

```
source ~/.bashrc
```
In a folder of your choice use the following command to transform the PCAP to JSON Zeek logs. 
```
zeek -C -r test.pcap LogAscii::use_json=T
```
<h3>Configuring Filebeat</h3>
Modify the ```filebeat.yml``` file:

```
sudo nano /etc/filebeat/filebeat.yml
```

Modify the following lines as needed:

```
   hosts: ["https://localhost:9200"]
   user: "elastic"
   password: "changeme"
```

Run the ```enable-zeek.py``` script:
```
sudo python3 ELK-install.py
```
Follow any instructions untill the configuration is finished.


