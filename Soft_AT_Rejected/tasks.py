# from celery import Celery
# from win32com.client import DispatchWithEvents
# import pythoncom
# import datetime
# from celery import shared_task
# from .utils import *
# # app = Celery('tasks', broker='pyamqp://guest@localhost//')
# from .views import *

# from UBR_Soft_Phy_AT_Rejection_App.utils import target_senders as ubr_target_senders
# import UBR_Soft_Phy_AT_Rejection_App.utils  as ubr_utils

# class OutlookEventHandler(object):
#     @staticmethod
#     def OnNewMailEx(EntryIDCollection):
#         for ID in EntryIDCollection.split(","):
#             item = Outlook.Session.GetItemFromID(ID)
#             if item.Class == 43:
#                 print(" current Time :           ",datetime.datetime.now())
#                 print("______________________mail item details_______________________")
#                 print(" SenderName :              " + item.SenderName)
#                 print(" Subject:                  " + item.Subject)
#                 print(" mail received time :      " + str(item.ReceivedTime))
#                 # print(" to: " + item.To)
#                 print(" Attachement Count :        ", item.Attachments.Count)
#                 print("________________________*******___________________________\n")
#                 # print("senderType...",type(item.SenderName))
                
#                 if item.SenderEmailAddress in target_senders:
#                     print("....Soft At Rejection App....")
#                     Soft_At_Rejection_Database_save(False,[item])
#                     print(".......task finished.........")
#                 if item.SenderEmailAddress in ubr_target_senders:
#                     print("....UBR Soft At Rejection App....")
#                     ubr_utils.UBR_Soft_AT_Rejected_save(False,[item])
#                     print(".......UBR task finished.........")
                    
                
# # @app.task
# # @shared_task
# # def outlook_listener():
# Outlook = DispatchWithEvents("Outlook.Application", OutlookEventHandler)
# olNs = Outlook.GetNamespace("MAPI")
# Inbox = olNs.GetDefaultFolder(6)
# pythoncom.PumpMessages()
    


# # if __name__ == "__main__":
# # outlook_listener()