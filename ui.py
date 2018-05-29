
#----------------------------------------------------------------------------------#
def print_pigeon():
    print("\n         .-''-.")
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
    print("2. List Timeline")
    print("3. List my Timeline")
    print("4. Follow")
    print("5. Unfollow")
    print("0. Exit")

#----------------------------------------------------------------------------------#
def select_action():
    print_options()
    #user_input = input('Insert option: ')
    user_input = input('')
    return int(user_input)

#----------------------------------------------------------------------------------#
def print_timeline(posts):
    for p in posts:
        print('From: %s\nAt: %s\n\t%s\n' %\
             #(p['from'], p['date'].strftime("%y/%m/%d %H:%M:%S"), p['text']))
             (p['from'], p['date'], p['text']))

#----------------------------------------------------------------------------------#
def print_info(msg):
    print('Info\t%s' % (msg))

#----------------------------------------------------------------------------------#
def get_user_input(msg):
    return "pru@pru.pru"
    #return input('%s: ' % (msg))
