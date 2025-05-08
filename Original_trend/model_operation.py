from models import *

unique_site_list=list(pre_post_report2.objects.values_list("Post_cell_site_id").distinct())
print(unique_site_list)

