htmltoc: Simple HTML Table of Contents
===

<script src="https://gist.github.com/1346114.js"></script>

htmltoc is a very simple Python method that uses the `BeautifulSoup` module to
generate a table of contents. It can be found [here][gist]. It takes a string
containing HTML as an argument, and outputs the table of contents as HTML. If
the headers have `id` attributes, it will add anchor links to the corresponding
items in the table of contents. You can see it in action at [docstore][].

[gist]: https://gist.github.com/1346114
[docstore]: http://docstore.haldean.org/artray



