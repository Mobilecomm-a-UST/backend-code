DEL_GPL_LMS_DST_SCRIPT = """

lt all
rbs
rbs
confbd+
gs+

$date = `date +%y%m%d_%H%M`

                                                                                                                 
                                                                                                                                                             
lt all                                                                                                                                                       
rbs                                                                                                                                                          
rbs                                                                                                                                                          
                                                                                                                                                             
confb+                                                                                                                                                       
gs+                                                                                                                                                          
                                                                                                                                                             
$date = `date +%y%m%d_%H%M`                                                                                                                                  
                                                                                                                                                             
cvms pre_X2                                                                                                                                                  
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
get Transport=1,Router=LTECP,RouteTableIPv4Static= routeTableIPv4StaticId > $MME_ROUTE                                                                       
                                                                                                                                                             
get Transport=1,Router=LTEUP,RouteTableIPv4Static= routeTableIPv4StaticId > $SGW_ROUTE                                                                       
                                                                                                                                                             
get Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=.*,NextHop= address$ > $X2CP_Nexthop                                                        
                                                                                                                                                             
get Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=.*,NextHop= address$ > $X2UP_Nexthop                                                        
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
st TermPointToENB 0                                                                                                                                          
                                                                                                                                                             
lbl st_group                                                                                                                                                 
                                                                                                                                                             
del Dst=X2                                                                                                                                                   
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
set PowerDistribution=1 controlDomainRef Cabinet=1                                                                                                           
y                                                                                                                                                            
set PowerSupply=1 controlDomainRef Cabinet=1                                                                                                                 
y                                                                                                                                                            
                                                                                                                                                             
set PowerDistribution=1 controlDomainRef Cabinet=1                                                                                                           
y                                                                                                                                                            
set PowerSupply=1 controlDomainRef Cabinet=1                                                                                                                 
y                                                                                                                                                            
                                                                                                                                                             
##### X2-CP ############                                                                                                                                     
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=X2-CP                                                                                        
0.0.0.0/0                                                                                                                                                    
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=X2-CP,NextHop=3                                                                              
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
##### X2-UP ############                                                                                                                                     
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=X2-UP                                                                                        
0.0.0.0/0                                                                                                                                                    
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=X2-UP,NextHop=2                                                                              
$X2UP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
////5G TWAMP////                                                                                                                                             
                                                                                                                                                             
rdel Transport=1,Router=LTEUP,TwampResponder=5                                                                                                               
rdel Transport=1,Router=LTEUP,TwampResponder=6                                                                                                               
rdel Transport=1,Router=LTECP,TwampResponder=5                                                                                                               
rdel Transport=1,Router=LTECP,TwampResponder=6                                                                                                               
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=NR                                                                                                               
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR                                                                                                       
udpPort 4001                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=NR_X2                                                                                                            
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                                                       
udpPort 4001                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
////TWAMP-TN-A////                                                                                                                                           
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=1                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_A_UP,AddressIPv4=TN_A_UP                                                                                             
udpPort 4001                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=2                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_A_UP,AddressIPv4=TN_A_UP                                                                                             
udpPort 4002                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=3                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_A_UP,AddressIPv4=TN_A_UP                                                                                             
udpPort 4003                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
                                                                                                                                                             
////TWAMP-TN-B////                                                                                                                                           
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=1                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_B_UP,AddressIPv4=TN_B_UP                                                                                             
udpPort 4001                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=2                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_B_UP,AddressIPv4=TN_B_UP                                                                                             
udpPort 4002                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=3                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_B_UP,AddressIPv4=TN_B_UP                                                                                             
udpPort 4003                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
////TWAMP-TN-C////                                                                                                                                           
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=1                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_C_UP,AddressIPv4=TN_C_UP                                                                                             
udpPort 4001                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=2                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_C_UP,AddressIPv4=TN_C_UP                                                                                             
udpPort 4002                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=3                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_C_UP,AddressIPv4=TN_C_UP                                                                                             
udpPort 4003                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
                                                                                                                                                             
////TWAMP-TN-D////                                                                                                                                           
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=1                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_D_UP,AddressIPv4=TN_D_UP                                                                                             
udpPort 4001                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=2                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_D_UP,AddressIPv4=TN_D_UP                                                                                             
udpPort 4002                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=3                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_D_UP,AddressIPv4=TN_D_UP                                                                                             
udpPort 4003                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
////TWAMP-TN-E////                                                                                                                                           
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=1                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_E_UP,AddressIPv4=TN_E_UP                                                                                             
udpPort 4001                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=2                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_E_UP,AddressIPv4=TN_E_UP                                                                                             
udpPort 4002                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=3                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_E_UP,AddressIPv4=TN_E_UP                                                                                             
udpPort 4003                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
                                                                                                                                                             
////TWAMP-TN-E////                                                                                                                                           
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=1                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_IDL_B_UP,AddressIPv4=TN_IDL_B_UP                                                                                     
udpPort 4001                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=2                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_IDL_B_UP,AddressIPv4=TN_IDL_B_UP                                                                                     
udpPort 4002                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
crn Transport=1,Router=LTEUP,TwampResponder=3                                                                                                                
ipAddress Router=LTEUP,InterfaceIPv4=TN_IDL_B_UP,AddressIPv4=TN_IDL_B_UP                                                                                     
udpPort 4003                                                                                                                                                 
userLabel                                                                                                                                                    
end                                                                                                                                                          
                                                                                                                                                             
                                                                                                                                                             
////TWAMP-ROUTES///                                                                                                                                          
                                                                                                                                                             
rdel Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=Twamp1                                                                                     
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
rdel Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=Twamp2                                                                                     
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
rdel Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=Twamp3                                                                                     
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=Twamp4                                                                                      
dst 10.61.112.168/29                                                                                                                                         
end                                                                                                                                                          
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=Twamp4,NextHop=7                                                                             
$X2UP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=Twamp5                                                                                      
dst 10.188.27.112/29                                                                                                                                         
end                                                                                                                                                          
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=Twamp5,NextHop=7                                                                             
$X2UP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
ldeb st_group                                                                                                                                                
                                                                                                                                                             
                                                                                                                                                             
////////////////                                                                                                                                             
// SGW ADDITION                                                                                                                                              
///////////////                                                                                                                                              
                                                                                                                                                             
                                                                                                                                                             
get Transport=1,Router=LTEUP,RouteTableIPv4Static= routeTableIPv4StaticId > $SGW_ROUTE                                                                       
                                                                                                                                                             
get Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=.*,NextHop= address$ > $SGW_Nexthop                                                         
                                                                                                                                                             
                                                                                                                                                             
rdel Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW1$                                                                                      
                                                                                                                                                             
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW2                                                                                         
10.155.72.48/32                                                                                                                                              
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW2,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW3                                                                                         
10.206.16.79/32                                                                                                                                              
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW3,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW4                                                                                         
10.206.17.12/32                                                                                                                                              
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW4,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW5                                                                                         
10.206.17.1/32                                                                                                                                               
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW5,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW6                                                                                         
10.0.123.5/32                                                                                                                                                
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW6,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW7                                                                                         
10.206.31.2/32                                                                                                                                               
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW7,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW8                                                                                         
10.0.123.37/32                                                                                                                                               
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW8,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW9                                                                                         
10.0.166.5/32                                                                                                                                                
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW9,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW10                                                                                        
10.0.166.37/32                                                                                                                                               
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW10,NextHop=1                                                                              
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW11                                                                                        
10.0.232.5/32                                                                                                                                                
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW11,NextHop=1                                                                              
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW12                                                                                        
10.50.96.5/32                                                                                                                                                
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW12,NextHop=1                                                                              
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW13                                                                                        
10.50.96.17/32                                                                                                                                               
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW13,NextHop=1                                                                              
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW14                                                                                        
10.50.97.5/32                                                                                                                                                
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW14,NextHop=1                                                                              
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW15                                                                                        
10.75.212.97/32                                                                                                                                              
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW15,NextHop=1                                                                              
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW17                                                                                        
10.92.7.86/32                                                                                                                                                
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=SGW17,NextHop=1                                                                              
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=DEL-NOI-S87-SAE-CUPS-IMS-01                                                                  
10.1.159.80/30                                                                                                                                               
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=DEL-NOI-S87-SAE-CUPS-IMS-01,NextHop=1                                                        
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=DEL-NOI-S87-SAEGW-UP-01                                                                      
10.1.159.66/31                                                                                                                                               
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=DEL-NOI-S87-SAEGW-UP-01,NextHop=1                                                            
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=DEL-NOI-S87-SAEGW-UP-03                                                                      
10.1.159.68/30                                                                                                                                               
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=DEL-NOI-S87-SAEGW-UP-03,NextHop=1                                                            
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=DEL-NOI-S87-SAEGW-UP-07                                                                      
10.1.159.72/29                                                                                                                                               
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=DEL-NOI-S87-SAEGW-UP-07,NextHop=1                                                            
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=POD1                                                                                         
10.58.96.101/32                                                                                                                                              
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=POD1,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=POD2                                                                                         
10.58.96.117/32                                                                                                                                              
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=POD2,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=POD3                                                                                         
10.58.96.133/32                                                                                                                                              
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=POD3,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=POD4                                                                                         
10.58.104.165/32                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=POD4,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=POD5                                                                                         
10.58.104.181/32                                                                                                                                             
cr Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=POD5,NextHop=1                                                                               
$SGW_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
//////////////////////////////                                                                                                                               
///// OSS ADDITION + GATEWAY                                                                                                                                 
//////////////////////////////                                                                                                                               
                                                                                                                                                             
get Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=.*,NextHop= address$ > $OSS_Nexthop                                                                    
                                                                                                                                                             
                                                                                                                                                             
set Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS2 dst 10.3.34.0/23                                                                                  
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS2                                                                                                    
10.3.34.0/23                                                                                                                                                 
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS2,NextHop=1                                                                                          
$OSS_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
set Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM1 dst 10.3.190.0/23                                                                                 
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM1                                                                                                    
10.3.190.0/23                                                                                                                                                
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM1,NextHop=1                                                                                          
$OSS_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM2                                                                                                    
10.3.244.0/24                                                                                                                                                
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM2,NextHop=1                                                                                          
$OSS_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM3                                                                                                    
10.2.66.0/24                                                                                                                                                 
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM3,NextHop=1                                                                                          
$OSS_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM4                                                                                                    
10.2.67.0/24                                                                                                                                                 
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM4,NextHop=1                                                                                          
$OSS_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM                                                                                                     
10.3.190.0/23                                                                                                                                                
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM,NextHop=1                                                                                           
$OSS_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM5                                                                                                    
10.99.165.0/24                                                                                                                                               
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM5,NextHop=1                                                                                          
$OSS_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM6                                                                                                    
10.2.40.0/26                                                                                                                                                 
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM6,NextHop=1                                                                                          
$OSS_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=EEA_ADAPTER                                                                                             
10.6.253.192/27                                                                                                                                              
cr Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=EEA_ADAPTER,NextHop=1                                                                                   
$OSS_Nexthop                                                                                                                                                 
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
                                                                                                                                                             
rdel Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS3                                                                                                  
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
rdel Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS4                                                                                                  
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
rdel Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS5                                                                                                  
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
//////////////////                                                                                                                                           
///ADD Termpoint to 3RD MME                                                                                                                                  
//////////////////                                                                                                                                           
                                                                                                                                                             
                                                                                                                                                             
rdel  ENodeBFunction=1,TermPointToMme=MME_DEL_1                                                                                                              
y                                                                                                                                                            
rdel  ENodeBFunction=1,TermPointToMme=MME_DEL_2                                                                                                              
y                                                                                                                                                            
rdel  ENodeBFunction=1,TermPointToMme=MME_DEL_4                                                                                                              
y                                                                                                                                                            
rdel  ENodeBFunction=1,TermPointToMme=MME_DEL_3                                                                                                              
y                                                                                                                                                            
rdel  ENodeBFunction=1,TermPointToMme=MME_DEL_6                                                                                                              
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
rdel Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME1$                                                                                      
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
rdel Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME2$                                                                                      
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
rdel Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME4$                                                                                      
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
rdel Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME3$                                                                                      
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
rdel Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME6$                                                                                      
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
rdel Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME_1$                                                                                     
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
rdel Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME_2$                                                                                     
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
rdel Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME_4$                                                                                     
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
rdel Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME_3$                                                                                     
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
rdel Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME_6$                                                                                     
y                                                                                                                                                            
y                                                                                                                                                            
                                                                                                                                                             
get Transport=1,Router=LTECP,RouteTableIPv4Static= routeTableIPv4StaticId > $MME_ROUTE                                                                       
get Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=.*,NextHop= address$ > $X2CP_Nexthop                                                        
                                                                                                                                                             
//MME10                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME10-Pri                                                                                    
10.103.44.12/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME10-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME10-Sec                                                                                    
10.103.44.13/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME10-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME10                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME10 ipAddress1 10.103.44.12                                                                                            
set ENodeBFunction=1,TermPointToMme=MME10 ipAddress2 10.103.44.13                                                                                            
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME10                                                                                                                   
y                                                                                                                                                            
//MME11                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME11-Pri                                                                                    
10.103.44.23/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME11-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME11-Sec                                                                                    
10.103.44.24/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME11-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME11                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME11 ipAddress1 10.103.44.23                                                                                            
set ENodeBFunction=1,TermPointToMme=MME11 ipAddress2 10.103.44.24                                                                                            
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME11                                                                                                                   
y                                                                                                                                                            
                                                                                                                                                             
//MME12                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME12-Pri                                                                                    
10.103.44.1/32                                                                                                                                               
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME12-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME12-Sec                                                                                    
10.103.44.2/32                                                                                                                                               
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME12-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME12                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME12 ipAddress1 10.103.44.1                                                                                             
set ENodeBFunction=1,TermPointToMme=MME12 ipAddress2 10.103.44.2                                                                                             
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME12                                                                                                                   
y                                                                                                                                                            
                                                                                                                                                             
//MME13                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME13-Pri                                                                                    
10.103.44.34/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME13-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME13-Sec                                                                                    
10.103.44.35/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME13-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME13                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME13 ipAddress1 10.103.44.34                                                                                            
set ENodeBFunction=1,TermPointToMme=MME13 ipAddress2 10.103.44.35                                                                                            
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME13                                                                                                                   
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
//MME14                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME14-Pri                                                                                    
10.103.10.42/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME14-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME14-Sec                                                                                    
10.103.10.44/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME14-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME14                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME14 ipAddress1 10.103.10.42                                                                                            
set ENodeBFunction=1,TermPointToMme=MME14 ipAddress2 10.103.10.44                                                                                            
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME14                                                                                                                   
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
//MME15                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME15-Pri                                                                                    
10.103.10.32/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME15-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME15-Sec                                                                                    
10.103.10.34/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME15-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME15                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME15 ipAddress1 10.103.10.32                                                                                            
set ENodeBFunction=1,TermPointToMme=MME15 ipAddress2 10.103.10.34                                                                                            
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME15                                                                                                                   
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
st mme                                                                                                                                                       
lbl mme                                                                                                                                                      
wait 5                                                                                                                                                       
ldeb ENodeBFunction=1,TermPointToMme=MME10                                                                                                                   
ldeb ENodeBFunction=1,TermPointToMme=MME11                                                                                                                   
ldeb ENodeBFunction=1,TermPointToMme=MME12                                                                                                                   
ldeb ENodeBFunction=1,TermPointToMme=MME13                                                                                                                   
ldeb ENodeBFunction=1,TermPointToMme=MME14                                                                                                                   
ldeb ENodeBFunction=1,TermPointToMme=MME15                                                                                                                   
st mme                                                                                                                                                       
rdel ENodeBFunction=1,TermPointToMme=MME09                                                                                                                   
rdel ENodeBFunction=1,TermPointToMme=MME_DEL_3                                                                                                               
rdel ENodeBFunction=1,TermPointToMme=MME_DEL_4                                                                                                               
rdel ENodeBFunction=1,TermPointToMme=MME_DEL_5                                                                                                               
rdel ENodeBFunction=1,TermPointToMme=MME_DEL_6                                                                                                               
rdel ENodeBFunction=1,TermPointToMme=MME_DEL_7                                                                                                               
rdel ENodeBFunction=1,TermPointToMme=MME_DEL_8                                                                                                               
rdel ENodeBFunction=1,TermPointToMme=MME_DEL_ULTRA                                                                                                           
                                                                                                                                                             
                                                                                                                                                             
                                                                                                                                                             
!TXN QOS_SCTP                                                                                                                                                
                                                                                                                                                             
set ENodeBFunction=1 dscpLabel 46                                                                                                                            
set ENodeBFunction=1 gtpuErrorIndicationDscp 46                                                                                                              
set ENodeBFunction=1 interEnbCaTunnelDscp 26                                                                                                                 
set ENodeBFunction=1 interEnbUlCompTunnelDscp 26                                                                                                             
set ENodeBFunction=1 s1GtpuEchoDscp 46                                                                                                                       
set ENodeBFunction=1 x2GtpuEchoDscp 46                                                                                                                       
                                                                                                                                                             
cr Transport=1,QosProfiles=1,DscpPcpMap=1                                                                                                                    
set QciTable=default,QciProfilePredefined=qci1$ dscp 34                                                                                                      
set QciTable=default,QciProfilePredefined=qci2$ dscp 34                                                                                                      
set QciTable=default,QciProfilePredefined=qci3$ dscp 26                                                                                                      
set QciTable=default,QciProfilePredefined=qci4$ dscp 26                                                                                                      
set QciTable=default,QciProfilePredefined=qci5$ dscp 46                                                                                                      
set QciTable=default,QciProfilePredefined=qci6$ dscp 32                                                                                                      
set QciTable=default,QciProfilePredefined=qci7$ dscp 40                                                                                                      
set QciTable=default,QciProfilePredefined=qci8$ dscp 30                                                                                                      
set QciTable=default,QciProfilePredefined=qci9$ dscp 26                                                                                                      
set SysM=1,OamTrafficClass=1 dscp 28                                                                                                                         
set SctpProfile= dscp 46                                                                                                                                     
set Ntp=.*,NtpFrequencySync= dscp 46                                                                                                                         
set Ntp=1,NtpFrequencySync= dscp 46                                                                                                                          
set Ntp=2,NtpFrequencySync= dscp 46                                                                                                                          
set EthernetPort=.*  egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                                                            
set EthernetPort=    egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                                                            
                                                                                                                                                             
lt all                                                                                                                                                       
set QosProfiles=1,DscpPcpMap=1 pcp0                                                                                                                          
set QosProfiles=1,DscpPcpMap=1 pcp1                                                                                                                          
set QosProfiles=1,DscpPcpMap=1 pcp2                                                                                                                          
set QosProfiles=1,DscpPcpMap=1 pcp3                                                                                                                          
set QosProfiles=1,DscpPcpMap=1 pcp4                                                                                                                          
set QosProfiles=1,DscpPcpMap=1 pcp5                                                                                                                          
set QosProfiles=1,DscpPcpMap=1 pcp6                                                                                                                          
set QosProfiles=1,DscpPcpMap=1 pcp7                                                                                                                          
                                                                                                                                                             
set Router=.*,InterfaceIPv4=                                egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                     
set Router=.*,InterfaceIPv4=                                ingressQosMarking QosProfiles=1,DscpPcpMap=1                                                     
set Router=LTECP,InterfaceIPv4=TN_.*_CP                      egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                    
set Router=LTEUP,InterfaceIPv4=TN_.*_UP                      egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                    
set Router=OAM,InterfaceIPv4=TN_.*_OAM                       egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                    
set Router=OAM,InterfaceIPv4=TN_.*_ABIS                      egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                    
set Router=OAM,InterfaceIPv4=TN_.*_IUB                       egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                    
set VlanPort=                                               egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                     
set VlanPort=TN_.*_CP                                        egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                    
set VlanPort=TN_.*_OAM                                       egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                    
set VlanPort=TN_.*_UP                                        egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                    
set VlanPort=TN_.*_IUB                                       egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                    
set VlanPort=TN_.*_ABIS                                      egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                    
                                                                                                                                                             
lt all                                                                                                                                                       
                                                                                                                                                             
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58
,59,60,61,62,63                                                                                                                                              
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22,24,26                                                                                                     
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6,8,10,30,32                                                                                                 
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12,14,40                                                                                                     
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4,28                                                                                                         
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16,18,34,42,44                                                                                               
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20,46                                                                                                        
set SctpProfile=Node_Internal_F1  dscp 46                                                                                                                    
set SctpProfile=1 dscp 46                                                                                                                                    
!cr Router=.*,DnsClient=1                                                                                                                                    
set Router=.*,DnsClient=1 dscp 28                                                                                                                            
                                                                                                                                                             
set . egressQosMarking QosProfiles=1,DscpPcpMap=1                                                                                                            
                                                                                                                                                             
set Transport=1,SctpProfile=Node_Internal_F1 alphaIndex 3                                                                                                    
set Transport=1,SctpProfile=Node_Internal_F1 pathMaxRtx 4                                                                                                    
set Transport=1,SctpProfile=Node_Internal_F1 assocMaxRtx 8                                                                                                   
set Transport=1,SctpProfile=Node_Internal_F1 betaIndex 2                                                                                                     
set Transport=1,SctpProfile=Node_Internal_F1 bundlingActivated TRUE                                                                                          
set Transport=1,SctpProfile=Node_Internal_F1 bundlingAdaptiveActivated TRUE                                                                                  
set Transport=1,SctpProfile=Node_Internal_F1 bundlingTimer 0                                                                                                 
set Transport=1,SctpProfile=Node_Internal_F1 cookieLife 60                                                                                                   
set Transport=1,SctpProfile=Node_Internal_F1 dscp 46                                                                                                         
set Transport=1,SctpProfile=Node_Internal_F1 hbMaxBurst 1                                                                                                    
set Transport=1,SctpProfile=Node_Internal_F1 heartbeatActivated TRUE                                                                                         
set Transport=1,SctpProfile=Node_Internal_F1 heartbeatInterval 2000                                                                                          
set Transport=1,SctpProfile=Node_Internal_F1 incCookieLife 30                                                                                                
set Transport=1,SctpProfile=Node_Internal_F1 initARWnd 16384                                                                                                 
set Transport=1,SctpProfile=Node_Internal_F1 maxRto 4000                                                                                                     
set Transport=1,SctpProfile=Node_Internal_F1 initRto 2000                                                                                                    
set Transport=1,SctpProfile=Node_Internal_F1 minRto 1000                                                                                                     
set Transport=1,SctpProfile=Node_Internal_F1 initialHeartbeatInterval 500                                                                                    
set Transport=1,SctpProfile=Node_Internal_F1 maxActivateThr 65535                                                                                            
set Transport=1,SctpProfile=Node_Internal_F1 maxBurst 4                                                                                                      
set Transport=1,SctpProfile=Node_Internal_F1 maxInStreams 2                                                                                                  
set Transport=1,SctpProfile=Node_Internal_F1 maxInitRt 5                                                                                                     
set Transport=1,SctpProfile=Node_Internal_F1 maxOutStreams 2                                                                                                 
set Transport=1,SctpProfile=Node_Internal_F1 maxSctpPduSize 1480                                                                                             
set Transport=1,SctpProfile=Node_Internal_F1 maxShutdownRt 5                                                                                                 
set Transport=1,SctpProfile=Node_Internal_F1 minActivateThr 1                                                                                                
set Transport=1,SctpProfile=Node_Internal_F1 noSwitchback TRUE                                                                                               
set Transport=1,SctpProfile=Node_Internal_F1 pathMaxRtx 4                                                                                                    
set Transport=1,SctpProfile=Node_Internal_F1 primaryPathAvoidance TRUE                                                                                       
set Transport=1,SctpProfile=Node_Internal_F1 primaryPathMaxRtx 0                                                                                             
set Transport=1,SctpProfile=Node_Internal_F1 sackTimer 100                                                                                                   
set Transport=1,SctpProfile=Node_Internal_F1 thrTransmitBuffer 48                                                                                            
set Transport=1,SctpProfile=Node_Internal_F1 thrTransmitBufferCongCeased 85                                                                                  
set Transport=1,SctpProfile=Node_Internal_F1 transmitBufferSize 64                                                                                           
set Transport=1,SctpProfile=Node_Internal_F1 userLabel SCTP                                                                                                  
set Transport=1,SctpProfile=1 alphaIndex 3                                                                                                                   
set Transport=1,SctpProfile=1 pathMaxRtx 4                                                                                                                   
set Transport=1,SctpProfile=1 assocMaxRtx 8                                                                                                                  
set Transport=1,SctpProfile=1 betaIndex 2                                                                                                                    
set Transport=1,SctpProfile=1 bundlingActivated TRUE                                                                                                         
set Transport=1,SctpProfile=1 bundlingAdaptiveActivated TRUE                                                                                                 
set Transport=1,SctpProfile=1 bundlingTimer 0                                                                                                                
set Transport=1,SctpProfile=1 cookieLife 60                                                                                                                  
set Transport=1,SctpProfile=1 dscp 46                                                                                                                        
set Transport=1,SctpProfile=1 hbMaxBurst 1                                                                                                                   
set Transport=1,SctpProfile=1 heartbeatActivated TRUE                                                                                                        
set Transport=1,SctpProfile=1 heartbeatInterval 2000                                                                                                         
set Transport=1,SctpProfile=1 incCookieLife 30                                                                                                               
set Transport=1,SctpProfile=1 initARWnd 16384                                                                                                                
set Transport=1,SctpProfile=1 maxRto 4000                                                                                                                    
set Transport=1,SctpProfile=1 initRto 2000                                                                                                                   
set Transport=1,SctpProfile=1 minRto 1000                                                                                                                    
set Transport=1,SctpProfile=1 initialHeartbeatInterval 500                                                                                                   
set Transport=1,SctpProfile=1 maxActivateThr 65535                                                                                                           
set Transport=1,SctpProfile=1 maxBurst 4                                                                                                                     
set Transport=1,SctpProfile=1 maxInStreams 2                                                                                                                 
set Transport=1,SctpProfile=1 maxInitRt 5                                                                                                                    
set Transport=1,SctpProfile=1 maxOutStreams 2                                                                                                                
set Transport=1,SctpProfile=1 maxSctpPduSize 1480                                                                                                            
set Transport=1,SctpProfile=1 maxShutdownRt 5                                                                                                                
set Transport=1,SctpProfile=1 minActivateThr 1                                                                                                               
set Transport=1,SctpProfile=1 noSwitchback TRUE                                                                                                              
set Transport=1,SctpProfile=1 pathMaxRtx 4                                                                                                                   
set Transport=1,SctpProfile=1 primaryPathAvoidance TRUE                                                                                                      
set Transport=1,SctpProfile=1 primaryPathMaxRtx 0                                                                                                            
set Transport=1,SctpProfile=1 sackTimer 100                                                                                                                  
set Transport=1,SctpProfile=1 thrTransmitBuffer 48                                                                                                           
set Transport=1,SctpProfile=1 thrTransmitBufferCongCeased 85                                                                                                 
set Transport=1,SctpProfile=1 transmitBufferSize 64                                                                                                          
set Transport=1,SctpProfile=1 userLabel SCTP                                                                                                                 
set  Fm=1  heartbeatInterval 100                                                                                                                             




cvms Pre_mcom


rdel UtranFreqRelation=10682
rdel ENodeBFunction=1,UtraNetwork=1,UtranFrequency=10682
rdel UtranFreqRelation=10657
rdel ENodeBFunction=1,UtraNetwork=1,UtranFrequency=10657
rdel EUtranFreqRelation=265
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=265
rdel EUtranFreqRelation=39050
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39050
rdel EUtranFreqRelation=39200
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39200
rdel EUtranFreqRelation=39025
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39025
rdel EUtranFreqRelation=39175
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39175
rdel EUtranFreqRelation=3665
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3665
rdel EUtranFreqRelation=1300
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1300
rdel EUtranFreqRelation=39000
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39000
rdel EUtranFreqRelation=39006
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39006
rdel EUtranFreqRelation=39144
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39144
rdel EUtranFreqRelation=39001
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39001
rdel EUtranFreqRelation=39199
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39199
rdel EUtranFreqRelation=39051
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39051
rdel EUtranFreqRelation=39149
rdel ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39149


rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=41$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=42$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=43$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=44$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=45$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=46$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=47$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=48$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=49$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=52$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=53$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=54$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=55$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=56$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=57$
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=553
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=554
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=555
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=556
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=557
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=558
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=559
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=560
rdel ENodeBFunction=1,GeraNetwork=1,GeranFrequency=561



cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=51
51
0

set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=51 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1


cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39150
39150
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39294
39294
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1346
1346
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3676
3676
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=240
240
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1345
1345
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39151
39151

unset all
$Tab[1] = F1
$Tab[2] = F3
$Tab[3] = F8
$Tab[4] = T2
$Tab[5] = T1
$Tab[6] = SMALL
mr F1
mr F3
mr F8
mr T2
mr T1
mr SMALL
ma F1 EUtranCellFDD earfcndl 240
ma F3 EUtranCellFDD earfcndl 1346
ma F8 EUtranCellFDD earfcndl 3676
ma T2 EUtranCellTDD earfcn 39150
ma T1 EUtranCellTDD earfcn 39294
ma SMALL EUtranCellTDD earfcn 39151

set GeranFreqGroupRelation=1 cellReselectionPriority 1
set EUtranFreqRelation=3676 cellReselectionPriority 3
set EUtranFreqRelation=1346 cellReselectionPriority 4
set EUtranFreqRelation=240 cellReselectionPriority 5
set EUtranFreqRelation=39294 cellReselectionPriority 6
set EUtranFreqRelation=39150 cellReselectionPriority 7
set EUtranFreqRelation=1345 cellReselectionPriority 7
set EUtranFreqRelation=39151 cellReselectionPriority 7

func EURel_240
for $mo in $Tab[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=240
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=240
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=240
  5
 fi 
done
endfunc

func EURel_1346
for $mo in $Tab[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=1346
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=1346
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1346
  4
 fi 
done
endfunc

func EURel_1345
for $mo in $Tab[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=1345
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=1345
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1345
  4
 fi 
done
endfunc


func EURel_3676
for $mo in $Tab[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=3676
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=3676
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3676
  3
 fi 
done
endfunc

func EURel_39150
for $mo in $Tab[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=39150
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39150
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39150
  7
 fi 
done
endfunc

func EURel_39151
for $mo in $Tab[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=39151
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39151
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39151
  7
 fi 
done
endfunc

func EURel_39294
for $mo in $Tab[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=39294
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39294
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39294
  6
 fi 
done
endfunc

func Gran_Rel
for $mo in $Tab[$i]
 $mordn = rdn($mo)
 pr $mordn,GeranFreqGroupRelation=1
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,GeranFreqGroupRelation=1
  ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
  1
 fi 
done
endfunc

func FreqPm_Rel
for $mo in $Tab[$i]
 $mordn = rdn($mo)
 pr ENodeBFunction=1,$mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1
  fi 
done
endfunc

cr ENodeBFunction=1,GeraNetwork=1
cr ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
1 #frequencyGroupId
rdel GeranFrequency=4[1-9]$

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=51
51
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=75
75
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=76
76
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=77
77
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=78
78
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=79
79
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=80
80
0


set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=51 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=75 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=76 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=77 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=78 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=79 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=80 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=562
562
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=563
563
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=564
564
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=565
565
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=566
566
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=567
567
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=568
568
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=569
569
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=570
570
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=571
571
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=572
572
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=596
596
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=562 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=563 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=564 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=565 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=566 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=567 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=568 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=569 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=570 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=571 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=572 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=596 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1

 
for $i = 1 to 6 
##########Relation with 240: ######
EURel_240
##########Relation with 1346: ######
EURel_1346
##########Relation with 1345: ######
EURel_1345
##########Relation with 3676: ######
EURel_3676
##########Relation with 39150: ######
EURel_39150
##########Relation with 39151: ######
EURel_39151
##########Relation with 39294: ######
EURel_39294
##########Relation with 2G: ######
Gran_Rel
##########Relation with FreqPm: ######
FreqPm_Rel
done  


#CommonParameter

set EUtranFreqRelation=1346 allowedmeasbandwidth 25
set EUtranFreqRelation=39150 allowedmeasbandwidth 100
set EUtranFreqRelation=39294 allowedmeasbandwidth 50
set EUtranFreqRelation=3676 allowedmeasbandwidth 25
set EUtranFreqRelation=240 allowedmeasbandwidth 50
set EUtranFreqRelation=1345 allowedmeasbandwidth 25
set EUtranFreqRelation=39151 allowedmeasbandwidth 100

set EUtranFreqRelation=1346 anrMeasOn true
set EUtranFreqRelation=39150 anrMeasOn true
set EUtranFreqRelation=39294 anrMeasOn true
set EUtranFreqRelation=3676 anrMeasOn true
set EUtranFreqRelation=240 anrMeasOn true

set . maxNoPciReportsEvent 30
set . maxTimeEventBasedPciConf 30
set . measuringEcgiWithAgActive false

set . anrUesEUtraIntraFMax 0
set . anrUesThreshInterFMax 0
set . cellAddRsrpThresholdEutran -1240
set . cellAddRsrqThresholdEutran -1530
set . cellAddEcNoThresholdUtranDelta -10
set . cellAddRscpThresholdUtranDelta -1
set . anrUesEUtraIntraFMin 0
set . anrUesThreshInterFMin 0
set AnrFunction=1 removeNcellTime 1
set AnrFunction=1 removeNenbTime 1
set AnrFunction=1 removeNrelTime 1
set AnrFunction=1 cellRelHoAttRateThreshold 15
set AnrFunction=1 problematicCellPolicy 1
set AnrFunction=1 probCellDetectMedHoSuccTime 2
set AnrFunction=1 probCellDetectLowHoSuccTime 4
set AnrFunction=1 probCellDetectMedHoSuccThres 50
set AnrFunction=1 probCellDetectLowHoSuccThres 10
set AnrFunction=1,AnrFunctionEUtran=1 anrInterFreqState 1
set AnrFunction=1,AnrFunctionEUtran=1 anrIntraFreqState 1
set . anrStateUtran 1

set . selectionPolicyUlWeighting 50
set . noOfEnhAdptReTxCand -1



set . pZeroNominalPusch -100
set . pZeroNominalPucch -110
set . alpha 10
set . eUlFssSwitchThresh 30

set . bothA5RsrpRsrqCheck True
set . hysteresisA2CriticalRsrq 100
set . timeandphasesynchcritical False



# UL COMP
cr ENodeBFunction=1,UlCompGroup=1
ENodeBFunction=1,SectorCarrier=7 ENodeBFunction=1,SectorCarrier=8 ENodeBFunction=1,SectorCarrier=9
deb ENodeBFunction=1,UlCompGroup=1

set QciTable=default,QciProfilePredefined=qci1 rlfProfileRef RlfProfile=1

set QciTable=default,QciProfilePredefined=QCI1 ResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI7 ResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI6 ResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI8 ResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI9 ResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci6 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci8 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci9 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci7 dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI1 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=QCI2 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=QCI5 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams b2Threshold2EcNoUtraOffset=0
set QciTable=default,QciProfilePredefined=QCI6 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI8 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI9 dlResourceAllocationStrategy 1
set QciProfilePredefined=qci1 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciProfilePredefined=qci2 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=2
set QciProfilePredefined=qci5 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=QCI6 schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI7 schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI8 schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI9 schedulingAlgorithm 4
lset QciTable=default,QciProfilePredefined=qci1 drxProfileRef DrxProfile=1
lset QciTable=default,QciProfilePredefined=qci2 drxProfileRef DrxProfile=2
lset QciTable=default,QciProfilePredefined=qci5 drxProfileRef DrxProfile=0
set QciTable=default,QciProfilePredefined=qci5              tReorderingUl 60
set QciTable=default,QciProfilePredefined=qci6             tReorderingUl 60
set QciTable=default,QciProfilePredefined=qci6              logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci7              logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci8              logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci9              logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set DataRadioBearer dlMaxRetxThreshold 32
set DataRadioBearer tPollRetransmitDl 80
set DataRadioBearer tPollRetransmitUl 80
set DataRadioBearer ulMaxRetxThreshold 32
set ENodeBFunction rrcConnReestActive 1
set . tRelocOverall 20
set ENodeBFunction tS1HoCancelTimer 3
set ENodeBFunction=1 s1HODirDataPathAvail true
set Rcs=1 tInactivityTimer 10
set Rrc=1 t301 2000
set Rrc=1 t300 2000
set Rrc=1 t304 2000
set Rrc=1 t320 30
set Rrc=1  tRrcConnectionReconfiguration 12
set SignalingRadioBearer dlMaxRetxThreshold 32
set SignalingRadioBearer tPollRetransmitDl 80
set SignalingRadioBearer tPollRetransmitUl 80
set SignalingRadioBearer ulMaxRetxThreshold 32
set Rcs=1 rlcDlDeliveryFailureAction 2
set QciProfilePredefined=qci6 counterActiveMode 0
set QciProfilePredefined=qci7 counterActiveMode 0
set QciProfilePredefined=qci8 counterActiveMode 0
set QciProfilePredefined=qci9 counterActiveMode 0
set AdmissionControl dlAdmDifferentiationThr 750
set AdmissionControl ulAdmDifferentiationThr 750
lset ENodeBFunction=1,DrxProfile=1$ drxRetransmissionTimer 2
lset ENodeBFunction=1,DrxProfile=2$ drxRetransmissionTimer 1
lset ENodeBFunction=1,DrxProfile=0$ drxRetransmissionTimer 4
lset ENodeBFunction=1,DrxProfile=1$ longDrxCycle 3
lset ENodeBFunction=1,DrxProfile=2$ longDrxCycle 3
lset ENodeBFunction=1,DrxProfile=0$ longDrxCycle 9
lset ENodeBFunction=1,DrxProfile=1$ longDrxCycleonly 3
lset ENodeBFunction=1,DrxProfile=2$ longDrxCycleonly 3
lset ENodeBFunction=1,DrxProfile=0$ longDrxCycleonly 9
lset ENodeBFunction=1,DrxProfile=1$ onDurationTimer 7
lset ENodeBFunction=1,DrxProfile=2$ onDurationTimer 6
lset ENodeBFunction=1,DrxProfile=0$ onDurationTimer 7
lset ENodeBFunction=1,DrxProfile=1$ shortDrxCycle 7
lset ENodeBFunction=1,DrxProfile=2$ shortDrxCycle 7
lset ENodeBFunction=1,DrxProfile=0$ shortDrxCycle 9
lset ENodeBFunction=1,DrxProfile=1$ shortDrxCycleTimer 0
lset ENodeBFunction=1,DrxProfile=2$ shortDrxCycleTimer 0
lset ENodeBFunction=1,DrxProfile=0$ shortDrxCycleTimer 1
lset QciTable=default,QciProfilePredefined=qci1 drxProfileRef DrxProfile=1
lset QciTable=default,QciProfilePredefined=qci2 drxProfileRef DrxProfile=2
lset QciTable=default,QciProfilePredefined=qci5 drxProfileRef DrxProfile=0
lset ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=2$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=0$ drxInactivityTimer 14
set ENodeBFunction alignTtiBundWUlTrigSinr 1
set RadioBearerTable=default,MACConfiguration=1 ulTtiBundlingMaxHARQTx 7
set QciTable=default,QciProfilePredefined=QCI1 PdbOffset 100
set QciTable=default,QciProfilePredefined=QCI2 PdbOffset 50
set QciTable=default,QciProfilePredefined=QCI5 PdbOffset 0
set QciTable=default,QciProfilePredefined=QCI1 rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI2 rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI5 rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI1 rlfPriority 10
set QciTable=default,QciProfilePredefined=qci1 harqPriority 1
set QciTable=default,QciProfilePredefined=qci1 dlMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=qci1 ulMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=qci1 tReorderingDl 120
set QciTable=default,QciProfilePredefined=QCI1 aqmMode 2
set QciTable=default,QciProfilePredefined=QCI2 aqmMode 2
set QciTable=default,QciProfilePredefined=QCI5 aqmMode 0
set QciTable=default,QciProfilePredefined=QCI1 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI2 dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI5 dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=QCI1 inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI2 inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI5 inactivityTimerOffset 0
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams b2Threshold2EcNoUtraOffset=0
set QciTable=default,QciProfilePredefined=QCI1 resourcetype 1
set QciTable=default,QciProfilePredefined=QCI2 resourcetype 1
set QciTable=default,QciProfilePredefined=QCI5 resourcetype 0
set QciTable=default,QciProfilePredefined=QCI1 rlcMode 1
set QciTable=default,QciProfilePredefined=QCI2 rlcMode 1
set QciTable=default,QciProfilePredefined=QCI5 rlcMode 0
set QciTable=default,QciProfilePredefined=QCI1 rohcEnabled 1
set QciTable=default,QciProfilePredefined=QCI2 rohcEnabled 0
set QciTable=default,QciProfilePredefined=QCI5 rohcEnabled 0
set QciTable=default,QciProfilePredefined=QCI1 schedulingAlgorithm 6
set QciTable=default,QciProfilePredefined=QCI2 schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=QCI5 schedulingAlgorithm 0
set QciTable=default,QciProfilePredefined=QCI1 serviceType 1
set QciTable=default,QciProfilePredefined=QCI2 serviceType 0
set QciTable=default,QciProfilePredefined=QCI5 serviceType 2
set QciTable=default,QciProfilePredefined=QCI1 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI2 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI5 absPrioOverride 1

set QciTable=default,QciProfilePredefined=qci1 drxPriority 99
set QciTable=default,QciProfilePredefined=qci2 drxPriority 100
set QciTable=default,QciProfilePredefined=qci5 drxPriority 1
set QciTable=default,QciProfilePredefined=QCI1 Priority 1
set QciTable=default,QciProfilePredefined=QCI2 Priority 4
set QciTable=default,QciProfilePredefined=QCI5 Priority 2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a1ThresholdRsrpPrimOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a2ThresholdRsrpPrimOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold1RsrpOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold2RsrpOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams b2Threshold1RsrpUtraOffset=2
set QciTable=default,QciProfilePredefined=QCI1 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI2 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI5 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI1 dscp 34
set QciTable=default,QciProfilePredefined=QCI2 dscp 34
set QciTable=default,QciProfilePredefined=QCI5 dscp 46
set QciTable=default,QciProfilePredefined=qci1 tReorderingUl 50
set QciTable=default,QciProfilePredefined=QCI1 Pdb 80
set QciTable=default,QciProfilePredefined=QCI2 Pdb 150
set QciTable=default,QciProfilePredefined=QCI5 Pdb 100
set QciTable=default,QciProfilePredefined=QCI2 dlMinBitRate 384
set QciTable=default,QciProfilePredefined=QCI2 UlMinBitRate 384
set QciProfilePredefined=qci1 counterActiveMode 0
set QciProfilePredefined=qci2 counterActiveMode 0
set QciProfilePredefined=qci5 counterActiveMode 0
set QciTable=default,QciProfilePredefined=qci1 rlfProfileRef RlfProfile=1
set RlfProfile=1$ n310 10
set RlfProfile=1$ n311 1
set RlfProfile=1$ t301 1000
set RlfProfile=1$ t310 500
set RlfProfile=1$ t311 5000
set RlfProfile=0$ n310 20
set RlfProfile=0$ n311 1
set RlfProfile=0$ t301 2000
set RlfProfile=0$ t310 2000
set RlfProfile=0$ t311 10000
set RadioBearerTable=default,SignalingRadioBearer=1 tReorderingUl 35
set Rrc=1 t311 5000
set Rrc=1 tRrcConnReest 2
set Rrc=1 tWaitForRrcConnReest 9
cr ENodeBFunction=1,TimerProfile=0
6	
8
3
10
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 timerProfileRef ENodeBFunction=1,TimerProfile=0
set TimerProfile=0                                          tWaitForRrcConnReest 6
set TimerProfile=0                                          tRrcConnectionReconfiguration 12
set TimerProfile=0                                          tRrcConnReest 3
set TimerProfile=0                                          tRelocOverall 20
set RadioBearerTable=default,MACConfiguration=1 ulMaxHARQTx 5
lset ENodeBFunction=1,DrxProfile=1$ drxState 0
set ENodeBFunction=1 zzzTemporary52 1
set EUtranFreqRelation=.* lbBnrPolicy 2
set LoadBalancingFunction=1 lbCeiling 500
set LoadBalancingFunction=1 lbThreshold 20
set LoadBalancingFunction=1 lbHitRateEUtranAddThreshold 5
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeIntensity 10
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeThreshold 10
set LoadBalancingFunction=1 lbHitRateEUtranRemoveThreshold 2
set LoadBalancingFunction=1 lbMeasScalingLimit 30
set LoadBalancingFunction=1 lbRateOffsetCoefficient 320
set LoadBalancingFunction=1 lbRateOffsetLoadThreshold 1000
set QciTable=default,QciProfilePredefined=qci1              qciSubscriptionQuanta 60
set QciTable=default,QciProfilePredefined=qci2              qciSubscriptionQuanta 384
set QciTable=default,QciProfilePredefined=qci5              qciSubscriptionQuanta 1
set QciTable=default,QciProfilePredefined=qci6              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci7              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci8              qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci9              qciSubscriptionQuanta 200
set AutoCellCapEstFunction=1 useEstimatedCellCap true
set QciTable=default,QciProfilePredefined=QCI6 dscp 26
set QciTable=default,QciProfilePredefined=QCI7 dscp 26
set QciTable=default,QciProfilePredefined=QCI8 dscp 26
set QciTable=default,QciProfilePredefined=QCI9 dscp 26
set QciTable=default,QciProfilePredefined=QCI6 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI7 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI8 absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI9 absPrioOverride 0

set QciProfilePredefined=qci6 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciProfilePredefined=qci7 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciProfilePredefined=qci8 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciProfilePredefined=qci9 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set AnrFunction=1,AnrFunctionEUtran=1                       lbCellOffloadCapacityPolicy  30000
set ENodeBFunction=1 zzzTemporary55 -2000000000
set ENodeBFunction=1 dnsLookupOnTai 1
set ENodeBFunction=1 x2SetupTwoWayRelations true
set ENodeBFunction=1 csfbMeasFromIdleMode true
set ENodeBFunction=1 x2GtpuEchoDscp 46
set ENodeBFunction=1 s1GtpuEchoDscp 46
set CarrierAggregationFunction=1                            dynamicSCellSelectionMethod 2
set RadioBearerTable=default,MACConfiguration=1             dlMaxHARQTx  4
set AnrFunction=1                                           cellRelHoAttRateThreshold 15
set AnrFunction=1                                           probCellDetectLowHoSuccTime 4
set AnrFunction=1                                           probCellDetectMedHoSuccTime 2
set ENodeBFunction=1                                        enabledUlTrigMeas True
set Paging=1                                                pagingDiscardTimerDrxNb 3
set Paging=1                                                maxNoOfPagingRecords 7 
set Paging=1                                          	    maxNoOfPagingRecordsNb 2 
set CarrierAggregationFunction=1                            fourLayerMimoPreferred false
set AnrFunction=1,AnrFunctionUtran=1                        hoAllowedUtranPolicy true
set AnrFunction=1,AnrFunctionEUtran=1                       x2SetupPolicy     true
set AnrFunction=1,AnrFunctionEUtran=1                       hoAllowedEutranPolicy true 
set AntennaUnitGroup=.*,RfBranch=.*          dlTrafficDelay -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 
set AntennaUnitGroup=.*,RfBranch=.*          ulTrafficDelay  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 

#CA
set LoadBalancingFunction=1 lbDiffCaOffset 100
set CarrierAggregationFunction caRateAdjustCoeff 5
set CarrierAggregationFunction waitForCaOpportunity 2000
set CarrierAggregationFunction sCellScheduleSinrThres 0
set CarrierAggregationFunction sCellActDeactDataThres 20
set CarrierAggregationFunction sCellActDeactDataThresHyst 20
set CarrierAggregationFunction sCellDeactProhibitTimer 50
set CarrierAggregationFunction causagelimit 200
set CarrierAggregationFunction sCellActProhibitTimer 10
set CarrierAggregationFunction caPreemptionThreshold 50
set CarrierAggregationFunction sCellSelectionMode 0
set LoadBalancingFunction lbCaThreshold 2000
set LoadBalancingFunction lbCaCapHysteresis 20
set CarrierAggregationFunction pdcchEnhancedLaForVolte False
set . ulTransNwBandwidth 2000

#CommonParameter

set . otdoaSuplActive True
set . prsMutingPatternLen 4
set . puschNcpChannelEstWindowSize 1

set . hysteresisA5RsrqOffset 0
set .  ul256qamEnabled False
set .  outOfCoverageSparseGrantingBsr 8
set EUtranCellTDD interferenceThresholdSinrClpc -100
set EUtranCellTDD rxSinrTargetClpc 20




set EUtranFreqRelation=1346 anrMeasOn true
set EUtranFreqRelation=39150 anrMeasOn true
set EUtranFreqRelation=39294 anrMeasOn true
set EUtranFreqRelation=3676 anrMeasOn true
set EUtranFreqRelation=240 anrMeasOn true

set EUtranFreqRelation=39150 anrMeasOn true
set EUtranFreqRelation=39294 anrMeasOn true

set . maxNoPciReportsEvent 30
set . maxTimeEventBasedPciConf 30
set . measuringEcgiWithAgActive false

set . anrUesEUtraIntraFMax 0
set . anrUesThreshInterFMax 0
set . cellAddRsrpThresholdEutran -1240
set . cellAddRsrqThresholdEutran -1530
set . cellAddEcNoThresholdUtranDelta -10
set . cellAddRscpThresholdUtranDelta -1
set . anrUesEUtraIntraFMin 0
set . anrUesThreshInterFMin 0
set AnrFunction=1 cellRelHoAttRateThreshold 15
set AnrFunction=1 problematicCellPolicy 1
set AnrFunction=1 probCellDetectMedHoSuccTime 2
set AnrFunction=1 probCellDetectLowHoSuccTime 4
set AnrFunction=1 probCellDetectMedHoSuccThres 50
set AnrFunction=1 probCellDetectLowHoSuccThres 10
set AnrFunction=1,AnrFunctionEUtran=1 anrInterFreqState 1
set AnrFunction=1,AnrFunctionEUtran=1 anrIntraFreqState 1
set . anrStateUtran 1
set . cioLowerLimitAdjBySon -6
set . cioUpperLimitAdjBySon 6

# UL COMP
cr ENodeBFunction=1,UlCompGroup=1
ENodeBFunction=1,SectorCarrier=7 ENodeBFunction=1,SectorCarrier=8 ENodeBFunction=1,SectorCarrier=9
deb ENodeBFunction=1,UlCompGroup=1


set  EUtranCellTDD=*.*,EUtranFreqRelation=1346*.*,EUtranCellRelation=40410-9 coverageIndicator 0
set  EUtranCellTDD=*.*,EUtranFreqRelation=1346*.*,EUtranCellRelation=40410-9 sCellCandidate 0 
set EUtranCellTDD=DL_E_T2_.*,EUtranFreqRelation=39294,EUtranCellRelation=40410-9 sCellCandidate 1
set EUtranCellTDD=DL_E_T1_.*,EUtranFreqRelation=39150,EUtranCellRelation=40410-9 sCellCandidate 1



lset UeMeasControl PrioOffsetPerQci qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,offsetPerQciPrio=7


##T2-TDD20 Parameters

get ENodeBFunction=1,EUtranCellTDD earfcn 39150
if $nr_of_mos > 0
for $mo in T2
    $mordn = rdn($mo)
set $mordn cellRange 6
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp   -106
set $mordn, SystemInformationBlock3 snonintrasearch=8
set $mordn, SystemInformationBlock3 qhyst=4
set $mordn,UeMeasControl=1,ReportConfigEUtraIFBestCell=1 triggerQuantityA3 0
set $mordn CfraEnable True
set $mordn pdcchCfiMode 5
set $mordn dlInterferenceManagementActive TRUE
set $mordn crsgain 0
set $mordn pdschTypeBGain 0
set $mordn  specialSubframePattern 7
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1 a3offsetAnrDelta 0
set $mordn,UeMeasControl=1,ReportConfigA5=1,ReportConfigA5Anr=1 a5Threshold1RsrpAnrDelta 1
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrq -195
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -170
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -190
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrq -195
set $mordn  highSpeedUEActive False
set $mordn  prsPowerBoosting 3
set $mordn,UeMeasControl=1 ueMeasurementsActive 1
set $mordn pdcchpowerboostmax 2
set $mordn noOfChannelSelectionsets 6
set $mordn,EUtranFreqRelation=.* caTriggeredRedirectionActive false
set $mordn,EUtranFreqRelation=39294 caTriggeredRedirectionActive false
set $mordn,EUtranFreqRelation=39294 a3RsrpFreqOffsetAdjustment 0
set $mordn,EUtranFreqRelation=39150,EUtranCellRelation=40410.*sCellCandidate    1
set $mordn,EUtranFreqRelation=39294,EUtranCellRelation=40410.*sCellCandidate    1
set $mordn  sCellHandlingAtVolteCall 1
set $mordn  transmissionMode 4
set $mordn  advCellSupAction 2
set $mordn  advCellSupSensitivity 25
set $mordn covTriggerdBlindHoAllowed 0
set $mordn  mobCtrlAtPoorCovActive true
set $mordn  pMaxServingCell 1000
set $mordn  preambleInitialReceivedTargetPower -110
set $mordn  ul64qamEnabled True
set $mordn  pZeroNominalPucch -110
set $mordn  pZeroNominalPusch -100
set $mordn  Alpha 10
set $mordn  pdcchLaGinrMargin 40
set $mordn  qRxLevMinOffset 1000
set $mordn  SystemInformationBlock3 qhyst=4
set $mordn  SystemInformationBlock3 snonintrasearch=8
set $mordn  SystemInformationBlock6 tReselectionutra=4
set $mordn  threshServingLow 8
set $mordn  qQualMin -34
set $mordn  qQualMinOffset 0
set $mordn tTimeAlignmentTimer 0
set $mordn,EUtranFreqRelation=.* qoffsetfreq 0
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,EUtranFreqRelation=.* tReselectionEutra 1
set $mordn,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set $mordn,UeMeasControl=1,ReportConfigA5=1 triggerquantitya5 0
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 a3offset 30
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 480
set $mordn,UeMeasControl=1,ReportConfigEUtraIFBestCell=1 triggerQuantityA3 0
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set $mordn,UeMeasControl=1 excludeInterFreqAtCritical True
set $mordn pdcchTargetBler 24
set $mordn pdcchCovImproveDtx 1
set $mordn pdcchCovImproveSrb false
set $mordn pdcchCovImproveQci1 1
set $mordn  adaptiveCfiHoProhibit 0
set $mordn allocThrPucchFormat1 50
set $mordn allocTimerPucchFormat1 50
set $mordn deallocThrPucchFormat1 100
set $mordn deallocTimerPucchFormat1 6000
set $mordn drxActive true
set $mordn  ulBlerTargetEnabled true
set $mordn  pdcchTargetBlerVolte 18
set $mordn  dlBlerTargetEnabled true
set $mordn  enableServiceSpecificHARQ true
set $mordn  pdcchOuterLoopInitialAdjVolte -46
set $mordn  pdcchOuterLoopUpStepVolte 9
set $mordn  tReorderingAutoConfiguration true
set $mordn  ulHarqVolteBlerTarget 3
set $mordn pdcchOuterLoopInitialAdj -70
set $mordn pdcchOuterLoopInitialAdjPCell -70
set $mordn pdcchOuterLoopUpStep 8
set $mordn pdcchOuterLoopUpStepPCell 6
set $mordn pdcchTargetBlerPCell 22
set $mordn,UeMeasControl=1,ReportConfigSearch=1 inhibitA2SearchConfig 0
set $mordn,UeMeasControl=1 measQuantityUtraFDD 1
set $mordn,UeMeasControl=1 ueMeasurementsActive 1
set $mordn enableSinrUplinkClpc 1
set $mordn,UeMeasControl=1 ueMeasurementsActiveIF true
set $mordn,UeMeasControl=1 ueMeasurementsActiveGERAN false
set $mordn,UeMeasControl=1                  a5B2MobilityTimer 0
set $mordn cellCapMaxCellSubCap 60000
set $mordn cellCapMinCellSubCap 1000
set $mordn  cellCapMinMaxWriProt true
set $mordn cellSubscriptionCapacity 24000
set $mordn,UeMeasControl=1                  inhibitB2RsrqConfig true
set $mordn,EUtranFreqRelation  interFreqMeasType 0
set $mordn,EUtranFreqRelation=39294  interFreqMeasType 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearch  40 
set $mordn,EUtranFreqRelation=.*,EUtranCellRelation=.* lbBnrAllowed true
set $mordn SystemInformationBlock3 snonintrasearchQ=0
set $mordn,EUtranFreqRelation=.* mobilityAction 1
set $mordn  	lbEUtranCellOffloadCapacity  30000
set TDD mappingInfo mappingInfoSIB3=1
set TDD mappingInfo mappingInfoSIB4=2
set TDD mappingInfo mappingInfoSIB5=3
set TDD mappingInfo mappingInfoSIB6=4
set TDD mappingInfo mappingInfoSIB7=5
set $mordn,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10
set $mordn                                  changeNotification changeNotificationSIB16=true
set $mordn                                  changeNotification changeNotificationSIB15=true
set $mordn                                  changeNotification changeNotificationSIB8=true
set $mordn  commonSrPeriodicity 20
set $mordn  dlFrequencyAllocationProportion 100
set $mordn  dl256QamEnabled true
set $mordn  servOrPrioTriggeredIFHo 0
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrp 4
set $mordn                                   hoOptAdjThresholdAbs 5
set $mordn                                   hoOptAdjThresholdPerc 50
set $mordn                                   hoOptStatTime  24
set $mordn,MimoSleepFunction=1              switchUpMonitorDurTimer 15
set $mordn,UeMeasControl=1,ReportConfigEUtraBadCovPrim=1 a2ThresholdRsrpPrim -140
set $mordn                                  ns05FullBandUsersInCellThres 1
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrq 11
set $mordn,EUtranFreqRelation=.*          allowedPlmnList   mcc=404,mnc=10,mncLength=2
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 maxReportCellsPm 8
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 reportIntervalPm 5
set $mordn  bsrThreshold 100
set $mordn  noOfUlImprovedUe 2
##1345 & 39151
set $mordn,EUtranFreqRelation=1345 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=1345 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=1345 voicePrio  7
set $mordn,EUtranFreqRelation=1345 a5Thr1RsrpFreqOffset 11
set $mordn,EUtranFreqRelation=1345 a5Thr2RsrpFreqOffset 4
set $mordn,EUtranFreqRelation=1345  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1345 lbA5Thr1RsrpFreqOffset  97
set $mordn,EUtranFreqRelation=1345 threshXHigh 10
set $mordn,EUtranFreqRelation=1345 qRxLevMin -124
set $mordn,EUtranFreqRelation=39151 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39151 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=39151 voicePrio  7
set $mordn,EUtranFreqRelation=39151 a5Thr1RsrpFreqOffset 13
set $mordn,EUtranFreqRelation=39151 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39151  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39151 lbA5Thr1RsrpFreqOffset  97
set $mordn,EUtranFreqRelation=39151 threshXHigh 10
set $mordn,EUtranFreqRelation=39151 qRxLevMin -124
##TD20 SINR LMS
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2UlSearchThreshold 40
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2UlSearch 20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1UlSearch 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlSearch 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2UlCriticalThreshold -150
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2UlCritical 150
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlCritical 480
set $mordn ulTrigActive True
set . enabledUlTrigMeas True
set $mordn,UeMeasControl=1 targetA2UlSearchOffset 20
set $mordn,UeMeasControl=1 ulSinrOffset 30
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold1Rsrp -44
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold2Rsrp -116
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 hysteresisA5 20
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 reportIntervalA5 12
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 timeToTriggerA5 480
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold2Rsrq -35
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold1Rsrq -195
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 b2Threshold2Geran -47
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 hysteresisB2 150
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 reportIntervalB2 12
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 timeToTriggerB2 640
set $mordn,UeMeasControl=1 a5B2MobilityTimer 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2UlThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2UlThrQciOffset=10
set $mordn,EUtranFreqRelation=.* interFreqMeasTypeUlSinr 0
set EnodebFunction=1,E.* ulTrigHoSupport 1
##T2 LMS
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrq 10
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -112
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -180
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRP -140
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset -20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -50
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=0,a1a2ThrRsrpQciOffset=46
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -114
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -116
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -140
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp -140
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -90
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp   -106
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5 10
set $mordn  qRxLevMin -124
set $mordn  SystemInformationBlock3 sintrasearch=44
set $mordn SystemInformationBlock3 snonintrasearch=8
set $mordn  SystemInformationBlock3 qhyst=4
set $mordn threshServingLow 8
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=240 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1346 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3676 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=.* a5Thr1RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr2RsrqFreqOffset 20
set $mordn,EUtranFreqRelation=1346 a5Thr2RsrqFreqOffset 70
set $mordn,EUtranFreqRelation=3676 a5Thr2RsrqFreqOffset 240
set $mordn,EUtranFreqRelation=39150  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39294  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=240  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=46,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-40,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1346  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=46,a5Thr2RsrpFreqQciOffset=2,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-90,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=3676  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr2RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=1346 a5Thr2RsrpFreqOffset 6
set $mordn,EUtranFreqRelation=3676 a5Thr2RsrpFreqOffset 64
set $mordn,EUtranFreqRelation=39150         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39294         lbA5Thr1RsrpFreqOffset 46
set $mordn,EUtranFreqRelation=1346         lbA5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=240         lbA5Thr1RsrpFreqOffset 46
set $mordn,EUtranFreqRelation=3676         lbA5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39294 cellReselectionPriority 6
set $mordn,EUtranFreqRelation=240 cellReselectionPriority 5
set $mordn,EUtranFreqRelation=1346 cellReselectionPriority 4
set $mordn,EUtranFreqRelation=3676 cellReselectionPriority 3
set $mordn,GeranFreqGroupRelation=1         cellReselectionPriority 1
set $mordn,GeranFreqGroupRelation=1         connectedModeMobilityPrio -1
set $mordn,EUtranFreqRelation=39150 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=39294 connectedmodemobilityprio 6
set $mordn,EUtranFreqRelation=240 connectedmodemobilityprio 5
set $mordn,EUtranFreqRelation=1346 connectedmodemobilityprio -1
set $mordn,EUtranFreqRelation=3676 connectedmodemobilityprio -1
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,GeranFreqGroupRelation=1         qRxLevMin         -111
set $mordn,EUtranFreqRelation=.* threshXHigh 12
set $mordn,EUtranFreqRelation=1346 threshXLow 16
set $mordn,EUtranFreqRelation=240 threshXLow 12
set $mordn,EUtranFreqRelation=3676 threshXLow 62
set $mordn,EUtranFreqRelation=39294 threshXlow 10
set $mordn,GeranFreqGroupRelation=1         threshXLow        62
set $mordn,EUtranFreqRelation=39150 voicePrio 5
set $mordn,EUtranFreqRelation=39294 voicePrio -1
set $mordn,EUtranFreqRelation=240 voicePrio 7
set $mordn,EUtranFreqRelation=1346 voicePrio 6
set $mordn,EUtranFreqRelation=3676 voicePrio -1
set $mordn,GeranFreqGroupRelation=1         voicePrio     -1
set $mordn,EUtranFreqRelation  interFreqMeasType 0
set $mordn,UeMeasControl=1                  ueMeasurementsActiveGERAN false
done
fi



##SMALL CELL Parameters

get ENodeBFunction=1,EUtranCellTDD earfcn 39151
if $nr_of_mos > 0
for $mo in SMALL
    $mordn = rdn($mo)
set $mordn cellRange 6
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp   -106
set $mordn, SystemInformationBlock3 snonintrasearch=8
set $mordn, SystemInformationBlock3 qhyst=4
set $mordn,UeMeasControl=1,ReportConfigEUtraIFBestCell=1 triggerQuantityA3 0
set $mordn CfraEnable True
set $mordn pdcchCfiMode 5
set $mordn dlInterferenceManagementActive TRUE
set $mordn crsgain 0
set $mordn pdschTypeBGain 0
set $mordn  specialSubframePattern 7
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1 a3offsetAnrDelta 0
set $mordn,UeMeasControl=1,ReportConfigA5=1,ReportConfigA5Anr=1 a5Threshold1RsrpAnrDelta 1
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrq -195
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -170
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -190
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrq -195
set $mordn  highSpeedUEActive False
set $mordn  prsPowerBoosting 3
set $mordn,UeMeasControl=1 ueMeasurementsActive 1
set $mordn pdcchpowerboostmax 2
set $mordn noOfChannelSelectionsets 6
set $mordn,EUtranFreqRelation=.* caTriggeredRedirectionActive false
set $mordn  transmissionMode 4
set $mordn  advCellSupAction 2
set $mordn  advCellSupSensitivity 25
set $mordn covTriggerdBlindHoAllowed 0
set $mordn  mobCtrlAtPoorCovActive true
set $mordn  pMaxServingCell 1000
set $mordn  preambleInitialReceivedTargetPower -110
set $mordn  ul64qamEnabled True
set $mordn  pZeroNominalPucch -110
set $mordn  pZeroNominalPusch -100
set $mordn  Alpha 10
set $mordn  pdcchLaGinrMargin 40
set $mordn  qRxLevMinOffset 1000
set $mordn  SystemInformationBlock3 qhyst=4
set $mordn  SystemInformationBlock3 snonintrasearch=8
set $mordn  SystemInformationBlock6 tReselectionutra=4
set $mordn  threshServingLow 8
set $mordn  qQualMin -34
set $mordn  qQualMinOffset 0
set $mordn tTimeAlignmentTimer 0
set $mordn,EUtranFreqRelation=.* qoffsetfreq 0
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,EUtranFreqRelation=.* tReselectionEutra 1
set $mordn,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set $mordn,UeMeasControl=1,ReportConfigA5=1 triggerquantitya5 0
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 a3offset 30
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 480
set $mordn,UeMeasControl=1,ReportConfigEUtraIFBestCell=1 triggerQuantityA3 0
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set $mordn,UeMeasControl=1 excludeInterFreqAtCritical True
set $mordn pdcchTargetBler 24
set $mordn pdcchCovImproveDtx 1
set $mordn pdcchCovImproveSrb false
set $mordn pdcchCovImproveQci1 1
set $mordn  adaptiveCfiHoProhibit 0
set $mordn allocThrPucchFormat1 50
set $mordn allocTimerPucchFormat1 50
set $mordn deallocThrPucchFormat1 100
set $mordn deallocTimerPucchFormat1 6000
set $mordn drxActive true
set $mordn  ulBlerTargetEnabled true
set $mordn  pdcchTargetBlerVolte 18
set $mordn  dlBlerTargetEnabled true
set $mordn  enableServiceSpecificHARQ true
set $mordn  pdcchOuterLoopInitialAdjVolte -46
set $mordn  pdcchOuterLoopUpStepVolte 9
set $mordn  tReorderingAutoConfiguration true
set $mordn  ulHarqVolteBlerTarget 3
set $mordn pdcchOuterLoopInitialAdj -70
set $mordn pdcchOuterLoopInitialAdjPCell -70
set $mordn pdcchOuterLoopUpStep 8
set $mordn pdcchOuterLoopUpStepPCell 6
set $mordn pdcchTargetBlerPCell 22
set $mordn,UeMeasControl=1,ReportConfigSearch=1 inhibitA2SearchConfig 0
set $mordn,UeMeasControl=1 measQuantityUtraFDD 1
set $mordn,UeMeasControl=1 ueMeasurementsActive 1
set $mordn enableSinrUplinkClpc 1
set $mordn,UeMeasControl=1 ueMeasurementsActiveIF true
set $mordn,UeMeasControl=1 ueMeasurementsActiveGERAN false
set $mordn,UeMeasControl=1                  a5B2MobilityTimer 0
set $mordn,UeMeasControl=1         bothA5RsrpRsrqCheck True
set $mordn cellCapMaxCellSubCap 60000
set $mordn cellCapMinCellSubCap 1000
set $mordn  cellCapMinMaxWriProt true
set $mordn cellSubscriptionCapacity 24000
set $mordn,UeMeasControl=1                  inhibitB2RsrqConfig true
set $mordn,EUtranFreqRelation  interFreqMeasType 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearch  40 
set $mordn,EUtranFreqRelation=.*,EUtranCellRelation=.* lbBnrAllowed true
set $mordn SystemInformationBlock3 snonintrasearchQ=0
set $mordn,EUtranFreqRelation=.* mobilityAction 1
set $mordn  	lbEUtranCellOffloadCapacity  30000
set TDD mappingInfo mappingInfoSIB3=1
set TDD mappingInfo mappingInfoSIB4=2
set TDD mappingInfo mappingInfoSIB5=3
set TDD mappingInfo mappingInfoSIB6=4
set TDD mappingInfo mappingInfoSIB7=5
set $mordn,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10
set $mordn                                  changeNotification changeNotificationSIB16=true
set $mordn                                  changeNotification changeNotificationSIB15=true
set $mordn                                  changeNotification changeNotificationSIB8=true
set $mordn  commonSrPeriodicity 20
set $mordn  dlFrequencyAllocationProportion 100
set $mordn  dl256QamEnabled true
set $mordn  servOrPrioTriggeredIFHo 0
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrp 4
set $mordn                                   hoOptAdjThresholdAbs 5
set $mordn                                   hoOptAdjThresholdPerc 50
set $mordn                                   hoOptStatTime  24
set $mordn,MimoSleepFunction=1              switchUpMonitorDurTimer 15
set $mordn,UeMeasControl=1,ReportConfigEUtraBadCovPrim=1 a2ThresholdRsrpPrim -140
set $mordn                                  ns05FullBandUsersInCellThres 1
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrq 11
set $mordn,EUtranFreqRelation=.*          allowedPlmnList   mcc=404,mnc=10,mncLength=2
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 maxReportCellsPm 8
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 reportIntervalPm 5
set $mordn  bsrThreshold 100
set $mordn  noOfUlImprovedUe 2
##1345 & 39151
set $mordn,EUtranFreqRelation=1345 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=1345 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=1345 voicePrio  7
set $mordn,EUtranFreqRelation=1345 a5Thr1RsrpFreqOffset 11
set $mordn,EUtranFreqRelation=1345 a5Thr2RsrpFreqOffset 4
set $mordn,EUtranFreqRelation=1345  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1345 lbA5Thr1RsrpFreqOffset  97
set $mordn,EUtranFreqRelation=1345 threshXHigh 10
set $mordn,EUtranFreqRelation=1345 qRxLevMin -124
set $mordn,EUtranFreqRelation=39151 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39151 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=39151 voicePrio  7
set $mordn,EUtranFreqRelation=39151 a5Thr1RsrpFreqOffset 13
set $mordn,EUtranFreqRelation=39151 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39151  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39151 lbA5Thr1RsrpFreqOffset  97
set $mordn,EUtranFreqRelation=39151 threshXHigh 10
set $mordn,EUtranFreqRelation=39151 qRxLevMin -124
##TD20 SINR LMS
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2UlSearchThreshold 40
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2UlSearch 20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1UlSearch 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlSearch 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2UlCriticalThreshold -150
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2UlCritical 150
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlCritical 480
set $mordn ulTrigActive True
set . enabledUlTrigMeas True
set $mordn,UeMeasControl=1 targetA2UlSearchOffset 20
set $mordn,UeMeasControl=1 ulSinrOffset 30
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold1Rsrp -44
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold2Rsrp -116
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 hysteresisA5 20
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 reportIntervalA5 12
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 timeToTriggerA5 480
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold2Rsrq -35
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold1Rsrq -195
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 b2Threshold2Geran -47
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 hysteresisB2 150
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 reportIntervalB2 12
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 timeToTriggerB2 640
set $mordn,UeMeasControl=1 a5B2MobilityTimer 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2UlThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2UlThrQciOffset=10
set $mordn,EUtranFreqRelation=.* interFreqMeasTypeUlSinr 0
set EnodebFunction=1,E.* ulTrigHoSupport 1
##T2 LMS
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrq 10
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -112
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -180
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRP -140
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset -20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -50
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=0,a1a2ThrRsrpQciOffset=46
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -114
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -116
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -140
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp -140
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -90
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp   -106
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5 10
set $mordn  qRxLevMin -124
set $mordn  SystemInformationBlock3 sintrasearch=44
set $mordn SystemInformationBlock3 snonintrasearch=8
set $mordn  SystemInformationBlock3 qhyst=4
set $mordn threshServingLow 8
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=240 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1346 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3676 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=.* a5Thr1RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr2RsrqFreqOffset 20
set $mordn,EUtranFreqRelation=1346 a5Thr2RsrqFreqOffset 70
set $mordn,EUtranFreqRelation=3676 a5Thr2RsrqFreqOffset 240
set $mordn,EUtranFreqRelation=39150  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39294  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=240  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=46,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-40,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1346  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=46,a5Thr2RsrpFreqQciOffset=2,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-90,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=3676  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr2RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=1346 a5Thr2RsrpFreqOffset 6
set $mordn,EUtranFreqRelation=3676 a5Thr2RsrpFreqOffset 64
set $mordn,EUtranFreqRelation=39150         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39294         lbA5Thr1RsrpFreqOffset 46
set $mordn,EUtranFreqRelation=1346         lbA5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=240         lbA5Thr1RsrpFreqOffset 46
set $mordn,EUtranFreqRelation=3676         lbA5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39294 cellReselectionPriority 6
set $mordn,EUtranFreqRelation=240 cellReselectionPriority 5
set $mordn,EUtranFreqRelation=1346 cellReselectionPriority 4
set $mordn,EUtranFreqRelation=3676 cellReselectionPriority 3
set $mordn,GeranFreqGroupRelation=1         cellReselectionPriority 1
set $mordn,GeranFreqGroupRelation=1         connectedModeMobilityPrio -1
set $mordn,EUtranFreqRelation=39150 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=39294 connectedmodemobilityprio 6
set $mordn,EUtranFreqRelation=240 connectedmodemobilityprio 5
set $mordn,EUtranFreqRelation=1346 connectedmodemobilityprio -1
set $mordn,EUtranFreqRelation=3676 connectedmodemobilityprio -1
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,GeranFreqGroupRelation=1         qRxLevMin         -111
set $mordn,EUtranFreqRelation=.* threshXHigh 12
set $mordn,EUtranFreqRelation=1346 threshXLow 16
set $mordn,EUtranFreqRelation=240 threshXLow 12
set $mordn,EUtranFreqRelation=3676 threshXLow 62
set $mordn,EUtranFreqRelation=39294 threshXlow 10
set $mordn,GeranFreqGroupRelation=1         threshXLow        62
set $mordn,EUtranFreqRelation=39150 voicePrio 5
set $mordn,EUtranFreqRelation=39294 voicePrio -1
set $mordn,EUtranFreqRelation=240 voicePrio 7
set $mordn,EUtranFreqRelation=1346 voicePrio 6
set $mordn,EUtranFreqRelation=3676 voicePrio -1
set $mordn,GeranFreqGroupRelation=1         voicePrio     -1
set $mordn,EUtranFreqRelation  interFreqMeasType 0
set $mordn,UeMeasControl=1                  ueMeasurementsActiveGERAN false
done
fi




##TDD 10 -T1 Parameters

get ENodeBFunction=1,EUtranCellTDD earfcn 39294
if $nr_of_mos > 0
for $mo in T1
    $mordn = rdn($mo)
set $mordn cellSubscriptionCapacity 12000
set $mordn cellRange 6
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp   -106
set $mordn, SystemInformationBlock3 snonintrasearch=8
set $mordn, SystemInformationBlock3 sintrasearch=44
set $mordn, SystemInformationBlock3 qhyst=4
set $mordn,UeMeasControl=1,ReportConfigEUtraIFBestCell=1 triggerQuantityA3 0
set $mordn CfraEnable True
set $mordn pdcchCfiMode 5
set $mordn dlInterferenceManagementActive TRUE
set $mordn crsgain 0
set $mordn pdschTypeBGain 0
set $mordn  specialSubframePattern 7
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1 a3offsetAnrDelta 0
set $mordn,UeMeasControl=1,ReportConfigA5=1,ReportConfigA5Anr=1 a5Threshold1RsrpAnrDelta 1
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrq -195
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -170
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -190
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrq -195
set $mordn  highSpeedUEActive False
set $mordn  prsPowerBoosting 3
set $mordn,UeMeasControl=1 ueMeasurementsActive 1
set $mordn pdcchpowerboostmax 2
set $mordn noOfChannelSelectionsets 6
set $mordn,EUtranFreqRelation=.* caTriggeredRedirectionActive false
set $mordn, sCellHandlingAtVolteCall 1
set $mordn,EUtranFreqRelation=39150,EUtranCellRelation=40410.*sCellCandidate    1
set $mordn,EUtranFreqRelation=39294,EUtranCellRelation=40410.*sCellCandidate    1
set $mordn  transmissionMode 4
set $mordn  advCellSupAction 2
set $mordn  advCellSupSensitivity 25
set $mordn covTriggerdBlindHoAllowed 0
set $mordn  mobCtrlAtPoorCovActive true
set $mordn  pMaxServingCell 1000
set $mordn  preambleInitialReceivedTargetPower -110
set $mordn  ul64qamEnabled True
set $mordn  pZeroNominalPucch -110
set $mordn  pZeroNominalPusch -100
set $mordn  Alpha 10
set $mordn  pdcchLaGinrMargin 40
set $mordn  qRxLevMin -124
set $mordn  qRxLevMinOffset 1000
set $mordn  SystemInformationBlock3 qhyst=4
set $mordn  SystemInformationBlock3 snonintrasearch=8
set $mordn  SystemInformationBlock6 tReselectionutra=4
set $mordn  threshServingLow 8
set $mordn  qQualMin -34
set $mordn  qQualMinOffset 0
set $mordn tTimeAlignmentTimer 0
set $mordn,EUtranFreqRelation=.* qoffsetfreq 0
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,EUtranFreqRelation=.* tReselectionEutra 1
set $mordn,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set $mordn,UeMeasControl=1,ReportConfigA5=1 triggerquantitya5 0
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 a3offset 30
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 480
set $mordn,UeMeasControl=1,ReportConfigEUtraIFBestCell=1 triggerQuantityA3 0
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set $mordn,UeMeasControl=1 excludeInterFreqAtCritical True
set $mordn pdcchTargetBler 24
set $mordn pdcchCovImproveDtx 1
set $mordn pdcchCovImproveSrb false
set $mordn pdcchCovImproveQci1 1
set $mordn  adaptiveCfiHoProhibit 0
set $mordn allocThrPucchFormat1 50
set $mordn allocTimerPucchFormat1 50
set $mordn deallocThrPucchFormat1 100
set $mordn deallocTimerPucchFormat1 6000
set $mordn drxActive true
set $mordn  ulBlerTargetEnabled true
set $mordn  pdcchTargetBlerVolte 18
set $mordn  dlBlerTargetEnabled true
set $mordn  enableServiceSpecificHARQ true
set $mordn  pdcchOuterLoopInitialAdjVolte -46
set $mordn  pdcchOuterLoopUpStepVolte 9
set $mordn  tReorderingAutoConfiguration true
set $mordn  ulHarqVolteBlerTarget 3
set $mordn pdcchOuterLoopInitialAdj -70
set $mordn pdcchOuterLoopInitialAdjPCell -70
set $mordn pdcchOuterLoopUpStep 8
set $mordn pdcchOuterLoopUpStepPCell 6
set $mordn pdcchTargetBlerPCell 22
set $mordn,UeMeasControl=1,ReportConfigSearch=1 inhibitA2SearchConfig 0
set $mordn,UeMeasControl=1 measQuantityUtraFDD 1
set $mordn,UeMeasControl=1 ueMeasurementsActive 1
set $mordn enableSinrUplinkClpc 1
set $mordn,UeMeasControl=1 ueMeasurementsActiveIF true
set $mordn,UeMeasControl=1 ueMeasurementsActiveGERAN false
set $mordn,UeMeasControl=1                  a5B2MobilityTimer 0
set $mordn,UeMeasControl=1         bothA5RsrpRsrqCheck True
set $mordn cellCapMaxCellSubCap 60000
set $mordn cellCapMinCellSubCap 1000
set $mordn  cellCapMinMaxWriProt true
set $mordn,UeMeasControl=1                  inhibitB2RsrqConfig true
set $mordn,EUtranFreqRelation  interFreqMeasType 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearch  40 
set $mordn,EUtranFreqRelation=.*,EUtranCellRelation=.* lbBnrAllowed true
set $mordn SystemInformationBlock3 snonintrasearchQ=0
set $mordn,EUtranFreqRelation=.* mobilityAction 1
set $mordn  	lbEUtranCellOffloadCapacity  30000
set TDD mappingInfo mappingInfoSIB3=1
set TDD mappingInfo mappingInfoSIB4=2
set TDD mappingInfo mappingInfoSIB5=3
set TDD mappingInfo mappingInfoSIB6=4
set TDD mappingInfo mappingInfoSIB7=5
set $mordn,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10
set $mordn                                  changeNotification changeNotificationSIB16=true
set $mordn                                  changeNotification changeNotificationSIB15=true
set $mordn                                  changeNotification changeNotificationSIB8=true
set $mordn  commonSrPeriodicity 20
set $mordn  dlFrequencyAllocationProportion 100
set $mordn  dl256QamEnabled true
set $mordn  servOrPrioTriggeredIFHo 0
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrp 4
set $mordn                                   hoOptAdjThresholdAbs 5
set $mordn                                   hoOptAdjThresholdPerc 50
set $mordn                                   hoOptStatTime  24
set $mordn,MimoSleepFunction=1              switchUpMonitorDurTimer 15
set $mordn,UeMeasControl=1,ReportConfigEUtraBadCovPrim=1 a2ThresholdRsrpPrim -140
set $mordn                                  ns05FullBandUsersInCellThres 1
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrq 11
set $mordn,EUtranFreqRelation=.*          allowedPlmnList   mcc=404,mnc=10,mncLength=2
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 maxReportCellsPm 8
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 reportIntervalPm 5
set $mordn  bsrThreshold 100
set $mordn  noOfUlImprovedUe 2
##1345 & 39151 
set $mordn,EUtranFreqRelation=1345 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=1345 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=1345 voicePrio  7
set $mordn,EUtranFreqRelation=1345 a5Thr1RsrpFreqOffset 11
set $mordn,EUtranFreqRelation=1345 a5Thr2RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=1345  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1345 lbA5Thr1RsrpFreqOffset  97
set $mordn,EUtranFreqRelation=1345 threshXHigh 10
set $mordn,EUtranFreqRelation=1345 qRxLevMin -124
set $mordn,EUtranFreqRelation=39151 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39151 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=39151 voicePrio  7
set $mordn,EUtranFreqRelation=39151 a5Thr1RsrpFreqOffset 13
set $mordn,EUtranFreqRelation=39151 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39151  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39151 lbA5Thr1RsrpFreqOffset  97
set $mordn,EUtranFreqRelation=39151 threshXHigh 10
set $mordn,EUtranFreqRelation=39151 qRxLevMin -124
##T1 SINR LMS
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2UlSearchThreshold 40
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2UlSearch 20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1UlSearch 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlSearch 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2UlCriticalThreshold -150
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2UlCritical 150
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlCritical 480
set $mordn ulTrigActive True
set . enabledUlTrigMeas True
set $mordn,UeMeasControl=1 targetA2UlSearchOffset 20
set $mordn,UeMeasControl=1 ulSinrOffset 30
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold1Rsrp -44
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold2Rsrp -116
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 hysteresisA5 20
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 reportIntervalA5 12
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 timeToTriggerA5 480
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold2Rsrq -35
set $mordn,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold1Rsrq -195
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 b2Threshold2Geran -47
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 hysteresisB2 150
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 reportIntervalB2 12
set $mordn,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 timeToTriggerB2 640
set $mordn,UeMeasControl=1 a5B2MobilityTimer 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2UlThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2UlThrQciOffset=10
set $mordn,EUtranFreqRelation=.* interFreqMeasTypeUlSinr 0
set EnodebFunction=1,E.* ulTrigHoSupport 1
##T1 LMS
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrq 10
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -112
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -180
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRp -140
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset -20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -50
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=0,a1a2ThrRsrpQciOffset=46
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -114
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -114
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -140
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -90
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp -140
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set $mordn SystemInformationBlock3 snonintrasearch=8
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp   -106
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5 10
set $mordn  qRxLevMin -124
set $mordn  SystemInformationBlock3 sintrasearch=44
set $mordn  SystemInformationBlock3 qhyst=4
set $mordn,EUtranFreqRelation=.* a5Thr1RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr2RsrqFreqOffset 20
set $mordn,EUtranFreqRelation=1346 a5Thr2RsrqFreqOffset 70
set $mordn,EUtranFreqRelation=3676 a5Thr2RsrqFreqOffset 240
set $mordn,EUtranFreqRelation=39150         lbA5Thr1RsrpFreqOffset 56
set $mordn,EUtranFreqRelation=39294         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=1346         lbA5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=240         lbA5Thr1RsrpFreqOffset 46
set $mordn,EUtranFreqRelation=3676         lbA5Thr1RsrpFreqOffset 0
set $mordn threshServingLow 8
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1346 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3676 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39294  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=240  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=46,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-40,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1346  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=46,a5Thr2RsrpFreqQciOffset=2,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-90,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=3676  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 64
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1346 a5Thr2RsrpFreqOffset 4
set $mordn,EUtranFreqRelation=3676 a5Thr2RsrpFreqOffset 64
set $mordn,EUtranFreqRelation=39150 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39294 cellReselectionPriority 6
set $mordn,EUtranFreqRelation=240 cellReselectionPriority 5
set $mordn,EUtranFreqRelation=1346 cellReselectionPriority 4
set $mordn,EUtranFreqRelation=3676 cellReselectionPriority 3
set $mordn,GeranFreqGroupRelation=1         cellReselectionPriority 1
set $mordn,GeranFreqGroupRelation=1         connectedModeMobilityPrio -1
set $mordn,EUtranFreqRelation=39150 connectedmodemobilityprio 6
set $mordn,EUtranFreqRelation=39294 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=240 connectedmodemobilityprio 5
set $mordn,EUtranFreqRelation=1346 connectedmodemobilityprio 4
set $mordn,EUtranFreqRelation=3676 connectedmodemobilityprio -1
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,GeranFreqGroupRelation=1         qRxLevMin         -111
set $mordn,EUtranFreqRelation=.* threshXHigh 12
set $mordn,EUtranFreqRelation=1346 threshXLow 16
set $mordn,EUtranFreqRelation=240 threshXLow 12
set $mordn,EUtranFreqRelation=3676 threshXLow 62
set $mordn,GeranFreqGroupRelation=1         threshXLow        62
set $mordn,GeranFreqGroupRelation=1         voicePrio     -1
set $mordn,EUtranFreqRelation=39150 voicePrio -1
set $mordn,EUtranFreqRelation=39294 voicePrio 5
set $mordn,EUtranFreqRelation=240 voicePrio 7
set $mordn,EUtranFreqRelation=1346 voicePrio 6
set $mordn,EUtranFreqRelation=3676 voicePrio -1
set $mordn,EUtranFreqRelation  interFreqMeasType 0
set $mordn,UeMeasControl=1                  ueMeasurementsActiveGERAN false
done
fi

##L1800 Parameters

get ENodeBFunction=1,EUtranCellFDD earfcndl 1346
if $nr_of_mos > 0
for $mo in F3
    $mordn = rdn($mo)
set $mordn cellSubscriptionCapacity 5000
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1 a3offsetAnrDelta 0
set $mordn dlInterferenceManagementActive TRUE
set $mordn CfraEnable True
set $mordn crsgain 0
set $mordn pdschTypeBGain 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrq -195
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -160
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -190
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrq -195
set $mordn pdcchCfiMode 5
set $mordn highSpeedUEActive False
set $mordn prsPowerBoosting 3
set $mordn cellRange 6
set $mordn noOfChannelSelectionsets 4
set $mordn channelSelectionsetSize 2
set $mordn,EUtranFreqRelation=.* caTriggeredRedirectionActive false
set $mordn,EUtranFreqRelation=39*.*,EUtranCellRelation=40410-9 coverageIndicator 0
set $mordn transmissionMode 4
set $mordn advCellSupAction 2
set $mordn advCellSupSensitivity 25
set $mordn covTriggerdBlindHoAllowed 0
set $mordn mobCtrlAtPoorCovActive true
set $mordn pMaxServingCell 1000
set $mordn preambleInitialReceivedTargetPower -110
set $mordn tTimeAlignmentTimer 0
set $mordn ul64qamEnabled True
set $mordn pdcchLaGinrMargin 40
set $mordn qRxLevMinOffset 1000
set $mordn SystemInformationBlock6 tReselectionutra=4
set $mordn qQualMin -34
set $mordn qQualMinOffset 0
set $mordn,EUtranFreqRelation=.* qoffsetfreq 0
set $mordn,EUtranFreqRelation=.* tReselectionEutra 1
set $mordn,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set $mordn,UeMeasControl=1,ReportConfigA5=1 triggerquantitya5 0
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2EcNoUtra -180
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2RscpUtra -190
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 timeToTriggerB2 1280
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 a3offset 30
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 480
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 triggerQuantityA3 0
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set $mordn,UeMeasControl=1 excludeInterFreqAtCritical False
set $mordn dlBlerTargetEnabled TRUE
set $mordn ulTrigActive False
set $mordn enableServiceSpecificHARQ TRUE
set $mordn pdcchOuterLoopInitialAdjVolte -46
set $mordn pdcchOuterLoopUpStepVolte 9
set $mordn pdcchTargetBlerVolte 18
set $mordn tReorderingAutoConfiguration true
set $mordn ulBlerTargetEnabled true
set $mordn ulHarqVolteBlerTarget 3
set $mordn pdcchOuterLoopInitialAdj -70
set $mordn pdcchOuterLoopInitialAdjPCell -70
set $mordn pdcchOuterLoopUpStep 8
set $mordn pdcchOuterLoopUpStepPCell 6
set $mordn pdcchTargetBler 24
set $mordn pdcchTargetBlerPCell 22
set $mordn ttiBundlingAfterHO 1
set $mordn ttiBundlingAfterReest 1
set $mordn ttiBundlingSwitchThres 150
set $mordn ttiBundlingSwitchThresHyst 30
set $mordn pdcchCovImproveDtx 1
set $mordn pdcchCovImproveSrb false
set $mordn pdcchCovImproveQci1 1
set $mordn adaptiveCfiHoProhibit 0
set $mordn allocThrPucchFormat1 50
set $mordn allocTimerPucchFormat1 50
set $mordn deallocThrPucchFormat1 100
set $mordn deallocTimerPucchFormat1 6000
set $mordn drxActive 1
set ExternalUtranCellFDD  srvccCapability 1
set $mordn,UeMeasControl=1,ReportConfigSearch=1 inhibitA2SearchConfig 0
set $mordn,UeMeasControl=1 ueMeasurementsActive 1
set $mordn enableSinrUplinkClpc 1
set $mordn,UeMeasControl=1 ueMeasurementsActiveIF true
set $mordn,UeMeasControl=1 ueMeasurementsActiveGERAN true
set $mordn,UeMeasControl=1                  a5B2MobilityTimer 0
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -140
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp   -111
set $mordn,UtranFreqRelation b2Thr1RsrpUtraFreqOffset 0
set $mordn,UtranFreqRelation b2Thr2EcNoUtraFreqOffset 0
set $mordn,UeMeasControl=1         bothA5RsrpRsrqCheck True
set $mordn cellCapMaxCellSubCap 60000
set $mordn cellCapMinMaxWriProt true
set $mordn,UeMeasControl=1                  inhibitB2RsrqConfig true
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearch  40 
set $mordn,EUtranFreqRelation=.*,EUtranCellRelation=.* lbBnrAllowed true
set $mordn SystemInformationBlock3 snonintrasearchQ=0
set $mordn SystemInformationBlock3 sintrasearchp=44
set $mordn,EUtranFreqRelation=.* mobilityAction 1
set $mordn mappingInfo mappingInfoSIB3=1
set $mordn mappingInfo mappingInfoSIB5=3
set $mordn mappingInfo mappingInfoSIB7=5
set $mordn mappingInfo mappingInfoSIB12=7
set $mordn mappingInfo mappingInfoSIB4=2
set $mordn mappingInfo mappingInfoSIB6=4
set $mordn                                  lbEUtranAcceptOffloadThreshold  10
set $mordn                                  lbEUtranTriggerOffloadThreshold 30
set $mordn,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10
set $mordn                                 changeNotification changeNotificationSIB16=true
set $mordn                                 changeNotification changeNotificationSIB15=true
set $mordn                                 changeNotification changeNotificationSIB8=true
set $mordn commonSrPeriodicity 10
set $mordn ulInternalChannelBandwidth 0
set $mordn dlInternalChannelBandwidth 0
set $mordn dlFrequencyAllocationProportion 100
set $mordn dl256QamEnabled true
set $mordn servOrPrioTriggeredIFHo 0
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrp 4
set $mordn                                  cellDownlinkCaCapacity 0
set $mordn                            servOrPrioTriggeredErabAction 3 
set $mordn                                  hoOptAdjThresholdAbs 5
set $mordn                                  hoOptAdjThresholdPerc 50
set $mordn,MimoSleepFunction=1              switchUpMonitorDurTimer 15
set $mordn,UeMeasControl=1,ReportConfigEUtraBadCovPrim=1 a2ThresholdRsrpPrim -140
set $mordn                                 ns05FullBandUsersInCellThres 1
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrq 11
set $mordn,EUtranFreqRelation=.*          allowedPlmnList   mcc=404,mnc=10,mncLength=2
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 maxReportCellsPm 8
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 reportIntervalPm 5
set $mordn bsrThreshold 100
set $mordn noOfUlImprovedUe 2
set $mordn,EUtranFreqRelation=39150,EUtranCellRelation=40410-9 sCellCandidate 1
set $mordn,EUtranFreqRelation=39294,EUtranCellRelation=40410-9 sCellCandidate 1
set $mordn pdcchpowerboostmax 2
##1345 & 39151
set $mordn,EUtranFreqRelation=1345 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=1345 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=1345 voicePrio  7
set $mordn,EUtranFreqRelation=1345 a5Thr1RsrpFreqOffset 9
set $mordn,EUtranFreqRelation=1345 a5Thr2RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=1345  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1345 lbA5Thr1RsrpFreqOffset  97
set $mordn,EUtranFreqRelation=1345 threshXHigh 10
set $mordn,EUtranFreqRelation=1345 qRxLevMin -124
set $mordn,EUtranFreqRelation=39151 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39151 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=39151 voicePrio  7
set $mordn,EUtranFreqRelation=39151 a5Thr1RsrpFreqOffset 11
set $mordn,EUtranFreqRelation=39151 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39151  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39151 lbA5Thr1RsrpFreqOffset  97
set $mordn,EUtranFreqRelation=39151 threshXHigh 10
set $mordn,EUtranFreqRelation=39151 qRxLevMin -124
###F3 LMS
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrq 10
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -88
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -160
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRp -140
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset -20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -50
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=0,a1a2ThrRsrpQciOffset=0
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -112
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -114
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp -140
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -90
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set $mordn,EUtranFreqRelation=39150         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39294         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=1346         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=240         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=3676         lbA5Thr1RsrpFreqOffset 0
set EUtranCellFDD=.* qRxLevMin -124
set EutrancellFDD=.* SystemInformationBlock3 sintrasearch=44
set $mordn SystemInformationBlock3 snonintrasearch=6
set EutrancellFDD=.* SystemInformationBlock3 qhyst=4
set $mordn threshServingLow 6
set $mordn ulTrigActive False
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 24
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 24
set $mordn,EUtranFreqRelation=240 a5Thr1RsrpFreqOffset 24
set $mordn,EUtranFreqRelation=1346 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3676 a5Thr1RsrpFreqOffset 6
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrqFreqOffset 10
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrqFreqOffset 10
set $mordn,EUtranFreqRelation=240 a5Thr1RsrqFreqOffset 10
set $mordn,EUtranFreqRelation=1346 a5Thr1RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=3676 a5Thr1RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=1346 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=3676 a5Thr2RsrqFreqOffset 150
set $mordn,EUtranFreqRelation=39150  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=68,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39294  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=68,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=240  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-20,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1346  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=3676  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=8,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-170,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1346 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3676 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39294 cellReselectionPriority 6
set $mordn,EUtranFreqRelation=240 cellReselectionPriority 5
set $mordn,EUtranFreqRelation=1346 cellReselectionPriority 4
set $mordn,EUtranFreqRelation=3676 cellReselectionPriority 3
set $mordn,GeranFreqGroupRelation=1         cellReselectionPriority 1
set $mordn,GeranFreqGroupRelation=1         connectedModeMobilityPrio -1
set $mordn,EUtranFreqRelation=39150 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=39294 connectedmodemobilityprio 6
set $mordn,EUtranFreqRelation=240 connectedmodemobilityprio 5
set $mordn,EUtranFreqRelation=1346 connectedmodemobilityprio 4
set $mordn,EUtranFreqRelation=3676 connectedmodemobilityprio 3
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,GeranFreqGroupRelation=1         qRxLevMin         -111
set $mordn,EUtranFreqRelation=39150 threshXHigh 12
set $mordn,EUtranFreqRelation=39294 threshXHigh 12
set $mordn,EUtranFreqRelation=240 threshXHigh 14
set $mordn,EUtranFreqRelation=3676 threshXLow 12
set $mordn,GeranFreqGroupRelation=1         threshXLow        62
set $mordn,EUtranFreqRelation=39150 voicePrio -1
set $mordn,EUtranFreqRelation=39294 voicePrio -1
set $mordn,EUtranFreqRelation=240 voicePrio 6
set $mordn,EUtranFreqRelation=1346 voicePrio 7
set $mordn,EUtranFreqRelation=3676 voicePrio 5
set $mordn,GeranFreqGroupRelation=1         voicePrio     -1
set $mordn,UeMeasControl=1                  ueMeasurementsActiveGERAN True
set EUtranCellFDD=.*,EUtranFreqRelation  interFreqMeasType 0
done
fi 


##L900 Parameters

get ENodeBFunction=1,EUtranCellFDD earfcndl 3676
if $nr_of_mos > 0
for $mo in F8
    $mordn = rdn($mo)
set $mordn cellSubscriptionCapacity 5000
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1 a3offsetAnrDelta 0
set $mordn dlInterferenceManagementActive TRUE
set $mordn CfraEnable True
set $mordn crsgain 177
set $mordn pdschTypeBGain 1
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrq -195
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -150
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -190
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrq -195
set $mordn pdcchCfiMode 5
set $mordn highSpeedUEActive False
set $mordn prsPowerBoosting 3
set $mordn cellRange 6
set $mordn noOfChannelSelectionsets 4
set $mordn channelSelectionsetSize 2
set $mordn,EUtranFreqRelation=.* caTriggeredRedirectionActive false
set $mordn,EUtranFreqRelation=39*.*,EUtranCellRelation=40410-9 coverageIndicator 0
set $mordn transmissionMode 4
set $mordn advCellSupAction 2
set $mordn advCellSupSensitivity 25
set $mordn covTriggerdBlindHoAllowed 0
set $mordn mobCtrlAtPoorCovActive true
set $mordn pMaxServingCell 1000
set $mordn preambleInitialReceivedTargetPower -110
set $mordn tTimeAlignmentTimer 0
set $mordn ul64qamEnabled True
set $mordn pdcchLaGinrMargin 40
set $mordn qRxLevMinOffset 1000
set $mordn SystemInformationBlock6 tReselectionutra=4
set $mordn qQualMin -34
set $mordn qQualMinOffset 0
set $mordn,EUtranFreqRelation=.* qoffsetfreq 0
set $mordn,EUtranFreqRelation=.* tReselectionEutra 1
set $mordn,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set $mordn,UeMeasControl=1,ReportConfigA5=1 triggerquantitya5 0
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2EcNoUtra -180
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2RscpUtra -190
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 timeToTriggerB2 1280
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 a3offset 30
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 480
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 triggerQuantityA3 0
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set $mordn,UeMeasControl=1 excludeInterFreqAtCritical False
set $mordn dlBlerTargetEnabled TRUE
set $mordn enableServiceSpecificHARQ TRUE
set $mordn pdcchOuterLoopInitialAdjVolte -46
set $mordn pdcchOuterLoopUpStepVolte 9
set $mordn pdcchTargetBlerVolte 18
set $mordn tReorderingAutoConfiguration true
set $mordn ulBlerTargetEnabled true
set $mordn ulHarqVolteBlerTarget 3
set $mordn pdcchOuterLoopInitialAdj -70
set $mordn pdcchOuterLoopInitialAdjPCell -70
set $mordn pdcchOuterLoopUpStep 8
set $mordn pdcchOuterLoopUpStepPCell 6
set $mordn pdcchTargetBler 24
set $mordn pdcchTargetBlerPCell 22
set $mordn ttiBundlingAfterHO 1
set $mordn ttiBundlingAfterReest 1
set $mordn ttiBundlingSwitchThres 150
set $mordn ttiBundlingSwitchThresHyst 30
set $mordn pdcchCovImproveDtx 1
set $mordn pdcchCovImproveSrb false
set $mordn pdcchCovImproveQci1 1
set $mordn adaptiveCfiHoProhibit 0
set $mordn allocThrPucchFormat1 50
set $mordn allocTimerPucchFormat1 50
set $mordn deallocThrPucchFormat1 100
set $mordn deallocTimerPucchFormat1 6000
set $mordn drxActive 1
set ExternalUtranCellFDD  srvccCapability 1
set $mordn,UeMeasControl=1,ReportConfigSearch=1 inhibitA2SearchConfig 0
set $mordn,UeMeasControl=1 ueMeasurementsActive 1
set $mordn enableSinrUplinkClpc 1
set $mordn,UeMeasControl=1 ueMeasurementsActiveIF true
set $mordn,UeMeasControl=1 ueMeasurementsActiveGERAN true
set $mordn,UeMeasControl=1                  a5B2MobilityTimer 0
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -44
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp   -111
set $mordn,UtranFreqRelation b2Thr1RsrpUtraFreqOffset 0
set $mordn,UtranFreqRelation b2Thr2EcNoUtraFreqOffset 0
set $mordn,UeMeasControl=1         bothA5RsrpRsrqCheck True
set $mordn cellCapMaxCellSubCap 60000
set $mordn cellCapMinMaxWriProt true
set $mordn,UeMeasControl=1                  inhibitB2RsrqConfig true
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearch  40 
set $mordn,EUtranFreqRelation=.*,EUtranCellRelation=.* lbBnrAllowed true
set $mordn SystemInformationBlock3 snonintrasearchQ=0
set $mordn SystemInformationBlock3 sintrasearchp=44
set $mordn,EUtranFreqRelation=.* mobilityAction 1
set $mordn mappingInfo mappingInfoSIB3=1
set $mordn mappingInfo mappingInfoSIB5=3
set $mordn mappingInfo mappingInfoSIB7=5
set $mordn mappingInfo mappingInfoSIB12=7
set $mordn mappingInfo mappingInfoSIB4=2
set $mordn mappingInfo mappingInfoSIB6=4
set $mordn                                  lbEUtranAcceptOffloadThreshold  10
set $mordn                                  lbEUtranTriggerOffloadThreshold 30
set $mordn,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10
set $mordn                                 changeNotification changeNotificationSIB16=true
set $mordn                                 changeNotification changeNotificationSIB15=true
set $mordn                                 changeNotification changeNotificationSIB8=true
set $mordn commonSrPeriodicity 10
set $mordn ulInternalChannelBandwidth 0
set $mordn dlInternalChannelBandwidth 0
set $mordn dlFrequencyAllocationProportion 100
set $mordn dl256QamEnabled true
set $mordn servOrPrioTriggeredIFHo 0
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrp 4
set $mordn                                  cellDownlinkCaCapacity 0
set $mordn                            servOrPrioTriggeredErabAction 3 
set $mordn                                  hoOptAdjThresholdAbs 5
set $mordn                                  hoOptAdjThresholdPerc 50
set $mordn,MimoSleepFunction=1              switchUpMonitorDurTimer 15
set $mordn,UeMeasControl=1,ReportConfigEUtraBadCovPrim=1 a2ThresholdRsrpPrim -140
set $mordn                                 ns05FullBandUsersInCellThres 1
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrq 11
set $mordn,EUtranFreqRelation=.*          allowedPlmnList   mcc=404,mnc=10,mncLength=2
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 maxReportCellsPm 8
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 reportIntervalPm 5
set $mordn bsrThreshold 100
set $mordn ulTrigActive False
set $mordn noOfUlImprovedUe 2
set $mordn pdcchpowerboostmax 2
###1345 & 39151
set $mordn,EUtranFreqRelation=39151 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39151 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=39151 voicePrio  7
set $mordn,EUtranFreqRelation=39151 a5Thr1RsrpFreqOffset 13
set $mordn,EUtranFreqRelation=39151 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39151  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39151 lbA5Thr1RsrpFreqOffset  0
set $mordn,EUtranFreqRelation=39151 threshXHigh 10
set $mordn,EUtranFreqRelation=39151 qRxLevMin -124
set $mordn,EUtranFreqRelation=1345 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=1345 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=1345 voicePrio  7
set $mordn,EUtranFreqRelation=1345 a5Thr1RsrpFreqOffset 11
set $mordn,EUtranFreqRelation=1345 a5Thr2RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=1345  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1345 lbA5Thr1RsrpFreqOffset  0
set $mordn,EUtranFreqRelation=1345 threshXHigh 10
set $mordn,EUtranFreqRelation=1345 qRxLevMin -124
######### F8 LMS
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrq 10
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -78
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -160
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRp -140
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset -20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -50
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=0,a1a2ThrRsrpQciOffset=0
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -114
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -114
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp -140
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -90
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set $mordn SystemInformationBlock3 sintrasearch=44
set $mordn SystemInformationBlock3 snonintrasearch=0
set $mordn SystemInformationBlock3 qhyst=4
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 36
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 36
set $mordn,EUtranFreqRelation=240 a5Thr1RsrpFreqOffset 36
set $mordn,EUtranFreqRelation=1346 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3676 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=.* a5Thr1RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=.* a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=.*         lbA5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=68,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39294  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=68,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=240  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-20,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1346  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-20,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=3676  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr2RsrpFreqOffset 4
set $mordn,EUtranFreqRelation=1346 a5Thr2RsrpFreqOffset 4
set $mordn,EUtranFreqRelation=3676 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39294 cellReselectionPriority 6
set $mordn,EUtranFreqRelation=240 cellReselectionPriority 5
set $mordn,EUtranFreqRelation=1346 cellReselectionPriority 4
set $mordn,EUtranFreqRelation=3676 cellReselectionPriority 3
set $mordn,GeranFreqGroupRelation=1         cellReselectionPriority 1
set $mordn,GeranFreqGroupRelation=1         connectedModeMobilityPrio -1
set $mordn,EUtranFreqRelation=39150 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=39294 connectedmodemobilityprio 6
set $mordn,EUtranFreqRelation=240 connectedmodemobilityprio 5
set $mordn,EUtranFreqRelation=1346 connectedmodemobilityprio 4
set $mordn,EUtranFreqRelation=3676 connectedmodemobilityprio 3
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,GeranFreqGroupRelation=1         qRxLevMin         -111
set $mordn,EUtranFreqRelation=39150 threshXHigh 12
set $mordn,EUtranFreqRelation=39294 threshXHigh 12
set $mordn,EUtranFreqRelation=240 threshXHigh 14
set $mordn,EUtranFreqRelation=1346 threshXHigh 16
set $mordn,GeranFreqGroupRelation=1     threshXLow  62
set $mordn,EUtranFreqRelation=39150 voicePrio -1
set $mordn,EUtranFreqRelation=39294 voicePrio -1
set $mordn,EUtranFreqRelation=240 voicePrio -1
set $mordn,EUtranFreqRelation=1346 voicePrio 7
set $mordn,EUtranFreqRelation=3676 voicePrio 5
set $mordn,GeranFreqGroupRelation=1         voicePrio     -1
set $mordn,EUtranFreqRelation  interFreqMeasType 0
set $mordn,UeMeasControl=1                  ueMeasurementsActiveGERAN True
set $mordn SystemInformationBlock3 sintrasearch=44
set $mordn SystemInformationBlock3 snonintrasearch=0
set $mordn SystemInformationBlock3 qhyst=4
set $mordn threshServingLow 0
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,GeranFreqGroupRelation=1         qRxLevMin         -111
set $mordn qRxLevMin -124
set $mordn SystemInformationBlock3 sintrasearch=44
set $mordn SystemInformationBlock3 qhyst=4
done
fi

##L2100 Parameters

get ENodeBFunction=1,EUtranCellFDD earfcndl 240
if $nr_of_mos > 0
for $mo in F1
    $mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1 a3offsetAnrDelta 0
set $mordn dlInterferenceManagementActive TRUE
set $mordn CfraEnable True
set $mordn crsgain 0
set $mordn pdschTypeBGain 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrq -195
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -170
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -190
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrq -195
set $mordn pdcchCfiMode 5
set $mordn highSpeedUEActive False
set $mordn prsPowerBoosting 3
set $mordn cellRange 6
set $mordn noOfChannelSelectionsets 4
set $mordn channelSelectionsetSize 2
set $mordn,EUtranFreqRelation=.* caTriggeredRedirectionActive false
set $mordn,EUtranFreqRelation=39*.*,EUtranCellRelation=40410-9 coverageIndicator 0
set $mordn transmissionMode 4
set $mordn advCellSupAction 2
set $mordn advCellSupSensitivity 25
set $mordn covTriggerdBlindHoAllowed 0
set $mordn mobCtrlAtPoorCovActive true
set $mordn pMaxServingCell 1000
set $mordn preambleInitialReceivedTargetPower -110
set $mordn tTimeAlignmentTimer 0
set $mordn ul64qamEnabled True
set $mordn pZeroNominalPusch -100
set $mordn pZeroNominalPucch -110
set $mordn alpha 10
wait 2
set $mordn pdcchLaGinrMargin 40
set $mordn pdcchpowerboostmax 2
set $mordn qRxLevMinOffset 1000
set $mordn SystemInformationBlock6 tReselectionutra=4
set $mordn qQualMin -34
set $mordn qQualMinOffset 0
set $mordn,EUtranFreqRelation=.* qoffsetfreq 0
set $mordn,EUtranFreqRelation=.* tReselectionEutra 1
set $mordn,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set $mordn,UeMeasControl=1,ReportConfigA5=1 triggerquantitya5 0
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2EcNoUtra -180
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2RscpUtra -190
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 timeToTriggerB2 1280
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 a3offset 30
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 480
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 triggerQuantityA3 0
set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set $mordn,UeMeasControl=1 excludeInterFreqAtCritical False
set $mordn dlBlerTargetEnabled TRUE
set $mordn enableServiceSpecificHARQ TRUE
set $mordn pdcchOuterLoopInitialAdjVolte -46
set $mordn pdcchOuterLoopUpStepVolte 9
set $mordn pdcchTargetBlerVolte 18
set $mordn tReorderingAutoConfiguration true
set $mordn ulBlerTargetEnabled true
set $mordn ulHarqVolteBlerTarget 3
set $mordn pdcchOuterLoopInitialAdj -70
set $mordn pdcchOuterLoopInitialAdjPCell -70
set $mordn pdcchOuterLoopUpStep 8
set $mordn pdcchOuterLoopUpStepPCell 6
set $mordn pdcchTargetBler 24
set $mordn pdcchTargetBlerPCell 22
set $mordn ttiBundlingAfterHO 1
set $mordn ttiBundlingAfterReest 1
set $mordn ttiBundlingSwitchThres 150
set $mordn ttiBundlingSwitchThresHyst 30
set $mordn pdcchCovImproveDtx 1
set $mordn pdcchCovImproveSrb false
set $mordn pdcchCovImproveQci1 1
set $mordn adaptiveCfiHoProhibit 0
set $mordn allocThrPucchFormat1 50
set $mordn allocTimerPucchFormat1 50
set $mordn deallocThrPucchFormat1 100
set $mordn deallocTimerPucchFormat1 6000
set $mordn drxActive 1
set ExternalUtranCellFDD  srvccCapability 1
set $mordn,UeMeasControl=1,ReportConfigSearch=1 inhibitA2SearchConfig 0
set $mordn,UeMeasControl=1 measQuantityUtraFDD 1
set $mordn,UeMeasControl=1 ueMeasurementsActive 1
set $mordn enableSinrUplinkClpc 1
set $mordn,UeMeasControl=1 ueMeasurementsActiveIF true
set $mordn,UeMeasControl=1 ueMeasurementsActiveGERAN true
set $mordn,UeMeasControl=1                  a5B2MobilityTimer 0
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -140
set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp   -111
set $mordn,UtranFreqRelation b2Thr1RsrpUtraFreqOffset 0
set $mordn,UtranFreqRelation b2Thr2EcNoUtraFreqOffset 0
set $mordn,UeMeasControl=1         bothA5RsrpRsrqCheck True
set $mordn cellCapMaxCellSubCap 60000
set $mordn cellCapMinCellSubCap 1500
set $mordn cellCapMinMaxWriProt true
set $mordn cellSubscriptionCapacity 12000
set ENodeBFunction=1,$mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5 10
set $mordn,UeMeasControl=1                  inhibitB2RsrqConfig true
set $mordn,EUtranFreqRelation=39150         lbA5Thr1RsrpFreqOffset 51
set $mordn,EUtranFreqRelation=39294         lbA5Thr1RsrpFreqOffset 46
set $mordn,EUtranFreqRelation=1346         lbA5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=240         lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=3676         lbA5Thr1RsrpFreqOffset 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearch  40 
set $mordn,EUtranFreqRelation=.*,EUtranCellRelation=.* lbBnrAllowed true
set $mordn SystemInformationBlock3 snonintrasearchQ=0
set $mordn SystemInformationBlock3 sintrasearchp=44
set $mordn,EUtranFreqRelation=.* mobilityAction 1
set $mordn mappingInfo mappingInfoSIB3=1
set $mordn mappingInfo mappingInfoSIB5=3
set $mordn mappingInfo mappingInfoSIB7=5
set $mordn mappingInfo mappingInfoSIB12=7
set $mordn mappingInfo mappingInfoSIB4=2
set $mordn mappingInfo mappingInfoSIB6=4
set $mordn                                  lbEUtranAcceptOffloadThreshold  10
set $mordn                                  lbEUtranTriggerOffloadThreshold 30
set $mordn,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10
set $mordn                                 changeNotification changeNotificationSIB16=true
set $mordn                                 changeNotification changeNotificationSIB15=true
set $mordn                                 changeNotification changeNotificationSIB8=true
set $mordn commonSrPeriodicity 10
set $mordn ulInternalChannelBandwidth 0
set $mordn dlInternalChannelBandwidth 0
set $mordn dlFrequencyAllocationProportion 100
set $mordn dl256QamEnabled true
set $mordn servOrPrioTriggeredIFHo 0
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrp 4
set $mordn                                  cellDownlinkCaCapacity 0
set $mordn                            servOrPrioTriggeredErabAction 3 
set $mordn                                  hoOptAdjThresholdAbs 5
set $mordn                                  hoOptAdjThresholdPerc 50
set $mordn,MimoSleepFunction=1              switchUpMonitorDurTimer 15
set $mordn,UeMeasControl=1,ReportConfigEUtraBadCovPrim=1 a2ThresholdRsrpPrim -140
set $mordn                                 ns05FullBandUsersInCellThres 1
set $mordn,UeMeasControl=1                  filterCoefficientEUtraRsrq 11
set $mordn,EUtranFreqRelation=.*          allowedPlmnList   mcc=404,mnc=10,mncLength=2
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 maxReportCellsPm 8
set $mordn,UeMeasControl=1,ReportConfigEUtraIntraFreqPm=1 reportIntervalPm 5
set $mordn bsrThreshold 100
set $mordn noOfUlImprovedUe 2
set $mordn,EUtranFreqRelation=39150,EUtranCellRelation=40410-9 sCellCandidate 1
set $mordn,EUtranFreqRelation=39294,EUtranCellRelation=40410-9 sCellCandidate 1
###1345 & 39151
set $mordn,EUtranFreqRelation=1345 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=1345 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=1345 voicePrio  7
set $mordn,EUtranFreqRelation=1345 a5Thr1RsrpFreqOffset 11
set $mordn,EUtranFreqRelation=1345 a5Thr2RsrpFreqOffset 2
set $mordn,EUtranFreqRelation=1345  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1345 lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=1345 threshXHigh 10
set $mordn,EUtranFreqRelation=1345 qRxLevMin -124
set $mordn,EUtranFreqRelation=39151 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39151 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=39151 voicePrio  7
set $mordn,EUtranFreqRelation=39151 a5Thr1RsrpFreqOffset 13
set $mordn,EUtranFreqRelation=39151 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39151  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39151 lbA5Thr1RsrpFreqOffset 97
set $mordn,EUtranFreqRelation=39151 threshXHigh 10
set $mordn,EUtranFreqRelation=39151 qRxLevMin -124
### F1 LMS
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrq 10
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -104
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -170
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2criticalthresholdRSRp -140
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset -20
set $mordn,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -50
set $mordn,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrqQciOffset=0,a1a2ThrRsrpQciOffset=0
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -114
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -114
set $mordn,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp -140
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -90
set $mordn,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set $mordn qRxLevMin -124
set $mordn SystemInformationBlock3 sintrasearch=44
set $mordn SystemInformationBlock3 snonintrasearch=8
set $mordn SystemInformationBlock3 snonintrasearchP=10
set $mordn SystemInformationBlock3 qhyst=4
set $mordn threshServingLow 8
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrpFreqOffset 10
set $mordn,EUtranFreqRelation=240 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1346 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3676 a5Thr1RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39150 a5Thr1RsrqFreqOffset 10
set $mordn,EUtranFreqRelation=39294 a5Thr1RsrqFreqOffset 10
set $mordn,EUtranFreqRelation=240 a5Thr1RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=1346 a5Thr1RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=3676 a5Thr1RsrqFreqOffset 10
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr2RsrqFreqOffset 0
set $mordn,EUtranFreqRelation=1346 a5Thr2RsrqFreqOffset 70
set $mordn,EUtranFreqRelation=3676 a5Thr2RsrqFreqOffset 150
set $mordn,EUtranFreqRelation=39150  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=68,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39294  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=68,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=240  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=0,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=1346  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-90,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=3676  EUtranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=-240,a5Thr2RsrqFreqQciOffset=-170,lbQciProfileHandling=1
set $mordn,EUtranFreqRelation=39150 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=39294 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=240 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=1346 a5Thr2RsrpFreqOffset 0
set $mordn,EUtranFreqRelation=3676 a5Thr2RsrpFreqOffset 4
set $mordn,EUtranFreqRelation=39150 cellReselectionPriority 7
set $mordn,EUtranFreqRelation=39294 cellReselectionPriority 6
set $mordn,EUtranFreqRelation=240 cellReselectionPriority 5
set $mordn,EUtranFreqRelation=1346 cellReselectionPriority 4
set $mordn,EUtranFreqRelation=3676 cellReselectionPriority 3
set $mordn,GeranFreqGroupRelation=1         cellReselectionPriority 1
set $mordn,GeranFreqGroupRelation=1         connectedModeMobilityPrio -1
set $mordn,EUtranFreqRelation=39150 connectedmodemobilityprio 7
set $mordn,EUtranFreqRelation=39294 connectedmodemobilityprio 6
set $mordn,EUtranFreqRelation=240 connectedmodemobilityprio 5
set $mordn,EUtranFreqRelation=1346 connectedmodemobilityprio 4
set $mordn,EUtranFreqRelation=3676 connectedmodemobilityprio 3
set $mordn,EUtranFreqRelation=.* qRxLevMin -124
set $mordn,GeranFreqGroupRelation=1         qRxLevMin         -111
set $mordn,EUtranFreqRelation=.* threshXHigh 12
set $mordn,EUtranFreqRelation=1346 threshXLow 12
set $mordn,EUtranFreqRelation=3676 threshXLow 12
set $mordn,GeranFreqGroupRelation=1     threshXLow  62
set $mordn,EUtranFreqRelation=39150 voicePrio -1
set $mordn,EUtranFreqRelation=39294 voicePrio -1
set $mordn,EUtranFreqRelation=240 voicePrio 6
set $mordn,EUtranFreqRelation=1346 voicePrio 7
set $mordn,EUtranFreqRelation=3676 voicePrio 5
set $mordn,GeranFreqGroupRelation=1         voicePrio     -1
set $mordn,EUtranFreqRelation  interFreqMeasType 0
set $mordn,UeMeasControl=1                  ueMeasurementsActiveGERAN True
set $mordn ulTrigActive False
done
fi


set  EUtranCellTDD=*.*,EUtranFreqRelation=39150 isHoAllowed 1
set  EUtranCellTDD=*.*,EUtranFreqRelation=39294 isHoAllowed 1
set  EUtranCellTDD=*.*,EUtranFreqRelation=240 isHoAllowed 1
set  EUtranCellTDD=*.*,EUtranFreqRelation=1346 isHoAllowed 1



##GERANPARAMETERSANDFEATURES

set ENodeBFunction csfbMeasFromIdleMode true
set ReportConfigCsfbGeran thresholdGeran -110
set ReportConfigCsfbGeran hysteresis 10
set ReportConfigCsfbGeran timetotrigger 40

set AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1


set CXC4011664 featurestate 0
set CXC4011663 featurestate 0
set CXC4010956 featurestate 1


set TDD mappingInfo mappingInfoSIB7=5
set FDD mappingInfo mappingInfoSIB7=5

#GERAN CSFB/SRVCC Parameter

set GeranFreqGroupRelation=1         csFallbackPrio    4
set GeranFreqGroupRelation=1         csFallbackPrioEC    4
set AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1
set GeranFreqGroup pmaxgeran 1000
set GeranFreqGroup Qoffsetfreq 0
set GeranFreqGroup nccpermitted 11111111
set GeranFreqGroup anrMeasOn TRUE
set GeranFreqGroup mobilityAction 1
set GeranFreqGroup mobilityActionCsfb 1
set GeranFreqGroup userLabel SIB7
set CXC4011664 featurestate 0
set CXC4011346 featurestate 1
set CXC4012240 featurestate 1
set CXC4010618 featurestate 1


set . srvccDelayTimer 3000
set EUtranCellFDD=DL_E_F3_.*,UeMeasControl=1,ReportConfigB2Geran=1 timeToTriggerB2   1280
seti EUtranCellFDD=DL_.*,UeMeasControl=1,ReportConfigB2Geran=1 reportIntervalB2   4

#RIM

set CXC4010973 featurestate 1
set ENodeBFunction=1                                        forcedSiTunnelingActive false
set CXC4010956 featurestate 1

#PLMN Whitelist GERAN

cr ENodeBFunction=1,PlmnInfo=1
mcc=404,mnc=10,mnclength=2
set ENodeBFunction=1,PlmnInfo=1 plmnWhiteList mcc=404,mnc=10,mnclength=2
set AnrFunction=1                                           plmnWhiteListGeranEnabled true
set AnrFunction=1                                           plmnWhiteListEnabled true

set EutrancellFDD=DL_E_F1_OM_.* noOfPucchSrUsers 420
set EutrancellFDD=DL_E_F1_OM_.* noOfPucchCqiUsers 320


set . tRrcConnectionSetup 10

##Features_GPL

set  CXC4011713   featurestate  0 
set  CXC4012238   featurestate  1
set  CXC4012097   featurestate  1
set  CXC4011368   featurestate  0 
set  CXC4012036   featurestate  1
set  CXC4010512   featurestate  0
set  CXC4010955   featurestate  0
set  CXC4010973   featurestate  1
set  CXC4011055   featurestate  0
set  CXC4011246   featurestate  0
set  CXC4011346   featurestate  1
set  CXC4011478   featurestate  0
set  cxc4011554   featurestate  0
set  CXC4011663   featurestate  0
set  CXC4011664   featurestate  0
set  CXC4011736   featurestate  0
set  CXC4011810   featurestate  0
set  cxc4011911   featurestate  0
set  cxc4011966   featurestate  0
set  CXC4011983   featurestate  1
set  CXC4011714   featurestate  0
set  CXC4010319   featurestate  1
set  CXC4010320   featurestate  1
set  CXC4010609   featurestate  1
set  CXC4010613   featurestate  1
set  CXC4010616   featurestate  1
set  CXC4010618   featurestate  1
set  CXC4010620   featurestate  1
set  CXC4010717   featurestate  1
set  CXC4010723   featurestate  1
set  CXC4010770   featurestate  1
set  CXC4010841   featurestate  1
set  CXC4010856   featurestate  1
set  CXC4010912   featurestate  1
set  CXC4010956   featurestate  1
set  CXC4010959   featurestate  1
set  CXC4010961   featurestate  1
set  CXC4010962   featurestate  1
set  CXC4010967   featurestate  1
set  CXC4010974   featurestate  1
set  CXC4010980   featurestate  1
set  CXC4010990   featurestate  1
set  CXC4011011   featurestate  1
set  CXC4011033   featurestate  1
set  CXC4011034   featurestate  1
set  CXC4011050   featurestate  1
set  CXC4011057   featurestate  1
set  CXC4011059   featurestate  1
set  CXC4011060   featurestate  1
set  CXC4011061   featurestate  1
set  CXC4011062   featurestate  1
set  CXC4011064   featurestate  1
set  CXC4011074   featurestate  1
set  CXC4011075   featurestate  1
set  CXC4011157   featurestate  1
set  CXC4011183   featurestate  1
set  CXC4011245   featurestate  1
set  CXC4011247   featurestate  1
set  CXC4011251   featurestate  1
set  CXC4011252   featurestate  1
set  CXC4011253   featurestate  1
set  CXC4011255   featurestate  1
set  CXC4011258   featurestate  1
set  CXC4011319   featurestate  1
set  CXC4011327   featurestate  1
set  CXC4011345   featurestate  1
set  CXC4011366   featurestate  1
set  CXC4011370   featurestate  1
set  CXC4011372   featurestate  1
set  CXC4011373   featurestate  1
set  CXC4011376   featurestate  1
set  CXC4011378   featurestate  1
set  CXC4011422   featurestate  1
set  CXC4011443   featurestate  1
set  CXC4011444   featurestate  1
set  CXC4011477   featurestate  1
set  CXC4011479   featurestate  1
set  CXC4011481   featurestate  1
set  CXC4011482   featurestate  1
set  CXC4011485   featurestate  1
set  CXC4011515   featurestate  1
set  CXC4011698   featurestate  1
set  CXC4011711   featurestate  1
set  CXC4011715   featurestate  1
set  CXC4011813   featurestate  1
set  CXC4011815   featurestate  1
set  CXC4011910   featurestate  1
set  CXC4011913   featurestate  0
set  CXC4011914   featurestate  1
set  CXC4011918   featurestate  1
set  CXC4011940   featurestate  1
set  CXC4011941   featurestate  1
set  CXC4011969   featurestate  1
set  CXC4012003   featurestate  1
set  CXC4012018   featurestate  1
set  CXC4012070   featurestate  1
set  CXC4012089   featurestate  1
set  CXC4011559   featurestate  1
set  CXC4011922   featurestate  1
set  CXC4011946   featurestate  1
set  CXC4012129   featurestate  1
set  CXC4012240   featurestate  1
set  CXC4011072   featurestate  1
set  CXC4011974	  featurestate  1 	

##20Q2 Features-

set CXC4012316 featurestate 1
set CXC4012271 featurestate 1
set CXC4012260 featurestate 1
set CXC4012374 featurestate 1
set CXC4012344 featurestate 0
set CXC4012370 featurestate 0
set CXC4012326 featurestate 1
set CXC4012349 featurestate 1
set CXC4012261 featurestate 1


#FORTDDSITEONLY4x4Quad

set  CXC4011667   featurestate  1
set  CXC4011056   featurestate  1

#OLD Running Features

set  CXC4010949   featurestate  1
set  CXC4010963   featurestate  1
set  CXC4010964   featurestate  1
set  CXC4011063   featurestate  1
set  CXC4011065   featurestate  1
set  CXC4011067   featurestate  1
set  CXC4011068   featurestate  1
set  CXC4011069   featurestate  1
set  CXC4011155   featurestate  1
set  CXC4011163   featurestate  1
set  CXC4011256   featurestate  1
set  CXC4011317   featurestate  1
set  CXC4011356   featurestate  1
set  CXC4011427   featurestate  1
set  CXC4011512   featurestate  1
set  CXC4011557   featurestate  1
set  CXC4011618   featurestate  1
set  CXC4011666   featurestate  1
set  CXC4011699   featurestate  1
set  CXC4011707   featurestate  1
set  CXC4011710   featurestate  1
set  CXC4011716   featurestate  1
set  CXC4011803   featurestate  1
set  CXC4011804   featurestate  1
set  CXC4011807   featurestate  1
set  CXC4011808   featurestate  1
set  CXC4011809   featurestate  1
set  CXC4011811   featurestate  1
set  CXC4011814   featurestate  1
set  CXC4011817   featurestate  1
set  CXC4011820   featurestate  1
set  CXC4011917   featurestate  1
set  CXC4011930   featurestate  1
set  CXC4011933   featurestate  1
set  CXC4011937   featurestate  1
set  CXC4011938   featurestate  1
set  CXC4011939   featurestate  1
set  CXC4011942   featurestate  1
set  CXC4011951   featurestate  1
set  CXC4011958   featurestate  1
set  CXC4011967   featurestate  1
set  CXC4011973   featurestate  1
set  CXC4011975   featurestate  1
set  CXC4011982   featurestate  1
set  CXC4011991   featurestate  1
set  CXC4012022   featurestate  1
set  CXC4040004   featurestate  1
set  CXC4040005   featurestate  1
set  CXC4040006   featurestate  1
set  CXC4040008   featurestate  1
set  CXC4040009   featurestate  1
set  CXC4040010   featurestate  1
set  CXC4040013   featurestate  1
set  CXC4040014   featurestate  1
set CXC4012259 featurestate 1


#RANFEATUREFORMME

set  CXC4011823   featurestate  1


##GERANPARAMETERSANDFEATURES

set ENodeBFunction csfbMeasFromIdleMode true
set ReportConfigCsfbGeran thresholdGeran -110
set ReportConfigCsfbGeran hysteresis 10
set ReportConfigCsfbGeran timetotrigger 40

set AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1


set CXC4011664 featurestate 0
set CXC4011663 featurestate 0
set CXC4010956 featurestate 1


set TDD mappingInfo mappingInfoSIB7=5
set FDD mappingInfo mappingInfoSIB7=5

#GERAN CSFB/SRVCC Parameter

set GeranFreqGroupRelation=1         csFallbackPrio    4
set GeranFreqGroupRelation=1         csFallbackPrioEC    4
set AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1
set GeranFreqGroup qRxLevMin -111
set GeranFreqGroup pmaxgeran 1000
set GeranFreqGroup Qoffsetfreq 0
set GeranFreqGroup nccpermitted 11111111
set GeranFreqGroup anrMeasOn TRUE
set GeranFreqGroup mobilityAction 1
set GeranFreqGroup mobilityActionCsfb 1
set GeranFreqGroup userLabel SIB7
set CXC4011346 featurestate 1
set CXC4012240 featurestate 1
set CXC4010618 featurestate 1
set . srvccDelayTimer 3000

set EUtranCell.*,UeMeasControl=1,ReportConfigB2Geran=1 timeToTriggerB2   1280


set GeranFreqGroupRelation=1         connectedModeMobilityPrio -1

#RIM

set CXC4010973 featurestate 1
set ENodeBFunction=1                                        forcedSiTunnelingActive false
set CXC4010956 featurestate 1

#PLMN Whitelist GERAN

cr ENodeBFunction=1,PlmnInfo=1
mcc=404,mnc=10,mnclength=2
set ENodeBFunction=1,PlmnInfo=1 plmnWhiteList mcc=404,mnc=10,mnclength=2
set AnrFunction=1                                           plmnWhiteListGeranEnabled true
set AnrFunction=1                                           plmnWhiteListEnabled true


set EUtranCellFDD=DL_.*,EUtranFreqRelation=.* tReselectionEutra 1
set EUtranCellTDD=DL_.*,EUtranFreqRelation=.* tReselectionEutra 1
set EUtranFreqRelation=.* lbBnrPolicy 2
set EUtranCellFDD=.*,EUtranFreqRelation=.* caTriggeredRedirectionActive false
set EUtranCellTDD=.*,EUtranFreqRelation=.* caTriggeredRedirectionActive false


set . pZeroNominalPucch -110
set . pZeroNominalPusch -100
set . alpha 10

scw 1566:33,1627:3,153:128,278:1,296:200,1738:230,2959:1,1225:50,3918:0
sysconwrite 3918 0

set ENodeBFunction=1 timeAndPhaseSynchAlignment 1

set SystemFunctions=1,Lm=1,FeatureState=CXC4011955 featureState 0
set  CXC4011955   featurestate  0
set ENodeBFunction=1 ulPhyProcResTradingEnabled 1

set EUTRANCELLTDD=DL_E_T2_.*  noOfPucchFormat1PrbPairsPerFrameConf  14  
set EUTRANCELLTDD=DL_E_T1_.*  noOfPucchFormat1PrbPairsPerFrameConf  8 
set EUTRANCELLTDD=DL_E_T2_.*  noOfPucchFormat2PrbPairsPerFrameConf  7 
set EUTRANCELLTDD=DL_E_T1_.*  noOfPucchFormat2PrbPairsPerFrameConf  5  
set EUTRANCELLFDD=DL_E_F1_.*  noOfPucchFormat1PrbPairsPerFrameConf  3
set EUTRANCELLFDD=DL_E_F1_.*  noOfPucchFormat2PrbPairsPerFrameConf  2  
set EUTRANCELLFDD=DL_E_F3_.*  noOfPucchFormat1PrbPairsPerFrameConf  2
set EUTRANCELLFDD=DL_E_F3_.*  noOfPucchFormat2PrbPairsPerFrameConf  1
set EUTRANCELLFDD=DL_E_F8_.*  noOfPucchFormat1PrbPairsPerFrameConf  2
set EUTRANCELLFDD=DL_E_F8_.*  noOfPucchFormat2PrbPairsPerFrameConf  1

set EUTRANCELLTDD=LD.....[ABCDEF]  noOfPucchFormat1PrbPairsPerFrameConf  14  
set EUTRANCELLTDD=LD.....[STUVWX]  noOfPucchFormat1PrbPairsPerFrameConf  8 
set EUTRANCELLTDD=LD.....[ABCDEF]  noOfPucchFormat2PrbPairsPerFrameConf  7 
set EUTRANCELLTDD=LD.....[STUVWX]  noOfPucchFormat2PrbPairsPerFrameConf  5  
set EUTRANCELLFDD=LU.....[KLMNOP]  noOfPucchFormat1PrbPairsPerFrameConf  3
set EUTRANCELLFDD=LU.....[KLMNOP]  noOfPucchFormat2PrbPairsPerFrameConf  2  
set EUTRANCELLFDD=LD.....[KLMNOP]  noOfPucchFormat1PrbPairsPerFrameConf  2
set EUTRANCELLFDD=LD.....[KLMNOP]  noOfPucchFormat2PrbPairsPerFrameConf  1
set EUTRANCELLFDD=LD.....[GHIJYZ]  noOfPucchFormat1PrbPairsPerFrameConf  2
set EUTRANCELLFDD=LD.....[GHIJYZ]  noOfPucchFormat2PrbPairsPerFrameConf  1

set EUTRANCELLTDD=DL_E_T2_.*  noOfPucchSrUsers   970  
set EUTRANCELLTDD=LD.....[ABCDEF]  noOfPucchSrUsers   970 
set EUTRANCELLTDD=DL_E_T1_.*  noOfPucchSrUsers   710  
set EUTRANCELLTDD=LD.....[STUVWX]  noOfPucchSrUsers   710           
set EutrancellTDD=.* noOfPucchCqiUsers   620 

set EUTRANCELLFDD=DL_E_F8_.*  noOfPucchSrUsers   160  
set EUTRANCELLFDD=LD.....[GHIJYZ]  noOfPucchSrUsers   160 
set EUTRANCELLFDD=DL_E_F8_.*  noOfPucchCqiUsers  160
set EUTRANCELLFDD=LD.....[GHIJYZ]  noOfPucchCqiUsers  160

set EUTRANCELLFDD=DL_E_F3_.*  noOfPucchSrUsers   780 
set EUTRANCELLFDD=LD.....[KLMNOP]  noOfPucchSrUsers   780   
set EUTRANCELLFDD=DL_E_F3_.*  noOfPucchCqiUsers  640
set EUTRANCELLFDD=LD.....[KLMNOP]  noOfPucchCqiUsers  640

set EUTRANCELLFDD=DL_E_F1_.*  noOfPucchSrUsers   420
set EUTRANCELLFDD=LU.....[KLMNOP]  noOfPucchSrUsers   420
set EUTRANCELLFDD=DL_E_F1_.*  noOfPucchCqiUsers  320
set EUTRANCELLFDD=LU.....[KLMNOP]  noOfPucchCqiUsers  320

#Addition
            
lset QciTable=default,qciprofilepredefined=qci2 drxProfileRef drxprofile=2
lset QciTable=default,qciprofilepredefined=qci1 drxProfileRef drxprofile=1
set AnrFunction=1 pciConflictMobilityEcgiMeas FALSE
set AnrFunction=1 pciConflictDetectionEcgiMeas FALSE
set ENodeBFunction=1 rrcConnReestActive TRUE

set ENodeBFunction=1,AnrFunction=1 pciConflictMobilityEcgiMeas       false
set ENodeBFunction=1,AnrFunction=1 pciConflictDetectionEcgiMeas      false

set $mordn SystemInformationBlock3 snonintrasearchP=10

set SystemFunctions=1,Lm=1,FeatureState=CXC4011955 featureState 0
set ENodeBFunction=1 ulPhyProcResTradingEnabled 1


set EUTRANCELLTDD=DL_E_T2_.*  noOfPucchFormat1PrbPairsPerFrameConf  14
set EUTRANCELLTDD=DL_E_T2_.*  noOfPucchFormat2PrbPairsPerFrameConf  7   
set EUTRANCELLTDD=DL_E_T1_.*  noOfPucchFormat1PrbPairsPerFrameConf  8 
set EUTRANCELLTDD=DL_E_T1_.*  noOfPucchFormat2PrbPairsPerFrameConf  5  
set EUTRANCELLFDD=DL_E_F1_.*  noOfPucchFormat1PrbPairsPerFrameConf  3
set EUTRANCELLFDD=DL_E_F1_.*  noOfPucchFormat2PrbPairsPerFrameConf  2  
set EUTRANCELLFDD=DL_E_F3_.*  noOfPucchFormat1PrbPairsPerFrameConf  2
set EUTRANCELLFDD=DL_E_F3_.*  noOfPucchFormat2PrbPairsPerFrameConf  1
set EUTRANCELLFDD=DL_E_F8_.*  noOfPucchFormat1PrbPairsPerFrameConf  2
set EUTRANCELLFDD=DL_E_F8_.*  noOfPucchFormat2PrbPairsPerFrameConf  1

set EUTRANCELLTDD=LD.....[ABCDEF]  noOfPucchFormat1PrbPairsPerFrameConf  14  
set EUTRANCELLTDD=LD.....[ABCDEF]  noOfPucchFormat2PrbPairsPerFrameConf  7 
set EUTRANCELLTDD=LD.....[STUVWX]  noOfPucchFormat1PrbPairsPerFrameConf  8 
set EUTRANCELLTDD=LD.....[STUVWX]  noOfPucchFormat2PrbPairsPerFrameConf  5  
set EUTRANCELLFDD=LU.....[KLMNOP]  noOfPucchFormat1PrbPairsPerFrameConf  3
set EUTRANCELLFDD=LU.....[KLMNOP]  noOfPucchFormat2PrbPairsPerFrameConf  2  
set EUTRANCELLFDD=LD.....[KLMNOP]  noOfPucchFormat1PrbPairsPerFrameConf  2
set EUTRANCELLFDD=LD.....[KLMNOP]  noOfPucchFormat2PrbPairsPerFrameConf  1
set EUTRANCELLFDD=LD.....[GHIJYZ]  noOfPucchFormat1PrbPairsPerFrameConf  2
set EUTRANCELLFDD=LD.....[GHIJYZ]  noOfPucchFormat2PrbPairsPerFrameConf  1



set EUTRANCELLTDD=DL_E_T2_.*  noOfPucchSrUsers   970  
set EUTRANCELLTDD=LD.....[ABCDEF]  noOfPucchSrUsers   970 
set EUTRANCELLTDD=DL_E_T1_.*  noOfPucchSrUsers   710  
set EUTRANCELLTDD=LD.....[STUVWX]  noOfPucchSrUsers   710           
set EutrancellTDD=.* noOfPucchCqiUsers   620 

set EUTRANCELLFDD=DL_E_F8_.*  noOfPucchSrUsers   160  
set EUTRANCELLFDD=LD.....[GHIJYZ]  noOfPucchSrUsers   160 
set EUTRANCELLFDD=DL_E_F8_.*  noOfPucchCqiUsers  160
set EUTRANCELLFDD=LD.....[GHIJYZ]  noOfPucchCqiUsers  160

set EUTRANCELLFDD=DL_E_F3_.*  noOfPucchSrUsers   780 
set EUTRANCELLFDD=LD.....[KLMNOP]  noOfPucchSrUsers   780   
set EUTRANCELLFDD=DL_E_F3_.*  noOfPucchCqiUsers  640
set EUTRANCELLFDD=LD.....[KLMNOP]  noOfPucchCqiUsers  640

set EUTRANCELLFDD=DL_E_F1_.*  noOfPucchSrUsers   420
set EUTRANCELLFDD=LU.....[KLMNOP]  noOfPucchSrUsers   420
set EUTRANCELLFDD=DL_E_F1_.*  noOfPucchCqiUsers  320
set EUTRANCELLFDD=LU.....[KLMNOP]  noOfPucchCqiUsers  320


st ENodeBFunction=1,EUtranCellTDD=
wait 1
if $nr_of_mos != 0 
Set CXC4012271 Featurestate 1
Set CXC4012316 Featurestate 1
Set CXC4012374 Featurestate 1
Set CXC4012260 Featurestate 1
Set CXC4012326 Featurestate 1
Set CXC4011476 Featurestate 1

Set CXC4012344 Featurestate 0
Set CXC4012256 Featurestate 1

scw 4292:10
done
else 
fi


get ENodeBFunction=1,EUtranCellTDD earfcn 39150
if $nr_of_mos > 0
for $mo in T2
 $mordn = rdn($mo)
set $mordn subframeAssignment 2
set $mordn specialSubframePattern 7
set $mordn ductIntOpMode 3
set EUtranCellTDD=.*   ductIntOpMode  3
set EUtranCellTDD=.*   ductIntPerfTuning ductIntCharSeqPwrThr=-105
set $mordn ductIntPerfTuning ductIntBgNoiseThr=-105
set $mordn ductIntPerfTuning ductIntCharSeqCorrPeakThr=50
set $mordn ductIntPerfTuning ductIntCharSeqPwrDiff=5
set $mordn ductIntPerfTuning ductIntRedTriggerThr=14
set $mordn ductIntPerfTuning ductIntRedRecovThr=10
set . ductIntCharInfoScheme 0
set . ductIntFlexibleDetectionEnabled FALSE
set $mordn ul256qamEnabled True
done
else 
fi

get ENodeBFunction=1,EUtranCellTDD earfcn 39294
if $nr_of_mos > 0
for $mo in T1
 $mordn = rdn($mo)
set $mordn subframeAssignment 2
set $mordn specialSubframePattern 7
set $mordn ductIntOpMode 3
set EUtranCellTDD=.*   ductIntOpMode  3
set EUtranCellTDD=.*   ductIntPerfTuning ductIntCharSeqPwrThr=-105
set $mordn ductIntPerfTuning ductIntBgNoiseThr=-105
set $mordn ductIntPerfTuning ductIntCharSeqCorrPeakThr=50
set $mordn ductIntPerfTuning ductIntCharSeqPwrDiff=5
set $mordn ductIntPerfTuning ductIntRedTriggerThr=14
set $mordn ductIntPerfTuning ductIntRedRecovThr=10
set . ductIntCharInfoScheme 0
set . ductIntFlexibleDetectionEnabled FALSE
set $mordn ul256qamEnabled True
done
else 
fi

get ENodeBFunction=1,EUtranCellTDD earfcn 39151
if $nr_of_mos > 0
for $mo in SMALL
 $mordn = rdn($mo)
set $mordn subframeAssignment 2
set $mordn specialSubframePattern 7
set $mordn ductIntOpMode 3
set EUtranCellTDD=.*   ductIntOpMode  3
set EUtranCellTDD=.*   ductIntPerfTuning ductIntCharSeqPwrThr=-105
set $mordn ductIntPerfTuning ductIntBgNoiseThr=-105
set $mordn ductIntPerfTuning ductIntCharSeqCorrPeakThr=50
set $mordn ductIntPerfTuning ductIntCharSeqPwrDiff=5
set $mordn ductIntPerfTuning ductIntRedTriggerThr=14
set $mordn ductIntPerfTuning ductIntRedRecovThr=10
set EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqTransThr=10
set EUtranCellTDD=.* ductIntPerfTuning ductIntSlopePwrDiffThr=3
set . ductIntCharInfoScheme 0
set . ductIntFlexibleDetectionEnabled FALSE
set $mordn ul256qamEnabled True
done
else 
fi

ma Smal10 EUtranCellTDD earfcn 39001
wait 1
if $nr_of_mos != 0 
for $mo in Smal10
$mordn = rdn($mo)
set $mordn subframeAssignment 2
set $mordn specialSubframePattern 7
set $mordn ductIntOpMode 3
set EUtranCellTDD=.*   ductIntPerfTuning ductIntCharSeqPwrThr=-105
set $mordn ductIntPerfTuning ductIntBgNoiseThr=-105
set $mordn ductIntPerfTuning ductIntCharSeqCorrPeakThr=50
set $mordn ductIntPerfTuning ductIntCharSeqPwrDiff=5
set $mordn ductIntPerfTuning ductIntRedTriggerThr=14
set $mordn ductIntPerfTuning ductIntRedRecovThr=10
set . ductIntCharInfoScheme 0
set . ductIntFlexibleDetectionEnabled FALSE
set $mordn ul256qamEnabled True
done
else 
fi

set EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqTransThr=10
set EUtranCellTDD=.* ductIntPerfTuning ductIntSlopePwrDiffThr=3
set EUtranCellTDD=.* ductIntPerfTuning ductIntSlopeDetectPeriod=10
set EUtranCellTDD=.* ductIntPerfTuning ductIntSlopeDetectRatioThr=50
set EUTRANCELLTDD=DL_E_T2_.*  channelBandwidth  20000  
set EUTRANCELLTDD=DL_E_T1_.*  channelBandwidth  10000 

set . celltracefilesize 20000

set SystemFunctions=1,Lm=1,FeatureState=CXC4011476 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011922 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011666 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011559 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012259 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012123 featureState 1
set Licensing=1,OptionalFeatureLicense=CarrierAggregation$  featureState  1
set Licensing=1,OptionalFeatureLicense=CarrierAggregationFddTdd$  featureState  1
set Licensing=1,OptionalFeatureLicense=CarrierAggregationAwareIFLB$  featureState  1
set Licensing=1,OptionalFeatureLicense=DynamicScellSelection$  featureState  1
set Licensing=1,OptionalFeatureLicense=VoLTEOptimizedCA$  featureState  1
set FeatureState=CXC4012123 featureState 1
set Licensing=1,OptionalFeatureLicense=AutomaticSCellManagement$  featureState  1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011983 featureState 1
set Licensing=1,OptionalFeatureLicense=InterENBCarrierAggregation$  featureState  1
set EUtranCell.*=.* sCellHandlingAtVolteCall 1
set EUtranCell.*=.*,EUtranFreqRelation=.*,EUtranCellRelation=.* sCellCandidate    2
set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=39294 asmSCellDetection 3
set EUtranCellFDD=LD.*[K,L,M,N,O,P],EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellFDD=LD.*[K,L,M,N,O,P],EUtranFreqRelation=39294 asmSCellDetection 3
set EUtranCellTDD=DL_E_T1_.*,EUtranFreqRelation=39294 asmSCellDetection 3
set EUtranCellTDD=DL_E_T2_.*,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellTDD=DL_E_T1_.*,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellTDD=DL_E_T2_.*,EUtranFreqRelation=39294 asmSCellDetection 3

set EUtranCellTDD=DL_E_T1_.*,EUtranFreqRelation=240 asmSCellDetection 0
set EUtranCellTDD=DL_E_T2_.*,EUtranFreqRelation=240 asmSCellDetection 0
set EUtranCellTDD=DL_E_T1_.*,EUtranFreqRelation=3676 asmSCellDetection 0
set EUtranCellTDD=DL_E_T2_.*,EUtranFreqRelation=3676 asmSCellDetection 0
set EUtranCellTDD=DL_E_T1_.*,EUtranFreqRelation=1346 asmSCellDetection 0
set EUtranCellTDD=DL_E_T2_.*,EUtranFreqRelation=1346 asmSCellDetection 0
set EUtranCellTDD=DL_E_T1_.*,EUtranFreqRelation=1345 asmSCellDetection 0
set EUtranCellTDD=DL_E_T2_.*,EUtranFreqRelation=1345 asmSCellDetection 0
set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=240 asmSCellDetection 0
set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=240 asmSCellDetection 0
set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=3676 asmSCellDetection 0
set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=3676 asmSCellDetection 0
set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=1345 asmSCellDetection 0
set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=1345 asmSCellDetection 0
set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=1346 asmSCellDetection 0
set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=1346 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=1300 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=1345 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=240 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=1346 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=3665 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=3667 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=39150 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=39151 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=39294 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=39299 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=265 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=39025 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=3676 asmSCellDetection 0
set EUtranCellFDD=DL_E_F1_.*,EUtranFreqRelation=39000 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=1300 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=1345 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=240 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=1346 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=3665 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=3667 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=39150 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=39151 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=39294 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=39299 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=265 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=39025 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=3676 asmSCellDetection 0
set EUtranCellFDD=DL_E_F8_.*,EUtranFreqRelation=39000 asmSCellDetection 0

set EUtranCellTDD=LD.*,EUtranFreqRelation=39294 asmSCellDetection 3
set EUtranCellTDD=LD.*,EUtranFreqRelation=39150 asmSCellDetection 3

set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=39294  caTriggeredRedirectionActive true
set EUtranCellFDD=DL_E_F3_.*,EUtranFreqRelation=39150  caTriggeredRedirectionActive true
set EUtranCellFDD=LD.*[K,L,M,N,O,P],EUtranFreqRelation=39294  caTriggeredRedirectionActive true
set EUtranCellFDD=LD.*[K,L,M,N,O,P],EUtranFreqRelation=39150  caTriggeredRedirectionActive true

set CarrierAggregationFunction=1$ dynamicSCellSelectionMethod 3
set SystemFunctions=1,Lm=1,FeatureState=CXC4012111 featureState 1
set Licensing=1,OptionalFeatureLicense=GlobalSCellEvaluation$ featureState 1

set LM=1,featurestate=CXC4012199 featureState 1
set LM=1,featurestate=CXC4012485 featureState 1
set LM=1,featurestate=CXC4012356 featureState 1
set LM=1,featurestate=CXC4011984 featureState 0
set LM=1,featurestate=CXC4011913 featureState 0

cr ENodeBFunction=1,SubscriberGroupProfile=1
set ENodeBFunction=1,SubscriberGroupProfile=1 bearerTriggerList qci=1
set ENodeBFunction=1,SubscriberGroupProfile=1 fastACqiReportEnabled True
set ENodeBFunction=1,SubscriberGroupProfile=1 profilePriority  10
set ENodeBFunction=1,SubscriberGroupProfile=1 dlDynBlerTargetMax -1
set ENodeBFunction=1,SubscriberGroupProfile=1 dlDynBlerTargetMin 1
set . dlMaxRetxRrcReleaseThr 8
set . tPollRetxRrcReleaseDl 80
set . dlActivitySubscrDelay 1
set . reportDlActivity 1
cr ENodeBFunction=1,SubscriberGroupProfile=2
set ENodeBFunction=1,SubscriberGroupProfile=2 bearerTriggerList qci=6
set ENodeBFunction=1,SubscriberGroupProfile=2 profilePriority  1
set ENodeBFunction=1,SubscriberGroupProfile=2 dlDynBlerTargetAlg 1
set ENodeBFunction=1,SubscriberGroupProfile=2 dlDynBlerTargetMin 10
set ENodeBFunction=1,SubscriberGroupProfile=2 dlDynBlerTargetMax 60
cr ENodeBFunction=1,SubscriberGroupProfile=3
set ENodeBFunction=1,SubscriberGroupProfile=3 bearerTriggerList qci=7
set ENodeBFunction=1,SubscriberGroupProfile=3 profilePriority  1
set ENodeBFunction=1,SubscriberGroupProfile=3 dlDynBlerTargetAlg 1
set ENodeBFunction=1,SubscriberGroupProfile=3 dlDynBlerTargetMin 10
set ENodeBFunction=1,SubscriberGroupProfile=3 dlDynBlerTargetMax 60
cr ENodeBFunction=1,SubscriberGroupProfile=4
set ENodeBFunction=1,SubscriberGroupProfile=4 bearerTriggerList qci=8
set ENodeBFunction=1,SubscriberGroupProfile=4 profilePriority  1
set ENodeBFunction=1,SubscriberGroupProfile=4 dlDynBlerTargetAlg 1
set ENodeBFunction=1,SubscriberGroupProfile=4 dlDynBlerTargetMin 10
set ENodeBFunction=1,SubscriberGroupProfile=4 dlDynBlerTargetMax 60
cr ENodeBFunction=1,SubscriberGroupProfile=5
set ENodeBFunction=1,SubscriberGroupProfile=5 bearerTriggerList qci=9
set ENodeBFunction=1,SubscriberGroupProfile=5 profilePriority  1
set ENodeBFunction=1,SubscriberGroupProfile=5 dlDynBlerTargetAlg 1
set ENodeBFunction=1,SubscriberGroupProfile=5 dlDynBlerTargetMin 10
set ENodeBFunction=1,SubscriberGroupProfile=5 dlDynBlerTargetMax 60

set LM=1,featurestate=CXC4012505 featureState 1


#Check
st cell

$date = `date +%y%m%d_%H%M`
cvms POST_M.com
gs-
confb-



lt all
rbs
rbs

$date = `date +%y%m%d_%H%M`
confb+

get . additionalUpperLayerIndList
get . primaryUpperLayerInd

set CXC4012371 featurestate 1
set CXC4012381 featurestate 1
set CXC4012504 featurestate 1
set CXC4012218 featurestate 1
set CXC4011559 featurestate 1
set CXC4012324 featurestate 1
set CXC4012385 featurestate 1
set CXC4012503 featurestate 1
set CXC4011967 featurestate 1
set CXC4011251 featurestate 1
set CXC4011163 featurestate 1
set CXC4011063 featurestate 1
set CXC4011345 featurestate 1
set CXC4011815 featurestate 1
set CXC4011477 featurestate 1
set CXC4012480 featurestate 0
set CXC4010620 featurestate 1
set CXC4012578 featurestate 1
set CXC4012015 featurestate 1
set CXC4012095 featurestate 1


set ENodeBFunction=1,EUtranCell.*DD= endcSetupDlPktVolThr 5
set EUtranCell.*DD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 hysteresisA5 10
set UePolicyOptimization=1  endcAwareImc 2

set CarrierAggregationFunction=1 dcSCellActDeactDataThres 30
set CarrierAggregationFunction=1 dcSCellActDeactDataThresHyst 30
set CarrierAggregationFunction=1 dcSCellDeactDelayTimer 200
set CarrierAggregationFunction=1 endcCaPolicy 1
set EUtranCell.DD=.*,UeMeasControl=1 endcMeasRestartTime 10000
set EUtranCell.DD=.*  measGapPattEndc 1
set ENodeBFunction=1   endcS1OverlapMode True
set EUtranCell.DD=.*,UeMeasControl=1 endcMeasTime 2000
set EUtranCell.DD=.*,UeMeasControl=1 endcB1MeasWindow 40
set EUtranCell.DD=.*,UeMeasControl=1 maxMeasB1Endc 3
set ENodeBFunction=1       endcDataUsageReportEnabled true
set ENodeBFunction=1       zzzTemporary81    1
crn ENodeBFunction=1,EndcProfile=2
meNbS1TermReqArpLev 15
splitNotAllowedUeArpLev 0
userLabel
end

set  ENodeBFunction=1,EndcProfile=2  meNbS1TermReqArpLev  15
set  ENodeBFunction=1,EndcProfile=2 splitNotAllowedUeArpLev 0
set QciTable=default,QciProfilePredefined=qci5              endcProfileRef    EndcProfile=2
set QciTable=default,QciProfilePredefined=qci1              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3
set QciTable=default,QciProfilePredefined=qci2              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3



ma cellockqqwer  ^eutrancell administrativeState 0
lbl  cell
ldeb cell
lbl cellockqqwer

#set EUtranCell.DD=.*  primaryUpperLayerInd 0
#set EUtranCell.DD=.*  additionalUpperLayerIndList 0 0 0 0 0
set ^EUtranCell.DD=.* endcAllowedPlmnList mcc=404,mnc=10,mnclength=2
set . anrstateNR 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength 26
set . endcX2IpAddrViaS1Active 1

set EUtranFreqRelation=39150    endcHoFreqPriority -1
set EUtranFreqRelation=39294    endcHoFreqPriority -1
set EUtranFreqRelation=39151    endcHoFreqPriority -1
set EUtranFreqRelation=39295    endcHoFreqPriority -1
set EUtranFreqRelation=1415     endcHoFreqPriority 7
set EUtranFreqRelation=3690    endcHoFreqPriority 6

set EUtranFreqRelation=39150    endcAwareIdleModePriority 5
set EUtranFreqRelation=39294    endcAwareIdleModePriority 5
set EUtranFreqRelation=39151    endcAwareIdleModePriority 7
set EUtranFreqRelation=39295    endcAwareIdleModePriority 7
set EUtranFreqRelation=1415     endcAwareIdleModePriority 6
set EUtranFreqRelation=3690    endcAwareIdleModePriority 4

##need to add small cell arfcn

cr ENodeBFunction=1,UePolicyOptimization=1
set UePolicyOptimization=1      t320              180
set GUtranFreqRelation=    endcB1MeasPriority 7
set ENodeBFunction=1       endcAllowed       true
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= triggerQuantityA5 0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= reportQuantityA5  0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= timeToTriggerA5  100
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold1Rsrp -44
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold1Rsrq -195
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold2Rsrp -113
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold2Rsrq -195
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= hysteresisA5 10

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 triggerQuantityB1 0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp -105
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrq -435

set EUtranCell.DD=.*,GUtranFreqRelation= b1ThrRsrpFreqOffset 0
set EUtranCell.DD=.*,GUtranFreqRelation=         b1ThrRsrqFreqOffset 0
set EUtranCell.DD=.*,GUtranFreqRelation= qOffsetFreq 0

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 hysteresisB1     6
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 timeToTriggerB1  640

set LoadBalancingFunction=1        lbAllowedForEndcUe False
set EUtranCell.DD=                 lbActionForEndcUe 0
set ENodeBFunction=1               endcSplitAllowedMoVoice false

###added SubscriberGroupProfile=ENDC(PA13)
crn ENodeBFunction=1,SubscriberGroupProfile=ENDC
customTriggerType 2
customTriggerList 2
qciOffsetForQCI6 24
qciOffsetForQCI9 22
end


###added Qci30=Qci6 and Qci31=Qci9//set eutranFreqToQciProfileRelation values (PA13)

crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci30
absPrioOverride                      0
aqmMode                              1
bitRateRecommendationEnabled         false
caOffloadingEnabled                  false
counterActiveMode                    false
dataFwdPerQciEnabled                 true
dlMaxHARQTxQci                       5
dlMaxWaitingTime                     0
dlMinBitRate                         2000
dlResourceAllocationStrategy         1
drxPriority                          0
drxProfileRef                        ENodeBFunction=1,DrxProfile=0
dscp                                 26
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
paPartitionOverride                  false
pdb                                  300
pdbOffset                            0
pdcpSNLength                         12
priority                             6
priorityFraction                     0
qci                                  30
qciACTuning                          1000
qciSubscriptionQuanta                200
relativePriority                     2
resourceAllocationStrategy           1
resourceType                         0
rlcMode                              0
rlcSNLength                          10
rlfPriority                          0
rlfProfileRef                        RlfProfile=0
rohcEnabled                          false
rohcForUlDataEnabled                 false
schedulingAlgorithm                  4
serviceType                          0
srsAllocationStrategy                0
tReorderingDl                        35
tReorderingUl                        60
timerPriority                        0
timerProfileRef
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         300
zzzTemporary1                        1
zzzTemporary2
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end

crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci31
absPrioOverride                      0
aqmMode                              1
bitRateRecommendationEnabled         false
caOffloadingEnabled                  false
counterActiveMode                    false
dataFwdPerQciEnabled                 true
dlMaxHARQTxQci                       5
dlMaxWaitingTime                     0
dlMinBitRate                         0
dlResourceAllocationStrategy         1
drxPriority                          0
drxProfileRef                        ENodeBFunction=1,DrxProfile=0
dscp                                 26
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
paPartitionOverride                  false
pdb                                  300
pdbOffset                            0
pdcpSNLength                         12
priority                             9
priorityFraction                     0
qci                                  31
qciACTuning                          1000
qciSubscriptionQuanta                200
relativePriority                     1
resourceAllocationStrategy           1
resourceType                         0
rlcMode                              0
rlcSNLength                          10
rlfPriority                          0
rlfProfileRef                        RlfProfile=0
rohcEnabled                          false
rohcForUlDataEnabled                 false
schedulingAlgorithm                  4
serviceType                          0
srsAllocationStrategy                0
tReorderingDl                        35
tReorderingUl                        35
timerPriority                        0
timerProfileRef
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         0
zzzTemporary1                        1
zzzTemporary2
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end

lt all

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6

mr TABTAB21
ma TABTAB21 ^eutrancell arfcn ^1415
pr TABTAB21
if $nr_of_mos >= 1
for $mo in TABTAB21
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc-6,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
done
fi

mr TABTAB23
ma TABTAB23 ^eutrancelltdd=
pr TABTAB23
if $nr_of_mos >= 1
for $mo in TABTAB23
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415  eutranFreqToQciProfileRelation   qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
done
fi


mr TABTAB09
ma TABTAB09 ^eutrancell earfcn  ^3690$
pr TABTAB09
if $nr_of_mos >= 1
for $mo in TABTAB09
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415  eutranFreqToQciProfileRelation   qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
done
fi

set QciTable=default,QciProfilePredefined=qci6$ relativePriority 2
set QciTable=default,QciProfileOperatorDefined=qci30$ relativePriority 100

cr EnodeBfunction=1,PmFlexCounterFilter=ENDC
set EnodeBfunction=1,PmFlexCounterFilter=ENDC endcFilterEnabled true
set EnodeBFunction=1,PmFlexCounterFilter=ENDC endcFilterMin 2
Set SubscriberGroupProfile=ENDC       profilePriority   5


#############################

gs+

set . qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1

set . eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1

set UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc

rdel ENodeBFunction=1,SubscriberGroupProfile=ENDC

rdel ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30

rdel ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31

#############################

mr TABTAB23
ma TABTAB23 ^eutrancelltdd=
pr TABTAB23
if $nr_of_mos >= 1
for $mo in TABTAB23
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415  eutranFreqToQciProfileRelation  a5Thr2RsrqFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
done
fi

#############################

## CAIMAC Priority Changes CAIMC for ULS earfcn will be highest followed with preferred anchor layer & then other lte layers ###


set UePolicyOptimization zzzTemporary1 1

set EUtranFreqRelation=39150    endcHoFreqPriority -1
set EUtranFreqRelation=39294    endcHoFreqPriority -1
set EUtranFreqRelation=39151    endcHoFreqPriority -1
set EUtranFreqRelation=39295    endcHoFreqPriority -1
set EUtranFreqRelation=1415     endcHoFreqPriority 7
set EUtranFreqRelation=3690    endcHoFreqPriority 6

set EUtranFreqRelation=39150    endcAwareIdleModePriority 5
set EUtranFreqRelation=39294    endcAwareIdleModePriority 5
set EUtranFreqRelation=39151    endcAwareIdleModePriority 7
set EUtranFreqRelation=39295    endcAwareIdleModePriority 7
set EUtranFreqRelation=1415     endcAwareIdleModePriority 6
set EUtranFreqRelation=3690    endcAwareIdleModePriority 4

wait 2

#############################################################

ma cellockqqwer  ^eutrancell administrativeState 0
wait 5
lbl  EUtranCell
wait 10
lt all
wait 10
st EUtranCell
ldeb EUtranCell
wait 20
lt all
ldeb EUtranCell
st EUtranCell
lbl cellockqqwer
wait 20

##################################################

mr BAN_FUPPER
mr BAN_F8PQ
ma BAN_FUPPER ^EUtranCell.*DD primaryUpperLayerInd 1
st BAN_FUPPER

if $nr_of_mos >= 1
ma BAN_F8PQ EUtranCellFDD earfcndl ^1415
ma BAN_F8PQ ^eutrancelltdd=
pr BAN_F8PQ
for $mo in BAN_F8PQ
$mordn = rdn($mo)
set $mordn primaryUpperLayerInd  1
done
fi

get BAN_F8PQ additionalUpperLayerIndList
get BAN_F8PQ primaryUpperLayerInd

################################

set EUtranCell.DD=.*,EUtranFreqRelation=.* anrMeasOn true

################## Twamp addition in anchor nodes #######

crn Transport=1,Router=LTEUP,TwampResponder=NR
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
end

crn Transport=1,Router=NR,TwampResponder=NR
ipAddress Router=NR,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
end

#################################################

$date = `date +%y%m%d_%H%M`
confb-
                                                                                                                                           

"""


