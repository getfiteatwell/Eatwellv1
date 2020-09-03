

function validate_fname(fname)
{
    //looking for empty field
    if((fname.value == "")||(/^.+\s.+$/g.test(fname.value)))
    {
        document.getElementById("validate-fname").innerHTML = "First name cannot be empty";
        return false;
    }

    else
    {
        document.getElementById("validate-fname").innerHTML = "";
        return true;
    }
}

function validate_lname(lname)
{
    //looking for empty field
    if((lname.value == "")||(/^.+\s.+$/g.test(lname.value)))
    {
        document.getElementById("validate-lname").innerHTML = "Last name cannot be empty";
        return false;
    }

    document.getElementById("validate-lname").innerHTML = "";
    return true;

}

function validate_email(email)
{
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

    //looking for empty field
    if((email.value == "")||(/^.+\s.+$/g.test(email.value)))
    {
        document.getElementById("validate-email").innerHTML = "Email cannot be empty";
        return false;
    }

    //looking for invalid email
    if(reg.test(email.value) == false)
    {
        document.getElementById("validate-email").innerHTML = "Invalid email";
        return false;
    }
    
    document.getElementById("validate-email").innerHTML = "";
    return true;
}

function validate_phone(phone)
{
    //looking for empty field
    if((phone.value == "")||(/^.+\s.+$/g.test(phone.value)))
    {
        document.getElementById("validate-phone").innerHTML = "Mobile number cannot be empty";
        return false;
    }

    //looking for invalid number
    if(/^\d*$/.test(phone.value) == false)
    {
        document.getElementById("validate-phone").innerHTML = "invalid mobile number";
        return false;
    }

    else
    {
        document.getElementById("validate-phone").innerHTML = "";
        return true;
    }

}

function validate_password(password)
{
    //looking for empty field
    if((password.value == "")||(/^.+\s.+$/g.test(password.value)))
    {
        document.getElementById("validate-password").innerHTML = "Password cannot be empty";
        return false;
    }

    else
    {
        document.getElementById("validate-password").innerHTML = "";
        return true;
    }
}

function validate_confirmpassword(cpassword)
{
    //looking for empty field
    if((cpassword.value == "")||(/^.+\s.+$/g.test(cpassword.value)))
    {
        document.getElementById("validate-cpass").innerHTML = "Confirm password cannot be empty";
        return false;
    }

    if(cpassword.value != document.getElementById("password").value)
    {
        document.getElementById("validate-cpass").innerHTML = "Entered invalid password";
        return false;
    }

    else
    {
        document.getElementById("validate-cpass").innerHTML = "";
        return true;
    }
}

function validate_terms(terms)
{
    var checked = false;
    if(terms.checked == true)
    {
        checked = true;
    }

    return checked;
}

function Validate_signup() 
{
    var form = document.getElementById("signup_form");
    if((validate_fname(form["fname"]))&&(validate_lname(form["lname"]))&&(validate_email(form["email"]))&&(validate_phone(form["phone"]))&&(validate_confirmpassword(form["passwordconfirm"]))&&(validate_terms(form["termscheck"])))
    {
        document.getElementById("signup_form").submit();
    }
}