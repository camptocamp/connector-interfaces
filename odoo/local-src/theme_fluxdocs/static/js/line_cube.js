var gScene;
var gObject;
var gLineContainer;
var gCamera;
var gRenderer;
var gControls;
var gLines;
var gSymbolLines;
var gRandomLines;
var gTargetRotation;
var gCurrentSymbolKeyIndex = 0;
var gRotationAxis;
var gRotationMatrix;
var gProjection;


const kViewWidth = 400;
const kViewHeight = 400;
const kZoom = 100;

const kRotationSteps = 240;
const kLineBuildSteps = kRotationSteps / 4 * 3;
const kSymbolLineWidth = 4;
const kRandomLineWidth = 2;
const kRandomLineCount = 4;
const kMinLineLength = 5;
const kMaxLineLength = 8;
const kCubeSize = 4;

const kAllOnesVector = new THREE.Vector3(1, 1, 1);
const kCubeBounds = {
	min: {
		x: 0,
		y: 0,
		z: 0
	},
	max: {
		x: kCubeSize,
		y: kCubeSize,
		z: kCubeSize
	}
};

const kCubeTranslation = new THREE.Vector3(-kCubeSize / 2, -kCubeSize / 2,
	-kCubeSize / 2);

const kDirections = [
	new THREE.Vector3(1, 0, 0),
	new THREE.Vector3(0, 1, 0),
	new THREE.Vector3(0, 0, 1),
	new THREE.Vector3(-1, 0, 0),
	new THREE.Vector3(0, -1, 0),
	new THREE.Vector3(0, 0, -1),
	new THREE.Vector3(1, 1, 0),
	new THREE.Vector3(0, 1, 1),
	new THREE.Vector3(1, 0, 1),
	new THREE.Vector3(-1, 1, 0),
	new THREE.Vector3(0, -1, 1),
	new THREE.Vector3(1, 0, -1),
	new THREE.Vector3(1, -1, 0),
	new THREE.Vector3(0, 1, -1),
	new THREE.Vector3(-1, 0, 1),
	new THREE.Vector3(-1, -1, 0),
	new THREE.Vector3(0, -1, -1),
	new THREE.Vector3(-1, 0, -1)
];

