//This script deals with admin tools including creating classes, tasks, and sending reminders
// info function to fetch basic server info
function info()
{
    //total accounts
    var acc = new XMLHttpRequest();
    acc.onreadystatechange = function() {
        if(this.status == 200)
        {
            var response = JSON.parse(this.responseText);

            document.getElementById("total_accounts").innerHTML = response["total"];
            document.getElementById("active_accounts").innerHTML = response["active"];

            acc.open("GET", "server's address", true);
            acc.setRequestHeader('Content-Type', 'application-json');
            acc.send(JSON.stringify({"query": "getInfo"}));
        }

    }

    acc.open("GET", "server's address", true);
    acc.setRequestHeader('Content-Type', 'application-json');
    acc.send(JSON.stringify({"query": "getInfo"}));
    //--------------------------------------------------------------
}

//function to create a class
function createClass(data_json)
{
    var acc = new XMLHttpRequest();
    acc.open("POST", "server's address", true);
    acc.setRequestHeader('Content-Type', 'application-json');
    var query = JSON.stringify({
        "query": "createClass",
        "title": data_json["title"],
        "description": data_json["description"]
    });
    acc.send(query);
}

//function to create a task
function createTask(data_json)
{
    var acc = new XMLHttpRequest();
    acc.open("POST", "server's address", true);
    acc.setRequestHeader('Content-Type', 'application-json');
    var query = JSON.stringify({
        "query": "createTask",
        "title": data_json["title"],
        "description": data_json["description"],
        "type": data_json["type"],
        "_id": data_json["_id"]
    });
    acc.send(query);
}