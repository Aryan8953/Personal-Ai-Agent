from screen_context import get_screen_context


question = input(
    "What do you want to know about your screen? "
)

print("\nAnalyzing screen...\n")

context = get_screen_context(question)

print("Screen Context:")
print(context)