def extract_info(name_of_file):
    f = open(name_of_file, "r")
    lines = f.read().split()
    f.close()

    # extract username, salts, hashes into lists
    usernames = []
    salts = []
    hashes = []

    for line in lines:
        if "$6" in line:
            sections = line.split("$")  # clean out the entries into expected part
            usernames.append(sections[0].split(":")[0])  # clean out the entries into expected part
            salts.append(sections[2])  # clean out the entries into expected part
            hashes.append(sections[3].split(":")[0])  # clean out the entries into expected part
    return usernames, salts, hashes


def find_password(usernames, salts, hashes):
    # import and test our hash function
    from passlib.hash import sha512_crypt
    # from itertools import permutations

    # We call in the special characters from the string library
    import string
    special_char = string.punctuation
    # May 28 Jax
    # policy: uppercase, lowercase, digit

    decodedusernames = []  # a variable to store usernames with broken password
    decodedpasswords = []  # a variable to store passwords that have been broken
    names = []  # a variable to hold all possible name combinations
    list1 = ["ibiso"]
    # list2 = ["03", "09", "08", "11", "01", "12"]
    # list3 = ["29"]
    # list4 = ["!", "@", "#", "$", "%", "ˆ", "&", "*", ")", "(", "_", "-", "+", "="]
    # iterate through and append all possibilities
    for l1 in list1:
        # for l2 in list2:
        # for l3 in list3:
        names.append(l1)
        print(names)
    # Next, we check for probable permutations
    from itertools import permutations
    for n in names:
        for c in special_char:
            permu = permutations([n, c, "10", "19"], 4)
            for p in list(permu):
                newpass = ''.join(p)
                # Finally, we iterate through our hashes in the shadow file and check for
                # comparisms
                for i in range(len(hashes)):
                    if hashes[1] == sha512_crypt.using(rounds=5000, salt=salts[i]).hash(newpass).split("$")[-1]:
                        decodedusernames.append(usernames[i])
                        decodedpasswords.append(newpass)
                    else:
                        print("Password for " + usernames[i] + " is not: " + newpass)
    return decodedusernames, decodedpasswords


def print_password(decodedusernames, decodedpasswords):
    for p in range(len(decodedusernames)):
        print("Decoded logon:");
        print("############################################################")
        print("Username is: " + decodedusernames[p] + " while Password is: " + decodedpasswords[p]);
        print("############################################################")
    import sys
    sys.exit()

# (usernames, salt, hashes) = extract_info('shadow');
# (username, password) = find_password(usernames, salt, hashes);
# print_password(username, password);
