var homepage = 'http://haldean.org'

$.domReady(function() {
  var page = document.location.search.substring(1)
  if (page[page.length - 1] == '/') page = page.substring(0, page.length - 1)
  if (!page) {
    window.location = homepage
    return
  }

  var url = 'text/' + page + '.md'

  document.title = page;
  document.getElementById("viewsource").setAttribute("href", url)

  $.ajax({
    url: url,
    type:'html',
    success: function(resp) {
      if (!resp) {
        window.location = homepage
      }

      document.getElementById("content").innerHTML = markdown.toHTML(resp)
      $('pre').each(function(el, index) {
        hljs.highlightBlock(el, '  ')
      })
    }})
})