DEL_TN_RN_GPS_MME_SCRIPT = """
crn Transport=1,QosProfiles=1,DscpPcpMap=1
defaultPcp 0
pcp0 0 1 2 3 4 5 6 7
pcp1 9 10 11 12 13 14 15
pcp2 16 17 18 19 20 21 22 23
pcp3 24 25 26 27 28 29 30 31
pcp4 32 33 34 35 36 37 38 39
pcp5 40 41 42 43 44 45 46 47
pcp6 48 49 50 51 52 53 54 55
pcp7 56 57 58 59 60 61 62 63
userLabel Traffic
end

#END Transport=1,QosProfiles=1,DscpPcpMap=1 --------------------

set Transport=1,EthernetPort= egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1
set Transport=1,Router=.*,InterfaceIPv4= egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1
set Transport=1,VlanPort= egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=TWAMP                                                                                                     
dst 0.0.0.0/0                                                                                                                                               
end                                                                                                                                                               

crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=TWAMP,NextHop=1                                                                                           
address {LTE_UP_GW}                                                                                                                                               
adminDistance 1                                                                                                                                                   
bfdMonitoring true                                                                                                                                              
discard false                                                                                                                                                     
reference                                                                                                                                                         
end

crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Transport=1,Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
udpPort 4001
userLabel TWAMP1
end
#END Transport=1,Router=LTEUP,TwampResponder=1 --------------------


crn Transport=1,SctpProfile=1
alphaIndex 3
assocMaxRtx 20
betaIndex 2
bundlingActivated true
bundlingTimer 10
cookieLife 60
dscp 46
hbMaxBurst 1
heartbeatInterval 5000
incCookieLife 30
initARWnd 16384
initialHeartbeatInterval 500
initRto 2000
maxActivateThr 65535
maxBurst 4
maxInitRt 8
maxInStreams 2
maxOutStreams 2
maxRto 4000
maxSctpPduSize 1480
maxShutdownRt 5
minActivateThr 1
minRto 1000
pathMaxRtx 4
primaryPathMaxRtx 0
sackTimer 10
transmitBufferSize 64
userLabel SCTP
end

#END Transport=1,SctpProfile=1 --------------------

crn Transport=1,SctpEndpoint=1
localIpAddress Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end
#END Transport=1,SctpEndpoint=1 --------------------

ld Transport=1,Synchronization=1 #SystemCreated
lset Transport=1,Synchronization=1$ fixedPosition true
lset Transport=1,Synchronization=1$ telecomStandard 1

crn Transport=1,Synchronization=1,RadioEquipmentClock=1
minQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1 --------------------

crn Transport=1,Synchronization=1,TimeSyncIO=1
encapsulation Equipment=1,FieldReplaceableUnit=4,SyncPort=1
end
#END Transport=1,Synchronization=1,TimeSyncIO=1 --------------------

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Transport=1,Synchronization=1,TimeSyncIO=1
priority 1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1 --------------------

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=2
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Transport=1,Ntp=1,NtpFrequencySync=NTP1
priority 2
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=2 --------------------

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=3
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Transport=1,Ntp=1,NtpFrequencySync=NTP2
priority 3
end


crn ENodeBFunction=1
eNodeBPlmnId mcc=404,mnc=10,mncLength=2
dscpLabel 46
eNBId {eNBId}
sctpRef Transport=1,SctpEndpoint=1
timeAndPhaseSynchAlignment true
upIpAddressRef Transport=1,Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
x2GtpuEchoDscp 14
end
#END ENodeBFunction=1 --------------------

ld ENodeBFunction=1,Paging=1 #SystemCreated
lset ENodeBFunction=1,Paging=1$ maxNoOfPagingRecords 7

ld ENodeBFunction=1,AdmissionControl=1 #SystemCreated
lset ENodeBFunction=1,AdmissionControl=1$ dlAdmDifferentiationThr 750
lset ENodeBFunction=1,AdmissionControl=1$ ulAdmDifferentiationThr 750

ld ENodeBFunction=1,AnrFunction=1 #SystemCreated
lset ENodeBFunction=1,AnrFunction=1$ maxNoPciReportsEvent 30
lset ENodeBFunction=1,AnrFunction=1$ maxTimeEventBasedPciConf 30
lset ENodeBFunction=1,AnrFunction=1$ removeNrelTime 7

ld ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 #SystemCreated
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrInterFreqState 1
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrIntraFreqState 1
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrUesEUtraIntraFMax 0
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrUesEUtraIntraFMin 0
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrUesThreshInterFMax 0
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrUesThreshInterFMin 0
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ cellAddRsrpThresholdEutran -1150

ld ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 #SystemCreated
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1$ anrStateGsm 1

ld ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 #SystemCreated
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1$ anrStateUtran 1
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1$ cellAddEcNoThresholdUtranDelta 0
lset ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1$ cellAddRscpThresholdUtranDelta 0

ld ENodeBFunction=1,DrxProfile=1 #SystemCreated
lset ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 3
lset ENodeBFunction=1,DrxProfile=1$ drxRetransmissionTimer 2
lset ENodeBFunction=1,DrxProfile=1$ longDrxCycle 3
lset ENodeBFunction=1,DrxProfile=1$ longDrxCycleOnly 3
lset ENodeBFunction=1,DrxProfile=1$ onDurationTimer 6
lset ENodeBFunction=1,DrxProfile=1$ shortDrxCycle 7
lset ENodeBFunction=1,DrxProfile=1$ shortDrxCycleTimer 0

ld ENodeBFunction=1,DrxProfile=2 #SystemCreated
lset ENodeBFunction=1,DrxProfile=2$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=2$ drxRetransmissionTimer 1
lset ENodeBFunction=1,DrxProfile=2$ longDrxCycle 3
lset ENodeBFunction=1,DrxProfile=2$ longDrxCycleOnly 3
lset ENodeBFunction=1,DrxProfile=2$ onDurationTimer 2
lset ENodeBFunction=1,DrxProfile=2$ shortDrxCycle 7
lset ENodeBFunction=1,DrxProfile=2$ shortDrxCycleTimer 0

ld ENodeBFunction=1,DrxProfile=0 #SystemCreated
lset ENodeBFunction=1,DrxProfile=0$ drxInactivityTimer 14
lset ENodeBFunction=1,DrxProfile=0$ drxRetransmissionTimer 4
lset ENodeBFunction=1,DrxProfile=0$ longDrxCycle 9
lset ENodeBFunction=1,DrxProfile=0$ longDrxCycleOnly 3
lset ENodeBFunction=1,DrxProfile=0$ onDurationTimer 7
lset ENodeBFunction=1,DrxProfile=0$ shortDrxCycle 9
lset ENodeBFunction=1,DrxProfile=0$ shortDrxCycleTimer 1

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ schedulingAlgorithm 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ schedulingAlgorithm 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ schedulingAlgorithm 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ schedulingAlgorithm 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dscp 46
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ schedulingAlgorithm 0

lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ schedulingAlgorithm 0


lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ schedulingAlgorithm 0


lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ schedulingAlgorithm 0


lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dscp 26
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ schedulingAlgorithm 0

lset ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ dlMaxRetxThreshold 16
lset ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ ulMaxRetxThreshold 16

ld ENodeBFunction=1,Rcs=1 #SystemCreated
lset ENodeBFunction=1,Rcs=1$ tInactivityTimer 10

ld ENodeBFunction=1,Rrc=1 #SystemCreated
lset ENodeBFunction=1,Rrc=1$ t300 2000
lset ENodeBFunction=1,Rrc=1$ t301 1000
lset ENodeBFunction=1,Rrc=1$ t311 3000


crn ENodeBFunction=1,GeraNetwork=1
end
#END ENodeBFunction=1,GeraNetwork=1 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
frequencyGroupId 1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1 --------------------

crn ENodeBFunction=1,EUtraNetwork=1
end

set 0 Userlabel {Phy_SiteID_Userlabel}

confb-
gs-

#######################MME############################################


get Transport=1,Router=LTECP,RouteTableIPv4Static= routeTableIPv4StaticId > $MME_ROUTE                                                                       
                                                                                                                                                             
get Transport=1,Router=LTEUP,RouteTableIPv4Static= routeTableIPv4StaticId > $SGW_ROUTE                                                                       
                                                                                                                                                             
get Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=.*,NextHop= address$ > $X2CP_Nexthop                                                        
                                                                                                                                                             
get Transport=1,Router=LTEUP,RouteTableIPv4Static=$SGW_ROUTE,Dst=.*,NextHop= address$ > $X2UP_Nexthop                                                        
           


get Transport=1,Router=LTECP,RouteTableIPv4Static= routeTableIPv4StaticId > $MME_ROUTE                                                                       
get Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=.*,NextHop= address$ > $X2CP_Nexthop                                                        
         


##MME10                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME10-Pri                                                                                    
10.103.44.12/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME10-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME10-Sec                                                                                    
10.103.44.13/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME10-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME10                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME10 ipAddress1 10.103.44.12                                                                                            
set ENodeBFunction=1,TermPointToMme=MME10 ipAddress2 10.103.44.13                                                                                            
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME10                                                                                                                   
y                                                                                                                                                            
##MME11                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME11-Pri                                                                                    
10.103.44.23/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME11-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME11-Sec                                                                                    
10.103.44.24/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME11-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME11                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME11 ipAddress1 10.103.44.23                                                                                            
set ENodeBFunction=1,TermPointToMme=MME11 ipAddress2 10.103.44.24                                                                                            
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME11                                                                                                                   
y                                                                                                                                                            
                                                                                                                                                             
##MME12                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME12-Pri                                                                                    
10.103.44.1/32                                                                                                                                               
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME12-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME12-Sec                                                                                    
10.103.44.2/32                                                                                                                                               
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME12-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME12                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME12 ipAddress1 10.103.44.1                                                                                             
set ENodeBFunction=1,TermPointToMme=MME12 ipAddress2 10.103.44.2                                                                                             
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME12                                                                                                                   
y                                                                                                                                                            
                                                                                                                                                             
##MME13                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME13-Pri                                                                                    
10.103.44.34/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME13-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME13-Sec                                                                                    
10.103.44.35/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME13-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME13                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME13 ipAddress1 10.103.44.34                                                                                            
set ENodeBFunction=1,TermPointToMme=MME13 ipAddress2 10.103.44.35                                                                                            
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME13                                                                                                                   
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
##MME14                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME14-Pri                                                                                    
10.103.10.42/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME14-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME14-Sec                                                                                    
10.103.10.44/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME14-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME14                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME14 ipAddress1 10.103.10.42                                                                                            
set ENodeBFunction=1,TermPointToMme=MME14 ipAddress2 10.103.10.44                                                                                            
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME14                                                                                                                   
y                                                                                                                                                            
                                                                                                                                                             
                                                                                                                                                             
##MME15                                                                                                                                                      
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME15-Pri                                                                                    
10.103.10.32/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME15-Pri,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME15-Sec                                                                                    
10.103.10.34/32                                                                                                                                              
cr Transport=1,Router=LTECP,RouteTableIPv4Static=$MME_ROUTE,Dst=MME15-sec,NextHop=1                                                                          
$X2CP_Nexthop                                                                                                                                                
false                                                                                                                                                        
                                                                                                                                                             
1                                                                                                                                                            
true                                                                                                                                                         
                                                                                                                                                             
cr ENodeBFunction=1,TermPointToMme=MME15                                                                                                                     
set ENodeBFunction=1,TermPointToMme=MME15 ipAddress1 10.103.10.32                                                                                            
set ENodeBFunction=1,TermPointToMme=MME15 ipAddress2 10.103.10.34                                                                                            
y                                                                                                                                                            
ldeb ENodeBFunction=1,TermPointToMme=MME15                                                                                                                   
y                                                                                                                                                            
                                                                                                                                                             


"""




