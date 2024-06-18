import { storage } from "./client_storage.js";

class ApiInteractor {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    async request(endpoint, method = 'GET', data = null) {
        const headers = {
            'Content-Type': 'application/json',
        };
        const token = storage.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            method: method,
            headers: headers,
        };

        if (data) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, config);
            const responseData = await response.json();
            if (!response.ok) {
                throw new Error(responseData.error || responseData.msg || 'API request failed');
            }

            return responseData;
        } catch (err) {
            return err;
        }
    }
}

class UserApi extends ApiInteractor {
    constructor(baseURL) {
        super(baseURL);
    }

    register(username, password) {
        return this.request('/register', 'POST', { username, password });
    }

    login(username, password) {
        return this.request('/login', 'POST', { username, password });
    }

    getAllUsers() {
        return this.request('/users', 'GET', null);
    }
}

class PostApi extends ApiInteractor {
    constructor(baseURL) {
        super(baseURL);
    }

    createPost(content) {
        return this.request('/posts', 'POST', { content });
    }

    getAllPosts() {
        return this.request('/posts', 'GET', null);
    }

    likePost(postId) {
        return this.request(`/posts/${postId}/like`, 'POST', null);
    }

    updatePost(postId, content) {
        return this.request(`/posts/${postId}`, 'PATCH', { "content":content });
    }

    replacePost(postId, content) {
        return this.request(`/posts/${postId}`, 'PUT', { content });
    }

    deletePost(postId) {
        return this.request(`/posts/${postId}`, 'DELETE', null);
    }
}

class CommentApi extends ApiInteractor {
    constructor(baseURL) {
        super(baseURL);
    }

    createComment(postId, content) {
        return this.request(`/posts/${postId}/comments`, 'POST', { content });
    }

    getComments(postId) {
        return this.request(`/posts/${postId}/comments`, 'GET', null);
    }
}

// Usage example:

const baseURL = 'http://localhost:5000';

const userApi = new UserApi(baseURL);
const postApi = new PostApi(baseURL);
const commentApi = new CommentApi(baseURL);

export function getApi(baseURL) {
    const api = {
        user: new UserApi(baseURL),
        post: new PostApi(baseURL),
        comment: new CommentApi(baseURL),
    };

    return api;
}

// Example usage
export async function example() {
    try {
        const api = getApi(baseURL);
        const tokenObj = await api.user.login("testuser", "password");
        storage.saveToken(tokenObj.access_token);

        console.log(await api.post.getAllPosts());
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// await example()
