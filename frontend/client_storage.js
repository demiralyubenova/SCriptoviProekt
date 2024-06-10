class Storage { // since the way of getting the token couls change in the future
    getToken() {
        const name = 'token=';
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookies = decodedCookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.indexOf(name) === 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }
        return "";
    }
    saveToken(token, days = 7) { // Added days parameter with default value
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = `token=${token};${expires};path=/`;
    }
}



export const storage = new Storage()


