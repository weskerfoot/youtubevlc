// ==UserScript==
// @description Make VLC play youtube videos on another computer
// @include https://www.youtube.com/*
// @include https://youtu.be/*
// @include http://youtu.be/*
// @include http://youtube.com/*
// @include http://www.youtu.be/*
// @include https://www.youtu.be/*
// @include http://www.youtube.com/*
// @name YoutubeVLC
// @namespace ytvlc
// @require http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js
// ==/UserScript==

var url = encodeURIComponent(document.location.href);

var buttonParent = $("#watch7-secondary-actions");

buttonParent.append(function() {
  return "<button class='addandplay yt-uix-button-epic-nav-item'>Play With VLC</button>";
});

$(".addandplay").click(
  function () {
    GM_xmlhttpRequest({
      method: "GET",
      url : "http://127.0.0.1:8080/addyoutube?url="+url+"&play=true",
      onload : function(response) {
        console.log(response.responseText);
      }
    });
  });

buttonParent.append(function() {
  return "<button class='vlcadd yt-uix-button-epic-nav-item'>Enqueue to VLC</button>";
});

$(".vlcadd").click(
  function () {
    GM_xmlhttpRequest({
      method: "GET",
      url : "http://127.0.0.1:8080/addyoutube?url="+url+"&play=false",
      onload : function(response) {
        console.log(response.responseText);
      }
    });
  });

buttonParent.append(function() {
  return "<button class='nextvideo yt-uix-button-epic-nav-item'>Next Video</button>";
});

$(".nextvideo").click(
    function () {
      GM_xmlhttpRequest({
        method : "GET",
        url : "http://127.0.0.1:8080/next",
        onload : function(response) {
          console.log(response);
        }
      });
    });
