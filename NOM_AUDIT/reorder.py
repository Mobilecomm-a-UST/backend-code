import pandas as pd
from NOM_AUDIT.technology_cells import (
    AP_technology_cell_dict,
    del_technology_cell,
    JK_technology_cell,
    RAJ_technology_cell,
)


def match_special_cells(pre_row, post_row):
    pre_special_cell = str(pre_row).split(",")[1].split("=")[-1].split("_")
    post_special_cell = str(post_row.MO).split(",")[1].split("=")[-1].split("_")

    pre_carrier_band = pre_special_cell[2]
    pre_sector = pre_special_cell[-1]
    post_carrier_band = post_special_cell[2]
    post_sector = post_special_cell[-1]

    if pre_carrier_band == post_carrier_band and pre_sector == post_sector:
        return list(post_row)
    else:
        if (pre_carrier_band in ['T1', 'T2'] and post_carrier_band in ['T1', 'T2']) and pre_sector == post_sector:
            return list(post_row)

    return None


def reorder_post_values(
    post_df, pre_df, start_point, circle, fdd_mapping_dict, tdd_mapping_dict
):
    # def reorder_post_values(post_df, pre_df, start_point, circle):
    matched_rows = []
    
    print(fdd_mapping_dict,"\n", tdd_mapping_dict)

    def match_row(pre_row, post_row, start_point, circle, freq):
        try:
            if pre_row != post_row.MO:
                if start_point in ["st cell"]:
                    first_two_for_del = str(pre_row).split(",")[1].split("=")[1][:2]
                    first_jk_letter = str(pre_row).split(",")[1].split("=")[1][0]
                    site_id = str(pre_row).split(",")[1].split("=")[-1]
                    last_letter = (
                        site_id[-1] if not site_id.endswith("1") else site_id[-2]
                    )
                    if circle == "AP":
                        site_id = str(pre_row).split(",")[1].split("=")[-1]
                        last_letter = (
                            site_id[-1] if not site_id.endswith("1") else site_id[-2]
                        )
                        cell_name = str(post_row.MO).split(",")[1].split("=")[1]
                        if last_letter in AP_technology_cell_dict.keys():
                            mapped_val = AP_technology_cell_dict[last_letter]
                            if (
                                mapped_val[0] in cell_name
                                and mapped_val[1] in cell_name
                            ):
                                return post_row
                        if "_" in pre_row and "_" in post_row.MO:
                            return match_special_cells(pre_row, post_row)
                    if circle == "DL":
                        if (
                            first_two_for_del in ["LD", "LU", "LM"]
                            and "_" not in str(pre_row).split(",")[1]
                        ):
                            # print("Enter into del circle")
                            pre_mo_start = str(pre_row).split(",")[1].split("=")[1][0]
                            pre_mo_last = str(pre_row).split(",")[1].split("=")[1][-1]
                            cell_name = str(post_row.MO).split(",")[1].split("=")[1]
                            if first_two_for_del in [
                                "LD",
                                "LU",
                                "LM",
                            ] and last_letter not in ["K", "L", "M", "N"]:
                                freq = "3676"
                                if last_letter in ["G", "H", "I", "J"]:
                                    mapped_val = del_technology_cell[freq][pre_mo_last]
                                    if (
                                        mapped_val[0] in cell_name
                                        and mapped_val[1] in cell_name
                                    ):
                                        return post_row
                                if last_letter in ["S", "T", "U", "V", "W", "X"]:
                                    freq = "39294"
                                    mapped_val = del_technology_cell[freq][pre_mo_last]
                                    if (
                                        mapped_val[0] in cell_name
                                        and mapped_val[1] in cell_name
                                    ):
                                        return post_row
                                if last_letter in ["A", "B", "C", "D", "E", "F"]:
                                    freq = "39150"
                                    mapped_val = del_technology_cell[freq][pre_mo_last]
                                    if (
                                        mapped_val[0] in cell_name
                                        and mapped_val[1] in cell_name
                                    ):
                                        return post_row
                                if last_letter in ["A", "B", "C", "D", "E", "F"]:
                                    freq = "39151"
                                    mapped_val = del_technology_cell[freq][pre_mo_last]
                                    if (
                                        mapped_val[0] in cell_name
                                        and mapped_val[1] in cell_name
                                    ):
                                        return post_row

                            elif first_two_for_del in [
                                "LD",
                                "LU",
                                "LM",
                            ] and last_letter in ["K", "L", "M", "N"]:
                                freq = freq
                                mapped_val = del_technology_cell[freq][pre_mo_last]
                                if (
                                    mapped_val[0] in cell_name
                                    and mapped_val[1] in cell_name
                                ):
                                    return post_row

                        elif "_" in pre_row and "_" in post_row.MO:
                            return match_special_cells(pre_row, post_row)

                    elif circle == "JK":
                        if (
                            first_jk_letter in ["L", "T", "F"]
                            and "_" not in str(pre_row).split(",")[1].split("=")[1]
                        ):
                            # print("enter into jk cell")
                            pre_mo_start = str(pre_row).split(",")[1].split("=")[1][0]
                            pre_row_parts = str(pre_row).split(",")
                            # pre_mo_last = str(pre_row).split(",")[1].split("=")[1][7:]
                            if len(pre_row_parts) > 1:
                                mo_value = pre_row_parts[1].split("=")
                                if len(mo_value) > 1:
                                    mo_string = mo_value[1]
                                    len_mo = len(mo_string)
                                    if mo_string[-1].isdigit():
                                        pre_mo_last = mo_string[-2:]
                                    else:
                                        pre_mo_last = mo_string[-1:]
                                    # print("Last part:", pre_mo_last)
                            cell_name = str(post_row.MO).split(",")[1].split("=")[1]
                            # print(pre_mo_start, pre_mo_last)
                            # print(cell_name)

                            if pre_mo_start == "L":
                                freq = "265"
                                if freq in JK_technology_cell.keys():
                                    mapped_cell = JK_technology_cell[freq].get(
                                        pre_mo_last
                                    )
                                    if (
                                        mapped_cell[0] in cell_name
                                        and mapped_cell[1] in cell_name
                                    ):
                                        return list(post_row)
                            elif pre_mo_start == "T":
                                freq = "39150"
                                if freq in JK_technology_cell.keys():
                                    mapped_cell = JK_technology_cell[freq].get(
                                        pre_mo_last
                                    )
                                    if (
                                        mapped_cell[0] in cell_name
                                        and mapped_cell[1] in cell_name
                                    ):
                                        return list(post_row)
                            elif pre_mo_start == "F":
                                freq = "1595"
                                if freq in JK_technology_cell.keys():
                                    mapped_cell = JK_technology_cell[freq].get(
                                        pre_mo_last
                                    )
                                    if (
                                        mapped_cell[0] in cell_name
                                        and mapped_cell[1] in cell_name
                                    ):
                                        return list(post_row)
                        elif "_" in pre_row and "_" in post_row.MO:
                            
                            return match_special_cells(pre_row, post_row)
                        
                    elif circle == "RAJ":
                        if "_" in pre_row and "_" in post_row.MO:
                            return match_special_cells(pre_row, post_row)

                        # print("enter into RAJ cell")
                        pre_mo_start = str(pre_row).split(",")[1].split("=")[1][0]
                        pre_row_parts = str(pre_row).split(",")
                        if len(pre_row_parts) > 1:
                            mo_value = pre_row_parts[1].split("=")
                            if len(mo_value) > 1:
                                mo_string = mo_value[1]
                                len_mo = len(mo_string)
                                if mo_string[-1].isdigit():
                                    pre_mo_last = mo_string[-2:]
                                else:
                                    pre_mo_last = mo_string[-1:]
                                # print("Last part:", pre_mo_last)
                        # len_mo = len(str(pre_row).split(",")[1].split("=")[1])
                        # pre_mo_last = str(pre_row).split(",")[1].split("=")[1][len_mo-1:] if not str(pre_row).split(",")[1].split("=")[1].isdigit() else str(pre_row).split(",")[1].split("=")[1][len_mo-2:]
                        cell_name = str(post_row.MO).split(",")[1].split("=")[1]
                        # print(pre_mo_start, pre_mo_last)
                        freq = freq
                        print("freq",freq)
                        if freq in RAJ_technology_cell.keys():
                            mapped_cell = RAJ_technology_cell[freq].get(pre_mo_last)
                            for i in mapped_cell:
                                print("mapped_cell", i)
                                print("cell_name",cell_name)
                                if i[0] in cell_name and i[1] in cell_name:
                                    print("post_row",list(post_row))
                                    return list(post_row)

                return None
            else:
                return list(post_row)
        except Exception as e:
            # print(f"Error occurred: {e}")
            return None

    if "MO" in pre_df.columns:
        for index, pre_row in enumerate(pre_df.MO):
            # print("pre_row", pre_row)
            freq = None

            if str(pre_row).split(",")[1].split("=")[0][10:] == "FDD":
                mo_name = str(pre_row).split(",")[1].split("=")[1]
                if mo_name in fdd_mapping_dict.keys():
                    freq = fdd_mapping_dict[mo_name]

            if str(pre_row).split(",")[1].split("=")[0][10:] == "TDD":
                mo_name = str(pre_row).split(",")[1].split("=")[1]
                if mo_name in tdd_mapping_dict.keys():
                    freq = tdd_mapping_dict[mo_name]

            try:
                matched = False
                for post_row in post_df.itertuples(index=False):
                    matched_row = match_row(
                        pre_row, post_row, start_point, circle, freq
                    )
                    if matched_row:
                        matched_rows.append(matched_row)
                        matched = True
                        break
                if not matched:
                    matched_rows.append([None] * len(post_df.columns))
            except Exception as e:
                # print(f"Error processing row {pre_row}: {e}")
                continue

    else:
        # print("The 'MO' column is missing in pre_df.")
        return None

    new_df = pd.DataFrame(matched_rows, columns=post_df.columns)
    return new_df
