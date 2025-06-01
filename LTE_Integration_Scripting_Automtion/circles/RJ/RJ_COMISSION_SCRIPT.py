SiteBasic_ipv6_6631 = """
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
        <dnPrefix>SubNetwork=ONRM_ROOT_MO,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
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
              <userLabel>NTP TOD1</userLabel>
              <serverAddress>10.19.109.12</serverAddress>
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
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
            <Snmp xmlns="urn:com:ericsson:ecim:RcsSnmp">
              <snmpId>1</snmpId>
              <administrativeState>UNLOCKED</administrativeState>
              <agentAddress>
                <host>0.0.0.0</host>
                <port>161</port>
              </agentAddress>
              <SnmpTargetV2C>
                <snmpTargetV2CId>1</snmpTargetV2CId>
                <community>public</community>
                <address>10.19.109.40</address>
                <port>162</port>
                <administrativeState>UNLOCKED</administrativeState>
              </SnmpTargetV2C>
            </Snmp>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>46</dscp>
              <syncServerNtpIpAddress>10.71.26.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>46</dscp>
              <syncServerNtpIpAddress>10.71.26.26</syncServerNtpIpAddress>
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
              <dscp>28</dscp>
              <serverAddress>10.19.109.12</serverAddress>
              <serverAddress>10.19.109.13</serverAddress>
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
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>1</routeTableIPv6StaticId>
              <Dst>
                <dstId>OAM</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              </RouteTableIPv6Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>LTEUP</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
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
                <dstId>LTECP</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
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
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
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

SiteBasic_ipv6_6651 = """
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
        <dnPrefix>SubNetwork=ONRM_ROOT_MO,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
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
              <userLabel>NTP TOD1</userLabel>
              <serverAddress>10.19.109.12</serverAddress>
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
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
            <Snmp xmlns="urn:com:ericsson:ecim:RcsSnmp">
              <snmpId>1</snmpId>
              <administrativeState>UNLOCKED</administrativeState>
              <agentAddress>
                <host>0.0.0.0</host>
                <port>161</port>
              </agentAddress>
              <SnmpTargetV2C>
                <snmpTargetV2CId>1</snmpTargetV2CId>
                <community>public</community>
                <address>10.19.109.40</address>
                <port>162</port>
                <administrativeState>UNLOCKED</administrativeState>
              </SnmpTargetV2C>
            </Snmp>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>46</dscp>
              <syncServerNtpIpAddress>10.71.26.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>46</dscp>
              <syncServerNtpIpAddress>10.71.26.26</syncServerNtpIpAddress>
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
              <dscp>28</dscp>
              <serverAddress>10.19.109.12</serverAddress>
              <serverAddress>10.19.109.13</serverAddress>
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
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>1</routeTableIPv6StaticId>
              <Dst>
                <dstId>OAM</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              </RouteTableIPv6Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>LTEUP</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
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
                <dstId>LTECP</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
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
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
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

SiteBasic_ipv6_6630 = """
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
        <dnPrefix>SubNetwork=ONRM_ROOT_MO,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
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
              <userLabel>NTP TOD1</userLabel>
              <serverAddress>10.19.109.12</serverAddress>
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
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
            <Snmp xmlns="urn:com:ericsson:ecim:RcsSnmp">
              <snmpId>1</snmpId>
              <administrativeState>UNLOCKED</administrativeState>
              <agentAddress>
                <host>0.0.0.0</host>
                <port>161</port>
              </agentAddress>
              <SnmpTargetV2C>
                <snmpTargetV2CId>1</snmpTargetV2CId>
                <community>public</community>
                <address>10.19.109.40</address>
                <port>162</port>
                <administrativeState>UNLOCKED</administrativeState>
              </SnmpTargetV2C>
            </Snmp>
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
            <vlanId>{LTE_S1_GW}</vlanId>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>46</dscp>
              <syncServerNtpIpAddress>10.71.26.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>46</dscp>
              <syncServerNtpIpAddress>10.71.26.26</syncServerNtpIpAddress>
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
              <dscp>28</dscp>
              <serverAddress>10.19.109.12</serverAddress>
              <serverAddress>10.19.109.13</serverAddress>
            </DnsClient>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>{tnPortId}_UP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>User Plane</userLabel>
            <vlanId>{LTE_UP_GW}</vlanId>
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
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>1</routeTableIPv6StaticId>
              <Dst>
                <dstId>OAM</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              </RouteTableIPv6Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>LTEUP</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
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
                <dstId>LTECP</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
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
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
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

SiteBasic_ipv6_6339 = """
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
        <dnPrefix>SubNetwork=ONRM_ROOT_MO,SubNetwork=LTE,MeContext={eNodeBName}</dnPrefix>
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
              <userLabel>NTP TOD1</userLabel>
              <serverAddress>10.19.109.12</serverAddress>
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
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>true</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
            <Snmp xmlns="urn:com:ericsson:ecim:RcsSnmp">
              <snmpId>1</snmpId>
              <administrativeState>UNLOCKED</administrativeState>
              <agentAddress>
                <host>0.0.0.0</host>
                <port>161</port>
              </agentAddress>
              <SnmpTargetV2C>
                <snmpTargetV2CId>1</snmpTargetV2CId>
                <community>public</community>
                <address>10.19.109.40</address>
                <port>162</port>
                <administrativeState>UNLOCKED</administrativeState>
              </SnmpTargetV2C>
            </Snmp>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>46</dscp>
              <syncServerNtpIpAddress>10.71.26.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>46</dscp>
              <syncServerNtpIpAddress>10.71.26.26</syncServerNtpIpAddress>
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
              <dscp>28</dscp>
              <serverAddress>10.19.109.12</serverAddress>
              <serverAddress>10.19.109.13</serverAddress>
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
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>1</routeTableIPv6StaticId>
              <Dst>
                <dstId>OAM</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              </RouteTableIPv6Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>LTEUP</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
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
                <dstId>LTECP</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>3</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
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
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
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

