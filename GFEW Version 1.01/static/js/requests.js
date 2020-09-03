/*
    This script deals with sending and receiving requests from the server
    The methods of this script can be edited to include more data or functionality
*/

//notification update method
//this method is the receive gateway to the server
//  ->all get requests to fetch data from database (posts, tasks, classes) take place via this method
//  -> this method deploys long polling request method
function notification_update(self) {

    if(Notification.permission !== 'granted')
            {
                Notification.requestPermission();
            }


//one notification request for fetching posts, tasks, and classes and notifications
    var fetch = new XMLHttpRequest();
    fetch.onreadystatechange = function() {
        if(this.status == 200)
        {
                var response = JSON.parse(this.responseText);

                if(response["type"] == "posts_" + self)
                {
                    var holder = document.getElementById("post_buffer");
                    if(holder)
                    {
                        console.log("inside post renderer");
                        render_post("post_buffer", response["payload"]);
                    }
                }

               /* if(response["type"] == "tasks")
                {
                    var holder1 = document.getElementById("cookingLog");
                    var holder2 = document.getElementById("toDo");

                    if(holder1 || holder2)
                        {
                            render_task(response["payload"]);
                        }
                }*/

                if(response["type"] == "classes")
                {
                    var holder = document.getElementById("class_buffer");
                    if(holder)
                    {
                        render_class("class_buffer", response["payload"]);
                    }
                }

                if(response["type"] == "notifications")
                {
                    if(document.getElementById("not_buffer"))
                    {
                        render_notification(response["payload"]);

                            var nots = response["payload"];
                            var not = nots[0];
                            new Notification('GFEW Notification', {
                                icon: '/static/images/admin-login.jpg',
                                body: not["sender"] + " " + not["action"] + " " + not["object"]
                            });
                    }
                }

            fetch.open("GET", "/dashboard/notifications", true);
            fetch.setRequestHeader('Content-Type', 'application-json');
            fetch.send();
        }

        else if(this.status == 504)
        {
            fetch.open("GET", "/dashboard/notifications", true);
            fetch.setRequestHeader('Content-Type', 'application-json');
            fetch.send();
        }
    }

    fetch.open("GET", "/dashboard/notifications", true);
    fetch.setRequestHeader('Content-Type', 'application-json');
    fetch.send();




    //get request for posts
    /*var post = new XMLHttpRequest();
    post.onreadystatechange = function() {
        if(this.status == 200)
        {
            if(this.responseText)
            {
                var response = JSON.parse(this.responseText);

            var holder = document.getElementById("post_buffer");
                if(holder)
                {
                    render_post("post_buffer", response);

                    //long polling to keep updated
                    post.open("GET", "/dashboard/posts/action=get/"+self, true);
                    post.setRequestHeader("Content-Type", "application/json");
                    post.send();
                }
            }
        }
    }

    post.open("GET", "/dashboard/posts/action=get/"+self, true);
    post.setRequestHeader("Content-Type", "application/json");
    post.send();
    //--------------------------------------------------------

    //get request for tasks
    var task = new XMLHttpRequest();
    task.onreadystatechange = function() {
        if(this.status == 200)
        {
            if(this.responseText)
            {
                var response = JSON.parse(this.responseText);

                var holder1 = document.getElementById("cookingLog");
                var holder2 = document.getElementById("toDo");

                if(holder1 || holder2)
                {
                    render_task(response);

                    task.open("GET", window.location.href + "/tasks/get", true);
                    task.setRequestHeader("Content-Type", "application/json");
                    task.send();
                }
            }
        }
    }

    task.open("GET", window.location.href + "/tasks/get", true);
    task.setRequestHeader("Content-Type", "application/json");
    task.send();
    //-----------------------------------------------------------

    //get request for classes
    var Class = new XMLHttpRequest();
    Class.onreadystatechange = function() {
        if(this.status == 200)
        {
            if(this.responseText)
            {
                var response = JSON.parse(this.responseText);

                var holder = document.getElementById("class_buffer");
                if(holder)
                {
                    render_class("class_buffer", response);

                    Class.open("GET", "/dashboard/classes/action=get", true);
                    Class.setRequestHeader("Content-Type", "application/json");
                    Class.send();
                }

            }

        }
    }

    Class.open("GET", "/dashboard/classes/action=get", true);
    Class.setRequestHeader("Content-Type", "application/json");
    Class.send();
    //----------------------------------------------------------------------

    //request to get miscellaneous notifications

    if(Notification.permission !== 'granted')
            {
                Notification.requestPermission();
            }
    var not = new XMLHttpRequest();
    not.onreadystatechange = function() {
        if(this.status == 200)
        {
            if(this.responseText)
            {
                var response = JSON.parse(this.responseText);

                if(document.getElementById("not_buffer"))
                {
                    render_notification(response);

                    if(response)
                    {
                    new Notification('GFEW Notification', {
                            icon: '/static/images/admin-login.jpg',
                            body: response[0]["sender"] + response[0]["action"] + response[0]["object"]
                        });

                    }
                    

                not.open("GET", window.location.href + "/notifications", true);
                not.setRequestHeader('Content-Type', 'application-json');
                not.send();
                }
            }
        }
    }

    not.open("GET", window.location.href + "/notifications", true);
    not.setRequestHeader('Content-Type', 'application-json');
    not.send();*/
}


//create Post method
function createPost(body) 
{
    //This part will deal with encoding any image or media to send as a request
    //------------------------------------------------------------------------

    //This part deals with sendind text to the database
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/dashboard/posts/action=post", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    var date = new Date().toDateString();
    query = JSON.stringify({
        "body": body["text"],
        "media": "",
        "date": date,
    });
    xhttp.send(query);
}


//request to get basic profile info
function profile_get() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.status == 200)
        {
            if(this.responseText)
            {
                var response = JSON.parse(this.responseText);
                render_profile(response);
            }
            
        }
    }

    xhttp.open("GET", window.location.href + "/get", true);
    xhttp.setRequestHeader("Content-Type", "application-json");
    xhttp.send();
}

//request to get posts for wall
function wall() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.status == 200)
        {
            if(this.responseText)
            {
                var response = JSON.parse(this.responseText);
                document.getElementById("post_buffer").innerHTML = "";
                render_post("post_buffer", response);
            }
            
        }
    }

    xhttp.open("GET", "/dashboard/wall/get", true);
    xhttp.setRequestHeader("Content-Type", "application-json");
    xhttp.send();
}