const kSymbols = {
	'c': new Symbol([
		[
			[ 1, 0, 0 ], [ 2, 0, 1 ], [ 2, 0, 2 ], [ 1, 0, 2 ], [ 0, 0, 2 ],
			[ 0, 1, 2 ], [ 0, 2, 2 ], [ 0, 2, 1 ], [ 0, 2, 0 ], [ 1, 2, 0 ],
			[ 1, 1, 0 ], [ 0, 1, 0 ], [ 0, 1, 1 ], [ 0, 0, 1 ], [ 1, 0, 1 ],
			[ 1, 0, 0 ]
		]
	]),
	'd': new Symbol([
		[
			[ 2, 0, 2 ], [ 1, 0, 2 ], [ 0, 0, 1 ], [ 0, 1, 1 ], [ 0, 2, 1 ],
			[ 0, 2, 0 ], [ 1, 2, 0 ], [ 2, 2, 0 ], [ 2, 1, 0 ], [ 2, 0, 0 ],
			[ 2, 0, 1 ], [ 2, 0, 2 ]
		],
		[
			[ 1, 0, 1 ], [ 0, 0, 0 ], [ 0, 1, 0 ], [ 1, 1, 0 ], [ 1, 0, 0 ],
			[ 1, 0, 1 ]
		]
	]),
	'f': new Symbol([
		[
			[ 3, 0, 2 ], [ 2, 0, 2 ], [ 1, 0, 2 ], [ 0, 0, 1 ], [ 0, 1, 1 ],
			[ 0, 2, 1 ], [ 0, 3, 1 ], [ 0, 2, 0 ], [ 0, 1, 0 ], [ 1, 1, 0 ],
			[ 1, 0, 0 ], [ 0, 0, 0 ], [ 1, 0, 1 ], [ 2, 0, 1 ], [ 3, 0, 2 ]
		]
	]),
	'k': new Symbol([
		[
			[ 3, 0, 3 ], [ 2, 0, 3 ], [ 1, 0, 2 ], [ 0, 0, 1 ], [ 0, 1, 1 ],
			[ 0, 2, 1 ], [ 0, 2, 0 ], [ 0, 1, 0 ], [ 1, 2, 0 ], [ 2, 3, 0 ],
			[ 2, 2, 0 ], [ 1, 1, 0 ], [ 0, 0, 0 ], [ 1, 0, 0 ], [ 2, 0, 0 ],
			[ 3, 0, 1 ], [ 2, 0, 1 ], [ 1, 0, 1 ], [ 2, 0, 2 ], [ 3, 0, 3 ]
		]
	]),
	'l': new Symbol([
		[
			[ 2, 0, 2 ], [ 2, 0, 3 ], [ 1, 0, 2 ], [ 0, 0, 1 ], [ 0, 1, 1 ],
			[ 0, 2, 1 ], [ 0, 2, 0 ], [ 1, 3, 0 ], [ 1, 2, 0 ], [ 0, 1, 0 ],
			[ 0, 0, 0 ], [ 1, 0, 1 ], [ 2, 0, 2 ]
		]
	]),
	'o': new Symbol([
		[
			[ 0, 0, 1 ], [ 1, 0, 1 ], [ 1, 0, 0 ], [ 1, 1, 0 ], [ 0, 1, 0 ],
			[ 0, 1, 1 ], [ 0, 0, 1 ]
		],
		[
			[ 0, 0, 2 ], [ 1, 0, 2 ], [ 2, 0, 2 ], [ 2, 0, 1 ], [ 2, 0, 0 ],
			[ 2, 1, 0 ], [ 2, 2, 0 ], [ 1, 2, 0 ], [ 0, 2, 0 ], [ 0, 2, 1 ],
			[ 0, 2, 2 ], [ 0, 1, 2 ], [ 0, 0, 2 ]
		]
	]),
	'u': new Symbol([
		[
			[ 1, 0, 2 ], [ 0, 0, 2 ], [ 0, 1, 2 ], [ 0, 2, 2 ], [ 0, 2, 1 ],
			[ 0, 2, 0 ], [ 1, 2, 0 ], [ 2, 2, 0 ], [ 2, 1, 0 ], [ 2, 0, 0 ],
			[ 2, 0, 1 ], [ 1, 0, 0 ], [ 1, 1, 0 ], [ 0, 1, 0 ], [ 0, 1, 1 ],
			[ 0, 0, 1 ], [ 1, 0, 2 ]
		]
	]),
	'x': new Symbol([
		[
			[ 0, 0, 0 ], [ 1, 0, 1 ], [ 2, 0, 2 ], [ 2, 0, 1 ], [ 1, 0, 0 ],
			[ 2, 0, 0 ], [ 3, 1, 0 ], [ 2, 1, 0 ], [ 1, 1, 0 ], [ 1, 2, 0 ],
			[ 1, 3, 0 ], [ 0, 2, 0 ], [ 0, 1, 0 ], [ 0, 2, 1 ], [ 0, 2, 2 ],
			[ 0, 1, 1 ], [ 0, 0, 0 ]
		]
	])
};
const kSymbolKeys = [ 'f', 'l', 'u', 'x', 'd', 'o', 'c', 'k' ];


function randomInteger(max, min)
{
	if (min == undefined)
		min = 0;

	return Math.floor(Math.random() * (max - min + 1)) + min;
}


function randomVector(bounds)
{
	return new THREE.Vector3(randomInteger(bounds.max.x, bounds.min.x),
		randomInteger(bounds.max.y, bounds.min.y),
		randomInteger(bounds.max.z, bounds.min.z));
}


