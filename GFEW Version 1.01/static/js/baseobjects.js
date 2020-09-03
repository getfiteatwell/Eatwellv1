/*      GFEW base classes iteration 1        

        notes:
        -> base classes are designed to streamline development and ease the compactability
            of code with other verisons

        -> Object to HTML template renderer is an inbuilt layer and not a seperate one
*/

//-------------------------------------------------------------------------------------------------

//posts class
class Posts {
    get() {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        //if request is successful
        if (this.status == 200) {
            var response = JSON.parse(this.responseText);

            //render posts to html
            var holder = document.getElementById("post_buffer");
            holder.innerHTML = "";
            var i = 0;
            console.log(response.length);
            for(i = response.length - 1; i >= 0; i--)
            {
                var temp = response[i];
                var post = document.createElement("div");
                var user = document.createElement("p");
                user.setAttribute("class", "user-name")
                var date = document.createElement("span");
                var username = document.createElement("strong");
                username.innerHTML = temp["username"]
                date.innerHTML = temp["date"].toString();
                user.appendChild(username);
                user.appendChild(date)
                post.appendChild(user);

                var body = document.createElement("p");
                body.innerHTML = temp["body"];
                var image = document.createElement("img");
                image.setAttribute("src", temp["pfpURL"]);
                post.appendChild(body);
                post.appendChild(image);

                post.setAttribute("class", "discussion-comment");
                holder.appendChild(post);
            }

        }

        else 
        {
            var holder = document.getElementById("post_buffer");
            holder.innerHTML = "There are no posts"
        }
}
        xhttp.open("GET", window.location.href + "/posts", true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send();
    }
}

//profile class
class Profile {
    get() {
        //making a request to get the profile from database
        //Fetches and sets profile creds from database
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        //if request is successful
        if (this.status == 200) {
            var response = JSON.parse(this.responseText);


        //          base profile renderer
        var profile = document.getElementById("profile").children;
        profile[0].src = response["pfpURL"];
        profile[1].innerHTML = response["username"];
        profile[2].innerHTML = "";
        var subprofile = profile[3].children;
        subprofile[0].innerHTML = response["meals"] + "<br><span>Meals</span>";
        subprofile[1].innerHTML = response["followers"] + "<br><span>Followers</span>";
        subprofile[2].innerHTML = response["following"] + "<br><span>Following</span>"

        //set level 
        var level = document.getElementById("level").children;
        var sublevel = level[0].children;
        if(response["level"] == "beginner")
        {
            sublevel[0].setAttribute("class", "active");
            sublevel[1].classList.remove("active");
            sublevel[2].classList.remove("active");
        }
        if(response["level"] == "intermediate")
        {
            sublevel[1].setAttribute("class", "active");
            sublevel[0].classList.remove("active");
            sublevel[2].classList.remove("active");
        }
        if(response["level" == "professional"])
        {
            sublevel[2].setAttribute("class", "active");
            sublevel[1].classList.remove("active");
            sublevel[0].classList.remove("active");
        }
        //----------------------------------------
        //          get posts
            //making a request to get the posts from database
            //Fetches and sets posts creds from database
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
            //if request is successful
            if (this.status == 200) {
                var response = JSON.parse(this.responseText);

                //render posts to html
                var holder = document.getElementById("post_buffer");
                holder.innerHTML = "";
                var i = 0;
                for(i = response.length - 1; i >= 0; i--)
                {
                    var temp = response[i];
                    var post = document.createElement("div");
                    var user = document.createElement("p");
                    user.setAttribute("class", "user-name")
                    var date = document.createElement("span");
                    var username = document.createElement("strong");
                    username.innerHTML = temp["username"]
                    date.innerHTML = temp["date"].toString();
                    user.appendChild(username);
                    user.appendChild(date)
                    post.appendChild(user);

                    var body = document.createElement("p");
                    body.innerHTML = temp["body"];
                    var image = document.createElement("img");
                    image.setAttribute("src", temp["pfpURL"]);
                    post.appendChild(body);
                    post.appendChild(image);

                    post.setAttribute("class", "discussion-comment");
                    holder.appendChild(post);
                }

            }

            else 
            {
                var holder = document.getElementById("post_buffer");
                holder.innerHTML = "There are no posts"
            }
    }
            xhttp.open("GET", "/dashboard/profile/id=" + response["_id"] + "/posts", true);
            xhttp.setRequestHeader("Content-Type", "application/json");
            xhttp.send();

        }


