import sys
    
#sys.path.insert(0, '/nfs/obelix/users1/erisinger/projects/cc/CerebralCortex-Kernel')

import pandas as pd
import datetime as dt
import math

def get_demo_df(num_vals=1000):
    """ Generate a demo dataframe for writing into Cerebral Cortex. """
    
    indices = range(num_vals)
    
    # timestamps
    now = dt.datetime.now().timestamp() * 1000
    t = list(map(lambda x: dt.datetime.fromtimestamp((now + x * 10) / 1000.0), indices))
    localtime = t.copy()
    
    # "reading" values
    x = list(map(lambda x: math.sin(x), indices))
    y = list(map(lambda x: math.sin(x + 1), indices))
    z = list(map(lambda x: math.sin(x + 2), indices))
    
    # user and version columns
    user = ["demo_user"] * num_vals
    version = ["1"] * num_vals
    
    df = pd.DataFrame({"timestamp": t, "localtime": localtime, "x": x, "y": y, "z": z, "version": version, "user": user})
    
    return df
    
def show_df(df, head_count=20, plot=False):
    """ Print the first head_count values of, and optionally plot, the dataframe. """
    
    print(df.head(head_count))
    
    if plot:
        
        import matplotlib.pyplot as plt
        
#        %matplotlib notebook
            
        df.plot(x="timestamp", y=["x", "y", "z"])
        plt.show()
        
def extract_features(stream, duration=1):
    """ Window and run statistical feature extraction over a demo dataframe. """
    
    from cerebralcortex.algorithms.stats.features import statistical_features
    
    windowed_stream = stream.window(duration)
    features = statistical_features(windowed_stream)
    
    return features
        
def get_demo_metadata(stream_name):
    from cerebralcortex.core.metadata_manager.stream.metadata import Metadata, DataDescriptor, ModuleMetadata
    
    metadata = Metadata().set_name(stream_name).set_description("Accelerometer readings from the MotionSense HRV.") \
        .add_dataDescriptor(
        DataDescriptor().set_name("timestamp").set_type("datetime").set_attribute("description", "Timestamp")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("localtime").set_type("datetime").set_attribute("description", "Timestamp")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("user").set_type("str").set_attribute("description", "mHealthLab badge ID")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("version").set_type("str").set_attribute("description", "Stream version")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("x").set_type("float").set_attribute("description", "Accelerometer x")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("y").set_type("float").set_attribute("description", "Accelerometer y")) \
        .add_dataDescriptor(
        DataDescriptor().set_name("z").set_type("float").set_attribute("description", "Accelerometer z")) \
        .add_module(
        ModuleMetadata().set_name("CerebralCortex.mHealthLab.integration").set_version("0.1.0").set_attribute("description", "This module demonstrates the integration of mHealthLab and CerebralCortex.").set_author(
            "Erik Risinger", "erisinger@umass.edu"))
    
    return metadata

def save_datastream(cc, ds):
    cc.save_stream(ds)
    
def make_datastream(df, metadata):
    from cerebralcortex.core.datatypes import DataStream
    ds = DataStream(df, metadata)
    return ds
    
def get_cc(config_filepath='/nfs/obelix/users1/erisinger/projects/cc/mhl-retriever/conf', study_name="default", new_study=True):
    from cerebralcortex import Kernel
    cc = Kernel(config_filepath, study_name=study_name, new_study=new_study)
    return cc
    
def get_datastream(cc, stream_name):
    datastream = cc.get_stream(stream_name)
    return datastream

def run_test(stream_name):
    cc = get_cc()
 
    # get dataframe and metadata
    print(f"Generating dataframe and metadata for datastream {stream_name}")
    df = get_demo_df()
    metadata = get_demo_metadata(stream_name)
    print(df.head())

    print(f"Generating datastream {stream_name}")
    input_stream = make_datastream(df, metadata)

    # create and save cc datastream
    print(f"Saving datastream {stream_name}")
    save_datastream(cc, input_stream)
    
    # retrieve stream and run analytics
    print(f"Retrieving datastream {stream_name}")
    output_stream = get_datastream(cc, stream_name)
    
    print("Extracting features from datastream {stream_name}")
    features = extract_features(output_stream)
    features.show()


if __name__ == '__main__':
	run_test('fancy-test-stream')

