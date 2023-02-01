<h1>ZELK</h1>

The ```ELK-install.py``` scripts installs the Elastic stack (ELK) with basic security features enabled by default. Once the stack is up and running the user can use the ```zeek-install.py``` script to download and enable the Zeek module in Filebeat to transfer zeek logs straight to elasticsearch

<h2>Usage</h2>

> **Note**
> scripts require elevated privileges.

<h3>Installing ELK</h3>
Clone this repository on to your local system and run:

```console
sudo python3 ELK-install.py
```

Once the installation finishes there will be an option to either:
- display security info.
- uninstall and revert all changes from script.

Displaying the security info will output to terminal all relevant information to start elasticsearch with basic security enabled:

- New elastic user password
- Kibana enrolnment token
- Kibana verification code

> **Note**
> If there is an error saying that the kibana verification code could not be created it is likely due to the fact that Kibana server could not be reached yet. Simply navgiate to the Kibana interface at ```localhost:5601``` when it is ready and follow any further instructions.

<h3>Configuring Filebeat and installing Zeek</h3>
As this installation has basic security enabled by default, the Filebeat config will have to be modified. 
Navigate to 

```/etc/filebeat/filebeat.yml``` and change the following fields accordingly in the 
```output.elasticsearch``` section:

- Hosts: ["https://localhost:9200"]
- username: "elastic"
- password: "pass from terminal"

To install Zeek and configure filebeat run:

```console
sudo python3 enable-zeek.py
```
The script will automatically install Zeek and enable the Zeek module in filebeat.

Once the installationis is done, when granted input the directory where the zeek logs will be saved.


