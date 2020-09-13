function auth_get(username)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.status == 200 && this.readyState == 4)
        {
            var response = JSON.parse(this.responseText);
            console.log(response);

            var _id = document.getElementById("get-text").value;
            var query = document.getElementById("query-get").value;
            var endpoint = document.getElementById("endpoint-get").value;
            get(query, endpoint, response["access_token"], _id);
        }
    }
    var url = encodeURI("http://localhost:5000/api/auth?username=" + username);
    xhttp.open("GET", url);
    xhttp.setRequestHeader("Sec-Fetch-Site", "cross-origin")
    xhttp.send();
}


function auth_post(username)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.status == 200 && this.readyState == 4)
        {
            var response = JSON.parse(this.responseText);
            console.log(response);

            var _id = document.getElementById("post-text").value;
            var query = document.getElementById("query-post").value;
            var endpoint = document.getElementById("endpoint-post").value;
            var json = JSON.stringify({"title": document.getElementById("title").value,
                                        "description": document.getElementById("description").value,
                                        "due_date": document.getElementById("due_date").value,
                                        "text": document.getElementById("text").value,
                                        "media": [document.getElementById("media")]});
            post(query, endpoint, response["access_token"], _id, json);
        }
    }
    var url = encodeURI("http://localhost:5000/api/auth?username=" + username);
    xhttp.open("GET", url);
    xhttp.setRequestHeader("Sec-Fetch-Site", "cross-origin")
    xhttp.send();
}

function get(query, endpoint, token, _id)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.status == 200 && this.readyState == 4)
        {
            console.log(JSON.parse(this.responseText));
        }
    }

    var url = encodeURI("http://localhost:5000/api/get/" + endpoint + "?_id=" + _id + "&query=" + query + "&access_token=" + token);
    xhttp.open("GET", url);
    xhttp.setRequestHeader("Sec-Fetch-Site", "cross-origin")
    xhttp.send();
}

function post(query, endpoint, token, _id, json)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(this.status == 200 && this.readyState == 4)
        {
            console.log(JSON.parse(this.responseText));
        }
    }

    var url = encodeURI("http://localhost:5000/api/post/" + endpoint + "?_id=" + _id + "&query=" + query + "&access_token=" + token);
    xhttp.open("POST", url);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.setRequestHeader("Sec-Fetch-Site", "cross-origin")
    xhttp.send(json);
}