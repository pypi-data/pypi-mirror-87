"""
This file contains all HTML code required for MiUpload to be displayed.

"""

HTML_PROGRESS_BAR = """<br><div class="progress">
          <div id="submitprogress" class="progress-bar progress-bar-info progress-bar-striped active" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%">
            <span id="current-progress"></span>
          </div>
        </div>"""

HTML_KERNEL_API_CALL_FAILED = """<div class="alert alert-block alert-warning">
                    <b>Failed to get filename of notebook from API!</b> <br>---> Please copy and paste filename and path of notebook <b>from URL</b> (copy everything after .../notebooks/
                    </div>"""
HTML_MESSAGE_INPUT_REQUIRED = """<div class="alert alert-block alert-warning">
                    <b>INPUT REQUIRED! Unable to find location of notebook</b> <br> Please submit your Jupyter Notebook manually using the form bellow:
                    </div>"""

HTML_MESSAGE_CONNECTION_FAILED = """<div class="alert alert-block alert-danger">
                                        <b>Upload failed!</b> Error: Cannot connect with the server. <br>Please check your internet connection. If the problem persist, email your notebook to your peer tutor manually.
                                        </div>"""
HTML_UPLOAD_ERROR_CUSTOM_START ="""<div class="alert alert-block alert-danger">
                                <b>Upload failed!</b> Error:"""

HTML_UPLOAD_ERROR_CUSTOM_END = """  <br>Please email your notebook to your peer tutor manually.
                                </div>"""

JS_PROGRESS_BAR_INIT = """$(function() {
          var interval3 = setInterval(function() {
               var current_progress = parseInt($("#submitprogress").attr("aria-valuenow"));
              current_progress += 1;
              $("#submitprogress")
              .css("width", current_progress + "%")
              .attr("aria-valuenow", current_progress)
              .text(current_progress + "% Complete");
              if (current_progress >= 30)
                  clearInterval(interval3);
          }, 200);
        });"""

JS_PROGRESS_BAR_FAST_STEP = """$(function() {
             var interval4 = setInterval(function() {
                  var current_progress = parseInt($("#submitprogress").attr("aria-valuenow"));
                 current_progress += 1;
                 $("#submitprogress")
                 .css("width", current_progress + "%")
                 .attr("aria-valuenow", current_progress)
                 .text(current_progress + "% Complete");
                 if (current_progress >= 55)
                     clearInterval(interval4);
             }, 30);
           });"""

JS_PROGRESS_BAR_STEPS = """$(function() {
      var interval = setInterval(function() {
           var current_progress = parseInt($("#submitprogress").attr("aria-valuenow"));
          current_progress += 1;
          $("#submitprogress")
          .css("width", current_progress + "%")
          .attr("aria-valuenow", current_progress)
          .text(current_progress + "% Complete");
          if (current_progress >= 91)
              clearInterval(interval);
      }, 600);
    });"""

JS_PROGRESS_BAR_FINAL = """
                    $(function() {
                  var interval2 = setInterval(function() {
                    var current_progress = parseInt($("#submitprogress").attr("aria-valuenow"));
                      current_progress += 1;
                      $("#submitprogress")
                      .css("width", current_progress + "%")
                      .attr("aria-valuenow", current_progress)
                      .text(current_progress + "% Complete");
                      if (current_progress >= 100)
                      $("#submitprogress").addClass('progress-bar-success')
                      .removeClass('progress-bar-info')
                      .removeClass('active')
                      if (current_progress >= 100)
                          clearInterval(interval2);  
                  }, 60);
                });"""

JS_PROGRESS_BAR_DANGER = """
                              $("#submitprogress")
                              .addClass('progress-bar-danger')
                              .removeClass('progress-bar-info')
                              .removeClass('active')
                          """

