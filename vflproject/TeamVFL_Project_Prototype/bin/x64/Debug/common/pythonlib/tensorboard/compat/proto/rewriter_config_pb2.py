# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/compat/proto/rewriter_config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorboard.compat.proto import attr_value_pb2 as tensorboard_dot_compat_dot_proto_dot_attr__value__pb2
from tensorboard.compat.proto import verifier_config_pb2 as tensorboard_dot_compat_dot_proto_dot_verifier__config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.tensorboard/compat/proto/rewriter_config.proto\x12\x0btensorboard\x1a)tensorboard/compat/proto/attr_value.proto\x1a.tensorboard/compat/proto/verifier_config.proto\";\n\x13\x41utoParallelOptions\x12\x0e\n\x06\x65nable\x18\x01 \x01(\x08\x12\x14\n\x0cnum_replicas\x18\x02 \x01(\x05\"+\n\x16ScopedAllocatorOptions\x12\x11\n\tenable_op\x18\x01 \x03(\t\"\xb2\x16\n\x0eRewriterConfig\x12\x44\n\x15\x63pu_layout_conversion\x18\x32 \x01(\x0e\x32%.tensorboard.RewriterConfig.CpuLayout\x12<\n\x10layout_optimizer\x18\x01 \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12<\n\x10\x63onstant_folding\x18\x03 \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12>\n\x12shape_optimization\x18\r \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12\x35\n\tremapping\x18\x0e \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12G\n\x1b\x63ommon_subgraph_elimination\x18\x18 \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12\x43\n\x17\x61rithmetic_optimization\x18\x07 \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12\x43\n\x17\x64\x65pendency_optimization\x18\x08 \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12=\n\x11loop_optimization\x18\t \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12\x41\n\x15\x66unction_optimization\x18\n \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12:\n\x0e\x64\x65\x62ug_stripper\x18\x0b \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12\x1d\n\x15\x64isable_model_pruning\x18\x02 \x01(\x08\x12I\n\x1dscoped_allocator_optimization\x18\x0f \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12\x44\n\x18pin_to_host_optimization\x18\x12 \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12\x43\n\x17implementation_selector\x18\x16 \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12@\n\x14\x61uto_mixed_precision\x18\x17 \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12\x44\n\x18\x61uto_mixed_precision_mkl\x18\x19 \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12P\n$auto_mixed_precision_onednn_bfloat16\x18\x1f \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12\x44\n\x18\x61uto_mixed_precision_cpu\x18\x1d \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12\x1e\n\x16\x64isable_meta_optimizer\x18\x13 \x01(\x08\x12\x1d\n\x15\x64isable_tfg_optimizer\x18  \x01(\x08\x12\x41\n\x15use_plugin_optimizers\x18\x1c \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12P\n$experimental_conditional_code_motion\x18\x1e \x01(\x0e\x32\".tensorboard.RewriterConfig.Toggle\x12P\n\x19meta_optimizer_iterations\x18\x0c \x01(\x0e\x32-.tensorboard.RewriterConfig.NumIterationsType\x12\x17\n\x0fmin_graph_nodes\x18\x11 \x01(\x05\x12;\n3experimental_disable_compressed_tensor_optimization\x18\x1a \x01(\x08\x12;\n3experimental_disable_folding_quantization_emulation\x18\x1b \x01(\x08\x12\x43\n\x13memory_optimization\x18\x04 \x01(\x0e\x32&.tensorboard.RewriterConfig.MemOptType\x12/\n\'memory_optimizer_target_node_name_scope\x18\x06 \x01(\t\x12!\n\x19meta_optimizer_timeout_ms\x18\x14 \x01(\x03\x12\x37\n\rauto_parallel\x18\x05 \x01(\x0b\x32 .tensorboard.AutoParallelOptions\x12 \n\x18\x66\x61il_on_optimizer_errors\x18\x15 \x01(\x08\x12\x42\n\x15scoped_allocator_opts\x18\x10 \x01(\x0b\x32#.tensorboard.ScopedAllocatorOptions\x12\x12\n\noptimizers\x18\x64 \x03(\t\x12L\n\x11\x63ustom_optimizers\x18\xc8\x01 \x03(\x0b\x32\x30.tensorboard.RewriterConfig.CustomGraphOptimizer\x12\x45\n\x1finter_optimizer_verifier_config\x18\xac\x02 \x01(\x0b\x32\x1b.tensorboard.VerifierConfig\x12G\n!post_optimization_verifier_config\x18\xad\x02 \x01(\x0b\x32\x1b.tensorboard.VerifierConfig\x1a\xcc\x01\n\x14\x43ustomGraphOptimizer\x12\x0c\n\x04name\x18\x01 \x01(\t\x12Y\n\rparameter_map\x18\x02 \x03(\x0b\x32\x42.tensorboard.RewriterConfig.CustomGraphOptimizer.ParameterMapEntry\x1aK\n\x11ParameterMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.tensorboard.AttrValue:\x02\x38\x01\"d\n\x06Toggle\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\x06\n\x02ON\x10\x01\x12\x07\n\x03OFF\x10\x02\x12\x0e\n\nAGGRESSIVE\x10\x03\x12\x15\n\x11\x45XPERIMENTAL_MLIR\x10\x04\x12\x15\n\x11\x45XPERIMENTAL_BOTH\x10\x05\"I\n\tCpuLayout\x12\x18\n\x14NO_CONVERSION_ON_CPU\x10\x00\x12\x10\n\x0cNCHW_TO_NHWC\x10\x01\x12\x10\n\x0cNHWC_TO_NCHW\x10\x02\"<\n\x11NumIterationsType\x12\x15\n\x11\x44\x45\x46\x41ULT_NUM_ITERS\x10\x00\x12\x07\n\x03ONE\x10\x01\x12\x07\n\x03TWO\x10\x02\"\x9f\x01\n\nMemOptType\x12\x13\n\x0f\x44\x45\x46\x41ULT_MEM_OPT\x10\x00\x12\x0e\n\nNO_MEM_OPT\x10\x01\x12\n\n\x06MANUAL\x10\x02\x12\x17\n\x13SWAPPING_HEURISTICS\x10\x04\x12\x1c\n\x18RECOMPUTATION_HEURISTICS\x10\x05\x12\x19\n\x15SCHEDULING_HEURISTICS\x10\x06\x12\x0e\n\nHEURISTICS\x10\x03\x42\x8c\x01\n\x18org.tensorflow.frameworkB\x14RewriterConfigProtosP\x01ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\xf8\x01\x01\x62\x06proto3')



