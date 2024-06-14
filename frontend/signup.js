// signup.js
import { getApi } from './api.js';

document.getElementById('signupForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    console.log('Username:', username);
    console.log('Password:', password);

    const baseURL = 'http://localhost:5000';
    const api = getApi(baseURL);
    console.log(api)

    try {
        const userObj = await api.user.register(username, password);
        alert(JSON.stringify(userObj))
        console.log("userObj", userObj);

        window.location.href = "/frontend/signin.html"

        
    } catch (error) {
        console.error('Error:', error.message);
    }
});
