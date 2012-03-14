docstore: Easy Public Document Storage
====

toc-here

What is docstore?
---
docstore is an incredibly simple collection of scripts that allow you to very
simply host a number of static Markdown documents. I designed it with the
intention of making it very easy to add and update documents while keeping the
system itself as simple as possible.

Installing docstore
---
docstore itself is just a few scripts which can be [downloaded as a ZIP
file][zipfile] or [cloned on Github][github] (pull requests welcome!). It
requires a Redis server running on the default port on the same machine that
serves the documents. It also requires the `BeautifulSoup`, `jinja2` and `redis`
python modules, both of which are available using `pip` or `easy_install`. The
`redis` module is not yet Python 3 compatible -- docstore will be Python 3
compatible as soon as the `redis` module is. Until then, it works on Python 2.5
through 2.7.

Note that `BeautifulSoup` is not required if you choose to not use the table of
contents feature.

[zipfile]: https://github.com/haldean/docstore/zipball/master
[github]: https://github.com/haldean/docstore/

Using docstore
---
Each page in docstore has a name and content (and that's it). The name must be a
string of alphanumeric characters, and may not contain spaces. The content can
be whatever you want. Documents can be accessed at `mydomain.com/title`, where
`title` is the title of the document.

docstore assumes that it is running on a different machine than the one you are
updating it from. As such, there are a number of scripts in the `scripts/`
directory which make it easy to remotely update the documents on your store.
Before they can be run, though, your server must be configured.

### Configuring the server
`docstore.py` is the meat of docstore -- it serves the pages from redis on port
8000. The port can be changed by changing the `port = 8000` line at the top of
`docstore.py`. I recommend running `docstore.py` as an unprivileged user on a
higher port, and use a webserver to proxy to that port, for both security
reasons and because docstore can't serve static files. To run
[docstore.haldean.org][ds], I run mongrel2 which proxies to
[haldean.org:8000][dsp] for any URL that doesn't match "`static/`". Requests for
static content like stylesheets and images then can be served from the
filesystem.

[ds]: http://docstore.haldean.org
[dsp]: http://haldean.org:8000

### Configuring output
docstore uses the two Jinja2 templates stored in the `templates/` directory to
style the output. `content.html` is the template used for the documents, and
`index.html` is used for the listing of all of the documents. If you want to
design your own content template, the template variable `content` contains the
document, and `title` contains the title of the page. The index template takes
only one parameter, `slugs`, which is a list of page titles. Note that there's
no requirement that you have a listing of documents on the homepage -- you can
safely remove the `slugs` variable from your template and have a static
homepage. 

### Remotely updating documents
docstore comes with two convenience scripts: `mkpage.sh` and `rmpage.sh`.
mkpage takes one or two arguments. The first argument is the page title. If the
second argument is provided, it is the Markdown file to be uploaded as the new
page. If I wanted to upload the file `docstore.md` as `docstore`, I would run:

    scripts/mkpage.sh docstore docstore.md

If the second argument is omitted, it will fire up your editor (defined in the
`EDITOR` shell variable). When you are finished writing your article, just save
and quit your editor. It will confirm that you want to upload what you just
wrote before committing the change. If you provide the name of an
already-existing document, it will insert the page into your editor so you can
edit it inline -- for example, if I wanted to edit the document I uploaded in
the last example, I could run:

    EDITOR=gvim scripts/mkpage.sh docstore

And gvim would open with the contents of docstore already in the editor. If I
make any changes, I can save and quit and it will upload my changes.

Note that these scripts require you to use SSH keys to connect to your server --
simple passphrase authentication will not work, as it is designed to work
without user interaction. If your keys have a passphrase, you can use `ssh-add`
to unlock your key in `ssh-agent`, which will then allow mkpage and rmpage to
upload without user interaction.









