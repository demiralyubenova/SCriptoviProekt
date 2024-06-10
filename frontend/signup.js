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
        console.log("userObj", userObj);
        // Optionally, you might want to log the user in directly after signup or show a success message
        // Redirect or show the next page
    } catch (error) {
        console.error('Error:', error.message);
    }
});
