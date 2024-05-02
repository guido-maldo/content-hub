var youtubeIframes = document.querySelectorAll('div.video iframe');
var players = [];

var tag = document.createElement('script');
tag.src = 'https://www.youtube.com/iframe_api';
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

youtubeIframes.forEach(iframe => { 
    iframe.src = iframe.src + '?enablejsapi=1';
    iframe.classList.add('youtube-iframe');
});

function onYouTubeIframeAPIReady() {
    youtubeIframes.forEach(iframe =>    
        players.push(new YT.Player(iframe))
    );
}

// Function to stop Reddit iframe video playback
function stopRedditVideo(modalId) {
  var iframe = document.querySelector('#' + modalId + ' iframe');
  
  // Reset the iframe to its initial state
  iframe.src = iframe.src;
}

// Observe for changes in reddit iframe's height attribute
function observeHeightChanges(iframe) {
  const observer = new MutationObserver(mutationsList => {
    for (let mutation of mutationsList) {
      if (mutation.type === 'attributes' && mutation.attributeName === 'height') {
        iframe.style.height = iframe.height + 'px';
        break; // No need to continue observing after one attribute change
      }
    }
  });

  observer.observe(iframe, { attributes: true });
}

function resizeRedditModal(modalId) {
  var iframe = document.querySelector('#' + modalId + ' iframe');

  // If the iframe height attribute is zero then give it a default style height
  if (iframe.height == '0') {
    iframe.style.height = '260px'; 
  } else { // Else match the iframe style height to its attribute height
    iframe.style.height = iframe.height + 'px';
  }

  // Match the iframe style width to its attribute width
  iframe.style.width = iframe.width + 'px';

  var postId = modalId.substring("post".length, modalId.indexOf("Modal"));
  var postType = document.querySelector('#post' + postId + 'Type').innerText;

  // Reddit posts of type 'Text' can include 'read more' that expands iframe
  if (postType == 'Text') {
    // Update iframe height dynamically after is initial resize
    observeHeightChanges(iframe);
  }
}

// Event listener for modal close event
document.addEventListener('hidden.bs.modal', event => {
  // Get the ID of the closed modal
  var modalId = event.target.id;
  
  // Check if the modalId begins with "video"
  if (modalId.startsWith("video")) {
    
    // Extract the value between "video" and "Modal"
    var videoId = parseInt(modalId.substring("video".length, modalId.indexOf("Modal")));

    // Stops video playback when modal is closed
    players[videoId-1].stopVideo();
  } else { 
    var postId = modalId.substring("post".length, modalId.indexOf("Modal"));
    var postType = document.querySelector('#post' + postId + 'Type').innerText;

    if (postType == 'Video') {
      stopRedditVideo(modalId);
    }
  }
});

// Event listener for modal open event
document.addEventListener('shown.bs.modal', event => {
  // Get the ID of the opened modal
  var modalId = event.target.id;

  if (modalId.startsWith("post")) {
    resizeRedditModal(modalId);
  }
});

window.addEventListener('load', function() {
  var redditIframes = document.querySelectorAll('.redditContent iframe');

  // Add a class to each iframe element embedding a reddit post
  redditIframes.forEach(iframe => { 
    iframe.classList.add('reddit-iframe');
  });
});