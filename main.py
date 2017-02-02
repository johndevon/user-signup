import webapp2
import re

welcomepage = """
    <head>
        <title> Unit 2 Signup </title>
    </head>

    <body>
        <h2> Welcome, %(username)s!</h2>
    </body>

"""

form = """

<body>
    <h2>Signup</h2>
    <form method="post">
        <table>
            <tr>
                <td class = "label">
                    Username
                </td>
                <td>
                    <input type="text" name="username" value="%(username)s">
                </td>
                <td class="error" style="color: red">
                    %(username_error)s
                </td>
            </tr>
            <tr>
                <td class = "label">
                    Password
                </td>
                <td>
                    <input type="password" name="password" value="">
                </td>
                <td class="error" style="color: red">
                    %(password_error)s
                </td>
            </tr>
            <tr>
                <td class = "label">
                    Verify Password
                </td>
                <td>
                    <input type="password" name="verify" value="">
                </td>
                <td class="error" style="color: red">
                    %(verify_error)s
                </td>
            </tr>
            <tr>
                <td class = "label">
                    Email (optional)
                </td>
                <td>
                    <input type="test" name="email" value="%(email)s">
                </td>
                <td class="error" style="color: red">
                    %(email_error)s
                </td>
            </tr>

        </table>
        <input type="submit" value="Submit"/>

        """

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):

    def write_form(self, username_error="", username="",
    password_error="",  verify_error="", email="", email_error=""):

        self.response.out.write(form % {"username_error":username_error,
                                        "username":username,
                                        "password_error":password_error,
                                        "verify_error": verify_error,
                                        "email": email,
                                        "email_error": email_error
                                         })

    def get(self):
        self.write_form()

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['username_error'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['password_error'] = "That wasn't a valid password"
            have_error = True
        elif password != verify:
            params['verify_error'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['email_error'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.write_form(**params)
        else:
            self.redirect('/Welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def write_form(self, username):
        self.response.out.write(welcomepage % {"username":username} )

    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.write_form(username)
        else:
            self.redirect('/')
app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/Welcome', Welcome)
], debug=True)
