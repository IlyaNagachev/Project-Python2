$(document).ready(function () {
    
    $(".text").textillate({
        loop: true,
        sync: true,
        in: {
            effect: "bounceIn",
        },
        out: {
            effect: "bounceOut",
        },

    });

    // Siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 640,
        height: 200,
        speed: 0.15,
        color: "#ff7300",
        autostart: true
        });

    // siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },
    });

    // siri message animation
    $(".siri-message").textillate({
        loop: true,
        sync: true,
        in: {
            effect: "fadeInUp",
            sync: true,
        },
        out: {
            effect: "fadeOutUp",
            sync: true,
        },

    });

    //mic btn click

    $("#MicBtn").click(function () {

        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.main()()
        
    });

});