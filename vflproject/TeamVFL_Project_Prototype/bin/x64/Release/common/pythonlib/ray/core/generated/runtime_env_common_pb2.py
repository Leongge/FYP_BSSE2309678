# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: src/ray/protobuf/runtime_env_common.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='src/ray/protobuf/runtime_env_common.proto',
  package='ray.rpc',
  syntax='proto3',
  serialized_options=b'\n\030io.ray.runtime.generated\370\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n)src/ray/protobuf/runtime_env_common.proto\x12\x07ray.rpc\"\xad\x01\n\rPipRuntimeEnv\x12\x37\n\x06\x63onfig\x18\x01 \x01(\x0b\x32\x1d.ray.rpc.PipRuntimeEnv.ConfigH\x00R\x06\x63onfig\x12*\n\x10virtual_env_name\x18\x02 \x01(\tH\x00R\x0evirtualEnvName\x1a$\n\x06\x43onfig\x12\x1a\n\x08packages\x18\x01 \x03(\tR\x08packagesB\x11\n\x0fpip_runtime_env\"h\n\x0f\x43ondaRuntimeEnv\x12\x18\n\x06\x63onfig\x18\x01 \x01(\tH\x00R\x06\x63onfig\x12&\n\x0e\x63onda_env_name\x18\x02 \x01(\tH\x00R\x0c\x63ondaEnvNameB\x13\n\x11\x63onda_runtime_env\"m\n\x13\x43ontainerRuntimeEnv\x12\x14\n\x05image\x18\x01 \x01(\tR\x05image\x12\x1f\n\x0bworker_path\x18\x02 \x01(\tR\nworkerPath\x12\x1f\n\x0brun_options\x18\x03 \x03(\tR\nrunOptions\"\x8f\x01\n\x10PluginRuntimeEnv\x12:\n\x07plugins\x18\x01 \x03(\x0b\x32 .ray.rpc.PluginRuntimeEnv.PluginR\x07plugins\x1a?\n\x06Plugin\x12\x1d\n\nclass_path\x18\x01 \x01(\tR\tclassPath\x12\x16\n\x06\x63onfig\x18\x02 \x01(\tR\x06\x63onfig\"\x10\n\x0eJarsRuntimeEnv\"\x11\n\x0fMavenRuntimeEnv\"\xb7\x01\n\x0eRuntimeEnvUris\x12&\n\x0fworking_dir_uri\x18\x01 \x01(\tR\rworkingDirUri\x12&\n\x0fpy_modules_uris\x18\x02 \x03(\tR\rpyModulesUris\x12\x1b\n\tconda_uri\x18\x03 \x01(\tR\x08\x63ondaUri\x12\x17\n\x07pip_uri\x18\x04 \x01(\tR\x06pipUri\x12\x1f\n\x0bplugin_uris\x18\x05 \x03(\tR\npluginUris\"\x91\x08\n\nRuntimeEnv\x12\x1d\n\npy_modules\x18\x01 \x03(\tR\tpyModules\x12\x1f\n\x0bworking_dir\x18\x02 \x01(\tR\nworkingDir\x12+\n\x04uris\x18\x03 \x01(\x0b\x32\x17.ray.rpc.RuntimeEnvUrisR\x04uris\x12;\n\x08\x65nv_vars\x18\x04 \x03(\x0b\x32 .ray.rpc.RuntimeEnv.EnvVarsEntryR\x07\x65nvVars\x12\x43\n\nextensions\x18\x05 \x03(\x0b\x32#.ray.rpc.RuntimeEnv.ExtensionsEntryR\nextensions\x12@\n\x0fpip_runtime_env\x18\x06 \x01(\x0b\x32\x16.ray.rpc.PipRuntimeEnvH\x00R\rpipRuntimeEnv\x12\x46\n\x11\x63onda_runtime_env\x18\x07 \x01(\x0b\x32\x18.ray.rpc.CondaRuntimeEnvH\x00R\x0f\x63ondaRuntimeEnv\x12W\n\x18py_container_runtime_env\x18\x08 \x01(\x0b\x32\x1c.ray.rpc.ContainerRuntimeEnvH\x00R\x15pyContainerRuntimeEnv\x12N\n\x15py_plugin_runtime_env\x18\t \x01(\x0b\x32\x19.ray.rpc.PluginRuntimeEnvH\x00R\x12pyPluginRuntimeEnv\x12\x43\n\x10jars_runtime_env\x18\n \x01(\x0b\x32\x17.ray.rpc.JarsRuntimeEnvH\x01R\x0ejarsRuntimeEnv\x12\x46\n\x11maven_runtime_env\x18\x0b \x01(\x0b\x32\x18.ray.rpc.MavenRuntimeEnvH\x01R\x0fmavenRuntimeEnv\x12[\n\x1ajava_container_runtime_env\x18\x0c \x01(\x0b\x32\x1c.ray.rpc.ContainerRuntimeEnvH\x01R\x17javaContainerRuntimeEnv\x12R\n\x17java_plugin_runtime_env\x18\r \x01(\x0b\x32\x19.ray.rpc.PluginRuntimeEnvH\x01R\x14javaPluginRuntimeEnv\x1a:\n\x0c\x45nvVarsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a=\n\x0f\x45xtensionsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42\x14\n\x12python_runtime_envB\x12\n\x10java_runtime_env\"\x95\x01\n\x0eRuntimeEnvInfo\x12\x34\n\x16serialized_runtime_env\x18\x01 \x01(\tR\x14serializedRuntimeEnv\x12\x12\n\x04uris\x18\x02 \x03(\tR\x04uris\x12\x39\n\x19runtime_env_eager_install\x18\x03 \x01(\x08R\x16runtimeEnvEagerInstallB\x1d\n\x18io.ray.runtime.generated\xf8\x01\x01\x62\x06proto3'
)




