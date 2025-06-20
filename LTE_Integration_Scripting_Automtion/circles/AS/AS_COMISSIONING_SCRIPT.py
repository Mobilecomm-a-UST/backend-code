
"""
🔧 Brief Breakdown
1.BBU (Baseband Unit) Setup:
    Sites in Assam Circle are configured using either IPv4 or IPv6.
    The commissioning scripts differ depending on the IP version.
2.Site Commissioning:
    You need to apply basic configuration scripts to each site.
    The script logic should detect the IP type and apply the correct configuration.
"""


AS_SiteBasic_5216_IPV4 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <dnPrefix>SubNetwork=ONRM_ROOT_MO_R,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <fingerprint>{eNodeBName}</fingerprint>
          </Lm>
          <SecM xmlns="urn:com:ericsson:ecim:RcsSecM">
            <secMId>1</secMId>
            <UserManagement>
              <userManagementId>1</userManagementId>
              <LdapAuthenticationMethod xmlns="urn:com:ericsson:ecim:RcsLdapAuthentication">
                <ldapAuthenticationMethodId>1</ldapAuthenticationMethodId>
                <administrativeState>UNLOCKED</administrativeState>
              </LdapAuthenticationMethod>
              <UserIdentity xmlns="urn:com:ericsson:ecim:RcsUser">
                <userIdentityId>1</userIdentityId>
                <MaintenanceUser>
                  <maintenanceUserId>1</maintenanceUserId>
                  <userName>rbs</userName>
                  <password>
                    <cleartext />
                    <password>rbs</password>
                  </password>
                </MaintenanceUser>
              </UserIdentity>
            </UserManagement>
          </SecM>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <CliTls>
              <cliTlsId>1</cliTlsId>
              <administrativeState>UNLOCKED</administrativeState>
            </CliTls>
            <NtpServer>
              <ntpServerId>1</ntpServerId>
              <userLabel>NTP TOD</userLabel>
              <serverAddress>10.102.220.6</serverAddress>
              <administrativeState>UNLOCKED</administrativeState>
            </NtpServer>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <ttl>64</ttl>
          </Router>
        </Transport>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <TnPort xmlns="urn:com:ericsson:ecim:ReqTnPort">
              <tnPortId>{tnPortId}</tnPortId>
              <userLabel>{tnPortId}</userLabel>
            </TnPort>
          </FieldReplaceableUnit>
        </Equipment>
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit=4,TnPort={tnPortId}</encapsulation>
            <userLabel>{tnPortId}</userLabel>
          </EthernetPort>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_OAM</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>OAM</userLabel>
            <vlanId>{OAM_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_OAM</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_OAM</encapsulation>
              <mtu>1500</mtu>
              <userLabel>OAM</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_OAM</addressIPv4Id>
                <address>{OAM_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
        </Transport>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <OamAccessPoint>
              <oamAccessPointId>1</oamAccessPointId>
              <accessPoint>ManagedElement=1,Transport=1,Router=OAM,InterfaceIPv4={tnPortId}_OAM,AddressIPv4={tnPortId}_OAM</accessPoint>
            </OamAccessPoint>
            <OamTrafficClass>
              <oamTrafficClassId>1</oamTrafficClassId>
              <dscp>28</dscp>
            </OamTrafficClass>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <ttl>64</ttl>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_CP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>Control Plane</userLabel>
            <vlanId>{LTE_S1_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_CP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_CP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>Control Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_CP</addressIPv4Id>
                <address>{LTE_S1_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP1</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.157.222.42</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.157.222.44</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <DnsClient xmlns="urn:com:ericsson:ecim:RtnDnsClient">
              <dnsClientId>1</dnsClientId>
              <dscp>46</dscp>
              <serverAddress>10.142.81.132</serverAddress>
            </DnsClient>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_UP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>User Plane</userLabel>
            <vlanId>{LTE_UP_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_UP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_UP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>User Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_UP</addressIPv4Id>
                <address>{LTE_UP_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>1</routeTableIPv4StaticId>
              <Dst>
                <dstId>OSS2</dstId>
                <dst>10.142.18.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>Default_ENM</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>OSS4_M</dstId>
                <dst>10.142.81.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>OSS4_N</dstId>
                <dst>10.142.80.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>SGW1</dstId>
                <dst>10.50.46.121/32</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2</dstId>
                <dst>10.26.144.0/21</dst>
                <NextHop>
                  <nextHopId>{fieldReplaceableUnitId}</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-2</dstId>
                <dst>10.26.152.0/22</dst>
                <NextHop>
                  <nextHopId>5</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-3</dstId>
                <dst>10.26.160.0/22</dst>
                <NextHop>
                  <nextHopId>6</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-4</dstId>
                <dst>10.26.168.0/22</dst>
                <NextHop>
                  <nextHopId>7</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>3</routeTableIPv4StaticId>
              <Dst>
                <dstId>MME1</dstId>
                <dst>10.210.211.160/28</dst>
                <NextHop>
                  <nextHopId>8</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC NTP</dstId>
                <dst>10.168.4.80/28</dst>
                <NextHop>
                  <nextHopId>9</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-5</dstId>
                <dst>10.26.128.0/21</dst>
                <NextHop>
                  <nextHopId>10</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-6</dstId>
                <dst>10.26.136.0/22</dst>
                <NextHop>
                  <nextHopId>11</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-7</dstId>
                <dst>10.26.156.0/22</dst>
                <NextHop>
                  <nextHopId>12</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-8</dstId>
                <dst>10.26.164.0/22</dst>
                <NextHop>
                  <nextHopId>14</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
        </Transport>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="2" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <networkManagedElementId>{eNodeBName}</networkManagedElementId>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>

"""


AS_SiteBasic_6630_IPV4 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <dnPrefix>SubNetwork=ONRM_ROOT_MO_R,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <fingerprint>{eNodeBName}</fingerprint>
          </Lm>
          <SecM xmlns="urn:com:ericsson:ecim:RcsSecM">
            <secMId>1</secMId>
            <UserManagement>
              <userManagementId>1</userManagementId>
              <LdapAuthenticationMethod xmlns="urn:com:ericsson:ecim:RcsLdapAuthentication">
                <ldapAuthenticationMethodId>1</ldapAuthenticationMethodId>
                <administrativeState>UNLOCKED</administrativeState>
              </LdapAuthenticationMethod>
              <UserIdentity xmlns="urn:com:ericsson:ecim:RcsUser">
                <userIdentityId>1</userIdentityId>
                <MaintenanceUser>
                  <maintenanceUserId>1</maintenanceUserId>
                  <userName>rbs</userName>
                  <password>
                    <cleartext />
                    <password>rbs</password>
                  </password>
                </MaintenanceUser>
              </UserIdentity>
            </UserManagement>
          </SecM>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <CliTls>
              <cliTlsId>1</cliTlsId>
              <administrativeState>UNLOCKED</administrativeState>
            </CliTls>
            <NtpServer>
              <ntpServerId>1</ntpServerId>
              <userLabel>NTP TOD</userLabel>
              <serverAddress>10.99.108.22</serverAddress>
              <administrativeState>UNLOCKED</administrativeState>
            </NtpServer>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <ttl>64</ttl>
          </Router>
        </Transport>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <TnPort xmlns="urn:com:ericsson:ecim:ReqTnPort">
              <tnPortId>{tnPortId}</tnPortId>
              <userLabel>{tnPortId}</userLabel>
            </TnPort>
          </FieldReplaceableUnit>
        </Equipment>
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit=4,TnPort={tnPortId}</encapsulation>
            <userLabel>{tnPortId}</userLabel>
          </EthernetPort>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_OAM</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>OAM</userLabel>
            <vlanId>{OAM_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_OAM</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_OAM</encapsulation>
              <mtu>1500</mtu>
              <userLabel>OAM</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_OAM</addressIPv4Id>
                <address>{OAM_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
        </Transport>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <OamAccessPoint>
              <oamAccessPointId>1</oamAccessPointId>
              <accessPoint>ManagedElement=1,Transport=1,Router=OAM,InterfaceIPv4={tnPortId}_OAM,AddressIPv4={tnPortId}_OAM</accessPoint>
            </OamAccessPoint>
            <OamTrafficClass>
              <oamTrafficClassId>1</oamTrafficClassId>
              <dscp>28</dscp>
            </OamTrafficClass>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <ttl>64</ttl>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_CP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>Control Plane</userLabel>
            <vlanId>{LTE_S1_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_CP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_CP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>Control Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_CP</addressIPv4Id>
                <address>{LTE_S1_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP1</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.157.222.42</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.157.222.44</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <DnsClient xmlns="urn:com:ericsson:ecim:RtnDnsClient">
              <dnsClientId>1</dnsClientId>
              <dscp>46</dscp>
              <serverAddress>10.142.81.132</serverAddress>
            </DnsClient>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_UP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>User Plane</userLabel>
            <vlanId>{LTE_UP_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_UP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_UP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>User Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_UP</addressIPv4Id>
                <address>{LTE_UP_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>1</routeTableIPv4StaticId>
              <Dst>
                <dstId>OSS2</dstId>
                <dst>10.142.18.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>Default_ENM</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>OSS4_M</dstId>
                <dst>10.142.81.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>OSS4_N</dstId>
                <dst>10.142.80.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>SGW1</dstId>
                <dst>10.50.46.121/32</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2</dstId>
                <dst>10.26.144.0/21</dst>
                <NextHop>
                  <nextHopId>{fieldReplaceableUnitId}</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-2</dstId>
                <dst>10.26.152.0/22</dst>
                <NextHop>
                  <nextHopId>5</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-3</dstId>
                <dst>10.26.160.0/22</dst>
                <NextHop>
                  <nextHopId>6</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-4</dstId>
                <dst>10.26.168.0/22</dst>
                <NextHop>
                  <nextHopId>7</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>3</routeTableIPv4StaticId>
              <Dst>
                <dstId>MME1</dstId>
                <dst>10.210.211.160/28</dst>
                <NextHop>
                  <nextHopId>8</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC NTP</dstId>
                <dst>10.168.4.80/28</dst>
                <NextHop>
                  <nextHopId>9</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-5</dstId>
                <dst>10.26.128.0/21</dst>
                <NextHop>
                  <nextHopId>10</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-6</dstId>
                <dst>10.26.136.0/22</dst>
                <NextHop>
                  <nextHopId>11</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-7</dstId>
                <dst>10.26.156.0/22</dst>
                <NextHop>
                  <nextHopId>12</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-8</dstId>
                <dst>10.26.164.0/22</dst>
                <NextHop>
                  <nextHopId>14</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
        </Transport>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="2" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <networkManagedElementId>{eNodeBName}</networkManagedElementId>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>

"""


AS_SiteBasic_6631_IPV4 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <dnPrefix>SubNetwork=ONRM_ROOT_MO_R,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <fingerprint>{eNodeBName}</fingerprint>
          </Lm>
          <SecM xmlns="urn:com:ericsson:ecim:RcsSecM">
            <secMId>1</secMId>
            <UserManagement>
              <userManagementId>1</userManagementId>
              <LdapAuthenticationMethod xmlns="urn:com:ericsson:ecim:RcsLdapAuthentication">
                <ldapAuthenticationMethodId>1</ldapAuthenticationMethodId>
                <administrativeState>UNLOCKED</administrativeState>
              </LdapAuthenticationMethod>
              <UserIdentity xmlns="urn:com:ericsson:ecim:RcsUser">
                <userIdentityId>1</userIdentityId>
                <MaintenanceUser>
                  <maintenanceUserId>1</maintenanceUserId>
                  <userName>rbs</userName>
                  <password>
                    <cleartext />
                    <password>rbs</password>
                  </password>
                </MaintenanceUser>
              </UserIdentity>
            </UserManagement>
          </SecM>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <CliTls>
              <cliTlsId>1</cliTlsId>
              <administrativeState>UNLOCKED</administrativeState>
            </CliTls>
            <NtpServer>
              <ntpServerId>1</ntpServerId>
              <userLabel>NTP TOD</userLabel>
              <serverAddress>10.102.220.6</serverAddress>
              <administrativeState>UNLOCKED</administrativeState>
            </NtpServer>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <ttl>64</ttl>
          </Router>
        </Transport>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <TnPort xmlns="urn:com:ericsson:ecim:ReqTnPort">
              <tnPortId>{tnPortId}</tnPortId>
              <userLabel>{tnPortId}</userLabel>
            </TnPort>
          </FieldReplaceableUnit>
        </Equipment>
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit=4,TnPort={tnPortId}</encapsulation>
            <userLabel>{tnPortId}</userLabel>
          </EthernetPort>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_OAM</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>OAM</userLabel>
            <vlanId>{OAM_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_OAM</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_OAM</encapsulation>
              <mtu>1500</mtu>
              <userLabel>OAM</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_OAM</addressIPv4Id>
                <address>{OAM_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
        </Transport>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <OamAccessPoint>
              <oamAccessPointId>1</oamAccessPointId>
              <accessPoint>ManagedElement=1,Transport=1,Router=OAM,InterfaceIPv4={tnPortId}_OAM,AddressIPv4={tnPortId}_OAM</accessPoint>
            </OamAccessPoint>
            <OamTrafficClass>
              <oamTrafficClassId>1</oamTrafficClassId>
              <dscp>28</dscp>
            </OamTrafficClass>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <ttl>64</ttl>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_CP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>Control Plane</userLabel>
            <vlanId>{LTE_S1_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_CP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_CP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>Control Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_CP</addressIPv4Id>
                <address>{LTE_S1_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP1</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.157.222.42</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.157.222.44</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <DnsClient xmlns="urn:com:ericsson:ecim:RtnDnsClient">
              <dnsClientId>1</dnsClientId>
              <dscp>46</dscp>
              <serverAddress>10.142.81.132</serverAddress>
            </DnsClient>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_UP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>User Plane</userLabel>
            <vlanId>{LTE_UP_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_UP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_UP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>User Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_UP</addressIPv4Id>
                <address>{LTE_UP_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>1</routeTableIPv4StaticId>
              <Dst>
                <dstId>OSS2</dstId>
                <dst>10.142.18.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_vlan}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>Default_ENM</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_vlan}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>OSS4_M</dstId>
                <dst>10.142.81.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_vlan}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>OSS4_N</dstId>
                <dst>10.142.80.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_vlan}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>SGW1</dstId>
                <dst>10.50.46.121/32</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2</dstId>
                <dst>10.26.144.0/21</dst>
                <NextHop>
                  <nextHopId>{fieldReplaceableUnitId}</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-2</dstId>
                <dst>10.26.152.0/22</dst>
                <NextHop>
                  <nextHopId>5</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-3</dstId>
                <dst>10.26.160.0/22</dst>
                <NextHop>
                  <nextHopId>6</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-4</dstId>
                <dst>10.26.168.0/22</dst>
                <NextHop>
                  <nextHopId>7</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>3</routeTableIPv4StaticId>
              <Dst>
                <dstId>MME1</dstId>
                <dst>10.210.211.160/28</dst>
                <NextHop>
                  <nextHopId>8</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC NTP</dstId>
                <dst>10.168.4.80/28</dst>
                <NextHop>
                  <nextHopId>9</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-5</dstId>
                <dst>10.26.128.0/21</dst>
                <NextHop>
                  <nextHopId>10</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-6</dstId>
                <dst>10.26.136.0/22</dst>
                <NextHop>
                  <nextHopId>11</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-7</dstId>
                <dst>10.26.156.0/22</dst>
                <NextHop>
                  <nextHopId>12</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-8</dstId>
                <dst>10.26.164.0/22</dst>
                <NextHop>
                  <nextHopId>14</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
        </Transport>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="2" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <networkManagedElementId>{eNodeBName}</networkManagedElementId>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>

"""


AS_SiteBasic_6651_IPV4 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <dnPrefix>SubNetwork=ONRM_ROOT_MO_R,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <fingerprint>{eNodeBName}</fingerprint>
          </Lm>
          <SecM xmlns="urn:com:ericsson:ecim:RcsSecM">
            <secMId>1</secMId>
            <UserManagement>
              <userManagementId>1</userManagementId>
              <LdapAuthenticationMethod xmlns="urn:com:ericsson:ecim:RcsLdapAuthentication">
                <ldapAuthenticationMethodId>1</ldapAuthenticationMethodId>
                <administrativeState>UNLOCKED</administrativeState>
              </LdapAuthenticationMethod>
              <UserIdentity xmlns="urn:com:ericsson:ecim:RcsUser">
                <userIdentityId>1</userIdentityId>
                <MaintenanceUser>
                  <maintenanceUserId>1</maintenanceUserId>
                  <userName>rbs</userName>
                  <password>
                    <cleartext />
                    <password>rbs</password>
                  </password>
                </MaintenanceUser>
              </UserIdentity>
            </UserManagement>
          </SecM>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <CliTls>
              <cliTlsId>1</cliTlsId>
              <administrativeState>UNLOCKED</administrativeState>
            </CliTls>
            <NtpServer>
              <ntpServerId>1</ntpServerId>
              <userLabel>NTP TOD</userLabel>
              <serverAddress>10.102.220.6</serverAddress>
              <administrativeState>UNLOCKED</administrativeState>
            </NtpServer>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <ttl>64</ttl>
          </Router>
        </Transport>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <TnPort xmlns="urn:com:ericsson:ecim:ReqTnPort">
              <tnPortId>{tnPortId}</tnPortId>
              <userLabel>{tnPortId}</userLabel>
            </TnPort>
          </FieldReplaceableUnit>
        </Equipment>
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit=4,TnPort={tnPortId}</encapsulation>
            <userLabel>{tnPortId}</userLabel>
          </EthernetPort>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_OAM</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>OAM</userLabel>
            <vlanId>{OAM_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_OAM</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_OAM</encapsulation>
              <mtu>1500</mtu>
              <userLabel>OAM</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_OAM</addressIPv4Id>
                <address>{OAM_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
        </Transport>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <OamAccessPoint>
              <oamAccessPointId>1</oamAccessPointId>
              <accessPoint>ManagedElement=1,Transport=1,Router=OAM,InterfaceIPv4={tnPortId}_OAM,AddressIPv4={tnPortId}_OAM</accessPoint>
            </OamAccessPoint>
            <OamTrafficClass>
              <oamTrafficClassId>1</oamTrafficClassId>
              <dscp>28</dscp>
            </OamTrafficClass>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <ttl>64</ttl>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_CP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>Control Plane</userLabel>
            <vlanId>{LTE_S1_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_CP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_CP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>Control Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_CP</addressIPv4Id>
                <address>{LTE_S1_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP1</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.157.222.42</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.157.222.44</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <DnsClient xmlns="urn:com:ericsson:ecim:RtnDnsClient">
              <dnsClientId>1</dnsClientId>
              <dscp>46</dscp>
              <serverAddress>10.142.81.132</serverAddress>
            </DnsClient>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_UP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>User Plane</userLabel>
            <vlanId>{LTE_UP_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_UP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_UP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>User Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_UP</addressIPv4Id>
                <address>{LTE_UP_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>1</routeTableIPv4StaticId>
              <Dst>
                <dstId>OSS2</dstId>
                <dst>10.142.18.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_vlan}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>Default_ENM</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_vlan}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>OSS4_M</dstId>
                <dst>10.142.81.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_vlan}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>OSS4_N</dstId>
                <dst>10.142.80.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_vlan}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>SGW1</dstId>
                <dst>10.50.46.121/32</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2</dstId>
                <dst>10.26.144.0/21</dst>
                <NextHop>
                  <nextHopId>{fieldReplaceableUnitId}</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-2</dstId>
                <dst>10.26.152.0/22</dst>
                <NextHop>
                  <nextHopId>5</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-3</dstId>
                <dst>10.26.160.0/22</dst>
                <NextHop>
                  <nextHopId>6</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-4</dstId>
                <dst>10.26.168.0/22</dst>
                <NextHop>
                  <nextHopId>7</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>3</routeTableIPv4StaticId>
              <Dst>
                <dstId>MME1</dstId>
                <dst>10.210.211.160/28</dst>
                <NextHop>
                  <nextHopId>8</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC NTP</dstId>
                <dst>10.168.4.80/28</dst>
                <NextHop>
                  <nextHopId>9</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-5</dstId>
                <dst>10.26.128.0/21</dst>
                <NextHop>
                  <nextHopId>10</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-6</dstId>
                <dst>10.26.136.0/22</dst>
                <NextHop>
                  <nextHopId>11</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-7</dstId>
                <dst>10.26.156.0/22</dst>
                <NextHop>
                  <nextHopId>12</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2-8</dstId>
                <dst>10.26.164.0/22</dst>
                <NextHop>
                  <nextHopId>14</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
        </Transport>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="2" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <networkManagedElementId>{eNodeBName}</networkManagedElementId>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>

"""


AS_SiteBasic_5216_IPV6 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <dnPrefix>SubNetwork=ONRM_ROOT_MO_R,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <fingerprint>{eNodeBName}</fingerprint>
          </Lm>
        </SystemFunctions>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="2" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <FeatureState>
              <featureStateId>CXC4040006</featureStateId>
              <featureState>ACTIVATED</featureState>
            </FeatureState>
          </Lm>
        </SystemFunctions>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="3" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SecM xmlns="urn:com:ericsson:ecim:RcsSecM">
            <secMId>1</secMId>
            <UserManagement>
              <userManagementId>1</userManagementId>
              <LdapAuthenticationMethod xmlns="urn:com:ericsson:ecim:RcsLdapAuthentication">
                <ldapAuthenticationMethodId>1</ldapAuthenticationMethodId>
                <administrativeState>UNLOCKED</administrativeState>
              </LdapAuthenticationMethod>
              <UserIdentity xmlns="urn:com:ericsson:ecim:RcsUser">
                <userIdentityId>1</userIdentityId>
                <MaintenanceUser>
                  <maintenanceUserId>1</maintenanceUserId>
                  <userName>rbs</userName>
                  <password>
                    <cleartext />
                    <password>rbs</password>
                  </password>
                </MaintenanceUser>
              </UserIdentity>
            </UserManagement>
          </SecM>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <CliTls>
              <cliTlsId>1</cliTlsId>
              <administrativeState>UNLOCKED</administrativeState>
            </CliTls>
            <NtpServer>
              <ntpServerId>1</ntpServerId>
              <userLabel>NTP TOD1</userLabel>
              <serverAddress>10.102.220.6</serverAddress>
              <administrativeState>UNLOCKED</administrativeState>
            </NtpServer>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <ttl>64</ttl>
          </Router>
        </Transport>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <TnPort xmlns="urn:com:ericsson:ecim:ReqTnPort">
              <tnPortId>{tnPortId}</tnPortId>
              <userLabel>{tnPortId}</userLabel>
            </TnPort>
          </FieldReplaceableUnit>
        </Equipment>
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit=4,TnPort={tnPortId}</encapsulation>
            <userLabel>{tnPortId}</userLabel>
          </EthernetPort>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_OAM</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>OAM</userLabel>
            <vlanId>{OAM_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>{tnPortId}_OAM</interfaceIPv6Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_OAM</encapsulation>
              <mtu>1500</mtu>
              <userLabel>OAM</userLabel>
              <AddressIPv6>
                <addressIPv6Id>{tnPortId}_OAM</addressIPv6Id>
                <address>{OAM_IP}</address>
              </AddressIPv6>
            </InterfaceIPv6>
          </Router>
        </Transport>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <OamAccessPoint>
              <oamAccessPointId>1</oamAccessPointId>
              <accessPoint>ManagedElement=1,Transport=1,Router=OAM,InterfaceIPv6={tnPortId}_OAM,AddressIPv6={tnPortId}_OAM</accessPoint>
            </OamAccessPoint>
            <OamTrafficClass>
              <oamTrafficClassId>1</oamTrafficClassId>
              <dscp>28</dscp>
            </OamTrafficClass>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <ttl>64</ttl>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_CP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>Control Plane</userLabel>
            <vlanId>{LTE_S1_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_CP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_CP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>Control Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_CP</addressIPv4Id>
                <address>{LTE_S1_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP1</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.177.250.60</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.177.250.62</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
          </Ntp>		  
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <DnsClient xmlns="urn:com:ericsson:ecim:RtnDnsClient">
              <dnsClientId>1</dnsClientId>
              <dscp>46</dscp>
              <serverAddress>10.142.9.179</serverAddress>
            </DnsClient>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_UP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>User Plane</userLabel>
            <vlanId>{LTE_UP_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_UP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_UP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>User Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_UP</addressIPv4Id>
                <address>{LTE_UP_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>SGW1</dstId>
                <dst>10.50.46.121/32</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X21</dstId>
                <dst>10.26.176.0/22</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X22</dstId>
                <dst>10.26.184.0/22</dst>
                <NextHop>
                  <nextHopId>{fieldReplaceableUnitId}</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X23</dstId>
                <dst>10.26.192.0/22</dst>
                <NextHop>
                  <nextHopId>5</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X24</dstId>
                <dst>10.26.200.0/22</dst>
                <NextHop>
                  <nextHopId>6</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>3</routeTableIPv4StaticId>
              <Dst>
                <dstId>MME1</dstId>
                <dst>10.50.46.168/29</dst>
                <NextHop>
                  <nextHopId>7</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X25</dstId>
                <dst>10.26.172.0/22</dst>
                <NextHop>
                  <nextHopId>8</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X26</dstId>
                <dst>10.26.180.0/22</dst>
                <NextHop>
                  <nextHopId>9</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X27</dstId>
                <dst>10.26.188.0/22</dst>
                <NextHop>
                  <nextHopId>10</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X28</dstId>
                <dst>10.26.196.0/22</dst>
                <NextHop>
                  <nextHopId>11</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.177.250.0/24</dst>
                <NextHop>
                  <nextHopId>12</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>1</routeTableIPv6StaticId>
              <Dst>
                <dstId>Default_OSS_ENM</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv6Static>
          </Router>
        </Transport>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="4" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <networkManagedElementId>{eNodeBName}</networkManagedElementId>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>

"""

AS_SiteBasic_6630_IPV6 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <dnPrefix>SubNetwork=ONRM_ROOT_MO_R,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <fingerprint>{eNodeBName}</fingerprint>
          </Lm>
        </SystemFunctions>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="2" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <FeatureState>
              <featureStateId>CXC4040006</featureStateId>
              <featureState>ACTIVATED</featureState>
            </FeatureState>
          </Lm>
        </SystemFunctions>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="3" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SecM xmlns="urn:com:ericsson:ecim:RcsSecM">
            <secMId>1</secMId>
            <UserManagement>
              <userManagementId>1</userManagementId>
              <LdapAuthenticationMethod xmlns="urn:com:ericsson:ecim:RcsLdapAuthentication">
                <ldapAuthenticationMethodId>1</ldapAuthenticationMethodId>
                <administrativeState>UNLOCKED</administrativeState>
              </LdapAuthenticationMethod>
              <UserIdentity xmlns="urn:com:ericsson:ecim:RcsUser">
                <userIdentityId>1</userIdentityId>
                <MaintenanceUser>
                  <maintenanceUserId>1</maintenanceUserId>
                  <userName>rbs</userName>
                  <password>
                    <cleartext />
                    <password>rbs</password>
                  </password>
                </MaintenanceUser>
              </UserIdentity>
            </UserManagement>
          </SecM>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <CliTls>
              <cliTlsId>1</cliTlsId>
              <administrativeState>UNLOCKED</administrativeState>
            </CliTls>
            <NtpServer>
              <ntpServerId>1</ntpServerId>
              <userLabel>NTP TOD1</userLabel>
              <serverAddress>10.142.22.6</serverAddress>
              <administrativeState>UNLOCKED</administrativeState>
            </NtpServer>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <ttl>64</ttl>
          </Router>
        </Transport>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <TnPort xmlns="urn:com:ericsson:ecim:ReqTnPort">
              <tnPortId>{tnPortId}</tnPortId>
              <userLabel>{tnPortId}</userLabel>
            </TnPort>
          </FieldReplaceableUnit>
        </Equipment>
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit=4,TnPort={tnPortId}</encapsulation>
            <userLabel>{tnPortId}</userLabel>
          </EthernetPort>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_OAM</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>OAM</userLabel>
            <vlanId>{OAM_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>{tnPortId}_OAM</interfaceIPv6Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_OAM</encapsulation>
              <mtu>1500</mtu>
              <userLabel>OAM</userLabel>
              <AddressIPv6>
                <addressIPv6Id>{tnPortId}_OAM</addressIPv6Id>
                <address>{OAM_IP}</address>
              </AddressIPv6>
            </InterfaceIPv6>
          </Router>
        </Transport>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <OamAccessPoint>
              <oamAccessPointId>1</oamAccessPointId>
              <accessPoint>ManagedElement=1,Transport=1,Router=OAM,InterfaceIPv6={tnPortId}_OAM,AddressIPv6={tnPortId}_OAM</accessPoint>
            </OamAccessPoint>
            <OamTrafficClass>
              <oamTrafficClassId>1</oamTrafficClassId>
              <dscp>28</dscp>
            </OamTrafficClass>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <ttl>64</ttl>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_CP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>Control Plane</userLabel>
            <vlanId>{LTE_S1_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_CP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_CP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>Control Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_CP</addressIPv4Id>
                <address>{LTE_S1_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP1</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.177.250.60</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.177.250.62</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
          </Ntp>		  
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <DnsClient xmlns="urn:com:ericsson:ecim:RtnDnsClient">
              <dnsClientId>1</dnsClientId>
              <dscp>46</dscp>
              <serverAddress>10.142.9.179</serverAddress>
            </DnsClient>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_UP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>User Plane</userLabel>
            <vlanId>{LTE_UP_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_UP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_UP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>User Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_UP</addressIPv4Id>
                <address>{LTE_UP_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>SGW1</dstId>
                <dst>10.50.46.121/32</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X21</dstId>
                <dst>10.26.176.0/22</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X22</dstId>
                <dst>10.26.184.0/22</dst>
                <NextHop>
                  <nextHopId>{fieldReplaceableUnitId}</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X23</dstId>
                <dst>10.26.192.0/22</dst>
                <NextHop>
                  <nextHopId>5</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X24</dstId>
                <dst>10.26.200.0/22</dst>
                <NextHop>
                  <nextHopId>6</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>3</routeTableIPv4StaticId>
              <Dst>
                <dstId>MME1</dstId>
                <dst>10.50.46.168/29</dst>
                <NextHop>
                  <nextHopId>7</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X25</dstId>
                <dst>10.26.172.0/22</dst>
                <NextHop>
                  <nextHopId>8</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X26</dstId>
                <dst>10.26.180.0/22</dst>
                <NextHop>
                  <nextHopId>9</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X27</dstId>
                <dst>10.26.188.0/22</dst>
                <NextHop>
                  <nextHopId>10</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X28</dstId>
                <dst>10.26.196.0/22</dst>
                <NextHop>
                  <nextHopId>11</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.177.250.0/24</dst>
                <NextHop>
                  <nextHopId>12</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>1</routeTableIPv6StaticId>
              <Dst>
                <dstId>Default_OSS_ENM</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv6Static>
          </Router>
        </Transport>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="4" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <networkManagedElementId>{eNodeBName}</networkManagedElementId>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>

"""

AS_SiteBasic_6631_IPV6 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <dnPrefix>SubNetwork=ONRM_ROOT_MO_R,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <fingerprint>{eNodeBName}</fingerprint>
          </Lm>
        </SystemFunctions>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="2" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <FeatureState>
              <featureStateId>CXC4040006</featureStateId>
              <featureState>ACTIVATED</featureState>
            </FeatureState>
          </Lm>
        </SystemFunctions>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="3" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SecM xmlns="urn:com:ericsson:ecim:RcsSecM">
            <secMId>1</secMId>
            <UserManagement>
              <userManagementId>1</userManagementId>
              <LdapAuthenticationMethod xmlns="urn:com:ericsson:ecim:RcsLdapAuthentication">
                <ldapAuthenticationMethodId>1</ldapAuthenticationMethodId>
                <administrativeState>UNLOCKED</administrativeState>
              </LdapAuthenticationMethod>
              <UserIdentity xmlns="urn:com:ericsson:ecim:RcsUser">
                <userIdentityId>1</userIdentityId>
                <MaintenanceUser>
                  <maintenanceUserId>1</maintenanceUserId>
                  <userName>rbs</userName>
                  <password>
                    <cleartext />
                    <password>rbs</password>
                  </password>
                </MaintenanceUser>
              </UserIdentity>
            </UserManagement>
          </SecM>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <CliTls>
              <cliTlsId>1</cliTlsId>
              <administrativeState>UNLOCKED</administrativeState>
            </CliTls>
            <NtpServer>
              <ntpServerId>1</ntpServerId>
              <userLabel>NTP TOD1</userLabel>
              <serverAddress>10.58.118.6</serverAddress>
              <administrativeState>UNLOCKED</administrativeState>
            </NtpServer>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <ttl>64</ttl>
          </Router>
        </Transport>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <TnPort xmlns="urn:com:ericsson:ecim:ReqTnPort">
              <tnPortId>{tnPortId}</tnPortId>
              <userLabel>{tnPortId}</userLabel>
            </TnPort>
          </FieldReplaceableUnit>
        </Equipment>
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit=4,TnPort={tnPortId}</encapsulation>
            <userLabel>{tnPortId}</userLabel>
          </EthernetPort>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_OAM</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>OAM</userLabel>
            <vlanId>{OAM_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>{tnPortId}_OAM</interfaceIPv6Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_OAM</encapsulation>
              <mtu>1500</mtu>
              <userLabel>OAM</userLabel>
              <AddressIPv6>
                <addressIPv6Id>{tnPortId}_OAM</addressIPv6Id>
                <address>{OAM_IP}</address>
              </AddressIPv6>
            </InterfaceIPv6>
          </Router>
        </Transport>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <OamAccessPoint>
              <oamAccessPointId>1</oamAccessPointId>
              <accessPoint>ManagedElement=1,Transport=1,Router=OAM,InterfaceIPv6={tnPortId}_OAM,AddressIPv6={tnPortId}_OAM</accessPoint>
            </OamAccessPoint>
            <OamTrafficClass>
              <oamTrafficClassId>1</oamTrafficClassId>
              <dscp>28</dscp>
            </OamTrafficClass>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <ttl>64</ttl>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_CP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>Control Plane</userLabel>
            <vlanId>{LTE_S1_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_CP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_CP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>Control Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_CP</addressIPv4Id>
                <address>{LTE_S1_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP1</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.177.250.60</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.177.250.62</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
          </Ntp>		  
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <DnsClient xmlns="urn:com:ericsson:ecim:RtnDnsClient">
              <dnsClientId>1</dnsClientId>
              <dscp>46</dscp>
              <serverAddress>10.142.9.179</serverAddress>
            </DnsClient>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_UP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>User Plane</userLabel>
            <vlanId>{LTE_UP_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_UP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_UP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>User Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_UP</addressIPv4Id>
                <address>{LTE_UP_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>SGW1</dstId>
                <dst>10.50.46.121/32</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X21</dstId>
                <dst>10.26.176.0/22</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X22</dstId>
                <dst>10.26.184.0/22</dst>
                <NextHop>
                  <nextHopId>{fieldReplaceableUnitId}</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X23</dstId>
                <dst>10.26.192.0/22</dst>
                <NextHop>
                  <nextHopId>5</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X24</dstId>
                <dst>10.26.200.0/22</dst>
                <NextHop>
                  <nextHopId>6</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>3</routeTableIPv4StaticId>
              <Dst>
                <dstId>MME1</dstId>
                <dst>10.50.46.168/29</dst>
                <NextHop>
                  <nextHopId>7</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X25</dstId>
                <dst>10.26.172.0/22</dst>
                <NextHop>
                  <nextHopId>8</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X26</dstId>
                <dst>10.26.180.0/22</dst>
                <NextHop>
                  <nextHopId>9</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X27</dstId>
                <dst>10.26.188.0/22</dst>
                <NextHop>
                  <nextHopId>10</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X28</dstId>
                <dst>10.26.196.0/22</dst>
                <NextHop>
                  <nextHopId>11</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.177.250.0/24</dst>
                <NextHop>
                  <nextHopId>12</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>1</routeTableIPv6StaticId>
              <Dst>
                <dstId>Default_OSS_ENM</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv6Static>
          </Router>
        </Transport>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="4" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <networkManagedElementId>{eNodeBName}</networkManagedElementId>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>

"""


AS_SiteBasic_6651_IPV6 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <dnPrefix>SubNetwork=ONRM_ROOT_MO_R,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <fingerprint>{eNodeBName}</fingerprint>
          </Lm>
        </SystemFunctions>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="2" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <FeatureState>
              <featureStateId>CXC4040006</featureStateId>
              <featureState>ACTIVATED</featureState>
            </FeatureState>
          </Lm>
        </SystemFunctions>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="3" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SecM xmlns="urn:com:ericsson:ecim:RcsSecM">
            <secMId>1</secMId>
            <UserManagement>
              <userManagementId>1</userManagementId>
              <LdapAuthenticationMethod xmlns="urn:com:ericsson:ecim:RcsLdapAuthentication">
                <ldapAuthenticationMethodId>1</ldapAuthenticationMethodId>
                <administrativeState>UNLOCKED</administrativeState>
              </LdapAuthenticationMethod>
              <UserIdentity xmlns="urn:com:ericsson:ecim:RcsUser">
                <userIdentityId>1</userIdentityId>
                <MaintenanceUser>
                  <maintenanceUserId>1</maintenanceUserId>
                  <userName>rbs</userName>
                  <password>
                    <cleartext />
                    <password>rbs</password>
                  </password>
                </MaintenanceUser>
              </UserIdentity>
            </UserManagement>
          </SecM>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <CliTls>
              <cliTlsId>1</cliTlsId>
              <administrativeState>UNLOCKED</administrativeState>
            </CliTls>
            <NtpServer>
              <ntpServerId>1</ntpServerId>
              <userLabel>NTP TOD1</userLabel>
              <serverAddress>10.58.118.6</serverAddress>
              <administrativeState>UNLOCKED</administrativeState>
            </NtpServer>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <ttl>64</ttl>
          </Router>
        </Transport>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <TnPort xmlns="urn:com:ericsson:ecim:ReqTnPort">
              <tnPortId>{tnPortId}</tnPortId>
              <userLabel>{tnPortId}</userLabel>
            </TnPort>
          </FieldReplaceableUnit>
        </Equipment>
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit=4,TnPort={tnPortId}</encapsulation>
            <userLabel>{tnPortId}</userLabel>
          </EthernetPort>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_OAM</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>OAM</userLabel>
            <vlanId>{OAM_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>{tnPortId}_OAM</interfaceIPv6Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_OAM</encapsulation>
              <mtu>1500</mtu>
              <userLabel>OAM</userLabel>
              <AddressIPv6>
                <addressIPv6Id>{tnPortId}_OAM</addressIPv6Id>
                <address>{OAM_IP}</address>
              </AddressIPv6>
            </InterfaceIPv6>
          </Router>
        </Transport>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <OamAccessPoint>
              <oamAccessPointId>1</oamAccessPointId>
              <accessPoint>ManagedElement=1,Transport=1,Router=OAM,InterfaceIPv6={tnPortId}_OAM,AddressIPv6={tnPortId}_OAM</accessPoint>
            </OamAccessPoint>
            <OamTrafficClass>
              <oamTrafficClassId>1</oamTrafficClassId>
              <dscp>28</dscp>
            </OamTrafficClass>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
          </Ntp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <ttl>64</ttl>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_CP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>Control Plane</userLabel>
            <vlanId>{LTE_S1_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_CP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_CP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>Control Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_CP</addressIPv4Id>
                <address>{LTE_S1_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Ntp xmlns="urn:com:ericsson:ecim:RsyncNtp">
            <ntpId>1</ntpId>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP1</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.177.250.60</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <syncServerNtpIpAddress>10.177.250.62</syncServerNtpIpAddress>
              <dscp>54</dscp>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
            </NtpFrequencySync>
          </Ntp>		  
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <DnsClient xmlns="urn:com:ericsson:ecim:RtnDnsClient">
              <dnsClientId>1</dnsClientId>
              <dscp>46</dscp>
              <serverAddress>10.142.9.179</serverAddress>
            </DnsClient>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_UP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>User Plane</userLabel>
            <vlanId>{LTE_UP_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>{tnPortId}_UP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort={tnPortId}_UP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>User Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_UP</addressIPv4Id>
                <address>{LTE_UP_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>SGW1</dstId>
                <dst>10.50.46.121/32</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X21</dstId>
                <dst>10.26.176.0/22</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X22</dstId>
                <dst>10.26.184.0/22</dst>
                <NextHop>
                  <nextHopId>{fieldReplaceableUnitId}</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X23</dstId>
                <dst>10.26.192.0/22</dst>
                <NextHop>
                  <nextHopId>5</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X24</dstId>
                <dst>10.26.200.0/22</dst>
                <NextHop>
                  <nextHopId>6</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>3</routeTableIPv4StaticId>
              <Dst>
                <dstId>MME1</dstId>
                <dst>10.50.46.168/29</dst>
                <NextHop>
                  <nextHopId>7</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X25</dstId>
                <dst>10.26.172.0/22</dst>
                <NextHop>
                  <nextHopId>8</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X26</dstId>
                <dst>10.26.180.0/22</dst>
                <NextHop>
                  <nextHopId>9</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X27</dstId>
                <dst>10.26.188.0/22</dst>
                <NextHop>
                  <nextHopId>10</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X28</dstId>
                <dst>10.26.196.0/22</dst>
                <NextHop>
                  <nextHopId>11</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.177.250.0/24</dst>
                <NextHop>
                  <nextHopId>12</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>1</routeTableIPv6StaticId>
              <Dst>
                <dstId>Default_OSS_ENM</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv6Static>
          </Router>
        </Transport>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="4" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <networkManagedElementId>{eNodeBName}</networkManagedElementId>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>

"""