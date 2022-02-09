import main as m
filename = "shadow"
(usernames, salt, hashes) = m.extract_info(filename)
(username, password) = m.find_password(usernames, salt, hashes)
m.print_password(username, password)