

profile_get();
//notification_update("self");


    var btn = document.getElementById("postbtn");
    btn.addEventListener("click", function() {
    createPost({"text": document.getElementById("postBox").value});
    document.getElementById("postBox").value = "";
    });

document.getElementById("taskcl").setAttribute("href", window.location.href + "/tasks/create");
document.getElementById("tasktodo").setAttribute("href", window.location.href + "/tasks/create");