SiteBasic_ipv6_6303 = """
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
              <serverAddress>10.19.105.6</serverAddress>
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
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.26</syncServerNtpIpAddress>
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
              <serverAddress>10.19.105.28</serverAddress>
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
                <dst>10.206.0.0/19</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_1</dstId>
                <dst>10.29.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_2</dstId>
                <dst>10.29.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW2</dstId>
                <dst>10.206.32.65/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW3</dstId>
                <dst>10.40.18.96/28</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW4</dstId>
                <dst>10.50.98.5/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW5</dstId>
                <dst>10.50.98.17/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_3</dstId>
                <dst>10.29.8.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_4</dstId>
                <dst>10.29.24.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_5</dstId>
                <dst>10.29.80.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_6</dstId>
                <dst>10.29.112.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_7</dstId>
                <dst>10.72.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_8</dstId>
                <dst>10.72.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_9</dstId>
                <dst>10.80.160.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_10</dstId>
                <dst>10.80.136.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_11</dstId>
                <dst>10.97.90.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_12</dstId>
                <dst>100.81.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_13</dstId>
                <dst>10.72.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_14</dstId>
                <dst>100.81.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_15</dstId>
                <dst>100.83.192.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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
                <dst>10.206.4.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME2</dstId>
                <dst>10.206.20.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME3</dstId>
                <dst>10.206.27.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME4</dstId>
                <dst>10.206.32.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.163.4.80/29</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MM5</dstId>
                <dst>10.0.235.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_16</dstId>
                <dst>10.29.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_17</dstId>
                <dst>10.29.0.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_18</dstId>
                <dst>10.29.16.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_19</dstId>
                <dst>10.72.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_20</dstId>
                <dst>10.72.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_21</dstId>
                <dst>10.80.152.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_22</dstId>
                <dst>10.29.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_23</dstId>
                <dst>10.80.128.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_24</dstId>
                <dst>10.97.88.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_25</dstId>
                <dst>100.81.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_26</dstId>
                <dst>100.81.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_27</dstId>
                <dst>10.72.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_28</dstId>
                <dst>10.29.64.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_29</dstId>
                <dst>10.29.96.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_30</dstId>
                <dst>100.83.208.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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
                <dstId>OSS</dstId>
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

SiteBasic_ipv4_6651 = """
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
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
            <TimeM xmlns="urn:com:ericsson:ecim:RcsTimeM">
              <timeMId>1</timeMId>
              <Ntp>
                <ntpId>1</ntpId>
                <NtpServer>
                  <ntpServerId>1</ntpServerId>
                  <userLabel>NTP TOD</userLabel>
                  <serverAddress>10.19.105.6</serverAddress>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
              </Ntp>
            </TimeM>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.26</syncServerNtpIpAddress>
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
              <serverAddress>10.19.105.28</serverAddress>
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
                <dstId>OSS</dstId>
                <dst>0.0.0.0/0</dst>
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
                <dst>10.206.0.0/19</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_1</dstId>
                <dst>10.29.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_2</dstId>
                <dst>10.29.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW2</dstId>
                <dst>10.206.32.65/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW3</dstId>
                <dst>10.40.18.96/28</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW4</dstId>
                <dst>10.50.98.5/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW5</dstId>
                <dst>10.50.98.17/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_3</dstId>
                <dst>10.29.8.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_4</dstId>
                <dst>10.29.24.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_5</dstId>
                <dst>10.29.80.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_6</dstId>
                <dst>10.29.112.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_7</dstId>
                <dst>10.72.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_8</dstId>
                <dst>10.72.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_9</dstId>
                <dst>10.80.160.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_10</dstId>
                <dst>10.80.136.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_11</dstId>
                <dst>10.97.90.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_12</dstId>
                <dst>100.81.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_13</dstId>
                <dst>10.72.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_14</dstId>
                <dst>100.81.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_15</dstId>
                <dst>100.83.192.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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
                <dst>10.206.4.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME2</dstId>
                <dst>10.206.20.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME3</dstId>
                <dst>10.206.27.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME4</dstId>
                <dst>10.206.32.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.163.4.80/29</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MM5</dstId>
                <dst>10.0.235.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_16</dstId>
                <dst>10.29.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_17</dstId>
                <dst>10.29.0.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_18</dstId>
                <dst>10.29.16.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_19</dstId>
                <dst>10.72.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_20</dstId>
                <dst>10.72.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_21</dstId>
                <dst>10.80.152.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_22</dstId>
                <dst>10.29.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_23</dstId>
                <dst>10.80.128.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_24</dstId>
                <dst>10.97.88.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_25</dstId>
                <dst>100.81.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_26</dstId>
                <dst>100.81.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_27</dstId>
                <dst>10.72.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_28</dstId>
                <dst>10.29.64.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_29</dstId>
                <dst>10.29.96.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_30</dstId>
                <dst>100.83.208.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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

