from mailapp.tasks import send_email
import pandas as pd

def send_email_for_Alarm(df_combined_dict , output_path):
    """
    Sends a summary email if multiple rows are either locked or unlocked,
    with colorful tables, status icons, and icons in the subject.
    """
    df_combined = pd.DataFrame(df_combined_dict)

    # Email recipients
    to_mails = ['Karamalla.Valli@ust.com','Nishant.Sharma2@ust.com','Saurabh.Rathore@ust.com',
                'Vijay.Kumar2@ust.com','Prateek.Saxena@ust.com','Amit.Rai@ust.com','Krishna.KantVerma@ust.com','Harsh.Rajender@ust.com','Deepu.Sharma@ust.com']
    cc_mails = ['Abhinav.Verma@ust.com', 'Prerna.PramodKumar@ust.com',
                'Mohit.Batra@ust.com','Deepak.KumarYadav@ust.com','','Vinay.Duklan@ust.com','Lalit.Namdev2@ust.com','Shashank.Rai@ust.com']
    
    # to_mails =['Abhinav.Verma@ust.com']
    # cc_mails = ['Prerna.PramodKumar@ust.com','Vinay.Duklan@ust.com']
    to_email = ";".join(to_mails)
    cc_email = ";".join(cc_mails)
    
    # Generate Remarks
    df_combined['Remark'] = df_combined.apply(lambda row: 
        "Locked" if row["4G Cell Status - Adm State_old"].lower() == "locked" and row["4G Cell Status - Adm State_new"].lower() == "locked"
        else ("Unlocked" if row["4G Cell Status - Adm State_old"].lower() == "unlocked" and row["4G Cell Status - Adm State_new"].lower() == "unlocked"
        else ""), axis=1)

    # Now filter only rows with meaningful remark
    locked_unlocked_rows = df_combined[df_combined['Remark'].isin(["Locked", "Unlocked"])]

    # Separate locked and unlocked rows
    # locked_unlocked_rows = df_combined[
    #     (df_combined["4G Cell Status - Adm State_old"].str.lower() == "locked") &
    #     (df_combined["4G Cell Status - Adm State_new"].str.lower() == "locked")&
    #     (df_combined["4G Cell Status - Adm State_old"].str.lower() == "unlocked")&
    #     (df_combined["4G Cell Status - Adm State_new"].str.lower() == "unlocked")
    # ]

    def generate_html_table(df_rows, table_color="#ffcccc", status_icon=""):
        """
        Generates a colorful HTML table with icons for email.
        """
        if df_rows.empty:
            return ""
    
        html = f"""
        <table style="border-collapse: collapse; width: 70%; font-family: Arial, sans-serif;">
            <thead>
                <tr style="background-color: {table_color}; color: #000; text-align: center;">
                    <th style="border: 1px solid #000; padding: 8px;">circle</th>
                    <th style="border: 1px solid #000; padding: 8px;">Old Site ID</th>
                    <th style="border: 1px solid #000; padding: 8px;">Old Cell</th>
                    <th style="border: 1px solid #000; padding: 8px;">New Site ID</th>
                    <th style="border: 1px solid #000; padding: 8px;">New Cell</th>
                    <th style="border: 1px solid #000; padding: 8px;">Remark</th>
                </tr>
            </thead>
            <tbody>
        """

        for i, row in df_rows.iterrows():
            if status_icon == "🔒":
                row_color = "#ffe6e6" if i % 2 == 0 else "#fff2f2"
            else:
                row_color = "#e6ffe6" if i % 2 == 0 else "#f2fff2"
            html += f"""
                <tr style="background-color: {row_color}; text-align: center;">
                    <td style="border: 1px solid #000; padding: 6px;">{row['Circle_old']}</td>
                    <td style="border: 1px solid #000; padding: 6px;">{row['Site ID_old']}</td>
                    <td style="border: 1px solid #000; padding: 6px;">{row['Cells_old']}</td>
                    <td style="border: 1px solid #000; padding: 6px;">{row['Site ID_new']}</td>
                    <td style="border: 1px solid #000; padding: 6px;">{row['Cells_new']}</td>
                    <td style="border: 1px solid #000; padding: 6px;">{row['Remark']}</td>

                </tr>
            """
        html += "</tbody></table>"
        return html

    # Send LOCKED email
    if not locked_unlocked_rows.empty:
        subject = "🔒 Alarm flag - Multiple sites LOCKED"
        body = f"""
        <p> <strong>both site LOCKED/ UNLOCKED</strong>:</p>
        {generate_html_table(locked_unlocked_rows, table_color="#DE5B64")}
        <p>Please review the details and take necessary action.</p>
        <p><em>Note: This is an automated email. Do not reply.</em></p>
        <p>Regards,<br>Developer Team</p>
        """
        try:
            print("Sending LOCKED email...")
            send_email.delay(
                    to_email,
                    cc_email,
                    subject,
                    body,
                    attachment_path=output_path,
                    is_html=True
                )            
            print("Locked email sent.")
        except Exception as e:
            print(f"Failed to send locked email: {e}")

