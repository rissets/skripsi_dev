$(document).ready(function () {
    const dropzone = $("#dropzone");
    let file;

    // Drag-and-drop functionality
    dropzone.on("dragover", function (e) {
        e.preventDefault();
        dropzone.css("background-color", "#e6e6e6");
    });

    dropzone.on("dragleave", function () {
        dropzone.css("background-color", "#f5f5f5");
    });

    dropzone.on("drop", function (e) {
        e.preventDefault();
        file = e.originalEvent.dataTransfer.files[0];
        handleUpload();
    });

    // Click functionality
    $("#upload-button").on("click", function () {
        file = $("#file-input")[0].files[0];
        handleUpload();
    });

    // File input
    const input = $("<input>")
        .attr("type", "file")
        .attr("accept", ".pdf")
        .hide();

    dropzone.on("click", function () {
        input.trigger("click");
    });

    input.on("change", function () {
        file = input[0].files[0];
        handleUpload();
    });

    function handleUpload() {
        if (file) {
            const formData = new FormData();
            formData.append("file", file);

            // Upload the file using AJAX
            $.ajax({
                url: "upload.php",
                type: "POST",
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    console.log("File uploaded successfully:", response);
                },
                error: function (xhr, status, error) {
                    console.error("File upload failed:", error);
                },
            });
        }
    }
});