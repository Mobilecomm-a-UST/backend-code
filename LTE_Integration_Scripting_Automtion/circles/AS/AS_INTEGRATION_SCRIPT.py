AS_GPL_LMS_DST_SCRIPT = """

lt all
rbs
rbs


get Router=OAM,RouteTableIPv4Static=1,Dst=Default_ENM,NextHop= address$ > $OAM-Nexthop                                                                               
get Router=LTEUP,RouteTableIPv4Static=2,Dst=SGW1,NextHop= address$ > $UP-Nexthop                                                                             
get Router=LTECP,RouteTableIPv4Static=3,Dst=MME1,NextHop= address$ > $CP-Nexthop                                                                              

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
set  CXC4011814   featurestate  1
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



confb-

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
set EUtranFreqRelation=240 cellReselectionPriority 3                                                                                                                                                                                                                                                                              
set EUtranFreqRelation=39294 cellReselectionPriority 5                                                                                                                                                                                                                                                                              
set EUtranFreqRelation=39150 cellReselectionPriority 6                                                                                                                                                                                                                                                                              
set EUtranFreqRelation=39348 cellReselectionPriority 6                                                                                                                                                                                                                                                                              
set ,UtranFreqRelation=10* cellReselectionPriority 3                                                                                                                                                                                                                                                                                

cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3663                                                                                                                                                                                                                                                                             
3663                                                                                                                                                                                                                                                                                                                                
0                                                                                                                                                                                                                                                                                                                                   
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1511                                                                                                                                                                                                                                                                             
1511                                                                                                                                                                                                                                                                                                                                
0   
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=240                                                                                                                                                                                                                                                                             
240                                                                                                                                                                                                                                                                                                                                
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
ma F3 EUtranCellFDD earfcndl 1511                                                                                                                                                                                                                                                                                                   
ma F8 EUtranCellFDD earfcndl 3663                                                                                                                                                                                                                                                                                                   
ma T2 EUtranCellTDD earfcn 39150                                                                                                                                                                                                                                                                                                    
ma T1 EUtranCellTDD earfcn ^39[2-3]                                                                                                                                                                                                                                                                                                 
ma F1 EUtranCellFDD earfcndl 240                                                                                                                                                                                                                                                                                                    
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
func EURel_1511                                                                                                                                                                                                                                                                                                                     
for $mo in $Tab[$i]                                                                                                                                                                                                                                                                                                                 
 $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                                  
 pr $mordn,EUtranFreqRelation=1511                                                                                                                                                                                                                                                                                                  
 if $nr_of_mos = 0                                                                                                                                                                                                                                                                                                                  
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=1511                                                                                                                                                                                                                                                                                
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1511                                                                                                                                                                                                                                                                              
  4                                                                                                                                                                                                                                                                                                                                 
 fi                                                                                                                                                                                                                                                                                                                                 
done 
endfunc                                                                                                                                                                                                                                                                                                                             
func EURel_240                                                                                                                                                                                                                                                                                                                     
for $mo in $Tab[$i]                                                                                                                                                                                                                                                                                                                 
 $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                                  
 pr $mordn,EUtranFreqRelation=240                                                                                                                                                                                                                                                                                                  
 if $nr_of_mos = 0                                                                                                                                                                                                                                                                                                                  
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=240                                                                                                                                                                                                                                                                                
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=240                                                                                                                                                                                                                                                                             
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
##########Relation with 1511: ######                                                                                                                                                                                                                                                                                                
EURel_1511
##########Relation with 240: ######                                                                                                                                                                                                                                                                                                
EURel_240                                                                                                                                                                                                                                                                                                                           
##########Relation with 39294: ######                                                                                                                                                                                                                                                                                               
EURel_39294                                                                                                                                                                                                                                                                                                                         
##########Relation with 39150: ######                                                                                                                                                                                                                                                                                               
EURel_39150                                                                                                                                                                                                                                                                                                                         
##########Relation with 39348: ######                                                                                                                                                                                                                                                                                               
EURel_39348                                                                                                                                                                                                                                                                                                                         
done                                                                                                                                                                                                                                                                                                                                
##########Relation Done#####                                                                                                                                                                                                                                                                                                        
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 anrStateGsm 1                                                                                                                                                                                                                                                                 
set  GeranFreqGroupRelation=1          csFallbackPrio 2                                                                                                                                                                                                                                                                             
set  GeranFreqGroupRelation=1          csFallbackPrioEC 2                                                                                                                                                                                                                                                                           
set GeranFreqGroupRelation=1           connectedModeMobilityPrio -1                                                                                                                                                                                                                                                                 
set AdmissionControl=1 dlAdmDifferentiationThr 750                                                                                                                                                                                                                                                                                  
set AdmissionControl=1 ulAdmDifferentiationThr 750                                                                                                                                                                                                                                                                                  
set AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrpThresholdEutran -1240                                                                                                                                                                                                                                                              
set AnrFunction=1,AnrFunctionUtran=1 cellAddEcNoThresholdUtranDelta -10                                                                                                                                                                                                                                                             
set AnrFunction=1,AnrFunctionUtran=1 cellAddRscpThresholdUtranDelta -1                                                                                                                                                                                                                                                              
set AnrFunction=1,AnrFunctionEUtran=1 lbCellOffloadCapacityPolicy 30000                                                                                                                                                                                                                                                             
set AnrFunction=1 removeNrelTime 3                                                                                                                                                                                                                                                                                                  
set AnrFunction=1 removeNenbTime 3                                                                                                                                                                                                                                                                                                  
set AnrFunction=1 maxNoPciReportsEvent 30                                                                                                                                                                                                                                                                                           
set AnrFunction=1 removeNcellTime 3                                                                                                                                                                                                                                                                                                 
set AnrFunction=1 cellRelHoAttRateThreshold 15                                                                                                                                                                                                                                                                                      
set AnrFunction=1 probCellDetectMedHoSuccTime 2                                                                                                                                                                                                                                                                                     
set AnrFunction=1 probCellDetectLowHoSuccTime 4                                                                                                                                                                                                                                                                                     
set AnrFunction=1 problematicCellPolicy 2                                                                                                                                                                                                                                                                                           
set CarrierAggregationFunction=1 dynamicSCellSelectionMethod 2                                                                                                                                                                                                                                                                      
set RadioBearerTable=default,DataRadioBearer=1 dlMaxRetxThreshold 16                                                                                                                                                                                                                                                                
set RadioBearerTable=default,SignalingRadioBearer=1 dlMaxRetxThreshold 16                                                                                                                                                                                                                                                           
set RadioBearerTable=default,DataRadioBearer=1 ulMaxRetxThreshold 16                                                                                                                                                                                                                                                                
set RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitUl 80                                                                                                                                                                                                                                                                 
set RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitUl 80                                                                                                                                                                                                                                                            
set RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitDl 80                                                                                                                                                                                                                                                                 
set RadioBearerTable=default,SignalingRadioBearer=1 ulMaxRetxThreshold 16                                                                                                                                                                                                                                                           
set RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitDl 80                                                                                                                                                                                                                                                            
set EUtranCell alpha 8                                                                                                                                                                                                                                                                                                              
set EUtranCell pZeroNominalPucch -110                                                                                                                                                                                                                                                                                               
set EUtranCellFDD pZeroNominalPusch -83                                                                                                                                                                                                                                                                                             
set EUtranCellTDD pZeroNominalPusch -86                                                                                                                                                                                                                                                                                             
set EUtranCell qQualMin -34                                                                                                                                                                                                                                                                                                         
set EUtranCell qRxLevMinOffset 1000                                                                                                                                                                                                                                                                                                 
set EUtranCell rtpTimeout 10                                                                                                                                                                                                                                                                                                        
set EUtranCellFDD ttiBundlingSwitchThresHyst 30                                                                                                                                                                                                                                                                                     
set EUtranCell tTimeAlignmentTimer 0                                                                                                                                                                                                                                                                                                
set EUtranCell ulBlerTargetEnabled true                                                                                                                                                                                                                                                                                             
set EUtranCell deallocThrPucchFormat1 100                                                                                                                                                                                                                                                                                           
set EUtranCell deallocTimerPucchFormat1 6000                                                                                                                                                                                                                                                                                        
set EUtranCell hoOptAdjThresholdAbs 5                                                                                                                                                                                                                                                                                               
set EUtranCell hoOptAdjThresholdPerc 50                                                                                                                                                                                                                                                                                             
set EUtranCell ns05FullBandSchedEnabled false                                                                                                                                                                                                                                                                                       
set EUtranCell ns05FullBandUsersInCellThres 1                                                                                                                                                                                                                                                                                       
set EUtranCell pMaxServingCell 1000                                                                                                                                                                                                                                                                                                 
set EUtranCell prsPowerBoosting 3                                                                                                                                                                                                                                                                                                   
set EUtranCellFDD mappingInfo mappingInfoSIB4:i=2                                                                                                                                                                                                                                                                                   
set EUtranCellFDD mappingInfo mappingInfoSIB6:i=4                                                                                                                                                                                                                                                                                   
set EUtranCellTDD mappingInfo mappingInfoSIB7:i=5                                                                                                                                                                                                                                                                                   
set EUtranCellFDD mappingInfo mappingInfoSIB12:i=7                                                                                                                                                                                                                                                                                  
set ENodeBFunction=1 rrcConnReestActive true                                                                                                                                                                                                                                                                                        
set ENodeBFunction=1 tS1HoCancelTimer 3                                                                                                                                                                                                                                                                                             
set ENodeBFunction=1 enabledUlTrigMeas false                                                                                                                                                                                                                                                                                        
set ENodeBFunction=1 s1HODirDataPathAvail true                                                                                                                                                                                                                                                                                      
set ENodeBFunction=1 tRelocOverall 20                                                                                                                                                                                                                                                                                               
set ENodeBFunction=1 zzzTemporary52 1                                                                                                                                                                                                                                                                                               
set ENodeBFunction=1 zzzTemporary55 -2000000000                                                                                                                                                                                                                                                                                     
set LoadBalancingFunction=1 lbCaThreshold 2000                                                                                                                                                                                                                                                                                      
set LoadBalancingFunction=1 lbThreshold 20                                                                                                                                                                                                                                                                                          
set RadioBearerTable=default,MACConfiguration=1 ulTtiBundlingMaxHARQTx 7                                                                                                                                                                                                                                                            
set EUtranCellFDD=.*,MimoSleepFunction=1 switchUpMonitorDurTimer 15                                                                                                                                                                                                                                                                 
set Rcs=1 rlcDlDeliveryFailureAction 2                                                                                                                                                                                                                                                                                              
set RadioBearerTable=default,SignalingRadioBearer=1 tReorderingUl 35                                                                                                                                                                                                                                                                
set EUtranCell.* pdcchCfiMode 5                                                                                                                                                                                                                                                                                                     
set EUtranCell.* adaptiveCfiHoProhibit 0                                                                                                                                                                                                                                                                                            
set EUtranCellTDD=.* enableSinrUplinkClpc true                                                                                                                                                                                                                                                                                      
for $mo in F3                                                                                                                                                                                                                                                                                                                       
        $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                           
        set $mordn$ enableSinrUplinkClpc true                                                                                                                                                                                                                                                                                       
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellTDD pdcchOuterLoopInitialAdjVolte -46                                                                                                                                                                                                                                                                                 
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBadCovPrim=1 a2ThresholdRsrpPrim -140                                                                                                                                                                                                                                         
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBadCovPrim=1 a2ThresholdRsrpPrim -140                                                                                                                                                                                                                                         
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -110                                                                                                                                                                                                                                                         
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -114                                                                                                                                                                                                                                                         
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
    set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp -114                                                                                                                                                                                                                                                               
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -110                                                                                                                                                                                                                                                         
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -114                                                                                                                                                                                                                                                         
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1 a3offsetAnrDelta 0                                                                                                                                                                                                                  
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1 a3offsetAnrDelta 0                                                                                                                                                                                                                  
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10                                                                                                                                                                                                                                     
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSCellA1A2=1 hysteresisA1A2RsrpBidirectional 10                                                                                                                                                                                                                                     
set EUtranCellTDD dlInterferenceManagementActive true                                                                                                                                                                                                                                                                               
set EUtranCellTDD ulInterferenceManagementActive true                                                                                                                                                                                                                                                                               
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn$ dlInterferenceManagementActive true                                                                                                                                                                                                                                                                             
    set $mordn$ ulInterferenceManagementActive true                                                                                                                                                                                                                                                                                 
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellTDD covTriggerdBlindHoAllowed false                                                                                                                                                                                                                                                                                   
set EUtranCellTDD transmissionMode 4                                                                                                                                                                                                                                                                                                
set EUtranCellFDD cellRange 6                                                                                                                                                                                                                                                                                                       
set EUtranCellTDD cellRange 6                                                                                                                                                                                                                                                                                                       
set EUtranCellFDD lbEUtranTriggerOffloadThreshold 30                                                                                                                                                                                                                                                                                
set EUtranCellFDD covTriggerdBlindHoAllowed false                                                                                                                                                                                                                                                                                   
set EUtranCellFDD systemInformationBlock3 sIntraSearchP:i=44                                                                                                                                                                                                                                                                        
set EUtranCell systemInformationBlock3 sNonIntraSearchP:i=10                                                                                                                                                                                                                                                                        
set EUtranCellTDD systemInformationBlock3 sIntraSearchP:i=44                                                                                                                                                                                                                                                                        
set EUtranCellFDD systemInformationBlock3 sIntraSearch:i=44                                                                                                                                                                                                                                                                         
set EUtranCellTDD systemInformationBlock3 sIntraSearch:i=44                                                                                                                                                                                                                                                                         
set EUtranCellFDD systemInformationBlock3 sNonIntraSearch:i=10                                                                                                                                                                                                                                                                      
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn$ systemInformationBlock3 sNonIntraSearch:i=0                                                                                                                                                                                                                                                                     
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellTDD systemInformationBlock3 sNonIntraSearch:i=8                                                                                                                                                                                                                                                                       
set EUtranCellFDD systemInformationBlock3 qHyst:i=4                                                                                                                                                                                                                                                                                 
set EUtranCellTDD systemInformationBlock3 qHyst:i=4                                                                                                                                                                                                                                                                                 
set EUtranCellFDD systemInformationBlock3 sNonIntraSearchQ:i=0                                                                                                                                                                                                                                                                      
set EUtranCellTDD systemInformationBlock3 sNonIntraSearchQ:i=0                                                                                                                                                                                                                                                                      
set EUtranCellFDD systemInformationBlock6 tReselectionUtra:i=4                                                                                                                                                                                                                                                                      
set EUtranCellTDD systemInformationBlock6 tReselectionUtra:i=4                                                                                                                                                                                                                                                                      
set EUtranCellFDD changeNotification changeNotificationSIB8:i=true                                                                                                                                                                                                                                                                  
set EUtranCellFDD changeNotification changeNotificationSIB15:i=true                                                                                                                                                                                                                                                                 
set EUtranCellFDD changeNotification changeNotificationSIB16:i=true                                                                                                                                                                                                                                                                 
set EUtranCellTDD changeNotification changeNotificationSIB8:i=true                                                                                                                                                                                                                                                                  
set EUtranCellTDD changeNotification changeNotificationSIB15:i=true                                                                                                                                                                                                                                                                 
set EUtranCellTDD changeNotification changeNotificationSIB16:i=true                                                                                                                                                                                                                                                                 
set EUtranCellFDD pdcchOuterLoopInitialAdjVolte -46                                                                                                                                                                                                                                                                                 
set EUtranCellFDD threshServingLow 8                                                                                                                                                                                                                                                                                                
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn$ threshServingLow 0                                                                                                                                                                                                                                                                                              
done                                                                                                                                                                                                                                                                                                                                
lt all                                                                                                                                                                                                                                                                                                                              
set EUtranCellTDD threshServingLow 8                                                                                                                                                                                                                                                                                                
set EUtranCellFDD lbEUtranAcceptOffloadThreshold 10                                                                                                                                                                                                                                                                                 
set EUtranCell.* pdcchOuterLoopUpStepVolte 9                                                                                                                                                                                                                                                                                        
set EUtranCellFDD transmissionMode 4                                                                                                                                                                                                                                                                                                
set EUtranCellFDD ttiBundlingAfterReest 1                                                                                                                                                                                                                                                                                           
set EUtranCellFDD enableServiceSpecificHARQ true                                                                                                                                                                                                                                                                                    
set EUtranCellTDD enableServiceSpecificHARQ true                                                                                                                                                                                                                                                                                    
set EUtranCellFDD pdcchOuterLoopInitialAdj -70                                                                                                                                                                                                                                                                                      
set EUtranCellFDD pdcchOuterLoopInitialAdjPCell -70                                                                                                                                                                                                                                                                                 
set EUtranCellFDD pdcchOuterLoopUpStep 8                                                                                                                                                                                                                                                                                            
set EUtranCellFDD pdcchOuterLoopUpStepPCell 6                                                                                                                                                                                                                                                                                       
set EUtranCellFDD pdcchTargetBler 24                                                                                                                                                                                                                                                                                                
set EUtranCellTDD pdcchTargetBler 24                                                                                                                                                                                                                                                                                                
set EUtranCellFDD pdcchTargetBlerPCell 22                                                                                                                                                                                                                                                                                           
set EUtranCellTDD pdcchTargetBlerPCell 22                                                                                                                                                                                                                                                                                           
set EUtranCellFDD tReorderingAutoConfiguration true                                                                                                                                                                                                                                                                                 
set EUtranCellFDD dlBlerTargetEnabled TRUE                                                                                                                                                                                                                                                                                          
set EUtranCellFDD ulHarqVolteBlerTarget 3                                                                                                                                                                                                                                                                                           
set EUtranCellTDD ulHarqVolteBlerTarget 3                                                                                                                                                                                                                                                                                           
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrp -140                                                                                                                                                                                                                                              
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrp -140                                                                                                                                                                                                                                              
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -114                                                                                                                                                                                                                                              
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -83                                                                                                                                                                                                                                               
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset:i=66,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                                  
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset:i=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                                   
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 inhibitA2SearchConfig 1                                                                                                                                                                                                                                                   
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 inhibitA2SearchConfig 1                                                                                                                                                                                                                                                   
set EUtranCellFDD=.*,UeMeasControl=1 filterCoefficientEUtraRsrp 4                                                                                                                                                                                                                                                                   
set EUtranCellTDD=.*,UeMeasControl=1 filterCoefficientEUtraRsrp 4                                                                                                                                                                                                                                                                   
set RlfProfile=1$ t301 1000                                                                                                                                                                                                                                                                                                         
set RlfProfile=1$ n310 10                                                                                                                                                                                                                                                                                                           
set RlfProfile=1$ t310 500                                                                                                                                                                                                                                                                                                          
set RlfProfile=1$ t311 5000                                                                                                                                                                                                                                                                                                         
set Rrc=1 t301 1000                                                                                                                                                                                                                                                                                                                 
set Rrc=1 t304 2000                                                                                                                                                                                                                                                                                                                 
set GeranFreqGroupRelation= cellReselectionPriority 1                                                                                                                                                                                                                                                                               
set EUtranFreqRelation=3663 cellReselectionPriority 2                                                                                                                                                                                                                                                                               
set EUtranFreqRelation=1511 cellReselectionPriority 5 
set EUtranFreqRelation=240 cellReselectionPriority 4                                                                                                                                                                                                                                                                               
set EUtranFreqRelation=39294 cellReselectionPriority 6                                                                                                                                                                                                                                                                              
set EUtranFreqRelation=39150 cellReselectionPriority 6                                                                                                                                                                                                                                                                              
set EUtranFreqRelation=39348 cellReselectionPriority 6                                                                                                                                                                                                                                                                              
set ,UtranFreqRelation=10* cellReselectionPriority 3                                                                                                                                                                                                                                                                                
set EUtranCell.*=.*,UtranFreqRelation=.* csFallbackPrio 3                                                                                                                                                                                                                                                                           
set EUtranCell.*=.*,UtranFreqRelation=.* csFallbackPrioEC 3                                                                                                                                                                                                                                                                         
set EUtranCell.*=.*,UtranFreqRelation=.* pMaxUtra 23                                                                                                                                                                                                                                                                                
set EUtranCell.*=.*,UtranFreqRelation=.* qRxLevMin -119                                                                                                                                                                                                                                                                             
set EUtranCellFDD=.*,UtranFreqRelation=.* threshXLow 24                                                                                                                                                                                                                                                                             
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,UtranFreqRelation=1511 threshXLow 62                                                                                                                                                                                                                                                                               
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*,UtranFreqRelation=.* threshXLow 62                                                                                                                                                                                                                                                                             
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
    set $mordn,EUtranFreqRelation=3663 threshXLow  14                                                                                                                                                                                                                                                                               
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*,EUtranFreqRelation=1509 threshXLow 14                                                                                                                                                                                                                                                                          
set EUtranCellTDD=.*,EUtranFreqRelation=3645 threshXLow 62                                                                                                                                                                                                                                                                          
for $mo in T2                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=39[2-3] threshXLow 10                                                                                                                                                                                                                                                                         
done                                                                                                                                                                                                                                                                                                                                
set UtraNetwork=1,UtranFrequency=10657,ExternalUtranCellFDD srvccCapability 1                                                                                                                                                                                                                                                       
set RadioBearerTable=default,MACConfiguration=1 ulMaxHARQTx 5                                                                                                                                                                                                                                                                       
set RadioBearerTable=default,MACConfiguration=1 dlMaxHARQTx 4                                                                                                                                                                                                                                                                       
set QciProfilePredefined=qci1$ absPrioOverride 0                                                                                                                                                                                                                                                                                    
set QciProfilePredefined=qci2$ absPrioOverride 0                                                                                                                                                                                                                                                                                    
set QciProfilePredefined=qci5$ absPrioOverride 1                                                                                                                                                                                                                                                                                    
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 aqmMode 2                                                                                                                                                                                                                                                           
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 dataFwdPerQciEnabled true                                                                                                                                                                                                                                           
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 dlResourceAllocationStrategy 1                                                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 drxPriority 99                                                                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 drxProfileRef DrxProfile=1                                                                                                                                                                                                                                          
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 dscp 34                                                                                                                                                                                                                                                             
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 inactivityTimerOffset 30                                                                                                                                                                                                                                            
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1                                                                                                                                                                                                       
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 pdb 80                                                                                                                                                                                                                                                              
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 pdbOffset 100                                                                                                                                                                                                                                                       
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 pdcpSNLength 12                                                                                                                                                                                                                                                     
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 priority 1                                                                                                                                                                                                                                                          
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 resourceType 1                                                                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 rlcMode 1                                                                                                                                                                                                                                                           
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 rlcSNLength 10                                                                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 rlfProfileRef RlfProfile=1                                                                                                                                                                                                                                          
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 rlfPriority 10                                                                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 rohcEnabled true                                                                                                                                                                                                                                                    
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 serviceType 1                                                                                                                                                                                                                                                       
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 tReorderingDl 120                                                                                                                                                                                                                                                   
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 tReorderingUl 50                                                                                                                                                                                                                                                    
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 schedulingAlgorithm 6                                                                                                                                                                                                                                               
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold1RsrpOffset=2                                                                                                                                                                                                                     
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold2RsrpOffset=2                                                                                                                                                                                                                     
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams b2Threshold1RsrpUtraOffset=2                                                                                                                                                                                                                 
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams b2Threshold2ECNOUtraOffset=20                                                                                                                                                                                                                
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a1ThresholdRsrpPrimOffset=2                                                                                                                                                                                                                  
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a2ThresholdRsrpPrimOffset=2                                                                                                                                                                                                                  
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 ResourceAllocationStrategy 1                                                                                                                                                                                                                                        
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 aqmMode 2                                                                                                                                                                                                                                                           
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 dataFwdPerQciEnabled true                                                                                                                                                                                                                                           
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 dlResourceAllocationStrategy 1                                                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 drxPriority 100                                                                                                                                                                                                                                                     
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 drxProfileRef DrxProfile=2                                                                                                                                                                                                                                          
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 dscp 34                                                                                                                                                                                                                                                             
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 inactivityTimerOffset 30                                                                                                                                                                                                                                            
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=2                                                                                                                                                                                                       
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 pdb 150                                                                                                                                                                                                                                                             
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 pdbOffset 50                                                                                                                                                                                                                                                        
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 pdcpSNLength 12                                                                                                                                                                                                                                                     
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 priority 4                                                                                                                                                                                                                                                          
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 resourceType 1                                                                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 rlcSNLength 10                                                                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 rlcMode 1                                                                                                                                                                                                                                                           
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 rohcEnabled false                                                                                                                                                                                                                                                   
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 serviceType 0                                                                                                                                                                                                                                                       
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 schedulingAlgorithm 3                                                                                                                                                                                                                                               
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 dlMinBitRate 384                                                                                                                                                                                                                                                    
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 ulMinBitRate 384                                                                                                                                                                                                                                                    
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 aqmMode 0                                                                                                                                                                                                                                                           
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 dataFwdPerQciEnabled true                                                                                                                                                                                                                                           
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 dlResourceAllocationStrategy 0                                                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 drxPriority 1                                                                                                                                                                                                                                                       
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 drxProfileRef DrxProfile=0                                                                                                                                                                                                                                          
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 dscp 46                                                                                                                                                                                                                                                             
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 inactivityTimerOffset 0                                                                                                                                                                                                                                             
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1                                                                                                                                                                                                       
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 pdb 100                                                                                                                                                                                                                                                             
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 pdbOffset 0                                                                                                                                                                                                                                                         
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 pdcpSNLength 12                                                                                                                                                                                                                                                     
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 priority 2                                                                                                                                                                                                                                                          
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 resourceType 0                                                                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 rlcSNLength 10                                                                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 rlcMode 0                                                                                                                                                                                                                                                           
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 rohcEnabled false                                                                                                                                                                                                                                                   
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 serviceType 2                                                                                                                                                                                                                                                       
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 schedulingAlgorithm 0                                                                                                                                                                                                                                               
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 tReorderingUl 35                                                                                                                                                                                                                                                    
set EUtranCell.*=.*,EUtranFreqRelation=.* caTriggeredRedirectionActive false                                                                                                                                                                                                                                                        
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39150 threshXHigh 12                                                                                                                                                                                                                                                       
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=39[2-3] threshXHigh 12                                                                                                                                                                                                                                                     
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=1511 threshXHigh  10                                                                                                                                                                                                                                                                          
done                                                                                                                                                                                                                                                                                                                                
for $mo in T1                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=39150 threshXHigh 12                                                                                                                                                                                                                                                                          
done                                                                                                                                                                                                                                                                                                                                
set EUtranCell.*=.*,EUtranFreqRelation=.* qOffsetFreq 0                                                                                                                                                                                                                                                                             
set UtranFreqRelation=10657  voicePrio -1                                                                                                                                                                                                                                                                                           
set GeranFreqGroupRelation=  voicePrio -1                                                                                                                                                                                                                                                                                           
for $mo in F8                                                                                                                                                                                                                                                                                                                       
        $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                           
        set $mordn,EUtranFreqRelation=39150  voicePrio -1                                                                                                                                                                                                                                                                           
        set $mordn,EUtranFreqRelation=39[2-3]  voicePrio -1                                                                                                                                                                                                                                                                         
        set $mordn,EUtranFreqRelation=1511  voicePrio 4                                                                                                                                                                                                                                                                             
        set $mordn,EUtranFreqRelation=3663  voicePrio 6 
        set $mordn,EUtranFreqRelation=240  voicePrio 4                                                                                                                                                                                                                                                                            
done                                                                                                                                                                                                                                                                                                                                
for $mo in F3                                                                                                                                                                                                                                                                                                                       
        $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                           
        set $mordn,EUtranFreqRelation=39150  voicePrio -1                                                                                                                                                                                                                                                                           
        set $mordn,EUtranFreqRelation=39[2-3]  voicePrio -1                                                                                                                                                                                                                                                                         
        set $mordn,EUtranFreqRelation=1511  voicePrio 6                                                                                                                                                                                                                                                                             
        set $mordn,EUtranFreqRelation=3663  voicePrio 3
        set $mordn,EUtranFreqRelation=240  voicePrio 4                                                                                                                                                                                                                                                                              
done
for $mo in F1                                                                                                                                                                                                                                                                                                                       
        $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                           
        set $mordn,EUtranFreqRelation=39150  voicePrio -1                                                                                                                                                                                                                                                                           
        set $mordn,EUtranFreqRelation=39[2-3]  voicePrio -1                                                                                                                                                                                                                                                                         
        set $mordn,EUtranFreqRelation=1511  voicePrio 6                                                                                                                                                                                                                                                                             
        set $mordn,EUtranFreqRelation=3663  voicePrio 3 
        set $mordn,EUtranFreqRelation=240  voicePrio 4                                                                                                                                                                                                                                                                             
done                                                                                                                                                                                                                                                                                                                                 
set EUtranCellTDD=.*,EUtranFreqRelation=3663  voicePrio 2                                                                                                                                                                                                                                                                           
set EUtranCellTDD=.*,EUtranFreqRelation=1511  voicePrio 4
set EUtranCellTDD=.*,EUtranFreqRelation=240  voicePrio 4
                                                                                                                                                                                                                                                                           
for $mo in T2                                                                                                                                                                                                                                                                                                                       
        $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                           
        set $mordn,EUtranFreqRelation=39150  voicePrio 6                                                                                                                                                                                                                                                                            
        set $mordn,EUtranFreqRelation=39[2-3]  voicePrio -1                                                                                                                                                                                                                                                                         
done                                                                                                                                                                                                                                                                                                                                
for $mo in T1                                                                                                                                                                                                                                                                                                                       
        $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                           
        set $mordn,EUtranFreqRelation=39150  voicePrio -1                                                                                                                                                                                                                                                                           
        set $mordn,EUtranFreqRelation=39[2-3]  voicePrio 6                                                                                                                                                                                                                                                                          
done                                                                                                                                                                                                                                                                                                                                
set GeranFreqGroupRelation= connectedModeMobilityPrio -1                                                                                                                                                                                                                                                                            
set UtranFreqRelation=10657 connectedModeMobilityPrio -1                                                                                                                                                                                                                                                                            
set EUtranCellFDD=.*,EUtranFreqRelation=3663  connectedModeMobilityPrio 2                                                                                                                                                                                                                                                           
set EUtranCellFDD=.*,EUtranFreqRelation=1511  connectedModeMobilityPrio 5                                                                                                                                                                                                                                                           
set EUtranCellFDD=.*,EUtranFreqRelation=39150 connectedModeMobilityPrio 6                                                                                                                                                                                                                                                           
set EUtranCellFDD=.*,EUtranFreqRelation=39294 connectedModeMobilityPrio 6                                                                                                                                                                                                                                                           
set EUtranCellFDD=.*,EUtranFreqRelation=39348 connectedModeMobilityPrio 6
set EUtranCellFDD=.*,EUtranFreqRelation=240 connectedModeMobilityPrio 4                                                                                                                                                                                                                                                            
for $mo in T2                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=39150 connectedModeMobilityPrio 6                                                                                                                                                                                                                                                             
        set $mordn,EUtranFreqRelation=39294 connectedModeMobilityPrio 6                                                                                                                                                                                                                                                             
        set $mordn,EUtranFreqRelation=39348 connectedModeMobilityPrio 6                                                                                                                                                                                                                                                             
        set $mordn,EUtranFreqRelation=1511 connectedModeMobilityPrio 5
        set $mordn,EUtranFreqRelation=240 connectedModeMobilityPrio 4                                                                                                                                                                                                                                                              
        set $mordn,EUtranFreqRelation=3663 connectedModeMobilityPrio -1                                                                                                                                                                                                                                                             
done                                                                                                                                                                                                                                                                                                                                
for $mo in T1                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=39150 connectedModeMobilityPrio 6                                                                                                                                                                                                                                                             
        set $mordn,EUtranFreqRelation=39294 connectedModeMobilityPrio 6                                                                                                                                                                                                                                                             
        set $mordn,EUtranFreqRelation=39348 connectedModeMobilityPrio 6                                                                                                                                                                                                                                                             
        set $mordn,EUtranFreqRelation=1511 connectedModeMobilityPrio 5
        set $mordn,EUtranFreqRelation=240 connectedModeMobilityPrio 4                                                                                                                                                                                                                                                              
        set $mordn,EUtranFreqRelation=3663 connectedModeMobilityPrio -1                                                                                                                                                                                                                                                             
done                                                                                                                                                                                                                                                                                                                                
set EUtranCell.*=.*,EUtranFreqRelation=.* interFreqMeasType 0                                                                                                                                                                                                                                                                       
set EUtranCell.*=.*,EUtranFreqRelation=.* qRxLevMin -124                                                                                                                                                                                                                                                                            
set EUtranCell.*=.*,EUtranFreqRelation=.* tReselectionEutra 2                                                                                                                                                                                                                                                                       
set EUtranCell.*=.*,EUtranFreqRelation=.* eutranFreqToQciProfileRelation lbQciProfileHandling:i=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                                      
set ENodeBFunction=1,EUtranCell.*=.*,EUtranFreqRelation=.* allowedPlmnList mcc=405,mnc=56,mncLength=2                                                                                                                                                                                                                               
set EUtranCellFDD=.*,EUtranFreqRelation=39150 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0                                                                                                                                                                                                                              
set EUtranCellFDD=.*,EUtranFreqRelation=39[2-3] eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0                                                                                                                                                                                                                            
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=1511 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=2                                                                                                                                                                                                                                 
        set $mordn,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0                                                                                                                                                                                                                                 
done                                                                                                                                                                                                                                                                                                                                
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=1511 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0                                                                                                                                                                                                                                 
        set $mordn,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=10                                                                                                                                                                                                                                
done 
for $mo in F1                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=240 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0                                                                                                                                                                                                                                 
        set $mordn,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=10                                                                                                                                                                                                                                
done                                                                                                                                                                                                                                                                                                                                 
set EUtranCellTDD=.*,EUtranFreqRelation=39[2-3] eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0                                                                                                                                                                                                                            
set EUtranCellTDD=.*,EUtranFreqRelation=1511 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=66
set EUtranCellTDD=.*,EUtranFreqRelation=240 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=66                                                                                                                                                                                                                              
set EUtranCellTDD=.*,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0                                                                                                                                                                                                                               
set EUtranCellTDD=.*,EUtranFreqRelation=39150 eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=0                                                                                                                                                                                                                              
set EUtranCellFDD=.*,EUtranFreqRelation=39150 eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=68                                                                                                                                                                                                                             
set EUtranCellFDD=.*,EUtranFreqRelation=39[2-3] eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=68                                                                                                                                                                                                                           
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=1511 eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0                                                                                                                                                                                                                                 
        set $mordn,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0
        set $mordn,EUtranFreqRelation=240 eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0                                                                                                                                                                                                                                 
done                                                                                                                                                                                                                                                                                                                                
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=1511 eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0
        set $mordn,EUtranFreqRelation=240 eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0                                                                                                                                                                                                                                 
        set $mordn,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=2                                                                                                                                                                                                                                 
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*,EUtranFreqRelation=3663 eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0                                                                                                                                                                                                                               
set EUtranCellTDD=.*,EUtranFreqRelation=39150 eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0                                                                                                                                                                                                                              
set EUtranCellTDD=.*,EUtranFreqRelation=39[2-3] eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0                                                                                                                                                                                                                            
set EUtranCellTDD=.*,EUtranFreqRelation=1511 eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0                                                                                                                                                                                                                               
set EUtranCellTDD=.*,EUtranFreqRelation=1511 a5Thr1RsrpFreqOffset 0 
set EUtranCellTDD=.*,EUtranFreqRelation=240 eutranFreqToQciProfileRelation a5Thr2RsrpFreqQciOffset=0                                                                                                                                                                                                                               
set EUtranCellTDD=.*,EUtranFreqRelation=240 a5Thr1RsrpFreqOffset 0                                                                                                                                                                                                                                                                 
set EUtranCellTDD=.*,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 0                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*,EUtranFreqRelation=3663 a5Thr1RsrpFreqOffset 0                                                                                                                                                                                                                                                                 
set EUtranCellTDD=.*,EUtranFreqRelation=39[2-3] a5Thr1RsrpFreqOffset 0                                                                                                                                                                                                                                                              
set EUtranCellFDD=.*,EUtranFreqRelation=39150 a5Thr1RsrpFreqOffset 27                                                                                                                                                                                                                                                               
set EUtranCellFDD=.*,EUtranFreqRelation=3663 a5Thr1RsrpFreqOffset 0                                                                                                                                                                                                                                                                 
set EUtranCellFDD=.*,EUtranFreqRelation=39[2-3] a5Thr1RsrpFreqOffset 27                                                                                                                                                                                                                                                             
set EUtranCellFDD=.*,EUtranFreqRelation=1511 a5Thr1RsrpFreqOffset 0                                                                                                                                                                                                                                                                 
set EUtranCellFDD=.*,EUtranFreqRelation=39[2-3]  a5Thr2RsrpFreqOffset  0                                                                                                                                                                                                                                                            
set EUtranCellFDD=.*,EUtranFreqRelation=39150  a5Thr2RsrpFreqOffset  0                                                                                                                                                                                                                                                              
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=1511  a5Thr2RsrpFreqOffset  4                                                                                                                                                                                                                                                                 
        set $mordn,EUtranFreqRelation=3663  a5Thr2RsrpFreqOffset  0
        set $mordn,EUtranFreqRelation=240  a5Thr2RsrpFreqOffset  4                                                                                                                                                                                                                                                                  
done                                                                                                                                                                                                                                                                                                                                
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=1511  a5Thr2RsrpFreqOffset  0                                                                                                                                                                                                                                                                 
        set $mordn,EUtranFreqRelation=3663  a5Thr2RsrpFreqOffset  2
        set $mordn,EUtranFreqRelation=240  a5Thr2RsrpFreqOffset  0                                                                                                                                                                                                                                                                 
done                                                                                                                                                                                                                                                                                                                                
for $mo in T1                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=1511  a5Thr2RsrpFreqOffset  0                                                                                                                                                                                                                                                                 
        set $mordn,EUtranFreqRelation=39[2-3]  a5Thr2RsrpFreqOffset  0                                                                                                                                                                                                                                                              
        set $mordn,EUtranFreqRelation=3663  a5Thr2RsrpFreqOffset  66                                                                                                                                                                                                                                                                
        set $mordn,EUtranFreqRelation=39150  a5Thr2RsrpFreqOffset  66
        set $mordn,EUtranFreqRelation=240  a5Thr2RsrpFreqOffset  0                                                                                                                                                                                                                                                                
done                                                                                                                                                                                                                                                                                                                                
for $mo in T2                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=1511  a5Thr2RsrpFreqOffset  0                                                                                                                                                                                                                                                                 
        set $mordn,EUtranFreqRelation=39[2-3]  a5Thr2RsrpFreqOffset  66                                                                                                                                                                                                                                                             
        set $mordn,EUtranFreqRelation=3663  a5Thr2RsrpFreqOffset  66                                                                                                                                                                                                                                                                
        set $mordn,EUtranFreqRelation=39150  a5Thr2RsrpFreqOffset  0
        set $mordn,EUtranFreqRelation=240  a5Thr2RsrpFreqOffset  0                                                                                                                                                                                                                                                                
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*,MimoSleepFunction=1 switchUpMonitorDurTimer 15                                                                                                                                                                                                                                                                 
set EUtranCellFDD servOrPrioTriggeredErabAction 3                                                                                                                                                                                                                                                                                   
set EUtranCell.*=.*,UtranFreqRelation=.* utranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                                          
set EUtranCellFDD=.*,EUtranFreqRelation=1511 interFreqMeasType 0                                                                                                                                                                                                                                                                    
set SectorCarrier radioTransmitPerformanceMode 2                                                                                                                                                                                                                                                                                    
set EUtranCellFDD pdcchPowerBoostMax 2                                                                                                                                                                                                                                                                                              
set EUtranCellTDD pdcchPowerBoostMax 2                                                                                                                                                                                                                                                                                              
set ENodeBFunction=1 alignTtiBundWUlTrigSinr 1                                                                                                                                                                                                                                                                                      
set EUtranCell.* allocTimerPucchFormat1 50                                                                                                                                                                                                                                                                                          
set EUtranCell.* allocThrPucchFormat1 50                                                                                                                                                                                                                                                                                            
set ReportConfigEUtraBestCell a3offset 30                                                                                                                                                                                                                                                                                           
set ReportConfigSearch a2CriticalThrQci1RsrqOffset -50                                                                                                                                                                                                                                                                              
set ReportConfigSearch a2CriticalThrQci1RsrpOffset -20                                                                                                                                                                                                                                                                              
set ENodeBFunction=1,DrxProfile=0 drxInactivityTimer 14                                                                                                                                                                                                                                                                             
set ENodeBFunction=1,DrxProfile=0 drxRetransmissionTimer 4                                                                                                                                                                                                                                                                          
set ENodeBFunction=1,DrxProfile=0 longDrxCycle 9                                                                                                                                                                                                                                                                                    
set ENodeBFunction=1,DrxProfile=0 longDrxCycleOnly 9                                                                                                                                                                                                                                                                                
set ENodeBFunction=1,DrxProfile=0 onDurationTimer 7                                                                                                                                                                                                                                                                                 
set ENodeBFunction=1,DrxProfile=0 shortDrxCycle 9                                                                                                                                                                                                                                                                                   
set ENodeBFunction=1,DrxProfile=0 shortDrxCycleTimer 1                                                                                                                                                                                                                                                                              
set ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 6                                                                                                                                                                                                                                                                             
set ENodeBFunction=1,DrxProfile=1$ drxRetransmissionTimer 2                                                                                                                                                                                                                                                                         
set ENodeBFunction=1,DrxProfile=1$ drxstate 0                                                                                                                                                                                                                                                                                       
set ENodeBFunction=1,DrxProfile=1$ longDrxCycle 3                                                                                                                                                                                                                                                                                   
set ENodeBFunction=1,DrxProfile=1$ longDrxCycleOnly 3                                                                                                                                                                                                                                                                               
set ENodeBFunction=1,DrxProfile=1$ onDurationTimer 7                                                                                                                                                                                                                                                                                
set ENodeBFunction=1,DrxProfile=1$ shortDrxCycle 7                                                                                                                                                                                                                                                                                  
set ENodeBFunction=1,DrxProfile=1$ shortDrxCycleTimer 0                                                                                                                                                                                                                                                                             
set ENodeBFunction=1,DrxProfile=2 drxInactivityTimer 6                                                                                                                                                                                                                                                                              
set ENodeBFunction=1,DrxProfile=2 drxRetransmissionTimer 1                                                                                                                                                                                                                                                                          
set ENodeBFunction=1,DrxProfile=2 longDrxCycle 3                                                                                                                                                                                                                                                                                    
set ENodeBFunction=1,DrxProfile=2 longDrxCycleOnly 3                                                                                                                                                                                                                                                                                
set ENodeBFunction=1,DrxProfile=2 onDurationTimer 6                                                                                                                                                                                                                                                                                 
set ENodeBFunction=1,DrxProfile=2 shortDrxCycle 7                                                                                                                                                                                                                                                                                   
set ENodeBFunction=1,DrxProfile=2 shortDrxCycleTimer 0                                                                                                                                                                                                                                                                              
set EUtranCell.* drxActive true                                                                                                                                                                                                                                                                                                     
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp -140                                                                                                                                                                                                                                                     
#for $mo in F8                                                                                                                                                                                                                                                                                                                      
#    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                              
#       set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp -140                                                                                                                                                                                                                                                       
#done                                                                                                                                                                                                                                                                                                                               
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp -140                                                                                                                                                                                                                                                     
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2EcNoUtra -180                                                                                                                                                                                                                                                 
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2EcNoUtra -180                                                                                                                                                                                                                                                 
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold2RscpUtra -109                                                                                                                                                                                                                                                  
set EUtranCell.*,UeMeasControl=1,ReportConfigB2Utra=1 hysteresisB2 20                                                                                                                                                                                                                                                               
set EUtranCellFDD=.*,UtranFreqRelation=.* utranFreqToQciProfileRelation b2Thr2EcNoUtraFreqQciOffset:i=20,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                               
set EUtranCellFDD=.*,UtranFreqRelation=.* utranFreqToQciProfileRelation b2Thr1RsrpUtraFreqQciOffset:i=3,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*,UtranFreqRelation=.* utranFreqToQciProfileRelation b2Thr1RsrpUtraFreqQciOffset:i=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*,UtranFreqRelation=.* utranFreqToQciProfileRelation b2Thr2EcNoUtraFreqQciOffset:i=20,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                               
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,UtranFreqRelation=.* utranFreqToQciProfileRelation b2Thr1RsrpUtraFreqQciOffset:i=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                                  
done                                                                                                                                                                                                                                                                                                                                
set AntennaUnitGroup=.*,RfBranch=.* dlTrafficDelay -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1                                                                                                                                                                                                                                                                                
set AntennaUnitGroup=.*,RfBranch=.* ulTrafficDelay -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1                                                                                                                                                                                                                                                                                
set EUtrancell.*=.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5  20                                                                                                                                                                                                                                                               
set EUtrancell.*=.*,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5  480                                                                                                                                                                                                                                                           
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 triggerQuantityA5 0                                                                                                                                                                                                                                                            
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Utra=1 timeToTriggerB2 1280                                                                                                                                                                                                                                                       
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,UeMeasControl=1,ReportConfigB2Utra=1 timeToTriggerB2 640                                                                                                                                                                                                                                                         
done                                                                                                                                                                                                                                                                                                                                
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0                                                                                                                                                                                                                                                        
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 hysteresisA3 10                                                                                                                                                                                                                                                     
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 timeToTriggerA3 320                                                                                                                                                                                                                                                 
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1 triggerQuantityA3   0                                                                                                                                                                                                                                               
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 20                                                                                                                                                                                                                                                
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0                                                                                                                                                                                                                                                 
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480                                                                                                                                                                                                                                                  
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Critical 480                                                                                                                                                                                                                                                
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480                                                                                                                                                                                                                                                  
set EUtranCell.*=.*,UeMeasControl=1 measQuantityUtraFDD 1                                                                                                                                                                                                                                                                           
set EUtranCell.*=.*,UeMeasControl=1 inhibitB2RsrqConfig true                                                                                                                                                                                                                                                                        
set EUtranCell.*=.*,UeMeasControl=1 ueMeasurementsActive true                                                                                                                                                                                                                                                                       
set EUtranCell.*=.*,UeMeasControl=1 filterCoefficientEUtraRsrq 11                                                                                                                                                                                                                                                                   
set Paging=1 pagingDiscardTimerNb 3                                                                                                                                                                                                                                                                                                 
set Paging=1 pagingDiscardTimerDrxNb 3                                                                                                                                                                                                                                                                                              
set Rcs=1 tInactivityTimer 10                                                                                                                                                                                                                                                                                                       
set EUtraNetwork=1,ExternalENodeBFunction=.*,ExternalEUtranCellTDD=.* lbEUtranCellOffloadCapacity 1000                                                                                                                                                                                                                              
set EUtranCell pdcchCovImproveSrb false                                                                                                                                                                                                                                                                                             
set EUtranCell pdcchCovImproveDtx true                                                                                                                                                                                                                                                                                              
set EUtranCell pdcchCovImproveQci1 true                                                                                                                                                                                                                                                                                             
set EUtranCell pdcchTargetBlerVolte 4                                                                                                                                                                                                                                                                                               
set EUTRANCELLFDD ttiBundlingAfterHO 1                                                                                                                                                                                                                                                                                              
set EUTRANCELLFDD ttiBundlingSwitchThres 150                                                                                                                                                                                                                                                                                        
set EUTRANCELLTDD dlBlerTargetEnabled TRUE                                                                                                                                                                                                                                                                                          
set EUTRANCELLTDD tReorderingAutoConfiguration TRUE                                                                                                                                                                                                                                                                                 
set EUtranCellFDD cellDownlinkCaCapacity 0                                                                                                                                                                                                                                                                                          
set EUtranCellTDD hoOptStatTime 24                                                                                                                                                                                                                                                                                                  
set EUtranCell cfraEnable true                                                                                                                                                                                                                                                                                                      
set EUtranCell qRxLevMin -124                                                                                                                                                                                                                                                                                                       
set RlfProfile=1$ n311 1                                                                                                                                                                                                                                                                                                            
set Rrc=1 t304 2000                                                                                                                                                                                                                                                                                                                 
set Rrc=1 t311 5000                                                                                                                                                                                                                                                                                                                 
set Rrc=1 tRrcConnReest 2                                                                                                                                                                                                                                                                                                           
set Rrc=1 tWaitForRrcConnReest 9                                                                                                                                                                                                                                                                                                    
set Rrc=1 tRrcConnectionReconfiguration 10                                                                                                                                                                                                                                                                                          
##Rev6 Addition ##                                                                                                                                                                                                                                                                                                                  
crn ENodeBFunction=1,TimerProfile=0                                                                                                                                                                                                                                                                                                 
tWaitForRrcConnReest 6                                                                                                                                                                                                                                                                                                              
tRrcConnectionReconfiguration 8                                                                                                                                                                                                                                                                                                     
tRrcConnReest 3                                                                                                                                                                                                                                                                                                                     
tRelocOverall 10                                                                                                                                                                                                                                                                                                                    
end                                                                                                                                                                                                                                                                                                                                 
set TimerProfile=0 tRelocOverall 10                                                                                                                                                                                                                                                                                                 
set TimerProfile=0 tRrcConnReest 3                                                                                                                                                                                                                                                                                                  
set TimerProfile=0 tWaitForRrcConnReest 6                                                                                                                                                                                                                                                                                           
set TimerProfile=0 tRrcConnectionReconfiguration 8                                                                                                                                                                                                                                                                                  
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ timerProfileRef TimerProfile=0                                                                                                                                                                                                                                     
cr EnodeBfunction=1,PmFlexCounterFilter=1                                                                                                                                                                                                                                                                                           
set EnodeBfunction=1,PmFlexCounterFilter=1 qciFilterEnabled true                                                                                                                                                                                                                                                                    
set EnodeBFunction=1,PmFlexCounterFilter=1 qciFilterMax 1                                                                                                                                                                                                                                                                           
set EnodeBFunction=1,PmFlexCounterFilter=1 qciFilterMin 0                                                                                                                                                                                                                                                                           
set EUtranCell.*= srvccDelayTimer 3000                                                                                                                                                                                                                                                                                              
set ^Utrancellrelation loadBalancing 0                                                                                                                                                                                                                                                                                              
set Eutranfreqrelation mobilityAction 1                                                                                                                                                                                                                                                                                             
set ^Utranfreqrelation lbBnrPolicy 0                                                                                                                                                                                                                                                                                                
set ReportConfigB2Geran=1 b2Threshold2Geran -102                                                                                                                                                                                                                                                                                    
set Reportconfigb2geranultrig= b2Threshold2Geran -102                                                                                                                                                                                                                                                                               
set GeranFreqGroupRelation altCsfbTargetPrio 2                                                                                                                                                                                                                                                                                      
set GeranFreqGroupRelation mobilityActionCsfb 1                                                                                                                                                                                                                                                                                     
set GeranFreqGroupRelation mobilityAction 1                                                                                                                                                                                                                                                                                         
set EUtranCell.*=.*,GeranFreqGroupRelation= threshXLow 62                                                                                                                                                                                                                                                                           
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
    set $mordn,GeranFreqGroupRelation= threshXLow 10                                                                                                                                                                                                                                                                                
done                                                                                                                                                                                                                                                                                                                                
set EUtranCell.*=.*,GeranFreqGroupRelation= qRxLevMin -115                                                                                                                                                                                                                                                                          
Set GeranCellRelation coverageIndicator 1                                                                                                                                                                                                                                                                                           
seti ReportConfigB2Geran reportIntervalB2 4                                                                                                                                                                                                                                                                                         
set DrxProfile=0  drxRetransmissionTimer 4                                                                                                                                                                                                                                                                                          
set DrxProfile=1$  drxRetransmissionTimer 2                                                                                                                                                                                                                                                                                         
set DrxProfile=2  drxRetransmissionTimer 1                                                                                                                                                                                                                                                                                          
##END##                                                                                                                                                                                                                                                                                                                             
set EUtranCell.*=.*,UtranFreqRelation=.* utranFreqToQciProfileRelation b2Thr2RscpUtraFreqQciOffset:i=2                                                                                                                                                                                                                              
set EUtranCell.*=.*,UtranFreqRelation=.* utranFreqToQciProfileRelation b2Thr1RsrqUtraFreqQciOffset:i=0                                                                                                                                                                                                                              
set EUtranCell.*=.*,UtranFreqRelation=.* qQualMin -18                                                                                                                                                                                                                                                                               
seti EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 reportAmountB2 1                                                                                                                                                                                                                                                         
seti EUtranCellFDD=.*,UeMeasControl=1,ReportConfigB2Utra=1 reportIntervalB2 3                                                                                                                                                                                                                                                       
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ counterActiveMode False                                                                                                                                                                                                                                            
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ counterActiveMode False                                                                                                                                                                                                                                            
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ counterActiveMode FALSE                                                                                                                                                                                                                                            
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ counterActiveMode FALSE                                                                                                                                                                                                                                            
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ counterActiveMode FALSE                                                                                                                                                                                                                                            
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ counterActiveMode FALSE                                                                                                                                                                                                                                            
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dlMaxHARQTxQci 7                                                                                                                                                                                                                                                   
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ ulMaxHARQTxQci 7                                                                                                                                                                                                                                                   
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ harqPriority 1                                                                                                                                                                                                                                                     
set ENodeBFunction=1 dscpLabel 46                                                                                                                                                                                                                                                                                                   
set EUtranCell.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 0                                                                                                                                                                                                                                                    
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3                                                                                                                                                                                                      
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3                                                                                                                                                                                                      
##Extra suggested by Prajesh - 8 & 11 Feb2019 ##                                                                                                                                                                                                                                                                                    
set EUtranCell.*=.*,EUtranFreqRelation=.* eutranFreqToQciProfileRelation lbQciProfileHandling:i=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                                      
set EUtranCell.*=.*,UtranFreqRelation=.* utranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                                          
set EUtranCell.*=.*,EUtranFreqRelation=.* caTriggeredRedirectionActive false                                                                                                                                                                                                                                                        
set AnrFunction=1 cellRelHoAttRateThreshold 15                                                                                                                                                                                                                                                                                      
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrqQciOffset=8,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                                       
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellFDD=.*  systemInformationBlock6 tReselectionUtra:i=4                                                                                                                                                                                                                                                                  
set EUtranCellTDD=.*  systemInformationBlock6 tReselectionUtra:i=4                                                                                                                                                                                                                                                                  
set SystemFunctions=1,Lm=1,FeatureState=CXC4010620 featurestate 1                                                                                                                                                                                                                                                                   
##Extra suggested by Prajesh - 20 Feb2019 ##                                                                                                                                                                                                                                                                                        
set EUtranCellTDD=.*.,EUtranFreqRelation=1511 allowedMeasBandwidth 50
set EUtranCellTDD=.*.,EUtranFreqRelation=240 allowedMeasBandwidth 50                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*.,EUtranFreqRelation=39150 allowedMeasBandwidth 100                                                                                                                                                                                                                                                             
set EUtranCellTDD=.*.,EUtranFreqRelation=39294 allowedMeasBandwidth 50                                                                                                                                                                                                                                                              
set EUtranCellTDD=.*.,EUtranFreqRelation=3663 allowedMeasBandwidth 25                                                                                                                                                                                                                                                               
set EUtranCellFDD=.*.,EUtranFreqRelation=39150 allowedMeasBandwidth 100                                                                                                                                                                                                                                                             
set EUtranCellFDD=.*.,EUtranFreqRelation=3663 allowedMeasBandwidth 25                                                                                                                                                                                                                                                               
set EUtranCellFDD=.*.,EUtranFreqRelation=39294 allowedMeasBandwidth 50                                                                                                                                                                                                                                                              
set EUtranCellFDD=.*.,EUtranFreqRelation=1511 allowedMeasBandwidth 50                                                                                                                                                                                                                                                               
set EUtranCell.*=.*.,EUtranFreqRelation=39348 allowedMeasBandwidth 100                                                                                                                                                                                                                                                              
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn$ noOfPucchSrUsers 420                                                                                                                                                                                                                                                                                            
        set $mordn$ noOfPucchCqiUsers 128                                                                                                                                                                                                                                                                                           
done                                                                                                                                                                                                                                                                                                                                
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn$ noOfPucchSrUsers 160                                                                                                                                                                                                                                                                                            
        set $mordn$ noOfPucchCqiUsers 160                                                                                                                                                                                                                                                                                           
done                                                                                                                                                                                                                                                                                                                                
for $mo in T2                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn$ noOfPucchSrUsers 510                                                                                                                                                                                                                                                                                            
        set $mordn$ noOfPucchCqiUsers 170                                                                                                                                                                                                                                                                                           
done                                                                                                                                                                                                                                                                                                                                
for $mo in T1                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn$ noOfPucchSrUsers 190                                                                                                                                                                                                                                                                                            
        set $mordn$ noOfPucchCqiUsers 79                                                                                                                                                                                                                                                                                            
done                                                                                                                                                                                                                                                                                                                                
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn$ crsGain 0                                                                                                                                                                                                                                                                                                     
done                                                                                                                                                                                                                                                                                                                                
for $mo in T1                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                              
        set $mordn$ crsGain 0                                                                                                                                                                                                                                                                                                     
done                                                                                                                                                                                                                                                                                                                                
for $mo in T2                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn$ crsGain 300                                                                                                                                                                                                                                                                                                     
done                                                                                                                                                                                                                                                                                                                                
set LoadBalancingFunction=1   lbRateOffsetCoefficient 320                                                                                                                                                                                                                                                                           
set LoadBalancingFunction=1    lbRateOffsetLoadThreshold 1000                                                                                                                                                                                                                                                                       
set QciTable=default,QciProfilePredefined=qci1$    qciSubscriptionQuanta 60                                                                                                                                                                                                                                                         
set QciTable=default,QciProfilePredefined=qci2$    qciSubscriptionQuanta 384                                                                                                                                                                                                                                                        
set QciTable=default,QciProfilePredefined=qci5$    qciSubscriptionQuanta 1                                                                                                                                                                                                                                                          
set QciTable=default,QciProfilePredefined=qci6$    qciSubscriptionQuanta 200                                                                                                                                                                                                                                                        
set QciTable=default,QciProfilePredefined=qci7$    qciSubscriptionQuanta 200                                                                                                                                                                                                                                                        
set QciTable=default,QciProfilePredefined=qci8$    qciSubscriptionQuanta 200                                                                                                                                                                                                                                                        
set QciTable=default,QciProfilePredefined=qci9$    qciSubscriptionQuanta 200                                                                                                                                                                                                                                                        
set LoadBalancingFunction=1     lbCeiling 500                                                                                                                                                                                                                                                                                       
set LoadBalancingFunction=1     lbThreshold 20                                                                                                                                                                                                                                                                                      
set EUtranCellFDD=.*     cellSubscriptionCapacity 5000                                                                                                                                                                                                                                                                              
set EUtranCellTDD=.*     cellSubscriptionCapacity 24000                                                                                                                                                                                                                                                                             
for $mo in T1                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn$ cellSubscriptionCapacity 12000                                                                                                                                                                                                                                                                                  
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1       a5Threshold1Rsrp -140                                                                                                                                                                                                                                     
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1       a5Threshold1Rsrp -44                                                                                                                                                                                                                                        
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1       a5Threshold1Rsrp -140                                                                                                                                                                                                                                     
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1       a5Threshold2Rsrp -110                                                                                                                                                                                                                                     
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1       a5Threshold2Rsrp -109                                                                                                                                                                                                                                     
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1       a5Threshold2Rsrp -116                                                                                                                                                                                                                                       
done                                                                                                                                                                                                                                                                                                                                
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1       hysteresisA5 10                                                                                                                                                                                                                                            
set EUtranCell.*=.*,EUtranFreqRelation=.*,EUtranCellRelation=.* lbBnrAllowed      TRUE                                                                                                                                                                                                                                              
set EUtranCell.*=.*,EUtranFreqRelation=.*         lbBnrPolicy 2                                                                                                                                                                                                                                                                     
set LoadBalancingFunction=1     lbHitRateEUtranAddThreshold 5                                                                                                                                                                                                                                                                       
set LoadBalancingFunction=1     lbHitRateEUtranMeasUeIntensity 10                                                                                                                                                                                                                                                                   
set LoadBalancingFunction=1     lbHitRateEUtranMeasUeThreshold 10                                                                                                                                                                                                                                                                   
set LoadBalancingFunction=1     lbHitRateEUtranRemoveThreshold 2                                                                                                                                                                                                                                                                    
set LoadBalancingFunction=1     lbMeasScalingLimit 30                                                                                                                                                                                                                                                                               
set AutoCellCapEstFunction=1            useEstimatedCellCap TRUE                                                                                                                                                                                                                                                                    
set EUtranCellFDD=.*       cellCapMinMaxWriProt TRUE                                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*       cellCapMinMaxWriProt TRUE                                                                                                                                                                                                                                                                                
set EUtranCellTDD=.*     cellCapMinCellSubCap 200                                                                                                                                                                                                                                                                                   
for $mo in T2                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn$ cellCapMinCellSubCap 500                                                                                                                                                                                                                                                                                        
done                                                                                                                                                                                                                                                                                                                                
set EUtranCellFDD=.*     cellCapMaxCellSubCap 60000                                                                                                                                                                                                                                                                                 
set EUtranCellTDD=.*     cellCapMaxCellSubCap 60000                                                                                                                                                                                                                                                                                 
set SystemFunctions=1,Lm=1,FeatureState=CXC4011373 featureState 1                                                                                                                                                                                                                                                                   
set SystemFunctions=1,Lm=1,FeatureState=CXC4011370 featureState 1                                                                                                                                                                                                                                                                   
set SystemFunctions=1,Lm=1,FeatureState=CXC4011698 featureState 1                                                                                                                                                                                                                                                                   
set EUtranCellTDD=.*,EUtranFreqRelation=39150       lbA5Thr1RsrpFreqOffset 97                                                                                                                                                                                                                                                       
set EUtranCellTDD=.*,EUtranFreqRelation=39[2-3]       lbA5Thr1RsrpFreqOffset 97                                                                                                                                                                                                                                                     
set EUtranCellTDD=.*,EUtranFreqRelation=1511       lbA5Thr1RsrpFreqOffset 0                                                                                                                                                                                                                                                         
set EUtranCellFDD=.*,EUtranFreqRelation=39150       lbA5Thr1RsrpFreqOffset 97                                                                                                                                                                                                                                                       
set EUtranCellFDD=.*,EUtranFreqRelation=39[2-3]       lbA5Thr1RsrpFreqOffset 97                                                                                                                                                                                                                                                     
set EUtranCellFDD=.*,EUtranFreqRelation=1511       lbA5Thr1RsrpFreqOffset 36                                                                                                                                                                                                                                                        
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,EUtranFreqRelation=39150       lbA5Thr1RsrpFreqOffset 0                                                                                                                                                                                                                                                          
        set $mordn,EUtranFreqRelation=39[2-3]       lbA5Thr1RsrpFreqOffset 0                                                                                                                                                                                                                                                        
        set $mordn,EUtranFreqRelation=1511       lbA5Thr1RsrpFreqOffset 0                                                                                                                                                                                                                                                           
done                                                                                                                                                                                                                                                                                                                                
## harpreet update ##                                                                                                                                                                                                                                                                                                               
set EUtranCell.*=L.*,UeMeasControl=1                   ueMeasurementsActiveIF  true                                                                                                                                                                                                                                                 
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset:i=66,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1                                                                                                                                                                                                                                                                                                                  
crn ENodeBFunction=1,UlCompGroup=3                                                                                                                                                                                                                                                                                                  
administrativeState 1                                                                                                                                                                                                                                                                                                               
sectorCarrierRef ENodeBFunction=1,SectorCarrier=31 ENodeBFunction=1,SectorCarrier=32 ENodeBFunction=1,SectorCarrier=33                                                                                                                                                                                                              
end                                                                                                                                                                                                                                                                                                                                 
crn ENodeBFunction=1,UlCompGroup=1                                                                                                                                                                                                                                                                                                  
administrativeState 1                                                                                                                                                                                                                                                                                                               
sectorCarrierRef ENodeBFunction=1,SectorCarrier=1 ENodeBFunction=1,SectorCarrier=2 ENodeBFunction=1,SectorCarrier=3                                                                                                                                                                                                                 
end                                                                                                                                                                                                                                                                                                                                 
crn ENodeBFunction=1,UlCompGroup=5                                                                                                                                                                                                                                                                                                  
administrativeState 1                                                                                                                                                                                                                                                                                                               
sectorCarrierRef ENodeBFunction=1,SectorCarrier=7 ENodeBFunction=1,SectorCarrier=8 ENodeBFunction=1,SectorCarrier=9                                                                                                                                                                                                                 
end                                                                                                                                                                                                                                                                                                                                 
crn ENodeBFunction=1,UlCompGroup=4                                                                                                                                                                                                                                                                                                  
administrativeState 1                                                                                                                                                                                                                                                                                                               
sectorCarrierRef ENodeBFunction=1,SectorCarrier=4 ENodeBFunction=1,SectorCarrier=5 ENodeBFunction=1,SectorCarrier=6                                                                                                                                                                                                                 
end                                                                                                                                                                                                                                                                                                                                 
set AnrFunction=1,AnrFunctionEUtran=1                       anrInterFreqState 1                                                                                                                                                                                                                                                     
set AnrFunction=1,AnrFunctionUtran=1                        anrStateUtran     1                                                                                                                                                                                                                                                     
set EUtranCellFDD=.*                                 mobCtrlAtPoorCovActive true                                                                                                                                                                                                                                                    
set EUtranCellTDD=.*                                 mobCtrlAtPoorCovActive true                                                                                                                                                                                                                                                    
set EUtranCellFDD mappingInfo mappingInfoSIB5:i=3                                                                                                                                                                                                                                                                                   
set EUtranCellTDD mappingInfo mappingInfoSIB5:i=3                                                                                                                                                                                                                                                                                   
set LM=1,featurestate=CXC4011345 featureState 1                                                                                                                                                                                                                                                                                     
set LM=1,featurestate=CXC4010974 featureState 1                                                                                                                                                                                                                                                                                     
set . problematicCellPolicy 2                                                                                                                                                                                                                                                                                                       
set EUtranCellFDD systemInformationBlock6 tReselectionUtra:i=4                                                                                                                                                                                                                                                                      
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Utra=1 timeToTriggerB2 1280                                                                                                                                                                                                                                                       
set AnrFunction=1 problematicCellPolicy 2                                                                                                                                                                                                                                                                                           
set EUtraNetwork=1,ExternalENodeBFunction=.*,ExternalEUtranCellTDD=.* lbEUtranCellOffloadCapacity 1000                                                                                                                                                                                                                              
set AnrFunction=1,AnrFunctionEUtran=1                       anrInterFreqState 1                                                                                                                                                                                                                                                     
set AnrFunction=1,AnrFunctionUtran=1                        anrStateUtran     1                                                                                                                                                                                                                                                     
set EUtranCellTDD=.*,UeMeasControl=1                excludeInterFreqAtCritical true                                                                                                                                                                                                                                                 
set EUtranCellFDD=.*,UeMeasControl=1                excludeInterFreqAtCritical false                                                                                                                                                                                                                                                
set EUtranCellTDD=.*,UeMeasControl=1                csfbHoTargetSearchTimer 1200                                                                                                                                                                                                                                                    
set EUtranCellFDD=.*,UeMeasControl=1                csfbHoTargetSearchTimer 1200                                                                                                                                                                                                                                                    
set EUtranCellTDD=.*,UeMeasControl=1                  ueMeasurementsActiveGERAN False                                                                                                                                                                                                                                               
set  AdmissionControl=1                                      admNrRbDifferentiationThr 750                                                                                                                                                                                                                                          
set AdmissionControl=1                                      admNrRrcDifferentiationThr 750                                                                                                                                                                                                                                          
set AnrFunction=1                                           cellRelHoAttRateThreshold 15                                                                                                                                                                                                                                            
set QciTable=default,QciProfilePredefined=qci1$              dlMaxHARQTxQci    7                                                                                                                                                                                                                                                    
set QciTable=default,QciProfilePredefined=qci1$              ulMaxHARQTxQci    7                                                                                                                                                                                                                                                    
set EUtranCellTDD=.*,UtranFreqRelation=10657, isRemoveAllowed   true                                                                                                                                                                                                                                                                
set EUtranCellFDD=.*,UtranFreqRelation=10657, isRemoveAllowed   true                                                                                                                                                                                                                                                                
set EUtranCell.*=                                  advCellSupAction  2                                                                                                                                                                                                                                                              
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigCsfbUtra=1 thresholdEcNo     -160                                                                                                                                                                                                                                                  
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigCsfbUtra=1 thresholdEcNo     -160                                                                                                                                                                                                                                                  
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigCsfbUtra=1 thresholdRscp     -109                                                                                                                                                                                                                                                  
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigCsfbUtra=1 thresholdRscp     -109                                                                                                                                                                                                                                                  
set EUtranCellFDD=.*,          b2Thr2EcNoUtraFreqOffset 0                                                                                                                                                                                                                                                                           
set EUtranCellTDD=.*,          b2Thr2EcNoUtraFreqOffset 0                                                                                                                                                                                                                                                                           
set EUtranCellFDD=.*,           b2Thr1RsrpUtraFreqOffset 0                                                                                                                                                                                                                                                                          
set EUtranCellTDD=.*,           b2Thr1RsrpUtraFreqOffset 0                                                                                                                                                                                                                                                                          
set EUtranCellFDD=.*                                   preambleInitialReceivedTargetPower -110                                                                                                                                                                                                                                      
set EUtranCellTDD=.*                                   preambleInitialReceivedTargetPower -110                                                                                                                                                                                                                                      
set EUtranCellFDD=.*                                   enableSinrUplinkClpc true                                                                                                                                                                                                                                                    
set EUtranCellTDD=.*                                   enableSinrUplinkClpc true                                                                                                                                                                                                                                                    
set EUtranCellFDD=.*                                   pdcchLaGinrMargin 40                                                                                                                                                                                                                                                         
set EUtranCellTDD=.*                                   pdcchLaGinrMargin 40                                                                                                                                                                                                                                                         
set EUtranCellFDD=.*,UeMeasControl=1                   ueMeasurementsActiveUTRAN true                                                                                                                                                                                                                                               
set EUtranCellTDD=.*,UeMeasControl=1                   ueMeasurementsActiveUTRAN true                                                                                                                                                                                                                                               
##Rev5 Addition##                                                                                                                                                                                                                                                                                                                   
set QciTable=default,QciProfilePredefined=qci6$    dscp 26                                                                                                                                                                                                                                                                          
set QciTable=default,QciProfilePredefined=qci7$    dscp 26                                                                                                                                                                                                                                                                          
set QciTable=default,QciProfilePredefined=qci8$    dscp 26                                                                                                                                                                                                                                                                          
set QciTable=default,QciProfilePredefined=qci9$    dscp 26                                                                                                                                                                                                                                                                          
set QciTable=default,QciProfilePredefined=qci6$    schedulingAlgorithm 4                                                                                                                                                                                                                                                            
set QciTable=default,QciProfilePredefined=qci7$    schedulingAlgorithm 4                                                                                                                                                                                                                                                            
set QciTable=default,QciProfilePredefined=qci8$    schedulingAlgorithm 4                                                                                                                                                                                                                                                            
set QciTable=default,QciProfilePredefined=qci9$    schedulingAlgorithm 4                                                                                                                                                                                                                                                            
set ^EUtranCellTDD subframeAssignment 2                                                                                                                                                                                                                                                                                             
set EUtranCell.*= systemInformationBlock7 tReselectionGeran:i=2                                                                                                                                                                                                                                                                     
##################################END###########################                                                                                                                                                                                                                                                                    
##Rev11 Addition- Suggested by Circle MS,SEP2.0 in May-2021##                                                                                                                                                                                                                                                                       
set .  hysteresisA1A2SearchRsrq    10                                                                                                                                                                                                                                                                                               
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -170                                                                                                                                                                                                                                              
set EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -160                                                                                                                                                                                                                                              
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
        set $mordn,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrq -150                                                                                                                                                                                                                                                
done                                                                                                                                                                                                                                                                                                                                
set .  a2CriticalThrQci1RsrqOffset    -100                                                                                                                                                                                                                                                                                          
set .  hysteresisA2CriticalRsrq    100                                                                                                                                                                                                                                                                                              
set .  inhibitA2SearchConfig 0                                                                                                                                                                                                                                                                                                      
set .  timeToTriggerA1SearchRsrq    1024                                                                                                                                                                                                                                                                                            
set .  timeToTriggerA2CriticalRsrq    1024                                                                                                                                                                                                                                                                                          
set .  timeToTriggerA2SearchRsrq    1024                                                                                                                                                                                                                                                                                            
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -160                                                                                                                                                                                                                                                         
for $mo in F8                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrq  -140                                                                                                                                                                                                                                                                  
done                                                                                                                                                                                                                                                                                                                                
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -160                                                                                                                                                                                                                                                         
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
set $mordn,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrq  -170                                                                                                                                                                                                                                                                  
done                                                                                                                                                                                                                                                                                                                                
set .  timeToTriggerA5Rsrq    1024                                                                                                                                                                                                                                                                                                  
for $mo in F3                                                                                                                                                                                                                                                                                                                       
    $mordn = rdn($mo)                                                                                                                                                                                                                                                                                                               
set $mordn,EUtranFreqRelation=39.* a5Thr1RsrqFreqOffset 10                                                                                                                                                                                                                                                                          
set $mordn,EUtranFreqRelation=36.* a5Thr2RsrqFreqOffset 10                                                                                                                                                                                                                                                                          
done                                                                                                                                                                                                                                                                                                                                
set EUtranCell.*=.*,EUtranFreqRelation=.* eutranFreqToQciProfileRelation  a5Thr1rsrqFreqQciOffset=0                                                                                                                                                                                                                                 
set EUtranCell.*=.*,EUtranFreqRelation=.* eutranFreqToQciProfileRelation  a5Thr2rsrqFreqQciOffset=290                                                                                                                                                                                                                               
set ,ReportConfigB2Geran=1  b2Threshold1Rsrq  -195                                                                                                                                                                                                                                                                                  
set ,ReportConfigB2Geran=1  hysteresisB2  20                                                                                                                                                                                                                                                                                        
set ,ReportConfigB2Geran=1  hysteresisB2RsrqOffset  100                                                                                                                                                                                                                                                                             
set ,ReportConfigB2Utra=1  b2Threshold1Rsrq  -195                                                                                                                                                                                                                                                                                   
set ,ReportConfigB2Utra=1  hysteresisB2RsrqOffset  100                                                                                                                                                                                                                                                                              
set ,ReportConfigB2Utra=1  b2Threshold2RscpUtra  -95                                                                                                                                                                                                                                                                                
set  EUtranCell.*=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrq  -170                                                                                                                                                                                                                                          
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=default ResourceAllocationStrategy 1                                                                                                                                                                                                                                     
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 ResourceAllocationStrategy 1                                                                                                                                                                                                                                        
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 ResourceAllocationStrategy 1                                                                                                                                                                                                                                        
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3 ResourceAllocationStrategy 1                                                                                                                                                                                                                                        
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4 ResourceAllocationStrategy 1                                                                                                                                                                                                                                        
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 ResourceAllocationStrategy 1                                                                                                                                                                                                                                        
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6 ResourceAllocationStrategy 1                                                                                                                                                                                                                                        
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7 ResourceAllocationStrategy 1                                                                                                                                                                                                                                        
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8 ResourceAllocationStrategy 1                                                                                                                                                                                                                                        
set ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9 ResourceAllocationStrategy 1                                                                                                                                                                                                                                        
set QciTable=default,QciProfilePredefined=qci6$ dataFwdPerQciEnabled true                                                                                                                                                                                                                                                           
set QciTable=default,QciProfilePredefined=qci7$ dataFwdPerQciEnabled true                                                                                                                                                                                                                                                           
set QciTable=default,QciProfilePredefined=qci8$ dataFwdPerQciEnabled true                                                                                                                                                                                                                                                           
set QciTable=default,QciProfilePredefined=qci9$ dataFwdPerQciEnabled true                                                                                                                                                                                                                                                           
##################################END###########################                                                                                                                                                                                                                                                                    
##Rev11 Addition- Suggested by Circle MS@ June-21##                                                                                                                                                                                                                                                                                 
set ,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp -140                                                                                                                                                                                                                                                                     
set ,UeMeasControl=1,ReportConfigB2Geran=1  b2Threshold1Rsrp  -140                                                                                                                                                                                                                                                                  
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
set Router=.*,InterfaceIPv4= egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                                                         
set Router=.*,InterfaceIPv4= ingressQosMarking QosProfiles=1,DscpPcpMap=1                                                                                                                                                                   
set VlanPort=  egressQosMarking  QosProfiles=1,DscpPcpMap=1                                                                                                    
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
ipAddress Transport=1,Router=LTEUP,InterfaceIPv4=TN_C_UP,AddressIPv4=TN_C_UP
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
localIpAddress Transport=1,Router=LTECP,InterfaceIPv4=TN_C_CP,AddressIPv4=TN_C_CP
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
upIpAddressRef Transport=1,Router=LTEUP,InterfaceIPv4=TN_C_UP,AddressIPv4=TN_C_UP
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

set 0 Userlabel {Phy SiteID/Userlabel}

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
###################################### TN SCRIPT ######################################

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
ipAddress Router=LTEUP,InterfaceIPv4=TN_E_UP,AddressIPv4=TN_E_UP
udpPort 4001
userLabel
end

crn Transport=1,Router=LTEUP,TwampResponder=3
ipAddress Router=LTEUP,InterfaceIPv4=TN_E_UP,AddressIPv4=TN_E_UP
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
localIpAddress Transport=1,Router=LTECP,InterfaceIPv4=TN_E_CP,AddressIPv4=TN_E_CP
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end

crn Transport=1,SctpEndpoint=X2_ENDC
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end

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

crn Transport=1,SctpEndpoint=F1_NRCUCP
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end

crn Transport=1,SctpEndpoint=F1_NRDU
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end

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
gNBId 28030291
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
gNBId 28030291
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
gNBId 28030291
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

###############################Cell Specific Started -- NRCellCU={gUtranCell}############################
{AS_GNBCUCPFunction}
##################################Cell Specific Ended-- NRCellCU={gUtranCell}############################




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

###############################Cell Specific Started -- NRCellDU={gUtranCell}############################
{AS_GNBDUFunction}
###############################Cell Specific Ended -- NRCellDU={gUtranCell}############################

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


AS_NR_GPL_LMS_script = """

"""

AS_GNBCUCPFunction=""" 
crn GNBCUCPFunction=1,NRCellCU={gUtranCell}
admissionLimitRef GNBCUCPFunction=1,AdmissionControl=1,AdmissionLimit=Default
admissionPriorityRef GNBCUCPFunction=1,AdmissionControl=1,AdmissionPriority=Default
advUePosMode 0
caCellMeasProfileRef CarrierAggregation=1,CaCellMeasProfile=Default
caCellProfileRef CarrierAggregation=1,CaCellProfile=Default
cellLocalId 311
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
"""

AS_GNBDUFunction = """
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
"""