################################################################################### 5G SCRIPS FOR INTEGRATION SCRIPTS ###################################################################################
DEL_5G_Cell_creation_Sctp_Endpoint_Creation = """
######################################################## IPV6 Interface for NR ####################################################################

cr Transport=1,Router=LTEUP,InterfaceIPv6=NR
VlanPort=TN_E_UP
false

crn Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
address {NR_IP}
configurationMode 0
duidType 0
primaryAddress true
userLabel
end


crn Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
address {NR_ENDC_IP}
configurationMode 0
duidType 0
primaryAddress false
userLabel
end

gs+

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=2                                                                                                              
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=2,Dst=default                                                                                                   
dst ::/0                                                                                                                                                          
end



crn Transport=1,Router=LTEUP,RouteTableIPv6Static=2,Dst=default,NextHop=1
address {NR_GW}
adminDistance 1
bfdMonitoring true
discard false
reference
end


##################################################################################### TN SCRIPT #########################################################################

crn Transport=1,QosProfiles=1,DscpPcpMap=1
defaultPcp 0
pcp0 0 1 2 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 36 37 38 39 41 43 45 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
pcp1
pcp2 22 24 26
pcp3 6 8 10 30 32
pcp4 12 14 40
pcp5 4 28
pcp6 16 18 34 42 44
pcp7 20 46
userLabel Traffic
end


crn Transport=1,Router=LTEUP,TwampResponder=2
ipAddress Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
udpPort 4001
userLabel
end

crn Transport=1,Router=LTEUP,TwampResponder=3
ipAddress Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
udpPort 4002
userLabel
end

crn Transport=1,Router=LTEUP,TwampResponder=NR
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
userLabel
end

crn Transport=1,SctpProfile=1
alphaIndex 3
assocMaxRtx 8
betaIndex 2
bundlingActivated true
bundlingTimer 0
cookieLife 60
dscp 46
hbMaxBurst 1
heartbeatInterval 5000
incCookieLife 30
initARWnd 16384
initialHeartbeatInterval 500
initRto 2000
maxActivateThr 65535
maxBurst 4
maxInitRt 5
maxInStreams 2
maxOutStreams 2
maxRto 4000
maxSctpPduSize 1480
maxShutdownRt 5
minActivateThr 1
minRto 1000
pathMaxRtx 4
primaryPathMaxRtx 0
sackTimer 100
transmitBufferSize 64
userLabel SCTP
end

crn Transport=1,SctpEndpoint=1
localIpAddress Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end

crn Transport=1,SctpEndpoint=X2_ENDC
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end

##########

crn Transport=1,SctpProfile=Node_Internal_F1
alphaIndex 3
assocMaxRtx 8
betaIndex 2
bundlingActivated true
bundlingAdaptiveActivated true
bundlingTimer 0
cookieLife 60
dscp 46
hbMaxBurst 1
heartbeatActivated true
heartbeatInterval 2000
incCookieLife 30
initARWnd 16384
initialHeartbeatInterval 500
initRto 2000
maxActivateThr 65535
maxBurst 4
maxInitRt 5
maxInStreams 2
maxOutStreams 2
maxRto 4000
maxSctpPduSize 1480
maxShutdownRt 5
minActivateThr 1
minRto 1000
noSwitchback true
pathMaxRtx 4
primaryPathAvoidance true
primaryPathMaxRtx 0
sackTimer 100
thrTransmitBuffer 48
thrTransmitBufferCongCeased 85
transmitBufferSize 64
end

cr Transport=1,Router=Node_Internal_F1

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP
aclEgress
aclIngress
arpTimeout 300
bfdProfile
bfdStaticRoutes 0
egressQosMarking
encapsulation
ingressQosMarking
ipOptionsDisabled false
loopback true
mtu 1500
pcpArp 6
routesHoldDownTimer
routingPolicyIngress
trackedInterface
userLabel
end

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP,AddressIPv4=1
address 10.0.0.1/32
configurationMode 0
dhcpClientIdentifier
dhcpClientIdentifierType 0
primaryAddress true
userLabel
end
gs-

crn Transport=1,SctpEndpoint=F1_NRCUCP
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end

############

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU
aclEgress
aclIngress
arpTimeout 300
bfdProfile
bfdStaticRoutes 0
egressQosMarking
encapsulation
ingressQosMarking
ipOptionsDisabled false
loopback true
mtu 1500
pcpArp 6
routesHoldDownTimer
routingPolicyIngress
trackedInterface
userLabel
end

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU,AddressIPv4=1
address 10.0.0.2/32
configurationMode 0
dhcpClientIdentifier
dhcpClientIdentifierType 0
primaryAddress true
userLabel
end
gs-

crn Transport=1,SctpEndpoint=F1_NRDU
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end

###########

crn Transport=1,SctpEndpoint=NG
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 38412
sctpProfile Transport=1,SctpProfile=1
end

crn Transport=1,SctpEndpoint=X2
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end

crn Transport=1,SctpEndpoint=F1
dtls
dtlsNodeCredential
dtlsSctpSecurityMode 0
dtlsTrustCategory
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 38472
sctpProfile SctpProfile=1
userLabel
end

gs+                                                                                                                                                          
crn Transport=1,SctpEndpoint=F1_NRCUCP                                                                                                                       
dtls                                                                                                                                                         
dtlsNodeCredential                                                                                                                                           
dtlsSctpSecurityMode 0                                                                                                                                       
dtlsTrustCategory                                                                                                                                            
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP,AddressIPv4=1                                                                       
portNumber 38472                                                                                                                                             
sctpProfile SctpProfile=Node_Internal_F1                                                                                                                     
userLabel                                                                                                                                                    
end  


###########################################GNBCUUPFunction=1#############################################################################

crn GNBCUUPFunction=1
gNBId {gNBId}
gNBIdLength 26
pLMNIdList mcc=404,mnc=10
sNSSAIList
userLabel
end

crn GNBCUUPFunction=1,EndpointResource=1
end

crn GNBCUUPFunction=1,EndpointResource=1,LocalIpEndpoint=1
addressRef Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
interfaceList 4 5 7 6
end


ld GNBCUUPFunction=1
lset GNBCUUPFunction=1$ endpointResourceRef GNBCUUPFunction=1,EndpointResource=1



crn GNBCUUPFunction=1,CardinalityLimits=1
maxNgUPath 600
maxS1UPath 600
end

crn GNBCUUPFunction=1,GtpuSupervision=1
gtpuErrorIndDscp 40
end

crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=S1
endpointResourceRef
gtpuEchoDscp 32
gtpuEchoEnabled true
interfaceList 5
userLabel
end

crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=X2
endpointResourceRef
gtpuEchoDscp 32
gtpuEchoEnabled true
interfaceList 7
userLabel
end


####################################GNBDUFunction=1###################################

crn GNBDUFunction=1
gNBDUId 1
gNBDUName
gNBId {gNBId}
gNBIdLength 26
end

crn GNBDUFunction=1,EndpointResource=1
end

crn GNBDUFunction=1,EndpointResource=1,LocalSctpEndpoint=1
interfaceUsed 3
sctpEndpointRef Transport=1,SctpEndpoint=F1_NRDU
end

crn GNBDUFunction=1,TermPointToGNBCUCP=1
administrativeState 1
ipv4Address 10.0.0.1
ipv6Address ::
end

ld GNBDUFunction=1
lset GNBDUFunction=1$ endpointResourceRef GNBDUFunction=1,EndpointResource=1


crn GNBDUFunction=1,MassiveMimoSleep=1                                                                                                                                                                             
end 

crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepProfile=1                                                                                                                                                         
sleepMode 0                                                                                                                                                                                                        
switchDownMonitorDurTimer 60                                                                                                                                                                                       
switchDownMonitorDurTimerEco 300                                                                                                                                                                                   
switchDownPrbThreshDl 10                                                                                                                                                                                           
switchDownPrbThreshDlEco 15                                                                                                                                                                                        
switchDownPrbThreshUlEco 10                                                                                                                                                                                        
switchDownRrcConnThresh 10                                                                                                                                                                                         
switchDownRrcConnThreshEco 30                                                                                                                                                                                      
switchUpMonitorDurTimer 30                                                                                                                                                                                         
switchUpMonitorDurTimerEco 120                                                                                                                                                                                     
switchUpPrbThreshDl 20                                                                                                                                                                                             
switchUpPrbThreshDlEco 30                                                                                                                                                                                          
switchUpPrbThreshUlEco 15                                                                                                                                                                                          
switchUpRrcConnThresh 20                                                                                                                                                                                           
switchUpRrcConnThreshEco 50                                                                                                                                                                                        
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1                                                                                                                                                       
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1,MMimoSleepTimeWindow=1                                                                                                                                
dayOfWeek 0                                                                                                                                                                                                        
mMimoSleepProfileRef MassiveMimoSleep=1,MMimoSleepProfile=1                                                                                                                                                        
startTime 20:30                                                                                                                                                                                                    
stopTime 23:30                                                                                                                                                                                                     
end    


{DEL_CGSWITCH_SCRIPT}

############################GNBCUCPFunction=1####################################################


crn GNBCUCPFunction=1
gNBId {gNBId}
gNBIdLength 26
pLMNId mcc=404,mnc=10
end

crn GNBCUCPFunction=1,EndpointResource=1
end

ld GNBCUCPFunction=1
lset GNBCUCPFunction=1$ endpointResourceRef GNBCUCPFunction=1,EndpointResource=1

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=1
interfaceUsed 4
sctpEndpointRef SctpEndpoint=NG
end

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=2
interfaceUsed 7
sctpEndpointRef SctpEndpoint=X2
end

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=3
interfaceUsed 3
sctpEndpointRef SctpEndpoint=F1_NRCUCP
end

                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,AnrFunction=1                                                                                                                                                                                
demoteCellRelMobAttThresh                                                                                                                                                                                          
promoteCellRelMobAttThresh                                                                                                                                                                                         
removeEUtranFreqRelTime 10000                                                                                                                                                                                      
removeEnbTime 7                                                                                                                                                                                                    
removeFreqRelTime 15                                                                                                                                                                                               
removeGnbTime 7                                                                                                                                                                                                    
removeNrelTime 7                                                                                                                                                                                                   
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1                                                                                                                                                                
anrAutoCreateXnForEndc false                                                                                                                                                                                       
anrCgiMeasInterFreqMode 0                                                                                                                                                                                          
anrCgiMeasIntraFreqEnabled true                                                                                                                                                                                    
anrEndcX2Enabled true                                                                                                                                                                                              
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1,AnrFunctionNRUeCfg=Base                                                                                                                                        
anrRsrpThreshold -156                                                                                                                                                                                              
anrRsrqThreshold -435                                                                                                                                                                                              
anrSinrThreshold -230                                                                                                                                                                                              
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   

crn GNBCUCPFunction=1,CarrierAggregation=1                                                                                                                                                                         
end                                                                                                                                                                                                                
                                       
crn GNBCUCPFunction=1,CarrierAggregation=1,CaCellMeasProfile=1                                                                                                                                                     
ueConfGroupType 0                                                                                                                                                                                                  
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,CarrierAggregation=1,CaCellMeasProfile=1,CaCellMeasProfileUeCfg=Base                                                                                                                         
betterSCellReportConfigMode 0                                                                                                                                                                                      
prefUeGroupList                                                                                                                                                                                                    
rsrpBetterSCell hysteresis=10,offset=30,timeToTrigger=160                                                                                                                                                          
rsrpSCellCoverage hysteresis=10,threshold=-117,timeToTrigger=160,timeToTriggerA1=-1                                                                                                                                
rsrqSCellCoverage hysteresis=10,threshold=-435,timeToTrigger=160,timeToTriggerA1=-1                                                                                                                                
sCellCoverageTriggerQuantity 0                                                                                                                                                                                     
ueConfGroupList                                                                                                                                                                                                    
ueGroupList                                                                                                                                                                                                        
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                            

crn GNBCUCPFunction=1,IntraFreqMC=1                                                                                                                                                                                
sCellDepHEnabled true                                                                                                                                                                                              
end                                                                                                                                                                                                                
                                                   
crn GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1                                                                                                                                                       
ueConfGroupType 0                                                                                                                                                                                                  
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base                                                                                                                      
betterSpCellTriggerQuantity 0                                                                                                                                                                                      
endcActionEvalFail 1                                                                                                                                                                                               
prefUeGroupList                                                                                                                                                                                                    
rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640                                                                                                                                                         
rsrqBetterSpCell hysteresis=10,offset=30,timeToTrigger=640                                                                                                                                                         
sinrBetterSpCell hysteresis=10,offset=30,timeToTrigger=640                                                                                                                                                         
ueConfGroupList                                                                                                                                                                                                    
ueGroupList                                                                                                                                                                                                        
useT312BetterPCellCandidateA3 false                                                                                                                                                                                
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                


crn GNBCUCPFunction=1,NRNetwork=1
end

crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30
arfcnValueNRDl 629952
bandListManual
smtcDuration 1
smtcOffset 0
smtcPeriodicity 20
smtcScs 30
ssRssiMeasIdle
ssbToMeasureIdle
end

crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30,NRFrequencyUeCfg=Base
prefUeGroupList
ssRssiMeasConnected
ssbToMeasureConnected
ueConfGroupList
ueGroupList
userLabel
end

crn GNBCUCPFunction=1,UeGroupSelection=1                                                                                                                                                                           
validityTimeEmergencyCause 6                                                                                                                                                                                       
validityTimeHighPrioAccCause 6                                                                                                                                                                                     
validityTimeMcsPrioAccCause 6                                                                                                                                                                                      
validityTimeMoDataCause 6                                                                                                                                                                                          
validityTimeMoSignallingCause 6                                                                                                                                                                                    
validityTimeMoSmsCause 6                                                                                                                                                                                           
validityTimeMoVideoCallCause 6                                                                                                                                                                                     
validityTimeMoVoiceCallCause 6                                                                                                                                                                                     
validityTimeMpsPrioAccCause 6                                                                                                                                                                                      
validityTimeMtAccessCause 6                                                                                                                                                                                        
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,ImeiSvGroups=1                                                                                                                                                            
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,PrefUeGroupSelectionProfile=QCI6                                                                                                                                          
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
prefUeGroupId 6                                                                                                                                                                                                    
prefUeGroupPriority 65534                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,PrefUeGroupSelectionProfile=QCI7                                                                                                                                          
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
prefUeGroupId 7                                                                                                                                                                                                    
prefUeGroupPriority 1000                                                                                                                                                                                           
selectionCriteria qci==7                                                                                                                                                                                           
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeGroupSelectionProfile=QCI6                                                                                                                                              
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
selectionProbability 100                                                                                                                                                                                           
ueGroupId 6                                                                                                                                                                                                        
ueGroupPriority 65534                                                                                                                                                                                              
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeGroupSelectionProfile=QCI7                                                                                                                                              
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==7                                                                                                                                                                                           
selectionProbability 100                                                                                                                                                                                           
ueGroupId 7                                                                                                                                                                                                        
ueGroupPriority 1000                                                                                                                                                                                               
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeMobilityGroupDefinition=QCI6                                                                                                                                            
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
ueMobilityGroupId 6                                                                                                                                                                                                
ueMobilityGroupPriority 65534                                                                                                                                                                                      
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeMobilityGroupDefinition=QCI7                                                                                                                                            
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==7                                                                                                                                                                                           
ueMobilityGroupId 7                                                                                                                                                                                                
ueMobilityGroupPriority 1000                                                                                                                                                                                       
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeServiceGroupDefinition=QCI6                                                                                                                                             
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
ueServiceGroupId 6                                                                                                                                                                                                 
ueServiceGroupPriority 65534                                                                                                                                                                                       
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeServiceGroupDefinition=QCI7                                                                                                                                             
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==7                                                                                                                                                                                           
ueServiceGroupId 7                                                                                                                                                                                                 
ueServiceGroupPriority 1000                                                                                                                                                                                        
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                

{DEL_GNBCUCPFunction}

crn GNBCUCPFunction=1,EUtraNetwork=1
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=1511
arfcnValueEUtranDl 1511
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=1526
arfcnValueEUtranDl 1526
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=240
arfcnValueEUtranDl 240
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=265
arfcnValueEUtranDl 265
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=3663
arfcnValueEUtranDl 3663
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39150
arfcnValueEUtranDl 39150
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39294
arfcnValueEUtranDl 39294
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39348
arfcnValueEUtranDl 39348
userLabel
end

{DEL_GNBDUFunction}

"""