SiteBasic_ipv4_6631 = """
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
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
            <TimeM xmlns="urn:com:ericsson:ecim:RcsTimeM">
              <timeMId>1</timeMId>
              <Ntp>
                <ntpId>1</ntpId>
                <NtpServer>
                  <ntpServerId>1</ntpServerId>
                  <userLabel>NTP TOD</userLabel>
                  <serverAddress>10.19.105.6</serverAddress>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
              </Ntp>
            </TimeM>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.26</syncServerNtpIpAddress>
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
              <serverAddress>10.19.105.28</serverAddress>
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
                <dstId>OSS</dstId>
                <dst>0.0.0.0/0</dst>
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
                <dst>10.206.0.0/19</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_1</dstId>
                <dst>10.29.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_2</dstId>
                <dst>10.29.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW2</dstId>
                <dst>10.206.32.65/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW3</dstId>
                <dst>10.40.18.96/28</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW4</dstId>
                <dst>10.50.98.5/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW5</dstId>
                <dst>10.50.98.17/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_3</dstId>
                <dst>10.29.8.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_4</dstId>
                <dst>10.29.24.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_5</dstId>
                <dst>10.29.80.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_6</dstId>
                <dst>10.29.112.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_7</dstId>
                <dst>10.72.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_8</dstId>
                <dst>10.72.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_9</dstId>
                <dst>10.80.160.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_10</dstId>
                <dst>10.80.136.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_11</dstId>
                <dst>10.97.90.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_12</dstId>
                <dst>100.81.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_13</dstId>
                <dst>10.72.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_14</dstId>
                <dst>100.81.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_15</dstId>
                <dst>100.83.192.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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
                <dst>10.206.4.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME2</dstId>
                <dst>10.206.20.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME3</dstId>
                <dst>10.206.27.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME4</dstId>
                <dst>10.206.32.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.163.4.80/29</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MM5</dstId>
                <dst>10.0.235.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_16</dstId>
                <dst>10.29.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_17</dstId>
                <dst>10.29.0.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_18</dstId>
                <dst>10.29.16.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_19</dstId>
                <dst>10.72.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_20</dstId>
                <dst>10.72.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_21</dstId>
                <dst>10.80.152.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_22</dstId>
                <dst>10.29.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_23</dstId>
                <dst>10.80.128.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_24</dstId>
                <dst>10.97.88.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_25</dstId>
                <dst>100.81.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_26</dstId>
                <dst>100.81.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_27</dstId>
                <dst>10.72.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_28</dstId>
                <dst>10.29.64.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_29</dstId>
                <dst>10.29.96.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_30</dstId>
                <dst>100.83.208.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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

SiteBasic_ipv4_6630 = """
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
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
            <TimeM xmlns="urn:com:ericsson:ecim:RcsTimeM">
              <timeMId>1</timeMId>
              <Ntp>
                <ntpId>1</ntpId>
                <NtpServer>
                  <ntpServerId>1</ntpServerId>
                  <userLabel>NTP TOD</userLabel>
                  <serverAddress>10.19.105.6</serverAddress>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
              </Ntp>
            </TimeM>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.26</syncServerNtpIpAddress>
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
              <serverAddress>10.19.105.28</serverAddress>
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
                <dstId>OSS</dstId>
                <dst>0.0.0.0/0</dst>
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
                <dst>10.206.0.0/19</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_1</dstId>
                <dst>10.29.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_2</dstId>
                <dst>10.29.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW2</dstId>
                <dst>10.206.32.65/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW3</dstId>
                <dst>10.40.18.96/28</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW4</dstId>
                <dst>10.50.98.5/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW5</dstId>
                <dst>10.50.98.17/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_3</dstId>
                <dst>10.29.8.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_4</dstId>
                <dst>10.29.24.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_5</dstId>
                <dst>10.29.80.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_6</dstId>
                <dst>10.29.112.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_7</dstId>
                <dst>10.72.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_8</dstId>
                <dst>10.72.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_9</dstId>
                <dst>10.80.160.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_10</dstId>
                <dst>10.80.136.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_11</dstId>
                <dst>10.97.90.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_12</dstId>
                <dst>100.81.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_13</dstId>
                <dst>10.72.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_14</dstId>
                <dst>100.81.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_15</dstId>
                <dst>100.83.192.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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
                <dst>10.206.4.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME2</dstId>
                <dst>10.206.20.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME3</dstId>
                <dst>10.206.27.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME4</dstId>
                <dst>10.206.32.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.163.4.80/29</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MM5</dstId>
                <dst>10.0.235.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_16</dstId>
                <dst>10.29.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_17</dstId>
                <dst>10.29.0.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_18</dstId>
                <dst>10.29.16.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_19</dstId>
                <dst>10.72.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_20</dstId>
                <dst>10.72.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_21</dstId>
                <dst>10.80.152.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_22</dstId>
                <dst>10.29.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_23</dstId>
                <dst>10.80.128.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_24</dstId>
                <dst>10.97.88.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_25</dstId>
                <dst>100.81.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_26</dstId>
                <dst>100.81.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_27</dstId>
                <dst>10.72.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_28</dstId>
                <dst>10.29.64.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_29</dstId>
                <dst>10.29.96.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_30</dstId>
                <dst>100.83.208.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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

