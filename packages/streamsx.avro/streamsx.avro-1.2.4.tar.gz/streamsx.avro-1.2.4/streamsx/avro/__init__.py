# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

"""
Overview
++++++++

Provides functions for serialization and deserialization of messages in an Apache Avro format.

The following transformations are supported:
 * JSON -> AVRO
 * AVRO -> JSON


Sample
++++++

A simple example of a Streams application that serializes and deserializes messages::

    from streamsx.topology.topology import *
    from streamsx.topology.schema import CommonSchema, StreamSchema
    from streamsx.topology.context import submit
    import streamsx.avro as avro

    topo = Topology()

    avro_schema = '{"type" : "record", "name" : "hw_schema", "fields" : [{"name" : "a", "type" : "string"}]}'
    s = topo.source([{'a': 'Hello'}, {'a': 'World'}, {'a': '!'}]).as_json()
    # convert json to avro blob
    o = s.map(avro.JSONToAvro(avro_schema))
    # convert avro blob to json
    res = o.map(avro.AvroToJSON(avro_schema))
    res.print()

    submit('STREAMING_ANALYTICS_SERVICE', topo)
    # Use for IBM Streams including IBM Cloud Pak for Data
    # submit ('DISTRIBUTED', topo, cfg)

"""

__version__='1.2.4'

__all__ = ['AvroToJSON', 'JSONToAvro', 'download_toolkit', 'json_to_avro', 'avro_to_json']
from streamsx.avro._avro import download_toolkit, json_to_avro, avro_to_json, AvroToJSON, JSONToAvro

