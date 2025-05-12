import pandas as pd


class ExcelWriter:
    @staticmethod
    def write_to_excel(tables, output_file, node_id=None):
        output_file = ExcelWriter._generate_output_file_path(output_file, node_id)

        with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
            workbook = writer.book

            for sheet_name, commands in tables.items():
                sheet_name = sheet_name[:31]
                temp_dfs = []

                for command, data in commands.items():
                    if data:
                        df = ExcelWriter._process_command_data(
                            data, sheet_name, node_id
                        )
                        temp_dfs.append(df)

                if temp_dfs:
                    temp_df = pd.concat(temp_dfs, axis=0, ignore_index=True)
                    if sheet_name == "cell_data":
                        temp_df = pd.concat(temp_dfs, axis=1, ignore_index=True)
                    ExcelWriter._write_sheet_to_excel(
                        writer, workbook, sheet_name, temp_df
                    )

        print(f"✅ Excel file saved: {output_file}")

    @staticmethod
    def _generate_output_file_path(output_file, node_id):
        return "\\".join(
            [
                f"{node_id}_{val}" if val.endswith("xlsx") else val
                for val in output_file.split("\\")
            ]
        )

    @staticmethod
    def _process_command_data(data, sheet_name, node_id):
        columns = [col.strip() for col in data[0].split(";")]
        max_cols = len(columns)
        data = [row.split(";") for row in data[1:]]
        data = [[i.strip() for i in val] for val in data]
        data = [
            (
                row + [None] * (max_cols - len(row))
                if len(row) < max_cols
                else row[:max_cols]
            )
            for row in data
        ]

        df = pd.DataFrame(data, columns=columns)

        if sheet_name == "gpl-para":
            df = df.melt(
                id_vars=["MO"] if "MO" in df.columns else [],
                var_name="Parameter",
                value_name="Value",
            )

        if node_id:
            df.insert(0, "Node_ID", [node_id] * len(df))

        return df

    @staticmethod
    def _write_sheet_to_excel(writer, workbook, sheet_name, df):
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=True)

        worksheet = writer.sheets[sheet_name]
        header_format = workbook.add_format(
            {"bold": True, "bg_color": "#D7E4BC", "border": 1}
        )

        for col_num, col_data in enumerate(df.columns):
            worksheet.write(0, col_num, col_data, header_format)
            max_length = max(
                df[col_data].astype(str).str.len().max(skipna=True) or 0,
                len(str(col_data)),
            )
            worksheet.set_column(col_num, col_num, max_length + 2)

    @staticmethod
    def _apply_audit_formatting(workbook, worksheet, df):
        header_format = workbook.add_format(
            {
                "bold": True,
                "bg_color": "#000957",
                "border": 2,
                "font_color": "#ffffff",
                "align": "center",
                "valign": "vcenter",
            }
        )

        center_format = workbook.add_format({"align": "center", "valign": "center"})
        ok_format = workbook.add_format(
            {
                "bg_color": "#90EE90",
                "font_color": "#000000",
                "align": "center",
                "valign": "Center",
            }
        )
        not_ok_format = workbook.add_format(
            {
                "bg_color": "#FF6347",
                "font_color": "#FFFFFF",
                "align": "center",
                "valign": "Center",
            }
        )

        worksheet.set_row(0, 23)

        for col_num, col_name in enumerate(df.columns):
            worksheet.write(0, col_num, str(col_name), header_format)
            column_series = df[col_name]

            if isinstance(column_series, pd.DataFrame):
                column_series = column_series.iloc[:, 0]

            max_length = max(
                column_series.fillna("").astype(str).str.len().max(skipna=True) or 0,
                len(str(col_name)),
            )
            max_length = min(max_length, 255)
            worksheet.set_column(col_num, col_num, max_length + 5)

        for row_num in range(1, len(df) + 1):
            worksheet.set_row(row_num, 15)
            for col_num in range(len(df.columns)):
                cell_value = str(df.iloc[row_num - 1, col_num])
                format_style = center_format

                if cell_value == "OK":
                    format_style = ok_format
                elif cell_value == "NOT OK":
                    format_style = not_ok_format

                worksheet.write(row_num, col_num, cell_value, format_style)
