document.addEventListener("DOMContentLoaded", function () {
    const chatWindow = document.getElementById("chat-window");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");

    // Function to add a new message to the chat
    function addMessage(message, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${sender}-message`; // Change class name based on the sender
        messageDiv.textContent = message;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Function to handle user input and simulate AI response
    function processUserInput() {
        const userMessage = userInput.value.trim();
        if (userMessage === "") return;

        // Add the user message to the chat
        addMessage(userMessage, "user");

        // Simulate AI response (replace this with actual API call if you have a backend)
        const aiResponse = "This is an AI response.";

        // Add AI response to the chat after a short delay to simulate AI processing time
        setTimeout(() => {
            addMessage(aiResponse, "ai");
        }, 800);

        // Clear the input field
        userInput.value = "";
    }

    // Event listener for the send button
    sendButton.addEventListener("click", processUserInput);

    // Event listener for Enter key in the input field
    userInput.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            processUserInput();
        }
    });
});