function randomDirection(previousDirection)
{
	var negatedPreviousDirection;
	if (previousDirection) {
		negatedPreviousDirection = previousDirection.clone();
		negatedPreviousDirection.negate();
	}

	while (true) {
		var direction = kDirections[randomInteger(kDirections.length - 1)];
		if (previousDirection && direction.equals(negatedPreviousDirection))
			continue;

		return direction.clone();
	}
}


function withinBounds(vector, bounds)
{
	return vector.x >= bounds.min.x && vector.y >= bounds.min.y
		&& vector.z >= bounds.min.z && vector.x <= bounds.max.x
		&& vector.y <= bounds.max.y && vector.z <= bounds.max.z;
}


function boundingBox(vector, size, bounds)
{
	return {
		min: {
			x: Math.max(vector.x - size.x, bounds.min.x),
			y: Math.max(vector.y - size.y, bounds.min.y),
			z: Math.max(vector.z - size.z, bounds.min.z)
		},
		max: {
			x: Math.min(vector.x + size.x, bounds.max.x),
			y: Math.min(vector.y + size.y, bounds.max.y),
			z: Math.min(vector.z + size.z, bounds.max.z)
		}
	};
}


function progression(previousVector, direction, bounds)
{
	result = previousVector.clone();
	result.add(direction);

	if (!withinBounds(result, bounds))
		return false;

	return result;
}


function Symbol(shapes)
{
	this.shapes = [];

	if (shapes) {
		shapes.forEach(function(shape) {
				var vertices = [];
				shape.forEach(function(vertex) {
						vertices.push(new THREE.Vector3(vertex[0], vertex[1],
							vertex[2]));
					});

				this.shapes.push(vertices);
			}.bind(this));
	}
}


Symbol.prototype.clone = function()
{
	var result = new Symbol();
	this.shapes.forEach(function(shape) {
			var vertices = [];
			shape.forEach(function(vertex) {
					vertices.push(vertex.clone());
				});
			result.shapes.push(vertices);
		});

	return result;
}


Symbol.prototype.rotateByMatrix = function(rotationMatrix)
{
	this.shapes.forEach(function(shape) {
			shape.forEach(function(vertex) {
					vertex.add(kCubeTranslation)
						.applyMatrix4(rotationMatrix)
						.sub(kCubeTranslation)
						.round();
				});
		});

	return this;
}


function Projection(rotationAxis, viewVector, rotation)
{
	this.rotationAxis = rotationAxis;
	this.viewVector = viewVector;
	this.negatedViewVector = viewVector.clone().negate();
	this.rotation = rotation;
}


Projection.prototype.findEquivalentPoints = function(base, vector, into,
	bounds)
{
	var next = base;
	while (next = progression(next, vector, bounds))
		into.push(next);
}


Projection.prototype.equivalentPointsFor = function(projectedPoint, bounds)
{
	if (bounds == undefined)
		bounds = kCubeBounds;

	var points = [];
	if (withinBounds(projectedPoint, bounds))
		points.push(projectedPoint.clone());

	this.findEquivalentPoints(projectedPoint, this.viewVector, points, bounds);
	this.findEquivalentPoints(projectedPoint, this.negatedViewVector, points,
		bounds);

	return points;
}


Projection.prototype.randomVectorForProjectedPoint = function(projectedPoint,
	bounds)
{
	var candidates = this.equivalentPointsFor(projectedPoint, bounds);
	return candidates[randomInteger(candidates.length - 1)];
}


Projection.prototype.randomProgression = function(originalFrom, randomizedFrom,
	originalTo)
{
	var equivalentTo = originalTo.clone();
	equivalentTo.sub(originalFrom);
	equivalentTo.add(randomizedFrom);
	return this.randomVectorForProjectedPoint(equivalentTo,
		boundingBox(randomizedFrom, kAllOnesVector, kCubeBounds));
}


Projection.prototype.randomProjectedSegment = function(from, to)
{
	var randomizedFrom = this.randomVectorForProjectedPoint(from);
	return [ randomizedFrom, this.randomProgression(from, randomizedFrom, to) ];
}


