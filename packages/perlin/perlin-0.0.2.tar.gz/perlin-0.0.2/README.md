# perlin
======

Create perlin noise in 1D, 2D, and 3D!

## Features

- 1D perlin noise
- 2D perlin noise
- 3D perlin noise
- Seed capability
- Tested
- Completly written in python
- No dependencies

## Usage

This library can be used for generating random terrain for games or getting perlin noise. This library also supports octaves.

## Example

```python
import perlin

p = perlin.Perlin(6789) #6789 is the seed

print(p.one(0)) #1D, 0 is the X value
print(p.two(0, 1)) #2D, 0 is the X value and 1 is the Y value
print(p.three(0, 1, 2)) #3D,  0 is the X value, 1 is the Y value, 2 is the Z value

print(p.one_octave(0)) #Use this for octaves, you can ajust the octave variables but this gives you 2 octaves
```

## Know limitations

Slower than noise library
Slower with octaves (Work in progress)
Some bugs on different seeds

## New Features

Now has octave support!