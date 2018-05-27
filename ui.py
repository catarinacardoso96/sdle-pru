
#----------------------------------------------------------------------------------#
def print_pigeon():
    print("         .-''-.")
    print("        / ,    \\")
    print("     .-'`(o)    ;")
    print("    '-==.       |")
    print("         `._...-;-.")
    print("          )--\"\"\"   `-.")
    print("         /   .        `-.")
    print("        /   /      `.    `-.")
    print("        |   \\    ;   \\      `-._________")
    print("        |    \\    `.`.;          -------`.")
    print("         \\    `-.   \\\\          `---...|")
    print("          `.     `-. ```\\.--'._   `---...|")
    print("            `-.....7`-.))\\     `-._`-.. /")
    print("              `._\\ /   `-`         `-.,'")
    print("                / /")
    print("               /=(_")
    print("            -./--' `")
    print(" Pru      ,^-(_")
    print("          ,--' `  \n")

#----------------------------------------------------------------------------------#
def print_options():
    print("Choose your option:")
    print("1. Post")
    print("2. Update Timeline")
    print("3. Follow")
    print("4. Unfollow")
    print("0. Exit")

#----------------------------------------------------------------------------------#
def select_action():
    print_options()
    user_input = input('Insert option: ')
    return int(user_input)

#----------------------------------------------------------------------------------#
def print_timeline():
    post = "Pru!"
    print('Your posts: %s' % (post))