DEL_Termpoint_GUtranFreqRelation_script = """


###########################Termpoint & FreqRelation################################



cvms bfranchor

#####1. Transport=1,Router=LTEUP,InterfaceIPv6=NR--Change TN Port as per configured in BBU

get Router=LTEUP,InterfaceIPv4=TN_._UP                      encapsulation  > $encapsulation

$reqipX2 = readinput( ipv6 IP for X2 ENDC )
$reqhopadd = readinput( ipv6 nexthop )

get Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR usedAddress > $reqipNR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
get GNBDUFunction=1 gNBId$ > $gnbid


gs+

crn Transport=1,Router=LTEUP,InterfaceIPv6=NR
aclEgress
aclIngress
bfdProfile
bfdStaticRoutes 0
dscpNdp 48
egressQosMarking
encapsulation $encapsulation
ingressQosMarking
loopback false
mtu 1500
neighborDiscoveryTimeout 30000
neighborSolicitationInterval 1000
routesHoldDownTimer
trackedInterface
userLabel
end


#####2. Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2/NR ---- Change IP address as per planning


crn Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
address $reqipX2 ###need to change ENDC IP according to plan in AD column###
configurationMode 0
duidType 0
primaryAddress true
userLabel
end	
gs-

#######3. Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default,NextHop=1/NR--Change Nexthop address as per planning

gs+

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1                                                                                                               
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default                                                                                                   
dst ::/0                                                                                                                                                          
end


crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default,NextHop=1
address $reqhopadd ###need to change ENDC gateway according to plan in AA column###
adminDistance 1
bfdMonitoring true
discard false
reference
end
gs-

#########4. Transport=1,SctpEndpoint=X2_ENDC/NR 


gs+

crn Transport=1,SctpEndpoint=X2_ENDC
dtls
dtlsNodeCredential
dtlsSctpSecurityMode 0
dtlsTrustCategory
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
portNumber 36422
sctpProfile SctpProfile=1
userLabel
end

set ENodeBFunction=1$  endcAllowed  true                                                                                                                 
set ENodeBFunction=1$  sctpEndcX2Ref Transport=1,SctpEndpoint=X2_ENDC                                                                                        
set ENodeBFunction=1$  upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                     
set ENodeBFunction=1$  intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                  
set ^EUtranCell.DD= endcAllowedPlmnList mcc=404,mnc=10,mnclength=2                                                                                                

crn ENodeBFunction=1,EndcProfile=1                                                                                                                                
end

set ENodeBFunction=1,EndcProfile=1 meNbS1TermReqArpLev 0                                                                                                          
set ENodeBFunction=1,EndcProfile=1 splitNotAllowedUeArpLev 0 
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6789]$ endcProfileRef ENodeBFunction=1,EndcProfile=1

cr ENodeBFunction=1,UePolicyOptimization=1                                                                                                                        
set ENodeBFunction=1,UePolicyOptimization=1 ueCapPrioList 0                                                                                                       
set ENodeBFunction=1,UePolicyOptimization=1 coverageAwareImc true                                                                                                 
set ENodeBFunction=1  endcX2IpAddrViaS1Active  true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR= gNodebIdLength 26                                                                                               
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1 anrStateNR 1 



################*Parameter Setting Required:

set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1  anrStateNR        1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1  anrFunctionNRId   1
set ENodeBFunction=1$   endcAllowed       true
set ENodeBFunction=1$  intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
set ENodeBFunction=1$  upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2

set  CXC4012095   featureState 1
set  CXC4012504   featurestate 1
set  CXC4012381   featurestate 1
set  CXC4012385   featurestate 1 
set  CXC4040006   featurestate 1                                                                                                                                   

set EUtranCellFDD=DL_.*,EUtranFreqRelation=240 endcHoFreqPriority 6
set EUtranCellFDD=DL_.*,EUtranFreqRelation=1511 endcHoFreqPriority 7
set EUtranCellFDD=DL_.*,EUtranFreqRelation=3663 endcAwareIdleModePriority 3
set EUtranCellTDD=DL_.*,EUtranFreqRelation=39150 endcAwareIdleModePriority 5
set EUtranCellTDD=DL_.*,EUtranFreqRelation=39151 endcAwareIdleModePriority 7
set EUtranCellTDD=DL_.*,EUtranFreqRelation=39348 endcAwareIdleModePriority 5
set EUtranCellTDD=DL_.*,EUtranFreqRelation=39349 endcAwareIdleModePriority 7             

get Router=*.*,RouteTableIPv6Static=.*,Dst=default,NextHop= address > $gwip                                                                                          
mcc Router=*.*,InterfaceIPv6=NR,AddressIPv6=X2 ping6 $gwip -c 4



#############################################5. ENodeBFunction=1,GUtraNetwork=1###########################################

gs+

cr ENodeBFunction=1,GUtraNetwork=1


#############################################6. ENodeBFunction=1,GUtraNetwork=1###########################################

gs+                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40410-$gnbid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
dirDataPathAvail true                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
eNBVlanPortRef                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
gNodeBId $gnbid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
gNodeBIdLength 26                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
gNodeBPlmnId mcc=404,mnc=10,mncLength=2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
userLabel                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
end   

crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40410-$gnbid,TermPointToGNB=40410-$gnbid                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
additionalCnRef                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
administrativeState 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
domainName                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
ipAddress 0.0.0.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
ipAddress2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
ipsecEpAddress ::                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
ipv6Address $reqipNR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
ipv6Address2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
upIpAddress ::                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
end    

########################7. ENodeBFunction=1,GUtraNetwork=1,GUtranSyncSignalFrequency=######################################

crn ENodeBFunction=1,GUtraNetwork=1,GUtranSyncSignalFrequency=629952-30
arfcn 629952
smtcScs 30
userLabel
end
gs-



lt all


get GNBDUFunction=1,NRCellDU= celllocalid > $CLID

mr CWA_CRP_2
ma CWA_CRP_2 EUtranCell.DD=.*,EUtranFreqRelation= cellReselectionPriority 2
lpr CWA_CRP_2

set CWA_CRP_2 cellReselectionPriority 4


ma L21_12_21 ^EUtranCell.DD                                                                                                                                       

for $mo in L21_12_21                                                                                                                                              
$mordn = rdn($mo)                                                                                                                                                 
pr ENodeBFunction=1,$mordn,GUtranFreqRelation=629952                                                                                                              
if $nr_of_mos = 0                                                                                                                                                 
cr ENodeBFunction=1,$mordn,GUtranFreqRelation=629952                                                                                                              
GUtraNetwork=1,GUtranSyncSignalFrequency=629952-30                                                                                                       
fi                                                                                                                                                                
done                                                                                                                                                              


func Relation_121L21                                                                                                                                              
for $j = 1 to 5                                                                                                                                                   
pr GUtraNetwork=1,ExternalGNodeBFunction=40410-$gnbid,ExternalGUtranCell=40410-000000$gnbid-31$j                                                                  
if $nr_of_mos = 1                                                                                                                                                 
crn ENodeBFunction=1,$mordn,GUtranFreqRelation=629952,GUtranCellRelation=40410-000000$gnbid-31$j                                                                  
essEnabled false                                                                                                                                                  
isRemoveAllowed false                                                                                                                                             
neighborCellRef GUtraNetwork=1,ExternalGNodeBFunction=40410-$gnbid,ExternalGUtranCell=40410-000000$gnbid-31$j                                                     
userLabel                                                                                                                                                         
end                                                                                                                                                               
fi                                                                                                                                                                
done                                                                                                                                                              
endfunc                                                                                                                                                           



func Relation_121L2_18L                                                                                                                                           
for $mo in L21_12_21                                                                                                                                              
$mordn = rdn($mo)                                                                                                                                                 
Relation_121L21                                                                                                                                                   
done                                                                                                                                                              
endfunc                                                                                                                                                           

Relation_121L2_18L        


set EUtranCell.DD=.*,GUtranFreqRelation=629952 cellReselectionPriority 5
set CWA_CRP_2 cellReselectionPriority 2

set ENodeBFunction=1$  endcAllowed  true                                                                                                                 
set ENodeBFunction=1$  sctpEndcX2Ref Transport=1,SctpEndpoint=X2_ENDC                                                                                        
set ENodeBFunction=1$  upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                     
set ENodeBFunction=1$  intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                  
set ^EUtranCell.DD= endcAllowedPlmnList mcc=404,mnc=10,mnclength=2                                                                                                

"""


