$.domReady(function() {
  var page = document.location.hash.substring(1)
  if (!page) {
    window.location = 'http://haldean.org'
  }

  $.ajax({
    url: 'text/' + page + '.md',
    type:'html',
    success: function(resp) {
      document.getElementById("content").innerHTML = markdown.toHTML(resp)
      $('pre').each(function(el, index) {
        console.log(el)
        hljs.highlightBlock(el, '  ')
      })
    }})
})
