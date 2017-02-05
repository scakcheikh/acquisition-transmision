#!/bin/sh

#Start wvdial
#wvdial

#Below script that will make all packets targeting port 2121 go through ppp0 link
#Get ppp0 @ip
ip_ptp=$(ip -4 addr show ppp0 | grep -oP '(?<=peer\s)\d+(\.\d+){3}')
ip_ppp0=$(ip -4 addr show ppp0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
#Create iptable
echo 1 modem3g >> /etc/iproute2/rt_tables
#Create routing rule
ip rule add from all fwmark 1 lookup modem3g prio 1000
#set up modem3g iptable
ip route add default dev ppp0 table modem3g
ip route add 0.0.0.0 via 0.0.0.0 dev ppp0 table modem3g

#Create iptable rules
iptables -t mangle -I PREROUTING -p tcp --dport 21 -j MARK --set-mark 1
iptables -t mangle -A OUTPUT -p tcp --dport 21 -j MARK --set-mark 1 