DEL_NR_GPL_LMS_SCRIPT = """


confb+

crn NodeSupport=1,ServiceDiscovery=1
localAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
nodeCredential
primaryGsds host=localhost,hostIPs=,port=8301,serviceArea=NR_NSA
secondaryGsds
trustCategory SecM=1,CertM=1,TrustCategory=1
end

crn NodeSupport=1,ServiceDiscovery=1
localAddress Transport=1,Router=NR,InterfaceIPv6=NR,AddressIPv6=NR
nodeCredential
primaryGsds host=localhost,hostIPs=,port=8301,serviceArea=NR_NSA
secondaryGsds
trustCategory SecM=1,CertM=1,TrustCategory=1
end

set NodeSupport=1,ServiceDiscovery=1 trustCategory SecM=1,CertM=1,TrustCategory=1


bl nrcell


get nrcelldu ssbFrequency$
set NRCellDU=.* ssbFrequency 629952







lt all
rbs
rbs

confb+

$date = `date +%y%m%d_%H%M`

lbl NRCellDU=.*
lbl NRSectorCarrier=

set CXC4012500 FeatureState 1
set CXC4012273 featurestate 1
set CXC4012375 featurestate 1
set CXC4012549 featurestate 1
set CXC4012492 featurestate 1
set CXC4012534 featurestate 1
set CXC4012347 featurestate 1
set CXC4012325 featurestate 1
set CXC4012493 featurestate 1
set CXC4012558 featurestate 1
set CXC4012272 featurestate 1
set CXC4012502 featurestate 1
set CXC4012347 featurestate 1
set CXC4012510 FeatureState 1
set CXC4012587 FeatureState 1
set CXC4010319 featureState 1
set CXC4010320 featureState 1
set CXC4010609 featureState 1
set CXC4010613 featureState 1
set CXC4010616 featureState 1
set CXC4010618 featureState 1
set CXC4010620 featureState 1
set CXC4010717 featureState 1
set CXC4010723 featureState 1
set CXC4010770 featureState 1
set CXC4010841 featureState 1
set CXC4010856 featureState 1
set CXC4010912 featureState 1
set CXC4010949 featureState 1
set CXC4010956 featureState 1
set CXC4010959 featureState 1
set CXC4010961 featureState 1
set CXC4010962 featureState 1
set CXC4010963 featureState 1
set CXC4010964 featureState 1
set CXC4010967 featureState 1
set CXC4010973 featureState 1
set CXC4010974 featureState 1
set CXC4010980 featureState 1
set CXC4010990 featureState 1
set CXC4011011 featureState 1
set CXC4011018 featureState 1
set CXC4011033 featureState 1
set CXC4011034 featureState 1
set CXC4011050 featureState 1
set CXC4011056 featureState 1
set CXC4011057 featureState 1
set CXC4011059 featureState 1
set CXC4011060 featureState 1
set CXC4011061 featureState 1
set CXC4011062 featureState 1
set CXC4011063 featureState 1
set CXC4011064 featureState 1
set CXC4011067 featureState 1
set CXC4011068 featureState 1
set CXC4011069 featureState 1
set CXC4011072 featureState 1
set CXC4011074 featureState 1
set CXC4011075 featureState 1
set CXC4011155 featureState 1
set CXC4011157 featureState 1
set CXC4011163 featureState 1
set CXC4011183 featureState 1
set CXC4011245 featureState 1
set CXC4011247 featureState 1
set CXC4011251 featureState 1
set CXC4011252 featureState 1
set CXC4011253 featureState 1
set CXC4011255 featureState 1
set CXC4011256 featureState 1
set CXC4011258 featureState 1
set CXC4011317 featureState 1
set CXC4011319 featureState 1
set CXC4011327 featureState 1
set CXC4011345 featureState 1
set CXC4011346 featureState 1
set CXC4011356 featureState 1
set CXC4011366 featureState 1
set CXC4011370 featureState 1
set CXC4011372 featureState 1
set CXC4011373 featureState 1
set CXC4011376 featureState 1
set CXC4011378 featureState 1
set CXC4011422 featureState 1
set CXC4011427 featureState 1
set CXC4011443 featureState 1
set CXC4011444 featureState 1
set CXC4011476 featureState 1
set CXC4011477 featureState 1
set CXC4011479 featureState 1
set CXC4011481 featureState 1
set CXC4011482 featureState 1
set CXC4011485 featureState 1
set CXC4011515 featureState 1
set CXC4011557 featureState 1
set CXC4011559 featureState 1
set CXC4011618 featureState 1
set CXC4011666 featureState 1
set CXC4011667 featureState 1
set CXC4011698 featureState 1
set CXC4011699 featureState 1
set CXC4011710 featureState 1
set CXC4011711 featureState 1
set CXC4011715 featureState 1
set CXC4011716 featureState 1
set CXC4011804 featureState 1
set CXC4011807 featureState 1
set CXC4011808 featureState 1
set CXC4011811 featureState 1
set CXC4011813 featureState 1
set CXC4011814 featureState 1
set CXC4011815 featureState 1
set CXC4011820 featureState 1
set CXC4011823 featureState 1
set CXC4011910 featureState 1
set CXC4011914 featureState 1
set CXC4011917 featureState 1
set CXC4011918 featureState 1
set CXC4011922 featureState 1
set CXC4011930 featureState 1
set CXC4011933 featureState 1
set CXC4011937 featureState 1
set CXC4011938 featureState 1
set CXC4011939 featureState 1
set CXC4011940 featureState 1
set CXC4011941 featureState 1
set CXC4011942 featureState 1
set CXC4011946 featureState 1
set CXC4011951 featureState 1
set CXC4011958 featureState 1
set CXC4011967 featureState 1
set CXC4011969 featureState 1
set CXC4011973 featureState 1
set CXC4011974 featureState 1
set CXC4011975 featureState 1
set CXC4011982 featureState 1
set CXC4011983 featureState 1
set CXC4011991 featureState 1
set CXC4012003 featureState 1
set CXC4012015 featureState 1
set CXC4012018 featureState 1
set CXC4012022 featureState 1
set CXC4012036 featureState 1
set CXC4012070 featureState 1
set CXC4012089 featureState 1
set CXC4012097 featureState 1
set CXC4012111 featureState 1
set CXC4012123 featureState 1
set CXC4012129 featureState 1
set CXC4012199 featureState 1
set CXC4012218 featureState 1
set CXC4012238 featureState 1
set CXC4012240 featureState 1
set CXC4012256 featureState 1
set CXC4012259 featureState 1
set CXC4012260 featureState 1
set CXC4012261 featureState 1
set CXC4012271 featureState 1
set CXC4012272 featureState 1
set CXC4012273 featureState 1
set CXC4012316 featureState 1
set CXC4012324 featureState 1
set CXC4012325 featureState 1
set CXC4012326 featureState 1
set CXC4012347 featureState 1
set CXC4012349 featureState 1
set CXC4012356 featureState 1
set CXC4012371 featureState 1
set CXC4012374 featureState 1
set CXC4012375 featureState 1
set CXC4012381 featureState 1
set CXC4012385 featureState 1
set CXC4012480 featureState 0
set CXC4012485 featureState 1
set CXC4012492 featureState 1
set CXC4012493 featureState 1
set CXC4012500 featureState 1
set CXC4012502 featureState 1
set CXC4012503 featureState 1
set CXC4012504 featureState 1
set CXC4012505 featureState 1
set CXC4012510 featureState 1
set CXC4012534 featureState 1
set CXC4012549 featureState 1
set CXC4012558 featureState 1
set CXC4012578 featureState 1
set CXC4012587 featureState 1
set CXC4040004 featureState 1
set CXC4040005 featureState 1
set CXC4040006 featureState 1
set CXC4040008 featureState 1
set CXC4040009 featureState 1
set CXC4040010 featureState 1
set CXC4040014 featureState 1
set CXC4012590 FeatureState 1
set CXC4012562 FeatureState 1
set CXC4012330 FeatureState 1
set CXC4012373 FeatureState 1
set CXC4012406 FeatureState 1
set CXC4012589 FeatureState 1
set CXC4012547 FeatureState 0


///common_Parameters_32t_8t
set NRSectorCarrier=.*,CommonBeamforming=1               cbfMacroTaperType 0
set CUUP5qi=6$  estimatedE2ERTT 50
set CUUP5qi=8$  estimatedE2ERTT 50
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1  tPollRetransmitUl 80
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 tStatusProhibitUl 10
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxInactivityTimer 15
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxLongCycle      10
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base  drxOnDurationTimer  39
set GNBCUUPFunction=1          dcDlPdcpInitialScgRate 100

set NRCellDU=.* tddSpecialSlotPattern 3
set NRCellDU=.* tddUlDlPattern 1
set NRCellDU=.* rachPreambleFormat 0
set NRCellDU=.* cellRange 5000
set NRCellDU=.* csiRsShiftingPrimary 1
set NRCellDU=.* csiRsShiftingSecondary 1
set NRCellDU=.* dl256QamEnabled true
set NRCellDU=.* drxProfileEnabled true
set NRCellDU=.* maxUeSpeed 2
set NRCellDU=.* pdschStartPrbStrategy 3
set NRCellDU=.* puschStartPrbStrategy 3
set NRCellDU=.* pZeroNomPucch -114
set NRCellDU=.* secondaryCellOnly False
set NRCellDU=.* ssbDuration 1
set NRCellDU=.* ssbOffset 0
set NRCellDU=.* ssbPeriodicity 20
set NRCellDU=.* ssbSubCarrierSpacing 30
set NRCellDU=.* subCarrierSpacing 30
set NRCellDU=.* trsPeriodicity 20
set NRCellDU=.* trsPowerBoosting 0
set NRCellDU=.* ul256QamEnabled true
set NRCellDU=.* rachPreambleRecTargetPower -110
set NRCellDU=.* rachPreambleTransMax 10
Set NRCellDU=.* maxUsersRachSchedPusch 100
set NRCellDU=.* pZeroNomPuschGrant -102
set NRCellDU=.* csiRsPeriodicity 40
set NRCellDU=.* additionalPucchForCaEnabled FALSE
set NRSectorCarrier=.* configuredMaxTxPower    200000
set NRCellDU=.*  maxNoOfAdvancedDlMuMimoLayers 8

#lkf required with dmrs feature for bm
set NRCellDU=.* pdschAllowedInDmrsSym TRUE
set NRCellDU=.* puschAllowedInDmrsSym TRUE

set QciProfileEndcConfigExt=1   initialUplinkConf 1
set GNBCUCPFunction=1,UeCC=1,InactivityProfile=Default,InactivityProfileUeCfg=Base tInactivityTimerEndcSn 5
set NRSectorCarrier= nRMicroSleepTxEnabled true
set NRSectorCarrier=.*,CommonBeamforming=1  coverageShape 1
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1    tPollRetransmitDl 80
set AnrFunctionNR anrCgiMeasInterFreqMode 1
set AnrFunctionNR anrCgiMeasIntraFreqEnabled TRUE
set AnrFunctionNR anrEndcX2Enabled TRUE
set AnrFunction removeGnbTime 7
set AnrFunction removeNrelTime 7
set GNBDUFunction=1,Rrc=1 n310 20
set GNBDUFunction=1,Rrc=1 n311 1
set GNBDUFunction=1,Rrc=1 t300 1500
set GNBDUFunction=1,Rrc=1 t301 600
set GNBDUFunction=1,Rrc=1 t304 2000
set GNBDUFunction=1,Rrc=1 t310 2000
set GNBDUFunction=1,Rrc=1 t311 3000
set GNBDUFunction=1,Rrc=1 t319 400

set GNBCUUPFunction=1    endcDataUsageReportEnabled true
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingUeMode 1
set . anrstateNR 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength 26
set . endcX2IpAddrViaS1Active 1

set NRCellDU=.* csiRsConfig4P csiRsControl4Ports=0,i11Restriction=
set NRCellDU=.* csiRsConfig8P  csiRsControl8Ports=1,i11Restriction=FFFF,i12Restriction=
set NRCellDU=.* csiRsConfig32P csiRsControl32Ports=EIGHT_TWO_N1AZ,i11Restriction=FFFFFFFF,i12Restriction=FF
set NRCellDU=.* ssbPowerBoost 6
set NRCellDU=.* advancedDlSuMimoEnabled TRUE
set NRCellDU=.* pZeroNomSrs -110
set NRCellDU=.* srsPeriodicity 40
set NRCellDU=.* dlMaxMuMimoLayers 8
set NRCellDU=.* ulMaxMuMimoLayers 4
set NRCellDU=.* pZeroUePuschOffset256Qam 4
set .  cbfMacroTaperType 0
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1         anrAutoCreateXnForEndc True

set . endcDlNrRetProhibTimer 400
set . endcDlNrQualHyst 3
set . initialUplinkConf SCG
set . endcUlNrRetProhibTimer 1000
set . dcDlAggActTime 1
set . dcDlAggExpiryTimer 100
set . ulDataSplitThreshold

set NRCellRelation= isHoAllowed true
set NRCellDU=.* endcDlLegSwitchEnabled true
set NRCellDU=.* endcDlNrLowQualThresh 0
set NRCellDU=.* endcUlLegSwitchEnabled true
set NRCellDU=.* endcUlNrLowQualThresh 10
set NRCellDU=.* endcUlNrQualHyst 6
set NRCellCU=.* mcpcPSCellEnabled true

cr GNBCUCPFunction=1,IntraFreqMC=1
cr GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1

set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base betterSpCellTriggerQuantity 0
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640


set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpSCellCoverage hysteresis=10,threshold=-117
set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpBetterSCell offset=30,hysteresis=10
set Mcpc=1,McpcPSCellProfile=.*,McpcPSCellProfileUeCfg=Base  rsrpCriticalEnabled true
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpSearchZone threshold=-112,hysteresis=10,timeToTriggerA1=160
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCandidateA5 threshold1=-118,threshold2=-112,hysteresis=10,timeToTrigger=640
set Mcpc=1,McpcPSCellNrFreqRelProfile=Default,McpcPSCellNrFreqRelProfileUeCfg=Base rsrpCandidateA5Offsets threshold1Offset=0,threshold2Offset=0
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical threshold=-110,timeToTrigger=256,hysteresis=20
set QciProfileEndcConfigExt=1  ulDataSplitThresholdMcg -1

set ENodeBFunction=1 dlBbCapacityTarget 300

wait 5

set NRCellDU=.* drxProfileRef GNBDUFunction=1,UeCC=1,DrxProfile=Default
set . mcpcPSCellProfileRef GNBCUCPFunction=1,Mcpc=1,McpcPSCellProfile=Default

##################################3

cvms pre_Twamp_NR

set SystemFunctions=1,Lm=1,FeatureState=CXC4040009 featureState 1
gs+

crn Transport=1,Router=NR,TwampResponder=NR
ipAddress Router=NR,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
userLabel
end

crn Transport=1,Router=LTEUP,TwampResponder=NR
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
userLabel
end

###################

set NRCellDU=.*  maxNoOfAdvancedDlMuMimoLayers 8
set PmEventService=1     cellTraceFileSize 30000

###########################

gs+
crn Transport=1,Synchronization=1,TimeSyncIO=1,GnssInfo=1
end
gs-

########  QOS ####################

cvms Pre_QOS_NR_$date
set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction=1 interEnbCaTunnelDscp 26
set ENodeBFunction=1 interEnbUlCompTunnelDscp 26
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2GtpuEchoDscp 46

cr Transport=1,QosProfiles=1,DscpPcpMap=1
set QciTable=default,QciProfilePredefined=qci1$ dscp 34
set QciTable=default,QciProfilePredefined=qci2$ dscp 34
set QciTable=default,QciProfilePredefined=qci3$ dscp 26
set QciTable=default,QciProfilePredefined=qci4$ dscp 26
set QciTable=default,QciProfilePredefined=qci5$ dscp 46
set QciTable=default,QciProfilePredefined=qci6$ dscp 32
set QciTable=default,QciProfilePredefined=qci7$ dscp 40
set QciTable=default,QciProfilePredefined=qci8$ dscp 30
set QciTable=default,QciProfilePredefined=qci9$ dscp 26
set SysM=1,OamTrafficClass=1 dscp 28
set SctpProfile= dscp 46
set Ntp=1,NtpFrequencySync= dscp 46

set QosProfiles=1,DscpPcpMap=1 pcp0
set QosProfiles=1,DscpPcpMap=1 pcp1
set QosProfiles=1,DscpPcpMap=1 pcp2
set QosProfiles=1,DscpPcpMap=1 pcp3
set QosProfiles=1,DscpPcpMap=1 pcp4
set QosProfiles=1,DscpPcpMap=1 pcp5
set QosProfiles=1,DscpPcpMap=1 pcp6
set QosProfiles=1,DscpPcpMap=1 pcp7

lset Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22,24,26
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6,8,10,30,32
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12,14,40
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4,28
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16,18,34,42,44
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20,46
set SctpProfile=Node_Internal_F1  dscp 46
set SctpProfile=1 dscp 46
set Router=.*,DnsClient=1 dscp 28

set . egressQosMarking QosProfiles=1,DscpPcpMap=1

######### Del Data_3 ######

rdel Equipment=1,FieldReplaceableUnit=AAS-S.*_N1,RiPort=DATA_3
y

################  Digital tilt for 3219 A #############

get NRSectorCarrier=S1_N11,CommonBeamforming=1  ^digitalTilt > $1st-sec-tilt
get NRSectorCarrier=S2_N11,CommonBeamforming=1  ^digitalTilt > $2nd-sec-tilt
get NRSectorCarrier=S3_N11,CommonBeamforming=1  ^digitalTilt > $3rd-sec-tilt

hget field prod@name 3219
for $mo in hget_group
$mordn = rdn($mo)
cr Equipment=1,$mordn,AntennaNearUnit=1
cr Equipment=1,$mordn,AntennaNearUnit=1,RetSubUnit=1
set Equipment=1,$mordn,Transceiver=1 retSubUnitRef $mordn,AntennaNearUnit=1,RetSubUnit=1
set FieldReplaceableUnit=AAS-S1_N1,AntennaNearUnit=1,RetSubUnit=1 electricalAntennaTilt $1st-sec-tilt
set FieldReplaceableUnit=AAS-S2_N1,AntennaNearUnit=1,RetSubUnit=1 electricalAntennaTilt $2nd-sec-tilt
set FieldReplaceableUnit=AAS-S3_N1,AntennaNearUnit=1,RetSubUnit=1 electricalAntennaTilt $3rd-sec-tilt
done

wait 3
lt all

accn hget_group restartunit 1 0 0

######################   SCTP profile for 5G    ########################

confd+
set Transport=1,SctpProfile=Node_Internal_F1 alphaIndex 3
set Transport=1,SctpProfile=Node_Internal_F1 assocMaxRtx 8
set Transport=1,SctpProfile=Node_Internal_F1 betaIndex 2
set Transport=1,SctpProfile=Node_Internal_F1 bundlingActivated TRUE
set Transport=1,SctpProfile=Node_Internal_F1 bundlingAdaptiveActivated TRUE
set Transport=1,SctpProfile=Node_Internal_F1 bundlingTimer 0
set Transport=1,SctpProfile=Node_Internal_F1 cookieLife 60
set Transport=1,SctpProfile=Node_Internal_F1 dscp 46
set Transport=1,SctpProfile=Node_Internal_F1 hbMaxBurst 1
set Transport=1,SctpProfile=Node_Internal_F1 heartbeatActivated TRUE
set Transport=1,SctpProfile=Node_Internal_F1 heartbeatInterval 2000
set Transport=1,SctpProfile=Node_Internal_F1 incCookieLife 30
set Transport=1,SctpProfile=Node_Internal_F1 initARWnd 16384
set Transport=1,SctpProfile=Node_Internal_F1 maxRto 4000
set Transport=1,SctpProfile=Node_Internal_F1 initRto 2000
set Transport=1,SctpProfile=Node_Internal_F1 minRto 1000
set Transport=1,SctpProfile=Node_Internal_F1 initialHeartbeatInterval 500
set Transport=1,SctpProfile=Node_Internal_F1 maxActivateThr 65535
set Transport=1,SctpProfile=Node_Internal_F1 maxBurst 4
set Transport=1,SctpProfile=Node_Internal_F1 maxInStreams 2
set Transport=1,SctpProfile=Node_Internal_F1 maxInitRt 5
set Transport=1,SctpProfile=Node_Internal_F1 maxOutStreams 2
set Transport=1,SctpProfile=Node_Internal_F1 maxSctpPduSize 1480
set Transport=1,SctpProfile=Node_Internal_F1 maxShutdownRt 5
set Transport=1,SctpProfile=Node_Internal_F1 minActivateThr 1
set Transport=1,SctpProfile=Node_Internal_F1 noSwitchback TRUE
set Transport=1,SctpProfile=Node_Internal_F1 pathMaxRtx 4
set Transport=1,SctpProfile=Node_Internal_F1 primaryPathAvoidance TRUE
set Transport=1,SctpProfile=Node_Internal_F1 primaryPathMaxRtx 0
set Transport=1,SctpProfile=Node_Internal_F1 sackTimer 100
set Transport=1,SctpProfile=Node_Internal_F1 thrTransmitBuffer 48
set Transport=1,SctpProfile=Node_Internal_F1 thrTransmitBufferCongCeased 85
set Transport=1,SctpProfile=Node_Internal_F1 transmitBufferSize 64
set Transport=1,SctpProfile=Node_Internal_F1 userLabel SCTP
set Transport=1,SctpProfile=1 alphaIndex 3
set Transport=1,SctpProfile=1 assocMaxRtx 8
set Transport=1,SctpProfile=1 betaIndex 2
set Transport=1,SctpProfile=1 bundlingActivated TRUE
set Transport=1,SctpProfile=1 bundlingAdaptiveActivated TRUE
set Transport=1,SctpProfile=1 bundlingTimer 0
set Transport=1,SctpProfile=1 cookieLife 60
set Transport=1,SctpProfile=1 dscp 46
set Transport=1,SctpProfile=1 hbMaxBurst 1
set Transport=1,SctpProfile=1 heartbeatActivated TRUE
set Transport=1,SctpProfile=1 heartbeatInterval 2000
set Transport=1,SctpProfile=1 incCookieLife 30
set Transport=1,SctpProfile=1 initARWnd 16384
set Transport=1,SctpProfile=1 maxRto 4000
set Transport=1,SctpProfile=1 initRto 2000
set Transport=1,SctpProfile=1 minRto 1000
set Transport=1,SctpProfile=1 initialHeartbeatInterval 500
set Transport=1,SctpProfile=1 maxActivateThr 65535
set Transport=1,SctpProfile=1 maxBurst 4
set Transport=1,SctpProfile=1 maxInStreams 2
set Transport=1,SctpProfile=1 maxInitRt 5
set Transport=1,SctpProfile=1 maxOutStreams 2
set Transport=1,SctpProfile=1 maxSctpPduSize 1480
set Transport=1,SctpProfile=1 maxShutdownRt 5
set Transport=1,SctpProfile=1 minActivateThr 1
set Transport=1,SctpProfile=1 noSwitchback TRUE
set Transport=1,SctpProfile=1 pathMaxRtx 4
set Transport=1,SctpProfile=1 primaryPathAvoidance TRUE
set Transport=1,SctpProfile=1 primaryPathMaxRtx 0
set Transport=1,SctpProfile=1 sackTimer 100
set Transport=1,SctpProfile=1 thrTransmitBuffer 48
set Transport=1,SctpProfile=1 thrTransmitBufferCongCeased 85
set Transport=1,SctpProfile=1 transmitBufferSize 64
set Transport=1,SctpProfile=1 userLabel SCTP

############# 5G GTP ##################################

set GtpuSupervision=1,GtpuSupervisionProfile=S1 gtpuEchoEnabled true
set GtpuSupervision=1,GtpuSupervisionProfile=X2 gtpuEchoEnabled true

set GtpuSupervision=1,GtpuSupervisionProfile=S1 gtpuEchoDscp 32
set GtpuSupervision=1,GtpuSupervisionProfile=X2 gtpuEchoDscp 32

set Transport=1,SctpProfile=Node_Internal_F1 pathMaxRtx 4
set Transport=1,SctpProfile=1 pathMaxRtx 4
set Transport=1,SctpProfile=Node_Internal_F1 assocMaxRtx 8
set Transport=1,SctpProfile=1 assocMaxRtx 8

######### PDCCH Beamforming

set CXC4012589 featurestate 1
set NRCellDU pdcchLaSinrOffset -20

set EUtranCell.DD=.*,EUtranFreqRelation=.* anrMeasOn true
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxEnabled        true

##### System Constant

scw RP136:20
scw RP137:20
scw RP138:20
scw RP139:20

#### Pmax #####

set NRCellDU pMax 26

##### DLMAX RETX #####

set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 dlMaxRetxThreshold 32
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 dlMaxRetxThreshold 32
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 ulMaxRetxThreshold 32
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 ulMaxRetxThreshold 32
set Mcfb=1,McfbCellProfile=1,McfbCellProfileUeCfg=Base      epsFallbackOperation 2

#### DFTS OFDM #####

set CXC4012373 featurestate 1
set NRCellDU dftSOfdmMsg3Enabled TRUE
set NRCellDU dftSOfdmPuschEnabled TRUE

##### endcActionEvalFail #####

set IntraFreqMCCellProfileUeCfg endcActionEvalFail 1

############# 2nd script from mail ##################

### advanced DL SUMIMO ###

set CXC4012510 featurestate 1
set NRCellDU advancedDlSuMimoEnabled TRUE
set NRCellDU nrSrsDlBufferVolThr 100
set NRCellDU nrSrsDlPacketAgeThr 0
set NRCellDU pZeroNomSrs -110
set NRCellDU srsPeriodicity 40
set NRCellDU srsHoppingBandwidth 0

###  tDcOverall ###

set GNBCUCPFunction tDcOverall 11

###  uldatasplitthreshold ###

set QciProfileEndcConfigExt uldatasplitthresholdmcg -1

set QciProfileEndcConfigExt uldatasplitthreshold 102400

#################################

set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitDl 80
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitUl 80

###################################

ldeb  NRSectorCarrier=
ldeb  NRCellDU=.*

#####################################

#######################################

$date = `date +%y%m%d_%H%M`
confb-


lt all
rbs
rbs

$date = `date +%y%m%d_%H%M`
confb+

get . additionalUpperLayerIndList
get . primaryUpperLayerInd

set CXC4012371 featurestate 1
set CXC4012381 featurestate 1
set CXC4012504 featurestate 1
set CXC4012218 featurestate 1
set CXC4011559 featurestate 1
set CXC4012324 featurestate 1
set CXC4012385 featurestate 1
set CXC4012503 featurestate 1
set CXC4011967 featurestate 1
set CXC4011251 featurestate 1
set CXC4011163 featurestate 1
set CXC4011063 featurestate 1
set CXC4011345 featurestate 1
set CXC4011815 featurestate 1
set CXC4011477 featurestate 1
set CXC4012480 featurestate 0
set CXC4010620 featurestate 1
set CXC4012578 featurestate 1
set CXC4012015 featurestate 1
set CXC4012095 featurestate 1


set ENodeBFunction=1,EUtranCell.*DD= endcSetupDlPktVolThr 5
set EUtranCell.*DD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 hysteresisA5 10
set UePolicyOptimization=1  endcAwareImc 2

set CarrierAggregationFunction=1 dcSCellActDeactDataThres 30
set CarrierAggregationFunction=1 dcSCellActDeactDataThresHyst 30
set CarrierAggregationFunction=1 dcSCellDeactDelayTimer 200
set CarrierAggregationFunction=1 endcCaPolicy 1
set EUtranCell.DD=.*,UeMeasControl=1 endcMeasRestartTime 10000
set EUtranCell.DD=.*  measGapPattEndc 1
set ENodeBFunction=1   endcS1OverlapMode True
set EUtranCell.DD=.*,UeMeasControl=1 endcMeasTime 2000
set EUtranCell.DD=.*,UeMeasControl=1 endcB1MeasWindow 40
set EUtranCell.DD=.*,UeMeasControl=1 maxMeasB1Endc 3
set ENodeBFunction=1       endcDataUsageReportEnabled true
set ENodeBFunction=1       zzzTemporary81    1
crn ENodeBFunction=1,EndcProfile=2
meNbS1TermReqArpLev 15
splitNotAllowedUeArpLev 0
userLabel
end

set  ENodeBFunction=1,EndcProfile=2  meNbS1TermReqArpLev  15
set  ENodeBFunction=1,EndcProfile=2 splitNotAllowedUeArpLev 0
set QciTable=default,QciProfilePredefined=qci5              endcProfileRef    EndcProfile=2
set QciTable=default,QciProfilePredefined=qci1              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3
set QciTable=default,QciProfilePredefined=qci2              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3



ma cellockqqwer  ^eutrancell administrativeState 0
lbl  cell
ldeb cell
lbl cellockqqwer

#set EUtranCell.DD=.*  primaryUpperLayerInd 0
#set EUtranCell.DD=.*  additionalUpperLayerIndList 0 0 0 0 0
set ^EUtranCell.DD=.* endcAllowedPlmnList mcc=404,mnc=49,mnclength=2
set . anrstateNR 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength 26
set . endcX2IpAddrViaS1Active 1

set EUtranFreqRelation=39150    endcHoFreqPriority -1
set EUtranFreqRelation=39294    endcHoFreqPriority -1
set EUtranFreqRelation=39151    endcHoFreqPriority -1
set EUtranFreqRelation=39295    endcHoFreqPriority -1
set EUtranFreqRelation=1415     endcHoFreqPriority 7
set EUtranFreqRelation=3690    endcHoFreqPriority 6

set EUtranFreqRelation=39150    endcAwareIdleModePriority 5
set EUtranFreqRelation=39294    endcAwareIdleModePriority 5
set EUtranFreqRelation=39151    endcAwareIdleModePriority 7
set EUtranFreqRelation=39295    endcAwareIdleModePriority 7
set EUtranFreqRelation=1415     endcAwareIdleModePriority 6
set EUtranFreqRelation=3690    endcAwareIdleModePriority 4

##need to add small cell arfcn

cr ENodeBFunction=1,UePolicyOptimization=1
set UePolicyOptimization=1      t320              180
set GUtranFreqRelation=    endcB1MeasPriority 7
set ENodeBFunction=1       endcAllowed       true
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= triggerQuantityA5 0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= reportQuantityA5  0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= timeToTriggerA5  100
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold1Rsrp -44
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold1Rsrq -195
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold2Rsrp -113
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold2Rsrq -195
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= hysteresisA5 10

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 triggerQuantityB1 0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp -105
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrq -435

set EUtranCell.DD=.*,GUtranFreqRelation= b1ThrRsrpFreqOffset 0
set EUtranCell.DD=.*,GUtranFreqRelation=         b1ThrRsrqFreqOffset 0
set EUtranCell.DD=.*,GUtranFreqRelation= qOffsetFreq 0

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 hysteresisB1     6
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 timeToTriggerB1  640

set LoadBalancingFunction=1        lbAllowedForEndcUe False
set EUtranCell.DD=                 lbActionForEndcUe 0
set ENodeBFunction=1               endcSplitAllowedMoVoice false

###added SubscriberGroupProfile=ENDC(PA13)
crn ENodeBFunction=1,SubscriberGroupProfile=ENDC
customTriggerType 2
customTriggerList 2
qciOffsetForQCI6 24
qciOffsetForQCI9 22
end


###added Qci30=Qci6 and Qci31=Qci9//set eutranFreqToQciProfileRelation values (PA13)

crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci30
absPrioOverride                      0
aqmMode                              1
bitRateRecommendationEnabled         false
caOffloadingEnabled                  false
counterActiveMode                    false
dataFwdPerQciEnabled                 true
dlMaxHARQTxQci                       5
dlMaxWaitingTime                     0
dlMinBitRate                         2000
dlResourceAllocationStrategy         1
drxPriority                          0
drxProfileRef                        ENodeBFunction=1,DrxProfile=0
dscp                                 26
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
paPartitionOverride                  false
pdb                                  300
pdbOffset                            0
pdcpSNLength                         12
priority                             6
priorityFraction                     0
qci                                  30
qciACTuning                          1000
qciSubscriptionQuanta                200
relativePriority                     2
resourceAllocationStrategy           1
resourceType                         0
rlcMode                              0
rlcSNLength                          10
rlfPriority                          0
rlfProfileRef                        RlfProfile=0
rohcEnabled                          false
rohcForUlDataEnabled                 false
schedulingAlgorithm                  4
serviceType                          0
srsAllocationStrategy                0
tReorderingDl                        35
tReorderingUl                        60
timerPriority                        0
timerProfileRef
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         300
zzzTemporary1                        1
zzzTemporary2
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end

crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci31
absPrioOverride                      0
aqmMode                              1
bitRateRecommendationEnabled         false
caOffloadingEnabled                  false
counterActiveMode                    false
dataFwdPerQciEnabled                 true
dlMaxHARQTxQci                       5
dlMaxWaitingTime                     0
dlMinBitRate                         0
dlResourceAllocationStrategy         1
drxPriority                          0
drxProfileRef                        ENodeBFunction=1,DrxProfile=0
dscp                                 26
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
paPartitionOverride                  false
pdb                                  300
pdbOffset                            0
pdcpSNLength                         12
priority                             9
priorityFraction                     0
qci                                  31
qciACTuning                          1000
qciSubscriptionQuanta                200
relativePriority                     1
resourceAllocationStrategy           1
resourceType                         0
rlcMode                              0
rlcSNLength                          10
rlfPriority                          0
rlfProfileRef                        RlfProfile=0
rohcEnabled                          false
rohcForUlDataEnabled                 false
schedulingAlgorithm                  4
serviceType                          0
srsAllocationStrategy                0
tReorderingDl                        35
tReorderingUl                        35
timerPriority                        0
timerProfileRef
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         0
zzzTemporary1                        1
zzzTemporary2
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end

lt all

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6

mr TABTAB21
ma TABTAB21 ^eutrancell arfcn ^1415
pr TABTAB21
if $nr_of_mos >= 1
for $mo in TABTAB21
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc-6,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
done
fi

mr TABTAB23
ma TABTAB23 ^eutrancelltdd=
pr TABTAB23
if $nr_of_mos >= 1
for $mo in TABTAB23
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415  eutranFreqToQciProfileRelation   qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
done
fi


mr TABTAB09
ma TABTAB09 ^eutrancell earfcn  ^3690$
pr TABTAB09
if $nr_of_mos >= 1
for $mo in TABTAB09
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415  eutranFreqToQciProfileRelation   qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
done
fi

set QciTable=default,QciProfilePredefined=qci6$ relativePriority 2
set QciTable=default,QciProfileOperatorDefined=qci30$ relativePriority 100

cr EnodeBfunction=1,PmFlexCounterFilter=ENDC
set EnodeBfunction=1,PmFlexCounterFilter=ENDC endcFilterEnabled true
set EnodeBFunction=1,PmFlexCounterFilter=ENDC endcFilterMin 2
Set SubscriberGroupProfile=ENDC       profilePriority   5


#############################

gs+

set . qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1

set . eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1

set UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc

rdel ENodeBFunction=1,SubscriberGroupProfile=ENDC

rdel ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30

rdel ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31

#############################

mr TABTAB23
ma TABTAB23 ^eutrancelltdd=
pr TABTAB23
if $nr_of_mos >= 1
for $mo in TABTAB23
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415  eutranFreqToQciProfileRelation  a5Thr2RsrqFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
done
fi

#############################

## CAIMAC Priority Changes CAIMC for ULS earfcn will be highest followed with preferred anchor layer & then other lte layers ###


set UePolicyOptimization zzzTemporary1 1

set EUtranFreqRelation=39150    endcHoFreqPriority -1
set EUtranFreqRelation=39294    endcHoFreqPriority -1
set EUtranFreqRelation=39151    endcHoFreqPriority -1
set EUtranFreqRelation=39295    endcHoFreqPriority -1
set EUtranFreqRelation=1415     endcHoFreqPriority 7
set EUtranFreqRelation=3690    endcHoFreqPriority 6

set EUtranFreqRelation=39150    endcAwareIdleModePriority 5
set EUtranFreqRelation=39294    endcAwareIdleModePriority 5
set EUtranFreqRelation=39151    endcAwareIdleModePriority 7
set EUtranFreqRelation=39295    endcAwareIdleModePriority 7
set EUtranFreqRelation=1415     endcAwareIdleModePriority 6
set EUtranFreqRelation=3690    endcAwareIdleModePriority 4

wait 2

#############################################################

ma cellockqqwer  ^eutrancell administrativeState 0
wait 5
lbl  EUtranCell
wait 10
lt all
wait 10
st EUtranCell
ldeb EUtranCell
wait 20
lt all
ldeb EUtranCell
st EUtranCell
lbl cellockqqwer
wait 20

##################################################

mr BAN_FUPPER
mr BAN_F8PQ
ma BAN_FUPPER ^EUtranCell.*DD primaryUpperLayerInd 1
st BAN_FUPPER

if $nr_of_mos >= 1
ma BAN_F8PQ EUtranCellFDD earfcndl ^1415
ma BAN_F8PQ ^eutrancelltdd=
pr BAN_F8PQ
for $mo in BAN_F8PQ
$mordn = rdn($mo)
set $mordn primaryUpperLayerInd  1
done
fi

get BAN_F8PQ additionalUpperLayerIndList
get BAN_F8PQ primaryUpperLayerInd

################################

set EUtranCell.DD=.*,EUtranFreqRelation=.* anrMeasOn true

################## Twamp addition in anchor nodes #######

crn Transport=1,Router=LTEUP,TwampResponder=NR
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
end

crn Transport=1,Router=NR,TwampResponder=NR
ipAddress Router=NR,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
end


"""


