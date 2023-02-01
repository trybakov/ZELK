import subprocess
import os
import fileinput
from os import path
 
if path.exists("/etc/apt/sources.list.d/security:zeek.list"):
    print("zeek source list already added")
else: 
    subprocess.run("echo 'deb http://download.opensuse.org/repositories/security:/zeek/xUbuntu_20.04/ /' | sudo tee /etc/apt/sources.list.d/security:zeek.list", shell=True)

if path.exists("/etc/apt/trusted.gpg.d/security_zeek.gpg"):
    print("Zeek PGP key already added")
else:
    subprocess.run("curl -fsSL https://download.opensuse.org/repositories/security:zeek/xUbuntu_20.04/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/security_zeek.gpg > /dev/null", shell=True)
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "zeek-lts"])

#filebeat configurations and enabling zeek module
print("Enabling zeek module")
subprocess.run(["filebeat", "modules", "enable", "zeek"])

#save a copy of the file, for overwrite purposes
if path.exists("/etc/filebeat/modules.d/zeek.yml.bak"):
    subprocess.run(["cp", "/etc/filebeat/modules.d/zeek.yml.bak", "/etc/filebeat/modules.d/zeek.yml"])
else:
    subprocess.run(["cp", "/etc/filebeat/modules.d/zeek.yml", "/etc/filebeat/modules.d/zeek.yml.bak"])

#save input to list before sending to file to prevent overwrite
lines = []
log_file = input("Enter the path to the zeek log files:")
# if input empty continue without changing file
file_dict = {
    "capture_loss": "capture_loss.log",
    "connection": "conn.log",
    "dce_rpc": "dce_rpc.log",
    "dhcp":"dhcp.log",
    "dnp3": "dnp3.log",
    "dns": "dns.log",
    "dpd": "dpd.log",
    "files": "files.log",
    "ftp": "ftp.log",
    "http": "http.log",
    "intel": "intel.log",
    "irc": "irc.log",
    "kerberos": "kerberos.log",
    "modbus": "modbus.log",
    "mysql": "mysql.log",
    "notice": "notice.log",
    "ntp": "ntp.log",
    "ntlm": "ntlm.log",
    "ocsp": "ocsp.log",
    "pe": "pe.log",
    "radius": "radius.log",
    "rdp": "rdp.log",
    "rfb": "rfb.log",
    #"signature": "signature.log", no support as of now
    "sip": "sip.log",
    "smb_cmd": "smb_cmd.log",
    "smb_files": "smb_files",
    "smb_mapping": "smb_mapping.log",
    "smtp": "smtp.log",
    "snmp": "snmp.log",
    "socks": "socks.log",
    "ssh": "ssh.log",
    "ssl": "ssl.log",
    "stats": "stats.log",
    "syslog": "syslog.log",
    "traceroute": "traceroute.log",
    "tunnel": "tunnel.log",
    "weird": "weird.log",
    "x509": "x509.log"
}

#write data to file
with open("/etc/filebeat/modules.d/zeek.yml") as f:
    for line in f:
        # remove original enabled: false
        if "enabled: false" not in line:
            lines.append(line)

        for start, filename in file_dict.items():
            if line.startswith(f"  {start}:"):
                lines.append("    enabled: true")
                lines.append(f'\n    var.paths: ["{log_file}{filename}"] \n')
                break
with open("/etc/filebeat/modules.d/zeek.yml", "w") as f:
    for line in lines:
        f.write(line)

print("Setting up filebeat assets")
subprocess.run(["filebeat", "setup"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Restarting filebeat")
subprocess.run(["systemctl", "restart", "filebeat"],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Operation finished. If you wish to reload the data delete the Index and rerun the script")




