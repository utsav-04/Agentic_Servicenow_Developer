# from graph.workflow import build_graph

# graph = build_graph()

# print("ServiceNow AI Assistant Started")
# print("Type 'exit' to quit\n")

# while True:

#     user_input = input("You: ")

#     if user_input.lower() == "exit":
#         break

#     result = graph.invoke({"input": user_input})

#     print("\nAgent:", result.get("result"))


from graph.workflow import build_graph

graph = build_graph()

def main():
    print("\nServiceNow AI Assistant Started")
    print("Type 'exit' or 'quit' to stop.\n")

    # Maintain conversation state
    state = {}

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Assistant stopped.")
                break

            # Add user input to state
            state["input"] = user_input

            # Invoke LangGraph workflow
            result = graph.invoke(state)

            # Get agent output
            output = result.get("output")

            print(f"\nAgent: {output}\n")

            # Update state for next turn
            state.update(result)

        except KeyboardInterrupt:
            print("\nAssistant stopped.")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()