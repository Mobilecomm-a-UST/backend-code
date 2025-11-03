AS_GPL_LMS_DST_SCRIPT = """

lt all
rbs
rbs


get Router=OAM,.*,Dst=.*,NextHop= address$ > $OAM-Nexthop                                                                               
get Router=LTEUP,.*,Dst=.*,NextHop= address$ > $UP-Nexthop                                                                             
get Router=LTECP,.*,Dst=.*,NextHop= address$ > $CP-Nexthop                                                                              

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS4N                                                                                                  
dst 10.142.81.0/24                                                                                                                                           
end                                                                                                                                                         

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS4N,NextHop=1                                                                                        
address $OAM-Nexthop                                                                                                                                      
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS4M                                                                                                  
dst 10.142.80.0/24                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS4M,NextHop=1                                                                                        
address $OAM-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS3M                                                                                                  
dst 10.142.90.0/24                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS3M,NextHop=1                                                                                        
address $OAM-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS3                                                                                                   
dst 10.142.91.0/24                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS3,NextHop=1                                                                                         
address $OAM-Nexthop                                                                                                                                      
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS2                                                                                                   
dst 10.142.18.0/24                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS2,NextHop=1                                                                                         
address $OAM-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS                                                                                                    
dst 10.142.9.0/24                                                                                                                                            
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS,NextHop=1                                                                                          
address $OAM-Nexthop                                                                                                                                      
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM4                                                                                                   
dst 10.58.118.0/24                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM4,NextHop=45                                                                                        
address $OAM-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM2                                                                                                   
dst 10.102.220.0/24                                                                                                                                          
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM2,NextHop=45                                                                                        
address $OAM-Nexthop                                                                                                                                      
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM                                                                                                    
dst 10.99.113.0/24                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM,NextHop=45                                                                                         
address $OAM-Nexthop                                                                                                                                     
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          


crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X24                                                                                                  
dst 10.26.200.0/22                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X24,NextHop=6                                                                                        
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X23                                                                                                  
dst 10.26.192.0/22                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X23,NextHop=5                                                                                        
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X22                                                                                                  
dst 10.26.184.0/22                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X22,NextHop=4                                                                                        
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X21                                                                                                  
dst 10.26.176.0/22                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X21,NextHop=3                                                                                        
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-50                                                                                                
dst 100.117.16.0/21                                                                                                                                          
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-50,NextHop=41                                                                                     
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-46                                                                                                
dst 100.117.0.0/17                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-46,NextHop=41                                                                                     
address $UP-Nexthop                                                                                                                                      
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-41                                                                                                
dst 10.94.128.0/18                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-41,NextHop=41                                                                                     
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-40                                                                                                
dst 10.26.238.0/23                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-40,NextHop=41                                                                                     
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-39                                                                                                
dst 10.26.236.0/23                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-39,NextHop=41                                                                                     
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-38                                                                                                
dst 10.26.228.0/23                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-38,NextHop=41                                                                                     
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-37                                                                                                
dst 10.26.226.0/23                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-37,NextHop=41                                                                                     
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-36                                                                                                
dst 10.26.224.0/23                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-36,NextHop=41                                                                                     
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-35                                                                                                
dst 10.26.232.0/22                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=X2-35,NextHop=41                                                                                     
address $UP-Nexthop                                                                                                                                      
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=Twamp                                                                                                
dst 10.61.97.8/29                                                                                                                                            
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=Twamp,NextHop=41                                                                                     
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW5                                                                                                 
dst 10.61.86.180/32                                                                                                                                          
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW5,NextHop=41                                                                                      
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW4                                                                                                 
dst 10.61.86.173/32                                                                                                                                          
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW4,NextHop=41                                                                                      
address $UP-Nexthop                                                                                                                                      
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW3                                                                                                 
dst 10.0.219.59/32                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW3,NextHop=2                                                                                       
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW1                                                                                                 
dst 10.50.46.121/32                                                                                                                                          
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW1,NextHop=2                                                                                       
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SBR_U                                                                                                
dst 0.0.0.0/0                                                                                                                                                
end                                                                                                                                                          
crn Transport=1,Router=LTEUP,RouteTableIPv4Static=2,Dst=SBR_U,NextHop=41                                                                                     
address $UP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          

crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X28                                                                                                  
dst 10.26.196.0/22                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X28,NextHop=11                                                                                       
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X27                                                                                                  
dst 10.26.188.0/22                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X27,NextHop=10                                                                                       
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X26                                                                                                  
dst 10.26.180.0/22                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X26,NextHop=9                                                                                        
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X25                                                                                                  
dst 10.26.172.0/22                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X25,NextHop=8                                                                                        
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-49                                                                                                
dst 100.118.16.0/21                                                                                                                                          
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-49,NextHop=44                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-48                                                                                                
dst 10.94.216.0/21                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-48,NextHop=44                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-47                                                                                                
dst 100.118.0.0/17                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-47,NextHop=44                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-45                                                                                                
dst 10.94.192.0/19                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-45,NextHop=7                                                                                      
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-44                                                                                                
dst 10.94.208.0/22                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-44,NextHop=20                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-43                                                                                                
dst 10.94.200.0/21                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-43,NextHop=20                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-34                                                                                                
dst 10.26.216.0/23                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-34,NextHop=19                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-33                                                                                                
dst 10.26.210.0/23                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-33,NextHop=18                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-32                                                                                                
dst 10.26.208.0/23                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-32,NextHop=17                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-31                                                                                                
dst 10.26.206.0/23                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-31,NextHop=16                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-30                                                                                                
dst 10.26.204.0/23                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-30,NextHop=15                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-29                                                                                                
dst 10.26.212.0/22                                                                                                                                           
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=X2-29,NextHop=14                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=SBR_C                                                                                                
dst 0.0.0.0/0                                                                                                                                                
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=SBR_C,NextHop=44                                                                                     
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=RNC                                                                                                  
dst 10.177.250.0/24                                                                                                                                          
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=RNC,NextHop=12                                                                                       
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME_NEW1                                                                                             
dst 10.61.126.218/31                                                                                                                                         
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME_NEW1,NextHop=44                                                                                  
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME3                                                                                                 
dst 10.50.47.168/29                                                                                                                                          
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME3,NextHop=7                                                                                       
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME1                                                                                                 
dst 10.50.46.168/29                                                                                                                                          
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=MME1,NextHop=7                                                                                       
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=AS_MMENEW4                                                                                           
dst 10.1.169.217/32                                                                                                                                          
end                                                                                                                                                          
crn Transport=1,Router=LTECP,RouteTableIPv4Static=3,Dst=AS_MMENEW4,NextHop=7                                                                                 
address $CP-Nexthop                                                                                                                                       
adminDistance 1                                                                                                                                              
bfdMonitoring true                                                                                                                                           
discard false                                                                                                                                                
reference                                                                                                                                                    
end

crn ENodeBFunction=1,TermPointToMme=MME_NEW1
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.61.126.218
ipAddress2 10.61.126.219
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

crn ENodeBFunction=1,TermPointToMme=MME_JHRT
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.50.47.171
ipAddress2 10.50.47.172
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

crn ENodeBFunction=1,TermPointToMme=MME_2
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.50.46.171
ipAddress2 10.50.46.172
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

crn ENodeBFunction=1,TermPointToMme=AS_MMENEW4
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.1.169.224
ipAddress2 10.1.169.225
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end


$date = `date +%y%m%d_%H%M`                                                                                                                                       
cvms Post_GPL_$date   

set  CXC4011368   featurestate  0
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
set  CXC4011983   featurestate  0
set  CXC4011714   featurestate  0
set  CXC4010319   featurestate  1
set  CXC4010320   featurestate  1
set  CXC4010609   featurestate  1
set  CXC4010613   featurestate  1
set  CXC4010616   featurestate  1
set  CXC4010618   featurestate  1
set  CXC4010620   featurestate  1
set  CXC4010717   featurestate  1
set  CXC4010723   featurestate 1
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
set  CXC4011183   featurestate 1
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
set  CXC4011913   featurestate  1
set  CXC4011914   featurestate  1
set  CXC4011918   featurestate  1
set  CXC4011940   featurestate  1
set  CXC4011941   featurestate  1
set  CXC4011955   featurestate  1
set  CXC4011969   featurestate  1
set  CXC4012003   featurestate  1
set  CXC4012018   featurestate  1
set  CXC4012070   featurestate  1
set  CXC4012089   featurestate  1
set  CXC4011476   featurestate  1
set  CXC4011559   featurestate  1
set  CXC4011922   featurestate  1
set  CXC4011946   featurestate  1
set  CXC4012129   featurestate  1
set  CXC4012240   featurestate  1
set  CXC4011072   featurestate  0
set  CXC4011974   featurestate  1
set  CXC4011667   featurestate  1
set  CXC4011056   featurestate  1
set  CXC4010949   featurestate  1
set  CXC4010963   featurestate  1
set  CXC4010964   featurestate  1
set  CXC4011063   featurestate  1
set  CXC4011067   featurestate  1
set  CXC4011068   featurestate  1
set  CXC4011069   featurestate  1
set  CXC4011163   featurestate  1
set  CXC4011256   featurestate  1
set  CXC4011317   featurestate  1
set  CXC4011356   featurestate  1
set  CXC4011427   featurestate  1
set  CXC4011512   featurestate  1
set  CXC4011618   featurestate  1
set  CXC4011699   featurestate  1
set  CXC4011707   featurestate  1
set  CXC4011710   featurestate  1
set  CXC4011716   featurestate  1
set  CXC4011804   featurestate  1
set  CXC4011807   featurestate  1
set  CXC4011809   featurestate  1
set  CXC4011811   featurestate  1
set  CXC4011814   featurestate 1
set  CXC4011817   featurestate  1
set  CXC4011820   featurestate  1
set  CXC4011917   featurestate  1
set  CXC4011930   featurestate  1
set  CXC4011933   featurestate  1
set  CXC4011803   featurestate  1
set  CXC4011937   featurestate  1
set  CXC4011938   featurestate  1
set  CXC4011939   featurestate  1
set  CXC4011942   featurestate  1
set  CXC4011951   featurestate  1
set  CXC4011958   featurestate  0
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
set  CXC4011155   featurestate  1
set  CXC4012261   featurestate  1



lt all                                                                                                                                                                                                                                                                                                                                  
rbs                                                                                                                                                                                                                                                                                                                                 
rbs                                                                                                                                                                                                                                                                                                                                 
confb+                                                                                                                                                                                                                                                                                                                              
gs+                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                    
del UtranFreqRelation=3018                                                                                                                                                                                                                                                                                                          
y                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                    
set ,UtranFreqRelation=10* cellReselectionPriority 0                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                    
set GeranFreqGroupRelation= cellReselectionPriority 1                                                                                                                                                                                                                                                                               
set EUtranFreqRelation=3663 cellReselectionPriority 2                                                                                                                                                                                                                                                                               
set EUtranFreqRelation=1511 cellReselectionPriority 4                                                                                                                                                                                                                                                                               
set EUtranFreqRelation=39294 cellReselectionPriority 5                                                                                                                                                                                                                                                                              
set EUtranFreqRelation=39150 cellReselectionPriority 6                                                                                                                                                                                                                                                                              
set EUtranFreqRelation=39348 cellReselectionPriority 6                                                                                                                                                                                                                                                                              
set ,UtranFreqRelation=10* cellReselectionPriority 3                                                                                                                                                                                                                                                                                
   

cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=265                                                                                                                                                                                                                                                                             
265                                                                                                                                                                                                                                                                                                                                
0     
                                                                                                                                                                                                                                                                                                                                    
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3663                                                                                                                                                                                                                                                                             
3663                                                                                                                                                                                                                                                                                                                               
0   
                                                                                                                                                                                                                                                                                                                                
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1511                                                                                                                                                                                                                                                                             
1511                                                                                                                                                                                                                                                                                                                                
0     

cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1526                                                                                                                                                                                                                                                                             
1526                                                                                                                                                                                                                                                                                                                                
0  
                                                                                                                                                                                                                                                                                                                              
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39150                                                                                                                                                                                                                                                                            
39150                                                                                                                                                                                                                                                                                                                               
0                                                                                                                                                                                                                                                                                                                                   
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39294                                                                                                                                                                                                                                                                            
39294                                                                                                                                                                                                                                                                                                                               
0                                                                                                                                                                                                                                                                                                                                   
cr ENodeBFunction=1,UtraNetwork=1,UtranFrequency=10657                                                                                                                                                                                                                                                                              
10657                                                                                                                                                                                                                                                                                                                               
0                                                                                                                                                                                                                                                                                                                                   
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39348                                                                                                                                                                                                                                                                            
39348                                                                                                                                                                                                                                                                                                                               
0                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                    
cr ENodeBFunction=1,GeraNetwork=1                                                                                                                                                                                                                                                                                                   
cr ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1                                                                                                                                                                                                                                                                                  
1 #frequencyGroupId#                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                    
cr ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=2                                                                                                                                                                                                                                                                                  
2 #frequencyGroupId#                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                    
func Gran_freq                                                                                                                                                                                                                                                                                                                      
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$arfcn                                                                                                                                                                                                                                                                             
$arfcn                                                                                                                                                                                                                                                                                                                              
0                                                                                                                                                                                                                                                                                                                                   
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=$arfcn geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=$g                                                                                                                                                                                                         
endfunc                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                    
for $arfcn = 27 to 37                                                                                                                                                                                                                                                                                                               
$g = 1                                                                                                                                                                                                                                                                                                                              
Gran_freq                                                                                                                                                                                                                                                                                                                           
done                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                    
for $arfcn = 755 to 759                                                                                                                                                                                                                                                                                                             
$g = 2                                                                                                                                                                                                                                                                                                                              
Gran_freq                                                                                                                                                                                                                                                                                                                           
done                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                    
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                    
##creating 2G,3G,4G Relation MO Final##                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                    
unset all                                                                                                                                                                                                                                                                                                                           
$Tab[1] = F3                                                                                                                                                                                                                                                                                                                        
$Tab[2] = F8                                                                                                                                                                                                                                                                                                                        
$Tab[3] = T2                                                                                                                                                                                                                                                                                                                        
$Tab[4] = T1                                                                                                                                                                                                                                                                                                                        
$Tab[5] = F1                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                    
mr F8                                                                                                                                                                                                                                                                                                                               
mr F3                                                                                                                                                                                                                                                                                                                               
mr T2                                                                                                                                                                                                                                                                                                                               
mr T1                                                                                                                                                                                                                                                                                                                               
mr F1                                                                                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                                                                    

ma F3 EUtranCellFDD earfcndl 1526                                                                                                                                                                                                                                                                                                   
ma F8 EUtranCellFDD earfcndl 3663                                                                                                                                                                                                                                                                                                   
ma T2 EUtranCellTDD earfcn 39150                                                                                                                                                                                                                                                                                                    
ma T1 EUtranCellTDD earfcn ^39[2-3]
ma F1 EUtranCellFDD earfcndl 265                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                    
func EURel_3663                                                                                                                                                                                                                                                                                                                     
for $mo in $Tab[$i]                                                                                                                                                                                                                                                                                                                 
 $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                                  
 pr $mordn,EUtranFreqRelation=3663                                                                                                                                                                                                                                                                                                  
 if $nr_of_mos = 0                                                                                                                                                                                                                                                                                                                  
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=3663                                                                                                                                                                                                                                                                                
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3663                                                                                                                                                                                                                                                                              
  2                                                                                                                                                                                                                                                                                                                                 
 fi                                                                                                                                                                                                                                                                                                                                 
done                                                                                                                                                                                                                                                                                                                                
endfunc

func EURel_265                                                                                                                                                                                                                                                                                                                     
for $mo in $Tab[$i]                                                                                                                                                                                                                                                                                                                 
 $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                                  
 pr $mordn,EUtranFreqRelation=265                                                                                                                                                                                                                                                                                                  
 if $nr_of_mos = 0                                                                                                                                                                                                                                                                                                                  
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=265                                                                                                                                                                                                                                                                                
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=265                                                                                                                                                                                                                                                                              
  2                                                                                                                                                                                                                                                                                                                                 
 fi                                                                                                                                                                                                                                                                                                                                 
done                                                                                                                                                                                                                                                                                                                                
endfunc                                                                                                                                                                                                                                                                                                                              


func EURel_1526                                                                                                                                                                                                                                                                                                                     
for $mo in $Tab[$i]                                                                                                                                                                                                                                                                                                                 
 $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                                  
 pr $mordn,EUtranFreqRelation=1526                                                                                                                                                                                                                                                                                                  
 if $nr_of_mos = 0                                                                                                                                                                                                                                                                                                                  
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=1526                                                                                                                                                                                                                                                                                
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1526                                                                                                                                                                                                                                                                              
  4                                                                                                                                                                                                                                                                                                                                 
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
  5                                                                                                                                                                                                                                                                                                                                 
 fi                                                                                                                                                                                                                                                                                                                                 
done                                                                                                                                                                                                                                                                                                                                
endfunc                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                    
func EURel_39348                                                                                                                                                                                                                                                                                                                    
for $mo in $Tab[$i]                                                                                                                                                                                                                                                                                                                 
 $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                                  
 pr $mordn,EUtranFreqRelation=39348                                                                                                                                                                                                                                                                                                 
 if $nr_of_mos = 0                                                                                                                                                                                                                                                                                                                  
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=39348                                                                                                                                                                                                                                                                               
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39348                                                                                                                                                                                                                                                                             
  6                                                                                                                                                                                                                                                                                                                                 
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
  6                                                                                                                                                                                                                                                                                                                                 
 fi                                                                                                                                                                                                                                                                                                                                 
done                                                                                                                                                                                                                                                                                                                                
endfunc                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                    
func URel_10657                                                                                                                                                                                                                                                                                                                     
for $mo in $Tab[$i]                                                                                                                                                                                                                                                                                                                 
 $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                                  
 pr $mordn,UtranFreqRelation=10657                                                                                                                                                                                                                                                                                                  
 if $nr_of_mos = 0                                                                                                                                                                                                                                                                                                                  
  cr ENodeBFunction=1,$mordn,UtranFreqRelation=10657                                                                                                                                                                                                                                                                                
  ENodeBFunction=1,UtraNetwork=1,UtranFrequency=10657                                                                                                                                                                                                                                                                               
  3                                                                                                                                                                                                                                                                                                                                 
 fi                                                                                                                                                                                                                                                                                                                                 
done                                                                                                                                                                                                                                                                                                                                
endfunc                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                    
func Gran_Rel_G9                                                                                                                                                                                                                                                                                                                    
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
                                                                                                                                                                                                                                                                                                                                    
func Gran_Rel_G18                                                                                                                                                                                                                                                                                                                   
for $mo in $Tab[$i]                                                                                                                                                                                                                                                                                                                 
 $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                                  
 pr $mordn,GeranFreqGroupRelation=2                                                                                                                                                                                                                                                                                                 
 if $nr_of_mos = 0                                                                                                                                                                                                                                                                                                                  
  cr ENodeBFunction=1,$mordn,GeranFreqGroupRelation=2                                                                                                                                                                                                                                                                               
  ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=2                                                                                                                                                                                                                                                                                   
  1                                                                                                                                                                                                                                                                                                                                 
 fi                                                                                                                                                                                                                                                                                                                                 
done                                                                                                                                                                                                                                                                                                                                
endfunc                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                    
for $i = 1 to 5                                                                                                                                                                                                                                                                                                                     
##########Relation with 2G: ######                                                                                                                                                                                                                                                                                                  
Gran_Rel_G9                                                                                                                                                                                                                                                                                                                         
Gran_Rel_G18                                                                                                                                                                                                                                                                                                                        
##########Relation with 10657: ######                                                                                                                                                                                                                                                                                               
URel_10657                                                                                                                                                                                                                                                                                                                          
##########Relation with 3663: ######                                                                                                                                                                                                                                                                                                
EURel_3663                                                                                                                                                                                                                                                                                                                          
##########Relation with 1526: ######                                                                                                                                                                                                                                                                                                
EURel_1526                                                                                                                                                                                                                                                                                                                          
##########Relation with 39294: ######                                                                                                                                                                                                                                                                                               
EURel_39294                                                                                                                                                                                                                                                                                                                         
##########Relation with 39150: ######                                                                                                                                                                                                                                                                                               
EURel_39150                                                                                                                                                                                                                                                                                                                         
##########Relation with 39348: ######                                                                                                                                                                                                                                                                                               
EURel_39348                                                                                                                                                                                                                                                                                                                         
done                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                    
##########Relation Done#####                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                    
########### GPL Update 10-09-2025 ##################

set ENodeBFunction=1 alignTtiBundWUlTrigSinr 1
set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 rrcConnReestActive 1
set ENodeBFunction=1 tRelocOverall 20
set ENodeBFunction=1 tS1HoCancelTimer 3
set ENodeBFunction=1 enabledUlTrigMeas true
set ENodeBFunction=1 zzzTemporary52 1
set ENodeBFunction=1 x2GtpuEchoDscp 46
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2SetupTwoWayRelations true
set ENodeBFunction=1 csfbMeasFromIdleMode true
set ENodeBFunction=1 dnsLookupOnTai 1
set ENodeBFunction=1 zzzTemporary13 -2000000000
set ENodeBFunction=1 caAwareMfbiIntraCellHo false
set ENodeBFunction=1 mfbiSupportPolicy false
set ENodeBFunction=1 s1HODirDataPathAvail true
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction=1 timePhaseMaxDeviationIeNbCa 30
set ENodeBFunction=1 s1GtpuEchoEnable  1
set ENodeBFunction=1 checkEmergencySoftLock false
set ENodeBFunction=1 combCellSectorSelectThreshRx 300
set ENodeBFunction=1 combCellSectorSelectThreshTx 300
set ENodeBFunction=1 licConnectedUsersPercentileConf 90
set ENodeBFunction=1 tddVoipDrxProfileId -1
set ENodeBFunction=1 timePhaseMaxDeviation 100
set ENodeBFunction=1 timePhaseMaxDeviationEdrx 10
set ENodeBFunction=1 timePhaseMaxDeviationMbms 50
set ENodeBFunction=1 timePhaseMaxDeviationOtdoa 9
set ENodeBFunction=1 timePhaseMaxDeviationSib16 100
set ENodeBFunction=1 timePhaseMaxDeviationTdd 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd1 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd2 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd3 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd4 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd5 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd6 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd7 15
set ENodeBFunction=1 timePhaseMaxDevIeNBUlComp 30
set ENodeBFunction=1 ulMaxWaitingTimeGlobal 0
set ENodeBFunction=1 ulSchedulerDynamicBWAllocationEnabled true
set ENodeBFunction=1 useBandPrioritiesInSCellEval false
set ENodeBFunction=1 x2GtpuEchoEnable  0
set ENodeBFunction=1 x2IpAddrViaS1Active true
set ENodeBFunction=1 x2retryTimerMaxAuto 1440
set ENodeBFunction=1 timeAndPhaseSynchAlignment true
set ENodeBFunction=1 timeAndPhaseSynchCritical false
set ENodeBFunction=1,SecurityHandling=1 securityHandlingId 1
set ENodeBFunction=1 csmMinHighHitThreshold 50
set ENodeBFunction=1,RadioBearerTable=default,MACConfiguration=1$ ulMaxHARQTx 5
set ENodeBFunction=1,AdmissionControl=1$ dlAdmDifferentiationThr 750
set ENodeBFunction=1,AdmissionControl=1$ ulAdmDifferentiationThr 750 
set ENodeBFunction=1$ enabledUlTrigMeas true
set ENodeBFunction=1$ s1HODirDataPathAvail true
set AutoCellCapEstFunction=1$ useEstimatedCellCap true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1$ anrStateGsm 1 



################  QciProfilePredefined ########################

set QciTable=default,QciProfilePredefined=QCI1$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI2$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI5$ absPrioOverride 1
set QciTable=default,QciProfilePredefined=QCI1$ aqmMode 2
set QciTable=default,QciProfilePredefined=QCI2$ aqmMode 2
set QciTable=default,QciProfilePredefined=QCI5$ aqmMode 0
set QciTable=default,QciProfilePredefined=qci6$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci8$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci9$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci2$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci5$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci6$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci8$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci9$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci7$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI1$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI2$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI5$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci1$ dlMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=QCI2$ dlMinBitRate 384
set QciTable=default,QciProfilePredefined=QCI1$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI2$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI5$ dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=QCI6$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI8$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI9$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci1$ drxPriority 99
set QciTable=default,QciProfilePredefined=qci2$ drxPriority 100
set QciTable=default,QciProfilePredefined=qci3$ drxPriority 0
set QciTable=default,QciProfilePredefined=qci5$ drxPriority 1
set QciTable=default,QciProfilePredefined=qci1$ drxProfileRef DrxProfile=1
set QciTable=default,QciProfilePredefined=qci2$ drxProfileRef DrxProfile=2
set QciTable=default,QciProfilePredefined=qci5$ drxProfileRef DrxProfile=0
set QciTable=default,QciProfilePredefined=QCI6$ dscp 32
set QciTable=default,QciProfilePredefined=QCI7$ dscp 40
set QciTable=default,QciProfilePredefined=QCI8$ dscp 30
set QciTable=default,QciProfilePredefined=QCI9$ dscp 26
set QciTable=default,QciProfilePredefined=QCI1$ dscp 34
set QciTable=default,QciProfilePredefined=QCI2$ dscp 34
set QciTable=default,QciProfilePredefined=QCI5$ dscp 46
set QciTable=default,QciProfilePredefined=qci1$ harqPriority 1
set QciTable=default,QciProfilePredefined=QCI1$ inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI2$ inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI5$ inactivityTimerOffset 0
set QciTable=default,QciProfilePredefined=qci1$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=qci2$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=2
set QciTable=default,QciProfilePredefined=qci5$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=qci6$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci7$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci8$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci9$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=QCI1$ Pdb 80
set QciTable=default,QciProfilePredefined=QCI2$ Pdb 150
set QciTable=default,QciProfilePredefined=QCI5$ Pdb 100
set QciTable=default,QciProfilePredefined=QCI1$ PdbOffset 100
set QciTable=default,QciProfilePredefined=QCI2$ PdbOffset 50
set QciTable=default,QciProfilePredefined=QCI5$ PdbOffset 0
set QciTable=default,QciProfilePredefined=QCI1$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI2$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI5$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI1$ Priority 1
set QciTable=default,QciProfilePredefined=QCI2$ Priority 4
set QciTable=default,QciProfilePredefined=QCI5$ Priority 2
set QciTable=default,QciProfilePredefined=qci1$ resourceType 1
set QciTable=default,QciProfilePredefined=qci2$ resourceType 1
set QciTable=default,QciProfilePredefined=qci5$ resourceType 0
set QciTable=default,QciProfilePredefined=QCI1$ rlcMode 1
set QciTable=default,QciProfilePredefined=QCI2$ rlcMode 1
set QciTable=default,QciProfilePredefined=QCI5$ rlcMode 0
set QciTable=default,QciProfilePredefined=QCI1$ rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI2$ rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI5$ rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI1$ rlfPriority 10
set QciTable=default,QciProfilePredefined=QCI1$ rohcEnabled TRUE
set QciTable=default,QciProfilePredefined=QCI2$ rohcEnabled FALSE
set QciTable=default,QciProfilePredefined=QCI5$ rohcEnabled FALSE
set QciTable=default,QciProfilePredefined=QCI1$ schedulingAlgorithm 6
set QciTable=default,QciProfilePredefined=QCI2$ schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=QCI5$ schedulingAlgorithm 0
set QciTable=default,QciProfilePredefined=QCI6$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI7$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI8$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI9$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI1$ serviceType 1
set QciTable=default,QciProfilePredefined=QCI2$ serviceType 0
set QciTable=default,QciProfilePredefined=QCI5$ serviceType 2
set QciTable=default,QciProfilePredefined=qci1$ tReorderingDl 120
set QciTable=default,QciProfilePredefined=qci1$ ulMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=QCI2$ UlMinBitRate 384
set QciTable=default,QciProfilePredefined=qci1$ tReorderingUl 50
set RadioBearerTable=default,SignalingRadioBearer=1 tReorderingUl 35
set QciTable=default,QciProfilePredefined=qci6$ dscp$ 32
set QciTable=default,QciProfilePredefined=qci7$ dscp$ 26
set QciTable=default,QciProfilePredefined=qci8$ dscp$ 26
set QciTable=default,QciProfilePredefined=qci9$ dscp$ 26
set QciTable=default,QciProfilePredefined=QCI6$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI7$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI8$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI9$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI6$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI7$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI8$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=QCI9$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=qci1$ qciSubscriptionQuanta 60
set QciTable=default,QciProfilePredefined=qci2$ qciSubscriptionQuanta 384
set QciTable=default,QciProfilePredefined=qci5$ qciSubscriptionQuanta 1
set QciTable=default,QciProfilePredefined=qci6$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci7$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci8$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci9$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a1ThresholdRsrpPrimOffset=14 (Deivated Value)
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a2ThresholdRsrpPrimOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold1RsrpOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold2RsrpOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams b2Threshold1RsrpUtraOffset=2
set QciTable=default,QciProfilePredefined=qci6$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci7$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci8$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci9$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=default bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci1    bitRateRecommendationEnabled true  (Should be True)
set QciTable=default,QciProfilePredefined=qci2    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci3    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci4    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci5    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci6    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci65   bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci66   bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci69   bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci7    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci70   bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci8    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci9    bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci1$ qciSubscriptionQuanta 60
set QciTable=default,QciProfilePredefined=qci2$ qciSubscriptionQuanta 384
set QciTable=default,QciProfilePredefined=qci6$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci7$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci8$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci9$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=default$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci1$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci2$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci3$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci4$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci5$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci6$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci7$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci8$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci9$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci1$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci2$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci1$ schedulingAlgorithm 6
set QciTable=default,QciProfilePredefined=qci2$ schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=qci6$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=qci8$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=qci9$ schedulingAlgorithm 4
set QciTable=default,QciProfilePredefined=qci1$ serviceType 1
set QciTable=default,QciProfilePredefined=qci1$ drxPriority 99
set QciTable=default,QciProfilePredefined=qci1$ dscp 34
set QciTable=default,QciProfilePredefined=qci1$ inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=qci1$ pdb 80
set QciTable=default,QciProfilePredefined=qci1$ pdbOffset 100
set QciTable=default,QciProfilePredefined=qci1$ priority 1
set QciTable=default,QciProfilePredefined=qci1$ rlcMode 1
set QciTable=default,QciProfilePredefined=qci1$ rlfPriority 10
set QciTable=default,QciProfilePredefined=qci1$ rohcEnabled true
set QciTable=default,QciProfilePredefined=qci1$ tReorderingDl 120
set QciTable=default,QciProfilePredefined=qci1$ tReorderingUl 50
set QciTable=default,QciProfilePredefined=qci2$ dlMinBitRate 384
set QciTable=default,QciProfilePredefined=qci2$ drxPriority 100
set QciTable=default,QciProfilePredefined=qci2$ dscp 34
set QciTable=default,QciProfilePredefined=qci2$ inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=qci2$ pdbOffset 50
set QciTable=default,QciProfilePredefined=qci2$ rlcMode 1
set QciTable=default,QciProfilePredefined=qci2$ ulMinBitRate 384
set QciTable=default,QciProfilePredefined=qci5$ drxPriority 1
set QciTable=default,QciProfilePredefined=qci5$ dscp 46
set QciTable=default,QciProfilePredefined=qci5$ priority 2
set QciTable=default,QciProfilePredefined=qci1$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci2$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci3$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci4$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci5$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci6$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci7$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci3$ schedulingAlgorithm 0
set QciTable=default,QciProfilePredefined=qci4$ schedulingAlgorithm 0

################ SCTP ####################

set Transport=1,SctpProfile=1 assocMaxRtx 8
set Transport=1,SctpProfile=1 heartbeatInterval 2000
set Transport=1,SctpProfile=1 initRto 2000
set Transport=1,SctpProfile=1 maxRto 4000
set Transport=1,SctpProfile=1 maxInStreams 2
set Transport=1,SctpProfile=1 maxInitRt 5
set Transport=1,SctpProfile=1 maxOutStreams 2
set Transport=1,SctpProfile=1 transmitBufferSize 64
set Transport=1,SctpProfile=1 minRto 1000
set Transport=1,SctpProfile=1 pathMaxRtx 10
set Transport=1,SctpProfile=1 hbMaxBurst 1
set Transport=1,SctpProfile=1 maxSctpPduSize 1480

##########  DRX Profile ##############

lset ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=2$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=0$ drxInactivityTimer 14
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
lset ENodeBFunction=1,DrxProfile=1$ drxState 1
set AnrPciConflictDrxProfile=1 anrPciConflictDrxInactivityTimer 8
set AnrPciConflictDrxProfile=1 anrPciConflictOnDurationTimer 4
set ENodeBFunction=1,DrxProfile=0$ drxInactivityTimer 14
set ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 6
set ENodeBFunction=1,DrxProfile=2$ drxInactivityTimer 6
set ENodeBFunction=1,DrxProfile=0$ drxRetransmissionTimer 4
set ENodeBFunction=1,DrxProfile=1$ drxRetransmissionTimer 2
set ENodeBFunction=1,DrxProfile=1$ drxState 0
set ENodeBFunction=1,DrxProfile=1$ longDrxCycle 3
set ENodeBFunction=1,DrxProfile=2$ longDrxCycle 3
set ENodeBFunction=1,DrxProfile=0$ longDrxCycleOnly 9
set ENodeBFunction=1,DrxProfile=1$ longDrxCycleOnly 3
set ENodeBFunction=1,DrxProfile=2$ longDrxCycleOnly 3
set ENodeBFunction=1,DrxProfile=2$ onDurationTimer 6
set ENodeBFunction=1,DrxProfile=0$ shortDrxCycle 9
set ENodeBFunction=1,DrxProfile=0$ shortDrxCycleTimer 1
set ENodeBFunction=1,DrxProfile=1$ shortDrxCycleTimer 0
set ENodeBFunction=1,DrxProfile=2$ shortDrxCycleTimer 0

###########  CarrierAggregationFunction ###################

set CarrierAggregationFunction=1 dynamicSCellSelectionMethod 2
set CarrierAggregationFunction=1 selectionPolicyUlWeighting 50
set CarrierAggregationFunction=1 fourLayerMimoPreferred false
set CarrierAggregationFunction=1 enhancedSelectionOfMimoAndCa false
set CarrierAggregationFunction=1 waitForAdditionalSCellOpportunity 3000
set CarrierAggregationFunction=1 sCellActProhibitTimer 10
set CarrierAggregationFunction=1 waitForBlindSelSCellRepLessTtt 600
set CarrierAggregationFunction=1 laaSCellDeactProhibitTimer 200


##################   ANR Function ##################

set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrInterFreqState 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrIntraFreqState 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 hoAllowedEutranPolicy true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 x2SetupPolicy true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMax 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMin 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMax 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMin 0
set ENodeBFunction=1,AnrFunction=1 maxNoPciReportsEvent 30
set ENodeBFunction=1,AnrFunction=1 removeNenbTime 3
set ENodeBFunction=1,AnrFunction=1 removeNrelTime 3
set ENodeBFunction=1,AnrFunction=1 probCellDetectMedHoSuccThres 50
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1
set ENodeBFunction=1,AnrFunction=1 plmnWhiteListEnabled true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrpThresholdEutran -1240
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 anrStateUtran 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 hoAllowedUtranPolicy true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 lbCellOffloadCapacityPolicy 30000
set ENodeBFunction=1,AnrFunction=1 plmnWhiteListEnabled false
set AutoCellCapEstFunction=1 useEstimatedCellCap true
set ENodeBFunction=1,AnrFunction=1$ removeNcellTime 3
set ENodeBFunction=1,AnrFunction=1$ removeNrelTime 3
set ENodeBFunction=1,AnrFunction=1$ removeNenbTime 3
set ENodeBFunction=1,AnrFunction=1$ cellRelHoAttRateThreshold 15
set ENodeBFunction=1,AnrFunction=1$ problematicCellPolicy 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1$ anrStateUtran 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ cellAddRsrpThresholdEutran -1240
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ anrInterFreqState 1
set ENodeBFunction=1,AnrFunction=1$ maxNoPciReportsEvent 30
set ENodeBFunction=1,AnrFunction=1$ probCellDetectLowHoSuccTime 4
set ENodeBFunction=1,AnrFunction=1$ probCellDetectMedHoSuccTime 2
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1$ lbCellOffloadCapacityPolicy 30000


######## Timer Profile ####################

set QciTable=default,QciProfilePredefined=qci1 rlfProfileRef RlfProfile=1
set RlfProfile=1$ n310 10
set RlfProfile=1$ n311 1
set RlfProfile=1$ t301 1000
set RlfProfile=1$ t310 500
set RlfProfile=1$ t311 5000
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
seti . tRrcConnectionSetup 10
set Rrc=1 t301 1000
set Rrc=1 t304 2000
set Rrc=1 t311 5000
set Rrc=1  tRrcConnectionReconfiguration 10
set Rcs=1 rlcDlDeliveryFailureAction 2
set Rcs=1 tInactivityTimer  10
set TimerProfile=0 tRelocOverall 20
set TimerProfile=0  tWaitForRrcConnReest 6
set TimerProfile=0  tRrcConnectionReconfiguration 8
set TimerProfile=0  tRrcConnReest 3
set RlfProfile=0$ n310 10
set RlfProfile=1$ n310 10
set RlfProfile=10$ n310 10
set RlfProfile=11$ n310 10
set RlfProfile=12$ n310 10
set RlfProfile=13$ n310 10
set RlfProfile=14$ n310 10
set RlfProfile=15$ n310 10
set RlfProfile=16$ n310 10
set RlfProfile=17$ n310 10
set RlfProfile=18$ n310 10
set RlfProfile=19$ n310 10
set RlfProfile=2$ n310 10
set RlfProfile=20$ n310 10
set RlfProfile=21$ n310 10
set RlfProfile=22$ n310 10
set RlfProfile=3$ n310 10
set RlfProfile=4$ n310 10
set RlfProfile=5$ n310 10
set RlfProfile=6$ n310 10
set RlfProfile=7$ n310 10
set RlfProfile=8$ n310 10
set RlfProfile=9$ n310 10
set RlfProfile=0$ t301 1000
set RlfProfile=0$ t310 500
set RlfProfile=1$ t311 5000
set ENodeBFunction=1,Rrc=1$ t301 1000
set ENodeBFunction=1,Rrc=1$ t311 5000
set ENodeBFunction=1,Rrc=1$ t304 2000
set ENodeBFunction=1,Rrc=1$ tRrcConnectionReconfiguration 10
set Rcs=1$ rlcDlDeliveryFailureAction 2
set ENodeBFunction=1$ tRelocOverall 20
set ENodeBFunction=1$ zzzTemporary52 1
set ENodeBFunction=1,Rrc=1$ tRrcConnReest 2
set ENodeBFunction=1,Rrc=1$ tWaitForRrcConnReest 9
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ dlMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ ulMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1$ dlMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1$ ulMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ tPollRetransmitUl 60
set RlfProfile=1$ t310 500
set RlfProfile=1$ t301 1000
set RlfProfile=5$ t301 1000

################   AdmissionControl #########################

set AdmissionControl=1 admNrRbDifferentiationThr 750
set AdmissionControl=1 admNrRrcDifferentiationThr 750
set AdmissionControl=1 arpBasedPreEmptionState 0
set AdmissionControl=1 ulAdmOverloadThr  950
set AdmissionControl=1 ulTransNwBandwidth 2000
set AdmissionControl=1 paArpOverride 2
set PmEventService=1 cellTraceFileSize 20000
set AdmissionControl dlAdmDifferentiationThr 950
set AdmissionControl ulAdmDifferentiationThr 950


################  MdtConfiguration  ######################

set MdtConfiguration=1 a2ThresholdRsrpMdt -140
set MdtConfiguration=1 a2ThresholdRsrqMdt -195
set MdtConfiguration=1 timeToTriggerA2Mdt 640
set MdtConfiguration=1 triggerQuantityA2Mdt 0

############### MACConfiguration ######################

set ENodeBFunction=1,RadioBearerTable=default,MACConfiguration=1 ulMaxHARQTx 5
set ENodeBFunction=1,RadioBearerTable=default,MACConfiguration=1 ulTtiBundlingMaxHARQTx 7
set ENodeBFunction=1,RadioBearerTable=default,MACConfiguration=1 dlMaxHARQTx 4

################# Signaling-DataRadioBearer-paging  ######################

set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitDl 80
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitUl 80
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 dlMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitUl 80
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitDl 80
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 dlMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 ulMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 ulMaxRetxThreshold 16
set ENodeBFunction=1,Paging=1 pagingDiscardTimerDrxNb 3
set ENodeBFunction=1,Paging=1 maxNoOfPagingRecordsNb 3
set ENodeBFunction=1,Paging=1 noOfDefPagCyclPrim 8

################  Load Balancing Function #################

set LoadBalancingFunction=1 lbRateOffsetCoefficient 320
set LoadBalancingFunction=1 lbRateOffsetLoadThreshold 320
set LoadBalancingFunction=1 lbCeiling 300
set LoadBalancingFunction=1 lbCaThreshold 2000
set LoadBalancingFunction=1 lbThreshold 30
set LoadBalancingFunction=1 lbHitRateEUtranAddThreshold 3
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeIntensity 10
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeThreshold 10
set LoadBalancingFunction=1 lbHitRateEUtranRemoveThreshold 0
set LoadBalancingFunction=1 lbMeasScalingLimit 50
set LoadBalancingFunction=1$ lbThreshold 30
set LoadBalancingFunction=1$ lbCeiling 300
set LoadBalancingFunction=1$ txPwrForOverlaidCellDetect 370



################  Common Cell Parameters TDD + FDD    ###########################

set EUtranCell.*=.* allocThrPucchFormat1 50
set EUtranCell.*=.* allocTimerPucchFormat1 50
set EUtranCell.*=.* deallocThrPucchFormat1 100
set EUtranCell.*=.* deallocTimerPucchFormat1 6000
set EUtranCell.*=.* dlBlerTargetEnabled true
set EUtranCell.*=.* drxActive true
set EUtranCell.*=.* enableServiceSpecificHARQ true
set EUtranCell.*=.* pdcchCovImproveDtx true
set EUtranCell.*=.* pdcchCovImproveSrb false
set EUtranCell.*=.* pdcchTargetBler 24
set EUtranCell.*=.* pdcchTargetBlerPCell 22
set EUtranCell.*=.* pMaxServingCell 26
set EUtranCell.*=.* tReorderingAutoConfiguration true
set EUtranCell.*=.* tTimeAlignmentTimer 0
set EUtranCell.*=.* ulBlerTargetEnabled true
set EUtranCell.*=.* ulHarqVolteBlerTarget 3
set EUtranCell.*=.* adaptiveCfiHoProhibit 0
set EUtranCell.*=.* enableSinrUplinkClpc true
set EUtranCell.*=.* pdcchCovImproveQci1 true
set EUtranCell.*=.* pdcchOuterLoopUpStepVolte 9
set EUtranCell.*=.* pdcchTargetBlerVolte 4
set EUtranCell.*=.* alpha 8
set EUtranCell.*=.* pZeroNominalPucch -110
set EUtranCell.*=.* cfraEnable true
set EUtranCell.*=.* changeNotification changeNotificationSIB15=true
set EUtranCell.*=.* changeNotification changeNotificationSIB16=true
set EUtranCell.*=.* changeNotification changeNotificationSIB7=true
set EUtranCell.*=.* changeNotification changeNotificationSIB2=true
set EUtranCell.*=.* changeNotification changeNotificationSIB3=true
set EUtranCell.*=.* changeNotification changeNotificationSIB4=true
set EUtranCell.*=.* changeNotification changeNotificationSIB1=true
set EUtranCell.*=.* changeNotification changeNotificationSIB6=true
set EUtranCell.*=.* changeNotification changeNotificationSIB5=true
set EUtranCell.*=.* changeNotification changeNotificationSIB13=true
set EUtranCell.*=.* changeNotification changeNotificationSIB8=true
set EUtranCell.*=.* mappingInfoCe mappingInfoSIB10=0
set EUtranCell.*=.* hoOptAdjThresholdAbs 5
set EUtranCell.*=.* hoOptAdjThresholdPerc 50
set EUtranCell.*=.* pdcchCfiMode 5
set EUtranCell.*=.* transmissionMode  4
set EUtranCell.*=.* ns05FullBandUsersInCellThres 1
set EUtranCell.*=.* puschNcpChannelEstWindowSize 1
set EUtranCell.*=.* mobCtrlAtPoorCovActive true
set EUtranCell.*=.* servOrPrioTriggeredIFHo 0
set EUtranCell.*=.* ul64qamEnabled true
set EUtranCell.*=.* dl256QamStatus 2
set EUtranCell.*=.* dl256QamEnabled true
set EUtranCell.*=.* qRxLevMinCe -140
set EUtranCell.*=.* pdcchLaGinrMargin 40
set EUtranCell.*=.* acBarringPresence acBarringForMmtelVideoPresence=0
set EUtranCell.*=.* acBarringPresence acBarringForMmtelVoicePresence=0
set EUtranCell.*=.* acBarringPresence acBarringPriorityMmtelVideo=0
set EUtranCell.*=.* acBarringPresence acBarringPriorityMmtelVoice=0
set EUtranCell.*=.* acBarringPresence acBarringForMoDataPresence=0
set EUtranCell.*=.* noOfEnhAdptReTxCand -1
set EUtranCell.*=.* dynUlResourceAllocEnabled true
set EUtranCell.*=.* systemInformationBlock6 tReselectionUtra=4
set EUtranCell.*=.* systemInformationBlock6 tReselectionUtraSfHigh=100
set EUtranCell.*=.* systemInformationBlock6 tReselectionUtraSfMedium=100
set EUtranCell.*=.* advCellSupAction  2
set EUtranCell.*=.* primaryPlmnReserved false
set EUtranCell.*=.* harqOffsetDl 3
set EUtranCell.*=.* harqOffsetUl 3
set EUtranCell.*=.* highSpeedUEActive false
set EUtranCell.*=.* initialBufferSizeDefault 86
set EUtranCell.*=.* prsTransmisScheme 0
set EUtranCell.*=.*  puschPwrOffset64qam 0
set EUtranCell.*=.* systemInformationBlock3 tEvaluation=240
set EUtranCell.*=.* cellRange 15
set EUtranCell.*=.* elcEnabled false
set EUtranCell.*=.* preambleInitialReceivedTargetPower -110
set EUtranCell.*=.* acBarringForCsfb acBarringFactor=95
set EUtranCell.*=.* acBarringForCsfb acBarringForSpecialAC=false false false false false
set EUtranCell.*=.* acBarringForCsfb acBarringTime=64
set EUtranCell.*=.* acBarringForEmergency false
set EUtranCell.*=.* acBarringForMoData acBarringFactor=95
set EUtranCell.*=.* acBarringForMoData acBarringForSpecialAC=false false false false false
set EUtranCell.*=.* acBarringForMoData acBarringTime=64
set EUtranCell.*=.* acBarringForMoSignalling acBarringFactor=95
set EUtranCell.*=.* acBarringForMoSignalling acBarringForSpecialAC=false false false false false
set EUtranCell.*=.* acBarringForMoSignalling acBarringTime=64
set EUtranCell.*=.* acBarringInfoPresent false
set EUtranCell.*=.* acBarringPresence acBarringForCsfbPresence=0
set EUtranCell.*=.* acBarringPresence acBarringForMoSignPresence=0
set EUtranCell.*=.* acBarringPresence acBarringPriorityCsfb=0
set EUtranCell.*=.* acBarringPresence acBarringPriorityMoData=0
set EUtranCell.*=.* acBarringPresence acBarringPriorityMoSignaling=0
set EUtranCell.*=.* spifhoSetupBearerAtInitialCtxtSetup false
set EUtranCell.*=.* srDetectHighThres 70
set EUtranCell.*=.* srProcessingLevel 0
set EUtranCell.*=.* ssacBarringForMMTELVideo acBarringFactor=95
set EUtranCell.*=.* ssacBarringForMMTELVideo acBarringForSpecialAC=false false false false false
set EUtranCell.*=.* ssacBarringForMMTELVideo acBarringTime=64
set EUtranCell.*=.* ssacBarringForMMTELVoice acBarringFactor=95
set EUtranCell.*=.* ssacBarringForMMTELVoice acBarringForSpecialAC=false false false false false
set EUtranCell.*=.* ssacBarringForMMTELVoice acBarringTime=64
set EUtranCell.*=.* systemInformationBlock3 tEvaluation=240
set EUtranCell.*=.* systemInformationBlock3 nCellChangeHigh=16
set EUtranCell.*=.* systemInformationBlock3 nCellChangeMedium=16
set EUtranCell.*=.* systemInformationBlock3 qHystSfHigh=0
set EUtranCell.*=.* systemInformationBlock3 qHystSfMedium=0
set EUtranCell.*=.* systemInformationBlock3 sIntraSearchQ=0
set EUtranCell.*=.* systemInformationBlock3 sNonIntraSearchv920Active=false
set EUtranCell.*=.* systemInformationBlock3 sIntraSearchv920Active=false
set EUtranCell.*=.* systemInformationBlock3 threshServingLowQ=1000
set EUtranCell.*=.* systemInformationBlock3 tHystNormal=240
set EUtranCell.*=.* systemInformationBlock7 tReselectionGeran=2
set EUtranCell.*=.* systemInformationBlock7 tReselectionGeranSfHigh=100
set EUtranCell.*=.* systemInformationBlock7 ReselectionGeranSfMedium=100
set EUtranCell.*=.* tUeBlockingTimer 200
set EUtranCell.*=.* ulImprovedUeSchedLastEnabled true
set EUtranCell.*=.* ulSCellPriority 5
set EUtranCell.*=.* ulSchedCtrlForOocUesEnabled true
set EUtranCell.*=.* ulSrsEnable False
set EUtranCell.*=.* ulTxPsdDistrThr 40
set EUtranCell.*=.* uncertAltitude 0
set EUtranCell.*=.* uncertSemiMajor 0
set EUtranCell.*=.* uncertSemiMinor 0
set EUtranCell.*=.* covTriggerdBlindHoAllowed false
set EUtranCell.*=.* qQualMin -34
set EUtranCell.*=.* qRxLevMin -124
set EUtranCell.*=.* srvccDelayTimer 3000
set EUtranCell.*=.* dlInterferenceManagementActive true
set EUtranCell.*=.* ulInterferenceManagementActive true
set EUtranCell.*=.* dlFrequencyAllocationProportion 100
set EUtranCell.*=.* ulConfigurableFrequencyStart 0
set EUtranCell.*=.* ulFrequencyAllocationProportion 100
set EUtranCell.*=.* outOfCoverageSparseGrantingBsr 8
set EUtranCell.*=.* eUlFssSwitchThresh 30
set EUtranCell.*=.* pdcchPowerBoostMax 2
set EUtranCell.*=.* dlMaxRetxRrcReleaseThr 8
set EUtranCell.*=.* sCellHandlingAtVolteCall 1


################  Common Cell Parameters FDD Technology   ###########################

set EUtranCellFDD=.* pdcchOuterLoopUpStep 8
set EUtranCellFDD=.* pdcchOuterLoopUpStepPCell 6
set EUtranCellFDD=.* ttiBundlingAfterHo 1
set EUtranCellFDD=.* ttiBundlingAfterReest 1
set EUtranCellFDD=.* ttiBundlingSwitchThres 150
set EUtranCellFDD=.* ttiBundlingSwitchThresHyst 30
set EUtranCellFDD=.* cellDownlinkCaCapacity 0
set EUtranCellFDD=.* mappingInfo mappingInfoSIB12=7
set EUtranCellFDD=.* mappingInfo mappingInfoSIB6$=4
set EUtranCellFDD=.* mappingInfo mappingInfoSIB4$=2
set EUtranCellFDD=.* mappingInfo mappingInfoSIB5=3
set EUtranCellFDD=.* servOrPrioTriggeredErabAction 3
set EUtranCellFDD=.* dlInternalChannelBandwidth 0
set EUtranCellFDD=.* ulInternalChannelBandwidth 0
set EUtranCellFDD=.* commonSrPeriodicity 10
set EUtranCellFDD=.* lbEUtranTriggerOffloadThreshold 30
set EUtranCellFDD=.* changeNotification changeNotificationSIB1=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB2=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB3=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB4=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB5=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB6=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB7=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB13=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB15=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB16=true
set EUtranCellFDD=.* changeNotification changeNotificationSIB8=true
set EUtranCellFDD=AS_E_F8.* pZeroNominalPusch -83
set EUtranCellFDD=AS_E_F3.* pZeroNominalPusch -83
set EUtranCellFDD=AS_E_F1.* pZeroNominalPusch -86
set EUtranCellFDD=AS_E_F8.* crsGain 300
set EUtranCellFDD=AS_E_F3.* crsGain 0
set EUtranCellFDD=AS_E_F1.* crsGain 300
set EUtranCellFDD=.* ulTrigActive false
set EUtranCellFDD=AS_E_F3.* pdschTypeBGain 0
set EUtranCellFDD=.* lbEUtranAcceptOffloadThreshold 10




################  Common Cell Parameters TDD Technology   ###########################

set EUtranCellTDD=.* hoOptStatTime 24
set EUtranCellTDD=.* channelBandwidth 20000
set EUtranCellTDD=.* dlMaxMuMimoLayers 0
set EUtranCellTDD=.* ulMaxMuMimoLayers 0
set EUtranCellTDD=.* subframeAssignment 2
set EUtranCellTDD=.* timePhaseMaxDeviationTDDIndex 0
set EUtranCellTDD=.* commonSrPeriodicity 20
set EUtranCellTDD=.* mappingInfo mappingInfoSIB7=5
set EUtranCellTDD=.* pZeroNominalPusch -86
set EUtranCellTDD=.* crsGain 0
set EUtranCellTDD=.* pdschTypeBGain 0
set EUtranCellTDD=.* ulTrigActive true
set EUtranCellTDD=.* cellRange 10
set EUtranCellTDD=.* outOfCoverageSparseGrantingBsr 8
set EUtranCellTDD=.* interferenceThresholdSinrClpc -100
set EUtranCellTDD=.* rxSinrTargetClpc 20
set EUtranCellTDD=.* lbEUtranAcceptOffloadThreshold 50
set EUtranCellTDD=.* systemInformationBlock3 sNonIntraSearch=12
set EUtranCellTDD=.* systemInformationBlock3 sNonIntraSearchQ=0
set EUtranCellTDD=.*,UeMeasControl=1$ inhibitB2RsrqConfig true
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrp 0
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1$ a3offsetAnrDelta 3
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1$ timeToTriggerA5 480
set EUtranCellTDD=.* alpha 8
set EUtranCellTDD=.* cellCapMaxCellSubCap 60000
set EUtranCellTDD=.* cellCapMinCellSubCap 2000
set EUtranCellTDD=.* drxActive true
set EUtranCellTDD=.* pdcchLaGinrMargin 40
set EUtranCellTDD=.* pdcchOuterLoopUpStepVolte 9
set EUtranCellTDD=.* pdcchPowerBoostMax 0
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA1Search 480
set EUtranCellTDD=.* ulBlerTargetEnabled true
set EUtranCellTDD=.* enableServiceSpecificHARQ true
set EUtranCellTDD=.* tReorderingAutoConfiguration true
set EUtranCellTDD=.* srvccDelayTimer 3000
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ b2Threshold2Geran -110
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1$ hysteresisB2 20
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1$ timeToTriggerB2 1280
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1$ timeToTriggerA3 480
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1$ timeToTriggerA3 480
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraIFBestCell=1$ timeToTriggerA3 480
set EUtranCellTDD=.*,UeMeasControl=1$ ueMeasurementsActive true
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2Search 480
set EUtranCellTDD=.* advCellSupAction 2
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ timeToTriggerB2 1280
set EUtranCellTDD=.* dlBlerTargetEnabled true
set EUtranCellTDD=.* pdcchCovImproveDtx true
set EUtranCellTDD=.* ulHarqVolteBlerTarget 3
set EUtranCellTDD=.* ns05FullBandUsersInCellThres 1
set EUtranCellTDD=.* puschNcpChannelEstWindowSize 1
set EUtranCellTDD=.* noOfEnhAdptReTxCand -1
set EUtranCellTDD=.* dynUlResourceAllocEnabled true
set EUtranCellTDD=.* acBarringInfoPresent false
set EUtranCellTDD=.* outOfCoverageSparseGrantingBsr 8
set EUtranCellTDD=.* eUlFssSwitchThresh 30
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold1Rsrp -140
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold1Rsrq -195
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold1Rsrq -195
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold2Rsrp -112
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold2Rsrq -195
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB1GUtra=1$ b1ThresholdRsrq -435
set EUtranCellTDD=.* crsGain 0
set EUtranCellTDD=.* cellSubscriptionCapacity 20000
set EUtranCellTDD=.* pdschTypeBGain 0
set EUtranCellTDD=.* pZeroNominalPusch -86
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrp -114
set EUtranCellTDD=.* pdcchTargetBlerVolte 4
set EUtranCellTDD=.*,UeMeasControl=1$ excludeInterFreqAtCritical true
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1$ hysteresisA5 20
set EUtranCellTDD=.* enableSinrUplinkClpc true
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA1UlSearch 480
set EUtranCellTDD=.* systemInformationBlock6 tReselectionUtra=4
set EUtranCellTDD=.* systemInformationBlock3 sIntraSearchQ=0,sNonIntraSearchQ=0
set EUtranCellTDD=.* changeNotification changeNotificationSIB15=true,changeNotificationSIB16=true

###############  Relation Parameters #################

set EUtranCell.*=.*,EUtranFreqRelation=.* tReselectionEutra 2
set EUtranCell.*=.*,EUtranFreqRelation=.* anrMeasOn true
set EUtranCell.*=.*,GeranFreqGroupRelation=1 anrMeasOn true
set EUtranCell.*=.*,EUtranFreqRelation=.*,EUtranCellRelation=.* isHoAllowed true
set EUtranCell.*=.*,GeranFreqGroupRelation=1 anrMeasOn true
set EUtranCell.*=.*,GeranFreqGroupRelation=1 qRxLevMin -111
set EUtranCell.*=.*,EUtranFreqRelation=.* qRxLevMinCe -140
set EUtranCell.*=.*,EUtranFreqRelation=.* pMax 1000
set EUtranCell.*=.*,EUtranFreqRelation=.* tReselectionEutraSfHigh 100
set EUtranCell.*=.*,EUtranFreqRelation=.* tReselectionEutraSfMedium 100
set EUtranCell.*=.*,EUtranFreqRelation=.* qRxLevMin -124
set EUtranCell.*=.*,EUtranFreqRelation=.* mobilityAction 1
set EUtranCell.*=.*,EUtranFreqRelation=.* lbBnrAllowed true
set EUtranCell.*=.*,EUtranFreqRelation=.* lbBnrPolicy 2
set EUtranCell.*=.* altCsfbTargetPrio 2
set EUtranCell.*=.* altCsfbTargetPrioEC 2
set EUtranCell.*=.* mobilityActionCsfb 1
set EUtranCell.*=.* mobilityAction 1
set EUtranCell.*=.*,EUtranFreqRelation=39150 allowedMeasBandwidth 100
set EUtranCell.*=.*,EUtranFreqRelation=39348 allowedMeasBandwidth 100
set EUtranCell.*=.*,EUtranFreqRelation=265 allowedMeasBandwidth 75
set EUtranCell.*=.*,EUtranFreqRelation=1526 allowedMeasBandwidth 50
set EUtranCell.*=.*,EUtranFreqRelation=3663 allowedmeasbandwidth 25

##################### UeMeasControl=1 ##############################

set EUtranCell.*=.*,UeMeasControl=1,ReportConfigCsfbUtra=1 hysteresis 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigCsfbGeran=1 hysteresis 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSCellA6=1 triggerQuantityA6 0
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrp -140
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 20
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Utra=1 hysteresisB2 20
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1SearchRsrq 1024
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2CriticalRsrq 1024
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2SearchRsrq 1024
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5Rsrq 1024
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 timeToTriggerB2 1280
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 triggerQuantityA3 0
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 triggerQuantityA5 0
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSCellA6=1 timeToTriggerA6 40
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigElcA1A2=1 hysteresisA1A2Rsrp 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB1Geran=1 hysteresisB1 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB1Utra=1 hysteresisB1 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigElcA1A2=1 timeToTriggerA1 40
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSCellA1A2=1 timeToTriggerA1 40
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1UlSearch 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSCellA1A2=1 timeToTriggerA2 40
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigElcA1A2=1 timeToTriggerA2 40
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2OutSearchRsrq -1
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB1Geran=1 timeToTriggerB1   640
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 timeToTriggerB2Rsrq -1
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Utra=1 timeToTriggerB2Rsrq -1
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5 10
set EUtranCell.*=.*,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset -20
set EUtranCell.*=.*,UeMeasControl=1 filterCoefficientEUtraRsrp 4
set EUtranCell.*=.*,UeMeasControl=1 ueMeasurementsActiveIF true
set EUtranCell.*=.*,UeMeasControl=1 zzzTemporary13    -2000000000
set EUtranCell.*=.*,UeMeasControl=1 sMeasure 0
set EUtranCell.*=.*,UeMeasControl=1 lowPrioMeasThresh 0
set EUtranCell.*=.*,UeMeasControl=1 maxUtranCellsToMeasure 32
set EUtranCell.*=.*,UeMeasControl=1 allowReleaseQci1 false
set EUtranCell.*=.*,UeMeasControl=1 ulSinrOffset 30
set EUtranCell.*=.*,UeMeasControl=1 ueMeasurementsActive true
set EUtranCell.*=.*,UeMeasControl=1 a5B2MobilityTimer 0
set EUtranCellFDD=.*,UeMeasControl=1 ueMeasurementsActiveGERAN true
set EUtranCellTDD=.*,UeMeasControl=1 ueMeasurementsActiveGERAN False
set EUtranCell.*=.*,UeMeasControl=1 excludeInterFreqAtCritical false
set EUtranCell.*=.*,UeMeasControl=1 a3SuspendCsgTimer 0
set EUtranCell.*=.*,UeMeasControl=1 ueMeasurementsActiveUTRAN true
set EUtranCellTDD=.*,UeMeasControl=1 excludeInterFreqAtCritical true
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlCritical 480
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlCritical 480
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlSearch 480
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2UlSearch 480
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1  hysteresisA5RsrqOffset 150
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -102
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp  -119
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrqOffset -100
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 a1a2UlSearchThreshold 60
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2UlCritical 150
set EUtranCell.*=.*,UeMeasControl=1 csfbHoTargetSearchTimer 1200
set EUtranCell.*=.*,UeMeasControl=1      bothA5RsrpRsrqCheck false
set EUtranCell.*=.*,UeMeasControl=1      inhibitB2RsrqConfig true
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 timeToTriggerB2Rsrq -1
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp  -140
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB1Geran=1 b1ThresholdGeran  -110
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 reportIntervalB2 4
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrq -195

######################  AnrFunction=1 ############################

set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1  cellAddEcNoThresholdUtranDelta -10
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrpThresholdEutran -1240
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1  cellAddRscpThresholdUtranDelta -1
set ENodeBFunction=1,AnrFunction=1 cellRelHoAttRateThreshold 15
set ENodeBFunction=1,AnrFunction=1 probCellDetectLowHoSuccTime 4
set ENodeBFunction=1,AnrFunction=1 probCellDetectMedHoSuccTime 2
set ENodeBFunction=1,AnrFunction=1 problematicCellPolicy 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 problematicCellPolicy 0
set ENodeBFunction=1,AnrFunction=1 removeNcellTime 3
set ENodeBFunction=1,AnrFunction=1 zzzTemporary13    -2000000000

######## QOS setting #######################################

set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction=1 interEnbCaTunnelDscp 26
set ENodeBFunction=1 interEnbUlCompTunnelDscp 26
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2GtpuEchoDscp 46
set ENodeBFunction=1 X2GtpuEchoDscp 46

cr Transport=1,QosProfiles=1,DscpPcpMap=1

set QciTable=default,QciProfilePredefined=qci1 dscp 34
set QciTable=default,QciProfilePredefined=qci2 dscp 34
set QciTable=default,QciProfilePredefined=qci3 dscp 26
set QciTable=default,QciProfilePredefined=qci4 dscp 26
set QciTable=default,QciProfilePredefined=qci5 dscp 46
set QciTable=default,QciProfilePredefined=qci6 dscp 26
set QciTable=default,QciProfilePredefined=qci7 dscp 26
set QciTable=default,QciProfilePredefined=qci8 dscp 26
set QciTable=default,QciProfilePredefined=qci9 dscp 26

set SysM=1,OamTrafficClass=1 dscp 28

set EthernetPort=TN_E egressQosMarking  QosProfiles=1,DscpPcpMap=1
set EthernetPort= egressQosMarking  QosProfiles=1,DscpPcpMap=1

set SctpProfile= dscp 46
set Ntp=1,NtpFrequencySync= dscp 34


lt all


set QosProfiles=1,DscpPcpMap=1  pcp0
set QosProfiles=1,DscpPcpMap=1  pcp1
set QosProfiles=1,DscpPcpMap=1  pcp2 
set QosProfiles=1,DscpPcpMap=1  pcp3
set QosProfiles=1,DscpPcpMap=1  pcp4
set QosProfiles=1,DscpPcpMap=1  pcp5
set QosProfiles=1,DscpPcpMap=1  pcp6
set QosProfiles=1,DscpPcpMap=1  pcp7


set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0 1 2 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 36 37 38 39 41 43 45 47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22 24 26

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6 8 10 30 32

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12 14 40

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4 28

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16 18 34 42 44

set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20 46

set Router=OAM,DnsClient=1 dscp 28

et Router=.*,InterfaceIPv4= egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=.*,InterfaceIPv4= ingressQosMarking QosProfiles=1,DscpPcpMap=1
set Router=LTECP,InterfaceIPv4=TN_E_CP  egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=LTEUP,InterfaceIPv4=TN_E_UP  egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=TN_E_OAM   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=TN_E_ABIS  egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=TN_E_IUB   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=     egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_E_CP    egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_E_OAM   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_E_UP    egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_E_IUB   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set VlanPort=TN_E_ABIS  egressQosMarking  QosProfiles=1,DscpPcpMap=1




###############  AMS & CA Scripts ############################


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
set FeatureState=CXC4012123 featureState 1
set Licensing=1,OptionalFeatureLicense=AutomaticSCellManagement$  featureState  1
set SystemFunctions=1,Lm=1,FeatureState=CXC4011983 featureState 1
set Licensing=1,OptionalFeatureLicense=InterENBCarrierAggregation$  featureState  1
set EUtranCell.*=.* sCellHandlingAtVolteCall 1
set EUtranCell.*=.*,EUtranFreqRelation=.*,EUtranCellRelation=.* sCellCandidate    2

set CXC4011958|CXC4011808|CXC4011803|CXC4011378 FeatureState 1

set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=39348 asmSCellDetection 3

set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=39151 asmSCellDetection 3
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=39150 asmSCellDetection 3
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=39151 asmSCellDetection 3

set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=265 asmSCellDetection 0
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=265 asmSCellDetection 0
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=3663 asmSCellDetection 0
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=3663 asmSCellDetection 0
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=1526 asmSCellDetection 0
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=1526 asmSCellDetection 0

set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=265 asmSCellDetection 0
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=3663 asmSCellDetection 0
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=1526 asmSCellDetection 0
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=39150 asmSCellDetection 0
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=39148 asmSCellDetection 0

set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=265 asmSCellDetection 0
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=3663 asmSCellDetection 0
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=1526 asmSCellDetection 0
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=39151 asmSCellDetection 0
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=39147 asmSCellDetection 0
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=39150 asmSCellDetection 0
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=39348 asmSCellDetection 0

set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=265 asmSCellDetection 0
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=3663 asmSCellDetection 0
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=1526 asmSCellDetection 0
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=39151 asmSCellDetection 0
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=39147 asmSCellDetection 0
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=39150 asmSCellDetection 0
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=39348 asmSCellDetection 0

set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=39150  caTriggeredRedirectionActive true
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=39348  caTriggeredRedirectionActive true

##############  LTE PIM Detection in Baseband #################

set EUtranCellFDD=.* pimDetectionEnabled true
set ENodeBFunction=1 pimAutoDetectionEnabled false
set CXC4010955|CXC4011368|CXC4011842 featurestate 0
set PreschedProfile=.* preschedulingDataSize 86
set PreschedProfile=.* preschedulingPeriod 5
set PreschedProfile=.* preschedulingDuration 200
set PreschedProfile=0 preschedulingSinrThreshold 15

##############  ASGH based Pre-Scheduling  ###################

set SubscriberGroupProfile=1 preschedulingMode 2
set CXC4012200|CXC4011715 featureState 1

############# Differential Uplink Power Contr ####################

set EUtranCellTDD=.* enableSinrUplinkClpc true
set EUtranCellTDD=.* rxSinrTargetClpc 16
set EUtranCellTDD=.* interferenceThresholdSinrClpc -105
set EUtranCellTDD=.* ulPsdLoadThresholdSinrClpc 2
set EUtranCellTDD=.* ulTxPsdDistrThr 40
set EUtranCellTDD=.* p0ClpcExGoodEnabled true
set EUtranCellTDD=.* p0ClpcExBadEnabled true
set EUtranCellTDD=.* p0ClpcExBadSinrThr -10
set EUtranCellTDD=.* p0ClpcExGoodSinrThr 16
set EUtranCellTDD=.* p0ClpcExGoodSinrOffset64Qam 3
set EUtranCellTDD=.* p0ClpcExGoodSinrOffset256Qam 10
set EUtranCellTDD=.* assumedUePowerMsg3 1000
set CXC4012089 featureState 1

############### Increase number of GTP-U connec ######################

set CXC4012022 featureState 1
set ENodeBFunction=1 s1GtpuEchoEnable 1

################  Atmospheric Duct Int Reduction  #########################

set EUtranCellTDD=.* subframeAssignment 2
set EUtranCellTDD=.* specialSubframePattern 7
set EUtranCellTDD=.* ductIntOpMode 3
set EUtranCellTDD=.* ductIntPerfTuning ductIntBgNoiseThr=-105
set EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqCorrPeakThr=50
set EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqPwrDiff=5
set EUtranCellTDD=.* ductIntPerfTuning ductIntRedTriggerThr=14
set EUtranCellTDD=.* ductIntPerfTuning ductIntRedRecovThr=10
set EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqPwrThr=-105
set EUtranCellTDD=.* ductIntPerfTuning ductIntSlopePwrDiffThr=3
set EUtranCellTDD=.* ductIntPerfTuning ductIntSlopeDetectPeriod=10
set EUtranCellTDD=.* ductIntPerfTuning ductIntSlopeDetectRatioThr=50
set EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqTransThr=10
set ENodeBFunction=1 ductIntCharInfoScheme 0
set ENodeBFunction=1 ductIntFlexibleDetectionEnabled false
set CXC4012256 featureState 1

################# Dyn SCell Selection for CA ###########


set SctpProfile=1 pathMaxRtx 4
set SctpProfile=Node_Internal_F1 pathMaxRtx 4
set SctpProfile=1 assocMaxRtx 8
set SctpProfile=Node_Internal_F1 assocMaxRtx 8
set SctpProfile=1 initRto 2000
set SctpProfile=Node_Internal_F1 initRto 2000
set SctpProfile=1 maxRto 4000
set SctpProfile=Node_Internal_F1 maxRto 4000
set SctpProfile=1 minRto 1000
set SctpProfile=Node_Internal_F1 minRto 1000

############ IFLB ############

set CXC4011373 FeatureState 1
set CXC4011370 FeatureState 1
set EUtranCellTDD=.* cellSubscriptionCapacity 20000
set EUtranCellFDD=AS_E_F3.* cellCapMinCellSubCap 6000
set EUtranCellFDD=AS_E_F8.* cellCapMinCellSubCap 6000
set EUtranCellFDD=AS_E_F1.* cellCapMinCellSubCap 6000
set EUtranCellTDD=AS_E_T.* cellCapMinCellSubCap 5000
set EUtranCell.*=.* cellCapMaxCellSubCap 60000
set EUtranCell.*=.* cellCapMinMaxWriProt true
set EUtranCell.*=.*,EUtranFreqRelation=.*,EUtranCellRelation=40556-.*-.* loadBalancing     1
set EUtranCell.*=.*,EUtranFreqRelation=3663,EUtranCellRelation=40556-.*-.* loadBalancing     0


set SctpProfile=1 pathMaxRtx 4
set SctpProfile=Node_Internal_F1 pathMaxRtx 4
set SctpProfile=1 assocMaxRtx 8
set SctpProfile=Node_Internal_F1 assocMaxRtx 8
set SctpProfile=1 initRto 2000
set SctpProfile=Node_Internal_F1 initRto 2000
set SctpProfile=1 maxRto 4000
set SctpProfile=Node_Internal_F1 maxRto 4000
set SctpProfile=1 minRto 1000
set SctpProfile=Node_Internal_F1 minRto 1000                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                    
#############END######################                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                    
lt all                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                    
wait 5                                                                                                                                                                                                                                                                                                                              
st ^eutrancell                                                                                                                                                                                                                                                                                                                      
ma unlockedcells ^eutrancell.*= administrativestate 1                                                                                                                                                                                                                                                                               
st unlockedcells                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                    
st EUtranCell(FDD|TDD)=                                                                                                                                                                                                                                                                                                             
bl EUtranCell(FDD|TDD)=                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                    
wait 5                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                    
st EUtranCell(FDD|TDD)=                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                    
wait 5                                                                                                                                                                                                                                                                                                                              
deb unlockedcells                                                                                                                                                                                                                                                                                                                   
y                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                    
gs-                                                                                                                                                                                                                                                                                                                                 
confb-                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                    
wait 5                                                                                                                                                                                                                                                                                                                              
st unlockedcells                                                                                                                                                                                                                                                                                                                    
mr unlockedcells                                                                                                                                                                                                                                                                                                                    
st EUtranCell(FDD|TDD)=                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                    
st EUtranCell(FDD|TDD)=                                                                                                                                                                                                                                                                                                             
hget . noOfPucchSrUsers|noOfPucchCqiUsers                                                                                                                                                                                                                                                                                           


get CXC4011958|CXC4011808|CXC4011803|CXC4011378 featurestate

set CXC4011958|CXC4011808|CXC4011803|CXC4011378 featurestate 1
hget . assocMaxRtx|initRto|maxRto|minrto|pathMaxRtx
set . initRto 2000
set . maxRto 4000
set . minrto 1000
set . pathMaxRtx 4
set . assocMaxRtx 8
set Fm=1 heartbeatInterval 100
set SctpProfile=1 heartbeatActivated true
set SctpProfile=1 heartbeatInterval 5000
set SctpProfile=1 initialHeartbeatInterval 500

#######################New LMS Changes###############################

lset CXC4012218 featurestate 1
lset CXC4012371 featurestate 1

set EUtranCellFDD=AS_E_F1.*      qRxLevMin         -124
set EutrancellFDD=AS_E_F1.* SystemInformationBlock3 snonintrasearch=14
set EUtranCellFDD=.*    threshServingLow 14
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=39.*         threshXLow        0
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=3663        threshXLow        14
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=265        threshXLow        0
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=1526        threshXLow        0
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=39.*         threshXHigh        10
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=3663        threshXHigh        0
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=265        threshXHigh        0
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=1526        threshXHigh       16
set EUtranCellFDD=AS_E_F3.*      qRxLevMin         -124
set EutrancellFDD=AS_E_F3.* SystemInformationBlock3 snonintrasearch=14
set EUtranCellFDD=AS_E_F3.*    threshServingLow 14
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=39.*         threshXLow        0
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=3663        threshXLow        14
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=265        threshXLow        16
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=1526        threshXLow        0
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=39.*         threshXHigh        10
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=3663        threshXHigh        0
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=265        threshXHigh        0
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=1526        threshXHigh        0
set EUtranCellFDD=AS_E_F8.*      qRxLevMin         -124
set EutrancellFDD=AS_E_F8.* SystemInformationBlock3 snonintrasearch=0
set EUtranCellFDD=AS_E_F8.*    threshServingLow 0
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=39.*         threshXLow        0
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=1526       threshXLow        0
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=265       threshXLow        0
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=3663       threshXLow        10
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=39.*         threshXHigh        10
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=1526       threshXHigh        10
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=265       threshXHigh        14
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=3663       threshXHigh        0
set EUtranCellTDD=AS_E_T2.*      qRxLevMin         -124
set EutrancellTDD=AS_E_T2.* SystemInformationBlock3 snonintrasearch=8
set EUtranCellTDD=AS_E_T2.*    threshServingLow 8
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=39348         threshXLow        62
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=1526       threshXLow        16
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=265       threshXLow        16
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=3663       threshXLow        62
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=39348         threshXHigh        12
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=1526       threshXHigh        12
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=265       threshXHigh        12
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=3663       threshXHigh        12
set EUtranCellTDD=AS_E_T1.*      qRxLevMin         -124
set EutrancellTDD=AS_E_T1.* SystemInformationBlock3 snonintrasearch=8
set EUtranCellTDD=AS_E_T1.*    threshServingLow 8
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=39150         threshXLow        62
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=1526       threshXLow        16
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=265       threshXLow        16
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=3663       threshXLow        62
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=39.*         threshXHigh        12
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=1526       threshXHigh       12
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=265       threshXHigh        12
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=3663       threshXHigh       12

set EUtranCellTDD=AS_E_T2_.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -114
set EUtranCellTDD=AS_E_T2_.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -114
set EUtranCellTDD=AS_E_T2_.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -112
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=39.* a5Thr1RsrpFreqOffset 2
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=39.* a5Thr2RsrpFreqOffset 66
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=265 a5Thr1RsrpFreqOffset 2
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=265 a5Thr2RsrpFreqOffset 4
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=1526 a5Thr1RsrpFreqOffset 2
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=1526 a5Thr2RsrpFreqOffset 8
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=3663 a5Thr1RsrpFreqOffset 2
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=3663 a5Thr2RsrpFreqOffset 64
set EUtranCellTDD=AS_E_T1_.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -114
set EUtranCellTDD=AS_E_T1_.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -114
set EUtranCellTDD=AS_E_T1_.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -112
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=39.* a5Thr1RsrpFreqOffset 2
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=39.* a5Thr2RsrpFreqOffset 66
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=265 a5Thr1RsrpFreqOffset 2
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=265 a5Thr2RsrpFreqOffset 4
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=1526 a5Thr1RsrpFreqOffset 2
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=1526 a5Thr2RsrpFreqOffset 8
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=3663 a5Thr1RsrpFreqOffset 2
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=3663 a5Thr2RsrpFreqOffset 64
set EUtranCellFDD=AS_E_F1_.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -104
set EUtranCellFDD=AS_E_F1_.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -114
set EUtranCellFDD=AS_E_F1_.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -112
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=39.* a5Thr1RsrpFreqOffset 8
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=39.* a5Thr2RsrpFreqOffset -2
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=265 a5Thr1RsrpFreqOffset 2
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=265 a5Thr2RsrpFreqOffset -2
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=1526 a5Thr1RsrpFreqOffset 2
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=1526 a5Thr2RsrpFreqOffset 2
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=3663 a5Thr1RsrpFreqOffset 8
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=3663 a5Thr2RsrpFreqOffset 65
set EUtranCellFDD=AS_E_F3_.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -100
set EUtranCellFDD=AS_E_F3_.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -114
set EUtranCellFDD=AS_E_F3_.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -112
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=39.* a5Thr1RsrpFreqOffset 12
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=39.* a5Thr2RsrpFreqOffset -2
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=265 a5Thr1RsrpFreqOffset 6
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=265 a5Thr2RsrpFreqOffset -2
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=1526 a5Thr1RsrpFreqOffset 2
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=1526 a5Thr2RsrpFreqOffset -2
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=3663 a5Thr1RsrpFreqOffset 2
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=3663 a5Thr2RsrpFreqOffset 2
set EUtranCellFDD=AS_E_F8_.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -88
set EUtranCellFDD=AS_E_F8_.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -83
set EUtranCellFDD=AS_E_F8_.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -112
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=39.* a5Thr1RsrpFreqOffset -5
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=39.* a5Thr2RsrpFreqOffset -2
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=265 a5Thr1RsrpFreqOffset -15
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=265 a5Thr2RsrpFreqOffset 0
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=1526 a5Thr1RsrpFreqOffset -15
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=1526 a5Thr2RsrpFreqOffset 0	
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=3663 a5Thr1RsrpFreqOffset -23
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=3663 a5Thr2RsrpFreqOffset 0

set EUtranCellTDD=AS_E_T2_.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrpQciOffset=66
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=39.* eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=66,a5Thr2RsrpFreqQciOffset=0
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=265 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=64,a5Thr2RsrpFreqQciOffset=-2
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=1526 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=64,a5Thr2RsrpFreqQciOffset=-2
set EUtranCellTDD=AS_E_T2.*,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=64,a5Thr2RsrpFreqQciOffset=-68
set EUtranCellTDD=AS_E_T1_.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrpQciOffset=66
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=39.* eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=66,a5Thr2RsrpFreqQciOffset=0
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=265 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=66,a5Thr2RsrpFreqQciOffset=-2
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=1526 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=66,a5Thr2RsrpFreqQciOffset=-2
set EUtranCellTDD=AS_E_T1.*,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=66,a5Thr2RsrpFreqQciOffset=-68
set EUtranCellFDD=AS_E_F1_.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrpQciOffset=4
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=39.* eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-8,a5Thr2RsrpFreqQciOffset=-8
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=265 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-2,a5Thr2RsrpFreqQciOffset=0
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=1526 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=0
set EUtranCellFDD=AS_E_F1.*,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=-4
set EUtranCellFDD=AS_E_F3_.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrpQciOffset=2
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=39.* eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-12,a5Thr2RsrpFreqQciOffset=66
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=265 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=0
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=1526 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-2,a5Thr2RsrpFreqQciOffset=0
set EUtranCellFDD=AS_E_F3.*,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=0
set EUtranCellFDD=AS_E_F8_.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a1a2ThrRsrpQciOffset=2
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=39.* eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-26,a5Thr2RsrpFreqQciOffset=70
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=265 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-12,a5Thr2RsrpFreqQciOffset=12
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=1526 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=-12,a5Thr2RsrpFreqQciOffset=8
set EUtranCellFDD=AS_E_F8.*,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,a5Thr1RsrpFreqQciOffset=8,a5Thr2RsrpFreqQciOffset=0
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=39.* voicePrio         -1
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=265.* voicePrio         4
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=1526.* voicePrio         6
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=3663.* voicePrio         3
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=39.* voicePrio         -1
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=265.* voicePrio         4
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=1526.* voicePrio         6
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=3663.* voicePrio         3
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=39.* voicePrio         -1
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=265.* voicePrio         3
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=1526.* voicePrio         4
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=3663.* voicePrio         6
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=39.* voicePrio         -1
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=265.* voicePrio         4
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=1526.* voicePrio         5
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=3663.* voicePrio         3
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=39.* voicePrio         -1
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=265.* voicePrio         4
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=1526.* voicePrio         5
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=3663.* voicePrio         3
Set EUtranCellFDD=AS_E_F1_.*                     cellSubscriptionCapacity 15000
Set EUtranCellFDD=AS_E_F3_.*                    cellSubscriptionCapacity 10000
Set EUtranCellFDD=AS_E_F8_.*                     cellSubscriptionCapacity 2500
Set EUtranCellTDD=AS_E_T2_.*                    cellSubscriptionCapacity 60000
Set EUtranCellTDD=AS_E_T1_.*                    cellSubscriptionCapacity 60000
Set EUtranCellFDD=AS_E_F1_.*                     cellCapMinCellSubCap 6000
Set EUtranCellFDD=AS_E_F3_.*                    cellCapMinCellSubCap 6000
Set EUtranCellFDD=AS_E_F8_.*                     cellCapMinCellSubCap 6000
Set EUtranCellTDD=AS_E_T2_.*                    cellCapMinCellSubCap 3000
Set EUtranCellTDD=AS_E_T1_.*                    cellCapMinCellSubCap 3000
set AutoCellCapEstFunction=1                                useEstimatedCellCap false
lset CXC4012687 featurestate 1
lset CXC4012344 featurestate 1

set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=265 connectedModeMobilityPrio 3
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=1526 connectedModeMobilityPrio 4
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=3663 connectedModeMobilityPrio 2
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=39.* connectedModeMobilityPrio 6
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=265 connectedModeMobilityPrio 3
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=1526 connectedModeMobilityPrio 4
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=3663 connectedModeMobilityPrio 2
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=39.* connectedModeMobilityPrio 6
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=265 connectedModeMobilityPrio 3
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=1526 connectedModeMobilityPrio 4
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=3663 connectedModeMobilityPrio 2
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=39.* connectedModeMobilityPrio 6
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=39.* connectedModeMobilityPrio 6
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=265 connectedModeMobilityPrio 4
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=1526 connectedModeMobilityPrio 3
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=3663 connectedModeMobilityPrio -1
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=39.* connectedModeMobilityPrio 6
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=265 connectedModeMobilityPrio 4
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=1526 connectedModeMobilityPrio 3
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=3663 connectedModeMobilityPrio -1

set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=265 endcHoFreqPriority 6
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=1526 endcHoFreqPriority 7
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=3663 endcHoFreqPriority -1
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=39.* endcHoFreqPriority -1
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=265 endcHoFreqPriority 6
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=1526 endcHoFreqPriority 7
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=3663 endcHoFreqPriority -1
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=39.* endcHoFreqPriority -1
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=265 endcHoFreqPriority 6
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=1526 endcHoFreqPriority 7
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=3663 endcHoFreqPriority -1
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=39.* endcHoFreqPriority -1
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=39.* endcHoFreqPriority -1
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=265 endcHoFreqPriority 6
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=1526 endcHoFreqPriority 7
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=3663 endcHoFreqPriority -1
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=39.* endcHoFreqPriority -1
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=265 endcHoFreqPriority 6
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=1526 endcHoFreqPriority 7
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=3663 endcHoFreqPriority -1

set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=265 cellreselectionpriority 3
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=1526 cellreselectionpriority 4
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=3663 cellreselectionpriority 2
set EUtranCellFDD=AS_E_F1_.*,EUtranFreqRelation=39.* cellreselectionpriority 6
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=265 cellreselectionpriority 3
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=1526 cellreselectionpriority 4
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=3663 cellreselectionpriority 2
set EUtranCellFDD=AS_E_F3_.*,EUtranFreqRelation=39.* cellreselectionpriority 6
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=265 cellreselectionpriority 3
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=1526 cellreselectionpriority 4
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=3663 cellreselectionpriority 2
set EUtranCellFDD=AS_E_F8_.*,EUtranFreqRelation=39.* cellreselectionpriority 6
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=39.* cellreselectionpriority 6
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=265 cellreselectionpriority 4
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=1526 cellreselectionpriority 3
set EUtranCellTDD=AS_E_T2_.*,EUtranFreqRelation=3663 cellreselectionpriority -1
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=39.* cellreselectionpriority 6
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=265 cellreselectionpriority 4
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=1526 cellreselectionpriority 3
set EUtranCellTDD=AS_E_T1_.*,EUtranFreqRelation=3663 cellreselectionpriority -1

gs-
confb-


confbd+
crn ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30
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
dscpArpMap                           dscpArp1=-1,dscpArp10=-1,dscpArp11=-1,dscpArp12=-1,dscpArp13=-1,dscpArp14=-1,dscpArp15=-1,dscpArp2=-1,dscpArp3=-1,dscpArp4=-1,dscpArp5=-1,dscpArp6=-1,dscpArp7=-1,dscpArp8=-1,dscpArp9=-1
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
measReportConfigParams               a1ThresholdRsrpPrimOffset=0,a1ThresholdRsrpSecOffset=0,a1ThresholdRsrqPrimOffset=0,a1ThresholdRsrqSecOffset=0,a2ThresholdRsrpPrimOffset=0,a2ThresholdRsrpSecOffset=0,a2ThresholdRsrqPrimOffset=0,a2ThresholdRsrqSecOffset=0,a3InterOffsetAdjustmentRsrp=0,a3InterOffsetAdjustmentRsrq=0,a3IntraOffsetAdjustmentRsrp=0,a3IntraOffsetAdjustmentRsrq=0,a5Threshold1RsrpOffset=0,a5Threshold1RsrqOffset=0,a5Threshold2RsrpOffset=0,a5Threshold2RsrqOffset=0,b2Threshold1RsrpCdma2000Offset=0,b2Threshold1RsrpGeranOffset=0,b2Threshold1RsrpUtraOffset=0,b2Threshold1RsrqCdma2000Offset=0,b2Threshold1RsrqGeranOffset=0,b2Threshold1RsrqUtraOffset=0,b2Threshold2Cdma2000Offset=0,b2Threshold2EcNoUtraOffset=0,b2Threshold2GeranOffset=0,b2Threshold2RscpUtraOffset=0,offsetPerQciPrio=0,timeToTriggerInterA3=-1,timeToTriggerInterA3Rsrq=-1,timeToTriggerIntraA3=-1
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
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         300
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
userLabel
end


crn ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
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
dscpArpMap                           dscpArp1=-1,dscpArp10=-1,dscpArp11=-1,dscpArp12=-1,dscpArp13=-1,dscpArp14=-1,dscpArp15=-1,dscpArp2=-1,dscpArp3=-1,dscpArp4=-1,dscpArp5=-1,dscpArp6=-1,dscpArp7=-1,dscpArp8=-1,dscpArp9=-1
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
measReportConfigParams               a1ThresholdRsrpPrimOffset=0,a1ThresholdRsrpSecOffset=0,a1ThresholdRsrqPrimOffset=0,a1ThresholdRsrqSecOffset=0,a2ThresholdRsrpPrimOffset=0,a2ThresholdRsrpSecOffset=0,a2ThresholdRsrqPrimOffset=0,a2ThresholdRsrqSecOffset=0,a3InterOffsetAdjustmentRsrp=0,a3InterOffsetAdjustmentRsrq=0,a3IntraOffsetAdjustmentRsrp=0,a3IntraOffsetAdjustmentRsrq=0,a5Threshold1RsrpOffset=0,a5Threshold1RsrqOffset=0,a5Threshold2RsrpOffset=0,a5Threshold2RsrqOffset=0,b2Threshold1RsrpCdma2000Offset=0,b2Threshold1RsrpGeranOffset=0,b2Threshold1RsrpUtraOffset=0,b2Threshold1RsrqCdma2000Offset=0,b2Threshold1RsrqGeranOffset=0,b2Threshold1RsrqUtraOffset=0,b2Threshold2Cdma2000Offset=0,b2Threshold2EcNoUtraOffset=0,b2Threshold2GeranOffset=0,b2Threshold2RscpUtraOffset=0,offsetPerQciPrio=0,timeToTriggerInterA3=-1,timeToTriggerInterA3Rsrq=-1,timeToTriggerIntraA3=-1
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
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         0
userLabel
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end

crn ENodeBFunction=1,SubscriberGroupProfile=ENDC
bearerTriggerList                    
caRateAdjustCoeff                    -1
cellTriggerList                      
customTriggerList                    0
customTriggerType                    2
dlAiLaDeltaSinrMax                   30
dlDynBlerTargetAlg                   0
dlDynBlerTargetMax                   -1
dlDynBlerTargetMin                   1
dlHarqBlerTarget                     10
drxMode                              0
endcUserProfileRef
fastACqiReportEnabled                false
featuresToDisableMeas                
groupExtendInactAfterVolteRel        0
higherPriorityEnabled                false
iuaMode                              0
iuaProfileRef
lastSchedLinkAdaptMode               0
pZeroNominalPucchOffset              0
pZeroNominalPuschOffset              0
pdcchFlexibleBlerMode                0
preschedProfileRef
preschedulingMode                    0
profilePriority                      5
qciOffsetForQCI6                     0
qciOffsetForQCI7                     0
qciOffsetForQCI8                     0
qciOffsetForQCI9                     0
sCellScheduleSinrThresOffset         0
selectionProbability                 100
spidTriggerList                      
subGroupConfiguration1               
subGroupConfiguration2               
subGroupConfiguration3               
subGroupConfiguration4               
subGroupConfiguration5               
subGroupConfiguration6               
subGroupConfiguration7               
ulCandidateToRegion                  false
ulHarqBlerTarget                     10
ulMcsLowerLimit                      -1
ulMcsUpperLimit                      -1
ulOuterloopStepSizeFactor            10
ulPlThresToRegion                    500
ulSinrThresToRegion                  400
userLabel
volteCodecRateForUlSinrEst           -1
end
confbd-



confbd+
set EUtranCell.*DD=.* endcAllowedPlmnList  mcc=405,mnc=56,mncLength=2
set ENodeBFunction=1                                        s1GtpuEchoEnable  1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          anrStateNR        1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength    26
Set ENodeBFunction=1                                        endcX2IpAddrViaS1Active true
set ENodeBFunction=1                                        endcAllowed       true
set ENodeBFunction=1                                        endcAwareMfbiIntraCellHo false
set ENodeBFunction=1                                        endcDataUsageReportEnabled true
set ENodeBFunction=1                                        endcIntraBandBlocked true
set ENodeBFunction=1                                        endcPowerOffsetLte 3
set ENodeBFunction=1                                        endcS1OverlapMode true
set ENodeBFunction=1                                        endcSplitAllowedMoVoice false
set ENodeBFunction=1                                        endcSplitAllowedNonDynPwrShUe false

set ENodeBFunction=1                                        endcOverheatingAssistance true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          endcRachFailThrPerUe 5
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          scgSessTimeForEndcRachFail 2500
set PmFlexCounterFilter=ENDC                                endcFilterMin     2



set ENodeBFunction=1,EndcProfile=1 meNbS1TermReqArpLev 0                                                                                                          
set ENodeBFunction=1,EndcProfile=1 splitNotAllowedUeArpLev 0 
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6789]$ endcProfileRef ENodeBFunction=1,EndcProfile=1
confbd-

confbd+
cr ENodeBFunction=1,UePolicyOptimization=1 
                                                                                                                       
set ENodeBFunction=1,UePolicyOptimization=1 ueCapPrioList 0                                                                                                       
set ENodeBFunction=1,UePolicyOptimization=1 coverageAwareImc true 
set UePolicyOptimization=1                                  endcAwareImc      2
set EUtranCell.*DD=.*                    endcB1MeasGapEnabled true
set EUtranCell.*DD=.*                      endcB1MeasGapConfig 0
set EUtranCell.*DD=.*                      endcSetupUlBsVolThr 5
set EUtranCell.*DD=.*                      loopingEndcBackoffDuration 200
set EUtranCell.*D=.*                      loopingEndcProtectionEnabled true
set EUtranCell>8DD=.*                      loopingEndcShortScgSessTime 3000


crn ENodeBFunction=1,EndcProfile=1
meNbS1TermReqArpLev                  0
splitNotAllowedUeArpLev              0
userLabel
end

crn ENodeBFunction=1,EndcProfile=2
meNbS1TermReqArpLev                  15
splitNotAllowedUeArpLev              0
userLabel
end

set QciTable=default,QciProfilePredefined=qci5              endcProfileRef    EndcProfile=2
set QciTable=default,QciProfilePredefined=qci6$             endcProfileRef    EndcProfile=1
set QciTable=default,QciProfilePredefined=qci7$             endcProfileRef    EndcProfile=1
set QciTable=default,QciProfilePredefined=qci8              endcProfileRef    EndcProfile=1
set QciTable=default,QciProfilePredefined=qci9              endcProfileRef    EndcProfile=1


$date = `date +%y%m%d_%H%M`                                                                                                                                       
cvms Post_GPL_$date                                                                                                                                      
confbd-                                                                                                                                                           
gs-                                                                                                                                              
                                                                                                                                            

"""


