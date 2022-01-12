function validateForm() {
    window.alert(getElementById("username").value);
    var result = true;

    var enteredUsenname = document.getElementById("username").value;

    var enteredPassword = document.getElementById("password").value;

    var selectedoption = document.getElementById("loginas");

    var patt = /[abc]/;

    if (enteredUsenname.length < 5) {
        result = false;
        alert("Username must minimmum 5 charecter length");
    }

    if (!patt.test(enteredPassword)) {
        result = false;
        alert("password must be 4 char length abc");
    }

    if (selectedoption.selectedIndex == 0) {
        result = false;
        alert("please select an option..");
    }

    return result;


}