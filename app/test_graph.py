from app.graph.workflow import app_graph


print("Starting Blue Data")
print()

question = input("Enter your question: ")

print()
print(f"User question: {question}")
print()

result = app_graph.invoke({
    "user_input": question,
    "intent": "",
    "response": "",
})

print()
print("✅ Graph executed")

print("\n==============================")
print("FINAL RESULT")
print("==============================")
print(result)
