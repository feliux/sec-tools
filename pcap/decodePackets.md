**Decoding packets faster**

If we know what layers to expect, we can use existing structures to store the packet information instead of creating new structs for every packet that takes time and memory. It is faster to use `DecodingLayerParser`. It is like marshaling and unmarshaling data.

This example demonstrates how to create layer variables at the beginning of the program and reuse the same variables over and over instead of creating new ones for each packet. A parser is created with `gopacket.NewDecodingLayerParser()`, which we provide with the layer variables we want to use. One caveat here is that it will only decode the layer types that you created initially.