SiteBasic_ipv4_6353 = """
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
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
            <TimeM xmlns="urn:com:ericsson:ecim:RcsTimeM">
              <timeMId>1</timeMId>
              <Ntp>
                <ntpId>1</ntpId>
                <NtpServer>
                  <ntpServerId>1</ntpServerId>
                  <userLabel>NTP TOD</userLabel>
                  <serverAddress>10.19.105.6</serverAddress>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
              </Ntp>
            </TimeM>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.26</syncServerNtpIpAddress>
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
              <serverAddress>10.19.105.28</serverAddress>
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
                <dstId>OSS</dstId>
                <dst>0.0.0.0/0</dst>
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
                <dst>10.206.0.0/19</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_1</dstId>
                <dst>10.29.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_2</dstId>
                <dst>10.29.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW2</dstId>
                <dst>10.206.32.65/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW3</dstId>
                <dst>10.40.18.96/28</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW4</dstId>
                <dst>10.50.98.5/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW5</dstId>
                <dst>10.50.98.17/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_3</dstId>
                <dst>10.29.8.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_4</dstId>
                <dst>10.29.24.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_5</dstId>
                <dst>10.29.80.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_6</dstId>
                <dst>10.29.112.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_7</dstId>
                <dst>10.72.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_8</dstId>
                <dst>10.72.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_9</dstId>
                <dst>10.80.160.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_10</dstId>
                <dst>10.80.136.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_11</dstId>
                <dst>10.97.90.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_12</dstId>
                <dst>100.81.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_13</dstId>
                <dst>10.72.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_14</dstId>
                <dst>100.81.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_15</dstId>
                <dst>100.83.192.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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
                <dst>10.206.4.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME2</dstId>
                <dst>10.206.20.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME3</dstId>
                <dst>10.206.27.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME4</dstId>
                <dst>10.206.32.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.163.4.80/29</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MM5</dstId>
                <dst>10.0.235.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_16</dstId>
                <dst>10.29.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_17</dstId>
                <dst>10.29.0.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_18</dstId>
                <dst>10.29.16.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_19</dstId>
                <dst>10.72.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_20</dstId>
                <dst>10.72.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_21</dstId>
                <dst>10.80.152.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_22</dstId>
                <dst>10.29.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_23</dstId>
                <dst>10.80.128.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_24</dstId>
                <dst>10.97.88.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_25</dstId>
                <dst>100.81.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_26</dstId>
                <dst>100.81.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_27</dstId>
                <dst>10.72.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_28</dstId>
                <dst>10.29.64.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_29</dstId>
                <dst>10.29.96.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_30</dstId>
                <dst>100.83.208.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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

SiteBasic_ipv4_6339 = """
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
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
            <TimeM xmlns="urn:com:ericsson:ecim:RcsTimeM">
              <timeMId>1</timeMId>
              <Ntp>
                <ntpId>1</ntpId>
                <NtpServer>
                  <ntpServerId>1</ntpServerId>
                  <userLabel>NTP TOD</userLabel>
                  <serverAddress>10.19.105.6</serverAddress>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
              </Ntp>
            </TimeM>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.26</syncServerNtpIpAddress>
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
              <serverAddress>10.19.105.28</serverAddress>
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
                <dstId>OSS</dstId>
                <dst>0.0.0.0/0</dst>
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
                <dst>10.206.0.0/19</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_1</dstId>
                <dst>10.29.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_2</dstId>
                <dst>10.29.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW2</dstId>
                <dst>10.206.32.65/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW3</dstId>
                <dst>10.40.18.96/28</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW4</dstId>
                <dst>10.50.98.5/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW5</dstId>
                <dst>10.50.98.17/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_3</dstId>
                <dst>10.29.8.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_4</dstId>
                <dst>10.29.24.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_5</dstId>
                <dst>10.29.80.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_6</dstId>
                <dst>10.29.112.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_7</dstId>
                <dst>10.72.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_8</dstId>
                <dst>10.72.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_9</dstId>
                <dst>10.80.160.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_10</dstId>
                <dst>10.80.136.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_11</dstId>
                <dst>10.97.90.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_12</dstId>
                <dst>100.81.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_13</dstId>
                <dst>10.72.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_14</dstId>
                <dst>100.81.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_15</dstId>
                <dst>100.83.192.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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
                <dst>10.206.4.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME2</dstId>
                <dst>10.206.20.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME3</dstId>
                <dst>10.206.27.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME4</dstId>
                <dst>10.206.32.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.163.4.80/29</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MM5</dstId>
                <dst>10.0.235.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_16</dstId>
                <dst>10.29.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_17</dstId>
                <dst>10.29.0.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_18</dstId>
                <dst>10.29.16.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_19</dstId>
                <dst>10.72.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_20</dstId>
                <dst>10.72.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_21</dstId>
                <dst>10.80.152.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_22</dstId>
                <dst>10.29.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_23</dstId>
                <dst>10.80.128.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_24</dstId>
                <dst>10.97.88.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_25</dstId>
                <dst>100.81.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_26</dstId>
                <dst>100.81.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_27</dstId>
                <dst>10.72.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_28</dstId>
                <dst>10.29.64.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_29</dstId>
                <dst>10.29.96.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_30</dstId>
                <dst>100.83.208.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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