_PIPRUNTIMEENV_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='ray.rpc.PipRuntimeEnv.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='packages', full_name='ray.rpc.PipRuntimeEnv.Config.packages', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='packages', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=173,
  serialized_end=209,
)

_PIPRUNTIMEENV = _descriptor.Descriptor(
  name='PipRuntimeEnv',
  full_name='ray.rpc.PipRuntimeEnv',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='config', full_name='ray.rpc.PipRuntimeEnv.config', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='config', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='virtual_env_name', full_name='ray.rpc.PipRuntimeEnv.virtual_env_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='virtualEnvName', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_PIPRUNTIMEENV_CONFIG, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='pip_runtime_env', full_name='ray.rpc.PipRuntimeEnv.pip_runtime_env',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=55,
  serialized_end=228,
)


_CONDARUNTIMEENV = _descriptor.Descriptor(
  name='CondaRuntimeEnv',
  full_name='ray.rpc.CondaRuntimeEnv',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='config', full_name='ray.rpc.CondaRuntimeEnv.config', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='config', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='conda_env_name', full_name='ray.rpc.CondaRuntimeEnv.conda_env_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='condaEnvName', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
    _descriptor.OneofDescriptor(
      name='conda_runtime_env', full_name='ray.rpc.CondaRuntimeEnv.conda_runtime_env',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=230,
  serialized_end=334,
)


_CONTAINERRUNTIMEENV = _descriptor.Descriptor(
  name='ContainerRuntimeEnv',
  full_name='ray.rpc.ContainerRuntimeEnv',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='image', full_name='ray.rpc.ContainerRuntimeEnv.image', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='image', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='worker_path', full_name='ray.rpc.ContainerRuntimeEnv.worker_path', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='workerPath', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='run_options', full_name='ray.rpc.ContainerRuntimeEnv.run_options', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='runOptions', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=336,
  serialized_end=445,
)


_PLUGINRUNTIMEENV_PLUGIN = _descriptor.Descriptor(
  name='Plugin',
  full_name='ray.rpc.PluginRuntimeEnv.Plugin',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='class_path', full_name='ray.rpc.PluginRuntimeEnv.Plugin.class_path', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='classPath', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='config', full_name='ray.rpc.PluginRuntimeEnv.Plugin.config', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='config', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=528,
  serialized_end=591,
)

_PLUGINRUNTIMEENV = _descriptor.Descriptor(
  name='PluginRuntimeEnv',
  full_name='ray.rpc.PluginRuntimeEnv',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='plugins', full_name='ray.rpc.PluginRuntimeEnv.plugins', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='plugins', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_PLUGINRUNTIMEENV_PLUGIN, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=448,
  serialized_end=591,
)


_JARSRUNTIMEENV = _descriptor.Descriptor(
  name='JarsRuntimeEnv',
  full_name='ray.rpc.JarsRuntimeEnv',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=593,
  serialized_end=609,
)


_MAVENRUNTIMEENV = _descriptor.Descriptor(
  name='MavenRuntimeEnv',
  full_name='ray.rpc.MavenRuntimeEnv',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=611,
  serialized_end=628,
)


_RUNTIMEENVURIS = _descriptor.Descriptor(
  name='RuntimeEnvUris',
  full_name='ray.rpc.RuntimeEnvUris',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='working_dir_uri', full_name='ray.rpc.RuntimeEnvUris.working_dir_uri', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='workingDirUri', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='py_modules_uris', full_name='ray.rpc.RuntimeEnvUris.py_modules_uris', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pyModulesUris', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='conda_uri', full_name='ray.rpc.RuntimeEnvUris.conda_uri', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='condaUri', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pip_uri', full_name='ray.rpc.RuntimeEnvUris.pip_uri', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pipUri', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='plugin_uris', full_name='ray.rpc.RuntimeEnvUris.plugin_uris', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pluginUris', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=631,
  serialized_end=814,
)


_RUNTIMEENV_ENVVARSENTRY = _descriptor.Descriptor(
  name='EnvVarsEntry',
  full_name='ray.rpc.RuntimeEnv.EnvVarsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ray.rpc.RuntimeEnv.EnvVarsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='key', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='ray.rpc.RuntimeEnv.EnvVarsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='value', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1695,
  serialized_end=1753,
)

_RUNTIMEENV_EXTENSIONSENTRY = _descriptor.Descriptor(
  name='ExtensionsEntry',
  full_name='ray.rpc.RuntimeEnv.ExtensionsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ray.rpc.RuntimeEnv.ExtensionsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='key', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='ray.rpc.RuntimeEnv.ExtensionsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='value', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1755,
  serialized_end=1816,
)

_RUNTIMEENV = _descriptor.Descriptor(
  name='RuntimeEnv',
  full_name='ray.rpc.RuntimeEnv',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='py_modules', full_name='ray.rpc.RuntimeEnv.py_modules', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pyModules', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='working_dir', full_name='ray.rpc.RuntimeEnv.working_dir', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='workingDir', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='uris', full_name='ray.rpc.RuntimeEnv.uris', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='uris', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='env_vars', full_name='ray.rpc.RuntimeEnv.env_vars', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='envVars', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extensions', full_name='ray.rpc.RuntimeEnv.extensions', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='extensions', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pip_runtime_env', full_name='ray.rpc.RuntimeEnv.pip_runtime_env', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pipRuntimeEnv', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='conda_runtime_env', full_name='ray.rpc.RuntimeEnv.conda_runtime_env', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='condaRuntimeEnv', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='py_container_runtime_env', full_name='ray.rpc.RuntimeEnv.py_container_runtime_env', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pyContainerRuntimeEnv', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='py_plugin_runtime_env', full_name='ray.rpc.RuntimeEnv.py_plugin_runtime_env', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='pyPluginRuntimeEnv', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='jars_runtime_env', full_name='ray.rpc.RuntimeEnv.jars_runtime_env', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='jarsRuntimeEnv', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='maven_runtime_env', full_name='ray.rpc.RuntimeEnv.maven_runtime_env', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='mavenRuntimeEnv', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='java_container_runtime_env', full_name='ray.rpc.RuntimeEnv.java_container_runtime_env', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='javaContainerRuntimeEnv', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='java_plugin_runtime_env', full_name='ray.rpc.RuntimeEnv.java_plugin_runtime_env', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='javaPluginRuntimeEnv', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_RUNTIMEENV_ENVVARSENTRY, _RUNTIMEENV_EXTENSIONSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='python_runtime_env', full_name='ray.rpc.RuntimeEnv.python_runtime_env',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='java_runtime_env', full_name='ray.rpc.RuntimeEnv.java_runtime_env',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=817,
  serialized_end=1858,
)


_RUNTIMEENVINFO = _descriptor.Descriptor(
  name='RuntimeEnvInfo',
  full_name='ray.rpc.RuntimeEnvInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='serialized_runtime_env', full_name='ray.rpc.RuntimeEnvInfo.serialized_runtime_env', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='serializedRuntimeEnv', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='uris', full_name='ray.rpc.RuntimeEnvInfo.uris', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='uris', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='runtime_env_eager_install', full_name='ray.rpc.RuntimeEnvInfo.runtime_env_eager_install', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='runtimeEnvEagerInstall', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1861,
  serialized_end=2010,
)

_PIPRUNTIMEENV_CONFIG.containing_type = _PIPRUNTIMEENV
_PIPRUNTIMEENV.fields_by_name['config'].message_type = _PIPRUNTIMEENV_CONFIG
_PIPRUNTIMEENV.oneofs_by_name['pip_runtime_env'].fields.append(
  _PIPRUNTIMEENV.fields_by_name['config'])
_PIPRUNTIMEENV.fields_by_name['config'].containing_oneof = _PIPRUNTIMEENV.oneofs_by_name['pip_runtime_env']
_PIPRUNTIMEENV.oneofs_by_name['pip_runtime_env'].fields.append(
  _PIPRUNTIMEENV.fields_by_name['virtual_env_name'])
_PIPRUNTIMEENV.fields_by_name['virtual_env_name'].containing_oneof = _PIPRUNTIMEENV.oneofs_by_name['pip_runtime_env']
_CONDARUNTIMEENV.oneofs_by_name['conda_runtime_env'].fields.append(
  _CONDARUNTIMEENV.fields_by_name['config'])
_CONDARUNTIMEENV.fields_by_name['config'].containing_oneof = _CONDARUNTIMEENV.oneofs_by_name['conda_runtime_env']
_CONDARUNTIMEENV.oneofs_by_name['conda_runtime_env'].fields.append(
  _CONDARUNTIMEENV.fields_by_name['conda_env_name'])
_CONDARUNTIMEENV.fields_by_name['conda_env_name'].containing_oneof = _CONDARUNTIMEENV.oneofs_by_name['conda_runtime_env']
_PLUGINRUNTIMEENV_PLUGIN.containing_type = _PLUGINRUNTIMEENV
_PLUGINRUNTIMEENV.fields_by_name['plugins'].message_type = _PLUGINRUNTIMEENV_PLUGIN
_RUNTIMEENV_ENVVARSENTRY.containing_type = _RUNTIMEENV
_RUNTIMEENV_EXTENSIONSENTRY.containing_type = _RUNTIMEENV
_RUNTIMEENV.fields_by_name['uris'].message_type = _RUNTIMEENVURIS
_RUNTIMEENV.fields_by_name['env_vars'].message_type = _RUNTIMEENV_ENVVARSENTRY
_RUNTIMEENV.fields_by_name['extensions'].message_type = _RUNTIMEENV_EXTENSIONSENTRY
_RUNTIMEENV.fields_by_name['pip_runtime_env'].message_type = _PIPRUNTIMEENV
_RUNTIMEENV.fields_by_name['conda_runtime_env'].message_type = _CONDARUNTIMEENV
_RUNTIMEENV.fields_by_name['py_container_runtime_env'].message_type = _CONTAINERRUNTIMEENV
_RUNTIMEENV.fields_by_name['py_plugin_runtime_env'].message_type = _PLUGINRUNTIMEENV
_RUNTIMEENV.fields_by_name['jars_runtime_env'].message_type = _JARSRUNTIMEENV
_RUNTIMEENV.fields_by_name['maven_runtime_env'].message_type = _MAVENRUNTIMEENV
_RUNTIMEENV.fields_by_name['java_container_runtime_env'].message_type = _CONTAINERRUNTIMEENV
_RUNTIMEENV.fields_by_name['java_plugin_runtime_env'].message_type = _PLUGINRUNTIMEENV
_RUNTIMEENV.oneofs_by_name['python_runtime_env'].fields.append(
  _RUNTIMEENV.fields_by_name['pip_runtime_env'])
_RUNTIMEENV.fields_by_name['pip_runtime_env'].containing_oneof = _RUNTIMEENV.oneofs_by_name['python_runtime_env']
_RUNTIMEENV.oneofs_by_name['python_runtime_env'].fields.append(
  _RUNTIMEENV.fields_by_name['conda_runtime_env'])
_RUNTIMEENV.fields_by_name['conda_runtime_env'].containing_oneof = _RUNTIMEENV.oneofs_by_name['python_runtime_env']
_RUNTIMEENV.oneofs_by_name['python_runtime_env'].fields.append(
  _RUNTIMEENV.fields_by_name['py_container_runtime_env'])
_RUNTIMEENV.fields_by_name['py_container_runtime_env'].containing_oneof = _RUNTIMEENV.oneofs_by_name['python_runtime_env']
_RUNTIMEENV.oneofs_by_name['python_runtime_env'].fields.append(
  _RUNTIMEENV.fields_by_name['py_plugin_runtime_env'])
_RUNTIMEENV.fields_by_name['py_plugin_runtime_env'].containing_oneof = _RUNTIMEENV.oneofs_by_name['python_runtime_env']
_RUNTIMEENV.oneofs_by_name['java_runtime_env'].fields.append(
  _RUNTIMEENV.fields_by_name['jars_runtime_env'])
_RUNTIMEENV.fields_by_name['jars_runtime_env'].containing_oneof = _RUNTIMEENV.oneofs_by_name['java_runtime_env']
_RUNTIMEENV.oneofs_by_name['java_runtime_env'].fields.append(
  _RUNTIMEENV.fields_by_name['maven_runtime_env'])
_RUNTIMEENV.fields_by_name['maven_runtime_env'].containing_oneof = _RUNTIMEENV.oneofs_by_name['java_runtime_env']
_RUNTIMEENV.oneofs_by_name['java_runtime_env'].fields.append(
  _RUNTIMEENV.fields_by_name['java_container_runtime_env'])
_RUNTIMEENV.fields_by_name['java_container_runtime_env'].containing_oneof = _RUNTIMEENV.oneofs_by_name['java_runtime_env']
_RUNTIMEENV.oneofs_by_name['java_runtime_env'].fields.append(
  _RUNTIMEENV.fields_by_name['java_plugin_runtime_env'])
_RUNTIMEENV.fields_by_name['java_plugin_runtime_env'].containing_oneof = _RUNTIMEENV.oneofs_by_name['java_runtime_env']
DESCRIPTOR.message_types_by_name['PipRuntimeEnv'] = _PIPRUNTIMEENV
DESCRIPTOR.message_types_by_name['CondaRuntimeEnv'] = _CONDARUNTIMEENV
DESCRIPTOR.message_types_by_name['ContainerRuntimeEnv'] = _CONTAINERRUNTIMEENV
DESCRIPTOR.message_types_by_name['PluginRuntimeEnv'] = _PLUGINRUNTIMEENV
DESCRIPTOR.message_types_by_name['JarsRuntimeEnv'] = _JARSRUNTIMEENV
DESCRIPTOR.message_types_by_name['MavenRuntimeEnv'] = _MAVENRUNTIMEENV
DESCRIPTOR.message_types_by_name['RuntimeEnvUris'] = _RUNTIMEENVURIS
DESCRIPTOR.message_types_by_name['RuntimeEnv'] = _RUNTIMEENV
DESCRIPTOR.message_types_by_name['RuntimeEnvInfo'] = _RUNTIMEENVINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PipRuntimeEnv = _reflection.GeneratedProtocolMessageType('PipRuntimeEnv', (_message.Message,), {

  'Config' : _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
    'DESCRIPTOR' : _PIPRUNTIMEENV_CONFIG,
    '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
    # @@protoc_insertion_point(class_scope:ray.rpc.PipRuntimeEnv.Config)
    })
  ,
  'DESCRIPTOR' : _PIPRUNTIMEENV,
  '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
  # @@protoc_insertion_point(class_scope:ray.rpc.PipRuntimeEnv)
  })
