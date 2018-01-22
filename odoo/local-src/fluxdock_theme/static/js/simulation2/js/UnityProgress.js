function UnityProgress(domElement)
{
	this.progress = 0.0;
	this.downloadProgress;
	this.domElement = domElement;

	var parent = domElement.parentNode;

	this.downloadProgress = document.querySelector(
		'#unityLoaderContainer .downloadProgress');
	this.loaderProgress = document.querySelector(
		'#unityLoaderContainer .loaderProgress');

	this.SetProgress = function(progress) {
		if (this.progress < progress)
			this.progress = progress;

		this.Update();
	}

	this.SetMessage = function(message) {
		this.Update();
	}

	this.Clear = function() {
		showQuerySelector('#unityLoaderContainer .loaderMessages', false);
		showQuerySelector('#unityLoaderContainer .startButton', true, 'block');
	}

	this.Update = function() {
		if (this.progress < 1) {
			this.downloadProgress.textContent
				= Math.round(this.progress * 100) + '%';
		} else if (this.progress < 2) {
			showQuerySelector('#unityLoaderContainer .downloadMessages', false);
			showQuerySelector('#unityLoaderContainer .loaderMessages', true);
			this.progress = 2;
		} else
			this.loaderProgress.textContent += '.';
	}

	this.Update();
}