function Line(initialVectors, minLineLength, maxLineLength, lineWidth, steps)
{
	this.minLineLength = minLineLength;
	this.maxLineLength = maxLineLength;

	this.geometry = new THREE.Geometry();
	this.geometry.dynamic = true;

	this.material = new THREE.LineBasicMaterial({
			color: 0,//randomInteger(0x888888),
			linewidth: lineWidth,
			linejoin: 'round',
			linecap: 'round'
		});
	this.object = new THREE.Line(this.geometry, this.material);

	this.buildSegments(initialVectors);

	this.vectors.forEach(function(vector) {
			this.geometry.vertices.push(this.vectors[0].clone());
		}.bind(this));

	this.state = this.STATE_BUILDUP;
	this.completeSegments = 0;
	this.tornSegments = 0;
	this.steps = steps;

	this.stepsPerCycle = Math.floor(steps / this.segments.length);
	this.cycleSteps = this.stepsPerCycle;
}


Line.prototype.STATE_BUILDUP = 0;
Line.prototype.STATE_STATIC = 1;
Line.prototype.STATE_TEARDOWN = 2;


Line.prototype.buildSegments = function(initialVectors)
{
	this.vectors = [ initialVectors[0] ];
	this.segments = [];

	for (var i = 1; i < initialVectors.length; i++) {
		var segment = initialVectors[i].clone();
		segment.sub(initialVectors[i - 1]);

		this.segments.push(segment);
		this.vectors.push(initialVectors[i]);
	}

	var previousVector = this.vectors[this.vectors.length - 1];
	var previousSegment;
	if (this.segments.length > 0)
		previousSegment = this.segments[this.segments.length - 1];

	for (var i = this.segments.length;
		i < randomInteger(this.maxLineLength, this.minLineLength); i++) {
		var nextSegment = randomDirection(previousSegment);
		var nextVector
			= progression(previousVector, nextSegment, kCubeBounds);
		if (!nextVector) {
			i--;
			continue;
		}

		this.segments.push(nextSegment);
		this.vectors.push(nextVector);

		previousSegment = nextSegment;
		previousVector = nextVector;
	}
}


Line.prototype.queueTeardown = function()
{
	this.queuedState = this.STATE_TEARDOWN;
	this.cycleSteps = 0;
}


Line.prototype.cycle = function()
{
	switch (this.state) {
		case this.STATE_BUILDUP:
			this.completeSegment();
			if (this.completeSegments < this.segments.length)
				this.startSegment();
			else {
				this.state = this.STATE_STATIC;
				if (this.onBuildupComplete)
					this.onBuildupComplete();
			}
			break;

		case this.STATE_STATIC:
			break;

		case this.STATE_TEARDOWN:
			this.tearSegment();
			if (this.tornSegments >= this.segments.length) {
				this.state = this.STATE_STATIC;
				if (this.onTeardownComplete)
					this.onTeardownComplete();
			}
			break;
	}

	if (this.queuedState) {
		this.state = this.queuedState;
		this.queuedState = undefined;
	}

	this.cycleSteps = this.stepsPerCycle;
}


Line.prototype.completeSegment = function()
{
	var lastIndex = this.geometry.vertices.length - 1;
	this.geometry.vertices[lastIndex].copy(
		this.vectors[this.completeSegments + 1]);

	this.geometry.verticesNeedUpdate = true;
	this.completeSegments++;
}


Line.prototype.startSegment = function()
{
	var lastIndex = this.geometry.vertices.length - 1;
	for (var i = this.completeSegments; i >= 0; i--) {
		this.geometry.vertices[lastIndex - i - 1].copy(
			this.geometry.vertices[lastIndex - i]);
	}
}


