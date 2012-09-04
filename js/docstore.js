var homepage = 'http://haldean.org'

var converter = new Showdown.converter();

$.domReady(function() {
  var page = document.location.search.substring(1)
  if (page[page.length - 1] == '/') page = page.substring(0, page.length - 1)
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
