'use strict';


new function(LogoNamespace) {


function randomInteger(max, min)
{
	if (min == undefined)
		min = 0;

	return Math.floor(Math.random() * (max - min + 1)) + min;
}


function randomVector(bounds)
{
	return new THREE.Vector3(randomInteger(bounds.max[0], bounds.min[0]),
		randomInteger(bounds.max[1], bounds.min[1]),
		randomInteger(bounds.max[2], bounds.min[2]));
}


function randomDirection(previousDirection, directions)
{
	var negatedPreviousDirection;
	if (previousDirection) {
		negatedPreviousDirection = previousDirection.clone();
		negatedPreviousDirection.negate();
	}

	while (true) {
		var direction = directions[randomInteger(directions.length - 1)];
		if (previousDirection && direction.equals(negatedPreviousDirection))
			continue;

		return direction.clone();
	}
}


function progression(previousVector, direction, boundingBox)
{
	var result = previousVector.clone();
	result.add(direction);
	return boundingBox.vectorWithin(result) ? result : false;
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


Symbol.prototype.copy = function(other)
{
	this.shapes.forEach(function(shape, shapeIndex) {
			shape.forEach(function(vertex, vertexIndex) {
					vertex.copy(other.shapes[shapeIndex][vertexIndex]);
				});
		});

	return this;
}


Symbol.prototype.rotateByMatrix = function(rotationMatrix, center)
{
	this.shapes.forEach(function(shape) {
			shape.forEach(function(vertex) {
					vertex.sub(center)
						.applyMatrix4(rotationMatrix)
						.add(center)
						.round();
				});
		});

	return this;
}


function Projection()
{
	this.viewVector = new THREE.Vector3();
	this.negatedViewVector = new THREE.Vector3();
}


Projection.prototype.setTo = function(viewVector)
{
	this.viewVector.copy(viewVector);
	this.negatedViewVector.copy(viewVector).negate();
}


Projection.prototype.findEquivalentPoints = function(base, vector, into,
	boundingBox)
{
	var next = base;
	while (next = progression(next, vector, boundingBox))
		into.push(next);
}


Projection.prototype.equivalentPointsFor = function(projectedPoint, boundingBox)
{
	var points = [];
	if (boundingBox.vectorWithin(projectedPoint))
		points.push(projectedPoint.clone());

	this.findEquivalentPoints(projectedPoint, this.viewVector, points,
		boundingBox);
	this.findEquivalentPoints(projectedPoint, this.negatedViewVector, points,
		boundingBox);

	return points;
}


Projection.prototype.randomVectorForProjectedPoint = function(projectedPoint,
	boundingBox)
{
	var candidates = this.equivalentPointsFor(projectedPoint, boundingBox);
	return candidates[randomInteger(candidates.length - 1)];
}


Projection.prototype.randomProgression = function(originalFrom, randomizedFrom,
	originalTo, boundingBox)
{
	var equivalentTo = originalTo.clone();
	equivalentTo.sub(originalFrom);
	equivalentTo.add(randomizedFrom);
	return this.randomVectorForProjectedPoint(equivalentTo,
		new BoundingBox(3).fromVector(randomizedFrom, randomizedFrom)
			.extendByWidth(1).constrainTo(boundingBox));
}


function Line(initialVectors, directions, boundingBox, center, minLineLength,
	maxLineLength, lineWidth, time)
{
	this.minLineLength = minLineLength;
	this.maxLineLength = maxLineLength;
	this.lineWidth = lineWidth;

	this.buildSegments(initialVectors, directions, boundingBox);

	this.vectors.forEach(function(vector) {
			vector.sub(center);
		});

	this.vertices = [ this.vectors[0].clone() ];
	this.projectedVertices = [ new THREE.Vector3() ];
	this.startSegment();

	this.state = this.STATE_BUILDUP;
	this.completeSegments = 0;
	this.tornSegments = 0;

	this.timePerCycle = time / this.segments.length;
	this.currentCycle = 0;
}


Line.prototype.STATE_BUILDUP = 0;
Line.prototype.STATE_STATIC = 1;
Line.prototype.STATE_TEARDOWN = 2;


Line.prototype.buildSegments = function(initialVectors, directions, boundingBox)
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
		var nextSegment = randomDirection(previousSegment, directions);
		var nextVector = progression(previousVector, nextSegment, boundingBox);
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


Line.prototype.startTeardown = function()
{
	if (this.state == this.STATE_TEARDOWN)
		return;

	this.state = this.STATE_TEARDOWN;
	this.currentCycle = 0;
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

	this.currentCycle++;
}


Line.prototype.completeSegment = function()
{
	this.completeSegments++;
	this.vertices[this.vertices.length - 1].copy(
		this.vectors[this.completeSegments]);
}


Line.prototype.startSegment = function()
{
	if (this.completeSegments > 0
		&& this.segments[this.completeSegments].equals(
			this.segments[this.completeSegments - 1])) {
		return;
	}

	this.vertices.push(this.vertices[this.vertices.length - 1].clone());
	this.projectedVertices.push(new THREE.Vector3());
}


Line.prototype.tearSegment = function()
{
	this.tornSegments++;
	if (this.tornSegments >= this.segments.length
		|| this.segments[this.tornSegments].equals(
			this.segments[this.tornSegments - 1])) {
		return;
	}

	this.vertices.shift();
	this.projectedVertices.shift();
}


Line.prototype.animationStep = function(elapsedTime)
{
	var progress = (elapsedTime - this.timePerCycle * this.currentCycle)
		/ this.timePerCycle;
	while (progress >= 1) {
		this.cycle();
		progress--;
	}

	switch (this.state) {
		case this.STATE_STATIC:
			break;

		case this.STATE_BUILDUP:
		{
			var base = this.vectors[this.completeSegments];
			var segment = this.segments[this.completeSegments];
			var last = this.vertices[this.vertices.length - 1];

			last.copy(base);
			last.addScaledVector(segment, progress);
			break;
		}

		case this.STATE_TEARDOWN:
		{
			var base = this.vectors[this.tornSegments];
			var segment = this.segments[this.tornSegments];
			var first = this.vertices[0];

			first.copy(base);
			first.addScaledVector(segment, progress);
			break;
		}
	}
}


function ObjectRotator(matrix)
{
	this.matrix = matrix;
	this.initialMatrix = matrix.clone();
	this.rotationMatrix = new THREE.Matrix4();
	this.currentRotation = 0;
}


ObjectRotator.prototype.resetMatrix = function(matrix)
{
	this.matrix.copy(matrix);
	this.initialMatrix.copy(matrix);
}


ObjectRotator.prototype.rotateTo = function(rotationAxis, rotation, time,
	onComplete)
{
	this.rotationAxis = rotationAxis;
	this.targetRotation = rotation;
	this.rotationStep = (this.targetRotation - this.currentRotation) / time;
	this.totalTime = time;
	this.complete = false;
	this.onComplete = onComplete;
}


ObjectRotator.prototype.cycle = function()
{
	this.complete = true;
	this.currentRotation = this.targetRotation;
	this.rotationStep = 0;
	if (this.onComplete)
		this.onComplete();
}


ObjectRotator.prototype.animationStep = function(elapsedTime)
{
	if (this.complete)
		return;

	if (elapsedTime >= this.totalTime)
		this.cycle();

	this.rotationMatrix.makeRotationAxis(this.rotationAxis,
		THREE.Math.degToRad(this.currentRotation
			+ this.rotationStep * elapsedTime));
	this.matrix.multiplyMatrices(this.initialMatrix, this.rotationMatrix);
}


function BoundingBox(components)
{
	this.min = new Array(components);
	this.max = new Array(components);
}


BoundingBox.prototype.fromArray = function(min, max)
{
	for (var i = 0; i < this.min.length; i++) {
		this.min[i] = min[i];
		this.max[i] = max[i];
	}

	return this;
}


BoundingBox.prototype.fromVector = function(min, max)
{
	for (var i = 0; i < this.min.length; i++) {
		this.min[i] = min.getComponent(i);
		this.max[i] = max.getComponent(i);
	}

	return this;
}


BoundingBox.prototype.reset = function()
{
	for (var i = 0; i < this.min.length; i++) {
		this.min[i] = 1000000;
		this.max[i] = 0;
	}

	return this;
}


BoundingBox.prototype.round = function()
{
	for (var i = 0; i < this.min.length; i++) {
		this.min[i] = Math.floor(this.min[i]);
		this.max[i] = Math.ceil(this.max[i]);
	}

	return this;
}


BoundingBox.prototype.vectorWithin = function(vector)
{
	for (var i = 0; i < this.min.length; i++) {
		if (vector.getComponent(i) < this.min[i]
			|| vector.getComponent(i) > this.max[i]) {
			return false;
		}
	}

	return true;
}


BoundingBox.prototype.include = function(components)
{
	for (var i = 0; i < this.min.length; i++) {
		this.min[i] = Math.min(this.min[i], components[i]);
		this.max[i] = Math.max(this.max[i], components[i]);
	}

	return this;
}


BoundingBox.prototype.extendByWidth = function(width)
{
	for (var i = 0; i < this.min.length; i++) {
		this.min[i] -= width;
		this.max[i] += width;
	}

	return this;
}


BoundingBox.prototype.constrainTo = function(boundingBox)
{
	for (var i = 0; i < this.min.length; i++) {
		this.min[i] = Math.max(this.min[i], boundingBox.min[i]);
		this.max[i] = Math.min(this.max[i], boundingBox.max[i]);
	}

	return this;
}


function Logo(targetElementId)
{
	this.initConfig();

	var canvas = document.getElementById(targetElementId);

	this.graphicsContext = canvas.getContext('2d', { alpha: false });
	this.graphicsContext.fillStyle = '#ffffff';
	this.graphicsContext.strokeStyle = '#000000';
	this.graphicsContext.lineCap = 'round';
	this.graphicsContext.lineJoin = 'round';

	this.boundingBox = new BoundingBox(2)
		.fromArray([ 0, 0 ], [ canvas.width, canvas.height ]);

	var orthographicProjection = new THREE.Matrix4().makeOrthographic(
		-this.config.cubeSize, this.config.cubeSize, -this.config.cubeSize,
		this.config.cubeSize, 1,
		this.config.cubeSize * 2 * this.config.cubeSize * 2);
	var lookAt = new THREE.Matrix4().lookAt(
		new THREE.Vector3(this.config.cubeSize * 2, this.config.cubeSize * 2,
			this.config.cubeSize * 2),
		new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 1, 0));

	var matrix = new THREE.Matrix4().makeScale(canvas.width / 2,
		-canvas.height / 2, 1);
	matrix.multiply(new THREE.Matrix4().makeTranslation(1, -1, 0));
	matrix.multiply(orthographicProjection);
	matrix.multiply(new THREE.Matrix4().getInverse(lookAt));

	this.initialMatrix = matrix.clone();
	this.objectRotator = new ObjectRotator(matrix);

	this.targetRotation = 0;
	this.rotationAxis = new THREE.Vector3(1, -1, 1).normalize();
	this.rotationMatrix = new THREE.Matrix4();
	this.viewVector = new THREE.Vector3();
	this.projection = new Projection();

	this.randomLines = [];
	this.symbolLines = [];
	this.lineClasses = [ this.randomLines, this.symbolLines ];

	this.currentSymbolKeyIndex = 0;
	this.symbolCache = {};

	this.triggerNextRotation();

	for (var i = 0; i < this.config.randomLineCount; i++)
		this.addRandomLine();
}


Logo.prototype.initConfig = function()
{
	var config = {};
	config.rotationTime = 4000;
	config.lineBuildTime = config.rotationTime / 4 * 3;
	config.pauseDuration = 1000;
	config.symbolLineWidth = 4;
	config.randomLineWidth = 2;
	config.randomLineCount = 4;
	config.minLineLength = 5;
	config.maxLineLength = 8;
	config.cubeSize = 4;

	config.cubeBounds = new BoundingBox(3).fromArray([ 0, 0, 0 ],
		[ config.cubeSize, config.cubeSize, config.cubeSize ]);

	config.cubeCenter = new THREE.Vector3(config.cubeSize / 2,
		config.cubeSize / 2, config.cubeSize / 2);

	config.directions = [
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

	config.symbols = {
			' ': new Symbol(),
			'c': new Symbol([
				[
					[ 1, 0, 0 ], [ 2, 0, 1 ], [ 2, 0, 2 ], [ 1, 0, 2 ],
					[ 0, 0, 2 ], [ 0, 1, 2 ], [ 0, 2, 2 ], [ 0, 2, 1 ],
					[ 0, 2, 0 ], [ 1, 2, 0 ], [ 1, 1, 0 ], [ 0, 1, 0 ],
					[ 0, 1, 1 ], [ 0, 0, 1 ], [ 1, 0, 1 ], [ 1, 0, 0 ]
				]
			]),
			'd': new Symbol([
				[
					[ 2, 0, 2 ], [ 1, 0, 2 ], [ 0, 0, 1 ], [ 0, 1, 1 ],
					[ 0, 2, 1 ], [ 0, 2, 0 ], [ 1, 2, 0 ], [ 2, 2, 0 ],
					[ 2, 1, 0 ], [ 2, 0, 0 ], [ 2, 0, 1 ], [ 2, 0, 2 ]
				],
				[
					[ 1, 0, 1 ], [ 0, 0, 0 ], [ 0, 1, 0 ], [ 1, 1, 0 ],
					[ 1, 0, 0 ], [ 1, 0, 1 ]
				]
			]),
			'f': new Symbol([
				[
					[ 3, 0, 2 ], [ 2, 0, 2 ], [ 1, 0, 2 ], [ 0, 0, 1 ],
					[ 0, 1, 1 ], [ 0, 2, 1 ], [ 0, 3, 1 ], [ 0, 2, 0 ],
					[ 0, 1, 0 ], [ 1, 1, 0 ], [ 1, 0, 0 ], [ 0, 0, 0 ],
					[ 1, 0, 1 ], [ 2, 0, 1 ], [ 3, 0, 2 ]
				]
			]),
			'k': new Symbol([
				[
					[ 3, 0, 3 ], [ 2, 0, 3 ], [ 1, 0, 2 ], [ 0, 0, 1 ],
					[ 0, 1, 1 ], [ 0, 2, 1 ], [ 0, 2, 0 ], [ 0, 1, 0 ],
					[ 1, 2, 0 ], [ 2, 3, 0 ], [ 2, 2, 0 ], [ 1, 1, 0 ],
					[ 0, 0, 0 ], [ 1, 0, 0 ], [ 2, 0, 0 ], [ 3, 0, 1 ],
					[ 2, 0, 1 ], [ 1, 0, 1 ], [ 2, 0, 2 ], [ 3, 0, 3 ]
				]
			]),
			'l': new Symbol([
				[
					[ 2, 0, 2 ], [ 2, 0, 3 ], [ 1, 0, 2 ], [ 0, 0, 1 ],
					[ 0, 1, 1 ], [ 0, 2, 1 ], [ 0, 2, 0 ], [ 1, 3, 0 ],
					[ 1, 2, 0 ], [ 0, 1, 0 ], [ 0, 0, 0 ], [ 1, 0, 1 ],
					[ 2, 0, 2 ]
				]
			]),
			'o': new Symbol([
				[
					[ 0, 0, 1 ], [ 1, 0, 1 ], [ 1, 0, 0 ], [ 1, 1, 0 ],
					[ 0, 1, 0 ], [ 0, 1, 1 ], [ 0, 0, 1 ]
				],
				[
					[ 0, 0, 2 ], [ 1, 0, 2 ], [ 2, 0, 2 ], [ 2, 0, 1 ],
					[ 2, 0, 0 ], [ 2, 1, 0 ], [ 2, 2, 0 ], [ 1, 2, 0 ],
					[ 0, 2, 0 ], [ 0, 2, 1 ], [ 0, 2, 2 ], [ 0, 1, 2 ],
					[ 0, 0, 2 ]
				]
			]),
			'u': new Symbol([
				[
					[ 1, 0, 2 ], [ 0, 0, 2 ], [ 0, 1, 2 ], [ 0, 2, 2 ],
					[ 0, 2, 1 ], [ 0, 2, 0 ], [ 1, 2, 0 ], [ 2, 2, 0 ],
					[ 2, 1, 0 ], [ 2, 0, 0 ], [ 2, 0, 1 ], [ 1, 0, 0 ],
					[ 1, 1, 0 ], [ 0, 1, 0 ], [ 0, 1, 1 ], [ 0, 0, 1 ],
					[ 1, 0, 2 ]
				]
			]),
			'x': new Symbol([
				[
					[ 0, 0, 0 ], [ 1, 0, 1 ], [ 2, 0, 2 ], [ 2, 0, 1 ],
					[ 1, 0, 0 ], [ 2, 0, 0 ], [ 3, 1, 0 ], [ 2, 1, 0 ],
					[ 1, 1, 0 ], [ 1, 2, 0 ], [ 1, 3, 0 ], [ 0, 2, 0 ],
					[ 0, 1, 0 ], [ 0, 2, 1 ], [ 0, 2, 2 ], [ 0, 1, 1 ],
					[ 0, 0, 0 ]
				]
			])
		};

	config.symbolKeys = [ 'f', 'l', 'u', 'x', 'd', 'o', 'c', 'k', ' ' ];

	this.config = config;
}


Logo.prototype.clearCanvas = function()
{
	this.boundingBox.round();

	//gContext.fillStyle = '#' + randomInteger(0xffffff);
	this.graphicsContext.fillRect(this.boundingBox.min[0],
		this.boundingBox.min[1],
		this.boundingBox.max[0] - this.boundingBox.min[0],
		this.boundingBox.max[1] - this.boundingBox.min[1]);

	this.boundingBox.reset();
}


Logo.prototype.renderLines = function()
{
	for (var i = 0; i < this.lineClasses.length; i++) {
		this.graphicsContext.beginPath();

		for (var j = 0; j < this.lineClasses[i].length; j++) {
			var line = this.lineClasses[i][j];

			this.graphicsContext.lineWidth = line.lineWidth;
			for (var k = 0; k < line.vertices.length; k++) {
				var projected = line.projectedVertices[k];
				projected.copy(line.vertices[k])
					.applyMatrix4(this.objectRotator.matrix);

				if (k == 0)
					this.graphicsContext.moveTo(projected.x, projected.y);
				else
					this.graphicsContext.lineTo(projected.x, projected.y);

				this.boundingBox.include([ projected.x, projected.y ]);
			}
		}

		this.graphicsContext.stroke();
	}

	this.boundingBox.extendByWidth(this.config.symbolLineWidth);
}


Logo.prototype.render = function()
{
	var elapsedTime = performance.now() - this.cycleStartTime;

	this.lineClasses.forEach(function(lineClass) {
			lineClass.forEach(function(line) {
					line.animationStep(elapsedTime);
				});
		});

	this.objectRotator.animationStep(elapsedTime);

	this.clearCanvas();
	this.renderLines();

	if (!this.pauseAnimation)
		requestAnimationFrame(this.render.bind(this));
}


Logo.prototype.startRotation = function()
{
	this.rotationMatrix.makeRotationAxis(this.rotationAxis,
		THREE.Math.degToRad(this.targetRotation));
	this.viewVector.set(-1, -1, -1).applyMatrix4(this.rotationMatrix).round();
	this.projection.setTo(this.viewVector);

	this.objectRotator.rotateTo(this.rotationAxis, -this.targetRotation,
		this.config.rotationTime, this.endRotation.bind(this));

	this.addSymbol(this.config.symbolKeys[this.currentSymbolKeyIndex],
		this.rotationMatrix);
	this.currentSymbolKeyIndex
		= (this.currentSymbolKeyIndex + 1) % this.config.symbolKeys.length;

	this.addRandomLine();
}


Logo.prototype.endRotation = function()
{
	this.pauseAnimation = true;
	if (Math.round(this.targetRotation % 360) == 0)
		this.objectRotator.resetMatrix(this.initialMatrix);

	setTimeout(this.triggerNextRotation.bind(this), this.config.pauseDuration);
}


Logo.prototype.triggerNextRotation = function()
{
	this.symbolLines.forEach(function(line) {
			line.startTeardown();
			line.onTeardownComplete = function() {
					this.symbolLines.splice(this.symbolLines.indexOf(line), 1);
				}.bind(this);
		}.bind(this));

	if (this.randomLines.length > 0) {
		this.randomLines[0].startTeardown();
		this.randomLines[0].onTeardownComplete = function() {
				this.randomLines.shift();
			}.bind(this);
	}

	this.targetRotation += 120;
	this.startRotation();

	this.pauseAnimation = false;
	this.cycleStartTime = performance.now();
	requestAnimationFrame(this.render.bind(this));
}


Logo.prototype.addSymbol = function(symbolKey, rotationMatrix)
{
	if (this.symbolCache.hasOwnProperty(symbolKey))
		this.symbolCache[symbolKey].copy(this.config.symbols[symbolKey]);
	else
		this.symbolCache[symbolKey] = this.config.symbols[symbolKey].clone();

	this.symbolCache[symbolKey].rotateByMatrix(rotationMatrix,
		this.config.cubeCenter);
	this.symbolCache[symbolKey].shapes.forEach(function(shape) {
			var segmentCount = shape.length - 1;
			for (var i = 0; i < segmentCount;) {
				var count = randomInteger(
					Math.min(segmentCount - i, this.config.maxLineLength), 1);
				var previousVector = shape[i];
				var previousRandomizedVector
					= this.projection.randomVectorForProjectedPoint(
						previousVector, this.config.cubeBounds);
				var vectors = [ previousRandomizedVector ];

				for (var j = 0; j < count; j++) {
					var vector = shape[i + j + 1];
					var randomizedVector
						= this.projection.randomProgression(previousVector,
							previousRandomizedVector, vector,
							this.config.cubeBounds);

					vectors.push(randomizedVector);

					previousVector = vector;
					previousRandomizedVector = randomizedVector;
				}

				var line = new Line(vectors, this.config.directions,
					this.config.cubeBounds, this.config.cubeCenter, 0, 0,
					this.config.symbolLineWidth, this.config.lineBuildTime);

				this.symbolLines.push(line);

				i += count;
			}
		}.bind(this));
}


Logo.prototype.addRandomLine = function()
{
	var start = randomVector(this.config.cubeBounds);
	var line = new Line([ start ], this.config.directions,
		this.config.cubeBounds, this.config.cubeCenter,
		this.config.minLineLength, this.config.maxLineLength,
		this.config.randomLineWidth, this.config.lineBuildTime);

	this.randomLines.push(line);
}


window.addEventListener('load', function() {
		window.logo = new Logo('logo-canvas');
	});


} // LogoNamespace
