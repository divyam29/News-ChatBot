import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import random

def init():
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    print("done")


def main():
    # News headlines list
    news_headlines = [
        "Breaking News: Scientists discover a new species of dinosaur",
        "Technology Update: New smartphone with advanced features released",
        "Sports News: Local team wins championship title",
        "Business Update: Stocks soar to all-time high",
        "Entertainment Buzz: Highly anticipated movie trailer released",
    ]

    exit_words = [
        "goodbye",
        "farewell",
        "bye",
        "adios",
        "later",
        "ciao",
        "cheers",
        "so long",
        "peace",
        "see ya",
        "out",
        "toodles",
        "hasta",
        "sayonara",
        "exit",
        "end",
        "stop",
        "quit",
        "close",
        "finish",
    ]
    goodbye_words = [
        "Farewell, dear friend! Until our next digital encounter.",
        "As my circuits rest, I bid you adieu, and may your days be filled with wonder.",
        "It's time to sign off now. Remember, I'm just a chat away if you need me again.",
        "Wishing you a wonderful day ahead! Goodbye for now.",
        "Stay curious, stay kind, and remember that I'll be here whenever you need a virtual pal. Goodbye!",
        "Thank you for sharing this conversation with me. Until we meet again, take care.",
        "It's been a pleasure chatting with you. Goodbye and keep exploring the vast realms of knowledge.",
        "May the digital winds guide you towards new adventures. Farewell!",
        "Signing off, but never truly gone. I'll be eagerly awaiting our next interaction. Goodbye!",
        "Until our paths cross in the digital realm once more, stay safe and farewell!",
    ]

    # nickname = input("Your nickname: ")
    # print("Chat (ask a question to start a conversation): ")

    cont = True
    response_num = 0

    while cont:
        # Ask bot something
        question = input("{}: ".format("D"))

        # Encode the input
        user_input = tokenizer.encode(question + tokenizer.eos_token, return_tensors="pt")
        print(user_input)
        print(type(user_input))

        ques_lst = question.split()

        # Concatenate the user input with the chat history
        chatbot_input = (
            torch.cat([chat_history, user_input], dim=-1)
            if response_num > 0
            else user_input
        )

        # Generate a response
        chat_history = model.generate(
            chatbot_input,
            max_length=10000000,
            do_sample=True,
            top_k=70,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
        )

        # Print the output
        chat = tokenizer.decode(
            chat_history[:, chatbot_input.shape[-1] :][0], skip_special_tokens=True
        )

        # Check if the response is a news-related query
        if any(word in question.lower() for word in ["news", "update", "headline"]):
            response = "Here are some recent news headlines:\n" + "\n".join(news_headlines)
        elif any(word in exit_words for word in ques_lst):
            cont = False
            response = random.choice(goodbye_words)
        else:
            response = chat

        print(f"Bot: {response}")
        response_num += 1

if __name__ == '__main__':
    init()
    main()