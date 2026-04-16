from mailapp.tasks import send_email
import pandas as pd
 
def send_email_for_Alarm(df_combined_dict, output_path):
    """Sends a detailed alarm email showing Locked/Unlocked cells per Circle."""
 
    df_combined = pd.DataFrame(df_combined_dict)
    def extract_matched_cells(val):
        if pd.isna(val) or val == "":
            return ("", "")
        parts = str(val).split("|")
        if len(parts) == 2:
            return parts[0], parts[1]
        return ("", "")
 
    df_combined[["Matched_old", "Matched_new"]] = df_combined["Matched_Cells"].apply(
        lambda x: pd.Series(extract_matched_cells(x))
    )

    for i in ['Site ID_old','Cells_old']:
        if i not in df_combined.columns:
            df_combined[i] = ""
 
    circle_to_emails = {
        "KK": [
            'Karamalla.Valli@ust.com','Rahul.Charak@ust.com',
            'Aashish.Sharma@ust.com'
        ],
        "AP": [
            'Rahul.Charak@ust.com','Aashish.Sharma@ust.com','Pankaj.Singh@ust.com','Ramesh.ThodaDurga@ust.com',
            'SattaChandra.Shekar@ust.com','LingisettyVenkata.Kumar@ust.com','RudraHari.Krishna@ust.com'
        ],
        "NESA" or "AS": [
            'Rahul.Charak@ust.com','Aashish.Sharma@ust.com','Mohit.Kumar@ust.com','Manoj.Kumar3@ust.com'
        ],
        "DEL": [
            'Nishant.Sharma2@ust.com','Vijay.Kumar2@ust.com',
            'Prateek.Saxena@ust.com','Deepu.Sharma@ust.com'
        ],
        "JK" :['Rahul.Charak@ust.com','Aashish.Sharma@ust.com','Manik.Mahajan@ust.com',
            'Lalit.Kaul@ust.com','Suman.Raman@ust.com','Namandeep.Singh@ust.com'
        ],
        "ROTN" or "CHN": ['A.Hariharasudhan@ust.com','Ajith.Thiyagarajesh@ust.com'],
 
        "HRY": ['Manoj.Kumar5@ust.com',"Umair.Wali@ust.com","Anil.Sharma@ust.com","Somnath.OmParkash@ust.com"],
        "UPW" :['Sanjay.Pandey2@ust.com','Shivam.Mittal@ust.com','Shubham.Gupta2@ust.com'],
        "RAJ" :['Raju.Maheshwari@ust.com','Manoj.Vishwakarma@ust.com','Pushkar.VimaljaKantShukla@ust.com']
    }
 
    cc_mails = [
        'Mohit.Batra@ust.com',
        'Deepak.KumarYadav@ust.com','Amit.rai@ust.com','Lalit.Namdev2@ust.com','Shashank.Rai@ust.com',
        'Krishna.KantVerma@ust.com','Saurabh.Rathore@ust.com',"Vishal.Yadav@ust.com",'Praveen.lakra@ust.com',
        'Chirag.bohra@ust.com','Gulafsha.Bano@ust.com','Priyanshi.sharma@ust.com','Deepu.Sharma@ust.com'
    ]
 
    cc_email = ";".join(cc_mails)
 
 
    def get_remark(row):
        old_state = str(row.get("4G Cell Status - Adm State_old", "")).strip().lower()
        new_state = str(row.get("4G Cell Status - Adm State_new", "")).strip().lower()
 
        matched_old = str(row.get("Matched_old", "")).strip()
        matched_new = str(row.get("Matched_new", "")).strip()
 
        if matched_old != "" and matched_new != "":
            if old_state == "locked" and new_state == "locked":
                return "old/new locked"
            if old_state == "unlocked" and new_state == "unlocked":
                return "old/new unlocked"
            return ""
 
        if old_state == "" and new_state == "locked":
            return "old down/new locked"
        if old_state == "" and new_state == "unlocked":
            return "old down/new unlocked"
        if old_state == "locked" and new_state == "":
            return "old locked/new down"
        if old_state == "unlocked" and new_state == "":
            return "old unlocked/new down"
        return ""
 
    df_combined["Remark"] = df_combined.apply(get_remark, axis=1)
 
    # df_combined.to_excel("debug_combined.xlsx", index=False)
 
 
    # SUMMARY TABLE (Matched only)
 
    df_matched = df_combined[df_combined["Remark"].isin(["old/new locked", "old/new unlocked"])].copy()
 
    # Circles that actually exist in the dataframe
    circles_in_data = df_combined["Circle"].unique().tolist()
    full_summary = pd.DataFrame({"Circle": circles_in_data})
 
    if not df_matched.empty:
        matched_summary = (
            df_matched.groupby("Circle")["Remark"]
            .value_counts()
            .unstack(fill_value=0)
            .reset_index()
        )
 
    # Ensure both columns exist
        for col in ["old/new locked", "old/new unlocked"]:
            if col not in matched_summary.columns:
                matched_summary[col] = 0
 
    # Total impacted sites
        total_sites = (
            df_matched.groupby("Circle")["Site ID_old"]
            .nunique()
            .reset_index(name="Total Impacted Sites")
        )
 
        matched_summary = matched_summary.merge(total_sites, on="Circle", how="left")
 
    else:
        # If no matched rows, create an empty summary
        matched_summary = pd.DataFrame(columns=[
            "Circle", "old/new locked", "old/new unlocked", "Total Impacted Sites"
        ])
 