_AUTOPARALLELOPTIONS = DESCRIPTOR.message_types_by_name['AutoParallelOptions']
_SCOPEDALLOCATOROPTIONS = DESCRIPTOR.message_types_by_name['ScopedAllocatorOptions']
_REWRITERCONFIG = DESCRIPTOR.message_types_by_name['RewriterConfig']
_REWRITERCONFIG_CUSTOMGRAPHOPTIMIZER = _REWRITERCONFIG.nested_types_by_name['CustomGraphOptimizer']
_REWRITERCONFIG_CUSTOMGRAPHOPTIMIZER_PARAMETERMAPENTRY = _REWRITERCONFIG_CUSTOMGRAPHOPTIMIZER.nested_types_by_name['ParameterMapEntry']
_REWRITERCONFIG_TOGGLE = _REWRITERCONFIG.enum_types_by_name['Toggle']
_REWRITERCONFIG_CPULAYOUT = _REWRITERCONFIG.enum_types_by_name['CpuLayout']
_REWRITERCONFIG_NUMITERATIONSTYPE = _REWRITERCONFIG.enum_types_by_name['NumIterationsType']
_REWRITERCONFIG_MEMOPTTYPE = _REWRITERCONFIG.enum_types_by_name['MemOptType']
AutoParallelOptions = _reflection.GeneratedProtocolMessageType('AutoParallelOptions', (_message.Message,), {
  'DESCRIPTOR' : _AUTOPARALLELOPTIONS,
  '__module__' : 'tensorboard.compat.proto.rewriter_config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.AutoParallelOptions)
  })
