from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from Zero_Count_Rna_Payload_Tool.models import Ticket_Counter_Table_Data
import uuid


# @receiver(pre_save, sender=Ticket_Counter_Table_Data)
# def set_ticket_id(sender, instance, **kwargs):
#     if not instance.ticket_id:
#         last_instance = Ticket_Counter_Table_Data.objects.order_by("-ticket_id").first()

#         if last_instance:
#             last_id = last_instance.ticket_id
#             last_num = int(last_id.split("_")[2])
#             new_num = last_num + 1
#         else:
#             new_num = 1

#         instance.ticket_id = f"MCPSINC_{(str(uuid.uuid4()).split('-')[1])[:3]}_00{new_num}"


@receiver(post_save, sender=Ticket_Counter_Table_Data)
def set_ticket_id(sender, instance, created, **kwargs):
    if created and not instance.ticket_id:
        last_instance = Ticket_Counter_Table_Data.objects.order_by("-ticket_id").first()

        if last_instance:
            last_id = last_instance.ticket_id
            last_num = int(last_id.split("_")[2])
            new_num = last_num + 1
        else:
            new_num = 1

        instance.ticket_id = f"MCPSINC_{(str(uuid.uuid4()).split('-')[1])[:3]}_00{new_num}"
        instance.save()