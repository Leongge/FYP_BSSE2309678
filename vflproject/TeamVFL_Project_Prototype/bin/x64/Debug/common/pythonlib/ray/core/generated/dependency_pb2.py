# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: src/ray/protobuf/dependency.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='src/ray/protobuf/dependency.proto',
  package='ray.rpc',
  syntax='proto3',
  serialized_options=b'\370\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n!src/ray/protobuf/dependency.proto\x12\x07ray.rpc\"\"\n\x0ePythonFunction\x12\x10\n\x03key\x18\x01 \x01(\x0cR\x03keyB\x03\xf8\x01\x01\x62\x06proto3'
)




_PYTHONFUNCTION = _descriptor.Descriptor(
  name='PythonFunction',
  full_name='ray.rpc.PythonFunction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ray.rpc.PythonFunction.key', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='key', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=46,
  serialized_end=80,
)

DESCRIPTOR.message_types_by_name['PythonFunction'] = _PYTHONFUNCTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PythonFunction = _reflection.GeneratedProtocolMessageType('PythonFunction', (_message.Message,), {
  'DESCRIPTOR' : _PYTHONFUNCTION,
  '__module__' : 'src.ray.protobuf.dependency_pb2'
  # @@protoc_insertion_point(class_scope:ray.rpc.PythonFunction)
  })
_sym_db.RegisterMessage(PythonFunction)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
