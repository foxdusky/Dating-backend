import resend

resend.api_key = "re_3f1x9zRU_P67UMyggCMJR3rVGutCsmo92"

r = resend.Emails.send({
    "from": "dating@resend.dev",
    "to": "mr.dusky.fox@gmail.com",
    "subject": "Hello World",
    "html": "<p>Congrats on sending your <strong>first email</strong>!</p>"
})

