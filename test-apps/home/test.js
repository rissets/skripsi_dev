document.addEventListener('DOMContentLoaded', () => {
  const messageInput = document.getElementById('message-input');
  const messages = document.getElementById('messages');

  messageInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      const message = event.target.value;
      const messageElement = document.createElement('li');
      messageElement.textContent = message;
      messageElement.classList.add('bg-blue-200', 'p-2', 'rounded');
      messages.appendChild(messageElement);
      event.target.value = '';
    }
  });
});

// Update the function in script.js
messageInput.addEventListener('keydown', (event) => {
 if (event.key === 'Enter') {
    const message = event.target.value;
    const messageElement = document.createElement('li');
    messageElement.textContent = message;
    messageElement.classList.add('bg-blue-200', 'p-2', 'rounded');
    messages.appendChild(messageElement);
    event.target.value = '';

    // Scroll to the bottom of the chat
    messages.scrollTop = messages.scrollHeight;
 }
});