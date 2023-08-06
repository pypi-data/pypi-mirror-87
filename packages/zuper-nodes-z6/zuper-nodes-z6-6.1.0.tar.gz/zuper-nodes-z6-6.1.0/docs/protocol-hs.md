
Minimal node protocol
====================

The node must support the following.

## Basic protocol

The wires contain a sequence of CBOR messages.

Each message is a dictionary.


## Basic control mechanism

To every message the node responds with one of the two messages "understood", or "not understood".

If understood:


```yaml
control: understood
```

If not understood:

```yaml
control: not-understood
   data: optional message string
```

In this case, the other party should not expect any result.

Then there is a sequence of messages, terminated with a sequence marker:

```yaml
control: over
```

## Get capabilities 

The node might receive a `capabilities` message,
whose `data` dictionary contains a dictionary.   The semantics
of these depend on the interaction. 

```yaml
control: capabilities
   data: 
      z2:
      protocol-reflection: true

```

The node must respond with the sequence:

```yaml
- control: understood
- control: capabilities
     data:
       z2:
        protocol-reflection: true
- control: over
```




