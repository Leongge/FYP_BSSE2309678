# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/streaming.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protobuf/streaming.proto',
  package='ray.streaming.proto',
  syntax='proto3',
  serialized_options=b'\n\"io.ray.streaming.runtime.generated',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18protobuf/streaming.proto\x12\x13ray.streaming.proto\"\x83\x04\n\x0fStreamingConfig\x12\x19\n\x08job_name\x18\x01 \x01(\tR\x07jobName\x12\x1f\n\x0bworker_name\x18\x03 \x01(\tR\nworkerName\x12\x17\n\x07op_name\x18\x04 \x01(\tR\x06opName\x12\x31\n\x04role\x18\x05 \x01(\x0e\x32\x1d.ray.streaming.proto.NodeTypeR\x04role\x12\x30\n\x14ring_buffer_capacity\x18\x06 \x01(\rR\x12ringBufferCapacity\x12\x34\n\x16\x65mpty_message_interval\x18\x07 \x01(\rR\x14\x65mptyMessageInterval\x12P\n\x11\x66low_control_type\x18\x08 \x01(\x0e\x32$.ray.streaming.proto.FlowControlTypeR\x0f\x66lowControlType\x12\x30\n\x14writer_consumed_step\x18\t \x01(\rR\x12writerConsumedStep\x12\x30\n\x14reader_consumed_step\x18\n \x01(\rR\x12readerConsumedStep\x12J\n\"event_driven_flow_control_interval\x18\x0b \x01(\rR\x1e\x65ventDrivenFlowControlInterval* \n\x08Language\x12\x08\n\x04JAVA\x10\x00\x12\n\n\x06PYTHON\x10\x01*<\n\x08NodeType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\n\n\x06SOURCE\x10\x01\x12\r\n\tTRANSFORM\x10\x02\x12\x08\n\x04SINK\x10\x03*A\n\x10ReliabilityLevel\x12\x08\n\x04NONE\x10\x00\x12\x11\n\rAT_LEAST_ONCE\x10\x01\x12\x10\n\x0c\x45XACTLY_ONCE\x10\x02*a\n\x0f\x46lowControlType\x12\x1d\n\x19UNKNOWN_FLOW_CONTROL_TYPE\x10\x00\x12\x1c\n\x18UnconsumedSeqFlowControl\x10\x01\x12\x11\n\rNoFlowControl\x10\x02\x42$\n\"io.ray.streaming.runtime.generatedb\x06proto3'
)

_LANGUAGE = _descriptor.EnumDescriptor(
  name='Language',
  full_name='ray.streaming.proto.Language',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='JAVA', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PYTHON', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=567,
  serialized_end=599,
)
_sym_db.RegisterEnumDescriptor(_LANGUAGE)

Language = enum_type_wrapper.EnumTypeWrapper(_LANGUAGE)
_NODETYPE = _descriptor.EnumDescriptor(
  name='NodeType',
  full_name='ray.streaming.proto.NodeType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SOURCE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TRANSFORM', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SINK', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=601,
  serialized_end=661,
)
_sym_db.RegisterEnumDescriptor(_NODETYPE)

NodeType = enum_type_wrapper.EnumTypeWrapper(_NODETYPE)
_RELIABILITYLEVEL = _descriptor.EnumDescriptor(
  name='ReliabilityLevel',
  full_name='ray.streaming.proto.ReliabilityLevel',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='AT_LEAST_ONCE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EXACTLY_ONCE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=663,
  serialized_end=728,
)
_sym_db.RegisterEnumDescriptor(_RELIABILITYLEVEL)

ReliabilityLevel = enum_type_wrapper.EnumTypeWrapper(_RELIABILITYLEVEL)
_FLOWCONTROLTYPE = _descriptor.EnumDescriptor(
  name='FlowControlType',
  full_name='ray.streaming.proto.FlowControlType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_FLOW_CONTROL_TYPE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UnconsumedSeqFlowControl', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='NoFlowControl', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=730,
  serialized_end=827,
)
_sym_db.RegisterEnumDescriptor(_FLOWCONTROLTYPE)

FlowControlType = enum_type_wrapper.EnumTypeWrapper(_FLOWCONTROLTYPE)
JAVA = 0
PYTHON = 1
UNKNOWN = 0
SOURCE = 1
TRANSFORM = 2
SINK = 3
NONE = 0
AT_LEAST_ONCE = 1
EXACTLY_ONCE = 2
UNKNOWN_FLOW_CONTROL_TYPE = 0
UnconsumedSeqFlowControl = 1
NoFlowControl = 2



_STREAMINGCONFIG = _descriptor.Descriptor(
  name='StreamingConfig',
  full_name='ray.streaming.proto.StreamingConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='job_name', full_name='ray.streaming.proto.StreamingConfig.job_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='jobName', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='worker_name', full_name='ray.streaming.proto.StreamingConfig.worker_name', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='workerName', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='op_name', full_name='ray.streaming.proto.StreamingConfig.op_name', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='opName', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='role', full_name='ray.streaming.proto.StreamingConfig.role', index=3,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='role', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ring_buffer_capacity', full_name='ray.streaming.proto.StreamingConfig.ring_buffer_capacity', index=4,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='ringBufferCapacity', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='empty_message_interval', full_name='ray.streaming.proto.StreamingConfig.empty_message_interval', index=5,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='emptyMessageInterval', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flow_control_type', full_name='ray.streaming.proto.StreamingConfig.flow_control_type', index=6,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='flowControlType', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='writer_consumed_step', full_name='ray.streaming.proto.StreamingConfig.writer_consumed_step', index=7,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='writerConsumedStep', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reader_consumed_step', full_name='ray.streaming.proto.StreamingConfig.reader_consumed_step', index=8,
      number=10, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='readerConsumedStep', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='event_driven_flow_control_interval', full_name='ray.streaming.proto.StreamingConfig.event_driven_flow_control_interval', index=9,
      number=11, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='eventDrivenFlowControlInterval', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=50,
  serialized_end=565,
)

_STREAMINGCONFIG.fields_by_name['role'].enum_type = _NODETYPE
_STREAMINGCONFIG.fields_by_name['flow_control_type'].enum_type = _FLOWCONTROLTYPE
DESCRIPTOR.message_types_by_name['StreamingConfig'] = _STREAMINGCONFIG
DESCRIPTOR.enum_types_by_name['Language'] = _LANGUAGE
DESCRIPTOR.enum_types_by_name['NodeType'] = _NODETYPE
DESCRIPTOR.enum_types_by_name['ReliabilityLevel'] = _RELIABILITYLEVEL
DESCRIPTOR.enum_types_by_name['FlowControlType'] = _FLOWCONTROLTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StreamingConfig = _reflection.GeneratedProtocolMessageType('StreamingConfig', (_message.Message,), {
  'DESCRIPTOR' : _STREAMINGCONFIG,
  '__module__' : 'protobuf.streaming_pb2'
  # @@protoc_insertion_point(class_scope:ray.streaming.proto.StreamingConfig)
  })
_sym_db.RegisterMessage(StreamingConfig)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