DEL_GNBCUCPFunction=""" 
########################################################################### Cell Specific Started -- NRCellCU={gUtranCell}##################################################

crn GNBCUCPFunction=1,NRCellCU={gUtranCell}
admissionLimitRef GNBCUCPFunction=1,AdmissionControl=1,AdmissionLimit=Default
admissionPriorityRef GNBCUCPFunction=1,AdmissionControl=1,AdmissionPriority=Default
advUePosMode 0
caCellMeasProfileRef CarrierAggregation=1,CaCellMeasProfile=Default
caCellProfileRef CarrierAggregation=1,CaCellProfile=Default
cellLocalId {cellLocalId}
checkUeGrpAtCellOffload false
hiPrioDetEnabled false
interfaceSupervision 0
intraFreqMCCellProfileRef IntraFreqMC=1,IntraFreqMCCellProfile=Default
mcfbCellProfileRef Mcfb=1,McfbCellProfile=Default
mcpcNrdcPSCellEnabled false
mcpcNrdcPSCellProfileRef
mcpcPCellEnabled false
mcpcPCellProfileRef Mcpc=1,McpcPCellProfile=Default
mcpcPSCellEnabled false
mcpcPSCellProfileRef Mcpc=1,McpcPSCellProfile=Default
mdtCellProfileRef Mdt=1,MdtCellProfile=Default
mdtEnabled false
nCellChangeHigh
nCellChangeMedium
nRFrequencyRef NRNetwork=1,NRFrequency=629952-30
noOfPeriodicUeMeasPerRop 900
nrdcMnCellProfileRef NrdcControl=1,NrdcMnCellProfile=Default
offloadCellProfileRef TrafficOffload=1,OffloadCellProfile=Default
periodicCellProfileRef
pmUeIntraFreqCellProfileRef
pmUeIntraFreqEnabled false
primaryPLMNId mcc=404,mnc=10
pwsEmergencyAreaIdList
qHyst 4
qHystSfHigh
qHystSfMedium
resourceStatusMaxConnUe -2
sNonIntraSearchP 0
sNonIntraSearchQ
tEvaluation
tHystNormal
threshServingLowP 0
threshServingLowQ
trStPSCellProfileRef TrafficSteering=1,TrStPSCellProfile=Default
trStSaCellProfileRef TrafficSteering=1,TrStSaCellProfile=Default
transmitSib2 false
transmitSib4 false
transmitSib5 false
transmitSib9 false
uacProfileRef GNBCUCPFunction=1,AdmissionControl=1,Uac=1,UacProfile=Default
ucmCellProfileRef UeCovMeas=1,UcmCellProfile=Default
ueMCCellProfileRef UeMC=1,UeMCCellProfile=Default
userLabel {gUtranCell}
end

crn GNBCUCPFunction=1,NRCellCU={gUtranCell},DESManagementFunction=1
desSwitch false
esNotAllowedTimePeriod
intraRatEsActivationOriginalCellLoadParameters threshold=10,timeDuration=900
periodicEsDuration 120
requiredWakeUpTime 180
end

crn GNBCUCPFunction=1,NRCellCU={gUtranCell},NRFreqRelation=629952
anrMeasOn true
caFreqRelMeasProfileRef CarrierAggregation=1,CaFreqRelMeasProfile=Default
cellReselectionPriority 7
cellReselectionSubPriority
mcpcPCellNrFreqRelProfileRef Mcpc=1,McpcPCellNrFreqRelProfile=Default
mcpcPSCellNrFreqRelProfileRef Mcpc=1,McpcPSCellNrFreqRelProfile=Default
mdtMeasOn true
nRFrequencyRef NRNetwork=1,NRFrequency=629952-30
nrdcA4ThrRsrpFreqOffset 0
offloadNrFreqRelProfileRef TrafficOffload=1,OffloadNrFreqRelProfile=Default
pMax 23
plmnIdList
plmnRestriction false
qOffsetFreq 0
qQualMin
qRxLevMin -140
redCapEnabled false
sIntraSearchP 62
sIntraSearchQ
tReselectionNR 2
tReselectionNrSfHigh
tReselectionNrSfMedium
threshXHighP 4
threshXHighQ
threshXLowP 0
threshXLowQ
trStSaNrFreqRelProfileRef TrafficSteering=1,TrStSaNrFreqRelProfile=Default
ucmNrFreqRelProfileRef UeCovMeas=1,UcmNrFreqRelProfile=Default
ueMCNrFreqRelProfileRef UeMC=1,UeMCNrFreqRelProfile=Default
end


##################################Cell Specific Ended-- NRCellCU={gUtranCell}############################


"""

