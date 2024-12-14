var commonUtils = {
  hasClass: function(node, className) {
    if (node.nodeType !== Node.ELEMENT_NODE) { return false; }
    if (node.classList) { return node.classList.contains(className); }

    var classNames = (node.getAttribute('class') || '').split(/\s/);
    return classNames.indexOf(className) >= 0;
  },
  addClassTo: function(node, className) {
    if (node.nodeType !== Node.ELEMENT_NODE) { return; }

    if(!commonUtils.hasClass(node, className)) {
      if (node.classList) {
        node.classList.add(className);
      } else {
        node.className = (node.className || '') + ' ' + className;
      }
    }
  },
  removeClassFrom: function(node, className) {
    if (node.nodeType !== Node.ELEMENT_NODE) { return; }

    if(commonUtils.hasClass(node, className)) {
      if (node.classList) {
        node.classList.remove(className);
      } else {
        var classNames = (node.getAttribute('class') || '').split(' ');
        var index = classNames.indexOf(className);
        if (index >= 0) { classNames.splice(index, 1); }
        node.setAttribute('class', classNames.join(' '));
      }
    }
  },
  getImageWidth: function (img, onServer) {
    if (img.jquery) { img = img[0]; }
    var result = null;
    if (onServer) {
      var pfDataWidth = img.getAttribute('pf-data-width') || img.getAttribute('data-pf_rect_width');
      if (pfDataWidth) { result = parseInt(pfDataWidth, 10); }
    } else if (img.getAttribute('data-pf_rect_width')) {
      result = parseInt(img.getAttribute('data-pf_rect_width'), 10);
    }

    /*
      Fetch current height/width if value is zero as firefox
      sets the width/height as zero for some images when we initially persist
      the values
    */
    if (result === null || result === 0 || typeof result != 'number' || isNaN(result)) {
      result = img.getBoundingClientRect().width;
    }
    return result;
  },

  getImageHeight: function (img, onServer) {
    if (img.jquery) { img = img[0]; }
    var result = null;
    if (onServer) {
      var pfDataHeight = img.getAttribute('pf-data-height') || img.getAttribute('data-pf_rect_height');
      if (pfDataHeight) { result = parseInt(pfDataHeight, 10); }
    } else if (img.getAttribute('data-pf_rect_height')) {
      result = parseInt(img.getAttribute('data-pf_rect_height'), 10);
    }

    /*
      Fetch current height/width if value is zero as firefox
      sets the width/height as zero for some images when we initially persist
      the values
    */
    if (result === null || result === 0 || typeof result != 'number' || isNaN(result)) {
      result = img.getBoundingClientRect().height;
    }
    return result;
  },

  MAX_SVG_SIZE: 1000,
  MAX_SVG_ICON_SIZE: 21,
  ICON_REGEXP: /icon/i,
  svgMaxValue: function(svg) {
    return this.ICON_REGEXP.test(svg.getAttribute('class') || '') ? this.MAX_SVG_ICON_SIZE : this.MAX_SVG_SIZE;
  },

  svgViewBox: function(svg) {
    var viewBox = svg.getAttribute('viewBox');
    if (viewBox) {
      var viewBoxValues = viewBox.split(' ');
      if (viewBoxValues.length === 4) { return { width: parseInt(viewBoxValues[2], 10), height: parseInt(viewBoxValues[3], 10) }; }
    }
    return {};
  },

  INFINITY: 1000000,
  getSvgImageWidth: function(svg, onServer) {
    var result = this.getImageWidth(svg, onServer) || this.INFINITY;
    var maxValue = this.svgMaxValue(svg);
    var viewBoxValue = this.svgViewBox(svg).width || this.INFINITY;
    return Math.min(result, maxValue, viewBoxValue);
  },

  getSvgImageHeight: function(svg, onServer) {
    var result = this.getImageHeight(svg, onServer);
    var maxValue = this.svgMaxValue(svg);
    var viewBoxValue = this.svgViewBox(svg).height || this.INFINITY;
    return Math.min(result, maxValue, viewBoxValue);
  },

  getTopWrapper: function(node) {
    var parent = node.parentNode;
    if (parent.childNodes.length > 1) { return node; }
    return this.getTopWrapper(parent);
  },
  selectorsNotToBeRemoved: [
    '.copyright',
    '#copyright',
    '.delete-no',
    '.delete-off',
    '.pf-author',
    '.print-content',
    '#print-content',
    '.pf-date',
    '#pf-date',
    '.pf-title',
    '.pf-footer',
    '.print-header',
    '.print-footer',
    '.print-yes',
    '.pf-content',
    '#pf-content',
  ],
  isDeletableElement: (function () {
    var CLICK_TO_DEL_ELEMENTS = 'small, footer, header, aside, details, dialog, figure, nav, summary, twitter-widget, p, img, blockquote, h1, h2, h3, h4, h5, h6, ol, ul, li, a, table, td, pre, span, code, dl, dt, dd, hr, div.pf-caption, video, figcaption, data';
    var MANY_ELEMENTS_THRESHOLD = 15;

    return function isDeletableElement(node) {
      return (
        !commonUtils.hasClass(node, 'non-delete') &&
        !$(node).find(commonUtils.selectorsNotToBeRemoved.join(', ')).length && (
          node.matches(CLICK_TO_DEL_ELEMENTS) ||
          $(node).find('*:visible').length <= MANY_ELEMENTS_THRESHOLD
        )
      );
    };
  })(),

  resizeImageCssClass: function(value) {
    return 'pf-size-' + value.replace('-size', '').replace('-images', '');
  },

  addCSS: function(css, doc, useBody) {
    var tagName = useBody ? 'body' : 'head';
    var element = doc.getElementsByTagName(tagName)[0];
    var style = doc.createElement('style');

    style.type = 'text/css';
    style.setAttribute('name', 'pf-style');

    if (style.styleSheet) {
      style.styleSheet.cssText = css;
    } else {
      style.appendChild(doc.createTextNode(css));
    }
    element.appendChild(style);
  },

  createIframe: function(doc) {
    var iframe = doc.createElement('iframe');
    // TODO: do we need this src? If yes add sha256 to manifest.json CSP to avoid. Commented for now
    // Error: "Refused to execute JavaScript URL because it violates the following Content Security Policy..."
    /* jshint -W107 */
    // iframe.src = "javascript:false";
    /* jshint +W107 */
    iframe.frameBorder = '0';
    iframe.allowTransparency = 'true';
    return iframe;
  },

  loadHtmlInIframe: function(doc, iframe, html) {
    var dom, idoc;

    try {
      idoc = iframe.contentWindow.document;
    } catch(e) {
      dom = doc.domain;
      /* jshint -W107 */
      iframe.src = "javascript:var d=document.open();d.domain='"+dom+"';void(0);";
      /* jshint +W107 */
      idoc = iframe.contentWindow.document;
    }
    idoc.write(html);
    idoc.close();
  }
};
function UUID() { // Public Domain/MIT
  var d = new Date().getTime();//Timestamp
  var d2 = ((typeof performance !== 'undefined') && performance.now && (performance.now()*1000)) || 0;//Time in microseconds since page-load or 0 if unsupported
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16;//random number between 0 and 16
      if(d > 0){//Use timestamp until depleted
          r = (d + r)%16 | 0;
          d = Math.floor(d/16);
      } else {//Use microseconds since page-load if supported
          r = (d2 + r)%16 | 0;
          d2 = Math.floor(d2/16);
      }
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
};
function toCdnUrl(url) {
  if(url.indexOf('//') === 0) { url = pfData.config.protocol + url; }
  var cdnPrefix = pfData.config.hosts.cdn;
  if (url.indexOf(cdnPrefix) === 0) { return url; }
  return cdnPrefix + url;
};
var persistComputedStylesAndRect = (function() {
  var STYLES_TO_SAVE = ['display', 'visibility'];
  var RECT_TO_SAVE = ['width', 'height'];
  var PREFIX = 'pf';

  function persistObject(node, object, propsToSave, objPrefix) {
    for(var i = 0, length = propsToSave.length; i < length; i++) {
      var prop = propsToSave[i];
      var key = [PREFIX, objPrefix, prop].join('_');
      node.dataset[key] = object[prop];
    }
  }

  function parentIsNotVisible(node) {
    var parent = node.parentElement;
    if (!parent) { return false; }
    return parent.getAttribute('data-pf_style_display') === 'none' || parent.getAttribute('data-pf_style_visibility') === 'hidden';
  }

  return function persistComputedStylesAndRect(node) {
    if(parentIsNotVisible(node)) {
      node.dataset.pf_style_display = 'none';
      node.dataset.pf_style_visibility = 'hidden';
      return;
    }

    var style = node.currentStyle || window.getComputedStyle(node);
    if (style) { persistObject(node, style, STYLES_TO_SAVE, 'style'); }
    var rect = node.getBoundingClientRect && node.getBoundingClientRect();
    var nodeName = node.nodeName.toUpperCase();
    if (nodeName === 'IMG' || nodeName === 'SVG' || nodeName === 'IFRAME') {
      if (rect) { persistObject(node, rect, RECT_TO_SAVE, 'rect'); }
    }
  };
})();
var toAbsoluteUrl = (function() {
  var absoluteUrlRegexp = /^https?:\/\//i;
  return function(src, pfConfigLocation) {
    if(!src) { return src; }
    var js = ['javascript', ':'].join('');

    if (src.startsWith(js)) {
      return src;
    } else if (src.startsWith('#')) {
      return src;
    } else if (absoluteUrlRegexp.test(src)) {
      return src;
    } else if (src.startsWith('//')) {
      return pfConfigLocation.protocol + src;
    } else {
      var imageDomain = pfConfigLocation.protocol + '//' + pfConfigLocation.host;
      if (!src.startsWith('/')) { src = '/' + src; }
      return imageDomain + src;
    }
  };
})();
var messageBus = (function() {
  var windowMappings = {
    algo: null,
    core: null,
    root: null
  };
  var setupDone = false;
  var connectionName;

  function findFrameWindow(name, rootWindow) {
    for (var i = 0; i < rootWindow.frames.length; i++) {
      var frame = rootWindow.frames[i];
      // NOTE: some 3d party iframes like twitter/youtube
      // doesn't allow to read their names throwing an exception
      try {
        if (frame.name === name) { return frame; }
      } catch(e) {}
    }
    var iframe = rootWindow.document.querySelector("iframe[name='" + name + "']");
    if (iframe) { return iframe.contentWindow; }
  }

  function findDestinationWindow(name) {
    var windowGetter = windowMappings[name];
    if (windowGetter) { return windowGetter(); }

    switch(connectionName) {
      case "algo":
        windowMappings.root = function() { return window.parent.parent; };
        windowMappings.core = function() { return window.parent; };
        windowMappings.algo = function() { return window; };
        break;
      case "pf-core":
        windowMappings.root = function() { return window.parent; };
        windowMappings.core = function() { return window; };
        windowMappings.algo = function() { return findFrameWindow('algo', window); };
        break;
      case "pdf_iframe":
        windowMappings.core = function() { return window.parent; };
        break;
      default:
        var coreWindow = function() { return findFrameWindow('pf-core', window); };
        windowMappings.root = function() { return window; };
        windowMappings.core = coreWindow;
        windowMappings.algo = function() { return findFrameWindow('algo', coreWindow()); };
        break;
    }

    return windowMappings[name]();
  }

  return {
    postMessage: function(destination, type, payload, onError) {
      var destinationWindow = findDestinationWindow(destination);
      if(!destinationWindow) {
        if (onError) { onError(); }
        return;
      }

      destinationWindow.postMessage({ type: type, payload: payload }, '*');
    },
    listen: function(name, handlers, onError) {
      if(setupDone) { return; }

      connectionName = name;

      window.addEventListener('message', function(event) {
        try {
          var data = event.data;
          if (!data) { return; }

          var type = data.type;
          if (!type) { return; }

          var handler = handlers[type];
          if (!handler) { return; }
          var payload = data.payload;

          handler(payload);
        } catch (e) {
          if (onError) { onError(e); }
          else { throw e; }
        }
      });
      setupDone = true;
    },
  };
})();
  