Line.prototype.tearSegment = function()
{
	for (var i = 0; i < this.geometry.vertices.length - 1; i++) {
		this.geometry.vertices[i].copy(
			this.geometry.vertices[i + 1]);
	}

	this.geometry.verticesNeedUpdate = true;
	this.tornSegments++;
}


Line.prototype.animationStep = function()
{
	switch (this.state) {
		case this.STATE_STATIC:
			break;

		case this.STATE_BUILDUP:
		{
			var base = this.vectors[this.completeSegments];
			var segment = this.segments[this.completeSegments];
			var last
				= this.geometry.vertices[this.geometry.vertices.length - 1];

			last.copy(base);
			last.addScaledVector(segment,
				1 - (this.cycleSteps / this.stepsPerCycle));

			this.geometry.verticesNeedUpdate = true;
			break;
		}

		case this.STATE_TEARDOWN:
		{
			var base = this.vectors[this.tornSegments];
			var segment = this.segments[this.tornSegments];
			var first = this.geometry.vertices[0];

			first.copy(base);
			first.addScaledVector(segment,
				1 - (this.cycleSteps / this.stepsPerCycle));

			this.geometry.verticesNeedUpdate = true;
			break;
		}
	}

	this.cycleSteps--;
	if (this.cycleSteps <= 0)
		this.cycle();
}


function ObjectRotator(object)
{
	this.object = object;
	this.currentRotation = 0;
	this.steps = 0;
}


ObjectRotator.prototype.rotateTo = function(rotationAxis, rotation, steps,
	onComplete)
{
	this.rotationAxis = rotationAxis;
	this.targetRotation = rotation;
	this.rotationStep = (this.targetRotation - this.currentRotation) / steps;
	this.steps = steps;
	this.onComplete = onComplete;
}


ObjectRotator.prototype.cycle = function()
{
	this.currentRotation = this.targetRotation;
	this.steps = 0;
	if (this.onComplete)
		this.onComplete();
}


ObjectRotator.prototype.animationStep = function()
{
	if (this.steps == 0)
		return;

	this.object.rotateOnAxis(this.rotationAxis,
		THREE.Math.degToRad(this.rotationStep));

	this.steps--;
	if (this.steps == 0)
		this.cycle();
}


function render()
{
	gControls.update();

	gLines.forEach(function(element) {
			element.animationStep();
		});

	gObjectRotator.animationStep();

	//console.log(gLines[0].geometry.vertices[0]);

	//gObject.rotateOnAxis(new THREE.Vector3(1, 0, 0), 0.01);

	gRenderer.render(gScene, gCamera);

	requestAnimationFrame(render);
}


function rotateBy(vector)
{
	gObject.rotateOnAxis(vector, THREE.Math.degToRad(90));
}


function startRotation(rotation)
{
	gRotationAxis = new THREE.Vector3(1, -1, 1).normalize();
	gRotationMatrix = new THREE.Matrix4().makeRotationAxis(gRotationAxis,
		THREE.Math.degToRad(rotation));

	var viewVector = new THREE.Vector3(-1, -1, -1).applyMatrix4(gRotationMatrix)
		.round();
	gProjection = new Projection(gRotationAxis, viewVector, rotation);

	gObjectRotator.rotateTo(gRotationAxis, -rotation, kRotationSteps,
		endRotation);

	gSymbolLines = [];
	addSymbol(kSymbolKeys[gCurrentSymbolKeyIndex]);
	gCurrentSymbolKeyIndex = (gCurrentSymbolKeyIndex + 1) % kSymbolKeys.length;

	addRandomLine();
}


function endRotation()
{
	setTimeout(function() {
			gSymbolLines.forEach(function(line) {
					line.queueTeardown();
					line.onTeardownComplete = function() {
							gLines.splice(gLines.indexOf(line), 1);
							gLineContainer.remove(line.object);
						};
				});

			var recycle = gRandomLines[0];
			recycle.queueTeardown();
			recycle.onTeardownComplete = function() {
					gLines.splice(gLines.indexOf(recycle), 1);
					gLineContainer.remove(recycle.object);
				};
			gRandomLines.splice(0, 1);

			gTargetRotation += 120;
			startRotation(gTargetRotation);
		}, 1000);
}


