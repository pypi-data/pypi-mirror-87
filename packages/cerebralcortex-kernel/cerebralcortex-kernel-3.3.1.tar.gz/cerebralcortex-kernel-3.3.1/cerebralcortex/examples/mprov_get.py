from pennprov.connection.mprov_connection_cache import MProvConnectionCache

graph_name = "mprov-graph"
connection_key = MProvConnectionCache.Key(user="demo", password="demo",
                                          host="http://127.0.0.1:8088", graph=graph_name)
mprov_conn = MProvConnectionCache.get_connection(connection_key)
if mprov_conn:
    mprov_conn.get_low_level_api().create_provenance_graph(graph_name)

tt=mprov_conn.get_source_entities("{http://mprov.md2k.org}65d92e293ca2aad0f40922944ef549e5a6061579")

print(tt)

##################################

# from pennprov.connection.mprov_connection import MProvConnection
# from pennprov.metadata.stream_metadata import BasicSchema, BasicTuple
# from datetime import datetime, timezone
#
# def area_circle(input):
#     return {'key': input['key'],
#             'value': input['value'] * input['value'] * 3.1415}
#
# conn = MProvConnection('demo', 'demo', 'http://127.0.0.1:8088')
# conn.prov_api.create_or_reset_provenance_graph(conn.get_graph())
#
# # Create a node representing the collection of items in the stream, and annotate that
# collection = conn.create_collection('stream1', 1, None)
# conn.store_annotations(collection, {'version': 1, 'privacy': 'none'})
#
# # Create a simple relation or stream, with a binary schema
# data_schema = BasicSchema('SampleStream', {'key': 'int', 'value':'int'})
#
# # Create a sample tuple
# for i in range(0,10):
#     tuple = BasicTuple(data_schema, {'key': i, 'value': 456 + i})
#     tuple_index = i
#
#     # Store the initial data, get the ID (token) of its node in the graph
#     input_token = conn.store_stream_tuple('SampleStream', tuple_index, tuple)
#     conn.add_to_collection(input_token, collection)
#
#     # Compute an operation over the tuple, convert it to a tuple
#     ts = datetime.now(timezone.utc)
#     result = area_circle(tuple)
#     out_tuple = BasicTuple(data_schema, result)
#
#     # Store the derived tuple and the derivation name / time
#     res = conn.store_derived_result('OutStream', tuple_index, out_tuple, input_token, 'area_circle', ts, ts)
#
#     # We can annotate each individual output tuple, if we like
#     conn.store_annotations(res, {'protected': True})
