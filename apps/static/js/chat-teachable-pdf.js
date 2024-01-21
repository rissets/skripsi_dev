const query = (obj) =>
  Object.keys(obj)
    .map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(obj[k]))
    .join("&");
const markdown = window.markdownit();
const message_box = document.getElementById(`messages`);
const message_input = document.getElementById(`message-input`);

hljs.addPlugin(new CopyButtonPlugin());

const format = (text) => {
  return text.replace(/(?:\r\n|\r|\n)/g, "<br>");
};

const trainPDF = async () => {
  try {
    const selectedPdfId = document.getElementById('pdf-select').value;

    if (selectedPdfId === '0') {
      alert('Please select a PDF before training.');
      return;
    }

    // Show loading overlay
    showLoadingOverlay();

    const response = await fetch(`/api/v2/teachable`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        accept: 'text/event-stream',
      },
      body: JSON.stringify({
        conversation_id: window.conversation_id,
        action: '_ask',
        meta: {
          content: {
            content_type: 'text',
            parts: [
              {
                content: 'test',
                role: 'user',
              },
            ],
            teachable_agent_slug: teachable_agent,
            pdf_id: selectedPdfId,
          },
        },
      }),
    });

    // Hide loading overlay
    hideLoadingOverlay();

    const reader = response.body.getReader();
    console.log(reader);

    // Display success notification

    // Additional code...

  } catch (e) {
    console.log(e);
  }
};

// Function to show loading overlay
const showLoadingOverlay = () => {
  const overlay = document.getElementById('overlay-loading');
  overlay.style.display = 'block';
  setTimeout(() => {
    overlay.style.display = 'none';
    showNotification('Training completed. You will receive an email when the process is finished.');
  }, 10000);

};

// Function to hide loading overlay
const hideLoadingOverlay = () => {
  const overlay = document.getElementById('loading-overlay');
  overlay.style.display = 'none';
};

// Function to display notification
const showNotification = (message) => {
  const notificationBox = document.getElementById('notification-box');
  notificationBox.innerHTML = message;

  // Display notification box (you can customize the styling as needed)
  notificationBox.style.display = 'block';

  // Hide notification after 5 seconds
  setTimeout(() => {
    notificationBox.style.display = 'none';
  }, 10000);
};