# import pandas as pd
# from mailapp.tasks import send_email

# def send_email_for_Alarm(df_combined_dict, output_path):
#     df_combined = pd.DataFrame(df_combined_dict)

#     # Email recipients
#     to_mails = ['Abhinav.Verma@ust.com']
#     cc_mails = ['Prerna.PramodKumar@ust.com', 'Vinay.Duklan@ust.com']
#     to_email = ";".join(to_mails)
#     cc_email = ";".join(cc_mails)

#     # Function to check if two cells are similar based on suffix match
#     def cells_similar(cells_old, cells_new, suffix_length=8):
#         cells_old = str(cells_old).strip()
#         cells_new = str(cells_new).strip()
#         if not cells_old or not cells_new:
#             return False
#         match = cells_old[-suffix_length:] == cells_new[-suffix_length:]
#         print(f"Comparing Cells: OLD={cells_old}, NEW={cells_new}, Match={match}")
#         return match

#     # Function to generate Remark column value
#     def get_remark(row):
#         old_cell = str(row.get("Cells_old", "")).strip()
#         new_cell = str(row.get("Cells_new", "")).strip()
#         old_state = str(row.get("5G Cell Status - Adm State_old", "")).strip().lower()
#         new_state = str(row.get("5G Cell Status - Adm State_new", "")).strip().lower()

#         if cells_similar(old_cell, new_cell, suffix_length=8):
#             if old_state == "locked" and new_state == "locked":
#                 print(f"✅ Locked Match: {old_cell} ↔ {new_cell}")
#                 return "Locked"
#             elif old_state == "unlocked" and new_state == "unlocked":
#                 print(f"✅ Unlocked Match: {old_cell} ↔ {new_cell}")
#                 return "Unlocked"
#         return ""

#     # Apply get_remark to dataframe
#     df_combined["Remark"] = df_combined.apply(get_remark, axis=1)

#     # Filter rows with Locked or Unlocked remark
#     locked_unlocked_rows = df_combined[df_combined["Remark"].isin(["Locked", "Unlocked"])]

#     # Function to generate HTML table for email body
#     def generate_html_table(df_rows):
#         if df_rows.empty:
#             return ""
#         html = """
#         <table style="border-collapse: collapse; width: 80%; font-family: Arial, sans-serif;">
#             <thead>
#                 <tr style="background-color: #ffcdd2; color: black;">
#                     <th style="border: 1px solid black; padding: 8px;">Circle</th>
#                     <th style="border: 1px solid black; padding: 8px;">Old Site ID</th>
#                     <th style="border: 1px solid black; padding: 8px;">Old Cell</th>
#                     <th style="border: 1px solid black; padding: 8px;">New Site ID</th>
#                     <th style="border: 1px solid black; padding: 8px;">New Cell</th>
#                     <th style="border: 1px solid black; padding: 8px;">Remark</th>
#                 </tr>
#             </thead>
#             <tbody>
#         """
#         for i, row in df_rows.iterrows():
#             bg_color = "#f8bbd0" if row['Remark'] == "Locked" else "#c8e6c9"
#             html += f"""
#                 <tr style="background-color: {bg_color}; text-align: center;">
#                     <td style="border: 1px solid black; padding: 6px;">{row.get('Circle_old', '')}</td>
#                     <td style="border: 1px solid black; padding: 6px;">{row.get('Site ID_old', '')}</td>
#                     <td style="border: 1px solid black; padding: 6px;">{row.get('Cells_old', '')}</td>
#                     <td style="border: 1px solid black; padding: 6px;">{row.get('Site ID_new', '')}</td>
#                     <td style="border: 1px solid black; padding: 6px;">{row.get('Cells_new', '')}</td>
#                     <td style="border: 1px solid black; padding: 6px;">{row.get('Remark', '')}</td>
#                 </tr>
#             """
#         html += "</tbody></table>"
#         return html

#     # Send email if there are locked/unlocked rows
#     if not locked_unlocked_rows.empty:
#         subject = "🔒 Alarm flag - Locked/Unlocked Sites Detected"
#         body = f"""
#         <p><strong>Sites with Locked or Unlocked states (based on Cell suffix match):</strong></p>
#         {generate_html_table(locked_unlocked_rows)}
#         <p>Please review and take action if required.</p>
#         <p><em>Note: This is an automated email. Do not reply.</em></p>
#         <p>Regards,<br>Developer Team</p>
#         """
#         try:
#             print("📤 Sending email...")
#             send_email.delay(
#                 to_email,
#                 cc_email,
#                 subject,
#                 body,
#                 attachment_path=output_path,
#                 is_html=True
#             )
#             print("✅ Email sent successfully.")
#         except Exception as e:
#             print(f"❌ Failed to send email: {e}")
#     else:
#         print("No locked/unlocked rows found; no email sent.")