function addSymbol(symbolKey)
{
	var symbol = kSymbols[symbolKey].clone().rotateByMatrix(gRotationMatrix);
	symbol.shapes.forEach(function(shape) {
			var segmentCount = shape.length - 1;
			for (var i = 0; i < segmentCount;) {
				var count = randomInteger(
					Math.min(segmentCount - i, kMaxLineLength), 1);
				var previousVector = shape[i];
				var previousRandomizedVector
					= gProjection.randomVectorForProjectedPoint(previousVector);
				var vectors = [ previousRandomizedVector ];

				for (var j = 0; j < count; j++) {
					var vector = shape[i + j + 1];
					var randomizedVector
						= gProjection.randomProgression(previousVector,
							previousRandomizedVector, vector);

					vectors.push(randomizedVector);

					previousVector = vector;
					previousRandomizedVector = randomizedVector;
				}

				var line = new Line(vectors, 0, 0, kSymbolLineWidth,
					kLineBuildSteps);

				gLines.push(line);
				gSymbolLines.push(line);
				gLineContainer.add(line.object);

				i += count;
			}
		});
}


function addRandomLine()
{
	var start = randomVector(kCubeBounds);
	var line = new Line([ start ], kMinLineLength, kMaxLineLength,
		kRandomLineWidth, kLineBuildSteps);

	gLines.push(line);
	gRandomLines.push(line);
	gLineContainer.add(line.object);
}


function init()
{
	console.log('line_cube init');
	
	gRenderer = new THREE.CanvasRenderer();
	gRenderer.setSize(kViewWidth, kViewHeight);
	gRenderer.setClearColor(0xffffff);
	document.body.appendChild(gRenderer.domElement);

	gCamera = new THREE.OrthographicCamera(-kViewWidth / kZoom,
		kViewWidth / kZoom, -kViewHeight / kZoom, kViewHeight / kZoom, 1, 1000);

	gCamera.position.set(10, 10, 10);
	gCamera.lookAt(new THREE.Vector3(0, 0, 0));

	gControls = new THREE.TrackballControls(gCamera);
	gControls.rotateSpeed = 10.0;
	gControls.zoomSpeed = 1.0;
	gControls.noPan = true;
	gControls.staticMoving = true;
	gControls.dynamicDampingFactor = 0.3;

	gLineContainer = new THREE.Object3D();
	gLines = [];
	gSymbolLines = [];
	gRandomLines = [];

	for (var i = 0; i < kRandomLineCount; i++)
		addRandomLine();

	for (var i = 0; i < 10; i++) {
		var start = randomVector(kCubeBounds);
		var middle = randomDirection(new THREE.Vector3(0, 0, 0));
		middle.add(start);

		var end = randomDirection(new THREE.Vector3(0, 0, 0));
		end.add(start);

		var geometry = new THREE.Geometry();
		geometry.vertices.push(start);
		geometry.vertices.push(middle);
		geometry.vertices.push(end);

		geometry.faces.push(new THREE.Face3(0, 1, 2));

		var material = new THREE.MeshBasicMaterial({
				color: 0x000000,
				side: THREE.DoubleSide
			});

		//gLineContainer.add(new THREE.Mesh(geometry, material));
	}

	gLineContainer.translateX(kCubeTranslation.x);
	gLineContainer.translateY(kCubeTranslation.y);
	gLineContainer.translateZ(kCubeTranslation.z);

	gObject = new THREE.Object3D();
	gObject.add(gLineContainer);
	//gObject.add(new THREE.AxisHelper(5));

	gScene = new THREE.Scene();
	gScene.add(gObject);

	gObjectRotator = new ObjectRotator(gObject);

	gTargetRotation = 120;
	startRotation(gTargetRotation);

	requestAnimationFrame(render);
}


window.onload = init;
