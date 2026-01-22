import os
import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime

class GplScriptGenerator(ABC):
    def __init__(self, mismatch_df: pd.DataFrame):
        """Initialize with mismatch DataFrame"""
        self.df = mismatch_df

    @abstractmethod
    def generate_commands(self):
        """Abstract method to generate AMOS commands"""
        pass

    def create_script(
        self,
        script_path: str,
        script_type: str,
        script_line: str,
        script_ender: str,
        node_id=None,
    ):
        """Creates the final script file with generated commands."""
        commands = self.generate_commands()
        if not commands:
            print("⚠ No commands generated. Check input DataFrame.")
            return

        # script_dir, script_file = os.path.split(script_path)
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = os.path.dirname(script_path)
        base_name = os.path.basename(script_path)

        if node_id:
            new_filename = (
                f"{node_id}_{base_name.replace('.txt', '')}_{current_datetime}.txt"
            )
        script_path = os.path.join(base_dir, new_filename)
        os.makedirs(os.path.dirname(script_path) or ".", exist_ok=True)

        script_content = (
            f"""
$date = `date +%y%m%d_%H`
cvms {script_type}_$date
gs+
gs+ safe
##################### {script_line} Script ####################

"""
            + "\n".join(commands)
            + "\n"
        )

        end_content = f"""
$date = `date +%y%m%d_%H`
cvms {script_ender}_$date
gs-
"""

        try:
            with open(script_path, "a") as file:  # Use "w" to avoid duplicate writes
                file.write(script_content + end_content)
            print(f"✅ Script successfully saved at: {script_path}")
        except Exception as e:
            print(f"❌ Error writing script file: {e}")


class CombinedScriptGenerator(GplScriptGenerator):
    def generate_commands(self):
        """Generate AMOS commands from DataFrame"""
        commands = []

        # required_columns = ["MO", "Parameter", "Pre-existing Value", "CXC ID", "Pre Existing FeatureState", "Relation Parameter", "Value"]
        # missing_cols = [col for col in required_columns if col not in self.df.columns]

        # if missing_cols:
        #     print(f"⚠ Missing required columns: {missing_cols}")
        #     return commands

        for _, row in self.df.iterrows():
            try:
                # Process general parameters
                if pd.notna(row.get("Pre-existing Value")) and pd.notna(row.get("MO")):
                    value = str(row["Pre-existing Value"]).split()[0]
                    commands.append(f"set {row['MO']}$ {row['Parameter']} {value}")

                # Process Feature State changes
                if pd.notna(row.get("Pre Existing FeatureState")) and pd.notna(
                    row.get("CXC ID")
                ):
                    value = int(row["Pre Existing FeatureState"])
                    commands.append(f"set {row['CXC ID']}$ featureState {value}")

                # Process Relation Parameters
                if pd.notna(row.get("Value")) and pd.notna(row.get("MO")):
                    value = (
                        row["Value"].split("|")[0]
                        if "|" in row["Value"]
                        else row["Value"]
                    )
                    commands.append(
                        f"set {row['MO']}$ {row['Relation Parameter']} {value}"
                    )

            except Exception as e:
                print(f"❌ Error processing row: {row.to_dict()} | Error: {e}")

        return commands


class GplScriptFactory:
    @staticmethod
    def create_generator(mismatch_df: pd.DataFrame):
        """Factory method to create script generator"""
        return CombinedScriptGenerator(mismatch_df)
