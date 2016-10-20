# Bootstrap Image Upload

`bootstrap-imgupload` is a Bootstrap/jQuery plugin which shows a preview/thumbnail of the image to be uploaded from both file and URL.

## Table of contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Demo](#demo)

## Requirements

- Bootstrap 3.0.0+
- jQuery 1.7+

## Installation

Following installation options are available:

- Download and include the files manually.
- Install with composer: `composer require egonolieux/bootstrap-imgupload`.

## Usage

### HTML

Use as many instances on the same page as you want.

```HTML
<div class="imgupload panel panel-default">
    <div class="panel-heading clearfix">
        <h3 class="panel-title pull-left">Upload image</h3>
        <div class="btn-group pull-right">
            <button type="button" class="btn btn-default active">File</button>
            <button type="button" class="btn btn-default">URL</button>
        </div>
    </div>
    <div class="file-tab panel-body">
        <div>
            <label class="btn btn-default btn-file">
                <span>Browse</span>
                 <!-- The file is stored here. -->
                <input type="file" name="image-file">
            </label>
            <button type="button" class="btn btn-default">Remove</button>
        </div>
    </div>
    <div class="url-tab panel-body">
        <div class="input-group">
            <input type="text" class="form-control" placeholder="Image URL">
            <div class="input-group-btn">
                <button type="button" class="btn btn-default">Submit</button>
            </div>
        </div>
        <!-- The URL is stored here. -->
        <input type="hidden" name="image-url">
    </div>
</div>
```

### jQuery

#### Using Default Options

```jQuery
$('imgupload').imgupload();
```

Default options are:

```jQuery
allowedFormats: [ "jpg", "jpeg", "png", "gif" ],
previewWidth: 250,
previewHeight: 250,
maxFileSizeKb: 2048
```

#### Overriding Default Options

```jQuery
$('imgupload').imgupload({
    allowedFormats: [ "jpg" ],
    maxFileSizeKb: 512
});

```

## Demo

https://egonolieux.github.io/bootstrap-imgupload
