﻿$(function () {
    $("#searchForm").on("submit", function (e) {
        if ($("#autocomplete").val().trim() === "") {
            e.preventDefault();
            return false;
        }
    });

    $("#autocomplete").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/Home/AutoComplete",
                type: "GET",
                data: { prefix: request.term },
                success: function (data) {
                    response(data);
                }
            });
        },
        minLength: 2,
        select: function (event, ui) {
            $("#autocomplete").val(ui.item.value);
            $("#searchForm").submit();
        }
    }).autocomplete("instance")._renderItem = function (ul, item) {
        var newText = String(item.label).replace(
            new RegExp(this.term, "gi"),
            "<strong>$&</strong>");

        return $("<li></li>")
            .data("item.autocomplete", item)
            .append("<div><img src='" + item.image + "' alt='" + item.label + "' style='width: 32px; height: 32px; margin-right: 10px;'>" + newText + "</div>")
            .appendTo(ul);
    };
});