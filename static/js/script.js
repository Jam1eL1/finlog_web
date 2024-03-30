// JavaScript function to toggle the visibility of the form
function toggleFormWrapper() {
    var save_form = document.getElementById("saveForm");
    var delete_form = document.getElementById("deleteForm");
     // Toggle Save Form
    if (save_form.style.display === "none") {
    save_form.style.display = "block";
    } else {
        save_form.style.display = "none";
    }

    // Toggle Delete Form
    if (delete_form.style.display === "none") {
        delete_form.style.display = "block";
    } else {
        delete_form.style.display = "none";
    }
    }


function confirmDelete() {
    return confirm("Your post has been deleted");
}

// function showMessage() {
//     alert('Hello, world!');
// }

// Call the function when the page loads
// window.onload = function() {
//     showMessage();
// };