//This script deals with logging in through social media APIs

//Linkedin API
function LinkedinAPI() 
{

    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        var response = JSON.parse(this.responseText);
        window.location.replace(response);
    }

    xhttp.open("GET", '/linkedinproxy');
    xhttp.send();
}