SiteBasic_ipv4_6339 = """
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
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
            <TimeM xmlns="urn:com:ericsson:ecim:RcsTimeM">
              <timeMId>1</timeMId>
              <Ntp>
                <ntpId>1</ntpId>
                <NtpServer>
                  <ntpServerId>1</ntpServerId>
                  <userLabel>NTP TOD</userLabel>
                  <serverAddress>10.19.105.6</serverAddress>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
              </Ntp>
            </TimeM>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.26</syncServerNtpIpAddress>
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
              <serverAddress>10.19.105.28</serverAddress>
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
                <dstId>OSS</dstId>
                <dst>0.0.0.0/0</dst>
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
                <dst>10.206.0.0/19</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_1</dstId>
                <dst>10.29.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_2</dstId>
                <dst>10.29.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW2</dstId>
                <dst>10.206.32.65/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW3</dstId>
                <dst>10.40.18.96/28</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW4</dstId>
                <dst>10.50.98.5/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW5</dstId>
                <dst>10.50.98.17/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_3</dstId>
                <dst>10.29.8.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_4</dstId>
                <dst>10.29.24.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_5</dstId>
                <dst>10.29.80.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_6</dstId>
                <dst>10.29.112.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_7</dstId>
                <dst>10.72.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_8</dstId>
                <dst>10.72.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_9</dstId>
                <dst>10.80.160.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_10</dstId>
                <dst>10.80.136.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_11</dstId>
                <dst>10.97.90.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_12</dstId>
                <dst>100.81.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_13</dstId>
                <dst>10.72.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_14</dstId>
                <dst>100.81.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_15</dstId>
                <dst>100.83.192.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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
                <dst>10.206.4.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME2</dstId>
                <dst>10.206.20.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME3</dstId>
                <dst>10.206.27.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME4</dstId>
                <dst>10.206.32.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.163.4.80/29</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MM5</dstId>
                <dst>10.0.235.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_16</dstId>
                <dst>10.29.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_17</dstId>
                <dst>10.29.0.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_18</dstId>
                <dst>10.29.16.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_19</dstId>
                <dst>10.72.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_20</dstId>
                <dst>10.72.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_21</dstId>
                <dst>10.80.152.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_22</dstId>
                <dst>10.29.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_23</dstId>
                <dst>10.80.128.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_24</dstId>
                <dst>10.97.88.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_25</dstId>
                <dst>100.81.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_26</dstId>
                <dst>100.81.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_27</dstId>
                <dst>10.72.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_28</dstId>
                <dst>10.29.64.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_29</dstId>
                <dst>10.29.96.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_30</dstId>
                <dst>100.83.208.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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

SiteBasic_ipv4_6303 = """
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
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
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
            <TimeM xmlns="urn:com:ericsson:ecim:RcsTimeM">
              <timeMId>1</timeMId>
              <Ntp>
                <ntpId>1</ntpId>
                <NtpServer>
                  <ntpServerId>1</ntpServerId>
                  <userLabel>NTP TOD</userLabel>
                  <serverAddress>10.19.105.6</serverAddress>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
              </Ntp>
            </TimeM>
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
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.24</syncServerNtpIpAddress>
            </NtpFrequencySync>
            <NtpFrequencySync>
              <ntpFrequencySyncId>NTP2</ntpFrequencySyncId>
              <addressIPv4Reference>ManagedElement=1,Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP</addressIPv4Reference>
              <dscp>54</dscp>
              <syncServerNtpIpAddress>10.163.190.26</syncServerNtpIpAddress>
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
              <serverAddress>10.19.105.28</serverAddress>
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
                <dstId>OSS</dstId>
                <dst>0.0.0.0/0</dst>
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
                <dst>10.206.0.0/19</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_1</dstId>
                <dst>10.29.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_2</dstId>
                <dst>10.29.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW2</dstId>
                <dst>10.206.32.65/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW3</dstId>
                <dst>10.40.18.96/28</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW4</dstId>
                <dst>10.50.98.5/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>SGW5</dstId>
                <dst>10.50.98.17/32</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_3</dstId>
                <dst>10.29.8.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_4</dstId>
                <dst>10.29.24.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_5</dstId>
                <dst>10.29.80.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_6</dstId>
                <dst>10.29.112.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_7</dstId>
                <dst>10.72.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_8</dstId>
                <dst>10.72.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_9</dstId>
                <dst>10.80.160.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_10</dstId>
                <dst>10.80.136.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_11</dstId>
                <dst>10.97.90.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_12</dstId>
                <dst>100.81.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_13</dstId>
                <dst>10.72.16.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_14</dstId>
                <dst>100.81.56.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_15</dstId>
                <dst>100.83.192.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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
                <dst>10.206.4.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME2</dstId>
                <dst>10.206.20.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME3</dstId>
                <dst>10.206.27.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MME4</dstId>
                <dst>10.206.32.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>RNC</dstId>
                <dst>10.163.4.80/29</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>MM5</dstId>
                <dst>10.0.235.0/24</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_16</dstId>
                <dst>10.29.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_17</dstId>
                <dst>10.29.0.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_18</dstId>
                <dst>10.29.16.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_19</dstId>
                <dst>10.72.32.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_20</dstId>
                <dst>10.72.40.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_21</dstId>
                <dst>10.80.152.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_22</dstId>
                <dst>10.29.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_23</dstId>
                <dst>10.80.128.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_24</dstId>
                <dst>10.97.88.0/23</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_25</dstId>
                <dst>100.81.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_26</dstId>
                <dst>100.81.48.0/21</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_27</dstId>
                <dst>10.72.0.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_28</dstId>
                <dst>10.29.64.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_29</dstId>
                <dst>10.29.96.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>X2_30</dstId>
                <dst>100.83.208.0/20</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
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



