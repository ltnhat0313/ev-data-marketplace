// SmoothScroll v1.2.1
// https://github.com/galambalazs/smoothscroll

(function () {
  var defaultOptions = {
    frameRate: 150,
    animationTime: 400,
    stepSize: 120,
    pulseAlgorithm: true,
    pulseScale: 8,
    pulseNormalize: 1,
    accelerationDelta: 20,
    accelerationMax: 1,
    keyboardSupport: true,
    arrowScroll: 50,
    touchpadSupport: true,
    fixedBackground: true,
    excluded: "",
  };
  var options = defaultOptions;
  var isExcluded = false;
  var isFrame = false;
  var direction = { x: 0, y: 0 };
  var initDone = false;
  var root = document.documentElement;
  var activeElement;
  var observer;
  var deltaBuffer = [];
  var isMac = /^Mac/.test(navigator.platform);
  var key = {
    left: 37,
    up: 38,
    right: 39,
    down: 40,
    spacebar: 32,
    pageup: 33,
    pagedown: 34,
    end: 35,
    home: 36,
  };
  function init() {
    if (!document.body) return;
    var body = document.body;
    var html = document.documentElement;
    var windowHeight = window.innerHeight;
    var scrollHeight = body.scrollHeight;
    root = document.compatMode.indexOf("CSS") >= 0 ? html : body;
    activeElement = body;
    initDone = true;
    if (top != self) {
      isFrame = true;
    } else if (
      scrollHeight > windowHeight &&
      (body.offsetHeight <= windowHeight || html.offsetHeight <= windowHeight)
    ) {
      var pending = false;
      var refresh = function () {
        if (!pending && html.scrollHeight != document.height) {
          pending = true;
          setTimeout(function () {
            html.style.height = document.height + "px";
            pending = false;
          }, 500);
        }
      };
      html.style.height = "auto";
      setTimeout(refresh, 10);
      if (root.offsetHeight <= windowHeight) {
        var underlay = document.createElement("div");
        underlay.style.clear = "both";
        body.appendChild(underlay);
      }
    }
    if (!options.fixedBackground && !isExcluded) {
      body.style.backgroundAttachment = "scroll";
      html.style.backgroundAttachment = "scroll";
    }
  }
  var que = [];
  var pending = false;
  var lastScroll = +new Date();
  function scrollArray(elem, left, top, delay) {
    delay || (delay = 1000);
    directionCheck(left, top);
    if (options.accelerationMax != 1) {
      var now = +new Date();
      var elapsed = now - lastScroll;
      if (elapsed < options.accelerationDelta) {
        var factor = (1 + 30 / elapsed) / 2;
        if (factor > 1) {
          factor = Math.min(factor, options.accelerationMax);
          left *= factor;
          top *= factor;
        }
      }
      lastScroll = +new Date();
    }
    que.push({
      x: left,
      y: top,
      lastX: left < 0 ? 0.99 : -0.99,
      lastY: top < 0 ? 0.99 : -0.99,
      start: +new Date(),
    });
    if (pending) {
      return;
    }
    var scrollWindow = elem === document.body;
    var step = function (time) {
      var now = +new Date();
      var scrollings = [];
      // ... (Phần còn lại của thư viện SmoothScroll)
    };
  }
  // ... (Phần còn lại của thư viện SmoothScroll)
})();