const chat = document.getElementById('chat');
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message');

// Example AI response
const aiResponse = 'This is an example AI response.';

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();

    if (!messageInput.value.trim()) {
        return;
    }

    const message = document.createElement('div');
    message.classList.add('flex', 'justify-between', 'mb-4');
    message.innerHTML = `
      <div class="text-gray-700">
        <span class="font-bold">User:</span> ${messageInput.value}
      </div>
    `;
    chat.appendChild(message);

    // Simulate AI response
    setTimeout(() => {
        const aiMessage = document.createElement('div');
        aiMessage.classList.add('flex', 'justify-between', 'mb-4');
        aiMessage.innerHTML = `
          <div class="text-blue-700">
            <span class="font-bold">AI:</span> ${aiResponse}
          </div>
        `;
        chat.appendChild(aiMessage);

        // Scroll to the bottom of the chat
        chat.scrollTop = chat.scrollHeight;

        // Clear the input field
        messageInput.value = '';
    }, 1000);
});
