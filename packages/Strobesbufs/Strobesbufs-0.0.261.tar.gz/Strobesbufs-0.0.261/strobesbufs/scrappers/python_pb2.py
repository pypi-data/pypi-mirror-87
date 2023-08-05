# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: python.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='python.proto',
  package='strobesbufs.scrappers.python',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0cpython.proto\x12\x1cstrobesbufs.scrappers.python\"\x92\x01\n\x06Python\x12\x0e\n\x06source\x18\x01 \x01(\t\x12\x0b\n\x03\x63ve\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x18\n\x10\x61\x66\x66\x65\x63ted_package\x18\x05 \x01(\t\x12\x19\n\x11\x61\x66\x66\x65\x63ted_versions\x18\x06 \x01(\t\x12\x15\n\rlast_modified\x18\x07 \x01(\t\">\n\x06Result\x12\x34\n\x06python\x18\x01 \x03(\x0b\x32$.strobesbufs.scrappers.python.Pythonb\x06proto3'
)




_PYTHON = _descriptor.Descriptor(
  name='Python',
  full_name='strobesbufs.scrappers.python.Python',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='source', full_name='strobesbufs.scrappers.python.Python.source', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cve', full_name='strobesbufs.scrappers.python.Python.cve', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='strobesbufs.scrappers.python.Python.id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='strobesbufs.scrappers.python.Python.description', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='affected_package', full_name='strobesbufs.scrappers.python.Python.affected_package', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='affected_versions', full_name='strobesbufs.scrappers.python.Python.affected_versions', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='last_modified', full_name='strobesbufs.scrappers.python.Python.last_modified', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=47,
  serialized_end=193,
)


_RESULT = _descriptor.Descriptor(
  name='Result',
  full_name='strobesbufs.scrappers.python.Result',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='python', full_name='strobesbufs.scrappers.python.Result.python', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=195,
  serialized_end=257,
)

_RESULT.fields_by_name['python'].message_type = _PYTHON
DESCRIPTOR.message_types_by_name['Python'] = _PYTHON
DESCRIPTOR.message_types_by_name['Result'] = _RESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Python = _reflection.GeneratedProtocolMessageType('Python', (_message.Message,), {
  'DESCRIPTOR' : _PYTHON,
  '__module__' : 'python_pb2'
  # @@protoc_insertion_point(class_scope:strobesbufs.scrappers.python.Python)
  })
_sym_db.RegisterMessage(Python)

Result = _reflection.GeneratedProtocolMessageType('Result', (_message.Message,), {
  'DESCRIPTOR' : _RESULT,
  '__module__' : 'python_pb2'
  # @@protoc_insertion_point(class_scope:strobesbufs.scrappers.python.Result)
  })
_sym_db.RegisterMessage(Result)


# @@protoc_insertion_point(module_scope)
