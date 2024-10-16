// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.14.0/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.14.0/firebase-auth.js";
import { createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.14.0/firebase-auth.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// function myname(){
//     var firstName=document.getElementById('fname').value;
//     var lastName=document.getElementById('lname').value;
//     var username=document.getElementById('rusername').value;
//     var password=document.getElementById('rpassword').value;

//     console.log(firstName);
//     console.log(lastName);
//     console.log(username);
//     console.log(password);
// }

const firebaseConfig = {
    apiKey: "AIzaSyA7UXw_IrB70J38jY1uhQh3l0G--fZfhOk",
    authDomain: "diapredict-24d55.firebaseapp.com",
    projectId: "diapredict-24d55",
    storageBucket: "diapredict-24d55.appspot.com",
    messagingSenderId: "385589653226",
    appId: "1:385589653226:web:e010447d5e12519d0ff193"
};


//Initialize Firebase

const app = initializeApp(firebaseConfig);
console.log(app)

// console.log(app);
const auth = getAuth();


//----- New Registration code start	  
document.getElementById("signup_btn").addEventListener("click", function () {
    var email = document.getElementById("email").value;
    var password = document.getElementById("pass").value;
    //For new registration
    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Signed in 
            const user = userCredential.user;
            console.log(user);
            alert("Registration successfully!!");
            // ...
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            // ..
            console.log(errorMessage);
            alert(error);
        });
});
//----- End

document.getElementById("login_btn").addEventListener("click", function () {
    var email = document.getElementById("login-email").value;
    var password = document.getElementById("login-password").value;

    signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
        const user = userCredential.user;
        console.log(user);
        alert(user.email + " Login successfully!!!");
        // Redirect to the Flask dashboard after a successful login
        window.location.href = "http://192.168.50.179:5000/dashboard"; // Make sure this URL matches your Flask route
    })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            console.log(errorMessage);
            alert(errorMessage);
        });
});