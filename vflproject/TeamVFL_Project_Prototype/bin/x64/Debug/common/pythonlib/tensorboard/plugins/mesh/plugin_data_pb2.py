# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/plugins/mesh/plugin_data.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*tensorboard/plugins/mesh/plugin_data.proto\x12\x10tensorboard.mesh\"\xea\x01\n\x0eMeshPluginData\x12\x0f\n\x07version\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x42\n\x0c\x63ontent_type\x18\x03 \x01(\x0e\x32,.tensorboard.mesh.MeshPluginData.ContentType\x12\x13\n\x0bjson_config\x18\x05 \x01(\t\x12\r\n\x05shape\x18\x06 \x03(\x05\x12\x12\n\ncomponents\x18\x07 \x01(\r\"=\n\x0b\x43ontentType\x12\r\n\tUNDEFINED\x10\x00\x12\n\n\x06VERTEX\x10\x01\x12\x08\n\x04\x46\x41\x43\x45\x10\x02\x12\t\n\x05\x43OLOR\x10\x03\x62\x06proto3')



_MESHPLUGINDATA = DESCRIPTOR.message_types_by_name['MeshPluginData']
_MESHPLUGINDATA_CONTENTTYPE = _MESHPLUGINDATA.enum_types_by_name['ContentType']
MeshPluginData = _reflection.GeneratedProtocolMessageType('MeshPluginData', (_message.Message,), {
  'DESCRIPTOR' : _MESHPLUGINDATA,
  '__module__' : 'tensorboard.plugins.mesh.plugin_data_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.mesh.MeshPluginData)
  })
_sym_db.RegisterMessage(MeshPluginData)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESHPLUGINDATA._serialized_start=65
  _MESHPLUGINDATA._serialized_end=299
  _MESHPLUGINDATA_CONTENTTYPE._serialized_start=238
  _MESHPLUGINDATA_CONTENTTYPE._serialized_end=299
# @@protoc_insertion_point(module_scope)
