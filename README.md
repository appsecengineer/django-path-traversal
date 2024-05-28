# Path Traversal With Django

Hey AppSecEngineer,

Welcome to the **Attack and Defense Path Traversal With Django** Course - The **attack** subject

Let's delve into the realm of Path Traversal attacks and understand the nuances of exploiting vulnerabilities in web applications.

## What is Path Traversal?

Path Traversal attacks, also known as Directory Traversal or ../ (dot dot slash) attacks, occur when an attacker exploits the inadequate validation of user-supplied input to navigate through the file system directories.

By manipulating file paths, an attacker aims to access files and directories that are outside the intended scope of the web application. This attack is particularly potent when web applications dynamically generate file paths based on user input without implementing proper security measures.

Exploiting Path Traversal, an attacker can access sensitive files, configuration files, or even execute arbitrary code on the server, depending on the level of vulnerability present in the web application.

## Path Traversal attacks unfold in the following manner

### Input Validation

The attack commences when untrusted user input is accepted by the web application, often in the form of file or directory names.

### Construction of File Paths

The attacker manipulates the input to construct file paths that go beyond the intended scope, aiming to access unauthorized files or directories.

### Unauthorized Access

The crafted file paths are used to access files and directories outside the expected boundaries, potentially exposing sensitive information or compromising the integrity of the web application.

### Impact of Path Traversal

The consequences of a successful Path Traversal attack can range from unauthorized access to critical system files to the execution of malicious code on the server. Attackers may obtain sensitive data, such as configuration files, passwords, or other confidential information.

---

## Let us Start the DIY Attack Lab

Let us start the vulnerable application and perform a path traversal attack against it.

- Provision the lab and then navigate to `/root/django-path-traversal-course`
- Run the command `docker-compose up -d`. This would start our application at `****.appsecengineer.training` at port `8880`. (http://****.appsecengineer.training:8880)
`****.appsecengineer.training` is your Lab Instance URL.
- We are greeted by an application that looks like an image fetcher i.e we provide a name of the image which exists within the django applications `static/images` folder.
- There exists an image called `cat.jpg` , so let us enter the value and hit submit. We see an image of the cat
- If we look closely this value is submitted to the application via the  `filename` GET parameter. We can assume that this value is being appended to a local path within the application

Enter the below in your browser.

>Note: Replace **** with your lab instance url below

```txt
http://*****.appsecengineer.training:8880/image/fetch_image/?filename=cat.jpg
```

### Let us try a path traversal payload

Now as an attacker, we can try

- An absolute path traversal payload (`/etc/passwd`)
- Or we can choose to climb up the directory structure (`../../../../../../etc/passwd`)

Entering either of the above payload successfully retrieves the `/etc/passwd` file!

>Do attempt to retrieve the source code of the application by playing with the directory structure!

---

Now that we have successfully exploited the application against a path traversal attack. Let us now figure out where the application went wrong.

## Vulnerable Code Investigation

- Open `/root/django-path-traversal-course/image_app/views.py`, we see the below code

```py
    # image_app/views.py

    from django.shortcuts import render
    from django.http import HttpResponse
    from django.conf import settings
    import mimetypes
    import os


    def home(request):
        return render(request, 'home.html')

    def fetch_image(request):
        param = request.GET.get('filename')
        file_path = os.path.join(settings.BASE_DIR, "image_app", "static", "images", param)

        f = open(file_path, 'rb')
        return HttpResponse(content=f, content_type=get_content_type(file_path))

    def get_content_type(file_path):
        # Use mimetypes module to determine the MIME type based on file extension
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or 'text/plain'
```

The `fetch_image` function looks odd. The logic entails the application to accept a filename parameter and **dangerously** attempts to concatenate the filename with local base directory via `os.path.join(settings.BASE_DIR, "image_app", "static", "images",`

The direct concatenation of the filepath as a string results in the path traversal vulnerability!

## The End

We have successfully detected and exploited a path traversal attack! We have also figured out where the application went wrong.

LEt us head on to the **defense** subject to secure this vulnerable application

## References

- <https://owasp.org/www-community/attacks/Path_Traversal>
