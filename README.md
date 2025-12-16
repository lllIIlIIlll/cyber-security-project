## Cyber Security Base 2025 Project

#### LINK: https://github.com/lllIIlIIlll/cyber-security-project

**The flaws in the project are from the OWASP top 10, 2017 edition.**

---

### INSTRUCTIONS

##### How to create a basic user:

Type this command to terminal:

```sh
python3 manage.py shell
```

Copy and paste the following:

```python
from django.contrib.auth.models import User

User.objects.create_user(username='user', password='password123')

exit()
```

###### How to create a superuser:

python3 manage.py createsuperuser

---

### FLAW 1:

https://github.com/lllIIlIIlll/cyber-security-project/blob/b688093595ce52d06873aa821fa0ca6040e41a24/blog/views.py#L17

**Description:**

Cross-site request forgery (CSRF) flaw. The backend does not verify the origin of POST requests. This allows the attacker to post on behalf of an authenticated user. The flaw happens because CSRF protection is disabled from the view handling post creation using @csrf_exempt.

**Demo:**

1. Create a user and log into the app.

2. Start a separate server in the demo_pages folder with command:

```sh
python3 -m http.server 5000.
```

3. While still logged in, open a new tab and visit: http://127.0.0.1:5000/csrf_demo.html.

4. Click the "claim prize"-button.

5. Now you can see the latest post created by the attacker without user doing anything.

**How to fix it:**

In the views.py file, remove the @csrf_exempt so that Django’s built in CSRF protection is active.

### FLAW 2:

https://github.com/lllIIlIIlll/cyber-security-project/blob/b688093595ce52d06873aa821fa0ca6040e41a24/blog/templates/blog/index.html#L40

**Description:**

Cross-site scripting (XSS) flaw. The post creation form does not sanitize the user input, and the input is stored and rendered without proper escaping. This happens because the template uses the |safe filter that allows the attacker to execute HTML or JavaScript through the post creation form.

**Demo:**

1. Log into the app.

2. Create a post with the following content:

```html
<script>
  alert('XSS in action')
</script>
```

3. You should immediately see the alert pop up.

4. Log in with a different user to check that the injected script executes for other users as well.

**How to fix it:**

In the views.py, remove "|safe" from the end of the post.content variable, so that Django escapes user generated content by default.

### FLAW 3:

https://github.com/lllIIlIIlll/cyber-security-project/blob/b688093595ce52d06873aa821fa0ca6040e41a24/blog/views.py#L37

**Description:**

Broken access control flaw. The backend does not verify ownership when deleting posts which results in a normal user being able to delete posts created by other users, even though only the post author or a superuser should be allowed to do so. The application only checks that the user is authenticated but it lacks proper authorization at the backend.

**Demo:**

1. Make two users (you can use the ones created earlier).

2. Using user1 log in and create a post, then log out.

3. Using user2 log in and create a post, then delete it.

4. Open browser developer tools and go to the network tab.

5. Delete user2’s own post normally, select the deletion request and copy the CSRF token from the request.

6. Switch to the browser console and copy paste the following POST request that deletes user1’s post by changing the post id (check the id from the database if necessary) in the URL:

```python
fetch("http://127.0.0.1:8000/delete_post/POST_ID/", {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
    "X-CSRFToken": "YOUR_CSRF_TOKEN"
    }
});
```

7. Verify that the post gets deleted.

**How to fix it:**

In the views.py, uncomment the authorization check that verifies that only the post author and superuser can delete posts. This ensures that the deletions are restricted at the backend level and prevent unauthorized users from deleting posts.

### FLAW 4:

https://github.com/lllIIlIIlll/cyber-security-project/blob/b688093595ce52d06873aa821fa0ca6040e41a24/blog/views.py#L54

**Description:**

SQL injection flaw. The attacker can perform SQL injection through the search input field. The search function uses Django’s raw() method with string formatting that allows the attacker to modify the SQL query arbitrarily. The demonstration below alters the WHERE clause of the SQL query, causing the database to return all posts instead of only matching ones. In a real app and more complex database this kind of flaw could be used for much worse, for example to return posts that user should not be able to access.

**Demo:**

1. Copy and paste: “' OR 1=1 --” to the search box on top of the page and click search.

2. You should see all the blog posts in the database regardless of their content.

**How to fix it:**

In the views.py, comment out the unsafe raw() SQL query and uncomment the safe method that is above the linked line. The safe method prevents the SQL injection automatically.

### FLAW 5:

https://github.com/lllIIlIIlll/cyber-security-project/blob/b688093595ce52d06873aa821fa0ca6040e41a24/blog/views.py#L60

**Description:**

Sensitive data exposure flaw. The application leaks the user’s session id by passing it from backend to frontend. The session id is then embedded in the HTML and visible to anyone accessing the page. This kind of security flaw puts the user in danger of session hijacking and unauthorized account access whether the attacker is scraping DOM content with a browser extension or simply looking at the user’s screen.

**Demo:**

1. Log into the app.

2. Click on “profile” link at the top of the page.

3. Session id can be seen on the profile page.

4. Anyone with access to the token could hijack the session.

**How to fix it:**

Remove session_id from the render object in views.py as there is no point to ever expose it manually. Comment out the line: https://github.com/lllIIlIIlll/cyber-security-project/blob/b688093595ce52d06873aa821fa0ca6040e41a24/blog/templates/blog/profile.html#L11 that tries to render it.
