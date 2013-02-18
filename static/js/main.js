/*
 * jQuery File Upload Plugin JS Example 6.11
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint nomen: true, unparam: true, regexp: true */
/*global $, window, document */

$(function () {
    'use strict';
	var initial_image_path = "";

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
        // Uncomment the following to send cross-domain cookies:
        //xhrFields: {withCredentials: true},
        url: '/upload/uploader/'
    });


	$('#fileupload').fileupload('option', {
		autoUpload: true,
		previewAsCanvas: true,
		maxNumberOfFiles: 10,
		maxFileSize: 5000000,
		minFileSize: 5000,
		acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
		process: [
			{
				action: 'load',
				fileTypes: /^image\/(gif|jpeg|png)$/,
			},
			{
				action: 'save'
			}
		]
	});

	/*if ($.support.cors) {
		$.ajax({
			type: 'HEAD'
		}).fail(function () {
				$('<span class="alert alert-error"/>')
					.text('Upload server currently unavailable - ' +
					new Date())
					.appendTo('#fileupload');
			});
	}*/

	$('#fileupload')
		.bind('fileuploadadd', function (e, data) {

		})
		.bind('fileuploaddestroy', function (e, data) {

		})
		.bind('fileuploaddone', function (e, data) {

		})
		.bind('fileuploadfail', function (e, data) {
			alert("Sorry Image upload has failed");
		});


    // Load existing files:
    $.ajax({
        // Uncomment the following to send cross-domain cookies:
        //xhrFields: {withCredentials: true},
        url: $('#fileupload').fileupload('option', 'url'),
        dataType: 'json',
        context: $('#fileupload')[0]
    }).done(function (result) {
        if (result && result.length) {
            $(this).fileupload('option', 'done').call(this, null, {result: result});
        }
    });
});
