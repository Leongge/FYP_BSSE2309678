# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/compat/proto/resource_handle.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorboard.compat.proto import tensor_shape_pb2 as tensorboard_dot_compat_dot_proto_dot_tensor__shape__pb2
from tensorboard.compat.proto import types_pb2 as tensorboard_dot_compat_dot_proto_dot_types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.tensorboard/compat/proto/resource_handle.proto\x12\x0btensorboard\x1a+tensorboard/compat/proto/tensor_shape.proto\x1a$tensorboard/compat/proto/types.proto\"\xa8\x02\n\x13ResourceHandleProto\x12\x0e\n\x06\x64\x65vice\x18\x01 \x01(\t\x12\x11\n\tcontainer\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x11\n\thash_code\x18\x04 \x01(\x04\x12\x17\n\x0fmaybe_type_name\x18\x05 \x01(\t\x12I\n\x11\x64types_and_shapes\x18\x06 \x03(\x0b\x32..tensorboard.ResourceHandleProto.DtypeAndShape\x1a\x63\n\rDtypeAndShape\x12$\n\x05\x64type\x18\x01 \x01(\x0e\x32\x15.tensorboard.DataType\x12,\n\x05shape\x18\x02 \x01(\x0b\x32\x1d.tensorboard.TensorShapeProtoJ\x04\x08\x07\x10\x08\x42\x87\x01\n\x18org.tensorflow.frameworkB\x0eResourceHandleP\x01ZVgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/resource_handle_go_proto\xf8\x01\x01\x62\x06proto3')



_RESOURCEHANDLEPROTO = DESCRIPTOR.message_types_by_name['ResourceHandleProto']
_RESOURCEHANDLEPROTO_DTYPEANDSHAPE = _RESOURCEHANDLEPROTO.nested_types_by_name['DtypeAndShape']
ResourceHandleProto = _reflection.GeneratedProtocolMessageType('ResourceHandleProto', (_message.Message,), {

  'DtypeAndShape' : _reflection.GeneratedProtocolMessageType('DtypeAndShape', (_message.Message,), {
    'DESCRIPTOR' : _RESOURCEHANDLEPROTO_DTYPEANDSHAPE,
    '__module__' : 'tensorboard.compat.proto.resource_handle_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.ResourceHandleProto.DtypeAndShape)
    })
  ,
  'DESCRIPTOR' : _RESOURCEHANDLEPROTO,
  '__module__' : 'tensorboard.compat.proto.resource_handle_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.ResourceHandleProto)
  })
_sym_db.RegisterMessage(ResourceHandleProto)
_sym_db.RegisterMessage(ResourceHandleProto.DtypeAndShape)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030org.tensorflow.frameworkB\016ResourceHandleP\001ZVgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/resource_handle_go_proto\370\001\001'
  _RESOURCEHANDLEPROTO._serialized_start=147
  _RESOURCEHANDLEPROTO._serialized_end=443
  _RESOURCEHANDLEPROTO_DTYPEANDSHAPE._serialized_start=338
  _RESOURCEHANDLEPROTO_DTYPEANDSHAPE._serialized_end=437
# @@protoc_insertion_point(module_scope)
