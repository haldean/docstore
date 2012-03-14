$.domReady(function() {
  var page = document.location.search.substring(1)
  if (page[-1] == '/') page = page.substring(0, page.length - 1)
  if (!page) {
    window.location = 'http://haldean.org'
  }

  $.ajax({
    url: 'text/' + page + '.md',
    type:'html',
    success: function(resp) {
      document.getElementById("content").innerHTML = markdown.toHTML(resp)
      $('pre').each(function(el, index) {
        hljs.highlightBlock(el, '  ')
      })
    }})
})
