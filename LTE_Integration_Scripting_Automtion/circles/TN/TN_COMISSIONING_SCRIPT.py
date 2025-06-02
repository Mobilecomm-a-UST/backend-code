TN_SITEBASIC_SCRIPT_BBU6630_BBU6631 = """
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
          <SecM xmlns="urn:com:ericsson:ecim:ComSecM">
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
              <serverAddress>2401:4900:00d4:0a00:0000:0000:0000:0963</serverAddress>
              <administrativeState>UNLOCKED</administrativeState>
            </NtpServer>
            <NtpServer>	
              <ntpServerId>2</ntpServerId>	
              <serverAddress>2401:4900:00d4:0a00:0000:0000:0000:0962</serverAddress>	
              <administrativeState>UNLOCKED</administrativeState>	
            </NtpServer>
            </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
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
                <address>2401:4900:00d4:0a00:0000:0000:0000:0963</address>
                <port>162</port>
                <administrativeState>UNLOCKED</administrativeState>
              </SnmpTargetV2C>
            </Snmp>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTEUP</routerId>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTECP</routerId>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>OAM</routerId>
            <DnsClient xmlns="urn:com:ericsson:ecim:RtnDnsClient">
              <dnsClientId>1</dnsClientId>
              <serverAddress>2401:4900:00d4:0a00:0000:0000:0000:0962</serverAddress>	
              <serverAddress>2401:4900:00d4:0a00:0000:0000:0000:0963</serverAddress>
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
              <userLabel>User Plane</userLabel>	
            </InterfaceIPv4>	
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
            </InterfaceIPv4>	
          </Router>	
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">	
            <routerId>LTEUP</routerId>	
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">	
              <interfaceIPv4Id>{tnPortId}_UP</interfaceIPv4Id>
              <userLabel>User Plane</userLabel>
              <AddressIPv4>
                <addressIPv4Id>{tnPortId}_UP</addressIPv4Id>
                <address>{LTE_UP_IP}</address>
                </AddressIPv4>	
            </InterfaceIPv4>	
          </Router>	
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">	
            <routerId>LTECP</routerId>	
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">	
              <interfaceIPv4Id>{tnPortId}_CP</interfaceIPv4Id>	
              <AddressIPv4>	
                <addressIPv4Id>{tnPortId}_CP</addressIPv4Id>	
                <address>{LTE_S1_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
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

TN_SITEBASIC_SCRIPT_BBU6651 = """
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
        <dnPrefix>SubNetwork=ONRM_ROOT_MO,SubNetwork=LTE_5G,SubNetwork=Baseband,MeContext={eNodeBName}</dnPrefix>
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
            <routerId>LTE_NR</routerId>
            <ttl>64</ttl>
          </Router>
        </Transport>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <TnPort xmlns="urn:com:ericsson:ecim:ReqTnPort">
              <tnPortId>{tnPortId}</tnPortId>
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
            <vlanPortId>LTE_NR</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>LTE_NR</userLabel>
            <vlanId>{OAM_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_NR</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>NR</interfaceIPv6Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort=LTE_NR</encapsulation>
              <mtu>1500</mtu>
              <userLabel>NR_S1U_OAM</userLabel>
              <AddressIPv6>
                <addressIPv6Id>NR_S1U_OAM</addressIPv6Id>
                <address>{OAM_IP}</address>
                <primaryAddress>true</primaryAddress>
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
              <accessPoint>ManagedElement=1,Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM</accessPoint>
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
                <address>10.142.90.203</address>
                <port>162</port>
                <administrativeState>UNLOCKED</administrativeState>
              </SnmpTargetV2C>
            </Snmp>
            <TimeM xmlns="urn:com:ericsson:ecim:RcsTimeM">
              <timeMId>1</timeMId>
              <Ntp>
                <ntpId>1</ntpId>
                <NtpServer>
                  <ntpServerId>1</ntpServerId>
                  <userLabel>NTP TOD</userLabel>
                  <serverAddress>2401:4900:00d4:0a00:0000:0000:0000:0562</serverAddress>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
              </Ntp>
            </TimeM>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_CP</routerId>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>Node_Internal_F1</routerId>
            <hopLimit>64</hopLimit>
            <pathMtuExpiresIPv6>86400</pathMtuExpiresIPv6>
            <ttl>64</ttl>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_NR</routerId>
            <DnsClient xmlns="urn:com:ericsson:ecim:RtnDnsClient">
              <dnsClientId>1</dnsClientId>
              <dscp>28</dscp>
              <serverAddress>2401:4900:00d4:0a00:0000:0000:0000:0562</serverAddress>
              <serverAddress>2401:4900:00d4:0a00:0000:0000:0000:0563</serverAddress>
            </DnsClient>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>LTE_UP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort=LTE_NR</encapsulation>
              <mtu>1500</mtu>
              <userLabel>LTE_UP</userLabel>
            </InterfaceIPv4>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>LTE_CP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <userLabel>LTE_CP</userLabel>
            <vlanId>{LTE_S1_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_CP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>LTE_CP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort=LTE_CP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>LTE_CP</userLabel>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>Node_Internal_F1</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>NR_CUCP</interfaceIPv4Id>
              <arpTimeout>300</arpTimeout>
              <bfdStaticRoutes>DISABLED</bfdStaticRoutes>
              <loopback />
              <mtu>1500</mtu>
              <pcpArp>6</pcpArp>
            </InterfaceIPv4>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>NR_DU</interfaceIPv4Id>
              <arpTimeout>300</arpTimeout>
              <bfdStaticRoutes>DISABLED</bfdStaticRoutes>
              <loopback />
              <mtu>1500</mtu>
              <pcpArp>6</pcpArp>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_NR</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>LTE_UP</interfaceIPv4Id>
              <AddressIPv4>
                <addressIPv4Id>LTE_UP</addressIPv4Id>
                <address>{LTE_UP_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_CP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>LTE_CP</interfaceIPv4Id>
              <AddressIPv4>
                <addressIPv4Id>LTE_CP</addressIPv4Id>
                <address>{LTE_S1_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>Node_Internal_F1</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>NR_CUCP</interfaceIPv4Id>
              <AddressIPv4>
                <addressIPv4Id>1</addressIPv4Id>
                <address>10.0.0.1/32</address>
                <configurationMode>MANUAL</configurationMode>
                <dhcpClientIdentifierType>AUTOMATIC</dhcpClientIdentifierType>
              </AddressIPv4>
            </InterfaceIPv4>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>NR_DU</interfaceIPv4Id>
              <AddressIPv4>
                <addressIPv4Id>1</addressIPv4Id>
                <address>10.0.0.2/32</address>
                <configurationMode>MANUAL</configurationMode>
                <dhcpClientIdentifierType>AUTOMATIC</dhcpClientIdentifierType>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_NR</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>NR</interfaceIPv6Id>
              <AddressIPv6>
                <addressIPv6Id>X2_ENDC</addressIPv6Id>
                <address>{NR_ENDC_IP}</address>
                <primaryAddress>false</primaryAddress>
              </AddressIPv6>
            </InterfaceIPv6>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>SGW</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_CP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>MME</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_NR</routerId>
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>2</routeTableIPv6StaticId>
              <Dst>
                <dstId>ENM_SGW</dstId>
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

TN_SITEEQUIPMENT_SCRIPT = """
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