# Final merge ensuring only data circles are shown
 
    matched_summary = (
        full_summary.merge(matched_summary, on="Circle", how="left")
        .fillna({
            "old/new locked": 0,
            "old/new unlocked": 0,
            "Total Impacted Sites": 0
        })
    )
 
# DOWN/UP CASES TABLE
 
    down_cases_list = [
        "old down/new locked", "old down/new unlocked",
        "old locked/new down", "old unlocked/new down",
        "new down/old locked", "new down/old unlocked",
        "new locked/old down", "new unlocked/old down"
    ]
    df_down_cases = df_combined[df_combined["Remark"].isin(down_cases_list)].copy()
 
# HTML TABLES
 
    def generate_matched_summary_html(df):
        if df.empty:
            return """
            <div style='background:#f0f7ff;
                        border-left:4px solid #007BFF;
                        padding:12px 18px;
                        margin-bottom:20px;
                        border-radius:6px;'>
                <p style='margin:0; color:#003d80; font-size:14px;'>
                    ..............There has no any both locked and both unlocked Summary.............
                </p>
            </div>
        """
 
        html = """
        <h3> Alarm Summary</h3>
        <table border="1" style="border-collapse: collapse; width:50%;">
            <thead style="background-color:#444; color:white;">
                <tr>
                    <th>Circle</th>
                    <th>Total Locked cell(Old/New)</th>
                    <th>Total Unlocked cell(Old/New)</th>
                    <th>Total Impacted Sites</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, r in df.iterrows():
            html += f"""
            <tr style="text-align:center;">
                <td>{r['Circle']}</td>
                <td>{r['old/new locked']}</td>
                <td>{r['old/new unlocked']}</td>
                <td>{r['Total Impacted Sites']}</td>
            </tr>
            """
        html += "</tbody></table>"
        return html
    valid_remarks = ["old/new locked", "old/new unlocked"]
    table_df = df_combined[df_combined["Remark"].isin(valid_remarks)][["Circle", "Site ID_old", "Cells_old", "Site ID_new", "Cells_new", "Remark"]].copy()
 
    # table_df.to_excel("debug_table_df.xlsx", index=False)
   
    def generate_matched_details_html(df):
        if table_df.empty:
            return """
            <div style='background:#f0f7ff;
                        border-left:4px solid #007BFF;
                        padding:12px 18px;
                        margin-bottom:20px;
                        border-radius:6px;'>
                <p style='margin:0; color:#003d80; font-size:14px;'>
                    ...........There has no any both locked and both unlocked Sites...........
                </p>
            </div>
        """
        html = """
        <h3>📋 Alarm Details (Old/New)</h3>
        <table border="1" style="border-collapse: collapse; width:95%;">
            <thead style="background-color:#444; color:white;">
                <tr>
                    <th>Circle</th><th>Old Site</th><th>Old Cell</th>
                    <th>New Site</th><th>New Cell</th><th>Remark</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, r in table_df.iterrows():
            color = "#ffcccc" if r["Remark"] == "old/new locked" else "#ccffcc"
            text_color = "#D9534F" if r["Remark"] == "old/new locked" else "#5cb85c"
            html += f"""
            <tr style="background-color:{color}; text-align:center;">
                <td>{r['Circle']}</td>
                <td>{r['Site ID_old']}</td>
                <td>{r.get('Cells_old', '')}</td>
                <td>{r['Site ID_new']}</td>
                <td>{r.get('Cells_new', '')}</td>
                <td style="color:{text_color}; font-weight:bold;">{r['Remark']}</td>
            </tr>
            """
        html += "</tbody></table>"
        return html
 
    def generate_down_cases_html(df_rows):
        if df_rows.empty:
            return "<p><b>No Down/Up cases found.</b></p>"
        html = """
        <h3>⚠️ Down/Up Status Cases (Old & New)</h3>
        <table border="1" style="border-collapse: collapse; width:95%;">
            <thead style="background-color:#444; color:white;">
                <tr>
                    <th>Circle</th><th>Old Site</th><th>Old Cell</th>
                    <th>New Site</th><th>New Cell</th><th>Remark</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, r in df_rows.iterrows():
            if "locked" in r["Remark"] and "down" in r["Remark"]:
                bg = "#ffcccc"; color = "#d9534f"
            elif "locked" in r["Remark"]:
                bg = "#ffdddd"; color = "#d9534f"
            else:
                bg = "#ccffcc"; color = "#5cb85c"
            html += f"""
            <tr style="background:{bg}; text-align:center;">
                <td>{r['Circle']}</td>
                <td>{r['Site ID_old']}</td>
                <td>{r.get('Cells_old','')}</td>
                <td>{r['Site ID_new']}</td>
                <td>{r.get('Cells_new','')}</td>
                <td style="color:{color}; font-weight:bold;">{r['Remark']}</td>
            </tr>
            """
        html += "</tbody></table>"
        return html
 
    Summary_html = generate_matched_summary_html(matched_summary)
    Alarm_details_html = generate_matched_details_html(df_matched)
    down_cases_html = generate_down_cases_html(df_down_cases)
 
 
    for circle, circle_df in df_combined.groupby("Circle"):
        if circle not in circle_to_emails:
            continue
        subject = f"🔔 4G Alarm Summary Report - {circle}"
 
        to_email = ";".join(circle_to_emails[circle])
        body = f"""
        <html>
        <body style="font-family:Arial; background-color:#f7f7f7; padding:20px;">
            <div style="background-color:white; padding:20px; border-radius:8px; border:1px solid black;">
                <h2 style="
                    color:#007BFF;
                    margin-top:0;
                    font-size:26px;
                    letter-spacing:0.5px;
                    border-bottom:2px solid #e3e3e3;
                    padding-bottom:10px;
                ">
                    🔔 Alarm Status Report — <span style="color:#333;">{circle}</span>
                </h2>
                {Summary_html}
                {Alarm_details_html}
                {down_cases_html}
                <div style="
                    margin-top:35px;
                    padding:15px;
                    background:#f7f7f7;
                    border-radius:6px;
                    font-size:13px;
                    color:#444;
                ">
                    <p><b>Note:</b> This is an automated system-generated email. Please do not reply.</p>
                    <p style="margin:5px 0 0 0;">Regards,<br>
                    <span style="color:#007BFF; font-weight:bold;">Developer Team</span></p>
                </div>
            </div>
        </body>
        </html>
        """
        try:
            print(f"📧 Sending email for {circle} → {to_email} (cc: {cc_email})")
            send_email(to_email, cc_email, subject, body, attachment_path=output_path, is_html=True)
            print(f"✅ Email sent successfully for {circle}")
        except Exception as e:
            print(f"❌ Failed to send email for {circle}: {e}")
       
 
# -------------------------------------------5G Alarm email function--------------------------------------------------
 
def send_email_for_5G_Alarm(df_combined_dict, output_path):
    """Sends a detailed alarm email showing Locked/Unlocked cells per Circle."""
 
    df_combined = pd.DataFrame(df_combined_dict)
    def extract_matched_cells(val):
        if pd.isna(val) or val == "":
            return ("", "")
        parts = str(val).split("|")
        if len(parts) == 2:
            return parts[0], parts[1]
        return ("", "")
 
    df_combined[["Matched_old", "Matched_new"]] = df_combined["Matched_Cells"].apply(
        lambda x: pd.Series(extract_matched_cells(x))
    )

    for i in ['Site ID_old','Cells_old']:
        if i not in df_combined.columns:
            df_combined[i] = ""
 
    circle_to_emails = {
        "KK": [
            'Karamalla.Valli@ust.com','Rahul.Charak@ust.com',
            'Aashish.Sharma@ust.com'
        ],
        "AP": [
            'Rahul.Charak@ust.com','Aashish.Sharma@ust.com','Pankaj.Singh@ust.com','Ramesh.ThodaDurga@ust.com',
            'SattaChandra.Shekar@ust.com','LingisettyVenkata.Kumar@ust.com','RudraHari.Krishna@ust.com'
        ],
        "NESA" or "AS": [
            'Rahul.Charak@ust.com','Aashish.Sharma@ust.com','Mohit.Kumar@ust.com','Manoj.Kumar3@ust.com'
        ],
        "DEL": [
            'Nishant.Sharma2@ust.com','Vijay.Kumar2@ust.com',
            'Prateek.Saxena@ust.com','Deepu.Sharma@ust.com'
        ],
        "JK" :['Rahul.Charak@ust.com','Aashish.Sharma@ust.com','Manik.Mahajan@ust.com',
            'Lalit.Kaul@ust.com','Suman.Raman@ust.com','Namandeep.Singh@ust.com'
        ],
        "ROTN" or "CHN": ['A.Hariharasudhan@ust.com','Ajith.Thiyagarajesh@ust.com'],
 
        "HRY": ['Manoj.Kumar5@ust.com',"Umair.Wali@ust.com","Anil.Sharma@ust.com","Somnath.OmParkash@ust.com"],
        "UPW" :['Sanjay.Pandey2@ust.com','Shivam.Mittal@ust.com','Shubham.Gupta2@ust.com'],
        "RAJ" :['Raju.Maheshwari@ust.com','Manoj.Vishwakarma@ust.com','Pushkar.VimaljaKantShukla@ust.com']
    }
 
    cc_mails = [
        'Mohit.Batra@ust.com',
        'Deepak.KumarYadav@ust.com','Amit.rai@ust.com','Lalit.Namdev2@ust.com','Shashank.Rai@ust.com',
        'Krishna.KantVerma@ust.com','Saurabh.Rathore@ust.com',"Vishal.Yadav@ust.com",'Praveen.lakra@ust.com',
        'Chirag.bohra@ust.com','Gulafsha.Bano@ust.com','Priyanshi.sharma@ust.com','Deepu.Sharma@ust.com'
    ]
 
 
    cc_email = ";".join(cc_mails)
 
 
    def get_remark(row):
        old_state = str(row.get("5G Cell Status - Adm State_old", "")).strip().lower()
        new_state = str(row.get("5G Cell Status - Adm State_new", "")).strip().lower()
 
        matched_old = str(row.get("Matched_old", "")).strip()
        matched_new = str(row.get("Matched_new", "")).strip()
 
        if matched_old != "" and matched_new != "":
            if old_state == "locked" and new_state == "locked":
                return "old/new locked"
            if old_state == "unlocked" and new_state == "unlocked":
                return "old/new unlocked"
            return ""
 
        if old_state == "" and new_state == "locked":
            return "old down/new locked"
        if old_state == "" and new_state == "unlocked":
            return "old down/new unlocked"
        if old_state == "locked" and new_state == "":
            return "old locked/new down"
        if old_state == "unlocked" and new_state == "":
            return "old unlocked/new down"
        return ""
 
    df_combined["Remark"] = df_combined.apply(get_remark, axis=1)
 
    # df_combined.to_excel("debug_combined.xlsx", index=False)
 
    # SUMMARY TABLE (Matched only)
 
    df_matched = df_combined[df_combined["Remark"].isin(["old/new locked", "old/new unlocked"])].copy()
 
    # Circles that actually exist in the dataframe
    circles_in_data = df_combined["Circle"].unique().tolist()
    full_summary = pd.DataFrame({"Circle": circles_in_data})
 
    if not df_matched.empty:
        matched_summary = (
            df_matched.groupby("Circle")["Remark"]
            .value_counts()
            .unstack(fill_value=0)
            .reset_index()
        )
 
        # Ensure both columns exist
        for col in ["old/new locked", "old/new unlocked"]:
            if col not in matched_summary.columns:
                matched_summary[col] = 0
 
        # Total impacted sites
        total_sites = (
            df_matched.groupby("Circle")["Site ID_old"]
            .nunique()
            .reset_index(name="Total Impacted Sites")
        )
 
        matched_summary = matched_summary.merge(total_sites, on="Circle", how="left")
 
    else:
        # If no matched rows, create an empty summary
        matched_summary = pd.DataFrame(columns=[
            "Circle", "old/new locked", "old/new unlocked", "Total Impacted Sites"
        ])
 
    # Final merge ensuring only data circles are shown
    matched_summary = (
        full_summary.merge(matched_summary, on="Circle", how="left")
        .fillna({
            "old/new locked": 0,
            "old/new unlocked": 0,
            "Total Impacted Sites": 0
        })
    )
 
    # DOWN/UP CASES TABLE
 
    down_cases_list = [
        "old down/new locked", "old down/new unlocked",
        "old locked/new down", "old unlocked/new down",
        "new down/old locked", "new down/old unlocked",
        "new locked/old down", "new unlocked/old down"
    ]
    df_down_cases = df_combined[df_combined["Remark"].isin(down_cases_list)].copy()
 
    # HTML TABLES
 
    def generate_matched_summary_html(df):
        if df.empty:
            return """
            <div style='background:#f0f7ff;
                        border-left:4px solid #007BFF;
                        padding:12px 18px;
                        margin-bottom:20px;
                        border-radius:6px;'>
                <p style='margin:0; color:#003d80; font-size:14px;'>
                    ...............There has no any both locked and both unlocked Summary..............
                </p>
            </div>
        """
        html = """
        <h3> Alarm Summary</h3>
        <table border="1" style="border-collapse: collapse; width:50%;">
            <thead style="background-color:#444; color:white;">
                <tr>
                    <th>Circle</th>
                    <th>Total Locked cell(Old/New)</th>
                    <th>Total Unlocked cell(Old/New)</th>
                    <th>Total Impacted Sites</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, r in df.iterrows():
            html += f"""
            <tr style="text-align:center;">
                <td>{r['Circle']}</td>
                <td>{r['old/new locked']}</td>
                <td>{r['old/new unlocked']}</td>
                <td>{r['Total Impacted Sites']}</td>
            </tr>
            """
        html += "</tbody></table>"
        return html
    valid_remarks = ["old/new locked", "old/new unlocked"]
    table_df = df_combined[
        df_combined["Remark"].isin(valid_remarks)
    ][["Circle", "Site ID_old", "Cells_old", "Site ID_new", "Cells_new", "Remark"]].copy()
 
    # table_df.to_excel("debug_table_df.xlsx", index=False)
   
    def generate_matched_details_html(df):
        if table_df.empty:
            return """
            <div style='background:#f0f7ff;
                        border-left:4px solid #007BFF;
                        padding:12px 18px;
                        margin-bottom:20px;
                        border-radius:6px;'>
                <p style='margin:0; color:#003d80; font-size:14px;'>
                    .............There has no any both locked and both unlocked Sites....................
                </p>
            </div>
        """
        html = """
        <h3>📋 Alarm Details (Old/New)</h3>
        <table border="1" style="border-collapse: collapse; width:95%;">
            <thead style="background-color:#444; color:white;">
                <tr>
                    <th>Circle</th><th>Old Site</th><th>Old Cell</th>
                    <th>New Site</th><th>New Cell</th><th>Remark</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, r in table_df.iterrows():
            color = "#ffcccc" if r["Remark"] == "old/new locked" else "#ccffcc"
            text_color = "#D9534F" if r["Remark"] == "old/new locked" else "#103c10"
            html += f"""
            <tr style="background-color:{color}; text-align:center;">
                <td>{r['Circle']}</td>
                <td>{r['Site ID_old']}</td>
                <td>{r.get('Cells_old', '')}</td>
                <td>{r['Site ID_new']}</td>
                <td>{r.get('Cells_new', '')}</td>
                <td style="color:{text_color}; font-weight:bold;">{r['Remark']}</td>
            </tr>
            """
        html += "</tbody></table>"
        return html
 
    def generate_down_cases_html(df_rows):
        if df_rows.empty:
            return "<p><b>There has no Down Sites .</b></p>"
        html = """
        <h3>⚠️ Down/Up Status Cases (Old & New)</h3>
        <table border="1" style="border-collapse: collapse; width:95%;">
            <thead style="background-color:#444; color:white;">
                <tr>
                    <th>Circle</th><th>Old Site</th><th>Old Cell</th>
                    <th>New Site</th><th>New Cell</th><th>Remark</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, r in df_rows.iterrows():
            if "locked" in r["Remark"] and "down" in r["Remark"]:
                bg = "#ffcccc"; color = "#eca8a5"
            elif "locked" in r["Remark"]:
                bg = "#ffdddd"; color = "#e9a29f"
            else:
                bg = "#ccffcc"; color = "#b9e4b9"
            html += f"""
            <tr style="background:{bg}; text-align:center;">
                <td>{r['Circle']}</td>
                <td>{r['Site ID_old']}</td>
                <td>{r.get('Cells_old','')}</td>
                <td>{r['Site ID_new']}</td>
                <td>{r.get('Cells_new','')}</td>
                <td style="color:{color}; font-weight:bold;">{r['Remark']}</td>
            </tr>
            """
        html += "</tbody></table>"
        return html
 
    Summary_html = generate_matched_summary_html(matched_summary)
    Alarm_details_html = generate_matched_details_html(df_matched)
    down_cases_html = generate_down_cases_html(df_down_cases)
 
    # EMAIL SENDING
 
    for circle, circle_df in df_combined.groupby("Circle"):
        if circle not in circle_to_emails:
            continue
        subject = f"🔔 5G Alarm Summary Report  - {circle}"
 
        to_email = ";".join(circle_to_emails[circle])
        body = f"""
        <html>
        <body style="font-family:Arial; background-color:#f7f7f7; padding:20px;">
            <div style="background-color:white; padding:20px; border-radius:8px; border:1px solid black;">
                <h2 style="
                    color:#007BFF;
                    margin-top:0;
                    font-size:26px;
                    letter-spacing:0.5px;
                    border-bottom:2px solid #e3e3e3;
                    padding-bottom:10px;
                ">
                    🔔 Alarm Status Report — <span style="color:#333;">{circle}</span>
                </h2>
 
                {Summary_html}
                {Alarm_details_html}
                {down_cases_html}
 
                <div style="
                    margin-top:35px;
                    padding:15px;
                    background:#f7f7f7;
                    border-radius:6px;
                    font-size:13px;
                    color:#444;
                ">
                    <p><b>Note:</b> This is an automated system-generated email. Please do not reply.</p>
                    <p style="margin:5px 0 0 0;">Regards,<br>
                    <span style="color:#007BFF; font-weight:bold;">Developer Team</span></p>
                </div>
            </div>
        </body>
        </html>
        """
        try:
            print(f"📧 Sending email for {circle} → {to_email} (cc: {cc_email})")
            send_email(to_email, cc_email, subject, body, attachment_path=output_path, is_html=True)
            print(f"✅ Email sent successfully for {circle}")
        except Exception as e:
            print(f"❌ Failed to send email for {circle}: {e}")