AS_TN_RN_GPS_MME_SCRIPT = """
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
eNodeBPlmnId mcc=405,mnc=56,mncLength=2
alignTtiBundWUlTrigSinr 1
dscpLabel 46
eNBId {eNBId}
gtpuErrorIndicationDscp 46
measuringEcgiWithAgActive false
rrcConnReestActive true
s1GtpuEchoDscp 46
sctpRef Transport=1,SctpEndpoint=1
timeAndPhaseSynchAlignment true
tRelocOverall 5
tS1HoCancelTimer 3
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

crn ENodeBFunction=1,TermPointToMme=MME_NEW1
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.61.126.218
ipAddress2 10.61.126.219
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

crn ENodeBFunction=1,TermPointToMme=MME_JHRT
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.50.47.171
ipAddress2 10.50.47.172
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

crn ENodeBFunction=1,TermPointToMme=MME_2
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.50.46.171
ipAddress2 10.50.46.172
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

crn ENodeBFunction=1,TermPointToMme=AS_MMENEW4
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 10.1.169.224
ipAddress2 10.1.169.225
ipv6Address1 ::
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
end

"""




################################################################################### 5G SCRIPS FOR INTEGRATION SCRIPTS ###################################################################################
AS_5G_Cell_creation_Sctp_Endpoint_Creation = """
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


###########################################GNBCUUPFunction=1#############################################################################

crn GNBCUUPFunction=1
altDepHServAdapUPProfEnabled false
dataFwdRateTo5Gs 5000
dataFwdRateToEps 200
dcDlAggActTime 1
dcDlAggExpiryTimer 100
dcDlPdcpInitialMcgRate 20
dcDlPdcpInitialScgRate 100
dlPdcpSpsTargetTimeLTE 25
dlPdcpSpsTargetTimeNR 25
endcDataUsageReportEnabled true
endcDlNrRetProhibTimer 400
endcUlNrRetProhibTimer 1000
estimatedUeL2Buffer
gNBId {gNBId}
gNBIdLength 26
pLMNIdList mcc=405,mnc=56
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
altDepHMultCGPeriodEnabled false
altDepHServAdapUPProfEnabled false
autoLockDelay 0
caVlanPortRef
capacityAllocationPolicy 0
configuredGrantConfMode 0
dlBbCapacityTarget
dynTACConfigEnabled false
esiSuetEnabled false
gNBDUId 1
gNBDUName
gNBId {gNBId}
gNBIdLength 26
mixedSrsModeEnabled false
multiTddPatternSmEnabled false
pimCancAutoConfigEnabled false
pwsEtwsPrimaryInd 8
servAdapUPProfDepHEnabled true
userLabel
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


{AS_CGSWITCH_SCRIPT}

############################GNBCUCPFunction=1####################################################


crn GNBCUCPFunction=1
advUePosPeriodicityMode 0
caDepHEnabled true
cellRelationMOThresh 1500
dnsLookup5GsTaiPeriodicTimer 0
dnsLookupOn5GsTai false
extEnbRemoveTime 1440
extendedBandN77Supported false
extendedBandN77TwoSupported false
gNBCUName
gNBId {gNBId}
gNBIdLength 26
maxCommonProcTime 30
maxNgRetryTime 30
nasInactivityTime 5
networkIdInUeCapEnq false
ngcDedProcTime 5
nrNeedForGapsSupported true
pLMNId mcc=405,mnc=56
pimAutoDetectionEnabled false
prefInterGnbHo 0
ranNodeName
resourceStatusReportDefault -2
resourceStatusReportF1Enabled true
rfspSpidPairList
ribTmAutoMax 0
rrcReestSupportType 0
tDcOverall 7
tXnDcOverall 5
tXnDcPrep 5
userLabel
xnIpAddrViaNgActive true
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

{AS_GNBCUCPFunction}

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

{AS_GNBDUFunction}

"""

