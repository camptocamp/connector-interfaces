/*!
 * bootstrap-imgupload v2.2.0 2016/08/05
 * https://github.com/egonolieux/bootstrap-imgupload
 * Copyright 2016 Egon Olieux
 * Released under the MIT license
 */

(function($) {
    var options = {
        allowedFormats: [ "jpg", "jpeg", "png", "gif" ],
        previewWidth: 250,
        previewHeight: 250,
        maxFileSizeKb: 2048
    };

    $.fn.imgupload = function(givenOptions) {
        if (this.filter("div").hasClass("imgupload")) {
            options = $.extend(options, givenOptions); 

            var $fileTab = this.find(".file-tab");
            var $urlTab = this.find(".url-tab");
            var $fileTabButton = this.find(".panel-heading .btn:eq(0)");
            var $removeFileButton = $fileTab.find(".btn:eq(1)");
            var $urlTabButton = this.find(".panel-heading .btn:eq(1)");
            var $submitUrlButton = $urlTab.find(".btn:eq(0)");

            // Show file tab by default and do a reset.
            resetFileTab($fileTab);
            showFileTab($fileTab);

            // Unbind all previous bound event handlers.
            $fileTabButton.off();
            $fileTab.off("change", ".btn:eq(0)");
            $removeFileButton.off();
            $urlTabButton.off();
            $submitUrlButton.off();

            // Handle file tab button clicked.
            $fileTabButton.on("click", function() {
                $(this).blur();
                showFileTab($fileTab);
            });

            // Handle file input changed.
            $fileTab.on("change", ".btn:eq(0)", function() {
                $(this).blur();
                selectImageFile($fileTab);
            });

            // handle remove file button clicked.
            $removeFileButton.on("click", function() {
                $(this).blur();
                resetFileTab($fileTab);
            });

            // Handle URL tab clicked.
            $urlTabButton.on("click", function() {
                $(this).blur();
                showUrlTab($urlTab);
            });

            // Handle submit URL clicked.
            $submitUrlButton.on("click", function() {
                $(this).blur();
                selectImageUrl($urlTab);
            });
        }

        return this;
    };

    function getAlertHtml(message) {
        var html = [];
        html.push("<div class='alert alert-danger alert-dismissible'>");
        html.push("<button type='button' class='close' data-dismiss='alert'>");
        html.push("<span>&times;</span>");
        html.push("</button>" + message);
        html.push("</div>");
        return html.join("");
    }

    function getImageThumbnailHtml(src) {
        return "<img src='" + src + "' alt='Image preview' class='thumbnail' style='max-width: " + options.previewWidth + "px; max-height: " + options.previewHeight + "px'>";
    }

    function isValidImageUrl(url, callback) {
        var image = new Image();
        image.onerror = function() {
            callback(false, "Image could not be found.");
        };
        image.onload =  function() {
            // Check image format by file extension.
            var fileExtension = url.substr(url.lastIndexOf('.') + 1).toLowerCase();
            if ($.inArray(fileExtension, options.allowedFormats) > -1) {
                callback(true, "");
            }
            else {
                callback(false, "File type is not allowed.");
            }
        };
        image.src = url;
    }

    function showFileTab($fileTab) {
        var $imgupload = $fileTab.closest(".imgupload");
        var $fileTabButton = $imgupload.find(".panel-heading .btn:eq(0)");

        if (!$fileTabButton.hasClass("active")) {
            var $urlTab = $imgupload.find(".url-tab");

            // Show file tab and hide URL tab.
            $imgupload.find(".panel-heading .btn:eq(1)").removeClass("active");
            $fileTabButton.addClass("active");
            $urlTab.hide();
            $fileTab.show();
            resetUrlTab($urlTab);
        }
    }

    function resetFileTab($fileTab) {
        $fileTab.find(".alert").remove();
        $fileTab.find(".btn:eq(1)").hide();
        $fileTab.find(".btn span").text("Browse");
        $fileTab.find("input").val("");
        $fileTab.find("img").remove();
    }

    function selectImageFile($fileTab) {
        var $submitUrlButton = $fileTab.find(".btn:eq(0)");
        var $fileInput = $submitUrlButton.find("input");
        
        // Remove errors and previous image.
        $fileTab.find(".alert").remove();
        $fileTab.find("img").remove();

        // Check if file was uploaded.
        var hasFile = $fileInput[0].files && $fileInput[0].files[0];
        if (!hasFile) return;

        // Check file size.
        var file = $fileInput[0].files[0];
        if (file.size / 1024 > options.maxFileSizeKb)
        {
            $fileInput.val("");
            $fileTab.prepend(getAlertHtml("File is too large (max " + options.maxFileSizeKb + "kB)."));
            return;
        }

        // Check image format by file extension.
        var fileExtension = file.name.substr(file.name.lastIndexOf('.') + 1).toLowerCase();
        if ($.inArray(fileExtension, options.allowedFormats) > -1) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $fileTab.append(getImageThumbnailHtml(e.target.result));
            };
            reader.onerror = function(e) {
                $fileInput.val("");
                $fileTab.prepend(getAlertHtml("Error loading image."));
            };
            reader.readAsDataURL(file);

            // Change submit button text to "change" and show remove button.
            $submitUrlButton.find("span").text("Change");
            $fileTab.find(".btn:eq(1)").css("display", "inline-block");
        }
        else {
            $fileInput.val("");
            $fileTab.prepend(getAlertHtml("File type is not allowed."));
        }
    }

    function showUrlTab($urlTab) {
        var $imgupload = $urlTab.closest(".imgupload");
        var $urlTabButton = $imgupload.find(".panel-heading .btn:eq(1)");

        if (!$urlTabButton.hasClass("active")) {
            var $fileTab = $imgupload.find(".file-tab");

            // Show URL tab and hide file tab.
            $imgupload.find(".panel-heading .btn:eq(0)").removeClass("active");
            $urlTabButton.addClass("active");
            $fileTab.hide();
            $urlTab.show();
            resetFileTab($fileTab);
        }
    }

    function resetUrlTab($urlTab) {
        $urlTab.find(".alert").remove();
        $urlTab.find("input").val("");
        $.each($urlTab.find(".btn"), function(key, value) {
            if ($(value).text() == "Remove") {
                $(value).remove();
            }
            else {
                $(value).text("Submit");
            }
        });
        $urlTab.find("img").remove();
    }

    function selectImageUrl($urlTab) {
        var url = $urlTab.find("input:text").val();
        if (!url) return;

        var $textInput = $urlTab.find("input:text");
        var $buttons = $urlTab.find(".btn");
        
        // Disable input.
        $textInput.prop("disabled", true);
        $buttons.prop("disabled", true);

        // Remove errors and previous image.
        $urlTab.find(".alert").remove();
        $urlTab.find("img").remove();

        isValidImageUrl(url, function(isValid, message) {
            if (isValid) {
                $urlTab.find("input:hidden").val(url);
                $urlTab.append(getImageThumbnailHtml(url));

                if ($buttons.length == 1) {
                    $urlTab.find(".input-group-btn").append("<button type='button' class='btn btn-default'>Remove</button>");

                    // Remove URL and remove remove button.
                    $urlTab.find(".btn:eq(1)").on("click", function() {
                        $(this).blur();
                        $urlTab.find(".alert").remove();
                        $urlTab.find("input").val("");
                        $urlTab.find("img").remove();
                        $(this).remove();
                    });
                }
            }
            else {
                if ($buttons.length == 2) $buttons[1].remove();
                $urlTab.prepend(getAlertHtml(message));
            }

            // Enable input.
            $textInput.prop("disabled", false);
            $buttons.prop("disabled", false);
        });
    }
}(jQuery));