_sym_db.RegisterMessage(AutoParallelOptions)

ScopedAllocatorOptions = _reflection.GeneratedProtocolMessageType('ScopedAllocatorOptions', (_message.Message,), {
  'DESCRIPTOR' : _SCOPEDALLOCATOROPTIONS,
  '__module__' : 'tensorboard.compat.proto.rewriter_config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.ScopedAllocatorOptions)
  })
_sym_db.RegisterMessage(ScopedAllocatorOptions)

RewriterConfig = _reflection.GeneratedProtocolMessageType('RewriterConfig', (_message.Message,), {

  'CustomGraphOptimizer' : _reflection.GeneratedProtocolMessageType('CustomGraphOptimizer', (_message.Message,), {

    'ParameterMapEntry' : _reflection.GeneratedProtocolMessageType('ParameterMapEntry', (_message.Message,), {
      'DESCRIPTOR' : _REWRITERCONFIG_CUSTOMGRAPHOPTIMIZER_PARAMETERMAPENTRY,
      '__module__' : 'tensorboard.compat.proto.rewriter_config_pb2'
      # @@protoc_insertion_point(class_scope:tensorboard.RewriterConfig.CustomGraphOptimizer.ParameterMapEntry)
      })
    ,
    'DESCRIPTOR' : _REWRITERCONFIG_CUSTOMGRAPHOPTIMIZER,
    '__module__' : 'tensorboard.compat.proto.rewriter_config_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.RewriterConfig.CustomGraphOptimizer)
    })
  ,
  'DESCRIPTOR' : _REWRITERCONFIG,
  '__module__' : 'tensorboard.compat.proto.rewriter_config_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.RewriterConfig)
  })
_sym_db.RegisterMessage(RewriterConfig)
_sym_db.RegisterMessage(RewriterConfig.CustomGraphOptimizer)
_sym_db.RegisterMessage(RewriterConfig.CustomGraphOptimizer.ParameterMapEntry)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030org.tensorflow.frameworkB\024RewriterConfigProtosP\001ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\370\001\001'
  _REWRITERCONFIG_CUSTOMGRAPHOPTIMIZER_PARAMETERMAPENTRY._options = None
  _REWRITERCONFIG_CUSTOMGRAPHOPTIMIZER_PARAMETERMAPENTRY._serialized_options = b'8\001'
  _AUTOPARALLELOPTIONS._serialized_start=154
  _AUTOPARALLELOPTIONS._serialized_end=213
  _SCOPEDALLOCATOROPTIONS._serialized_start=215
  _SCOPEDALLOCATOROPTIONS._serialized_end=258
  _REWRITERCONFIG._serialized_start=261
  _REWRITERCONFIG._serialized_end=3127
  _REWRITERCONFIG_CUSTOMGRAPHOPTIMIZER._serialized_start=2522
  _REWRITERCONFIG_CUSTOMGRAPHOPTIMIZER._serialized_end=2726
  _REWRITERCONFIG_CUSTOMGRAPHOPTIMIZER_PARAMETERMAPENTRY._serialized_start=2651
  _REWRITERCONFIG_CUSTOMGRAPHOPTIMIZER_PARAMETERMAPENTRY._serialized_end=2726
  _REWRITERCONFIG_TOGGLE._serialized_start=2728
  _REWRITERCONFIG_TOGGLE._serialized_end=2828
  _REWRITERCONFIG_CPULAYOUT._serialized_start=2830
  _REWRITERCONFIG_CPULAYOUT._serialized_end=2903
  _REWRITERCONFIG_NUMITERATIONSTYPE._serialized_start=2905
  _REWRITERCONFIG_NUMITERATIONSTYPE._serialized_end=2965
  _REWRITERCONFIG_MEMOPTTYPE._serialized_start=2968
  _REWRITERCONFIG_MEMOPTTYPE._serialized_end=3127
# @@protoc_insertion_point(module_scope)
