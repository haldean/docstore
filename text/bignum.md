The math of arbitrary-sized integers
====

Numbers in programming languages are usually a fixed size; an integer is usually
32 bits long, a "long integer" 64, etc. This isn't useful for lots of
applications &ndash; especially science and cryptography &ndash; and so most
programming langauges provide a mechanism for creating arbitrarily large
numbers.  Arbitrary-sized integers (also called "big numbers" or "bignums") are
numbers whose size is bounded only by the amount of memory available to your
program, at the expense of efficiency; arithmetic on bignums is not as fast as
arithmetic on native integral types, because they're not implemented in
hardware. Bignums are so useful that many programming languages including Python
and Lisp use bignums as the default integral type. In this article, I'll write
about some of the math behind bignums. Feel free to <a
href="will.h.brown+bignum@gmail.com">email me</a> with any questions you may
have.

Encoding bignums
---
The first thing we have to settle on is the encoding of our bignums. A lot of
introductory courses will have students implement them using an array of single
decimal digits, like so:

    8675309 = [8, 6, 7, 5, 3, 0, 9]

This is inefficient, though, as we don't have an easy way to store numbers less
than 10 compactly; the smallest data type we have at our disposal is usually a
`byte`, which has 8 bits of storage. Single digits never need more than 4.  This
encoding, then, uses about twice as much storage as it needs; the first four
bits of every digit in the array will always be zero.

We can extend this idea to be space-efficient, though. Let's stick with the
array of integers, but instead of saying that each is one decimal digit, let's
say that each is one digit in base 4294967296 (that's 2^32). Each element in the
array can then use all of the storage provided by a 32-bit `int`. For future
sections, we'll call this list $c$, and elements in the list will be $c\_i$,
where $c\_0$ is the least significant "digit". Given $c$, we can find the number
it represents (let's call it $X$) using the following formula:

$$
X = \Sigma\_{i = 0}^N (2^{32})^i c\_i
$$

The idea here is that, for each element in $c$, we take the power of 2^32 its
associated with, and multiply it by the element. Then we add these all up. It
may be more clear why this works if we consider it with 2^32 replaces by 10.
Then, for a bignum `[3, 4, 2]`, we get the following:

    10^2 * 3 + 10^1 * 4 + 10^0 * 2 = 300 + 40 + 2 = 342

Above, we're doing the same, but in base 2^32 instead.

Getting $c$ from $X$ is a bit harder to express so succinctly; an algorithm to
do it can be expressed in pseudo-C as:

    for (i = 0; X > 0; i++) {
      c[i] = X % 2^32;
      X /= 2^32;
    }

Here, we find the least significant digit using the modulo operator, store it in
`c`, take that digit off, and repeat. I'm assuming that we're using integer
division here, where the fractional part is truncated, so `3 / 4 = 0`.

Alright. Now we have a way to encode our bignums. Now we need to do something
interesting with them. Let's start with...

Addition
---
Now let's get down to business. 