var logger = (function() {
  var METHODS = ['log', 'error', 'time', 'timeEnd'];
  var NOOP = function() {};

  function logEnabled(pfData) {
    return (
      pfData.config.environment === "development" ||
      pfData.config.environment === 'test' ||
      pfData.config.pfEnableLog ||
      pfData.config.urls.page.indexOf("pfdebug=1") >= 0
    );
  }

  var result = {
    init: function(pfData) {
      for(var i = 0; i < METHODS.length; i++) {
        var functionName = METHODS[i];
        if (logEnabled(pfData)) {
          result[functionName] = Function.prototype.bind.call(console[functionName], console);
        } else {
          result[functionName] = NOOP;
        }
      }
    },
  };

  // NOTE: setup default is to proxy to console
  for(var i = 0; i < METHODS.length; i++) {
    var functionName = METHODS[i];
    result[functionName] = Function.prototype.bind.call(console[functionName], console);
  }

  return result;
})();
var pfRedirect = (function () {
  return function(pfHost, userSettings, url) {
    var components = ['source=cs', 'url=' + encodeURIComponent(url)];

    for(var config in userSettings) {
      var setting = userSettings[config];
      if (typeof setting === 'object' && setting.value) {
        components.push(config + '=' + encodeURIComponent(setting.value));
      } else if (typeof setting !== 'undefined') {
        components.push(config + '=' + encodeURIComponent(setting));
      }
    }
    return pfHost + '/print/?' + components.join('&');
  };
})();
var printfriendlyOptionsParser = (function() {
  var META_REGEXP = /meta\[(\w+)=['"]([^'"]+)['"]\]/i;

  var __printfriendlyOptionsElement;
  var printfriendlyOptions = function() {
    __printfriendlyOptionsElement = __printfriendlyOptionsElement || document.querySelector('printfriendly-options');
    return __printfriendlyOptionsElement;
  };

  /**
   * This function accepts attribute value like this `foobar=1;foobaz=2;foobag=3`
   * and based on that constructs a new object. Example:
   * ```js
   * parseAttribute('foobar=1;foobaz=2;foobag=3')
   * => {
   *   foobar: 1, // read from string
   *   foobaz: 2, // read from string
   *   foobag: 3
   * }
   * ```
   * @param {string} attrValue - string like `foobar=1;foobaz=2;foobag=3`
   * @returns {Object}
  */
  var parseAttribute = function(attrValue) {
    var result = {};
    if(!attrValue) { return result; }

    var attrValuePieces = attrValue.trim().split(';');
    for (var i = 0; i < attrValuePieces.length; i++) {
      var element = attrValuePieces[i].trim();
      if (element) {
        var splitPoint = element.indexOf('=');
        var key = element.slice(0, splitPoint).trim();
        var value = element.slice(splitPoint + 1).trim();
        if (key && value) {
          if (value.startsWith('meta')) {
            var match = value.match(META_REGEXP);
            if (match) {
              result[key] = {type: 'meta', attributeName: match[1], attributeValue: match[2], value: value};
            }
          } else {
            result[key] = {type: 'selector', value: value};
          }
        }
      }
    }
    return result;
  };

  return {
    selectors: function() {
      var result = {};

      var options = printfriendlyOptions();
      if(!options) { return result; }

      var printfriendlyOptionsValue = options.getAttribute('data-selectors') || options.getAttribute('data-content');
      var parsedAttributeResult = parseAttribute(printfriendlyOptionsValue);

      if (parsedAttributeResult.contentSelectors) { result.contentSelectors = parsedAttributeResult.contentSelectors; }
      if (parsedAttributeResult.titleSelector) { result.titleSelector = parsedAttributeResult.titleSelector; }
      if (parsedAttributeResult.primaryImageSelector) { result.primaryImageSelector = parsedAttributeResult.primaryImageSelector; }
      if (parsedAttributeResult.authorSelector) { result.authorSelector = parsedAttributeResult.authorSelector; }
      if (parsedAttributeResult.dateSelector) { result.dateSelector = parsedAttributeResult.dateSelector; }
      if (parsedAttributeResult.removeSelectors) { result.removeSelectors = parsedAttributeResult.removeSelectors; }

      return result;
    },
    contentFeatures: function() {
      var result = { primaryImage: 'all', fetchOriginalPage: 'default' };
      var options = printfriendlyOptions();
      if(!options) { return result; }

      var contentFeaturesValue = options.getAttribute('data-content-features');
      var parsedAttributeResult = parseAttribute(contentFeaturesValue);

      if (parsedAttributeResult.showHiddenContent) { result.showHiddenContent = parsedAttributeResult.showHiddenContent.value; }
      if (parsedAttributeResult.customCSSURL) { result.customCSSURL = parsedAttributeResult.customCSSURL.value; }
      if (parsedAttributeResult.disablePDF) { result.disablePDF = parsedAttributeResult.disablePDF.value; }
      if (parsedAttributeResult.disablePrint) { result.disablePrint = parsedAttributeResult.disablePrint.value; }
      if (parsedAttributeResult.disableEmail) { result.disableEmail = parsedAttributeResult.disableEmail.value; }
      if (parsedAttributeResult.disableClickToDel) { result.disableClickToDel = parsedAttributeResult.disableClickToDel.value; }
      if (parsedAttributeResult.imageDisplayStyle) { result.imageDisplayStyle = parsedAttributeResult.imageDisplayStyle.value; }
      if (parsedAttributeResult.hideImages && parsedAttributeResult.hideImages.value === '1') {
        result.imagesSize = 'remove-images';
      }
      if (parsedAttributeResult.headerImageUrl) { result.headerImageUrl = parsedAttributeResult.headerImageUrl.value; }
      if (parsedAttributeResult.headerTagline) { result.headerTagline = parsedAttributeResult.headerTagline.value; }
      if (parsedAttributeResult.encodeImages) { result.encodeImages = parsedAttributeResult.encodeImages.value === '1'; }
      if (parsedAttributeResult.primaryImage) { result.primaryImage = parsedAttributeResult.primaryImage; }
      if (parsedAttributeResult.fetchOriginalPage) { result.fetchOriginalPage = parsedAttributeResult.fetchOriginalPage.value; }
      if (parsedAttributeResult.keepStyle) { result.keepStyle = parsedAttributeResult.keepStyle.value; }
      if (parsedAttributeResult.bgImageUrlSupport) { result.bgImageUrlSupport = parsedAttributeResult.bgImageUrlSupport.value; }

      return result;
    },

    fallbackStrategy: function() {
      var result = 'algo';
      var options = printfriendlyOptions();
      if(!options) { return result; }

      var fallbackStrategyValue = options.getAttribute('data-fallback-strategy');
      if (!fallbackStrategyValue) { return result; }
      result = fallbackStrategyValue.trim();
      return result;
    }
  };
})();
var OriginalPageFetch = (function() {
  var __fetchOriginalPageCallbacksQueue = [];
  var __fetchOriginalPageResult = null;

  function triggerCallbacks() {
    for (var i = 0; i < __fetchOriginalPageCallbacksQueue.length; i++) {
      var callback = __fetchOriginalPageCallbacksQueue[i];
      callback(__fetchOriginalPageResult);
    }
  }

  return function(pfData, callback) {
    if (__fetchOriginalPageResult) {
      if (callback) { callback(__fetchOriginalPageResult); }
      return;
    }
    if (__fetchOriginalPageCallbacksQueue > 0) {
      if (callback) { __fetchOriginalPageCallbacksQueue.push(callback); }
      return;
    }

    if (callback) { __fetchOriginalPageCallbacksQueue.push(callback); }

    var isEnabled = false;
    if (pfData.userSettings.fetchOriginalPage === 'default') {
      isEnabled = pfData.config.isExtension || pfData.config.isBookmarklet;
    } else {
      isEnabled = pfData.userSettings.fetchOriginalPage === 'yes';
    }

    if (!isEnabled) {
      __fetchOriginalPageResult = {status: 'disabled'};
      triggerCallbacks();
      return;
    }

    var xhr = new XMLHttpRequest();
    xhr.open('GET', pfData.page.location.href);
    xhr.timeout = 5000;
    xhr.onload = function() {
      if (__fetchOriginalPageResult) { return; }

      __fetchOriginalPageResult = {
        status: 'success',
        responseText: xhr.responseText,
        headers: { CSP: xhr.getResponseHeader('Content-Security-Policy') }
      };
      triggerCallbacks();
    };

    xhr.timeout = function() {
      if (__fetchOriginalPageResult) { return; }

      __fetchOriginalPageResult = {status: 'timeout'};
      triggerCallbacks();
    };
    xhr.send();
  };
})();












