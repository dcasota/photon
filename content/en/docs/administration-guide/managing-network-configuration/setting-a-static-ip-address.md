---
title:  Setting a Static IP Address
weight: 5
---

Before you set a static IP address, obtain the name of your Ethernet link by running the following command: 

	networkctl
	IDX LINK             TYPE               OPERATIONAL SETUP
	  1 lo               loopback           carrier     unmanaged
	  2 eth0             ether              routable    configured

In the results of the command, you can see the name of an Ethernet link, `eth0`.

To create a network configuration file that systemd-networkd uses to establish a static IP address for the eth0 network interface, execute the following command as root: 

	cat > /etc/systemd/network/10-static-en.network << "EOF"

	[Match]
	Name=eth0

	[Network]
	Address=198.51.0.2/24
	Gateway=198.51.0.1
	EOF

Change the new file's mode bits by running the `chmod` command:

    chmod 644 10-static-en.network

Apply the configuration by running either the first or the second step:

	


1. `systemctl restart systemd-networkd `  
       



1. `networkctl reload` 
  `networkctl reconfigure *interface_name/index_number*`

Note: The advantage of using reload and reconfigure is that the settings of other interfaces are not disturbed and only the settings of the specific interface are reloaded and reconfigured.

For more information, see the man page for systemd-networkd: `man systemd.network`