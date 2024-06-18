import { getApi } from "./api.js";
import { storage } from "./client_storage.js";

const baseURL = 'http://localhost:5000';
const api = getApi(baseURL);
console.log("loaded js");

// HTML constructor for a post renderer
function createPostElement(post) {
    const postElement = document.createElement('div');
    postElement.className = 'post';
    postElement.dataset.postId = post.id;

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
            const response = await api.post.likePost(post.id);
            likesElement.textContent = `Likes: ${response.likes}`;
        } catch (error) {
            console.error('Error liking post:', error.message);
        }
    });
    postElement.appendChild(likeButton);

    const redactButton = document.createElement('button');
    redactButton.textContent = 'Redact';
    redactButton.addEventListener('click', () => {
        const newContent = prompt('Edit your post:', post.content);
        if (newContent !== null) {
            updatePost(post.id, newContent);
        }
    });
    postElement.appendChild(redactButton);

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.addEventListener('click', async () => {
        if (confirm('Are you sure you want to delete this post?')) {
            deletePost(post.id);
        }
    });
    postElement.appendChild(deleteButton);

    return postElement;
}

async function loadPosts() {
    try {
        const posts = await api.post.getAllPosts();
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

async function handleCreatePost(event) {
    event.preventDefault();
    const content = document.getElementById('post-content').value;

    if (content.trim() === '') {
        alert('Post content cannot be empty.');
        return;
    }

    try {
        const newPost = await api.post.createPost(content);
        const postsContainer = document.getElementById('posts-container');
        const postElement = createPostElement(newPost);
        postsContainer.prepend(postElement); // Add new post at the top

        document.getElementById('create-post-form').reset(); // Clear the form
    } catch (error) {
        console.error('Error creating post:', error.message);
    }
}

async function updatePost(postId, content) {
    try {
        await api.post.updatePost(postId, content);
        loadPosts();
    } catch (error) {
        console.error('Error updating post:', error.message);
    }
}

async function deletePost(postId) {
    try {
        await api.post.deletePost(postId);
        loadPosts();
    } catch (error) {
        console.error('Error deleting post:', error.message);
    }
}

async function initApp() {
    try {
        await loadPosts();
    } catch (error) {
        console.error('Error initializing app:', error.message);
    }
}

document.getElementById('create-post-form').addEventListener('submit', handleCreatePost);

initApp().catch(error => console.error('Error in initApp:', error.message));
