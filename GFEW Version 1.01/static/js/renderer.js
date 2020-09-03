//This script deals with rendering data setched from database to html
//Script methods can be edited accorfing to the html design and rendering options

//post renderer
function render_post(div, list) {
    var i = 0;
    for(i = 0; i < list.length; i++)
    {
        var data_json = list[i];
        var post = '<div class="discussion-comment" id="' + data_json["_id"] + '">\
                    <p class="user-name"><strong>' + data_json["username"] + '</strong>, ' + data_json["role"] + '<span>' + data_json["date"] + '</span></p>\
                    <p>' + data_json["body"] + '</p>\
                    <img src="' + data_json["pfpURL"] + '">\
                </div>';


        document.getElementById(div).insertAdjacentHTML("afterbegin", post);
    } 
}


//task renderer
function render_task(list) {

    var i = 0;
    for(i = 0; i < list.length; i++)
    {
        var data_json = list[i];
        var task = '<div class="task-card">\
                        <div class="row">\
                            <div class="col-md-2 col-2">\
                                <input type="checkbox" name="fruit-4" value="Apple">\
                                <label for="fruit4"></label>\
                            </div>\
                            <div class="col-md-10 col-10">\
                                <p>' + data_json["title"] + 's</p>\
                                <div class="user-type">\
                                    <img src="' + data_json["pfpURL"] + '"><span class="pill pill-blue">Me</span>\
                                </div>\
                            </div>\
                        </div>\
                    </div>';


        if(data_json["type"] == "cookingLog")
        {
            document.getElementById("cookingLog").insertAdjacentHTML("afterbegin", task);
        }
        else if(data_json["type"] == "toDo")
        {
            document.getElementById("toDo").insertAdjacentHTML("afterbegin", task);
        }
    }

}


//class renderer
function render_class(div, list) {
    var i = 0;
    for(i = 0; i < list.length; i++)
    {
        var data_json = list[i];
        var Class = '<div class="discussion-comment" id="' + data_json["_id"] + '">\
                    <p class="user-name"><strong>' + data_json["title"] + '</strong><span></span></p>\
                    <p>' + data_json["body"] + '</p>\
                    <img src="' + data_json["pfpURL"] + '">\
                </div>';

        document.getElementById(div).insertAdjacentHTML("afterbegin", Class);
    }  
}

//profile renderer
function render_profile(data_json)
{
    var profile = '<div id="' + data_json["_id"] + '" class="profile-card">\
                        <img src="' + data_json["pfpURL"] + '" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; background-color: black;">\
                        <h2>' + data_json["username"] + '</h2>\
                        <p>' + data_json["role"] + '</p>\
                        <ul>\
                            <li>' + data_json["meals"] + ' <br><span>Meals</span></li>\
                            <li>' + data_json["followers"] + ' <br><span>Followers</span></li>\
                            <li>' + data_json["following"] + ' <br><span>Follows</span></li>\
                        </ul>\
                    </div>';

    document.getElementById("profileholder").innerHTML = profile;

    //when profile renderer is called all posts and tasks get rendered
    document.getElementById("post_buffer").innerHTML = "";
    document.getElementById("cookingLog").innerHTML = "";
    document.getElementById("toDo").innerHTML = "";
    document.getElementById("not_buffer").innerHTML = "";

    render_post("post_buffer", data_json["posts"]);
    render_task(data_json["tasks"]);
}

//notification renderer
function render_notification(list) {
    //notification rendering also requires a @mention class and time class and images
    //this renderer excludes both of them

    //notification rendering also requires
    var i = 0;
    for(i = 0; i < list.length; i++)
    {
        data_json = list[i];
        var now = new Date().toTimeString();
        var not = '<p> <span class="circle-green"><img src="/static/images/tick.svg"></span><strong>' + data_json["sender"] + '</strong> ' + data_json["action"] + ' <strong>' + data_json["object"] + '</strong> <br> <span>' + now + '</span></p>';
        document.getElementById("not_buffer").insertAdjacentHTML("afterbegin", not);
    }


}