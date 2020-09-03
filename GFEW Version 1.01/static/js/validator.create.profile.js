function validate_username(username)
{
    //checking for empty field
    if((username.value == "")||(/^.+\s.+$/g.test(username.value)))
    {
        document.getElementById("validate-username").innerHTML = "Username cannot be empty";
        return false;
    }

    else
    {
        var xhttp = new XMLHttpRequest();
        var status = false;

        var promise = new Promise(function(resolve, reject) {
            xhttp.onreadystatechange = function() {
                var response = JSON.parse(this.responseText);
                if(response)
                {
                    resolve(response);
                }
                else
                {
                    reject(response);
                }
            }
        });

        promise.then(function(response) {
            if(response == true)
            {
                document.getElementById("validate-username").innerHTML = "Username already exists";
                status = false;
            }
        });

        xhttp.open("POST", "/profile/create-profile/validate", true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(JSON.stringify({"username": username.value}));

        return status;
    }
}

function Validate_profile()
{
    var form = document.getElementById("create-profile");
    if((document.getElementById("validate-username").innerHTML != "Username already exists"))
    {
        form.submit();
    }
}