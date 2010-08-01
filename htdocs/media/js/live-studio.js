$(function() {
  var elem = $('#scrolling_log');

  if (elem.length == 0) {
    return;
  }

  window.setInterval(function () {
    $('pre', elem).load(elem.attr('data-url'));

    elem.attr({scrollTop: elem.attr("scrollHeight") });
  }, 1000);
});
