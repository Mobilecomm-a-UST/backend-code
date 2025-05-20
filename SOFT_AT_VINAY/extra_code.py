# exit()
    # circle_oem = request.data.get('circle_oem')
    # from_date=request.POST.get("from_date")
    # to_date=request.POST.get("to_date")
    # date=request.POST.get("date")
    # site_ID=request.POST.get("site_ID")

    
    # latest_date=Soft_At_Table.objects.latest('upload_date').upload_date

    # with connection.cursor() as cursor:
    #     if from_date != '' and to_date != '':
    #         from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    #         to_date= datetime.strptime(to_date, '%Y-%m-%d').date()
    #         # query= f"""select * from public."IntegrationTracker_integrationdata"
    #         # where "Integration_Date" between '{from_date}' and '{to_date}' and "Activity_Name" in ('UPGRADE', 'RELOCATION', 'ULS_HPSC', 'MACRO', '5G SECTOR ADDITION') """ 
    #         query = f"""select * from public."SOFT_AT_VINAY_soft_at_table"
    #                         where "soft_at_status" = 'ACCEPTED' and upload_date between '{from_date}' and '{to_date}'

    #                         union

    #                         select * from public."SOFT_AT_VINAY_soft_at_table"
    #                         where upload_date = '{latest_date}'"""
    #         if site_ID:
    #             query +=  f"""and "Site_ID" ='{site_ID}' """
    #         if circle:
    #             query +=  f"""and "CIRCLE" ='{circle}' """


    #     elif date !='':
    #         date=datetime.strptime(date, '%Y-%m-%d').date()
    #         # query= f"""select * from public."IntegrationTracker_integrationdata"
    #         # where "Integration_Date" = '{date}' and "Activity_Name" in ('UPGRADE', 'RELOCATION', 'ULS_HPSC', 'MACRO', '5G SECTOR ADDITION') """ 
    #         query = f""" select * from public."SOFT_AT_VINAY_soft_at_table"
    #                         where upload_date = '{date}'"""
    #         if site_ID:
    #             query +=  f"""and "Site_ID" ='{site_ID}' """
    #         if circle:
    #             query +=  f"""and "CIRCLE" ='{circle}' """
            
    #     else:
    #         query = f"""select * from public."SOFT_AT_VINAY_soft_at_table"
    #                         where "soft_at_status" = 'ACCEPTED' 

    #                         union

    #                         select * from public."SOFT_AT_VINAY_soft_at_table"
    #                         where upload_date = '{latest_date}'"""
    #         if site_ID:
    #             query +=  f"""and "Site_ID" ='{site_ID}' """
    #         if circle:
    #             query +=  f"""and "CIRCLE" ='{circle}' """
            

    #     cursor.execute(query)
    #     results = cursor.fetchall()




    def write_df_to_excel(wb, df):
    sheet = wb.sheets.active

    start_row = 2  # Start writing from row 2 (header in row 1)

    # Write data to the Excel sheet starting from row 2
    for r_idx, row in enumerate(df.values, start=start_row):
        for c_idx, value in enumerate(row, start=1):
            sheet.range((r_idx, c_idx)).value = value