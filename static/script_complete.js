$(window).on("load", () => {
    setTimeout(() => {
        if ($(".flashed_msgs") != undefined) {
            $(".flashed_msgs").remove();
        }
    }, 5000);
    $(".selectChoice").off("click");
    $('.selectChoice').unbind();
});
