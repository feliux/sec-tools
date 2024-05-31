**Converting bytes to and from packets**

In some cases, there may be raw bytes that you want to convert into a packet or vice versa. This example creates a simple packet and then obtains the raw bytes that make up the packet. The raw bytes are then taken and converted back into a packet to demonstrate the process.

In this example, we will create and serialize a packet using `gopacket.SerializeLayers()`. The packet consists of several layers: Ethernet, IP, TCP, and payload. During serialization, if any of the packets come back as nil, this means that it could not decode it into the proper layer (malformed or incorrect packet type). After serializing the packet into a buffer, we will get a copy of the raw bytes that make up the packet with `buffer.Bytes()`. With the raw bytes, we can then decode the data layer by layer using `gopacket.NewPacket()`. By taking advantage of `SerializeLayers()`, you can convert packet structs to raw bytes, and using `gopacket.NewPacket()`, you can convert the raw bytes back to structured data.

`NewPacket()` takes the raw bytes as the first parameter. The second parameter is the lowest-level layer you want to decode. It will decode that layer and all layers on top of it. The third parameter for `NewPacket()` is the type of decoding and must be one of the following:

- `gopacket.Default`: This is to decode all at once, and is the safest.
- `gopacket.Lazy`: This is to decode on demand, but it is not concurrent safe.
- `gopacket.NoCopy`: This will not create a copy of the buffer. Only use it if you can guarantee the packet data in the memory will not change