AS_Termpoint_GUtranFreqRelation_script = """
###########################Termpoint & FreqRelation################################


lt all

get GNBCUUPFunction=1  gNBId$ > $gnbid                                                                                       

get Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR ^address$ > $reqip                                                                                             


crn ENodeBFunction=1,GUtraNetwork=1                                                                                                                               
userLabel                                                                                                                                                         
end                                                                                                                                                               


crn ENodeBFunction=1,GUtraNetwork=1,GUtranSyncSignalFrequency=629952-30                                                                                                                                                                
arfcn 629952                                                                                                                                                                                                                           
band 78                                                                                                                                                                                                                                
smtcDuration 1                                                                                                                                                                                                                         
smtcOffset 0                                                                                                                                                                                                                           
smtcPeriodicity 20                                                                                                                                                                                                                     
smtcScs 30                                                                                                                                                                                                                             
userLabel                                                                                                                                                                                                                              
end                                                                                                                                                                                                                                    


crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40556-000000$gnbid                                                                                           
dirDataPathAvail true                                                                                                                                             
eNBVlanPortRef                                                                                                                                                    
gNodeBId $gnbid                                                                                                                                                   
gNodeBIdLength 26                                                                                                                                                 
gNodeBPlmnId mcc=405,mnc=56,mncLength=2                                                                                                                          
userLabel                                                                                                                                                         
end                                                                                                                                                               

crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40556-000000$gnbid,TermPointToGNB=40556-000000$gnbid                                                               
additionalCnRef                                                                                                                                                   
administrativeState 0                                                                                                                                             
domainName                                                                                                                                                        
ipAddress 0.0.0.0                                                                                                                                                 
ipAddress2                                                                                                                                                        
ipsecEpAddress ::                                                                                                                                                 
ipv6Address   $reqip                                                                                                                                            
ipv6Address2                                                                                                                                                      
upIpAddress ::                                                                                                                                                    
end    

set enodebfunction=1 upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
set ENodeBFunction=1 sctpEndcX2Ref Transport=1,SctpEndpoint=X2_ENDC                                                                                                                                                           

deb TermPointToGNB                                                                                                                                                


lt all

wait 5

lt all



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
pr GUtraNetwork=1,ExternalGNodeBFunction=40556-000000$gnbid,ExternalGUtranCell=40556-000000$gnbid-31$j                                                                  
if $nr_of_mos = 1                                                                                                                                                 
crn ENodeBFunction=1,$mordn,GUtranFreqRelation=629952,GUtranCellRelation=40556-000000$gnbid-31$j                                                                  
essEnabled false                                                                                                                                                  
isRemoveAllowed false                                                                                                                                             
neighborCellRef GUtraNetwork=1,ExternalGNodeBFunction=40556-000000$gnbid,ExternalGUtranCell=40556-000000$gnbid-31$j                                                     
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

"""


