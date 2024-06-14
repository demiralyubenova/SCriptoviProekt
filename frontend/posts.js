import { getApi } from "./api.js";
import { storage } from "./client_storage.js";

const baseURL = 'http://localhost:5000';
const api = getApi(baseURL);
console.log("loaded js");

// HTML constructor for a post renderer
function createPostElement(post) {
    const postElement = document.createElement('div');
    postElement.className = 'post';

    const contentElement = document.createElement('p');
    contentElement.textContent = post.content;
    postElement.appendChild(contentElement);

    const likesElement = document.createElement('p');
    likesElement.textContent = `Likes: ${post.likes}`;
    postElement.appendChild(likesElement);

    const likeButton = document.createElement('button');
    likeButton.textContent = 'Like';
    likeButton.addEventListener('click', async () => {
        try {
            const token = storage.getToken(); // Assumes the token is stored in localStorage
            const response = await api.post.likePost(post.id, token);
            likesElement.textContent = `Likes: ${response.likes}`;
        } catch (error) {
            console.error('Error liking post:', error.message);
        }
    });
    postElement.appendChild(likeButton);

    return postElement;
}

// Function to load and display posts
async function loadPosts() {
    try {
        const token = storage.getToken(); // Assumes the token is stored in localStoragezz
        const posts = await api.post.getAllPosts(token);

        const postsContainer = document.getElementById('posts-container');
        postsContainer.innerHTML = ''; // Clear previous posts

        posts.forEach(post => {
            const postElement = createPostElement(post);
            postsContainer.appendChild(postElement);
        });
    } catch (error) {
        console.error('Error loading posts:', error.message);
    }
}

// Function to handle new post submission
async function handleCreatePost(event) {
    event.preventDefault();
    const content = document.getElementById('post-content').value;

    if (content.trim() === '') {
        alert('Post content cannot be empty.');
        return;
    }

    try {
        const token = storage.getToken(); // Assumes the token is stored in localStorage
        const newPost = await api.post.createPost({ content }, token);

        const postsContainer = document.getElementById('posts-container');
        const postElement = createPostElement(newPost);
        postsContainer.prepend(postElement); // Add new post at the top
            
        document.getElementById('create-post-form').reset(); // Clear the form
    } catch (error) {
        console.error('Error creating post:', error.message);
    }
}

// Example function to initialize the app
async function initApp() {
    try {
        // Perform login and registration here if needed
        await loadPosts();
    } catch (error) {
        console.error('Error initializing app:', error.message);
    }
}

// Initialize the app
initApp().catch(error => console.error('Error in initApp:', error.message));

// Add event listener for creating posts
document.getElementById('create-post-form').addEventListener('submit', handleCreatePost);

// Add some styling to the posts
const style = document.createElement('style');
style.textContent = `
    #create-post-container {
        margin-bottom: 20px;
    }
    .post {
        border: 1px solid #ccc;
        padding: 16px;
        margin-bottom: 16px;
        border-radius: 8px;
        box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
        background-color: #fff;
    }
    .post p {
        margin: 8px 0;
    }
    .post button {
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        background-color: #007BFF;
        color: #fff;
        cursor: pointer;
    }
    .post button:hover {
        background-color: #0056b3;
    }
`;
document.head.appendChild(style);
