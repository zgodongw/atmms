var modal = document.getElementById('myModal');

// Get the button that opens the modal
var updatebtn = document.getElementById("myUpdateBtn");
var addbtn = document.getElementById("myAddBtn");
var logoutbtn = document.getElementById("myLogoutBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];


// When the user clicks the button, open the modal 


updatebtn.onclick = function() {
    modal.style.display = "block";
}

addbtn.onclick = function() {
    modal.style.display = "block";
}

logoutbtn.onclick = function() {
    modal.style.display = "block";
}


// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}