_sym_db.RegisterMessage(PipRuntimeEnv)
_sym_db.RegisterMessage(PipRuntimeEnv.Config)

CondaRuntimeEnv = _reflection.GeneratedProtocolMessageType('CondaRuntimeEnv', (_message.Message,), {
  'DESCRIPTOR' : _CONDARUNTIMEENV,
  '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
  # @@protoc_insertion_point(class_scope:ray.rpc.CondaRuntimeEnv)
  })
_sym_db.RegisterMessage(CondaRuntimeEnv)

ContainerRuntimeEnv = _reflection.GeneratedProtocolMessageType('ContainerRuntimeEnv', (_message.Message,), {
  'DESCRIPTOR' : _CONTAINERRUNTIMEENV,
  '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
  # @@protoc_insertion_point(class_scope:ray.rpc.ContainerRuntimeEnv)
  })
_sym_db.RegisterMessage(ContainerRuntimeEnv)

PluginRuntimeEnv = _reflection.GeneratedProtocolMessageType('PluginRuntimeEnv', (_message.Message,), {

  'Plugin' : _reflection.GeneratedProtocolMessageType('Plugin', (_message.Message,), {
    'DESCRIPTOR' : _PLUGINRUNTIMEENV_PLUGIN,
    '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
    # @@protoc_insertion_point(class_scope:ray.rpc.PluginRuntimeEnv.Plugin)
    })
  ,
  'DESCRIPTOR' : _PLUGINRUNTIMEENV,
  '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
  # @@protoc_insertion_point(class_scope:ray.rpc.PluginRuntimeEnv)
  })
