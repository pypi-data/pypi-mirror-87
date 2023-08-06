# coding: utf-8
import os
import logging

def get_stream_logger(name='ubik-toolbelt'):
	stream_logger = logging.getLogger(name)
	ch = logging.StreamHandler()
	stream_logger.setLevel(logging.INFO)
	ch.setLevel(logging.INFO)
	stream_logger.addHandler(ch)
	return stream_logger

stream_logger 	= get_stream_logger()