        //get tasks for cooking log
        xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        //if request is successful
        if (this.status == 200) {
            var response = JSON.parse(this.responseText);

            //render tasks to html
            document.getElementById("cookingLog").innerHTML = "";
            document.getElementById("toDo").innerHTML = "";
            var i = 0;
            for(i = response.length - 1; i >= 0; i--)
            {
                var obj = response[i];
                if(obj["type"] == "cookingLog")
                {
                    var taskHTML = '<div class="task-card">\
                    <div class="row">\
                        <div class="col-md-2 col-2">\
                            <input type="checkbox" id="fruit' + i.toString() + '" name="fruit-' + i.toString() + '" value="Apple">\
                            <label for="fruit' + i.toString() + '"></label>\
                        </div>\
                        <div class="col-md-10 col-10">\
                            <p>' + obj["title"] + '</p>\
                            <div class="user-type">\
                                <img src="' + obj["pfpURL"] + '"><span class="pill pill-blue">Me</span>\
                            </div>\
                        </div>\
                    </div>\
                </div>';
                document.getElementById("cookingLog").insertAdjacentHTML("beforeend", taskHTML);
                }

                else
                {
                    var taskHTML = '<div class="task-card">\
                    <div class="row">\
                        <div class="col-md-2 col-2">\
                            <input type="checkbox" id="fruit' + i.toString() + '" name="fruit-' + i.toString() + '" value="Apple">\
                            <label for="fruit' + i.toString() + '"></label>\
                        </div>\
                        <div class="col-md-10 col-10">\
                            <p>' + obj["title"] + '</p>\
                            <div class="user-type">\
                                <img src="' + obj["pfpURL"] + '"><span class="pill pill-blue">Me</span>\
                            </div>\
                        </div>\
                    </div>\
                </div>';
                document.getElementById("toDo").insertAdjacentHTML("beforeend", taskHTML);
                }
                }


            }

        else 
        {
            document.getElementById("tcookingLog").insertAdjacentHTML("beforeend", "There are no tasks");
            document.getElementById("toDo").insertAdjacentHTML("beforeend", "There are no tasks");
        }
}
        xhttp.open("GET", window.location.href + "/tasks/get", true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send();

}
        xhttp.open("GET", "/dashboard/profile/id=self", true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send();





    }

    makePost() {
        var post_body = document.getElementById("postBox").value;
        var post_date = new Date().toDateString();
        var url = this.pfpURL
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if(this.status == 200)
            {
                var response = JSON.parse(this.responseText);
                var holder = document.getElementById("post_buffer");
                holder.innerHTML = "";
                var post = document.createElement("div");
                var user = document.createElement("p");
                user.setAttribute("class", "user-name")
                var date = document.createElement("span")
                date.innerHTML = response["date"]
                user.appendChild(date);
                post.appendChild(user);

                var body = document.createElement("p");
                body.innerHTML = response["body"];
                var image = document.createElement("img");
                image.setAttribute("src", response["pfpURL"]);
                post.appendChild(body);
                post.appendChild(image);

                post.setAttribute("class", "discussion-comment");
                holder.appendChild(post);
            }
        }
        xhttp.open("POST", "/dashboard/post/action=post", true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        var query = JSON.stringify({"body": post_body, "date": post_date});
        xhttp.send(query);
    }


}

class Class {
    get() {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        //if request is successful
        if (this.status == 200) {
            var response = JSON.parse(this.responseText);

            //render posts to html
            var holder = document.getElementById("class_buffer");
            holder.innerHTML = "";
            var i = 0;
            console.log(response.length);
            for(i = response.length - 1; i >= 0; i--)
            {
                var temp = response[i];
                var post = document.createElement("div");
                var user = document.createElement("a");
                user.setAttribute("href", "/class/id=" + temp["_id"]);
                user.setAttribute("class", "user-name")
                var date = document.createElement("span");
                var username = document.createElement("strong");
                username.innerHTML = temp["title"]
                user.appendChild(username);
                post.appendChild(user);

                var body = document.createElement("p");
                body.innerHTML = temp["body"];
                post.appendChild(body);

                post.setAttribute("class", "discussion-comment");
                holder.appendChild(post);
            }

        }

        else 
        {
            var holder = document.getElementById("class_buffer");
            holder.innerHTML = "There are no posts"
        }
}
        xhttp.open("GET", "/dashboard/classes/action=get", true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send();
    }
}