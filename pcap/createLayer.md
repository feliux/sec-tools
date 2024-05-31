**Creating a custom layer**

You are not restricted to the most common layers, such as Ethernet, IP, and TCP. You can create your own layers. This has limited use for most people, but in some extremely rare cases it may make sense to replace the TCP layer with something customized to meet specific requirements.

This example demonstrates how to create a custom layer. This is good for implementing a protocol that is not already included with gopacket/layers package. There are over 100 layer types already included with gopacket. You can create custom layers at any level.

The first thing this code does is to define a custom data structure to represent our layer. The data structure not only holds our custom data (SomeByte and AnotherByte) but also needs a byte slice to store the rest of the actual payload, along with any other layers (restOfData).
