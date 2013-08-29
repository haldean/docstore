var homepage = 'http://haldean.org'

var converter = new Showdown.converter();

function findFirstOf(str, chars) {
  var first = -1;
  for (var i = 0; i < chars.length; i++) {
    var loc = str.indexOf(chars[i])
    if (loc != -1 && (loc < first || first == -1)) {
      first = loc;
    }
  }
  return first;
}

$.domReady(function() {
  var page = document.location.search.substring(1)
  var pageEnd = findFirstOf(page, ['&', '/'])
  if (pageEnd >= 0) {
    page = page.substring(0, pageEnd)
  }
  if (!page) {
    window.location = homepage
    return
  }

  var url = 'text/' + page + '.md'
  $.ajax({
    url: url,
    type:'html',
    success: function(resp) {
      if (!resp) {
        window.location = homepage
      }

      document.getElementById('content').innerHTML = converter.makeHtml(resp)
      $('pre').each(function(el, index) {
        hljs.highlightBlock(el, '  ')
      })
    }})

  document.title = page;
  document.getElementById('viewsource').setAttribute('href',
    'https://raw.github.com/haldean/docstore/master/' + url)

  MathJax.Hub.Config({
  tex2jax: {
    inlineMath: [['$','$'], ['\\(','\\)']],
    processEscapes: true
  }
});
})
