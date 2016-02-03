new function(SimulationNamespace) {

function resize()
{
	var ratio = /*window.devicePixelRatio ||*/ 1;
	var canvas = document.querySelector('canvas.emscripten');
	canvas.style.width = window.innerWidth + 'px';
	canvas.style.height = window.innerHeight + 'px';
	canvas.width = window.innerWidth * ratio;
	canvas.height = window.innerHeight * ratio;
}


function show(element, show, type)
{
	if (typeof element === 'string')
		element = document.querySelector(element);

	element.style.display = show ? type ? type : 'initial' : 'none';
}


function startApplication()
{
	show('#wrapwrap', false);

	var canvas = document.querySelector('canvas.emscripten');
	show(canvas, true, 'block');

	resize();
	window.onresize = resize;
	fullScreenApi.requestFullScreen(canvas);

	window.onhashchange = stopApplication;
	history.pushState({}, null, '#');
}


function stopApplication()
{
	fullScreenApi.cancelFullScreen();
	window.onresize = undefined;
	show('canvas.emscripten', false);
	show('#wrapwrap', true, 'block');
}


function checkFullScreenState()
{
	if (!fullScreenApi.isFullScreen())
		stopApplication();
}


function loadScript(url)
{
	var script = document.createElement('script');
	script.src = url;
	document.body.appendChild(script);
}


function initUI()
{
	var canvas = document.createElement('canvas');
	canvas.id = 'canvas';
	canvas.className = 'emscripten';
	canvas.width = 960;
	canvas.height = 600;
	canvas.style.display = 'none';
	canvas.oncontextmenu = function(event) { event.preventDefault(); };

	document.body.appendChild(canvas);

	canvas.addEventListener(fullScreenApi.fullScreenEventName,
		checkFullScreenState, true);
	document.addEventListener(fullScreenApi.fullScreenEventName,
		checkFullScreenState, true);

	loadScript('Release/UnityLoader.js');
}


window.Module = {
	TOTAL_MEMORY: 100663296,
	errorhandler: function() { return false; },
	compatibilitycheck: function() { return false; },
	dataUrl: "Release/WebGL.data",
	codeUrl: "Release/WebGL.js",
	memUrl: "Release/WebGL.mem",
};

window.showQuerySelector = show;
window.startApplication = startApplication;

loadScript('js/UnityProgress.js');
loadScript('js/fullscreenapi.js');

window.onload = initUI;

}; // SimulationNamespace