AS_NR_GPL_LMS_SCRIPT = """
lt all     	                                                                                                                                                       
rbs                                                                                                                                                        
rbs                                                                                                                                                               
confbd+                                                                                                                                                           
                                                                                                                                                                  
$date = `date +%y%m%d_%H%M`                                                                                                                                       
cvms Pre_5G_GPL_$date                                                                                                                                         
                                

                                                                        
confbd+
gs+

set GNBDUFunction=1                                         endpointResourceRef GNBDUFunction=1,EndpointResource=1
set GNBCUUPFunction=1                                         endpointResourceRef GNBCUUPFunction=1,EndpointResource=1
set GNBCUCPFunction=1                                         endpointResourceRef GNBCUCPFunction=1,EndpointResource=1

set GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=3 sctpEndpointRef   SctpEndpoint=F1_NRCUCP
set GNBDUFunction=1,EndpointResource=1,LocalSctpEndpoint=1  sctpEndpointRef   SctpEndpoint=F1_NRDU
set GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=1 sctpEndpointRef   SctpEndpoint=NG
set GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=2 sctpEndpointRef   SctpEndpoint=X2



crn GNBCUUPFunction=1,EndpointResource=1,LocalIpEndpoint=1
addressRef                           Transport=1,Router=LTE_NR,InterfaceIPv6=NR,AddressIPv6=NR_S1U_OAM
interfaceList                        4 5 7 6
mode                                 0
end


crn GNBCUCPFunction=1,IntraFreqMC=1
end





crn GNBDUFunction=1,MassiveMimoSleep=1
end

crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1
end

crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepProfile=1
sleepMode                            0
switchDownMonitorDurTimer            60
switchDownMonitorDurTimerEco         300
switchDownPrbThreshDl                10
switchDownPrbThreshDlEco             15
switchDownPrbThreshUlEco             10
switchDownRrcConnThresh              10
switchDownRrcConnThreshEco           30
switchUpMonitorDurTimer              30
switchUpMonitorDurTimerEco           120
switchUpPrbThreshDl                  20
switchUpPrbThreshDlEco               30
switchUpPrbThreshUlEco               15
switchUpRrcConnThresh                20
switchUpRrcConnThreshEco             50
end

crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1,MMimoSleepTimeWindow=1
dayOfWeek                            0
mMimoSleepProfileRef                 MassiveMimoSleep=1,MMimoSleepProfile=1
startTime                            20:30
stopTime                             23:30
end


set GNBDUFunction=1,NRSectorCarrier=.* mMimoSleepTimeGroupRef               MassiveMimoSleep=1,MMimoSleepTimeGroup=1



crn GNBCUCPFunction=1,AnrFunction=1
removeEnbTime                        7
removeFreqRelTime                    15
removeGnbTime                        7
removeNrelTime                       7
end

crn GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1
anrAutoCreateXnForEndc               true
anrCgiMeasInterFreqMode              1
anrCgiMeasIntraFreqEnabled           true
anrEndcX2Enabled                     true
end


crn GNBCUCPFunction=1,Mcpc=1,McpcPSCellProfile=Default
ueConfGroupType                      0
userLabel
end

crn GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=Default
ueConfGroupType                      0
userLabel
end


crn GNBCUCPFunction=1,UeMC=1,UeMCNrFreqRelProfile=Midband
ueConfGroupType                      0
userLabel
end


crn ENodeBFunction=1,EndcProfile=1
meNbS1TermReqArpLev                  0
splitNotAllowedUeArpLev              0
userLabel
end

crn ENodeBFunction=1,EndcProfile=2
meNbS1TermReqArpLev                  15
splitNotAllowedUeArpLev              0
userLabel
end

set QciTable=default,QciProfilePredefined=qci5              endcProfileRef    EndcProfile=2
set QciTable=default,QciProfilePredefined=qci6$             endcProfileRef    EndcProfile=1
set QciTable=default,QciProfilePredefined=qci7$             endcProfileRef    EndcProfile=1
set QciTable=default,QciProfilePredefined=qci8              endcProfileRef    EndcProfile=1
set QciTable=default,QciProfilePredefined=qci9              endcProfileRef    EndcProfile=1




crn ENodeBFunction=1,PmFlexCounterFilter=ENDC
arpFilterEnabled                     false
arpFilterMax                         0
arpFilterMin                         0
ceLevelFilterEnabled                 false
ceLevelFilterMax                     0
ceLevelFilterMin                     0
endcFilterEnabled                    true
lcgFilterEnabled                     false
pciFilterEnabled                     false
plmnFilterEnabled                    false
pviFilterEnabled                     false
qciFilterEnabled                     false
reportAppCounterOnly                 true
spidFilterEnabled                    false
spidFilterMax                        1
spidFilterMin                        1
subscriberGroupFilterEnabled         false
subscriberGroupFilterMax             0
subscriberGroupFilterMin             0
ueCatFilterEnabled                   false
ueCatFilterMax                       0
ueCatFilterMin                       0
uePowerClassFilterEnabled            false
uePowerClassFilterMax                1
uePowerClassFilterMin                1
end

crn ENodeBFunction=1,UePolicyOptimization=1
coverageAwareImc                     true
endcAwareImc                         2
t320                                 180
ueCapPrioList                        0
zzzTemporary1                        1
zzzTemporary2                        -2000000000
zzzTemporary3                        -2000000000
end


crn GNBCUUPFunction=1,GtpuSupervision=1
end


crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=S1
endpointResourceRef                  
gtpuEchoDscp                         32
gtpuEchoEnabled                      true
interfaceList                        5
userLabel
end


crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=X2
endpointResourceRef                  
gtpuEchoDscp                         32
gtpuEchoEnabled                      true
interfaceList                        7
userLabel
end


set QosProfiles=1,DscpPcpMap=1  pcp0
set QosProfiles=1,DscpPcpMap=1  pcp1
set QosProfiles=1,DscpPcpMap=1  pcp2
set QosProfiles=1,DscpPcpMap=1  pcp3
set QosProfiles=1,DscpPcpMap=1  pcp4
set QosProfiles=1,DscpPcpMap=1  pcp5
set QosProfiles=1,DscpPcpMap=1  pcp6
set QosProfiles=1,DscpPcpMap=1  pcp7
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22 24 26
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6 8 10 30 32
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12 14 40
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4 28
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16 18 34 42 44
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20 46

set QosProfiles=1,DscpPcpMap=1    pcp7   20 46                                                                       
set QosProfiles=1,DscpPcpMap=1    pcp6   16 18 34 42 44                                                              
set QosProfiles=1,DscpPcpMap=1    pcp5   4 28                                                                        
set QosProfiles=1,DscpPcpMap=1    pcp4   12 14 40                                                                    
set QosProfiles=1,DscpPcpMap=1    pcp3   6 8 10 30 32                                                                
set QosProfiles=1,DscpPcpMap=1    pcp2   22 24 26                                                                    
set QosProfiles=1,DscpPcpMap=1    pcp0   0 1 2 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 36 37 38 39 41 43 45 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63




set ENodeBFunction=1                                        zzzTemporary81    1                                                                                  
set UePolicyOptimization=1                                  zzzTemporary1     1                                                                                  
set EndcProfile=1                                           splitNotAllowedUeArpLev 0                                                                            
set EndcProfile=2                                           meNbS1TermReqArpLev 15                                                                               
set EUtranCellFDD=.*                      measGapPattEndc   1                                                                                  
set EUtranCellFDD=.*,UeMeasControl=1      maxMeasB1Endc     3                                                                                  
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength    26                                                                                 
set ENodeBFunction=1                                        endcS1OverlapMode true      
set EUtranCellFDD=.*,UeMeasControl=1      endcMeasTime      2000                                                                               
set EUtranCellFDD=.*,UeMeasControl=1      endcMeasRestartTime 10000                                                                            
set ENodeBFunction=1                                        endcDataUsageReportEnabled true                                                                      
set EUtranCellFDD=.*,UeMeasControl=1      endcB1MeasWindow  40                                                                                 
set QciTable=default,QciProfilePredefined=qci1              dscp              34                                                                                 
set QciTable=default,QciProfilePredefined=qci2              dscp              34                                                                                 
set QciTable=default,QciProfilePredefined=qci3              dscp              26                                                                                 
set QciTable=default,QciProfilePredefined=qci4              dscp              26                                                                                 
set QciTable=default,QciProfilePredefined=qci5              dscp              46                                                                                 
set QciTable=default,QciProfilePredefined=qci6$             dscp              32    
set QciTable=default,QciProfilePredefined=qci7$             dscp              40   
set QciTable=default,QciProfilePredefined=qci8              dscp              30                                                                                 
set QciTable=default,QciProfilePredefined=qci9              dscp              26                                                                                 
set CarrierAggregationFunction=1                            dcSCellDeactDelayTimer 200                                                                           
set CarrierAggregationFunction=1                            dcSCellActDeactDataThresHyst 30                                                                      
set CarrierAggregationFunction=1                            dcSCellActDeactDataThres 30                                                                          
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          anrStateNR        1                           
set EUtranCellFDD=.*,GUtranFreqRelation=629952 anrMeasOn         true                                                                          
set ENodeBFunction=1                                        x2retryTimerMaxAuto 1440                                                                             
set CarrierAggregationFunction=1                            endcCaPolicy      1                                                  


set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 ulMaxRetxThreshold 32                                                                              
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 ulMaxRetxThreshold 32                                                                              
set NRCellDU=.*                   ul256QamEnabled   true   
set GNBDUFunction=1,UeCC=1,RadioLinkControl=1,DrbRlc=Default,DrbRlcUeCfg=Base tStatusProhibitUl 10                                                               
set NRCellDU=.*                   trsPowerBoosting  0                                                                                  
set NRCellDU=.*                   trsPeriodicity    20                                                                                 
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitUl 80                                                                               
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitUl 80                                                                               
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitDl 80                                                                               
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitDl 80                                                                               
set GNBCUCPFunction=1,UeCC=1,InactivityProfile=Default,InactivityProfileUeCfg=Base tInactivityTimerEndcSn 5                                                      
set NRCellDU=.*                   tddUlDlPattern    1                                               
set NRCellDU=.*                   tddSpecialSlotPattern 3                                     
set GNBCUCPFunction=1                                       tDcOverall        11                                                                                 
set GNBDUFunction=1,Rrc=1                                   t319              400  
set GNBDUFunction=1,Rrc=1                                   t311              3000                                                                               
set GNBDUFunction=1,Rrc=1                                   t310              2000                                                                               
set GNBDUFunction=1,Rrc=1                                   t304              2000                                                                               
set GNBDUFunction=1,Rrc=1                                   t301              600                                                                                
set GNBDUFunction=1,Rrc=1                                   t300              1500                                                                               
set NRCellDU=.*                   subCarrierSpacing 30                                                                                 
set NRCellDU=.*                   ssbSubCarrierSpacing 30                                                                              
set NRCellDU=.*                   ssbPowerBoost     6                                                                                  
set NRCellDU=.*                   ssbPeriodicity    20                                                                                 
set NRCellDU=.*                   ssbOffset         0        
set NRCellDU=.*                   ssbDuration       1                                                                                  
set NRCellDU=.*                   srsPeriodicity    40                                                                                 
set NRCellDU=.*                   srsHoppingBandwidth 0                                                                         
set NRCellDU=.*                   secondaryCellOnly false                                                                              
set GNBCUCPFunction=1,AnrFunction=1                         removeNrelTime    7                                                                                                                           
set GNBCUCPFunction=1,AnrFunction=1                         removeGnbTime     7                                                                                  
set GNBCUCPFunction=1,AnrFunction=1                         removeEnbTime     7                                                                                  
set NRCellDU=.*                   rachPreambleTransMax 10                                                                              
set NRCellDU=.*                   rachPreambleRecTargetPower -110                                                                      
set NRCellDU=.*                   rachPreambleFormat 0                                        
set NRCellDU=.*                   pZeroUePuschOffset256Qam 4                                                                           
set NRCellDU=.*                   pZeroNomSrs       -110                                                                               
set NRCellDU=.*                   pZeroNomPuschGrant 1000                                                                              
set NRCellDU=.*                   pZeroNomPucch     -114                                                                               
set NRCellDU=.*                   puschStartPrbStrategy 3                                         
set NRCellDU=.*                   puschAllowedInDmrsSym true                                                                           
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingUeMode 1                                                    
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingDuration 100                                                                     
set NRCellDU=.*                   pMax              26                                                                                 
set NRCellDU=.*                   pdschStartPrbStrategy 3                                         
set NRCellDU=.*                   pdcchSymbConfig   0                                                                     
set NRCellDU=.*                   nrSrsDlPacketAgeThr 0                                                                                
set GNBDUFunction=1,Rrc=1                                   n311              1                                                                                  
set GNBDUFunction=1,Rrc=1                                   n310              20                                                                                 
set NRCellDU=.*                   maxUeSpeed        2                                                   
set NRCellDU=.*                   maxNoOfAdvancedDlMuMimoLayers 8                                                                      
set QciProfileEndcConfigExt=1                               initialUplinkConf 1   




                                                        
set GtpuSupervision=1,GtpuSupervisionProfile=S1             gtpuEchoEnabled   true                                                                               
set GtpuSupervision=1,GtpuSupervisionProfile=X2             gtpuEchoEnabled   true                                                                               
set GtpuSupervision=1,GtpuSupervisionProfile=S1             gtpuEchoDscp      32                                                                                 
set GtpuSupervision=1,GtpuSupervisionProfile=X2             gtpuEchoDscp      32                                                                                 
set GNBCUUPFunction=1,UeCC=1,AqmCfg=           estimatedE2ERTT   50                                                                                                                                                           
set ENodeBFunction=1                                        endcDataUsageReportEnabled true                                                                      
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base endcActionEvalFail 1                                             
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxRetransmissionTimerUl 8  
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxRetransmissionTimerDl 8                                                                    
set NRCellDU=.*                   drxProfileEnabled true                                                                               
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxOnDurationTimer 39
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxLongCycle      10                                               
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxInactivityTimer 15
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxEnabled        true                                                                        
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 dlMaxRetxThreshold 32                                                                              
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 dlMaxRetxThreshold 32                                                                              
set NRCellDU=.*                   dlDmrsMuxSinrThresh -10                                                                              
set NRCellDU=.*                   dl256QamEnabled   true                                                                               
set NRCellDU=.*                   dftSOfdmPuschEnabled true                                                                            
set NRCellDU=.*                   dftSOfdmMsg3Enabled true                                                                             
set GNBCUUPFunction=1                                       dcDlPdcpInitialScgRate 100               
set NRCellDU=.*                   csiRsShiftingSecondary 1                                         
set NRCellDU=.*                   csiRsShiftingPrimary 1                                 
set NRCellDU=.*                   csiRsPeriodicity  40                                                                                 
set NRCellDU=.*                   csiRsConfig8P     csiRsControl8Ports=1,i11Restriction=FFFF,i12Restriction=                                                                         
set NRCellDU=.*                   csiRsConfig32P    csiRsControl32Ports=1,i11Restriction=FFFFFFFF,i12Restriction=FF                                                                        
set NRCellDU=.*                   csiRsActivePortConfig 2 4                   
set NRSectorCarrier=.*                                 configuredMaxTxPower 200000                                                                          
                                                                              
set NRSectorCarrier=.*,CommonBeamforming=1              cbfMacroTaperType 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          anrStateNR        1                           
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1         anrEndcX2Enabled  true                                                                               
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1         anrCgiMeasIntraFreqEnabled true                                                                      
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1         anrAutoCreateXnForEndc true                                                                          
set NRCellDU=.*                   advancedDlSuMimoEnabled true                                                                         
set NRCellDU=.*                   additionalPucchForCaEnabled false                                                                    
set NRCellDU=.*                   ulMaxMuMimoLayers 4                                                                                  
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingDataSize 86                                                                      
set NRCellDU=.*                   pdschAllowedInDmrsSym true                                                                           
set NRSectorCarrier=.*                                  nRMicroSleepTxEnabled true                                                                           
set NRCellDU=.*                   maxUsersRachSchedPusch 100                                                                           
set NRCellDU=.*                   dlMaxMuMimoLayers 8                                                                                  
set NRCellDU=.*                   csiRsConfig4P     csiRsControl4Ports=OFF,i11Restriction=,i12Restriction=        
set NRSectorCarrier=.*,CommonBeamforming=1              coverageShape     1
set NRCellDU=.*                   nrSrsDlBufferVolThr 100                                                                              
set NRCellDU=.*                   pdcchLaSinrOffset -20      

                                                                          
set ENodeBFunction=1                                        s1GtpuEchoEnable  1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          anrStateNR        1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength    26
Set ENodeBFunction=1                                        endcX2IpAddrViaS1Active true
set ENodeBFunction=1                                        endcAllowed       true
set ENodeBFunction=1                                        endcAwareMfbiIntraCellHo false
set ENodeBFunction=1                                        endcDataUsageReportEnabled true
set ENodeBFunction=1                                        endcIntraBandBlocked true
set ENodeBFunction=1                                        endcPowerOffsetLte 3
set ENodeBFunction=1                                        endcS1OverlapMode true
set ENodeBFunction=1                                        endcSplitAllowedMoVoice false
set ENodeBFunction=1                                        endcSplitAllowedNonDynPwrShUe false

set ENodeBFunction=1                                        endcOverheatingAssistance true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          endcRachFailThrPerUe 5
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          scgSessTimeForEndcRachFail 2500
set PmFlexCounterFilter=ENDC                                endcFilterMin     2



set ENodeBFunction=1,EndcProfile=1 meNbS1TermReqArpLev 0                                                                                                          
set ENodeBFunction=1,EndcProfile=1 splitNotAllowedUeArpLev 0 
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6789]$ endcProfileRef ENodeBFunction=1,EndcProfile=1


cr ENodeBFunction=1,UePolicyOptimization=1 
                                                                                                                       
set ENodeBFunction=1,UePolicyOptimization=1 ueCapPrioList 0                                                                                                       
set ENodeBFunction=1,UePolicyOptimization=1 coverageAwareImc true 
set UePolicyOptimization=1                                  endcAwareImc      2
set EUtranCellFDD=.*                    endcB1MeasGapEnabled true
set EUtranCellFDD=.*                      endcB1MeasGapConfig 0
set EUtranCellFDD=.*                      endcSetupUlBsVolThr 5000
set EUtranCellFDD=.*                      loopingEndcBackoffDuration 200
set EUtranCellFDD=.*                      loopingEndcProtectionEnabled true
set EUtranCellFDD=.*                      loopingEndcShortScgSessTime 3000

set EutrancellFDD additionalUpperLayerIndList          1 1 1 1 1                                                    
set EutrancellFDD endcSetupDlPktVolThr                 5                                                                                                                            
set EutrancellFDD primaryUpperLayerInd                 1

set EutrancellTDD additionalUpperLayerIndList          1 1 1 1 1                                                    
set EutrancellTDD endcSetupDlPktVolThr                 5                                                                                                                            
set EutrancellTDD primaryUpperLayerInd                 1



set CXC4040004 FeatureState  1
set CXC4040005 FeatureState  1
set CXC4040006 FeatureState  1
set CXC4040008 FeatureState  1
set CXC4040009 FeatureState  1
set CXC4040010 FeatureState  1
set CXC4040014 FeatureState  1
set CXC4012492 FeatureState  1
set CXC4012271 FeatureState  1
set CXC4011067 FeatureState  1
set CXC4010963 FeatureState  1
set CXC4012505 FeatureState  1
set CXC4012356 FeatureState  1
set CXC4012200 FeatureState  1
set CXC4012199 FeatureState  1
set CXC4012349 FeatureState  1
set CXC4012018 FeatureState  1
set CXC4011814 FeatureState  1
set CXC4010320 FeatureState  1
set CXC4012590 FeatureState  1
set CXC4012510 FeatureState  1
set CXC4011967 FeatureState  1
set CXC4010620 FeatureState  1
set CXC4011422 FeatureState  1
set CXC4012256 FeatureState  1
set CXC4011373 FeatureState  1
set CXC4012123 FeatureState  1
set CXC4012218 FeatureState  1
set CXC4011370 FeatureState  1
set CXC4012371 FeatureState  1
set CXC4011476 FeatureState  1
set CXC4011666 FeatureState  1
set CXC4011922 FeatureState  1
set CXC4012374 FeatureState  1
set CXC4011958 FeatureState  1
set CXC4011378 FeatureState  1
set CXC4012097 FeatureState  1
set CXC4011698 FeatureState  1
set CXC4012589 FeatureState  1
set CXC4011910 FeatureState  1
set CXC4010949 FeatureState  1
set CXC4010956 FeatureState  1
set CXC4012129 FeatureState  1
set CXC4011064 FeatureState  1
set CXC4012238 FeatureState  1
set CXC4012373 FeatureState  1
set CXC4012089 FeatureState  1
set CXC4011062 FeatureState  1
set CXC4011951 FeatureState  1
set CXC4011969 FeatureState  1
set CXC4012558 FeatureState  1
set CXC4011255 FeatureState  1
set CXC4012326 FeatureState  1
set CXC4012406 FeatureState  1
set CXC4010912 FeatureState  1
set CXC4010609 FeatureState  1
set CXC4011060 FeatureState  1
set CXC4011061 FeatureState  1
set CXC4011937 FeatureState  1
set CXC4011559 FeatureState  1
set CXC4011940 FeatureState  1
set CXC4011034 FeatureState  1
set CXC4012504 FeatureState  1
set CXC4012381 FeatureState  1
set CXC4011069 FeatureState  1
set CXC4010964 FeatureState  1
set CXC4011245 FeatureState  1
set CXC4011482 FeatureState  1
set CXC4012316 FeatureState  1
set CXC4011930 FeatureState  1
set CXC4012111 FeatureState  1
set CXC4010618 FeatureState  1
set CXC4011256 FeatureState  1
set CXC4011157 FeatureState  1
set CXC4011941 FeatureState  1
set CXC4012385 FeatureState  1
set CXC4011983 FeatureState  1
set CXC4010770 FeatureState  1
set CXC4011319 FeatureState  1
set CXC4010974 FeatureState  1
set CXC4011804 FeatureState  1
set CXC4011557 FeatureState  1
set CXC4011443 FeatureState  1
set CXC4010613 FeatureState  1
set CXC4010319 FeatureState  1
set CXC4012273 FeatureState  1
set CXC4012375 FeatureState  1
set CXC4011807 FeatureState  1
set CXC4011481 FeatureState  1
set CXC4011372 FeatureState  1
set CXC4012578 FeatureState  1
set CXC4011808 FeatureState  1
set CXC4012502 FeatureState  1
set CXC4012272 FeatureState  1
set CXC4010967 FeatureState  1
set CXC4012015 FeatureState  1
set CXC4011018 FeatureState  1
set CXC4011811 FeatureState  1
set CXC4011345 FeatureState  1
set CXC4011982 FeatureState  1
set CXC4010723 FeatureState  1
set CXC4011485 FeatureState  1
set CXC4011815 FeatureState  1
set CXC4011366 FeatureState  1
set CXC4012324 FeatureState  1
set CXC4012534 FeatureState  1
set CXC4012549 FeatureState  1
set CXC4012547 FeatureState  1
set CXC4012503 FeatureState  1
set CXC4011068 FeatureState  1
set CXC4011163 FeatureState  1
set CXC4012485 FeatureState  1
set CXC4012563 FeatureState  1
set CXC4011716 FeatureState  1
set CXC4010962 FeatureState  1
set CXC4011699 FeatureState  1
set CXC4011813 FeatureState  1
set CXC4011183 FeatureState  1
set CXC4011515 FeatureState  1
set CXC4011033 FeatureState  1
set CXC4010717 FeatureState  1
set CXC4012424 FeatureState  1
set CXC4012347 FeatureState  1
set CXC4011715 FeatureState  1
set CXC4011942 FeatureState  1
set CXC4011938 FeatureState  1
set CXC4011711 FeatureState  1
set CXC4010980 FeatureState  1
set CXC4011252 FeatureState  1
set CXC4010959 FeatureState  1
set CXC4011427 FeatureState  1
set CXC4011667 FeatureState  1
set CXC4011056 FeatureState  1
set CXC4011710 FeatureState  1
set CXC4011057 FeatureState  1
set CXC4010856 FeatureState  1
set CXC4010973 FeatureState  1
set CXC4011939 FeatureState  1
set CXC4012261 FeatureState  1
set CXC4012019 FeatureState  1
set CXC4010961 FeatureState  1
set CXC4010990 FeatureState  1
set CXC4011251 FeatureState  1
set CXC4011075 FeatureState  1
set CXC4011327 FeatureState  1
set CXC4012070 FeatureState  1
set CXC4011918 FeatureState  1
set CXC4011477 FeatureState  1
set CXC4011059 FeatureState  1
set CXC4011479 FeatureState  1
set CXC4012260 FeatureState  1
set CXC4011155 FeatureState  1
set CXC4011063 FeatureState  1
set CXC4012500 FeatureState  1
set CXC4012325 FeatureState  1
set CXC4011356 FeatureState  1
set CXC4011917 FeatureState  1
set CXC4011974 FeatureState  1
set CXC4011317 FeatureState  1
set CXC4011050 FeatureState  1
set CXC4011618 FeatureState  1
set CXC4012022 FeatureState  1
set CXC4011253 FeatureState  1
set CXC4011975 FeatureState  1
set CXC4011991 FeatureState  1
set CXC4011933 FeatureState  1
set CXC4012562 FeatureState  1
set CXC4010841 FeatureState  1
set CXC4011911 FeatureState  1
set CXC4011946 FeatureState  1
set CXC4011444 FeatureState  1
set CXC4012587 FeatureState  1
set CXC4012036 FeatureState  1
set CXC4011074 FeatureState  1
set CXC4011820 FeatureState  1
set CXC4012003 FeatureState  1
set CXC4011072 FeatureState  1
set CXC4012330 FeatureState  1
set CXC4012493 FeatureState  1
set CXC4011258 FeatureState  1
set CXC4011823 FeatureState  1
set CXC4012259 FeatureState  1
set CXC4011914 FeatureState  1
set CXC4012333 FeatureState  1
set CXC4011011 FeatureState  1
set CXC4010616 FeatureState  1
set CXC4011707 FeatureState  1
set CXC4011809 FeatureState  1


crn ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30
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
dscpArpMap                           dscpArp1=-1,dscpArp10=-1,dscpArp11=-1,dscpArp12=-1,dscpArp13=-1,dscpArp14=-1,dscpArp15=-1,dscpArp2=-1,dscpArp3=-1,dscpArp4=-1,dscpArp5=-1,dscpArp6=-1,dscpArp7=-1,dscpArp8=-1,dscpArp9=-1
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
measReportConfigParams               a1ThresholdRsrpPrimOffset=0,a1ThresholdRsrpSecOffset=0,a1ThresholdRsrqPrimOffset=0,a1ThresholdRsrqSecOffset=0,a2ThresholdRsrpPrimOffset=0,a2ThresholdRsrpSecOffset=0,a2ThresholdRsrqPrimOffset=0,a2ThresholdRsrqSecOffset=0,a3InterOffsetAdjustmentRsrp=0,a3InterOffsetAdjustmentRsrq=0,a3IntraOffsetAdjustmentRsrp=0,a3IntraOffsetAdjustmentRsrq=0,a5Threshold1RsrpOffset=0,a5Threshold1RsrqOffset=0,a5Threshold2RsrpOffset=0,a5Threshold2RsrqOffset=0,b2Threshold1RsrpCdma2000Offset=0,b2Threshold1RsrpGeranOffset=0,b2Threshold1RsrpUtraOffset=0,b2Threshold1RsrqCdma2000Offset=0,b2Threshold1RsrqGeranOffset=0,b2Threshold1RsrqUtraOffset=0,b2Threshold2Cdma2000Offset=0,b2Threshold2EcNoUtraOffset=0,b2Threshold2GeranOffset=0,b2Threshold2RscpUtraOffset=0,offsetPerQciPrio=0,timeToTriggerInterA3=-1,timeToTriggerInterA3Rsrq=-1,timeToTriggerIntraA3=-1
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
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         300
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
userLabel
end




crn ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
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
dscpArpMap                           dscpArp1=-1,dscpArp10=-1,dscpArp11=-1,dscpArp12=-1,dscpArp13=-1,dscpArp14=-1,dscpArp15=-1,dscpArp2=-1,dscpArp3=-1,dscpArp4=-1,dscpArp5=-1,dscpArp6=-1,dscpArp7=-1,dscpArp8=-1,dscpArp9=-1
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
measReportConfigParams               a1ThresholdRsrpPrimOffset=0,a1ThresholdRsrpSecOffset=0,a1ThresholdRsrqPrimOffset=0,a1ThresholdRsrqSecOffset=0,a2ThresholdRsrpPrimOffset=0,a2ThresholdRsrpSecOffset=0,a2ThresholdRsrqPrimOffset=0,a2ThresholdRsrqSecOffset=0,a3InterOffsetAdjustmentRsrp=0,a3InterOffsetAdjustmentRsrq=0,a3IntraOffsetAdjustmentRsrp=0,a3IntraOffsetAdjustmentRsrq=0,a5Threshold1RsrpOffset=0,a5Threshold1RsrqOffset=0,a5Threshold2RsrpOffset=0,a5Threshold2RsrqOffset=0,b2Threshold1RsrpCdma2000Offset=0,b2Threshold1RsrpGeranOffset=0,b2Threshold1RsrpUtraOffset=0,b2Threshold1RsrqCdma2000Offset=0,b2Threshold1RsrqGeranOffset=0,b2Threshold1RsrqUtraOffset=0,b2Threshold2Cdma2000Offset=0,b2Threshold2EcNoUtraOffset=0,b2Threshold2GeranOffset=0,b2Threshold2RscpUtraOffset=0,offsetPerQciPrio=0,timeToTriggerInterA3=-1,timeToTriggerInterA3Rsrq=-1,timeToTriggerIntraA3=-1
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
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         0
userLabel
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end






crn ENodeBFunction=1,SubscriberGroupProfile=ENDC
bearerTriggerList                    
caRateAdjustCoeff                    -1
cellTriggerList                      
customTriggerList                    0
customTriggerType                    2
dlAiLaDeltaSinrMax                   30
dlDynBlerTargetAlg                   0
dlDynBlerTargetMax                   -1
dlDynBlerTargetMin                   1
dlHarqBlerTarget                     10
drxMode                              0
endcUserProfileRef
fastACqiReportEnabled                false
featuresToDisableMeas                
groupExtendInactAfterVolteRel        0
higherPriorityEnabled                false
iuaMode                              0
iuaProfileRef
lastSchedLinkAdaptMode               0
pZeroNominalPucchOffset              0
pZeroNominalPuschOffset              0
pdcchFlexibleBlerMode                0
preschedProfileRef
preschedulingMode                    0
profilePriority                      5
qciOffsetForQCI6                     0
qciOffsetForQCI7                     0
qciOffsetForQCI8                     0
qciOffsetForQCI9                     0
sCellScheduleSinrThresOffset         0
selectionProbability                 100
spidTriggerList                      
subGroupConfiguration1               
subGroupConfiguration2               
subGroupConfiguration3               
subGroupConfiguration4               
subGroupConfiguration5               
subGroupConfiguration6               
subGroupConfiguration7               
ulCandidateToRegion                  false
ulHarqBlerTarget                     10
ulMcsLowerLimit                      -1
ulMcsUpperLimit                      -1
ulOuterloopStepSizeFactor            10
ulPlThresToRegion                    500
ulSinrThresToRegion                  400
userLabel
volteCodecRateForUlSinrEst           -1
end

confbd-
gs-
cvms Post_5G_GPL_$date


lt all     	                                                                                                                                                       
rbs                                                                                                                                                        
rbs                                                                                                                                                               
confbd+                                                                                                                                                           
                                                                                                                                                                  
$date = `date +%y%m%d_%H%M`                                                                                                                                       
cvms Pre_LMS_Settings_5G_$date                                                                                                                                         
                                  


confbd+
gs+
set NRCellDU=.*                   cellRange         10000 
set NRCellDU=.*                   ssbGscn           7790                                                                               
set NRCellDU=.*                   ssbFrequency      629952     

set EUtranCellFDD=.* endcAllowedPlmnList  mcc=405,mnc=56,mncLength=2
set EUtranCellTDD=.* endcAllowedPlmnList  mcc=405,mnc=56,mncLength=2


Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical hysteresis=10,threshold=-118,timeToTrigger=160
Set EUtranCellFDD=.*,GUtranFreqRelation=629952 b1ThrRsrqFreqOffset 0
Set EUtranCellFDD=.*,GUtranFreqRelation=629952 b1ThrRsrpFreqOffset 0
Set EUtranCellFDD=.*,GUtranFreqRelation=629952 endcB1MeasPriority 7


confbd+
gs+
set EUtranCellFDD=.*,EUtranFreqRelation=3651 endcHoFreqPriority 6
set EUtranCellFDD=.*,EUtranFreqRelation=415 endcHoFreqPriority -1
set EUtranCellFDD=.*,EUtranFreqRelation=39150 endcHoFreqPriority -1
set EUtranCellFDD=.*,EUtranFreqRelation=39348 endcHoFreqPriority -1
set EUtranCellFDD=.*,EUtranFreqRelation=1301 endcHoFreqPriority 7

set EUtranCellFDD=.*,EUtranFreqRelation=3651 endcAwareIdleModePriority 5
set EUtranCellFDD=.*,EUtranFreqRelation=415 endcAwareIdleModePriority 6
set EUtranCellFDD=.*,EUtranFreqRelation=39150 endcAwareIdleModePriority 3
set EUtranCellFDD=.*,EUtranFreqRelation=39348 endcAwareIdleModePriority 3
set EUtranCellFDD=.*,EUtranFreqRelation=1301 endcAwareIdleModePriority 7

set EUtranCellFDD=.*,GUtranFreqRelation=629952 cellReselectionPriority 2
set EUtranCellFDD=.*,GUtranFreqRelation=629952 qRxLevMin         -124

#####TDD###
set EUtranCellTDD=.*,EUtranFreqRelation=3651 endcHoFreqPriority 6
set EUtranCellTDD=.*,EUtranFreqRelation=415 endcHoFreqPriority -1
set EUtranCellTDD=.*,EUtranFreqRelation=39150 endcHoFreqPriority -1
set EUtranCellTDD=.*,EUtranFreqRelation=39348 endcHoFreqPriority -1
set EUtranCellTDD=.*,EUtranFreqRelation=1301 endcHoFreqPriority 7

set EUtranCellTDD=.*,EUtranFreqRelation=3651 endcAwareIdleModePriority 5
set EUtranCellTDD=.*,EUtranFreqRelation=415 endcAwareIdleModePriority 6
set EUtranCellTDD=.*,EUtranFreqRelation=39150 endcAwareIdleModePriority 3
set EUtranCellTDD=.*,EUtranFreqRelation=39348 endcAwareIdleModePriority 3
set EUtranCellTDD=.*,EUtranFreqRelation=1301 endcAwareIdleModePriority 7

set EUtranCellTDD=.*,GUtranFreqRelation=629952 cellReselectionPriority 2
set EUtranCellTDD=.*,GUtranFreqRelation=629952 qRxLevMin         -124



crn GNBCUCPFunction=1,EUtraNetwork=1
end




crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=415
arfcnValueEUtranDl                   415
userLabel
end


crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39150
arfcnValueEUtranDl                   39150
userLabel
end

crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39348
arfcnValueEUtranDl                   39348
userLabel
end

crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=3651
arfcnValueEUtranDl                   3651
userLabel
end





Set GNBCUCPFunction=1,QciProfileEndcConfigExt=1  ulDataSplitThresholdMcg              -1
Set GNBCUCPFunction=1,QciProfileEndcConfigExt=1 ulDataSplitThreshold                 102400
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB1GUtra= triggerQuantityB1    0
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1  triggerQuantityA5     0
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 timeToTriggerB1   320
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 timeToTriggerA5    100
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base  rsrpSearchZone hysteresis=10,threshold=-112,timeToTrigger=160,timeToTriggerA1=-1
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base  rsrpCandidateA5  hysteresis=10,threshold1=-118,threshold2=-112,timeToTrigger=640
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base  rsrpCandidateA5  hysteresis=10,threshold1=-118,threshold2=-112,timeToTrigger=256
set McpcPSCellNrFreqRelProfileUeCfg=Base  rsrpCandidateA5Offset threshold1Offset=0,threshold2Offset=0
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base  rsrpCandidateA5  hysteresis=10,threshold1=-118,threshold2=-112,timeToTrigger=640
set McpcPSCellNrFreqRelProfileUeCfg=Base  rsrpCandidateA5Offset threshold1Offset=0,threshold2Offset=0
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base  rsrpCandidateA5  hysteresis=10,threshold1=-118,threshold2=-112,timeToTrigger=640
set McpcPSCellProfileUeCfg=Base  rsrpSearchZone threshold=-112
set IntraFreqMCCellProfileUeCfg=Base rsrpSCellCoverage threshold=-117
Set UePolicyOptimization=1        t320    180
Set UeCA=1,CaSCellHandling=Default,CaSCellHandlingUeCfg=Base sCellActDeactDataThresHyst 90
Set UeCA=1,CaSCellHandling=Default,CaSCellHandlingUeCfg=Base sCellActDeactDataThres -1
Set McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCriticalEnabled true
Set IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base  rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base  rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base  rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set EUtranCellFDD=.*,EUtranFreqRelation=.* qOffsetFreq       0
Set EUtranCellFDD=.*,EUtranFreqRelation=.* qOffsetFreq       0
SET ENodeBFunction=1,SubscriberGroupProfile=ENDC qciOffsetForQCI9                     0
SET ENodeBFunction=1,SubscriberGroupProfile=ENDC qciOffsetForQCI6                     0
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA1A2Endc=1 a2OuterSearchThrRsrqOffsetEndc       0
set ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc a1a2ThrRsrqQciOffsetEndc=0
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA1A2Endc=1 a2OuterSearchThrRsrpOffsetEndc       0
set ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc a1a2ThrRsrpQciOffsetEndc=0
set ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=0,a1a2ThrRsrqQciOffset=0
Set EUtranCellFDD=.*                      primaryUpperLayerInd 1
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set NRCellCU=.*                   mcpcPSCellProfileRef Mcpc=1,McpcPSCellProfile=Default
Set NRCellCU=.*                   mcpcPSCellEnabled true
set EUtranCell.*DD=.*                      lbActionForEndcUe 0
Set EUtranCellFDD=.*,EUtranFreqRelation=.*,EUtranCellRelation=.*  isHoAllowed       true
Set QciProfileEndcConfigExt=1                               initialUplinkConf 1
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 hysteresisA5      20
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640
Set GNBCUUPFunction=1                                       endcUlNrRetProhibTimer 1000
Set NRCellDU=.*                   endcUlNrQualHyst  6
Set NRCellDU=.*                   endcUlNrLowQualThresh 10
Set NRCellDU=.*                   endcUlLegSwitchEnabled true
Set ENodeBFunction=1                                        endcSplitAllowedMoVoice false
Set EUtranCellFDD=.*                      endcSetupDlPktAgeThr 0
Set GNBCUUPFunction=1                                       endcDlNrRetProhibTimer 400 
Set UePolicyOptimization=1         endcAwareImc      2
Set ENodeBFunction=1                                        endcAllowed       true 
Set GNBCUUPFunction=1                                       dcDlAggExpiryTimer 100
Set GNBCUUPFunction=1                                       dcDlAggActTime    1
SET ENodeBFunction=1,SubscriberGroupProfile=ENDC customTriggerType                    2
SET ENodeBFunction=1,SubscriberGroupProfile=ENDC customTriggerList                    0
Set IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base betterSpCellTriggerQuantity 0

Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrq   -435
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp   -115 
Set EUtranCellFDD=.*                      additionalUpperLayerIndList  1 1 1 1 1
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 a5Threshold2Rsrq  -195
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 a5Threshold2Rsrp  -112
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 a5Threshold1Rsrq  -195 
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 a5Threshold1Rsrp  -44


Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1  reportQuantityA5   0
Set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB1GUtra=1  hysteresisB1     0
Set GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=20,offset=30,timeToTrigger=640
Set EUtranCellFDD=.*                      endcSetupDlPktVolThr 5


confbd-
gs-
cvms Post_LMS_Settings_5G_$date  
"""


AS_GNBCUCPFunction=""" 
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
primaryPLMNId mcc=405,mnc=56
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

AS_GNBDUFunction = """
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
pLMNIdList mcc=405,mnc=56
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
dlStartCrb 0
endcUlLegSwitchEnabled true
endcUlNrLowQualThresh -4
endcUlNrQualHyst 6
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


AS_CGSWITCH_SCRIPT = """
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