SiteEquipment_5216 = """
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
        <userLabel>{Phy_SiteID_Userlabel}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <Cabinet xmlns="urn:com:ericsson:ecim:ReqCabinet">
            <cabinetId>1</cabinetId>
            <smokeDetector>false</smokeDetector>
            <climateSystem>STANDARD</climateSystem>
          </Cabinet>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <administrativeState>UNLOCKED</administrativeState>
            <EcPort xmlns="urn:com:ericsson:ecim:ReqEcPort">
              <ecPortId>1</ecPortId>
              <hubPosition>A</hubPosition>
            </EcPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>A</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>B</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>C</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>D</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>E</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>F</riPortId>
            </RiPort>
            <SyncPort xmlns="urn:com:ericsson:ecim:ReqSyncPort">
              <syncPortId>1</syncPortId>
            </SyncPort>
          </FieldReplaceableUnit>
        </Equipment>
        <EquipmentSupportFunction xmlns="urn:com:ericsson:ecim:ResEquipmentSupportFunction">
          <equipmentSupportFunctionId>1</equipmentSupportFunctionId>
          <supportSystemControl>true</supportSystemControl>
          <PowerDistribution xmlns="urn:com:ericsson:ecim:ResPowerDistribution">
            <powerDistributionId>1</powerDistributionId>
            <controlDomainRef>ManagedElement=1,Equipment=1,Cabinet=1</controlDomainRef>
          </PowerDistribution>
          <PowerSupply xmlns="urn:com:ericsson:ecim:ResPowerSupply">
            <powerSupplyId>1</powerSupplyId>
            <controlDomainRef>ManagedElement=1,Equipment=1,Cabinet=1</controlDomainRef>
          </PowerSupply>
        </EquipmentSupportFunction>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>
          <MpClusterHandling xmlns="urn:com:ericsson:ecim:RmeMpClusterHandling">
            <mpClusterHandlingId>1</mpClusterHandlingId>
            <primaryCoreRef>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId}</primaryCoreRef>
          </MpClusterHandling>
        </NodeSupport>
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
SiteEquipment_6303 = """
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
        <userLabel>{Phy_SiteID_Userlabel}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <administrativeState>UNLOCKED</administrativeState>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>A</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>B</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>C</riPortId>
            </RiPort>
            <SyncPort xmlns="urn:com:ericsson:ecim:ReqSyncPort">
              <syncPortId>1</syncPortId>
            </SyncPort>
          </FieldReplaceableUnit>
        </Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>
          <MpClusterHandling xmlns="urn:com:ericsson:ecim:RmeMpClusterHandling">
            <mpClusterHandlingId>1</mpClusterHandlingId>
            <primaryCoreRef>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId}</primaryCoreRef>
          </MpClusterHandling>
        </NodeSupport>
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
SiteEquipment_6339 = """
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
        <userLabel>{Phy_SiteID_Userlabel}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <administrativeState>UNLOCKED</administrativeState>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>A</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>B</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>C</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>D</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>E</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>F</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>G</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>H</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>J</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>K</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>L</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>M</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>N</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>P</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>Q</riPortId>
            </RiPort>
            <SyncPort xmlns="urn:com:ericsson:ecim:ReqSyncPort">
              <syncPortId>1</syncPortId>
            </SyncPort>
          </FieldReplaceableUnit>
        </Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>
          <MpClusterHandling xmlns="urn:com:ericsson:ecim:RmeMpClusterHandling">
            <mpClusterHandlingId>1</mpClusterHandlingId>
            <primaryCoreRef>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId}</primaryCoreRef>
          </MpClusterHandling>
        </NodeSupport>
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
SiteEquipment_6353 = """
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
        <userLabel>{Phy_SiteID_Userlabel}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <administrativeState>UNLOCKED</administrativeState>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>A</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>B</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>C</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>D</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>E</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>F</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>G</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>H</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>J</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>K</riPortId>
            </RiPort>
            <SyncPort xmlns="urn:com:ericsson:ecim:ReqSyncPort">
              <syncPortId>1</syncPortId>
            </SyncPort>
          </FieldReplaceableUnit>
        </Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>
          <MpClusterHandling xmlns="urn:com:ericsson:ecim:RmeMpClusterHandling">
            <mpClusterHandlingId>1</mpClusterHandlingId>
            <primaryCoreRef>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId}</primaryCoreRef>
          </MpClusterHandling>
        </NodeSupport>
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
SiteEquipment_6630 = """
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
        <userLabel>{Phy_SiteID_Userlabel}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <administrativeState>UNLOCKED</administrativeState>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>A</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>B</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>C</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>D</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>E</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>F</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>G</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>H</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>J</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>K</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>L</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>M</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>N</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>P</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>Q</riPortId>
            </RiPort>
            <SyncPort xmlns="urn:com:ericsson:ecim:ReqSyncPort">
              <syncPortId>1</syncPortId>
            </SyncPort>
          </FieldReplaceableUnit>
        </Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>
          <MpClusterHandling xmlns="urn:com:ericsson:ecim:RmeMpClusterHandling">
            <mpClusterHandlingId>1</mpClusterHandlingId>
            <primaryCoreRef>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId}</primaryCoreRef>
          </MpClusterHandling>
        </NodeSupport>
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
SiteEquipment_6631 = """
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
        <userLabel>{Phy_SiteID_Userlabel}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <administrativeState>UNLOCKED</administrativeState>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>A</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>B</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>C</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>D</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>E</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>F</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>G</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>H</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>J</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>K</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>L</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>M</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>N</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>P</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>Q</riPortId>
            </RiPort>
            <SyncPort xmlns="urn:com:ericsson:ecim:ReqSyncPort">
              <syncPortId>1</syncPortId>
            </SyncPort>
          </FieldReplaceableUnit>
        </Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>
          <MpClusterHandling xmlns="urn:com:ericsson:ecim:RmeMpClusterHandling">
            <mpClusterHandlingId>1</mpClusterHandlingId>
            <primaryCoreRef>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId}</primaryCoreRef>
          </MpClusterHandling>
        </NodeSupport>
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
SiteEquipment_6648 = """
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
        <userLabel>{Phy_SiteID_Userlabel}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <administrativeState>UNLOCKED</administrativeState>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>A</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>B</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>C</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>D</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>E</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>F</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>G</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>H</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>J</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>K</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>L</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>M</riPortId>
            </RiPort>
            <SyncPort xmlns="urn:com:ericsson:ecim:ReqSyncPort">
              <syncPortId>1</syncPortId>
            </SyncPort>
          </FieldReplaceableUnit>
        </Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>
          <MpClusterHandling xmlns="urn:com:ericsson:ecim:RmeMpClusterHandling">
            <mpClusterHandlingId>1</mpClusterHandlingId>
            <primaryCoreRef>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId}</primaryCoreRef>
          </MpClusterHandling>
        </NodeSupport>
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
SiteEquipment_R503 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:com:ericsson:ebase:0.1.0</capability>
    <capability>urn:com:ericsson:ebase:1.1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="Equipment=XMU" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <administrativeState>UNLOCKED</administrativeState>
            <fieldReplaceableUnitId>R503</fieldReplaceableUnitId>
            <isSharedWithExternalMe>false</isSharedWithExternalMe>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>1</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>2</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>3</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>4</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>5</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>6</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>7</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>9</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>10</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>11</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>12</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>13</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>14</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>15</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>16</riPortId>
              <administrativeState>UNLOCKED</administrativeState>
            </RiPort>
          </FieldReplaceableUnit>
		  </Equipment>
		</ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session/>
</rpc>
]]>]]>


<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:com:ericsson:ebase:0.1.0</capability>
    <capability>urn:com:ericsson:ebase:1.1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="Equipment=data,NodeSupport=data" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>1</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=1,RiPort=A</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=R503,RiPort=1</riPortRef2>
            <transportType>NOT_SET</transportType>
          </RiLink>
  		  </Equipment>
		</ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session/>
</rpc>
]]>]]>


<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:com:ericsson:ebase:0.1.0</capability>
    <capability>urn:com:ericsson:ebase:1.1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="Equipment=data,NodeSupport=data" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>2</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=1,RiPort=B</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=R503,RiPort=2</riPortRef2>
            <transportType>NOT_SET</transportType>
          </RiLink>
  		  </Equipment>
		</ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session/>
</rpc>
]]>]]>



<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:com:ericsson:ebase:0.1.0</capability>
    <capability>urn:com:ericsson:ebase:1.1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="Equipment=data,NodeSupport=data" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>3</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=1,RiPort=C</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=R503,RiPort=3</riPortRef2>
            <transportType>NOT_SET</transportType>
          </RiLink>
  		  </Equipment>
		</ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session/>
</rpc>
]]>]]>

"""