DEL_GNBDUFunction = """
###############################Cell Specific Started -- NRCellDU={gUtranCell}############################


crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}
administrativeState 1
arfcnDL {arfcnDL}
arfcnUL {arfcnUL}
bSChannelBwDL {bSChannelBwDL_UL}
bSChannelBwUL {bSChannelBwDL_UL}
configuredMaxTxPower {configuredMaxTxPower}
latitude {Latitude}
longitude {Longitude}
sectorEquipmentFunctionRef NodeSupport=1,SectorEquipmentFunction={sectorEquipmentFunctionId}
txDirection 0
txPowerChangeRate 1
txPowerPersistentLock false
txPowerRatio 100
end

crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId},CommonBeamforming=1
cbfMacroTaperType 0
coverageShape 1
digitalTilt 30
end

crn GNBDUFunction=1,NRCellDU={gUtranCell}
csiRsConfig16P csiRsControl16Ports=0
csiRsConfig2P aRestriction=3F,csiRsControl2Ports=1
csiRsConfig32P csiRsControl32Ports=0
csiRsConfig4P csiRsControl4Ports=1,i11Restriction=FF
csiRsConfig8P csiRsControl8Ports=1,i11Restriction=FFFF
pLMNIdList mcc=404,mnc=10
sibType2 siBroadcastStatus=0,siPeriodicity=64
sibType4 siBroadcastStatus=0,siPeriodicity=64
sibType5 siBroadcastStatus=0,siPeriodicity=64
sibType6 siBroadcastStatus=0,siPeriodicity=16
sibType7 siBroadcastStatus=0,siPeriodicity=64
sibType8 siBroadcastStatus=0,siPeriodicity=64
administrativeState 0
ailgDlPrbLoadLevel 0
ailgModType 0
ailgPdcchLoadLevel 0
bandListManual 78
cellBarred 1
cellLocalId {cellLocalId}
cellRange 12000
cellReservedForOperator 1
csiReportFormat 0
csiRsPeriodicity 40
dftSOfdmMsg3Enabled false
dftSOfdmPuschEnabled false
dl256QamEnabled true
dlMaxMuMimoLayers 0
maxUeSpeed 2
nRPCI {nRPCI}
nRSectorCarrierRef GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}
nRTAC {nRTAC}
pdschStartPrbStrategy 3
pMax 23
puschStartPrbStrategy 3
pZeroNomPucch -110
pZeroNomPuschGrant -102
qRxLevMin -128
rachPreambleFormat 0
rachPreambleRecTargetPower -110
rachPreambleTransMax 10
rachRootSequence {rachRootSequence}
secondaryCellOnly false
siWindowLength 20
ssbDuration 1
ssbFrequency 629952
ssbOffset 0
ssbPeriodicity 20
ssbSubCarrierSpacing 30
subCarrierSpacing 30
tddSpecialSlotPattern 3
tddUlDlPattern 1
trsPeriodicity 40
trsPowerBoosting 0
ul256QamEnabled true
ulMaxMuMimoLayers 0
ulStartCrb 0
userLabel {gUtranCell}
end

############################################################################ Cell Specific Ended -- NRCellDU={gUtranCell}##########################################

"""


DEL_CGSWITCH_SCRIPT = """
############Cell Specific Started -- CgSwitch={gUtranCell}################

crn GNBDUFunction=1,UeCC=1,CgSwitch={gUtranCell}
ueConfGroupType 1
userLabel
end

crn GNBDUFunction=1,UeCC=1,CgSwitchCfg={gUtranCell}
dlCgSwitchMode 1
dlScgCritQualHyst 100
dlScgCritQualThresh
dlScgLowQualHyst 50
dlScgLowQualThresh 50
dlScgNoDataAcsiPeriodicity 300
ulCgSwitchMode 1
ulScgCritQualHyst 100
ulScgCritQualThresh
ulScgLowQualHyst 60
ulScgLowQualThresh 170
userLabel
end

crn GNBDUFunction=1,UeCC=1,CgSwitch={gUtranCell},CgSwitchUeCfg=Base
cgSwitchCfgRef GNBDUFunction=1,UeCC=1,CgSwitchCfg={gUtranCell}
prefUeGroupList
ueConfGroupList
ueGroupList
userLabel
end

############Cell Specific Ended -- CgSwitch={gUtranCell}################

"""
