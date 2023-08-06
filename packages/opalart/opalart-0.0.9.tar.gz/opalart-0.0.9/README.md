# Opal Art

Gathers beautiful art. Perhaps as beautiful as [Opal](https://en.wikipedia.org/wiki/Opal).

## Installing

```bash
$ pip install opalart
```

## Quick Start

```python
import opalart
client = opalart.yandere()
images = await client.getposts(['thighhighs'])
# Do stuff with the images
```

Or grab a single image.  
This makes the same call as the above, but returns a single random image from the results.

```python
import opalart
client = opalart.yandere()
image = await client.randpost(['thighhighs'])
# Do stuff with the image
```
