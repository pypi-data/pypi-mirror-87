Kasten 🖃


Binary serialization format with metadata, validation, and configurable hash IDs with proof-of-work (VDF) support.

Kasten is intended to wrap messages for transport agnostic communication.

Sending a message:

```
import kasten

# Bob creates message

message = b"hello world"
# Mode for any external lib to use
encrypt_mode = 0
packed_message: bytes = kasten.generator.pack.pack(message, 'txt', encrypt_mode)

# We pick the base generator which checks for sha3_256 validity and that's it
# However we could also pick KastenMimcGenerator which has both validity and proof-of-work ratelimiting
# Or, we could make our own. Both parties just need the same logic.
kasten = kasten.generator.KastenBaseGenerator.generate(packed_message)

message_checksum: bytes = kasten.id

# Bob sends packed_message and message_checksum to Alice

```

Receiving a message:

```
import kasten

# Alice receives message
bobs_message = b'\x93\xa3txt\x00\xce_F\xc7!\nhello world'
bobs_checksum = b"\xac\x83K=n\xdb\xba\x9aJ\xca:\x82]'9b\xd0\x98\xda\xee'\x9f\xf2\xd7\x94\x9e\x91\x94\x9dnh6\x02\x03\xf0\xfe\x85\xbdrLj]R\xeb;xB@"

# Recreate on Alice's end using the checksum, message, and the same generator
# The generator will automatically check message validity and throw a kasten.exceptions.InvalidID exception if failed
kasten_message = kasten.Kasten(bobs_checksum, bobs_message, kasten.generator.KastenBaseGenerator)
```

