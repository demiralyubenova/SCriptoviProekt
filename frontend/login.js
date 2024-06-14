import { getApi } from './api.js';
import { storage } from './client_storage.js';
document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    console.log('Username:', username);
    console.log('Password:', password);

    const baseURL = 'http://localhost:5000';
    const api = getApi(baseURL);
    console.log(api)

    try {
        const tokenObj = await api.user.login(username, password);
        console.log("tokenObj", tokenObj);
        // Assuming you have a method to save the token
        storage.saveToken(tokenObj.access_token);
        // Redirect 
        window.location.href="/frontend/posts.html"
    } catch (error) {
        console.error('Error:', error.message);
    }
});
