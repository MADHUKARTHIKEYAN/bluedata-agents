from app.graph.workflow import build_graph


graph = build_graph()


initial_state = {
    "user_input": "Where is a good fishing zone?",
    "intent": "",
    "response": "",
}


result = graph.invoke(initial_state)


print("\n==============================")
print("FINAL RESULT")
print("==============================")
print(result)