_sym_db.RegisterMessage(PluginRuntimeEnv)
_sym_db.RegisterMessage(PluginRuntimeEnv.Plugin)

JarsRuntimeEnv = _reflection.GeneratedProtocolMessageType('JarsRuntimeEnv', (_message.Message,), {
  'DESCRIPTOR' : _JARSRUNTIMEENV,
  '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
  # @@protoc_insertion_point(class_scope:ray.rpc.JarsRuntimeEnv)
  })
_sym_db.RegisterMessage(JarsRuntimeEnv)

MavenRuntimeEnv = _reflection.GeneratedProtocolMessageType('MavenRuntimeEnv', (_message.Message,), {
  'DESCRIPTOR' : _MAVENRUNTIMEENV,
  '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
  # @@protoc_insertion_point(class_scope:ray.rpc.MavenRuntimeEnv)
  })
_sym_db.RegisterMessage(MavenRuntimeEnv)

RuntimeEnvUris = _reflection.GeneratedProtocolMessageType('RuntimeEnvUris', (_message.Message,), {
  'DESCRIPTOR' : _RUNTIMEENVURIS,
  '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
  # @@protoc_insertion_point(class_scope:ray.rpc.RuntimeEnvUris)
  })
_sym_db.RegisterMessage(RuntimeEnvUris)

