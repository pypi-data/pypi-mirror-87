# IMPORT PACKAGES
from cerebralcortex import Kernel
import numpy as np
import pandas as pd
from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql.types import StructField, StructType, IntegerType, TimestampType, StringType, FloatType
from cerebralcortex.algorithms.utils.mprov_helper import CC_MProvAgg

# CREATE CC OBJECT
CC = Kernel(cc_configs="default", )

# GET STREAM DATA FOR ONE USER
# md2k_aa_rice user_id = a57f8608-439a-4f11-9bbf-085ca01577f6
# rice user_id = 047dfad3-0807-37f0-bc90-7fd9dedb9bde
ecg_ds = CC.get_stream("ecg--org.md2k.autosense--autosense_chest--chest").filter("ecg>2390")

# Show 2 rows
ecg_ds.show(2)


# This is the schema (column name and data type) that pandas udf should return. You can change types and column names to
# start experimenting with. These types and column names should match with the pandas DF return from pandas udf.
schema = StructType([
    StructField("timestamp", TimestampType()),
    StructField("localtime", TimestampType()),
    StructField("user", StringType()),
    StructField("version", IntegerType()),
    StructField("activity", StringType())
])

# This is a sample pandas udf, input to this (sample_udaf) is pandas df and return type is pandas df
#@pandas_udf(schema, PandasUDFType.GROUPED_MAP)
@CC_MProvAgg('org.md2k.autosense.ecg.stress.probability.imputed', 'stress_episodes_estimation', "stream_name-test-test", ['user', 'timestamp'], ['user', 'timestamp'])
def sample_udaf(data):
    all_vals = []

    for index, row in data.iterrows():
        # NOTE: IF YOU ARE USING MD2K_AA_RICE STUDY THEN COLUMN NAMES ARE DIFFERENT, PLEASE UPDATE
        ecg = row["ecg"]

        if ecg>1880:
            activity = "active"
        else:
            activity = "stationary"
        all_vals.append([row["timestamp"],row["localtime"], row["user"],1,activity])

    return pd.DataFrame(all_vals,columns=['timestamp','localtime', 'user', 'version','activity'])

# Use CC built method to apply a pandas udf on the streamd data
result = ecg_ds._data.groupBy(["user","version"]).applyInPandas(sample_udaf, schema)

# show results
result.show(truncate=False)






import pyarrow as pa
import pyarrow.parquet as pq
import pickle


hdfs_url = "hdfs://dantooine10dot:8020"
hdfs = pa.hdfs.connect(hdfs_url)
mismatched_metadata = []

for study in hdfs.ls("/cc3/"):
    print("PROCESSING STUDY", study)
    try:
        for stream in hdfs.ls(study):
            try:
                for version in hdfs.ls(stream):
                    try:
                        for user in hdfs.ls(version):
                            try:
                                files = hdfs.ls(user)
                                if len(files)>2:
                                    old_schema = []
                                    for fle in hdfs.ls(user):
                                        try:
                                            if "_SUCCESS" not in fle:
                                                with hdfs.open(hdfs_url+fle) as f:

                                                    current_schema = pq.read_schema(f).names
                                                    mismatched_metadata.append({
                                                        "total_files":len(files),
                                                        "file_name":fle, "schema": current_schema, "user_folder":user
                                                    })
                                        except Exception as e:
                                            print(str(e))
                            except Exception as e:
                                print(str(e))
                    except Exception as e:
                        print(str(e))
            except Exception as e:
                print(str(e))
    except Exception as e:
        print(str(e))

with open("mismatched_metadata.pkl", 'wb') as f:
    pickle.dump(mismatched_metadata, f, pickle.HIGHEST_PROTOCOL)