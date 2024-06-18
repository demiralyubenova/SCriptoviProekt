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
        const res = await api.user.register(username, password);
        console.log("res", res);
        if(!(res.id)){ // check if the response is succesful
        alert(JSON.stringify(res.error)) 
        console.log("jijiij")
        return
    }  
       window.location.href="/frontend/signin.html"

    } catch (error) {
        console.error('Error:', error.message);
    }
});