var PF_VERSION='client';

// FF browser extension doesn't have direct access to original page global variables
(function() {
  // PF Firefox Extension 1.2 uses hidden div element to pass data
  var dataElement = document.getElementById("printfriendly-data");
  if (dataElement) {
    var jsonData = JSON.parse(dataElement.getAttribute('data'));
    window.pfstyle = jsonData.pfstyle;
    window.pfOptions = jsonData.pfOptions;
    window.pfShowHiddenContent = jsonData.pfShowHiddenContent;
  }

  // PF Firefox Extension 1.3 uses wrappedJSObject to pass data
  if (window.wrappedJSObject && window.wrappedJSObject.extensionPath) {
    var originalWindow = window.wrappedJSObject;
    window.extensionId = originalWindow.extensionId;
    window.extensionRootTabId = originalWindow.extensionRootTabId;
    window.extensionPath = originalWindow.extensionPath;
    window.extensionPageSize = originalWindow.extensionPageSize;
    window.extensionFingerprint = originalWindow.extensionFingerprint;
    window.pfstyle = originalWindow.pfstyle;
    window.pfOptions = originalWindow.pfOptions;
    window.pfShowHiddenContent = originalWindow.pfShowHiddenContent;
  }
})();

var pfMod = window.pfMod || (function(window, undef) {
  var doc = window.document;
  var protocol = 'https:';

  messageBus.listen('', {
    PfCoreLoaded: function() {
      messageBus.postMessage('core', 'PfStartCore', {pfData: pf.pfData, dsData: pf.dsData});
    },
    PfExtensionCoreLoaded: function() {
      messageBus.postMessage('core', 'PfLoadCore', {pfData: pf.pfData});
    },
    PfClosePreview: function() {
      pf.closePreview();
    },
    PfAddCSS: function(payload) {
      commonUtils.addCSS(payload.css, doc, payload.useBody);
    },
    PfRestoreStyles: function() {
      docHelper.restoreStyles();
    },
    PfAddViewPortTag: function() {
      docHelper.addViewPortTag();
    },
    PfScrollTop: function() {
      window.scrollTo(0,0);
    },
    PfFinished: function(payload) {
      pf.hasContent = payload.hasContent;
      pf.finished = true;
    },
    PfOriginalPageFetch: function() {
      OriginalPageFetch(pfMod.pfData, function(data) {
        messageBus.postMessage('core', 'PfOriginalPageFetchResult', data);
      });
    },
    PfImageToBase64: function(payload) {
      var xhr = new XMLHttpRequest();
      xhr.onload = function() {
        var reader = new FileReader();
        reader.onloadend = function() {
          messageBus.postMessage('core', 'PfImageToBase64Hook', {id: payload.id, state: 'success', data: reader.result});
        };
        reader.readAsDataURL(xhr.response);
      };
      xhr.onerror = function() {
        messageBus.postMessage('core', 'PfImageToBase64Hook', {id: payload.id, state: 'error', data: payload.url});
      };
      xhr.open('GET', payload.url);
      xhr.responseType = 'blob';
      xhr.send();
    },
    PfRedirectIfNecessary: function(payload) {
      pf.dsData = payload.dsData;
      var redirectCheck = pf.runRedirectChecks();
      switch(redirectCheck.action) {
        case 'redirect':
          pf.redirect();
          break;
        case 'proceed':
          messageBus.postMessage('core',  'PfLaunchCore');
          break;
      }
    }
  },
  function(e) {
    logger.error(e);
    // Since we have got an exception we are setting the finished status to true
    pf.finished = true;
  });


  var defaultConfig = {
    environment: 'production',
    disableUI: false,
    protocol: protocol,
    dir: 'ltr',
    usingBM: false,
    maxImageWidth: 750,
    filePath: '/assets/',
    platform: 'unknown',
    enablePrintOnly: false,
    hosts: {
      cdn: protocol + '//cdn.printfriendly.com',
      pf: 'https://www.printfriendly.com',
      ds: 'https://www.printfriendly.com',
      translations: 'https://www.printfriendly.com',
      ds_cdn: 'https://www.printfriendly.com',
      pdf: 'https://pdf.printfriendly.com',
      email: 'https://www.printfriendly.com',
      page: window.location.host.split(':')[0]
    },
    domains: {
      page: window.location.host.split(':')[0].split('www.').pop()
    }
  };

  var utils = {
    isBookmarklet: function() {
      return (window.pfstyle && window.pfstyle !== 'wp');
    },
    removeEmailsFromUrl: function(url) {
      url = url.split('?')[0];
      var parts = url.split('/');

      //reverse iteration as may be destructive
      for (var i = parts.length; i-- > 0;) {
        var foundIndex = parts[i].indexOf('@');
        // NOTE: we ignore case where @ is first character as it's might be an nickname
        // Ex.: https://medium.com/@marikalam/study-guide-cassandra-data-consistency-496e5bf9cadb
        if (foundIndex > 0) {
          parts.splice(i, 1);
        }
      }

      return parts.join('/');
    },

    ogImageUrl: function() {
      var url = '';
      var ogImageElement = document.querySelector &&
        document.querySelector('meta[property="og:image"]');
      if (ogImageElement && ogImageElement.content) {
        url = ogImageElement.content;
      }
      return url;
    },

    isWix: function() {
      return utils.ogImageUrl().indexOf('wixstatic.com') !== -1;
    },

    isOverBlog: function() {
      return utils.ogImageUrl().indexOf('over-blog-kiwi.com') !== -1;
    },

    isLocalHost: function() {
      var host = window.location.host;
      var hostName = window.location.hostname;
      return host.indexOf(':') !== -1 ||
             !!hostName.match(/\d+\.\d+\.\d+\.\d+/) ||
             hostName === 'localhost' ||
             !!hostName.split('.').pop().match(/invalid|test|example|localhost|dev/);
    }
  };

  var docHelper = {
    addViewPortTag: function() {
      var head = doc.getElementsByTagName('head')[0];
      var meta = doc.querySelector("meta[name=viewport]");

      if (!meta) {
        meta = doc.createElement('meta');
        meta.name = 'viewport';
      }

      meta.content = 'width=device-width, initial-scale=1';
      head.appendChild(meta);
    },

    restoreStyles: function() {
      var elements = document.getElementsByName("pf-style");

      for (var index = elements.length - 1; index >= 0; index--) {
          elements[index].parentNode.removeChild(elements[index]);
      }
    }
  };

  // FIXME: Extract non dom methods to another var - helper
  var dom = {
    isReady: false,
    readyBound: false,

    ready: function() {
      if ( !dom.isReady) {
        if ( !document.body) {
          return setTimeout( dom.ready, 13);
        }
        dom.isReady = true;
        dom.readyFunc.call();
      }
    },

    doScrollCheck: function() {
      if ( dom.isReady ) {
        return;
      }

      try {
        document.documentElement.doScroll("left");
      } catch(e) {
        return setTimeout(dom.doScrollCheck, 50);
      }
      dom.detach();
      dom.ready();
    },

    detach: function() {
      if ( document.addEventListener ) {
          document.removeEventListener( "DOMContentLoaded", dom.completed, false );
          window.removeEventListener( "load", dom.completed, false );
      } else if ( document.attachEvent ) {
        if ( document.readyState === "complete" ) {
          document.detachEvent( "onreadystatechange", dom.completed );
          window.detachEvent( "onload", dom.completed );
        }
      }
      if (this.raceTimeoutId) { clearTimeout(this.raceTimeoutId); }
    },

    completed: function(event) {
      if ( document.addEventListener || event.type === "load" || document.readyState === "complete" ) {
        dom.detach();
        dom.ready();
      }
    },

    bindReady: function() {
      if(dom.readyBound)
        return;

      dom.readyBound = true;

      if ( document.readyState === "complete" ) {
        return dom.ready();
      }
      // NOTE: setup race condition in case we are not on server
      // as the PF rendering triggered by user
      if (!pf.onServer) {
        this.raceTimeoutId = setTimeout(function() {
          dom.detach();
          dom.ready();
        }, 1500);
      }
      if ( document.addEventListener ) {
        document.addEventListener("DOMContentLoaded", dom.completed, false );
        window.addEventListener( "load", dom.completed, false );
      } else if ( document.attachEvent ) {
        document.attachEvent("onreadystatechange", dom.completed);
        window.attachEvent( "onload", dom.completed );
        var toplevel = false;

        try {
          /* jshint -W041 */
          toplevel = window.frameElement == null && document.documentElement;
          /* jshint +W041 */
        } catch(e) {}

        if ( toplevel && toplevel.doScroll ) {
          dom.doScrollCheck();
        }
      }
    },

    domReady: function(fn) {
      this.readyFunc = fn;
      this.bindReady();
    },

    canonicalize: function (url) {
      if(url) {
        var div = document.createElement('div');
        div.innerHTML = "<a></a>";
        div.firstChild.href = url; // Ensures that the href is properly escaped
        div.innerHTML = div.innerHTML; // Run the current innerHTML back through the parser
        url = div.firstChild.href;
        if (url.indexOf("//") !== -1) {
          url = window.location.protocol + '//' + div.firstChild.href.split("//")[1];
        }
      }
      return url;
    }
  };
  var userSettings = {
    headerImageUrl: dom.canonicalize(window.pfHeaderImgUrl),
    headerTagline: window.pfHeaderTagline,
    imageDisplayStyle: window.pfImageDisplayStyle,
    customCSSURL: !window.extensionPath && dom.canonicalize(window.pfCustomCSS),
    disableClickToDel: window.pfdisableClickToDel,
    disablePDF: window.pfDisablePDF,
    disableImages: window.pfDisableImages,
    encodeImages: window.pfEncodeImages === undefined ? window.location.protocol === 'http:' : (parseInt(window.pfEncodeImages) === 1),
    showHiddenContent: (parseInt(window.pfShowHiddenContent) === 1),
    disablePrint: window.pfDisablePrint,
    disableEmail: window.pfDisableEmail
  };

  if('|full-size|remove-images|large|medium|small|'.indexOf('|' + window.pfImagesSize + '|') !== -1) {
    userSettings.imagesSize = window.pfImagesSize;
  } else {
    userSettings.imagesSize = window.pfHideImages == 1 ? 'remove-images' : 'full-size';
  }

  var pf = {
    version: PF_VERSION,
    initialized: false,
    finished: false,
    onServer: false,
    hasContent: false,
    messages: [],
    errors: [],
    waitDsCounter: 0,
    autoStart: false,
    stats: {},

    init: function(options) {
      try {
        this.initialized = true;
        this.configure(options);
        this.onServerSetup();
        this.getDSSettingsFromPFServer()
        this.setVariables();
        this.detectBrowser();
        this.setStats();
        this.startIfNecessary();

        window.print = function() {
          pf.start();
        };
      } catch(e) {
        logger.error(e);
        // Since we have got an exception we are setting the finished status to true
        pf.finished = true;
      }
    },

    configure: function(options) {
      this.config = defaultConfig;
      if (options) {
        this.config.environment = options.environment || 'development';
        for(var val in options.hosts) {
          this.config.hosts[val] = options.hosts[val];
        }
        if(options.filePath) {
          this.config.filePath = options.filePath;
        }
        if(options.ssLocation) {
          this.config.ssLocation = options.ssLocation;
        }
        if(options.ssStyleSheetHrefs) {
          this.config.ssStyleSheetHrefs = options.ssStyleSheetHrefs;
        }
        if(options.ssFaviconUrl) {
          this.config.ssFaviconUrl = options.ssFaviconUrl;
        }
        if (options.enablePrintOnly) {
          this.config.enablePrintOnly = options.enablePrintOnly;
        }
      }
      this.config.enableLog = this.config.environment === 'development' ||
        this.config.environment === 'test' ||
        window.pfEnableLog;
      this.config.isExtension = !!window.extensionPath;
      this.config.isBookmarklet = utils.isBookmarklet();
      this.config.extensionFingerprint = window.extensionFingerprint;
    },

    // Pass an object a string path. Similar to
    // https://github.com/TheNodeILs/lodash-contrib/blob/master/docs/_.object.selectors.js.md#getpath
    // Pass an object and property names separated by dot
    // like country.state.city
    getVal: function(obj, path) {
      var keys = path.split('.');
      while( (typeof obj !== 'undefined') && keys.length) {
        obj = obj[keys.shift()];
      }
      return obj;
    },

    startIfNecessary: function() {
      if (window.pfstyle || this.autoStart) { this.start(); }
    },

    urlHasAutoStartParams: function() {
      return this.config.urls.page.indexOf('pfstyle=wp') !== -1;
    },

    setUserSettings: function() {
      function mergeToUserSettings(object) {
        for (var key in object) { pf.userSettings[key] = object[key]; }
      }

      mergeToUserSettings(printfriendlyOptionsParser.selectors());
      pf.userSettings.fallbackStrategy = printfriendlyOptionsParser.fallbackStrategy();
      mergeToUserSettings(printfriendlyOptionsParser.contentFeatures());

      var printfriendlyCss = document.querySelector('printfriendly-css');
      if (printfriendlyCss) {
        pf.userSettings.customCssStyle = printfriendlyCss.textContent;
      }
    },

    start: function() {
      // Extension must load DS in core because of CSP
      pf.config.extensionPageSize = window.extensionPageSize;
      this.setUserSettings();
      if (pf.onServer) {
        pf.launch();
      } else if(pf.config.isExtension) {
        pf.launch();
      } else {
        // Wait 2 seconds for DS API
        pf.waitDsCounter += 1;
        if (pf.waitDsCounter < 20 && !pf.dsData) {
          return setTimeout(function(){pf.start();}, 100);
        }
        var redirectCheck = pf.runRedirectChecks();
        switch(redirectCheck.action) {
          case 'show_message':
            alert('Current domain is not supported for printfriendly.com');
            break;
          case 'redirect':
            pf.redirect();
            break;
          case 'proceed':
            if (pf.supportedSiteType()) {
              pf.launch();
            }
            break;
        }
      }
    },

    launch: function() {
      dom.domReady(function() {
        try {
          pf.startTime = new Date().getTime();

          htmlPreProcessor.run();
          pf.pfData = pfDataHelper.get();
          logger.init(pf.pfData);
          if (!pf.config.disableUI) {
            pf.sanitizeLocation();
            pf.createMask();
          }
          pf.loadCore();
        } catch(e) {
          logger.error(e);
          // Since we have got an exception we are setting the finished status to true
          pf.finished = true;
        }
      });
    },

    // Remove Querystring and emails from URL to avoid sending PII to google
    sanitizeLocation: function() {
      url = document.location.href.split('?')[0];
      url = utils.removeEmailsFromUrl(url);

      if(url !== document.location.href) {
        if (history && typeof history.pushState === 'function') {
          history.pushState({pf: 'sanitized'}, document.title, url);
        }
      }
    },

    // Restore url to be able to refresh page
    unsanitizeLocation: function() {
      if (history && history.state && history.state.pf == 'sanitized') {
        history.back();
      }
    },

    onServerSetup: function() {
      if (window.onServer) {
        this.onServer = true;
        this.config.disableUI = true;
      }
    },

    setVariables: function() {
      var _t = this;
      var url;
      var cdnVersion = _t.config.hosts.cdn + _t.config.filePath + _t.version;
      var pfAppCSS = this.config.disableUI ? '' : "//cdn.printfriendly.com/assets/pf-app/main-c36253da3343cb23bf7a97cd270432cd04936a6a275a18a7e1a6963ff9c5080b.css";
      var contentCSS = this.config.disableUI ? '' : "//cdn.printfriendly.com/assets/content/main-3cfe82c205ab841b23bdee21da68b74f56d6d802a559448e5723798431f88cd9.css";
      var js = {
        jquery: "//cdn.printfriendly.com/assets/unversioned/jquery/3.6.0.min-62efb0f451c1202e83668dd0942d2b0839e18b4a76c73809174dec2cad131a10.js",
        core: "//cdn.printfriendly.com/assets/client/core-130f51c6e2ee2faf2c639859e017f62223079f3998a3c58da0cd6133f7984aa2.js",
        algo: "//cdn.printfriendly.com/assets/client/algo-6a828bbc1ba6d90953b7e58df646c8a75b71401bd2e36690814733a4ef226980.js"
      };

      this.config.urls = {
        version: cdnVersion,
        js: js,
        css: {
          pfApp: pfAppCSS,
          content: contentCSS
        },
        pdfMake: _t.config.hosts.pdf + '/pdfs/make',
        email: _t.config.hosts.email + '/email/new'
      };
      try {url = top.location.href;} catch(e) {url = window.location.href;}

      this.config.urls.page = url;
      this.userSettings = userSettings;
      this.config.pfstyle = window.pfstyle;

      if(window.pfstyle && (window.pfstyle === "bk" || window.pfstyle === "nbk" || window.pfstyle === "cbk")) {
        this.config.usingBM = true;
      }

      this.autoStart = this.urlHasAutoStartParams();
    },

    detectBrowser: function() {
      this.browser = {};
      if (navigator.userAgentData) {
        this.browser.isIE = false;
      } else if (navigator.appVersion) {
        var versionString = navigator.appVersion;
        if (versionString && versionString.indexOf('MSIE') !== -1) {
          this.browser.version = parseFloat(versionString.split('MSIE')[1]);
          this.browser.isIE = true;
        } else {
          this.browser.isIE = false;
        }
      }
    },

    redirect: function() {
      var href = typeof pfData !== 'undefined' ? pfData.page.location.href : top.window.location.href;
      var url = pfRedirect(this.config.hosts.pf, userSettings, href)
      // If PF was started automatically by URL params, location.replace ensures that the page
      // won't be in browser history thus avoiding a redirect loop if the the back button is
      // used.
      if (this.autoStart) {
        top.location.replace(url);
      } else {
        top.location.href = url;
      }
    },

    supportedSiteType: function() {
      if(pf.config.urls.page === 'about:blank' ||
         (pf.config.protocol !== 'http:' && pf.config.protocol !== 'https:')) {
        return false;
      } else {
        return true;
      }
    },

    setStats: function() {
      pf.stats.page = {
        bm: utils.isBookmarklet(),
        local: utils.isLocalHost(),
        unSupported: utils.isWix() || utils.isOverBlog()
      };
    },

    domainsListInclude: function(domain, domainsList) {
      if (!domainsList.length) { return false; }

      var domainsListRegexp = new RegExp(domainsList.join('|').replace(/\./g, "\\."));
      return domain.match(domainsListRegexp);
    },

    skipRedirectReasons: [
      {
        name: 'noApiResponse',
        check: function() { return !pf.dsData; }
      }, {
        name: 'adFree',
        check: function() {
          return pf.dsData.domain_settings.ad_free;
        }
      }, {
        name: 'isLocalHost',
        check: function() {
          return utils.isLocalHost();
        },
      }, {
        name: 'unSupportedBySS',
        check: function() {
          return utils.isWix() || utils.isOverBlog();
        },
      }, {
        name: 'BMExt',
        check: function() {
          return utils.isBookmarklet();
        }
      }
    ],

    forceRedirectReasons: [
      {
        name: 'unSupportedBrowser',
        check: function() {
          try {
            var edge = !navigator.userAgentData && navigator.userAgent.match(/Edge\/(\d+.\d+)/);
            var isLegacyEdge = edge && edge[1] && parseFloat(edge[1]) < 79;
            var supportedLegacyDomainsRegexp = /^((.+\.)?jhana-dev\.com|(.+\.)?jhana-stage\.com|(.+\.)?jhana\.com|guide\.matrix\.ip\.com|guide\.ip\.com|componentagro\.test\.huss\.nl|componentagro\.nl|hansa-online\.de|binnenschifffahrt-online\.de|mikrooek-apotheke\.de)$/;
            if (isLegacyEdge && !supportedLegacyDomainsRegexp.test(pf.config.domains.page)) { return true; }
            if(!utils.isBookmarklet() &&
               (!(history && typeof history.pushState === 'function') ||
                (!navigator.userAgentData && navigator.userAgent.match(/(ipod|opera.mini|blackberry|playbook|bb10)/i)) ||
                pf.browser.isIE)
            ) {
              return true;
            } else {
              return false;
            }
          } catch(e) {
            logger.error(e);
            return false;
          }
        }
      }
    ],

    unsupportedReasons: [
      {
        name: 'blacklist',
        check: function() {
          return pf.domainsListInclude(pf.config.domains.page, [
            // 'unsupported-domain.org'
          ]);
        }
      }
    ],

    runChecksFor: function(checks) {
      for(var i = 0, length = checks.length; i < length; i++) {
        var reason = checks[i];
        if (reason.check()) { return reason; }
      }
    },

    __redirectChecksResult: null,
    runRedirectChecks: function() {
      if (this.__redirectChecksResult) { return this.__redirectChecksResult; }

      var result, forceRedirectReason, skipRedirectReason, unsupportedReason;

      if (!(skipRedirectReason = this.runChecksFor(this.skipRedirectReasons))) {
        result = { action: 'redirect' };
      } else if (unsupportedReason = this.runChecksFor(this.unsupportedReasons)) {
        result = { reason: unsupportedReason.name, action: 'show_message' }
      } else if (forceRedirectReason = this.runChecksFor(this.forceRedirectReasons)) {
        result = { reason: forceRedirectReason.name, action: 'redirect' };
      } else {
        result = { reason: skipRedirectReason.name, action: 'proceed' }
      }

      this.__redirectChecksResult = result;
      return this.__redirectChecksResult;
    },

    createMask: function() {
      var div = document.createElement('div');
      div.innerHTML = '<div id="pf-mask" style="z-index: 2147483627!important; position: fixed !important; top: 0pt !important; left: 0pt !important; background-color: rgb(0, 0, 0) !important; opacity: 0.8 !important;filter:progid:DXImageTransform.Microsoft.Alpha(opacity=80); height: 100% !important; width: 100% !important;"></div>';
      document.body.appendChild(div.firstChild);
    },

    closePreview: function() {
      dom.readyBound = false;
      dom.isReady = false;

      pf.unsanitizeLocation();

      var pfCoreElement = document.getElementById('pf-core');
      if (pfCoreElement && pfCoreElement.parentElement) {
        pfCoreElement.parentElement.removeChild(pfCoreElement);
      }

      var maskElement = document.getElementById('pf-mask');
      if (maskElement && maskElement.parentElement) {
        maskElement.parentElement.removeChild(maskElement);
      }

      var gaiframe = document.getElementById('gaiframe');
      if (gaiframe && gaiframe.parentElement) {
        gaiframe.parentElement.removeChild(gaiframe);
      }
    },

    removeDoubleSemiColon: function(str) {
      return str.replace(/;{2}/g, ';');
    },

    loadCore: function() {
      window.coreIframe = commonUtils.createIframe(document);
      coreIframe.id = 'pf-core';
      coreIframe.name = 'pf-core';

      document.body.appendChild(coreIframe);

      var style = coreIframe.style.cssText + ';' + 'width: 100% !important;max-width:100vw !important;height: 100% !important; max-height:100vh !important; display: block !important; overflow: hidden !important; position: absolute !important; top: 0px !important; left: 0px !important; background-color: transparent !important; z-index: 2147483647!important';
      coreIframe.style.cssText = this.removeDoubleSemiColon(style);

      if (this.config.isExtension) {
        // extensionPath is declared if script running from browser extension
        coreIframe.src = extensionPath + '/pages/core.html';
        coreIframe.onload = function() {
          messageBus.postMessage('core', 'PfInitCoreExtension', {extensionRootTabId: window.extensionRootTabId});
        };
      } else {
        coreIframe.src = "//cdn.printfriendly.com/assets/client/core-ca5dccad8043d5ce9cbb17ab57b9e4000c89735eb1ea68c616b48aefb6fd89c5.html"
      }
    },

    getDSSettingsFromPFServer: function() {
      if (pf.onServer || this.config.isExtension) { return; }

      var script = document.createElement('script');

      script.src = pf.config.hosts.ds_cdn + '/api/v3/domain_settings/a' +
        '?callback=pfMod.saveDSSettings' +
        '&hostname=' + pf.config.hosts.page +
        '&client_version=' + pf.version;

      document.getElementsByTagName('head')[0].appendChild(script);
    },

    saveDSSettings: function(data) {
      pf.dsData = data;
      if (window.coreIframe && coreIframe.contentWindow) {
        messageBus.postMessage('core', 'PfConfigureDSSettings', {dsData: data});
      }
    }
  };

  var pfDataHelper = {
    emailText: function() {
      var elements = document.getElementsByClassName('pf-email');
      return elements.length ? elements[0].textContent : '';
    },

    csStyleSheetHrefs: function() {
      var hrefs = [];

      for(var i = 0; i < doc.styleSheets.length; i++) {
        hrefs.push(doc.styleSheets[i].href);
      }

      return hrefs;
    },

    metas: function () {
      var metaTags = doc.getElementsByTagName('meta');
      var metas = [];

      for(var i = 0; i < metaTags.length; i++) {
        metas.push({
          name: metaTags[i].getAttribute('name'),
          content: metaTags[i].getAttribute('content'),
          property: metaTags[i].getAttribute('property'),
          itemprop: metaTags[i].getAttribute('itemprop')
        });
      }

      return metas;
    },

    screen: function() {
      var w = window.top;
      try {
        w.document;
      } catch(e) {
        w = window;
      }
      return {
        x: typeof w.screenX != 'undefined' ? w.screenX : w.screenLeft,
        y: typeof w.screenY != 'undefined' ? w.screenY : w.screenTop,
        width: typeof w.outerWidth!='undefined' ? w.outerWidth : w.document.documentElement.clientWidth,
        height: typeof w.outerHeight != 'undefined' ? w.outerHeight: (w.document.documentElement.clientHeight - 22)
      };
    },

    language: function() {
      var lang = document.getElementsByTagName('html')[0].getAttribute('lang');

      if (!lang) {
        var metaLang = document.querySelector('meta[http-equiv=Content-Language]');
        if (metaLang) {
          lang = metaLang.getAttribute('content');
        }
      }

      return lang;
    },

    canvasDataUrls: function() {
      var dataUrls = [];

      var canvases = doc.getElementsByTagName('canvas');
      for (var i = 0; i < canvases.length; i++) {
        try {
          var canvas = canvases[i];
          var dataUrl = canvas.toDataURL('image/png');
          canvas.setAttribute('pf-dataurl-index', dataUrls.length);
          dataUrls.push(dataUrl);
        } catch(e) {} // Ignore canvas tainted error
      }

      return dataUrls;
    },

    favicon: function() {
      if (pf.config.ssFaviconUrl) { return pf.config.ssFaviconUrl; }

      var faviconRels = ['shortcut icon', 'icon', 'apple-touch-icon', 'apple-touch-icon-precomposed'];
      var faviconElement = null;
      for (var i = 0; i < faviconRels.length; i++) {
        var rel = faviconRels[i];
        var result = document.querySelector('link[rel="' + rel +'"]');
        if (result) {
          faviconElement = result;
          break;
        }
      }

      if (!faviconElement || !faviconElement.href) { return "https://cdn.printfriendly.com/icons/globe.svg"; }

      return faviconElement.href;
    },

    enablePrintOnly: function(doc) {
      return !!doc.querySelector('.at-svc-printfriendly, a[href*="printfriendly\.com"], script[src*="\/\/cdn\.printfriendly\.com"], script[src*="\/\/pf-cdn\.printfriendly\.com"], img[src*="\/\/cdn\.printfriendly\.com"]') ||
        pf.config.enablePrintOnly;
    },

    getApplicationLd: function(doc) {
      var applicationLdNode = doc.querySelector('script[type="application/ld+json"]')
      if (applicationLdNode) {
        var applicationLdJSON = applicationLdNode.textContent.replace(/^\s*\/*\s<!\[CDATA\[|\]\]>\s*$/g, "").replace(/[/\s]*$/, '');
        try {
          return JSON.parse(applicationLdJSON);
        } catch (e) {
          logger.error(e);
        }
      }
    },

    replaceShadowRootElements: function(body) {
      var duplicate = body.cloneNode(true);
      duplicate.innerHTML = body.innerHTML;

      body.querySelectorAll('.pf-shadow-root').forEach(function(shadowRoot) {
        var shadowRootContent = shadowRoot.shadowRoot.innerHTML;
        if(!shadowRootContent) return;
        var replace = duplicate.querySelector('[data-pf-shadow-root="' + shadowRoot.dataset.pfShadowRoot + '"]')
        if (!replace) { return; }
        var shadowRootContentElement = document.createElement('div');
        shadowRootContentElement.innerHTML = shadowRootContent;
        replace.parentNode.replaceChild(shadowRootContentElement, replace);
      });

      return duplicate;
    },
    get: function() {
      pf.config.extensionId = window.extensionId;
      pf.config.extensionRootTabId = window.extensionRootTabId;
      pf.config.extensionPath = window.extensionPath;

      var canvasDataUrls = this.canvasDataUrls();
      var location = document.location;
      page = {
        dir: doc.body.getAttribute('dir') || doc.querySelector('html').getAttribute('dir') || getComputedStyle(doc.body).getPropertyValue('direction') || 'ltr',
        bodyClassList: [].slice.call(doc.body.classList || doc.body.className.split(' ')), // Convert Array like object to Array
        emailText: this.emailText(),
        screen: this.screen(),
        metas: this.metas(),
        csStyleSheetHrefs: this.csStyleSheetHrefs(),
        location: {
          href: location.href,
          host: location.host,
          pathname: location.pathname,
          protocol: location.protocol
        },
        enablePrintOnly: this.enablePrintOnly(doc),
        hasPrintOnly: !!doc.querySelector('#print-only, .print-only'),
        title: document.title,
        // NOTE: in case we populate algo iframe with HTML containing <embed> tag in some cases it become broken for printing
        // Ref.: https://github.com/printfriendly/printfriendly/issues/2099
        body: this.replaceShadowRootElements(document.body).innerHTML.replace(/<\s*?embed[^>]*?>(.*?<\s*?\/\s*?embed\s*?>)?/g, ''),
        language: this.language(),
        canvasDataUrls: canvasDataUrls,
        favicon: this.favicon(),
        applicationLd: this.getApplicationLd(doc)
      };

      return {
        startTime: pf.startTime,
        config: pf.config,
        userSettings: pf.userSettings,
        version: pf.version,
        onServer: pf.onServer,
        browser: pf.browser,
        dsData: pf.dsData,
        stats: pf.stats,
        page: page
      };
    }
  };

  var htmlPreProcessor = {
    LARGE_IMAGE_WIDTH: 300,
    LARGE_IMAGE_HEIGHT: 200,

    run: function() {
      this.processChildren(document.body);
    },

    /* Mark hidden elements
     * Set Full URLs for images and links
     * Set width and height for images to keep size with removed stylesheets
     * Not splitting it into separate functions to avoid the
     * function call overhead as allElements can be very huge
     */
    processChildren: function(sourceElement) {
      var nodeName;
      var queue = [];
      // NOTE: phantomjs children property returns `undefined` for some elements(ex. SVGElements)
      // so we have to verify it first
      if (sourceElement.children && sourceElement.children.length) {
        for(var i = 0, length = sourceElement.children.length; i < length; i++) { queue.push(sourceElement.children[i]); }
      }

      var sourceChild = null;
      while (sourceChild = queue.shift()) {
        if (!commonUtils.hasClass(sourceChild, 'comment-list')) {
          // Process current element
          if (sourceChild.nodeType === Node.ELEMENT_NODE) {
            try {
              nodeName = sourceChild.nodeName.toLowerCase();

              persistComputedStylesAndRect(sourceChild);
              if(sourceChild.shadowRoot) {
                commonUtils.addClassTo(sourceChild, 'pf-shadow-root');
                sourceChild.dataset.pfShadowRoot = UUID();
              }
              if (!userSettings.showHiddenContent && (sourceChild.getAttribute('data-pf_style_display') === 'none' || sourceChild.getAttribute('data-pf_style_visibility') === 'hidden')) {
                commonUtils.addClassTo(sourceChild, "hidden-originally");
              } else if (commonUtils.hasClass(sourceChild, 'hidden-originally')) {
                commonUtils.removeClassFrom(sourceChild, 'hidden-originally');
              }

              if (nodeName === 'a') {
                // A: Convert relative to absolute URL
                var href = sourceChild.getAttribute('href');
                if(href && !href.startsWith('#') && !href.startsWith('http') && !href.startsWith('javascript') && !href.startsWith('mailto')) {
                  // sourceChild.href gives the full URL. So we use it here instead of
                  // the result of getAttribute which return the original href
                  sourceChild.setAttribute('href', toAbsoluteUrl(href, window.location));
                }
              } else if ((nodeName === 'input' || nodeName === 'textarea') && !pfMod.onServer) {
                if (sourceChild.type === 'radio' || sourceChild.type === 'checkbox') {
                  if (sourceChild.checked) {
                    sourceChild.setAttribute("checked", "checked");
                  }
                } else {
                  sourceChild.setAttribute('value', sourceChild.value);
                }
              } else if (!pfMod.onServer && nodeName === 'select' && sourceChild.options.length && sourceChild.selectedIndex >= 0) {
                sourceChild.options[sourceChild.selectedIndex].setAttribute("selected", "selected");
              } else if (nodeName === 'img' || nodeName === 'svg') {
                // Convert relative to absolute URL
                if (sourceChild.getAttribute('src')) { sourceChild.src = sourceChild.src; }
                var srcset = sourceChild.getAttribute('srcset') || sourceChild.getAttribute('data-srcset');
                if (srcset) {
                  var srcs = srcset.split(/,\s/);
                  var newSrcs = [];
                  for (var j = 0; j < srcs.length; j++) {
                    var src = srcs[j];
                    newSrcs.push(toAbsoluteUrl(src, window.location));
                  }

                  sourceChild.setAttribute('pf-data-srcset', newSrcs.join(', '));
                }
                if (nodeName === 'img' && !commonUtils.hasClass(sourceChild, 'hidden-originally')) {
                  var imgHeight = commonUtils.getImageHeight(sourceChild, pfMod.onServer);
                  var imgWidth =  commonUtils.getImageWidth(sourceChild, pfMod.onServer);

                  if ((imgWidth * imgHeight) > (this.LARGE_IMAGE_WIDTH * this.LARGE_IMAGE_HEIGHT)) {
                    commonUtils.addClassTo(sourceChild, 'pf-large-image');
                  }
                }
              } else if (pf.userSettings.bgImageUrlSupport === 'on') {
                var bgSrc = window.getComputedStyle(sourceChild).backgroundImage
                if(bgSrc !== 'none') {
                  bgSrc = bgSrc.replace(/^url\("(.+)"\)/, '$1')

                  sourceChild.setAttribute('data-pf-style-background-image', bgSrc);
                  if (!commonUtils.hasClass(sourceChild, 'hidden-originally')) {
                    var imgHeight = commonUtils.getImageHeight(sourceChild, pfMod.onServer);
                    var imgWidth =  commonUtils.getImageWidth(sourceChild, pfMod.onServer);

                    if ((imgWidth * imgHeight) > (this.LARGE_IMAGE_WIDTH * this.LARGE_IMAGE_HEIGHT)) {
                      commonUtils.addClassTo(sourceChild, 'pf-large-image');
                    }
                  }
                }
              }

            // For some edgecases getComputedStyle returns null
            // Sometimes nodeName is undefined (should never happen ideally but it does happen)
            } catch(e) {}
          }

          // NOTE: phantomjs children property returns `undefined` for some elements(ex. SVGElements)
          // so we have to verify it first
          if (sourceChild.children && sourceChild.children.length) {
            for(var i = 0, length = sourceChild.children.length; i < length; i++) { queue.push(sourceChild.children[i]); }
          }
        }
      }
    }
  };

  return pf;
})(window);
window.pfMod = pfMod;
var priFri = pfMod;

// Required for browser extensions second run
if (pfMod.initialized && (document.getElementById('printfriendly-data') || window.extensionPath)) {
  pfMod.start();
} else if (window.name !== 'algo' && window.name !== 'pf-core' && !pfMod.initialized) {
  pfMod.init(window.pfOptions);
};
