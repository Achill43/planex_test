var mainModal = new bootstrap.Modal(document.getElementById('js-main-modal'))

$(document).ready(function () {
    $("body").on("click", ".js-export-to-csv", function(e) {
        e.preventDefault();
        var schema_ids_checkbox = document.getElementsByName('export_schema');
        var schema_ids = [];
        for (var index = 0; index < schema_ids_checkbox.length; index++) {
            if (schema_ids_checkbox[index].checked) {
                schema_ids.push(parseInt(schema_ids_checkbox[index].value));
            }
        }
        console.log(schema_ids);
        $.ajax({
            url: $(this).attr("href"),
            type: "GET",
            data: {
                "schema_ids": schema_ids
            },
            success: function(data) {
                $(".js-modal-body").html(data.html);
                mainModal.show();
            },
        });
    })
})