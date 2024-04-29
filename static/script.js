$(window).on("load", () => {
    setTimeout(() => {
        if ($(".flashed_msgs") != undefined) {
            $(".flashed_msgs").remove();
        }
    }, 5000);
    $(".selectChoice").on("click", (e) => {
        $(".selected").filter(v => v!== $(e.target)).toggleClass("selected");
        $("#selectedChoice").val($(e.target).attr("id")).change();
        $(e.target).addClass("selected");
    });
});
