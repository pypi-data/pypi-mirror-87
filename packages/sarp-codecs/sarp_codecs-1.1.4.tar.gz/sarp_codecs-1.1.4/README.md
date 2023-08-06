## __Codecs for SARP__

Codecs is a package containing message schema for all networked SARP systems. It will help establish a consistent encoding scheme for all SARP related network communication.

## Installation

`pip install sarp_codecs`

## Example Usage

`from sarp_codecs.template_codec import TemplateCodec`

`telem_item = {"timestamp": 12345, "example_channel_1": 1, "example_channel_2": 2, "example_channel_3": 3}`

`fill_codec = TemplateCodec()`

`fill_codec.encode(telem_item)`

### Expected Output
The expected output will be the encoded version of telem_item