RuntimeEnv = _reflection.GeneratedProtocolMessageType('RuntimeEnv', (_message.Message,), {

  'EnvVarsEntry' : _reflection.GeneratedProtocolMessageType('EnvVarsEntry', (_message.Message,), {
    'DESCRIPTOR' : _RUNTIMEENV_ENVVARSENTRY,
    '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
    # @@protoc_insertion_point(class_scope:ray.rpc.RuntimeEnv.EnvVarsEntry)
    })
  ,

  'ExtensionsEntry' : _reflection.GeneratedProtocolMessageType('ExtensionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _RUNTIMEENV_EXTENSIONSENTRY,
    '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
    # @@protoc_insertion_point(class_scope:ray.rpc.RuntimeEnv.ExtensionsEntry)
    })
  ,
  'DESCRIPTOR' : _RUNTIMEENV,
  '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
  # @@protoc_insertion_point(class_scope:ray.rpc.RuntimeEnv)
  })
_sym_db.RegisterMessage(RuntimeEnv)
_sym_db.RegisterMessage(RuntimeEnv.EnvVarsEntry)
_sym_db.RegisterMessage(RuntimeEnv.ExtensionsEntry)

RuntimeEnvInfo = _reflection.GeneratedProtocolMessageType('RuntimeEnvInfo', (_message.Message,), {
  'DESCRIPTOR' : _RUNTIMEENVINFO,
  '__module__' : 'src.ray.protobuf.runtime_env_common_pb2'
  # @@protoc_insertion_point(class_scope:ray.rpc.RuntimeEnvInfo)
  })
_sym_db.RegisterMessage(RuntimeEnvInfo)


DESCRIPTOR._options = None
_RUNTIMEENV_ENVVARSENTRY._options = None
_RUNTIMEENV_EXTENSIONSENTRY._options = None
# @@protoc_insertion_point(module_scope)
