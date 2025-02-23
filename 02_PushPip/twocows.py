import cowsay
import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument("-e", "--first_eyes", default="oo")
my_parser.add_argument("-E", "--second_eyes", default="oo")
my_parser.add_argument("-F", "--second_type", default="cow")
my_parser.add_argument("-f", "--first_type", default="cow")
my_parser.add_argument("-N", "--no_wrap", action="store_true")
my_parser.add_argument("msg1")
my_parser.add_argument("msg2")
args = my_parser.parse_args()

if args.first_type in cowsay.list_cows() and args.second_type in cowsay.list_cows():
    first_cow = cowsay.cowsay(message=args.msg1, cow=args.first_type, eyes=args.first_eyes)
    second_cow = cowsay.cowsay(message=args.msg2, cow=args.second_type, eyes=args.second_eyes)
    first_lst = first_cow.split("\n")
    second_lst = second_cow.split("\n")
    if len(first_lst) < len(second_lst):
        first_lst = [""] * (len(second_lst) - len(first_lst)) + first_lst
    else:
        second_lst = [""] * (len(first_lst) - len(second_lst)) + second_lst
    width = max(len(i) for i in first_lst)
    for i in range(len(first_lst)):
        print(first_lst[i].ljust(width), second_lst[i])